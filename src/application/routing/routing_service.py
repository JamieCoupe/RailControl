import logging

from src.application.application_enums import RouteMode
from src.application.dto.route_request import RouteRequest
from src.application.dto.route_result import RouteResult
from src.application.routing.routing_edge import RoutingEdge
from src.application.routing.routing_graph import RoutingGraph
from src.application.routing.path_finder import Dijkstra
from src.application.routing.routing_node import RoutingNode
from src.application.utils.scale_conversion import travel_time_seconds
from src.domain.domain_enums import TrackBlockType

logger = logging.getLogger(__name__)


class RoutingService:
    def __init__(self, graph: RoutingGraph):
        self.graph = graph

    # ---------- small helpers ----------

    @staticmethod
    def _normalise_type(value) -> str:
        """
        Normalise enums/strings for reliable comparison.
        Examples:
          - TrackBlockType.MAINLINE -> "MAINLINE"
          - "mainline" -> "MAINLINE"
          - "Passing loop" -> "PASSING_LOOP"
        """
        if value is None:
            return ""
        # Enum instance -> use its name
        if hasattr(value, "name"):
            return value.name.upper()
        # String-ish
        return str(value).upper().replace(" ", "_")

    # ---------- basic route ----------

    def find_route(self, start_junction_id: str, end_junction_id: str) -> RouteResult:
        if not (start_junction_id in self.graph.nodes and end_junction_id in self.graph.nodes):
            raise ValueError("NodeError: start or end junction not in graph")

        finder = Dijkstra(self.graph)
        return finder.find_path(start_junction_id, end_junction_id)

    # ---------- graph cloning ----------

    def clone_graph(self) -> RoutingGraph:
        # Create Empty Graph
        cloned_graph = RoutingGraph()

        # Copy nodes
        for node_id, routing_node in self.graph.nodes.items():
            cloned_graph.nodes[node_id] = RoutingNode(routing_node.id)

        # Copy edges (deep enough for our purposes)
        for node_id, edge_list in self.graph.edges.items():
            cloned_graph.edges[node_id] = []
            for edge in edge_list:
                cloned_graph.edges[node_id].append(
                    RoutingEdge(
                        edge.from_node,
                        edge.to_node,
                        edge.track_section_id,
                        edge.track_block_id,
                        edge.length_mm,
                        edge.max_speed,
                        edge.weight,
                        edge.block_class,
                        edge.block_type,
                    )
                )

        return cloned_graph

    # ---------- advanced route with request ----------

    def find_route_by_request(self, route_request: RouteRequest) -> RouteResult:
        logger.info(
            "Routing request %s -> %s, mode=%s",
            route_request.start_id,
            route_request.end_id,
            route_request.routing_mode,
        )

        # 1) Start from a cloned graph so we don't mutate the main one
        filtered_graph = self.clone_graph()

        # Helper to count edges for debug
        def count_edges(graph: RoutingGraph) -> int:
            return sum(len(v) for v in graph.edges.values())

        logger.debug("Initial edge count: %d", count_edges(filtered_graph))

        # 2) Apply "avoid specific blocks"
        if route_request.avoid_blocks:
            avoid_blocks = set(route_request.avoid_blocks)
            for node_id in filtered_graph.edges:
                new_edge_list = []
                for edge in filtered_graph.edges[node_id]:
                    if edge.track_block_id not in avoid_blocks:
                        new_edge_list.append(edge)
                filtered_graph.edges[node_id] = new_edge_list

            logger.debug(
                "After avoid_blocks filter (%s), edge count: %d",
                avoid_blocks,
                count_edges(filtered_graph),
            )

        # 3) Apply "avoid block types"
        if route_request.avoid_block_types:
            avoid_types = {self._normalise_type(t) for t in route_request.avoid_block_types}
            for node_id in filtered_graph.edges:
                new_edge_list = []
                for edge in filtered_graph.edges[node_id]:
                    edge_type_norm = self._normalise_type(edge.block_type)
                    if edge_type_norm not in avoid_types:
                        new_edge_list.append(edge)
                filtered_graph.edges[node_id] = new_edge_list

            logger.debug(
                "After avoid_block_types filter (%s), edge count: %d",
                avoid_types,
                count_edges(filtered_graph),
            )

        # 4) Exclude platforms if requested
        if not route_request.include_platforms:
            for node_id in filtered_graph.edges:
                new_edge_list = []
                for edge in filtered_graph.edges[node_id]:
                    klass_norm = self._normalise_type(edge.block_class)
                    if klass_norm != "PLATFORM":
                        new_edge_list.append(edge)
                filtered_graph.edges[node_id] = new_edge_list

            logger.debug(
                "After include_platforms=False filter, edge count: %d",
                count_edges(filtered_graph),
            )

        # 5) Cap max speed if specified (recalculate time-based weight)
        if route_request.max_train_speed:
            max_speed = route_request.max_train_speed
            for node_id in filtered_graph.edges:
                for edge in filtered_graph.edges[node_id]:
                    if edge.max_speed > max_speed:
                        edge.max_speed = max_speed
                    # Recalculate travel time-based weight (for FASTEST mode)
                    edge.weight = travel_time_seconds(edge.length_mm, edge.max_speed)

            logger.debug(
                "After max_train_speed=%s adjustment, edge count: %d",
                max_speed,
                count_edges(filtered_graph),
            )

        # 6) Apply routing mode (FASTEST, SHORTEST, MAINLINE_ONLY, etc.)
        mode = route_request.routing_mode
        if mode is not None:
            for node_id in list(filtered_graph.edges.keys()):
                edge_list = filtered_graph.edges[node_id]
                new_edge_list: list[RoutingEdge] = []

                for edge in edge_list:
                    block_type_norm = self._normalise_type(edge.block_type)
                    block_class_norm = self._normalise_type(edge.block_class)

                    if mode == RouteMode.FASTEST:
                        # Weight is already travel time (ensured above / in topology)
                        new_edge_list.append(edge)

                    elif mode == RouteMode.SHORTEST:
                        # Weight = physical length
                        edge.weight = edge.length_mm
                        new_edge_list.append(edge)

                    elif mode == RouteMode.MAINLINE_ONLY:
                        # Allow MAINLINE and PASSING_LOOP (for realistic operations)
                        allowed_types = {"MAINLINE", "PASSING_LOOP"}
                        if block_type_norm in allowed_types:
                            new_edge_list.append(edge)
                        # else: drop the edge

                    elif mode == RouteMode.AVOID_INDUSTRY:
                        # Drop edges whose block_class is INDUSTRY
                        if block_class_norm != "INDUSTRY":
                            new_edge_list.append(edge)

                    elif mode == RouteMode.CUSTOM_WEIGHT:
                        # We'll implement this later
                        raise NotImplementedError("CUSTOM_WEIGHT mode is not implemented yet")

                filtered_graph.edges[node_id] = new_edge_list

            logger.debug(
                "After routing_mode=%s filter, edge count: %d",
                mode,
                count_edges(filtered_graph),
            )

        # 7) Allow reverse moves or not
        if not route_request.allow_reverse:
            for node_id in list(filtered_graph.edges.keys()):
                edge_list = filtered_graph.edges[node_id]
                new_edge_list: list[RoutingEdge] = []

                for edge in edge_list:
                    # A reverse edge is one where an edge exists with same section_id
                    # and opposite direction. We arbitrarily drop the "reverse" one
                    # based on from/to for now.
                    is_reverse = False

                    for candidate in filtered_graph.edges.get(edge.to_node, []):
                        if (
                            candidate.track_section_id == edge.track_section_id
                            and candidate.from_node == edge.to_node
                            and candidate.to_node == edge.from_node
                        ):
                            # Here we decide that one direction is "primary" and one is "reverse".
                            # We'll treat the edge whose from_node has a "higher" id as reverse.
                            if edge.from_node > candidate.from_node:
                                is_reverse = True
                            break

                    if not is_reverse:
                        new_edge_list.append(edge)

                filtered_graph.edges[node_id] = new_edge_list

            logger.debug(
                "After allow_reverse=False filter, edge count: %d",
                count_edges(filtered_graph),
            )

        # 8) Apply preferred block types (small weight discount)
        if route_request.prefer_block_types:
            preferred = {self._normalise_type(t) for t in route_request.prefer_block_types}
            for node_id in filtered_graph.edges:
                for edge in filtered_graph.edges[node_id]:
                    block_type_norm = self._normalise_type(edge.block_type)
                    if block_type_norm in preferred:
                        edge.weight *= 0.5  # strong reward
                    else:
                        edge.weight *= 2.0  # strong penalty

            logger.debug(
                "After prefer_block_types=%s adjustment, edge count: %d",
                preferred,
                count_edges(filtered_graph),
            )

        # 9) Run Dijkstra on the filtered graph
        finder = Dijkstra(filtered_graph)
        return finder.find_path(route_request.start_id, route_request.end_id)

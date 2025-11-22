from src.application.application_enums import RouteMode
from src.application.dto.route_request import RouteRequest
from src.application.dto.route_result import RouteResult
from src.application.routing.routing_edge import RoutingEdge
from src.application.routing.routing_graph import RoutingGraph
from src.application.routing.path_finder import Dijkstra
from src.application.routing.routing_node import RoutingNode
from src.application.utils.scale_conversion import travel_time_seconds
from src.domain.domain_enums import TrackBlockType


class RoutingService:
    def __init__(self, graph: RoutingGraph):
        self.graph = graph

    def find_route(self, start_junction_id: str, end_junction_id: str) -> RouteResult:
        if not (start_junction_id in self.graph.nodes and end_junction_id in self.graph.nodes):
            raise "NodeError"

        finder = Dijkstra(self.graph)
        return finder.find_path(start_junction_id, end_junction_id)

    def clone_graph(self) -> RoutingGraph:
        # Create Empty Graph
        cloned_graph = RoutingGraph()

        # Iterate through existing nodes and create a new one foreach
        for node_id, routing_node in self.graph.nodes.items():
            cloned_graph.nodes[node_id] = RoutingNode(routing_node.id)

        # For each edge create a new one
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
                        edge.block_type
                    )
                )

        return cloned_graph

    def find_route_by_request(self, route_request: RouteRequest):
        #Create clone of graph
        filtered_graph = self.clone_graph()

        #Apply filter for avoid blocks
        if route_request.avoid_blocks:
            for node_id in filtered_graph.edges:
                new_edge_list = []
                for edge in filtered_graph.edges[node_id]:
                    if edge.track_block_id not in route_request.avoid_blocks:
                        new_edge_list.append(edge)

                filtered_graph.edges[node_id] = new_edge_list

        #Apply the filter for any avoid block_types
        if route_request.avoid_block_types:
            for node_id in filtered_graph.edges:
                new_edge_list = []
                for edge in filtered_graph.edges[node_id]:
                    if edge.block_type not in route_request.avoid_block_types:
                        new_edge_list.append(edge)

                filtered_graph.edges[node_id] = new_edge_list

        #Apply platforms or not
        if not route_request.include_platforms:
            for node_id in filtered_graph.edges:
                new_edge_list = []
                for edge in filtered_graph.edges[node_id]:
                    if edge.block_class != "PLATFORM":
                        new_edge_list.append(edge)

                filtered_graph.edges[node_id] = new_edge_list

        #Apply max speed adjustment
        if route_request.max_train_speed:
            for node_id in filtered_graph.edges:
                new_edge_list = []
                for edge in filtered_graph.edges[node_id]:
                    if edge.max_speed > route_request.max_train_speed:
                        edge.max_speed = route_request.max_train_speed
                        edge.weight = travel_time_seconds(edge.length_mm, edge.max_speed)
                        new_edge_list.append(edge)
                    else:
                        new_edge_list.append(edge)

                filtered_graph.edges[node_id] = new_edge_list

        #Apply routing Mode adjustment
        if route_request.routing_mode:
            for node_id in filtered_graph.edges:
                new_edge_list = []
                for edge in filtered_graph.edges[node_id]:
                    match route_request.routing_mode:
                        case RouteMode.FASTEST:
                            #Default based on travel time weight
                            edge.weight = travel_time_seconds(edge.length_mm, edge.max_speed)
                            new_edge_list.append(edge)
                        case RouteMode.SHORTEST:
                            #Switch to length as the weight
                            edge.weight = edge.length_mm
                            new_edge_list.append(edge)
                        case RouteMode.MAINLINE_ONLY:
                            #Remove anything that is not a mainline
                            allowed_types = [TrackBlockType.MAINLINE.name, TrackBlockType.PASSING_LOOP.name]
                            if edge.block_type in allowed_types:
                                new_edge_list.append(edge)
                            else:
                                continue
                        case RouteMode.AVOID_INDUSTRY:
                            # Remove anything that is industry
                            if edge.block_class != "INDUSTRY":
                                new_edge_list.append(edge)
                            else:
                                continue

                        case RouteMode.CUSTOM_WEIGHT:
                            raise NotImplementedError("CUSTOM_WEIGHT mode is not implemented yet")


                filtered_graph.edges[node_id] = new_edge_list

        # Allow reverse moves or not
        if not route_request.allow_reverse:
            for node_id in list(filtered_graph.edges.keys()):
                new_edge_list = []

                for edge in filtered_graph.edges[node_id]:
                    # A reverse edge is one where the opposite direction exists
                    is_reverse = False

                    for candidate in filtered_graph.edges.get(edge.to_node, []):
                        if (
                                candidate.track_section_id == edge.track_section_id
                                and candidate.from_node == edge.to_node
                                and candidate.to_node == edge.from_node
                        ):
                            # If we are at the reverse direction, mark it
                            if node_id == edge.to_node:
                                is_reverse = True
                                break

                    if not is_reverse:
                        new_edge_list.append(edge)

                filtered_graph.edges[node_id] = new_edge_list

        #Apply preferred block type adjustment
        if route_request.prefer_block_types:
            for node_id in filtered_graph.edges:
                for edge in filtered_graph.edges[node_id]:
                    if edge.block_type in route_request.prefer_block_types:
                        edge.weight = edge.weight * 0.8

        #Put new graph in Dijkstra and return
        finder = Dijkstra(filtered_graph)
        return finder.find_path(route_request.start_id, route_request.end_id)

        pass
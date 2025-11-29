import logging
from railcontrol.application.dto.route_result import RouteResult
from railcontrol.application.routing.routing_graph import RoutingGraph

logger = logging.getLogger(__name__)


class Dijkstra:
    def __init__(self, graph: RoutingGraph):
        self.graph = graph

    def find_path(self, start: str, end: str) -> RouteResult:
        logger.debug(f"Running Dijkstra from {start} to {end}")

        nodes = self.graph.nodes
        edges = self.graph.edges

        distance_table = {nid: float("inf") for nid in nodes}
        previous_table = {nid: None for nid in nodes}
        unvisited_set = set(nodes.keys())

        distance_table[start] = 0

        while unvisited_set:
            current = min(unvisited_set, key=lambda nid: distance_table[nid])

            if current == end:
                logger.debug("Destination reached — stopping early")
                break

            for edge in edges[current]:
                neighbour = edge.to_node

                if neighbour not in unvisited_set:
                    continue

                new_dist = distance_table[current] + edge.weight

                if new_dist < distance_table[neighbour]:
                    distance_table[neighbour] = new_dist
                    previous_table[neighbour] = current
                    logger.debug(f"Updated {neighbour}: dist={new_dist}, prev={current}")

            unvisited_set.remove(current)

        if previous_table[end] is None and start != end:
            logger.warning("No route found")
            return RouteResult([], [], 0, 0, [], success=False, message="Failed to Find Route")

        # Reconstruct path
        path_nodes = []
        node = end
        while node is not None:
            path_nodes.append(node)
            node = previous_table[node]
        path_nodes.reverse()

        # Calculate stats
        total_time = 0
        total_len = 0
        blocks = []
        edge_ids = []

        for i in range(len(path_nodes) - 1):
            cur = path_nodes[i]
            nxt = path_nodes[i + 1]

            for edge in edges[cur]:
                if edge.to_node == nxt:
                    total_time += edge.weight
                    total_len += edge.length_mm
                    blocks.append(edge.track_block_id)
                    edge_ids.append(edge.track_section_id)
                    break

        logger.debug(f"Dijkstra returned path: {path_nodes}, time={total_time}, length={total_len}")

        return RouteResult(
            path_nodes,
            edge_ids,
            total_time,
            total_len,
            blocks,
            success=True
        )

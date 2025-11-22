from src.application.dto.route_result import RouteResult
from src.application.routing.routing_graph import RoutingGraph


class Dijkstra:
    def __init__(self, graph: RoutingGraph):
        self.graph = graph

    def find_path(self, start: str, end:str) -> RouteResult:
        # Initilise for dijkstra
        nodes = self.graph.nodes
        edges = self.graph.edges

        distance_table = {node_id: float("inf") for node_id in nodes}
        previous_table =  {node_id: None for node_id in nodes}
        unvisited_set = set(nodes.keys())
        distance_table[start] = 0
        assert start in unvisited_set

        # Start the path finding
        while unvisited_set:
            current_node = min(unvisited_set, key=lambda node_id: distance_table[node_id])

            if current_node == end:
                break

            for edge in edges[current_node]:
                neighbour = edge.to_node

                if neighbour not in unvisited_set:
                    continue

                new_distance = distance_table[current_node] + edge.weight

                if new_distance < distance_table[neighbour]:
                    distance_table[neighbour] = new_distance
                    previous_table[neighbour] = current_node

            # mark the current node as visited (remove from unvisited set)
            unvisited_set.remove(current_node)

        # stop when you reach the destination or when no reachable nodes remain
        if previous_table[end] is None and start != end:
            return RouteResult([],[],0,0,[],success=False, message="Failed to Find Route")


        # reconstruct path by following previous[] backwards from end → start
        path_nodes = []
        node = end
        while node is not None:
            path_nodes.append(node)
            node = previous_table[node]
        path_nodes.reverse()

        total_time_seconds = 0
        total_length_mm = 0
        blocks = []
        edge_ids = []

        for i in range(0,len(path_nodes) -1):
            current_node = path_nodes[i]
            next_node = path_nodes[i+1]

            for edge in edges[current_node]:
                if edge.to_node == next_node:
                    total_time_seconds += edge.weight
                    total_length_mm += edge.length_mm
                    blocks.append(edge.track_block_id)
                    edge_ids.append(edge.track_section_id)
                    break

        return RouteResult(path_nodes,edge_ids,total_time_seconds,total_length_mm,blocks,success=True)
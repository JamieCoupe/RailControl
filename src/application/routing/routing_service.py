from src.application.dto.route_result import RouteResult
from src.application.routing.routing_graph import RoutingGraph
from src.application.routing.path_finder import Dijkstra


class RoutingService:
    def __init__(self, graph: RoutingGraph):
        self.graph = graph

    def find_route(self, start_junction_id: str, end_junction_id: str) -> RouteResult:
        if not (start_junction_id in self.graph.nodes and end_junction_id in self.graph.nodes):
            raise "NodeError"

        finder = Dijkstra(self.graph)
        return finder.find_path(start_junction_id, end_junction_id)

    def find_route_between_blocks(self, origin_id: str, destination_id: str):
        pass

    def find_route_fast(self, origin_id: str, destination_id: str):
        pass

    def find_route_with_options(self, route_request):
        pass
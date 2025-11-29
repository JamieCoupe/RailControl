from railcontrol.application.routing.routing_node import RoutingNode
from railcontrol.application.routing.routing_edge import RoutingEdge


class RoutingGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}

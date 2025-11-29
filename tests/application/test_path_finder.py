from railcontrol.application.routing.path_finder import Dijkstra
from railcontrol.application.routing.routing_graph import RoutingGraph
from railcontrol.application.routing.routing_node import RoutingNode
from railcontrol.application.routing.routing_edge import RoutingEdge

def build_manual_test_graph():
    graph = RoutingGraph()

    # --- Create Nodes ---
    graph.nodes["J1"] = RoutingNode("J1")
    graph.nodes["J2"] = RoutingNode("J2")
    graph.nodes["J3"] = RoutingNode("J3")

    # --- Initialise adjacency lists ---
    graph.edges["J1"] = []
    graph.edges["J2"] = []
    graph.edges["J3"] = []

    # --- Create Edges ---
    # J1 -> J2 (1 sec)
    edge_J1_J2 = RoutingEdge(
        "J1", "J2",
        "S1", "B1",
        1000, 100,
        1.0,
        "NORMAL", "MAINLINE"
    )

    # J2 -> J3 (1 sec)
    edge_J2_J3 = RoutingEdge(
        "J2", "J3",
        "S2", "B1",
        1000, 100,
        1.0,
        "NORMAL", "MAINLINE"
    )

    # J1 -> J3 (5 sec)
    edge_J1_J3 = RoutingEdge(
        "J1", "J3",
        "S3", "B1",
        1000, 100,
        5.0,
        "NORMAL", "MAINLINE"
    )

    # --- Insert edges ---
    graph.edges["J1"].append(edge_J1_J2)
    graph.edges["J2"].append(edge_J2_J3)
    graph.edges["J1"].append(edge_J1_J3)

    return graph

def test_dijkstra_finder_1_edge():
    graph = build_manual_test_graph()
    finder = Dijkstra(graph)
    result = finder.find_path("J1", "J2")

    assert result.success
    assert result.node_ids == ['J1', 'J2']
    assert result.total_time_seconds == 1.0
    assert len(result.edge_ids) == 1

def test_dijkstra_finder_2_edge():
    graph = build_manual_test_graph()
    finder = Dijkstra(graph)
    result = finder.find_path("J1", "J3")

    assert result.success
    assert result.node_ids == ['J1', 'J2', 'J3']
    assert result.total_time_seconds == 2.0
    assert len(result.edge_ids) == 2

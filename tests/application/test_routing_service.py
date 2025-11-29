from src.application.application_enums import RouteMode
from src.application.dto.route_request import RouteRequest
from src.application.routing.path_finder import Dijkstra
from src.application.routing.routing_graph import RoutingGraph
from src.application.routing.routing_node import RoutingNode
from src.application.routing.routing_edge import RoutingEdge
from src.application.routing.routing_service import RoutingService


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

def build_manual_graph_with_passing_loop():
    """
    Builds a minimal graph:
        J1 --(MAINLINE)--> J2 --(PASSING_LOOP)--> J3
    And includes reverse edges too (for realism).
    """

    from src.application.routing.routing_graph import RoutingGraph
    from src.application.routing.routing_node import RoutingNode
    from src.application.routing.routing_edge import RoutingEdge
    from src.domain.domain_enums import TrackBlockType

    graph = RoutingGraph()

    # --- Create Nodes ---
    graph.nodes = {
        "J1": RoutingNode("J1"),
        "J2": RoutingNode("J2"),
        "J3": RoutingNode("J3"),
    }

    # Prepare empty adjacency lists
    graph.edges = {
        "J1": [],
        "J2": [],
        "J3": [],
    }

    # --- Edge S1: J1 → J2 (MAINLINE) ---
    edge_S1_fwd = RoutingEdge(
        from_node="J1",
        to_node="J2",
        track_section_id="S1",
        track_block_id="B_MAIN",
        length_mm=1000,
        max_speed=100,
        weight=1.0,
        block_class="NORMAL",
        block_type=TrackBlockType.MAINLINE.name,
    )

    edge_S1_rev = RoutingEdge(
        from_node="J2",
        to_node="J1",
        track_section_id="S1",
        track_block_id="B_MAIN",
        length_mm=1000,
        max_speed=100,
        weight=1.0,
        block_class="NORMAL",
        block_type=TrackBlockType.MAINLINE.name,
    )

    graph.edges["J1"].append(edge_S1_fwd)
    graph.edges["J2"].append(edge_S1_rev)

    # --- Edge S2: J2 → J3 (PASSING_LOOP) ---
    edge_S2_fwd = RoutingEdge(
        from_node="J2",
        to_node="J3",
        track_section_id="S2",
        track_block_id="B_LOOP",
        length_mm=800,
        max_speed=80,
        weight=1.0,
        block_class="NORMAL",
        block_type=TrackBlockType.PASSING_LOOP.name,
    )

    edge_S2_rev = RoutingEdge(
        from_node="J3",
        to_node="J2",
        track_section_id="S2",
        track_block_id="B_LOOP",
        length_mm=800,
        max_speed=80,
        weight=1.0,
        block_class="NORMAL",
        block_type=TrackBlockType.PASSING_LOOP.name,
    )

    graph.edges["J2"].append(edge_S2_fwd)
    graph.edges["J3"].append(edge_S2_rev)

    return graph


def test_routing_service_2_junctions():
    graph = build_manual_test_graph()
    routing_service = RoutingService(graph)
    result = routing_service.find_route("J1", "J2")

    assert result.success
    assert result.node_ids == ['J1', 'J2']
    assert result.total_time_seconds == 1.0
    assert len(result.edge_ids) == 1

def test_clone_graph_valid_clone():
    graph = build_manual_test_graph()
    routing_service =  RoutingService(graph)
    cloned_graph = routing_service.clone_graph()

    assert len(graph.nodes) == len(cloned_graph.nodes)
    assert len(graph.edges) == len(cloned_graph.nodes)
    assert list(cloned_graph.nodes.keys()) == ["J1", "J2", "J3"]

def test_clone_graph_is_deep_copy():
    graph = build_manual_test_graph()
    routing_service =  RoutingService(graph)
    cloned_graph = routing_service.clone_graph()

    cloned_graph.edges["J1"][0].weight = 10

    assert graph.edges['J1'][0].weight == 1
    assert cloned_graph.edges["J1"][0].weight == 10

def test_clone_graph_node_objects_independant():
    graph = build_manual_test_graph()
    routing_service =  RoutingService(graph)
    cloned_graph = routing_service.clone_graph()

    cloned_graph.nodes['J4'] = RoutingNode('J4')
    assert len(graph.nodes) == 3 and len(cloned_graph.nodes) ==4

def test_avoid_specific_block():
    graph = build_manual_test_graph()
    service = RoutingService(graph)

    # avoid B1 → removes all edges using block B1
    req = RouteRequest(
        start_id="J1",
        end_id="J2",
        routing_mode=RouteMode.FASTEST,
        avoid_blocks=["B1"]
    )

    result = service.find_route_by_request(req)
    assert not result.success

def test_avoid_block_types():
    graph = build_manual_test_graph()
    service = RoutingService(graph)

    req = RouteRequest(
        start_id="J1",
        end_id="J2",
        routing_mode=RouteMode.FASTEST,
        avoid_block_types=["MAINLINE"]
    )

    result = service.find_route_by_request(req)
    assert not result.success
def test_exclude_platforms():
    graph = build_manual_test_graph()

    # convert J1→J2 block_class into PLATFORM
    for edge in graph.edges["J1"]:
        if edge.to_node == "J2":
            edge.block_class = "PLATFORM"
    for edge in graph.edges["J2"]:
        if edge.to_node == "J1":
            edge.block_class = "PLATFORM"

    service = RoutingService(graph)

    req = RouteRequest(
        start_id="J1",
        end_id="J2",
        include_platforms=False,
        routing_mode=RouteMode.FASTEST,
    )

    result = service.find_route_by_request(req)
    assert not result.success

def test_no_reverse_moves():
    graph = build_manual_test_graph()
    service = RoutingService(graph)

    req = RouteRequest(
        start_id="J2",
        end_id="J1",
        allow_reverse=False,
        routing_mode=RouteMode.FASTEST
    )

    result = service.find_route_by_request(req)
    assert not result.success

def test_max_speed_cap():
    graph = build_manual_test_graph()
    service = RoutingService(graph)

    req = RouteRequest(
        start_id="J1",
        end_id="J2",
        max_train_speed=50,
        routing_mode=RouteMode.FASTEST
    )

    result = service.find_route_by_request(req)
    assert result.success
    assert result.total_time_seconds > 1.0  # slower than original

def test_shortest_mode():
    graph = build_manual_test_graph()
    service = RoutingService(graph)

    req = RouteRequest(
        start_id="J1",
        end_id="J2",
        routing_mode=RouteMode.SHORTEST
    )

    result = service.find_route_by_request(req)
    assert result.success
    assert result.node_ids == ["J1", "J2"]

def test_prefer_block_type():
    graph = build_manual_test_graph()
    service = RoutingService(graph)

    # Make J1→J3 a MAINLINE and J1→J2 NOT MAINLINE
    for edge in graph.edges["J1"]:
        if edge.to_node == "J2":
            edge.block_type = "BRANCH"
        if edge.to_node == "J3":
            edge.block_type = "MAINLINE"

    req = RouteRequest(
        start_id="J1",
        end_id="J3",
        prefer_block_types=["MAINLINE"],
        routing_mode=RouteMode.FASTEST
    )

    result = service.find_route_by_request(req)
    assert result.success
    assert result.node_ids == ["J1", "J3"]

def test_mainline_only():
    graph = build_manual_test_graph()
    service = RoutingService(graph)

    # Mark J1→J2 as BRANCH (so it should be removed)
    for edge in graph.edges["J1"]:
        if edge.to_node == "J2":
            edge.block_type = "BRANCH"

    req = RouteRequest(
        start_id="J1",
        end_id="J2",
        routing_mode=RouteMode.MAINLINE_ONLY
    )

    result = service.find_route_by_request(req)
    assert not result.success

def test_avoid_industry():
    graph = build_manual_test_graph()
    service = RoutingService(graph)

    # Mark the J1→J2 block as INDUSTRY
    for edge in graph.edges["J1"]:
        if edge.to_node == "J2":
            edge.block_class = "INDUSTRY"

    req = RouteRequest(
        start_id="J1",
        end_id="J2",
        routing_mode=RouteMode.AVOID_INDUSTRY
    )

    result = service.find_route_by_request(req)
    assert not result.success

def test_mainline_only_allows_passing_loops():
    """
    MAINLINE_ONLY should still allow PASSING_LOOP block types.
    This ensures operational realism: passing loops are part of the mainline flow.
    """

    # Build a graph where J1 -> J2 is MAINLINE
    # and J2 -> J3 is PASSING_LOOP.
    graph = build_manual_graph_with_passing_loop()

    service = RoutingService(graph)

    req = RouteRequest(
        start_id="J1",
        end_id="J3",
        routing_mode=RouteMode.MAINLINE_ONLY,
        avoid_blocks=[],
        avoid_block_types=[],
        prefer_block_types=[],
        max_train_speed=None,
        allow_reverse=False,
        include_platforms=True,
    )

    result = service.find_route_by_request(req)

    assert result.success
    assert result.node_ids == ["J1", "J2", "J3"]
    assert "B_LOOP" in result.block_ids

    def test_routing_fails_when_turnout_blocks_path():

        graph = build_manual_test_graph()
        service = RoutingService(graph)

        result = service.find_route("J1", "J3")  # only reachable via diverging
        assert not result.success
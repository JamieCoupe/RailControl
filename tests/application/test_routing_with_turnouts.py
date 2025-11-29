from src.application.routing.routing_service import RoutingService
from src.application.topology.topology_builder import TopologyBuilder
from src.domain.domain_enums import TurnoutState

from tests.helpers.repositories import (
    StubJunctionRepository,
    StubTrackSectionRepository,
    StubTrackBlockRepository,
    StubTurnoutRepository
)


def test_routing_fails_when_turnout_blocks_path():
    """
    If the only path from J1 -> J3 is via the diverging section S2,
    and the turnout is in STRAIGHT (thus blocking S2),
    then routing must fail.
    """
    topology = TopologyBuilder(
        StubJunctionRepository(),
        StubTrackSectionRepository(),
        StubTrackBlockRepository(),
        StubTurnoutRepository(state=TurnoutState.STRAIGHT)
    )

    graph = topology.build_graph()
    service = RoutingService(graph)

    result = service.find_route("J1", "J3")

    assert not result.success, "Routing should fail because diverging leg is filtered out"

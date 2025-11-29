from src.domain.domain_enums import JunctionType, TrackBlockType, TurnoutType, TurnoutState, TrackBlockClass
from src.domain.track.junction import Junction
from src.application.topology.topology_builder import TopologyBuilder
from src.domain.track.track_block import TrackBlock
from src.domain.track.track_section import TrackSection
from src.domain.track.turnout import Turnout


#Setup
class JunctionRepository:
    def get_all(self):
        return [
            Junction("J1", "One", JunctionType.STANDARD),
            Junction("J2", "Two", JunctionType.STANDARD),
            Junction("J3", "Three", JunctionType.STANDARD),
        ]

class TrackSectionRepository:
    def get_all(self):
        return [
            TrackSection("S1","B1","J1","J2",1000,125),
            TrackSection("S2", "B2", "J1", "J3", 800, 100),
        ]

class TrackBlockRepository:
    def get(self,id):
        return TrackBlock("B1","TestBlockOne",TrackBlockType.MAINLINE, TrackBlockClass.MAINLINE)

class TurnoutRepository:
    def __init__(self, state):
        self.state = state

    def get_all(self):
        return [
            Turnout(
                id="T1",
                name="Test Turnout",
                turnout_type=TurnoutType.STANDARD_LEFT,
                straight_section_id="S1",
                diverging_section_id="S2",
                current_state=self.state
            )
        ]

class TrackSectionRepositoryUnrelated:
    def get_all(self):
        return [
            TrackSection("S3", "B3", "J2", "J3", 1200, 100),   # unrelated
            TrackSection("S4", "B4", "J1", "J2", 900, 90),     # unrelated
        ]

class TurnoutRepositoryUnused:
    def get_all(self):
        return [
            Turnout(
                id="T1",
                name="Turnout",
                turnout_type=TurnoutType.STANDARD_RIGHT,
                straight_section_id="S1",    # not present
                diverging_section_id="S2",   # not present
                current_state=TurnoutState.STRAIGHT
            )
        ]


#Tests
def test_graph_has_correct_nodes():
    topology_builder = TopologyBuilder(JunctionRepository(), TrackSectionRepository(), TrackBlockRepository(), TurnoutRepository(TurnoutState.STRAIGHT))
    graph = topology_builder.build_graph()
    assert len(graph.nodes) == 3
    assert "J1" in graph.nodes
    assert "J2" in graph.nodes

def test_graph_has_correct_edge():
    topology_builder = TopologyBuilder(JunctionRepository(), TrackSectionRepository(), TrackBlockRepository(), TurnoutRepository(TurnoutState.STRAIGHT))
    graph = topology_builder.build_graph()
    assert len(graph.edges) == 3
    assert len(graph.edges["J1"]) ==1
    assert len(graph.edges["J2"]) == 1

    edge = graph.edges["J1"][0]
    assert edge.track_section_id == "S1"
    assert edge.from_node == "J1"
    assert edge.to_node == "J2"
    assert edge.block_class == "NORMAL"
    assert edge.block_type == "MAINLINE"

    rev = graph.edges["J2"][0]
    assert rev.track_section_id == "S1"
    assert rev.from_node == "J2"
    assert rev.to_node == "J1"

    assert 2.5 < edge.weight < 3


#Turnouts are filtered correctly
def test_turnout_filters_straight_when_diverging():
    topology = TopologyBuilder(
        JunctionRepository(),
        TrackSectionRepository(),
        TrackBlockRepository(),
        TurnoutRepository(TurnoutState.DIVERGING)
    )

    graph = topology.build_graph()

    # J1 should only have an edge to J3 (the diverging route)
    assert len(graph.edges["J1"]) == 1
    assert graph.edges["J1"][0].to_node == "J3"

    # Ensure J1→J2 has been filtered out
    assert all(edge.to_node != "J2" for edge in graph.edges["J1"])

def test_turnout_filters_diverging_when_straight():
    topology = TopologyBuilder(
        JunctionRepository(),
        TrackSectionRepository(),
        TrackBlockRepository(),
        TurnoutRepository(TurnoutState.STRAIGHT)
    )

    graph = topology.build_graph()

    # J1 should only have an edge to J3 (the diverging route)
    assert len(graph.edges["J1"]) == 1
    assert graph.edges["J1"][0].to_node == "J2"

    # Ensure J1→J2 has been filtered out
    assert all(edge.to_node != "J3" for edge in graph.edges["J1"])


def test_turnout_does_not_affect_unrelated_sections():
    topology = TopologyBuilder(
        JunctionRepository(),
        TrackSectionRepositoryUnrelated(),
        TrackBlockRepository(),
        TurnoutRepositoryUnused()
    )
    graph = topology.build_graph()

    # All edges should remain untouched
    assert len(graph.edges["J1"]) == 1
    assert len(graph.edges["J2"]) == 2
    assert len(graph.edges["J3"]) == 1
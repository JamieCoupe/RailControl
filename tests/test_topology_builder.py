from src.domain.domain_enums import JunctionType, TrackBlockType
from src.domain.track.junction import Junction
from src.application.topology.topology_builder import TopologyBuilder
from src.domain.track.track_block import TrackBlock
from src.domain.track.track_section import TrackSection


class JunctionRepository:
    def get_all(self):
        return [
            Junction("J1", "One", JunctionType.PLAIN),
            Junction("J2", "Two", JunctionType.PLAIN),
        ]

class TrackSectionRepository:
    def get_all(self):
        return [
            TrackSection("S1","B1","J1","J2",1000,125)
        ]

class TrackBlockRepository:
    def get(self,id):
        return TrackBlock("B1","TestBlockOne",TrackBlockType.MAINLINE)


def test_graph_has_correct_nodes():
    topology_builder = TopologyBuilder(JunctionRepository(), TrackSectionRepository(), TrackBlockRepository())
    graph = topology_builder.build_graph()
    assert len(graph.nodes) == 2
    assert "J1" in graph.nodes
    assert "J2" in graph.nodes

def test_graph_has_correct_edge():
    topology_builder = TopologyBuilder(JunctionRepository(), TrackSectionRepository(), TrackBlockRepository())
    graph = topology_builder.build_graph()
    assert len(graph.edges) == 2
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
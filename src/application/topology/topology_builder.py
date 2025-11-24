from src.application.routing.routing_graph import RoutingGraph
from src.application.routing.routing_node import RoutingNode
from src.application.routing.routing_edge import RoutingEdge
from src.domain.domain_enums import TurnoutState
from src.domain.track.track_block import  TrackBlock, PlatformTrackBlock, IndustryTrackBlock
from src.infrastructure.repository.junction_repository import JunctionRepository
from src.infrastructure.repository.track_block_repository import TrackBlockRepository
from src.infrastructure.repository.track_section_repository import TrackSectionRepository
from src.application.utils.scale_conversion import travel_time_seconds
from src.infrastructure.repository.turnout_repository import TurnoutRepository


class TopologyBuilder:
    def __init__(
            self,
            junction_repository: JunctionRepository,
            track_section_repository: TrackSectionRepository,
            track_block_repository: TrackBlockRepository,
            turnout_repository: TurnoutRepository
        ):
        self.junction_repository = junction_repository
        self.track_section_repository = track_section_repository
        self.track_block_repository = track_block_repository
        self.turnout_repository = turnout_repository

    def build_graph(self):
        #Initilise Graph Objects
        route_graph = RoutingGraph()

        #Load Domain Objects
        junctions = self.junction_repository.get_all()
        track_sections = self.track_section_repository.get_all()
        turnouts = self.turnout_repository.get_all()

        #Create RoutingNode for each junction
        for junction in junctions:
            route_graph.nodes[junction.junction_id] = RoutingNode(junction.junction_id)

        #Build Adjacency list
        for node in route_graph.nodes:
            node_edges = list()
            route_graph.edges[node] = node_edges

        #Create FWD and REV RoutingEdge for each track section with all metadata
        for track_section in track_sections:
            start_junction = track_section.start_junction_id
            end_junction = track_section.end_junction_id

            section_block = self.track_block_repository.get(track_section.block_id)
            if isinstance(section_block, PlatformTrackBlock):
                block_class = "PLATFORM"
            elif isinstance(section_block, IndustryTrackBlock):
                block_class = "INDUSTRY"
            elif isinstance(section_block, TrackBlock):
                block_class = "NORMAL"
            else:
                block_class = "UNKOWN"

            block_type = section_block.track_block_type.name

            #Create FWD and REV edges
            travel_time_s = travel_time_seconds(track_section.length_mm, track_section.max_speed)

            route_edge_fwd = RoutingEdge(
                start_junction,
                end_junction,
                track_section.id,
                track_section.block_id,
                track_section.length_mm,
                track_section.max_speed,
                travel_time_s,
                block_class,
                block_type)

            route_edge_rev = RoutingEdge(
                end_junction,
                start_junction,
                track_section.id,
                track_section.block_id,
                track_section.length_mm,
                track_section.max_speed,
                travel_time_s,
                block_class,
                block_type)
            route_graph.edges[start_junction].append(route_edge_fwd)
            route_graph.edges[end_junction].append(route_edge_rev)

        # turnout
        turnout_by_section = {}
        for turnout in turnouts:
            turnout_by_section[turnout.straight_section_id] = turnout
            turnout_by_section[turnout.diverging_section_id] = turnout

        for node_id in route_graph.edges:
            valid_edge_list = []
            for edge in route_graph.edges[node_id]:
                if edge.track_section_id in turnout_by_section:
                    turnout = turnout_by_section[edge.track_section_id]
                    if ((
                            turnout.current_state == TurnoutState.STRAIGHT
                            and edge.track_section_id == turnout.straight_section_id)
                            or
                            (turnout.current_state == TurnoutState.DIVERGING
                             and edge.track_section_id == turnout.diverging_section_id)
                    ):
                        valid_edge_list.append(edge)
                    else:
                        continue
                else:
                    valid_edge_list.append(edge)
            route_graph.edges[node_id] = valid_edge_list


        #Construct the Routing Graph
        return route_graph
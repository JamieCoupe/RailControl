import pytest

from railcontrol.application.timetable.block_occupancy_generator import BlockOccupancyGenerator
from railcontrol.domain.timetable.expanded_passenger_leg import ExpandedPassengerLeg
from railcontrol.domain.timetable.expanded_passenger_route import ExpandedPassengerRoute
from railcontrol.domain.timetable.block_occupancy import BlockOccupancy
from railcontrol.application.routing.routing_edge import RoutingEdge
from railcontrol.domain.domain_enums import Direction


class DummyEdge:
    def __init__(self, block_id, length_mm, max_speed, from_node="A", to_node="B"):
        self.track_block_id = block_id
        self.length_mm = length_mm
        self.max_speed = max_speed
        self.from_node = from_node
        self.to_node = to_node

def test_block_occupancy_sequence_generation():
    """
    Ensure the generator:
      - steps through inbound edges in order
      - applies traversal_time + buffer
      - then processes the platform dwell
      - accumulates times correctly
      - uses ExpandedPassengerRoute.direction
    """

    # --- Setup dummy edges ---
    e1 = DummyEdge(block_id="BLK_MAIN_1", length_mm=1000, max_speed=60)
    e2 = DummyEdge(block_id="BLK_MAIN_2", length_mm=500, max_speed=30)

    # --- First leg has no inbound edges (origin station) ---
    legA = ExpandedPassengerLeg(
        station_id="STA",
        platform_block_id="BLK_STA_P1",
        arrival_junction_id="J1",
        departure_junction_id="J2",
        inbound_path_edges=[],
        dwell_time=30,
        is_request_stop=False,
        platform_length_mm=400,
        platform_max_speed=25,
    )

    # --- Second leg has 2 inbound edges (track between stations) ---
    legB = ExpandedPassengerLeg(
        station_id="STB",
        platform_block_id="BLK_STB_P1",
        arrival_junction_id="J3",
        departure_junction_id="J4",
        inbound_path_edges=[e1, e2],
        dwell_time=20,
        is_request_stop=False,
        platform_length_mm=400,
        platform_max_speed=25,
    )

    route = ExpandedPassengerRoute(
        legs=[legA, legB],
        direction=Direction.UP
    )

    gen = BlockOccupancyGenerator(
        service_id="SVC1",
        start_time=1000,
        expanded_route=route
    )

    results = gen.generate()


    # ---------------------------------------------------
    # EXPECTED ORDER:
    #   (1) STA platform dwell
    #   (2) e1 inbound
    #   (3) e2 inbound
    #   (4) STB platform dwell
    # ---------------------------------------------------

    assert len(results) == 4

    # 1. First is STA platform
    assert results[0].block_id == "BLK_STA_P1"
    assert results[0].service_id == "SVC1"
    assert results[0].direction == Direction.UP

    # 2. Then inbound edges in order
    assert results[1].block_id == "BLK_MAIN_1"
    assert results[2].block_id == "BLK_MAIN_2"

    # 3. Final is station B platform
    assert results[3].block_id == "BLK_STB_P1"

    # Times must be strictly increasing
    assert results[0].t_entry == 1000
    assert results[0].t_exit < results[1].t_entry
    assert results[1].t_exit < results[2].t_entry
    assert results[2].t_exit < results[3].t_entry


def test_zero_dwell_handling():
    """
    If a leg has dwell_time = 0, occupancy still exists (train still occupies the block briefly)
    """
    leg = ExpandedPassengerLeg(
        station_id="STA",
        platform_block_id="BLK_STA_P1",
        arrival_junction_id="J1",
        departure_junction_id="J2",
        inbound_path_edges=[],
        dwell_time=0,
        is_request_stop=False,
        platform_length_mm=400,
        platform_max_speed=25,
    )

    route = ExpandedPassengerRoute(
        legs=[leg],
        direction=Direction.DOWN
    )

    gen = BlockOccupancyGenerator(
        service_id="SVCX",
        start_time=0,
        expanded_route=route
    )

    results = gen.generate()

    assert len(results) == 1
    assert results[0].block_id == "BLK_STA_P1"
    assert results[0].direction == Direction.DOWN
    assert results[0].t_exit > results[0].t_entry   # buffer should apply

import pytest

from railcontrol.application.timetable.passenger_timetable_service import PassengerTimetableService
from railcontrol.domain.domain_enums import Direction
from railcontrol.domain.timetable.expanded_passenger_route import ExpandedPassengerRoute
from railcontrol.domain.timetable.expanded_passenger_leg import ExpandedPassengerLeg

class DummyEdge:
    def __init__(self, weight):
        self.weight = weight

def test_single_station_timetable():
    service = PassengerTimetableService()

    # Expanded route with a single station
    legs = [
        ExpandedPassengerLeg(
            station_id="A",
            platform_block_id="P1",
            arrival_junction_id="J1",
            departure_junction_id="J2",
            inbound_path_edges=[],   # first station
            dwell_time=30,
            is_request_stop=False,
            platform_length_mm=400,
            platform_max_speed=25,
        )
    ]

    route = ExpandedPassengerRoute(legs, direction=Direction.UP)
    timetable = service.generate_timetable(route, start_time_seconds=1000)

    assert len(timetable) == 1
    assert timetable[0]["arrival_time"] == 1000
    assert timetable[0]["departure_time"] == 1030
    assert timetable[0]["station_id"] == "A"


def test_two_station_timetable():
    service = PassengerTimetableService()

    legA = ExpandedPassengerLeg(
        station_id="A",
        platform_block_id="PA",
        arrival_junction_id="JA1",
        departure_junction_id="JA2",
        inbound_path_edges=[],
        dwell_time=30,
        is_request_stop=False,
        platform_length_mm=400,
        platform_max_speed=25,
    )

    legB = ExpandedPassengerLeg(
        station_id="B",
        platform_block_id="PB",
        arrival_junction_id="JB1",
        departure_junction_id="JB2",
        inbound_path_edges=[DummyEdge(20), DummyEdge(10)],   # 30 sec travel
        dwell_time=45,
        is_request_stop=False,
        platform_length_mm=400,
        platform_max_speed=25,
    )

    route = ExpandedPassengerRoute([legA, legB], Direction.UP)
    timetable = service.generate_timetable(route, start_time_seconds=0)

    # A
    assert timetable[0]["arrival_time"] == 0
    assert timetable[0]["departure_time"] == 30

    # B
    assert timetable[1]["arrival_time"] == 30 + 30    # A dep + travel
    assert timetable[1]["departure_time"] == 60 + 45
    assert timetable[1]["station_id"] == "B"

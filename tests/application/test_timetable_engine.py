import pytest

from railcontrol.application.timetable.timetable_engine import TimetableEngine
from railcontrol.domain.timetable.timetable_row import TimetableRow


class DummyLeg:
    def __init__(self, station_id, runtime, dwell):
        self.station_id = station_id
        self.running_time_s = runtime
        self.dwell_used_s = dwell
        # The engine doesn’t use other fields


def test_single_leg_timetable():
    """
    Only one station in route.
    Should have arrival at start time and no departure.
    """
    legs = [DummyLeg("STN_A", runtime=0, dwell=30)]

    class DummyRoute:
        pass

    route = DummyRoute()
    route.legs = legs

    engine = TimetableEngine()
    rows = engine.generate_timetable(route, start_time_seconds=1000)

    assert len(rows) == 2

    row = rows[0]
    assert row.station_id == "STN_A"
    assert row.arrival_s == 1000
    assert row.departure_s == 1030
    assert row.dwell_s == 30
    assert row.runtime_s == 0


def test_two_station_timetable():
    """
    Simple 2-station route.
    First station uses dwell.
    Second station has arrival only.
    """

    legs = [
        DummyLeg("STN_A", runtime=0, dwell=60),
        DummyLeg("STN_B", runtime=120, dwell=45),
    ]

    class DummyRoute:
        pass

    route = DummyRoute()
    route.legs = legs

    engine = TimetableEngine()
    rows = engine.generate_timetable(route, start_time_seconds=0)

    assert len(rows) == 2

    # STN_A
    r0 = rows[0]
    assert r0.station_id == "STN_A"
    assert r0.arrival_s == 0
    assert r0.departure_s == 60
    assert r0.runtime_s == 0

    # STN_B
    r1 = rows[1]
    assert r1.station_id == "STN_B"
    assert r1.arrival_s == 60 + 120
    assert r1.departure_s is None
    assert r1.runtime_s == 120


def test_multi_station_chain():
    """
    3-station chain, verifies cumulative propagation:
    A → B → C
    """

    legs = [
        DummyLeg("A", runtime=0, dwell=50),
        DummyLeg("B", runtime=100, dwell=40),
        DummyLeg("C", runtime=200, dwell=30),
    ]

    class DummyRoute:
        pass

    route = DummyRoute()
    route.legs = legs

    engine = TimetableEngine()
    rows = engine.generate_timetable(route, start_time_seconds=1000)

    # Station A
    assert rows[0].arrival_s == 1000
    assert rows[0].departure_s == 1050  # +50 dwell

    # Station B
    assert rows[1].arrival_s == 1050 + 100
    assert rows[1].departure_s == rows[1].arrival_s + 40

    # Station C
    assert rows[2].arrival_s == rows[1].departure_s + 200
    assert rows[2].departure_s is None
    assert rows[2].runtime_s == 200

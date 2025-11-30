import pytest

from railcontrol.application.timetable.running_time_calculator import RunningTimeCalculator
from railcontrol.application.timetable.timetable_profile import TimetableProfile
from railcontrol.application.utils.scale_conversion import travel_time_seconds
from railcontrol.domain.timetable.expanded_passenger_leg import ExpandedPassengerLeg


class DummyEdge:
    def __init__(self, block_id, length_mm, max_speed, from_node="A", to_node="B"):
        self.track_block_id = block_id
        self.length_mm = length_mm
        self.max_speed = max_speed
        self.from_node = from_node
        self.to_node = to_node


def expected_leg_time(length_mm, mph, dwell, padding):
    raw = travel_time_seconds(length_mm, mph)
    return pytest.approx(raw + dwell + padding, abs=1), raw


def test_travel_time_platform_only():
    leg = ExpandedPassengerLeg(
        station_id="STN",
        platform_block_id="P1",
        arrival_junction_id=None,
        departure_junction_id=None,
        inbound_path_edges=[],
        dwell_time=5,
        is_request_stop=False,
        platform_length_mm=400,
        platform_max_speed=25,
    )

    calc = RunningTimeCalculator()
    result = calc.calculate_leg_travel_time(leg, "express")

    profile = TimetableProfile.get_profile("express")
    eff_speed = max(1, int(25 * profile["speed_factor"]))

    expected_total, expected_raw = expected_leg_time(
        400, eff_speed, max(5, profile["minimum_dwell"]), profile["padding_seconds"]
    )

    assert result["time_s"] == expected_total
    assert result["effective_speed_mph"] == eff_speed
    assert result["raw_time_s"] == pytest.approx(expected_raw, abs=1)
    assert result["dwell_s"] == max(5, profile["minimum_dwell"])
    assert result["padding_s"] == profile["padding_seconds"]


def test_travel_time_inbound_only():
    edge = DummyEdge("BLK1", length_mm=5000, max_speed=60)

    leg = ExpandedPassengerLeg(
        station_id="STN",
        platform_block_id=None,
        arrival_junction_id="A",
        departure_junction_id="B",
        inbound_path_edges=[edge],
        dwell_time=0,
        is_request_stop=False,
        platform_length_mm=0,
        platform_max_speed=40,
    )

    calc = RunningTimeCalculator()
    result = calc.calculate_leg_travel_time(leg, "express")

    profile = TimetableProfile.get_profile("express")
    eff_speed = max(1, int(60 * profile["speed_factor"]))

    expected_total, expected_raw = expected_leg_time(
        5000, eff_speed, profile["minimum_dwell"], profile["padding_seconds"]
    )

    assert result["time_s"] == expected_total
    assert result["effective_speed_mph"] == eff_speed
    assert result["raw_time_s"] == pytest.approx(expected_raw, abs=1)


def test_inbound_uses_minimum_speed():
    edges = [
        DummyEdge("BLK1", length_mm=3000, max_speed=100),
        DummyEdge("BLK2", length_mm=3000, max_speed=40),
    ]

    leg = ExpandedPassengerLeg(
        station_id="STN",
        platform_block_id=None,
        arrival_junction_id="A",
        departure_junction_id="C",
        inbound_path_edges=edges,
        dwell_time=0,
        is_request_stop=False,
        platform_length_mm=0,
        platform_max_speed=200,
    )

    calc = RunningTimeCalculator()
    result = calc.calculate_leg_travel_time(leg, "express")

    profile = TimetableProfile.get_profile("express")
    eff_speed = max(1, int(40 * profile["speed_factor"]))

    expected_total, expected_raw = expected_leg_time(
        6000, eff_speed, profile["minimum_dwell"], profile["padding_seconds"]
    )

    assert result["time_s"] == expected_total
    assert result["effective_speed_mph"] == eff_speed


def test_dwell_logic_max_of_leg_and_profile():
    leg = ExpandedPassengerLeg(
        station_id="TEST",
        platform_block_id="P1",
        arrival_junction_id=None,
        departure_junction_id=None,
        inbound_path_edges=[],
        dwell_time=25,
        is_request_stop=False,
        platform_length_mm=400,
        platform_max_speed=25,
    )

    calc = RunningTimeCalculator()
    result = calc.calculate_leg_travel_time(leg, "stopping")

    profile = TimetableProfile.get_profile("stopping")
    eff_speed = max(1, int(25 * profile["speed_factor"]))

    dwell_used = max(25, profile["minimum_dwell"])

    expected_total, expected_raw = expected_leg_time(
        400, eff_speed, dwell_used, profile["padding_seconds"]
    )

    assert result["time_s"] == expected_total
    assert result["dwell_s"] == dwell_used
    assert result["effective_speed_mph"] == eff_speed
    assert result["padding_s"] == profile["padding_seconds"]


def test_dwell_uses_profile_minimum_if_leg_dwell_low():
    leg = ExpandedPassengerLeg(
        station_id="TEST",
        platform_block_id="P1",
        arrival_junction_id=None,
        departure_junction_id=None,
        inbound_path_edges=[],
        dwell_time=5,
        is_request_stop=False,
        platform_length_mm=400,
        platform_max_speed=25,
    )

    calc = RunningTimeCalculator()
    result = calc.calculate_leg_travel_time(leg, "stopping")

    profile = TimetableProfile.get_profile("stopping")
    eff_speed = max(1, int(25 * profile["speed_factor"]))

    dwell_used = max(5, profile["minimum_dwell"])

    expected_total, expected_raw = expected_leg_time(
        400, eff_speed, dwell_used, profile["padding_seconds"]
    )

    assert result["dwell_s"] == dwell_used
    assert result["time_s"] == expected_total


def test_speed_floor_of_1_mph():
    edge = DummyEdge("BLK1", length_mm=1000, max_speed=1)

    leg = ExpandedPassengerLeg(
        station_id="STN",
        platform_block_id=None,
        arrival_junction_id="A",
        departure_junction_id="B",
        inbound_path_edges=[edge],
        dwell_time=0,
        is_request_stop=False,
        platform_length_mm=0,
        platform_max_speed=0,
    )

    calc = RunningTimeCalculator()
    result = calc.calculate_leg_travel_time(leg, "stopping")

    profile = TimetableProfile.get_profile("stopping")
    eff_speed = max(1, int(1 * profile["speed_factor"]))

    expected_total, expected_raw = expected_leg_time(
        1000, eff_speed, profile["minimum_dwell"], profile["padding_seconds"]
    )

    assert result["effective_speed_mph"] == eff_speed
    assert result["time_s"] == expected_total


def test_request_stop_still_includes_min_dwell():
    leg = ExpandedPassengerLeg(
        station_id="X",
        platform_block_id="Y",
        arrival_junction_id=None,
        departure_junction_id=None,
        inbound_path_edges=[],
        dwell_time=0,
        is_request_stop=True,
        platform_length_mm=400,
        platform_max_speed=25,
    )

    calc = RunningTimeCalculator()
    result = calc.calculate_leg_travel_time(leg, "express")

    profile = TimetableProfile.get_profile("express")
    eff_speed = max(1, int(25 * profile["speed_factor"]))

    expected_total, expected_raw = expected_leg_time(
        400, eff_speed, profile["minimum_dwell"], profile["padding_seconds"]
    )

    assert result["dwell_s"] == profile["minimum_dwell"]
    assert result["time_s"] == expected_total


def test_platform_speed_used_only_when_no_inbound_edges():
    edge = DummyEdge("BLK_MAIN", length_mm=2000, max_speed=20)

    leg = ExpandedPassengerLeg(
        station_id="STN",
        platform_block_id="P",
        arrival_junction_id="A",
        departure_junction_id="B",
        inbound_path_edges=[edge],
        dwell_time=0,
        is_request_stop=False,
        platform_length_mm=5000,
        platform_max_speed=5,
    )

    calc = RunningTimeCalculator()
    result = calc.calculate_leg_travel_time(leg, "stopping")

    profile = TimetableProfile.get_profile("stopping")
    eff_speed = max(1, int(20 * profile["speed_factor"]))

    expected_total, expected_raw = expected_leg_time(
        7000, eff_speed, profile["minimum_dwell"], profile["padding_seconds"]
    )

    assert result["effective_speed_mph"] == eff_speed
    assert result["time_s"] == expected_total

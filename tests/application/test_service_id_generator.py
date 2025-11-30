import pytest

from railcontrol.application.timetable.service_id_generator import ServiceIDGenerator
from railcontrol.application.application_enums import TimetableProfileTypes
from railcontrol.domain.domain_enums import Direction
from railcontrol.domain.timetable.expanded_passenger_route import ExpandedPassengerRoute


class DummyRoute:
    """Minimal dummy representing ExpandedPassengerRoute for region tests."""
    def __init__(self):
        self.direction = Direction.UP
        # minimal legs list with a station_id for future use
        class L:
            station_id = "STN_TEST"
        self.legs = [L()]


def test_class_mapping():
    gen = ServiceIDGenerator()

    assert gen.train_class_from_profile(TimetableProfileTypes.EXPRESS.value) == 1
    assert gen.train_class_from_profile(TimetableProfileTypes.STOPPING.value) == 2
    assert gen.train_class_from_profile(TimetableProfileTypes.ECS.value) == 5
    assert gen.train_class_from_profile(TimetableProfileTypes.LIGHT_ENGINE.value) == 0
    assert gen.train_class_from_profile(TimetableProfileTypes.FREIGHT_SLOW.value) == 7
    assert gen.train_class_from_profile(TimetableProfileTypes.FREIGHT_FAST.value) == 4
    assert gen.train_class_from_profile(TimetableProfileTypes.FREIGHT_HEAVY.value) == 6


def test_region_mapping():
    gen = ServiceIDGenerator()
    route = DummyRoute()

    assert gen.region_code_from_route(route) == "S"


def test_next_number_sequential():
    gen = ServiceIDGenerator()

    assert gen.next_number() == "01"
    assert gen.next_number() == "02"
    assert gen.next_number() == "03"


def test_number_rollover():
    gen = ServiceIDGenerator()
    gen.counter = 99

    assert gen.next_number() == "99"
    assert gen.next_number() == "01"  # roll over to 01


def test_generate_headcode_basic():
    gen = ServiceIDGenerator()
    route = DummyRoute()

    headcode = gen.generate_headcode(TimetableProfileTypes.EXPRESS.value, route)

    assert headcode.startswith("1S")   # express + Scotland
    assert len(headcode) == 4         # e.g., '1S01'


def test_multiple_headcodes_increment():
    gen = ServiceIDGenerator()
    route = DummyRoute()

    hc1 = gen.generate_headcode(TimetableProfileTypes.STOPPING.value, route)
    hc2 = gen.generate_headcode(TimetableProfileTypes.STOPPING.value, route)

    assert hc1 != hc2
    assert hc1[:2] == hc2[:2] == "2S"  # stopping + Scotland

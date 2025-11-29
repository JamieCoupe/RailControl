import pytest

from src.domain.domain_enums import TrackBlockType, TrackBlockClass
from src.domain.station.passenger_stop import PassengerStop
from src.domain.station.station import Station
from src.domain.timetable.passenger_route import PassengerRoute
from src.domain.track.track_block import PlatformTrackBlock
from src.application.routing.passenger_route_expander import PassengerRouteExpander
from src.domain.track.track_section import TrackSection


class DummyBlockRepo:
    """
    Matches real TrackBlockRepository interface sufficiently for tests.
    """
    def __init__(self, platform_blocks):
        self._platform_blocks = platform_blocks

    def get_platform_blocks_for_station(self, station_id):
        return self._platform_blocks

    # NEW (the expander now expects this)
    def get_by_station(self, station_id):
        return self._platform_blocks

class DummyTrackSectionRepo:
    def __init__(self, sections):
        self._sections = sections

    def get_by_block_id(self, block_id):
        return self._sections

class DummyRoutingGraph:
    def __init__(self):
        self.edges = {}

class DummyRoutingService:
    def __init__(self):
        # minimal graph object
        self.graph = type(
            "G",
            (),
            {"edges": {"j1": [], "j2": [], "J_ENTRY": [], "J_EXIT": []}}
        )()

    def find_route(self, a, b):
        class R:
            success = True
            path_nodes = [a, b]
            node_ids = [a, b]      # <-- REQUIRED FIX
            edge_ids = []          # no edges in dummy scenario
            message = ""
        return R()

class DummyStationRepo:
    def __init__(self, stations):
        self.stations = stations

    def get(self, station_id):
        # Always return a Station object for the requested id
        return Station(id=station_id, name=f"Station {station_id}", track_blocks=[])


def make_expander(platform_blocks):
    station = Station(id="ABC", name="Test Station", track_blocks=[])
    section = TrackSection(
        id="section1",
        block_id="blk1",
        start_junction_id="j1",
        end_junction_id="j2",
        length_mm=100,
        max_speed=100
    )

    station_repo = DummyStationRepo({"ABC": station})
    block_repo = DummyBlockRepo(platform_blocks)
    section_repo = DummyTrackSectionRepo([section])
    routing = DummyRoutingService()

    return PassengerRouteExpander(
        station_repo,
        block_repo,
        section_repo,
        routing,
    )


def test_resolve_platform_block_with_preference():
    p1 = PlatformTrackBlock(id="P1", station_id="ABC", name="test-1",
                            track_block_type=TrackBlockType.PLATFORM_TRACK,
                            track_block_class=TrackBlockClass.PLATFORM,
                            dwell_time_minutes=10, platform_number=1)
    p2 = PlatformTrackBlock(id="P2", station_id="ABC", name="test-2",
                            track_block_type=TrackBlockType.PLATFORM_TRACK,
                            track_block_class=TrackBlockClass.PLATFORM,
                            dwell_time_minutes=10, platform_number=2)

    expander = make_expander([p1, p2])

    stop = PassengerStop(station_id="ABC", platform_preference=2)
    result = expander._resolve_platform_block_for_stop(stop)

    assert result == p2


def test_resolve_platform_block_invalid_preference_raises():
    p1 = PlatformTrackBlock(id="P1", station_id="ABC", name="test-1",
                            track_block_type=TrackBlockType.PLATFORM_TRACK,
                            track_block_class=TrackBlockClass.PLATFORM,
                            dwell_time_minutes=10, platform_number=1)

    expander = make_expander([p1])

    stop = PassengerStop(station_id="ABC", platform_preference=3)

    with pytest.raises(ValueError):
        expander._resolve_platform_block_for_stop(stop)


def test_resolve_platform_block_single_platform():
    p1 = PlatformTrackBlock(id="P1", station_id="ABC", name="test-1",
                            track_block_type=TrackBlockType.PLATFORM_TRACK,
                            track_block_class=TrackBlockClass.PLATFORM,
                            dwell_time_minutes=10, platform_number=1)

    expander = make_expander([p1])

    stop = PassengerStop(station_id="ABC")
    result = expander._resolve_platform_block_for_stop(stop)

    assert result == p1


def test_resolve_platform_block_multiple_platform_default_first():
    p1 = PlatformTrackBlock(id="P1", station_id="ABC", name="test-1",
                            track_block_type=TrackBlockType.PLATFORM_TRACK,
                            track_block_class=TrackBlockClass.PLATFORM,
                            dwell_time_minutes=10, platform_number=1)
    p2 = PlatformTrackBlock(id="P2", station_id="ABC", name="test-2",
                            track_block_type=TrackBlockType.PLATFORM_TRACK,
                            track_block_class=TrackBlockClass.PLATFORM,
                            dwell_time_minutes=10, platform_number=2)

    expander = make_expander([p1, p2])

    stop = PassengerStop(station_id="ABC")
    result = expander._resolve_platform_block_for_stop(stop)

    assert result == p1


def test_resolve_platform_block_no_platforms_raises():
    expander = make_expander([])

    stop = PassengerStop(station_id="ABC")

    with pytest.raises(ValueError):
        expander._resolve_platform_block_for_stop(stop)


def test_stop_level_dwell_overrides_platform():
    platform = PlatformTrackBlock(
        id="P1", name="Platform1", track_block_type=TrackBlockType.PLATFORM_TRACK,
        track_block_class=TrackBlockClass.PLATFORM,
        dwell_time_minutes=3, platform_number=1, station_id="STA"
    )

    expander = make_expander([platform])

    stop_a = PassengerStop(station_id="STA", dwell_time=None)
    stop_b = PassengerStop(station_id="STA", dwell_time=10)

    leg = expander._build_route_leg(stop_a, stop_b)

    assert leg.dwell_time == 10


def test_fallback_to_platform_dwell():
    platform = PlatformTrackBlock(
        id="P2", name="Platform2", track_block_type=TrackBlockType.PLATFORM_TRACK,
        track_block_class=TrackBlockClass.PLATFORM,
        dwell_time_minutes=2, platform_number=1, station_id="STB"
    )

    expander = make_expander([platform])

    stop_a = PassengerStop(station_id="STB")
    stop_b = PassengerStop(station_id="STB")

    leg = expander._build_route_leg(stop_a, stop_b)

    assert leg.dwell_time == 120


def test_negative_dwell_raises_error():
    platform = PlatformTrackBlock(
        id="P3", name="Platform3", track_block_type=TrackBlockType.PLATFORM_TRACK,
        track_block_class=TrackBlockClass.PLATFORM,
        dwell_time_minutes=1, platform_number=1, station_id="STC"
    )

    expander = make_expander([platform])

    stop_a = PassengerStop(station_id="STC")
    stop_b = PassengerStop(station_id="STC", dwell_time=-5)

    with pytest.raises(ValueError):
        expander._build_route_leg(stop_a, stop_b)



def test_expand_route_includes_first_station():
    """
    Ensure the expander includes a first leg for the origin station
    BEFORE any routing occurs.
    """

    # --- Setup platform + junctions ---
    pblock = PlatformTrackBlock(
        id="P1",
        name="Platform 1",
        track_block_type=TrackBlockType.PLATFORM_TRACK,
        track_block_class=TrackBlockClass.PLATFORM,
        station_id="STA",
        dwell_time_minutes=2,
        platform_number=1
    )

    # its track section defines entry/exit junctions
    section = TrackSection(
        id="TS1",
        block_id="P1",
        start_junction_id="J_ENTRY",
        end_junction_id="J_EXIT",
        length_mm=100,
        max_speed=60
    )

    # --- repos ---
    station_repo = DummyStationRepo({"STA": object()})   # station object not used here
    block_repo = DummyBlockRepo([pblock])
    section_repo = DummyTrackSectionRepo([section])
    routing = DummyRoutingService()

    expander = PassengerRouteExpander(
        station_repo,
        block_repo,
        section_repo,
        routing
    )

    # --- Stops: only one relevant here ---
    stopA = PassengerStop(station_id="STA", dwell_time=30)
    stopB = PassengerStop(station_id="STA", dwell_time=10)  # second stop unused for first-leg validation

    route = PassengerRoute(id="tTR1", name="Test Route", stops=[stopA, stopB])

    expanded = expander.expand_route(route)

    # --------------------
    #   ASSERTIONS
    # --------------------
    first_leg = expanded.legs[0]

    assert first_leg.station_id == "STA"
    assert first_leg.inbound_path_edges == []          # critical
    assert first_leg.platform_block_id == "P1"
    assert first_leg.arrival_junction_id == "J_ENTRY"
    assert first_leg.departure_junction_id == "J_EXIT"
    assert first_leg.dwell_time == 30                  # dwell override
    assert first_leg.is_request_stop is False
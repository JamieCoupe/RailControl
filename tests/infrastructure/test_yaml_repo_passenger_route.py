import pytest

from railcontrol.domain.domain_enums import Direction
from railcontrol.infrastructure.data_sources.yaml.passenger_route_loader import PassengerRouteYamlLoader
from railcontrol.infrastructure.repository.yaml.yaml_passenger_route_repository import YamlPassengerRouteRepository


def test_passenger_route_repo_loads_passenger_routes_correctly(tmp_path):
    yaml_text = """
        passenger_routes:
          - id: RTE_RNFR_ABTI_UP
            name: Renfrew to Abbots Inch
            direction: UP
            stops:
              - station_id: STN_RNFR
                dwell_time: 60
                platform: 1
        
              - station_id: STN_ABTI
                dwell_time: 45
        """

    yaml_file = tmp_path / "passenger_routes.yaml"
    yaml_file.write_text(yaml_text)

    repo = YamlPassengerRouteRepository(PassengerRouteYamlLoader(str(yaml_file)))

    passenger_route = repo.get("RTE_RNFR_ABTI_UP")

    assert passenger_route.id == "RTE_RNFR_ABTI_UP"
    assert passenger_route.name == "Renfrew to Abbots Inch"
    assert len(passenger_route.stops) == 2
    assert passenger_route.direction == Direction.UP


def test_passenger_route_repo_loads_passenger_routes_correctly_with_no_stops(tmp_path):
    yaml_text = """
            passenger_routes:
              - id: RTE_RNFR_ABTI_UP
                name: Renfrew to Abbots Inch
                direction: UP
                stops: 
            """

    yaml_file = tmp_path / "passenger_routes.yaml"
    yaml_file.write_text(yaml_text)

    repo = YamlPassengerRouteRepository(PassengerRouteYamlLoader(str(yaml_file)))

    passenger_route = repo.get("RTE_RNFR_ABTI_UP")

    assert passenger_route.id == "RTE_RNFR_ABTI_UP"
    assert passenger_route.name == "Renfrew to Abbots Inch"
    assert len(passenger_route.stops) == 0
    assert passenger_route.direction == Direction.UP

def test_repo_raises_for_missing_stations(tmp_path):
    yaml_text = """
            passenger_routes:
              - id: RTE_RNFR_ABTI_UP
                name: Renfrew to Abbots Inch
                direction: UP
                stops:
                  - station_id: STN_RNFR
                    dwell_time: 60
                    platform: 1

                  - station_id: STN_ABTI
                    dwell_time: 45
            """

    yaml_file = tmp_path / "passenger_routes.yaml"
    yaml_file.write_text(yaml_text)

    repo = YamlPassengerRouteRepository(PassengerRouteYamlLoader(str(yaml_file)))

    with pytest.raises(KeyError):
        repo.get("NOPE")

def test_passenger_route_get_by_station(tmp_path):
    yaml_text = """
    passenger_routes:
      - id: R1
        name: Route 1
        direction: UP
        stops:
          - station_id: STN_A
          - station_id: STN_B
      - id: R2
        name: Route 2
        direction: DOWN
        stops:
          - station_id: STN_C
    """

    yaml_file = tmp_path / "passenger_routes.yaml"
    yaml_file.write_text(yaml_text)

    repo = YamlPassengerRouteRepository(PassengerRouteYamlLoader(str(yaml_file)))

    result = repo.get_by_station("STN_A")

    assert len(result) == 1
    assert result[0].id == "R1"
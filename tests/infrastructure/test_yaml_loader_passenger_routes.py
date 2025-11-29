import pytest

from railcontrol.infrastructure.data_sources.yaml.passenger_route_loader import PassengerRouteYamlLoader


def test_yaml_is_loaded(tmp_path):
    yaml_file = tmp_path / "passenger_routes.yaml"
    yaml_file.write_text("""
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
    """)

    loader = PassengerRouteYamlLoader(str(yaml_file))
    data = loader.load()

    assert "passenger_routes" in data
    assert data["passenger_routes"][0]["id"] == "RTE_RNFR_ABTI_UP"

def test_validation_for_invalid_yaml(tmp_path):
    yaml_file = tmp_path / "passenger_routes.yaml"
    yaml_file.write_text("""
    - hello
    - world
    """)

    loader = PassengerRouteYamlLoader(str(yaml_file))
    with pytest.raises(ValueError):
        loader.load()

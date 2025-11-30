import pytest

from railcontrol.infrastructure.data_sources.yaml.station_loader import StationYamlLoader
from railcontrol.infrastructure.data_sources.yaml.track_block_loader import TrackBlockYamlLoader
from railcontrol.infrastructure.repository.yaml.yaml_station_repository import YamlStationRepository
from railcontrol.infrastructure.repository.yaml.yaml_track_block_repository import YamlTrackBlockRepository


def test_station_repo_loads_stations_correctly(tmp_path):
    yaml_text = """
        track_blocks:
          - id: BLK_P1
            name: Renfrew Platform 1
            block_type: PLATFORM_TRACK
            block_class: PLATFORM
            station_id: STN_RNFR
            dwell_time_minutes: 1
            platform_number: 1
            length_mm: 600
        """

    yaml_file = tmp_path / "track_blocks.yaml"
    yaml_file.write_text(yaml_text)

    platform_repo = YamlTrackBlockRepository(TrackBlockYamlLoader(str(yaml_file)))

    yaml_text = """
    stations:
      - id: STN_RNFR
        name: Renfrew
    
      - id: STN_ABTI
        name: Abbots Inch
    """

    yaml_file = tmp_path / "stations.yaml"
    yaml_file.write_text(yaml_text)

    loader = StationYamlLoader(str(yaml_file))
    repo = YamlStationRepository(loader, platform_repo)

    station = repo.get("STN_RNFR")

    assert station.id == "STN_RNFR"
    assert station.name == "Renfrew"
    assert len(station.track_blocks) == 1
    assert station.track_blocks[0].name == "Renfrew Platform 1"


def test_station_repo_loads_stations_correctly_with_no_platforms(tmp_path):
    yaml_text = """
        track_blocks:
          - id: BLK_P1
            name: Renfrew Platform 1
            block_type: PLATFORM_TRACK
            block_class: PLATFORM
            station_id: STN_RNFR
            dwell_time_minutes: 1
            platform_number: 1
            length_mm: 600
        """

    yaml_file = tmp_path / "track_blocks.yaml"
    yaml_file.write_text(yaml_text)

    platform_repo = YamlTrackBlockRepository(TrackBlockYamlLoader(str(yaml_file)))

    yaml_text = """
    stations:
      - id: STN_RNFR
        name: Renfrew

      - id: STN_ABTI
        name: Abbots Inch
    """

    yaml_file = tmp_path / "stations.yaml"
    yaml_file.write_text(yaml_text)

    loader = StationYamlLoader(str(yaml_file))
    repo = YamlStationRepository(loader, platform_repo)

    station = repo.get("STN_ABTI")

    assert station.id == "STN_ABTI"
    assert station.name == "Abbots Inch"
    assert len(station.track_blocks) == 0
    assert station.track_blocks == []

def test_repo_raises_for_missing_stations(tmp_path):
    yaml_text = """
            track_blocks:
              - id: BLK_P1
                name: Renfrew Platform 1
                block_type: PLATFORM_TRACK
                block_class: PLATFORM
                station_id: STN_RNFR
                dwell_time_minutes: 1
                platform_number: 1
                length_mm: 600
            """

    yaml_file = tmp_path / "track_blocks.yaml"
    yaml_file.write_text(yaml_text)

    platform_repo = YamlTrackBlockRepository(TrackBlockYamlLoader(str(yaml_file)))

    yaml_text = """
       stations:
         - id: STN_RNFR
           name: Renfrew

         - id: STN_ABTI
           name: Abbots Inch
       """

    yaml_file = tmp_path / "stations.yaml"
    yaml_file.write_text(yaml_text)

    loader = StationYamlLoader(str(yaml_file))
    repo = YamlStationRepository(loader, platform_repo)

    with pytest.raises(KeyError):
        repo.get("NOPE")


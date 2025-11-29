import pytest

from src.domain.domain_enums import TrackBlockType
from src.infrastructure.data_sources.yaml.track_block_loader import TrackBlockYamlLoader

def test_yaml_is_loaded(tmp_path):
    yaml_file = tmp_path / "track_blocks.yaml"
    yaml_file.write_text("""
    track_blocks:
      - id: BLK_10
        name: Renfrew P1 Block
        block_type: PLATFORM
        station_id: STN_RNFR
        dwell_time_minutes: 1
        platform_number: 1
    
      - id: BLK_11
        name: Renfrew P2 Block
        block_type: PLATFORM
        station_id: STN_RNFR
        dwell_time_minutes: 1
        platform_number: 2
    
      - id: BLK_UNLOAD_1
        name: Fuel Unload Road 1
        block_type: INDUSTRY
        industry_id: IND_FUEL
        load_time_minutes: 10
    
      - id: BLK_MAIN_1
        name: Mainline Between Renfrew–Abbots Inch
        block_type: MAINLINE
    """)

    loader = TrackBlockYamlLoader(str(yaml_file))
    data = loader.load()

    assert "track_blocks" in data
    assert data["track_blocks"][0]['id'] == "BLK_10"

def test_validation_for_invalid_yaml(tmp_path):
    yaml_file = tmp_path / "track_blocks.yaml"
    yaml_file.write_text("""
    - hello
    - world
    """)

    loader = TrackBlockYamlLoader(str(yaml_file))
    with pytest.raises(ValueError):
        loader.load()

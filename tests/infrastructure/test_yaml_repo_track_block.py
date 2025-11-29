import pytest

from src.domain.domain_enums import TrackBlockType, TrackBlockClass
from src.domain.track.track_block import TrackBlock, PlatformTrackBlock, IndustryTrackBlock
from src.infrastructure.data_sources.yaml.track_block_loader import TrackBlockYamlLoader
from src.infrastructure.repository.yaml.yaml_track_block_repository import YamlTrackBlockRepository

def test_track_block_repo_loads_plain_block(tmp_path):
    yaml_text = """
    track_blocks:
      - id: BLK_MAIN_1
        name: Mainline Section
        block_type: MAINLINE
        block_class: MAINLINE
    """

    yaml_file = tmp_path / "track_blocks.yaml"
    yaml_file.write_text(yaml_text)

    repo = YamlTrackBlockRepository(TrackBlockYamlLoader(str(yaml_file)))

    block = repo.get("BLK_MAIN_1")

    assert isinstance(block,TrackBlock)
    assert block.id == "BLK_MAIN_1"
    assert block.name == "Mainline Section"
    assert block.track_block_type == TrackBlockType.MAINLINE
    assert block.track_block_class == TrackBlockClass.MAINLINE
    assert len(repo.get_all()) == 1

def test_track_block_repo_loads_platform_block(tmp_path):
    yaml_text = """
    track_blocks:
      - id: BLK_P1
        name: Renfrew Platform 1
        block_type: PLATFORM_TRACK
        block_class: PLATFORM
        station_id: STN_RNFR
        dwell_time_minutes: 1
        platform_number: 1
    """

    yaml_file = tmp_path / "track_blocks.yaml"
    yaml_file.write_text(yaml_text)

    repo = YamlTrackBlockRepository(TrackBlockYamlLoader(str(yaml_file)))

    block = repo.get("BLK_P1")

    assert isinstance(block,PlatformTrackBlock)
    assert block.id == "BLK_P1"
    assert block.name == "Renfrew Platform 1"
    assert block.station_id == "STN_RNFR"
    assert block.track_block_type == TrackBlockType.PLATFORM_TRACK
    assert block.track_block_class == TrackBlockClass.PLATFORM
    assert block.dwell_time_minutes == 1
    assert block.platform_number == 1
    assert len(repo.get_all()) == 1
    assert len(repo.get_all_platform_blocks()) == 1
    assert type(repo.get_all_platform_blocks()[0]) is PlatformTrackBlock
    assert repo.get_all_industry_blocks() == []


def test_track_block_repo_loads_industry_block(tmp_path):
    yaml_text = """
    track_blocks:
      - id: BLK_FUEL
        name: Fuel Loading Road
        block_type: SIDING
        block_class: INDUSTRY
        industry_id: IND_FUEL
        load_time_minutes: 10
    """

    yaml_file = tmp_path / "track_blocks.yaml"
    yaml_file.write_text(yaml_text)

    repo = YamlTrackBlockRepository(TrackBlockYamlLoader(str(yaml_file)))

    block = repo.get("BLK_FUEL")

    assert isinstance(block, IndustryTrackBlock)
    assert block.industry_id == "IND_FUEL"
    assert block.load_time_minutes == 10
    assert block.track_block_type == TrackBlockType.SIDING
    assert block.track_block_class == TrackBlockClass.INDUSTRY
    assert type(repo.get_all_industry_blocks()[0]) is IndustryTrackBlock
    assert repo.get_all_platform_blocks() == []


def test_track_block_repo_raises_for_missing_id(tmp_path):
    yaml_text = """
    track_blocks:
      - id: BLK_MAIN_1
        name: Mainline
        block_type: MAINLINE
        block_class: MAINLINE
    """

    yaml_file = tmp_path / "track_blocks.yaml"
    yaml_file.write_text(yaml_text)

    repo = YamlTrackBlockRepository(TrackBlockYamlLoader(str(yaml_file)))

    with pytest.raises(KeyError):
        repo.get("NOPE")


def test_track_block_loader_rejects_invalid_yaml(tmp_path):
    yaml_file = tmp_path / "track_blocks.yaml"
    yaml_file.write_text("""
    - not a dict
    - still broken
    """)

    loader = TrackBlockYamlLoader(str(yaml_file))

    with pytest.raises(ValueError):
        loader.load()

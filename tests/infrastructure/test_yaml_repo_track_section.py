import pytest

from src.infrastructure.data_sources.yaml.track_section_loader import TrackSectionYamlLoader
from src.infrastructure.repository.yaml.yaml_track_section_repository import YamlTrackSectionRepository


def test_track_section_repo_loads_track_section_correctly(tmp_path):
    yaml_text = """
    track_sections:
      - id: SEC_01
        block_id: BLK_MAIN_1
        start_junction_id: J_RNFR_EAST
        end_junction_id: J_ABTI_WEST
        length_mm: 1000
        max_speed: 80
        """

    yaml_file = tmp_path / "track_sections.yaml"
    yaml_file.write_text(yaml_text)

    loader = TrackSectionYamlLoader(str(yaml_file))
    repo = YamlTrackSectionRepository(loader)

    track_section = repo.get("SEC_01")

    assert track_section.block_id == "BLK_MAIN_1"
    assert track_section.start_junction_id == "J_RNFR_EAST"
    assert track_section.end_junction_id == "J_ABTI_WEST"
    assert track_section.length_mm == 1000
    assert track_section.max_speed == 80

def test_repo_raises_for_missing_track_sections(tmp_path):
    yaml_text = """
    track_sections:
      - id: SEC_01
        block_id: BLK_MAIN_1
        start_junction_id: J_RNFR_EAST
        end_junction_id: J_ABTI_WEST
        length_mm: 1000
        max_speed: 80
    """

    yaml_file = tmp_path / "track_sections.yaml"
    yaml_file.write_text(yaml_text)

    loader = TrackSectionYamlLoader(str(yaml_file))
    repo = YamlTrackSectionRepository(loader)

    with pytest.raises(KeyError):
        repo.get("NOPE")
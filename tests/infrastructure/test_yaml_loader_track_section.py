import pytest

from src.infrastructure.data_sources.yaml.track_section_loader import TrackSectionYamlLoader

def test_yaml_is_loaded(tmp_path):
    yaml_file = tmp_path / "track_sections.yaml"
    yaml_file.write_text("""
    track_sections:
      - id: SEC_01
        block_id: BLK_MAIN_1
        start_junction_id: J_RNFR_EAST
        end_junction_id: J_ABTI_WEST
        length_mm: 1200
        max_speed: 80
    """)

    loader = TrackSectionYamlLoader(str(yaml_file))
    data = loader.load()

    assert "track_sections" in data
    assert data["track_sections"][0]["id"] == "SEC_01"

def test_validation_for_invalid_yaml(tmp_path):
    yaml_file = tmp_path / "track_sections.yaml"
    yaml_file.write_text("""
    - hello
    - world
    """)

    loader = TrackSectionYamlLoader(str(yaml_file))
    with pytest.raises(ValueError):
        loader.load()

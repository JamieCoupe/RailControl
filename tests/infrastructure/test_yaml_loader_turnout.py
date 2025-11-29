import pytest

from railcontrol.infrastructure.data_sources.yaml.turnout_loader import TurnoutYamlLoader


def test_yaml_is_loaded(tmp_path):
    yaml_file = tmp_path / "turnouts.yaml"
    yaml_file.write_text("""
    turnouts:
      - id: T01
        name: Renfrew East
        turnout_type: STANDARD_LEFT
        straight_section_id: SEC_05
        diverging_section_id: SEC_06
        current_state: STRAIGHT
    
      - id: T02
        name: Abbots Inch West
        turnout_type: STANDARD_RIGHT
        straight_section_id: SEC_10
        diverging_section_id: SEC_11
        current_state: DIVERGING
    """)

    loader = TurnoutYamlLoader(str(yaml_file))
    data = loader.load()

    assert "turnouts" in data
    assert data["turnouts"][0]["id"] == "T01"

def test_validation_for_invalid_yaml(tmp_path):
    yaml_file = tmp_path / "turnouts.yaml"
    yaml_file.write_text("""
    - hello
    - world
    """)

    loader = TurnoutYamlLoader(str(yaml_file))
    with pytest.raises(ValueError):
        loader.load()

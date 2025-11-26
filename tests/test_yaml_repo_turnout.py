import pytest

from src.domain.domain_enums import TurnoutType, TurnoutState
from src.infrastructure.data_sources.yaml.turnout_loader import TurnoutYamlLoader
from src.infrastructure.repository.yaml.yaml_turnout_repository import YamlTurnoutRepository


def test_turnout_repo_loads_turnouts_correctly(tmp_path):
    yaml_text = """
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
        """

    yaml_file = tmp_path / "turnouts.yaml"
    yaml_file.write_text(yaml_text)

    loader = TurnoutYamlLoader(str(yaml_file))
    repo = YamlTurnoutRepository(loader)

    turnout = repo.get("T01")

    assert turnout.name == "Renfrew East"
    assert turnout.turnout_type == TurnoutType.STANDARD_LEFT
    assert turnout.straight_section_id == "SEC_05"
    assert turnout.diverging_section_id == "SEC_06"
    assert turnout.current_state == TurnoutState.STRAIGHT

def test_validation_for_invalid_yaml(tmp_path):
    yaml_file = tmp_path / "turnouts.yaml"
    yaml_file.write_text("""
    - hello
    - world
    """)

    loader = TurnoutYamlLoader(str(yaml_file))
    with pytest.raises(ValueError):
        loader.load()

def test_turnout_repo_loads_turnouts_by_section(tmp_path):
    yaml_text = """
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
        """

    yaml_file = tmp_path / "turnouts.yaml"
    yaml_file.write_text(yaml_text)

    loader = TurnoutYamlLoader(str(yaml_file))
    repo = YamlTurnoutRepository(loader)

    turnout = repo.get_by_section("SEC_05")

    assert turnout.name == "Renfrew East"
    assert turnout.turnout_type == TurnoutType.STANDARD_LEFT
    assert turnout.straight_section_id == "SEC_05"
    assert turnout.diverging_section_id == "SEC_06"
    assert turnout.current_state == TurnoutState.STRAIGHT
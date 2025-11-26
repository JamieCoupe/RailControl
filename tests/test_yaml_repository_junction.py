import pytest

from src.domain.domain_enums import JunctionType
from src.infrastructure.data_sources.yaml.junction_loader import JunctionYamlLoader
from src.infrastructure.repository.yaml.yaml_junction_repository import YamlJunctionRepository


def test_junction_repo_loads_junctions_correctly(tmp_path):
    yaml_text = """
    junctions:
      - id: J1
        name: Renfrew East Junction
        type: plain

      - id: J2
        name: Renfrew West Junction
        type: crossover
    """

    yaml_file = tmp_path / "junctions.yaml"
    yaml_file.write_text(yaml_text)

    loader = JunctionYamlLoader(str(yaml_file))
    repo = YamlJunctionRepository(loader)

    j1 = repo.get("J1")
    j2 = repo.get("J2")

    assert j1.junction_id == "J1"
    assert j1.name == "Renfrew East Junction"
    assert j1.junction_type == JunctionType.PLAIN

    assert j2.junction_type == JunctionType.CROSSOVER


def test_junction_repo_raises_for_missing_id(tmp_path):
    yaml_text = """
    junctions:
      - id: J1
        name: Test Junction
        type: plain
    """

    yaml_file = tmp_path / "junctions.yaml"
    yaml_file.write_text(yaml_text)

    loader = JunctionYamlLoader(str(yaml_file))
    repo = YamlJunctionRepository(loader)

    with pytest.raises(KeyError):
        repo.get("NOPE")

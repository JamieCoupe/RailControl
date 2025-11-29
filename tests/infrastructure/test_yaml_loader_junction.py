import pytest
from railcontrol.infrastructure.data_sources.yaml.junction_loader import JunctionYamlLoader


def test_junction_loader_reads_yaml(tmp_path):
    yaml_text = """
    junctions:
      - junction_id: J1
        name: Renfrew East
        type: standard
    """

    yaml_file = tmp_path / "junctions.yaml"
    yaml_file.write_text(yaml_text)

    loader = JunctionYamlLoader(str(yaml_file))
    data = loader.load()

    assert "junctions" in data
    assert data["junctions"][0]["junction_id"] == "J1"
    assert data["junctions"][0]["type"] == "standard"


def test_junction_loader_rejects_invalid_yaml(tmp_path):
    yaml_file = tmp_path / "junctions.yaml"
    yaml_file.write_text("""
    - not
    - a
    - dict
    """)

    loader = JunctionYamlLoader(str(yaml_file))

    with pytest.raises(ValueError):
        loader.load()

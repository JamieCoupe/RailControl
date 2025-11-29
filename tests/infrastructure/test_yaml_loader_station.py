from railcontrol.infrastructure.data_sources.yaml.industry_loader import IndustryYamlLoader
import pytest

def test_yaml_is_loaded(tmp_path):
    yaml_file = tmp_path / "industries.yaml"
    yaml_file.write_text("""
    industries:
      - id: IND_TEST
        name: Test Industry
        industry_type: TEST
        inputs: []
        outputs: []
    """)

    loader = IndustryYamlLoader(str(yaml_file))
    data = loader.load()

    assert "industries" in data
    assert data["industries"][0]["id"] == "IND_TEST"

def test_validation_for_invalid_yaml(tmp_path):
    yaml_file = tmp_path / "industries.yaml"
    yaml_file.write_text("""
    - hello
    - world
    """)

    loader = IndustryYamlLoader(str(yaml_file))
    with pytest.raises(ValueError):
        loader.load()

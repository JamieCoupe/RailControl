from railcontrol.infrastructure.data_sources.yaml.commodity_loader import CommodityYamlLoader
import pytest

def test_yaml_is_loaded(tmp_path):
    yaml_file = tmp_path / "commodities.yml"
    yaml_file.write_text("""
    commodities:
      - id: COAL
        name: Coal
        unit: tons
        default_wagon_classification: HOPPER
    
      - id: OIL
        name: Crude Oil
        unit: tons
        default_wagon_classification: TANKER
    
      - id: AVGAS
        name: Aviation Gas
        unit: tons
        default_wagon_classification: TANKER
    """)

    loader = CommodityYamlLoader(str(yaml_file))
    data = loader.load()

    assert "commodities" in data
    assert data["commodities"][0]["id"] == "COAL"

def test_validation_for_invalid_yaml(tmp_path):
    yaml_file = tmp_path / "commodities.yml"
    yaml_file.write_text("""
    - hello
    - world
    """)

    loader = CommodityYamlLoader(str(yaml_file))
    with pytest.raises(ValueError):
        loader.load()

import pytest

from src.domain.domain_enums import WagonType
from src.infrastructure.data_sources.yaml.commodity_loader import CommodityYamlLoader
from src.infrastructure.repository.yaml.yaml_commodity_repository import YamlCommodityRepository


def test_commodity_repo_loads_commodity_correctly(tmp_path):
    # arrange: create YAML + repo
    yaml_text = """
    commodities:
      - id: COAL
        name: Coal
        unit: tons
        default_wagon_type: HOPPER
    
      - id: OIL
        name: Crude Oil
        unit: tons
        default_wagon_type: TANKER
    
      - id: AVGAS
        name: Aviation Gas
        unit: tons
        default_wagon_type: TANKER
        """

    yaml_file = tmp_path / "commodities.yaml"
    yaml_file.write_text(yaml_text)

    # act: load commodity
    loader = CommodityYamlLoader(str(yaml_file))
    repo = YamlCommodityRepository(loader)

    commodity = repo.get("COAL")

    assert commodity.name == "Coal"
    assert commodity.unit == "tons"
    assert commodity.default_wagon_type == WagonType.HOPPER

def test_repo_raises_for_missing_commodity(tmp_path):
    # arrange repo with valid YAML
    yaml_text = """
    commodities:
      - id: COAL
        name: Coal
        unit: tons
        default_wagon_type: HOPPER
    
      - id: OIL
        name: Crude Oil
        unit: tons
        default_wagon_type: TANKER
    
      - id: AVGAS
        name: Aviation Gas
        unit: tons
        default_wagon_type: TANKER
            """

    yaml_file = tmp_path / "commodities.yaml"
    yaml_file.write_text(yaml_text)

    # act: load Commodities
    loader = CommodityYamlLoader(str(yaml_file))
    repo = YamlCommodityRepository(loader)

    # act + assert
    with pytest.raises(KeyError):
        repo.get("NOPE")
import pytest

from railcontrol.domain.domain_enums import IndustryType
from railcontrol.infrastructure.data_sources.yaml.industry_loader import IndustryYamlLoader
from railcontrol.infrastructure.repository.yaml.yaml_industry_repository import YamlIndustryRepository


def test_industry_repo_loads_industries_correctly(tmp_path):
    # arrange: create YAML + repo
    yaml_text = """
        industries:
          - id: IND_COAL
            name: Coal Mine
            industry_type: mine
            inputs: []
            outputs:
              - commodity_id: COAL
                amount: 15
    
          - id: IND_STEEL
            name: Steel Works
            industry_type: factory
            inputs:
              - commodity_id: COAL
                amount: 10
            outputs: []
        """

    yaml_file = tmp_path / "industries.yaml"
    yaml_file.write_text(yaml_text)

    # act: load industries
    loader = IndustryYamlLoader(str(yaml_file))
    repo = YamlIndustryRepository(loader)

    ind = repo.get("IND_COAL")

    assert ind.name == "Coal Mine"
    assert ind.industry_type == IndustryType.MINE


def test_industry_repo_loads_inputs_outputs(tmp_path):
    # arrange: YAML with inputs + outputs
    yaml_text = """
            industries:
              - id: IND_COAL
                name: Coal Mine
                industry_type: mine
                inputs: []
                outputs:
                  - commodity_id: COAL
                    amount: 15

              - id: IND_STEEL
                name: Steel Works
                industry_type: factory
                inputs:
                  - commodity_id: COAL
                    amount: 10
                outputs: []
            """

    yaml_file = tmp_path / "industries.yaml"
    yaml_file.write_text(yaml_text)

    # act: load industries
    loader = IndustryYamlLoader(str(yaml_file))
    repo = YamlIndustryRepository(loader)

    # act
    inputs = repo.get_inputs("IND_STEEL")
    outputs = repo.get_outputs("IND_COAL")

    # assert
    assert len(inputs) == 1
    assert inputs[0].commodity_id == "COAL"
    assert inputs[0].amount == 10

    assert len(outputs) == 1
    assert outputs[0].commodity_id == "COAL"
    assert outputs[0].amount == 15

def test_repo_raises_for_missing_industry(tmp_path):
    # arrange repo with valid YAML
    yaml_text = """
            industries:
              - id: IND_COAL
                name: Coal Mine
                industry_type: mine
                inputs: []
                outputs:
                  - commodity_id: COAL
                    amount: 15

              - id: IND_STEEL
                name: Steel Works
                industry_type: factory
                inputs:
                  - commodity_id: COAL
                    amount: 10
                outputs: []
            """

    yaml_file = tmp_path / "industries.yaml"
    yaml_file.write_text(yaml_text)

    # act: load industries
    loader = IndustryYamlLoader(str(yaml_file))
    repo = YamlIndustryRepository(loader)

    # act + assert
    with pytest.raises(KeyError):
        repo.get("NOPE")
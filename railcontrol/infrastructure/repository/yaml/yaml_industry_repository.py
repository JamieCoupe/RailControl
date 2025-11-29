# src/infrastructure/repositories/yaml_industry_repository.py
from railcontrol.domain.domain_enums import IndustryType
from railcontrol.domain.industry.industry import Industry
from railcontrol.domain.industry.industry_input import IndustryInput
from railcontrol.domain.industry.industry_output import IndustryOutput
from railcontrol.infrastructure.repository.industry_repository import IndustryRepository

from railcontrol.infrastructure.data_sources.yaml.industry_loader import IndustryYamlLoader

class YamlIndustryRepository(IndustryRepository):

    def __init__(self, loader: IndustryYamlLoader):
        raw = loader.load()

        self._industries: dict [str, Industry] = {}
        self._industry_inputs: dict [str, list[IndustryInput]] = {}
        self._industry_outputs: dict [str, list[IndustryOutput]] = {}

        for raw_industry in raw["industries"]:
            industry = Industry(
                raw_industry["id"],
                raw_industry["name"],
                IndustryType[raw_industry["industry_type"].upper()]
            )
            self._industries[industry.id] = industry

            industry_inputs = []
            for raw_industry_input in raw_industry.get('inputs', []) or []:
                industry_inputs.append(IndustryInput(
                                            raw_industry['id'],
                                            raw_industry_input["commodity_id"],
                                            raw_industry_input["amount"]))

            self._industry_inputs[industry.id] = industry_inputs

            industry_outputs = []
            for raw_industry_output in raw_industry.get('outputs', []) or []:
                industry_outputs.append(IndustryOutput(
                                            raw_industry['id'],
                                            raw_industry_output["commodity_id"],
                                            raw_industry_output["amount"]))

            self._industry_outputs[industry.id] = industry_outputs


    def get(self, industry_id: str) -> Industry:
        return self._industries[industry_id]

    def get_all(self) -> list[Industry]:
        return list(self._industries.values())

    def get_inputs(self, industry_id: str) -> list[IndustryInput]:
        return self._industry_inputs[industry_id]

    def get_outputs(self, industry_id: str) -> list[IndustryOutput]:
        return self._industry_outputs[industry_id]

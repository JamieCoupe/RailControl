from src.domain.industry.industry import Industry
from src.domain.industry.industry_input import IndustryInput
from src.domain.industry.industry_output import IndustryOutput


class IndustryRepository:
    def get(self, industry_id: str) -> Industry:
        raise NotImplementedError
    def get_all(self) -> list[Industry]:
        raise NotImplementedError
    def get_inputs(self, industry_id) -> list[IndustryInput]:
        raise NotImplementedError
    def get_outputs(self,industry_id) -> list[IndustryOutput]:
        raise NotImplementedError


from src.domain.industry.industry_input import IndustryInput

class IndustryInputRepository:
    def get(self, industry_input_id: str) -> IndustryInput:
        raise NotImplementedError
    def list_all(self) -> list[IndustryInput]:
        raise NotImplementedError


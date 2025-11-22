from src.domain import IndustryOutput

class IndustryOutputRepository:
    def get(self, industry_output_id: str) -> IndustryOutput:
        raise NotImplementedError
    def list_all(self) -> list[IndustryOutput]:
        raise NotImplementedError


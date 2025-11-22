from src.domain import Industry

class IndustryRepository:
    def get(self, industry_id: str) -> Industry:
        raise NotImplementedError
    def list_all(self) -> list[Industry]:
        raise NotImplementedError


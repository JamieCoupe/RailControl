from src.domain.industry.commodity import Commodity

class CommodityRepository:
    def get(self, commmodity_id: str) -> Commodity:
        raise NotImplementedError
    def list_all(self) -> list[Commodity]:
        raise NotImplementedError

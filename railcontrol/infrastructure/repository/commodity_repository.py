from railcontrol.domain.freight.commodity import Commodity

class CommodityRepository:
    def get(self, commodity_id: str) -> Commodity:
        raise NotImplementedError
    def get_all(self) -> list[Commodity]:
        raise NotImplementedError

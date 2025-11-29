from railcontrol.domain.domain_enums import WagonType
from railcontrol.domain.freight.commodity import Commodity
from railcontrol.domain.rolling_stock.wagon_classification import WagonClassification
from railcontrol.infrastructure.repository.commodity_repository import CommodityRepository

from railcontrol.infrastructure.data_sources.yaml.commodity_loader import CommodityYamlLoader


class YamlCommodityRepository(CommodityRepository):

    def __init__(self, loader: CommodityYamlLoader):
        raw = loader.load()

        self._commodities: dict [str, Commodity] = {}

        for raw_commodity in raw["commodities"]:
            commodity = Commodity(
                raw_commodity['id'],
                raw_commodity['name'],
                raw_commodity['unit'],
                WagonType[raw_commodity['default_wagon_type'].upper()]
                )
            self._commodities[raw_commodity['id']] = commodity

    def get(self, commodity_id: str) -> Commodity:
        return self._commodities[commodity_id]

    def get_all(self) -> list[Commodity]:
        return list(self._commodities.values())
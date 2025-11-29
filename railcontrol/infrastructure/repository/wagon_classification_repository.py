from railcontrol.domain.rolling_stock.wagon_classification import WagonClassification

class WagonClassificationRepositry:
    def get(self, wagon_classification_id: str) -> WagonClassification:
        raise NotImplementedError
    def list_all(self) -> list[WagonClassification]:
        raise NotImplementedError

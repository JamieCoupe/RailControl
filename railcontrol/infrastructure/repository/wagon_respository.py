from railcontrol.domain.rolling_stock.wagon import Wagon

class WagonRepositry:
    def get(self, wagon_id: str) -> Wagon:
        raise NotImplementedError
    def list_all(self) -> list[Wagon]:
        raise NotImplementedError

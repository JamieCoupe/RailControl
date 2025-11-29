from railcontrol.domain.freight.waybill import Waybill

class WaybillRepositry:
    def get(self, wagon_id: str) -> Waybill:
        raise NotImplementedError
    def list_all(self) -> list[Waybill]:
        raise NotImplementedError

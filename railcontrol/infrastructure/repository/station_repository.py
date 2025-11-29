from railcontrol.domain.station.station import Station

class StationRepository:
    def get(self, station_id: str) -> Station:
        raise NotImplementedError
    def get_all(self) -> list[Station]:
        raise NotImplementedError

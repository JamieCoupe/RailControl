from railcontrol.domain.station.station import Station
from railcontrol.infrastructure.repository.station_repository import StationRepository
from railcontrol.infrastructure.data_sources.yaml.station_loader import StationYamlLoader
from railcontrol.infrastructure.repository.track_block_repository import TrackBlockRepository


class YamlStationRepository(StationRepository):

    def __init__(self, loader: StationYamlLoader, track_block_repo: TrackBlockRepository):
        raw = loader.load()
        self._stations: dict[str, Station] = {}

        for raw_station in raw["stations"]:
            station = Station(
                raw_station['id'],
                raw_station['name'],
                track_block_repo.get_by_station(raw_station['id'])
            )
            self._stations[raw_station['id']] = station

    def get(self, station_id: str) -> Station:
        return self._stations[station_id]

    def get_all(self) -> list[Station]:
        return list(self._stations.values())
from src.domain.domain_enums import Direction
from src.domain.station.passenger_stop import PassengerStop
from src.domain.timetable.passenger_route import PassengerRoute
from src.infrastructure.data_sources.yaml.passenger_route_loader import PassengerRouteYamlLoader
from src.infrastructure.repository.passenger_route_repository import PassengerRouteRepository


class YamlPassengerRouteRepository(PassengerRouteRepository):

    def __init__(self, loader: PassengerRouteYamlLoader):
        raw = loader.load()

        self._passenger_routes: dict[str, PassengerRoute] = {}

        for raw_passenger_route in raw["passenger_routes"]:
            stops = []

            raw_stops = raw_passenger_route['stops'] or []
            for stop in raw_stops:
                stops.append(PassengerStop(
                    stop['station_id'],
                    stop.get('dwell_time'),
                    stop.get('platform'),
                    stop.get('is_request_stop', False)
                ))

            passenger_route = PassengerRoute(
                raw_passenger_route['id'],
                raw_passenger_route['name'],
                stops,
                Direction[raw_passenger_route['direction'].upper()]
                )
            self._passenger_routes[raw_passenger_route['id']] = passenger_route

    def get(self, passenger_route_id: str) -> PassengerRoute:
        return self._passenger_routes[passenger_route_id]

    def get_all(self) -> list[PassengerRoute]:
        return list(self._passenger_routes.values())

    def get_by_station(self, station_id: str) -> list[PassengerRoute]:
        return [
            route
            for route in self._passenger_routes.values()
            if any(stop.station_id == station_id for stop in route.stops)
        ]
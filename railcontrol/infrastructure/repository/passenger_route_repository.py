from railcontrol.domain.timetable.passenger_route import PassengerRoute

class PassengerRouteRepository:
    def get(self, passenger_route_id: str) -> PassengerRoute:
        raise NotImplementedError
    def get_all(self) -> list[PassengerRoute]:
        raise NotImplementedError
    def get_by_station(self, station_id: str) -> list[PassengerRoute]:
        raise NotImplementedError

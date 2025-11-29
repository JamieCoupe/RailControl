from railcontrol.domain.domain_enums import Direction
from railcontrol.domain.station.passenger_stop import PassengerStop


class PassengerRoute:
    def __init__(self, id: str, name: str, stops: list[PassengerStop], direction: Direction | None = None):
        self.id = id
        self.name = name
        self.stops = stops
        self.direction = direction

    def get_station_ids(self):
        return [stop.station_id for stop in self.stops]
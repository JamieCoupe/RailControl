from railcontrol.domain.domain_enums import Direction
from railcontrol.domain.timetable.expanded_passenger_leg import ExpandedPassengerLeg


class ExpandedPassengerRoute:
    def __init__(self, legs: list[ExpandedPassengerLeg], direction: Direction):
        self.legs = legs
        self.direction = direction

    def total_distance_mm(self):
        return sum(
            edge.length_mm
            for leg in self.legs
            for edge in leg.inbound_path_edges
        )

    def total_time(self, start_time_seconds):
        raise NotImplementedError

    def stations(self):
        return [leg.station_id for leg in self.legs]

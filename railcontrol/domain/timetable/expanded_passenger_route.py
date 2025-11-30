from railcontrol.domain.domain_enums import Direction
from railcontrol.domain.timetable.expanded_passenger_leg import ExpandedPassengerLeg


class ExpandedPassengerRoute:
    def __init__(self, legs: list[ExpandedPassengerLeg], direction: Direction):
        self.legs = legs
        self.direction = direction

    def stations(self):
        return [leg.station_id for leg in self.legs]

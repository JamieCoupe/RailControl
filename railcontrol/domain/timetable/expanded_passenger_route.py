from railcontrol.domain.timetable.expanded_passenger_leg import ExpandedPassengerLeg


class ExpandedPassengerRoute:
    def __init__(self, legs: list[ExpandedPassengerLeg]):
        self.legs = legs

    def total_distance_mm(self):
        return sum(
            edge.length_mm
            for leg in self.legs
            for edge in leg.inbound_path_edges
        )

    def expand_times(self, expanded_route, start_time_seconds):
        """
        Given an ExpandedPassengerRoute with legs resolved,
        compute the arrival/departure times at each stop.

        Implementation:
          - NOT YET. This is Lesson 9.7.
        """
        raise NotImplementedError

    def stations(self):
        return [leg.station_id for leg in self.legs]

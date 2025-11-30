from railcontrol.application.timetable.running_time_calculator import RunningTimeCalculator
from railcontrol.domain.timetable.expanded_passenger_route import ExpandedPassengerRoute


class RunningTimeEngine:
    def __init__(self, calculator: RunningTimeCalculator):
        self.calculator = calculator

    def compute_for_route(self, expanded_route: ExpandedPassengerRoute, profile: str):
        for leg in expanded_route.legs:

            leg.total_length_mm = (
                sum(edge.length_mm for edge in leg.inbound_path_edges)
                + leg.platform_length_mm
            )

            # Per-leg timing
            leg_calc = self.calculator.calculate_leg_travel_time(leg, profile)
            leg.running_time_s = leg_calc["time_s"]
            leg.effective_speed_mph = leg_calc["effective_speed_mph"]
            leg.raw_time_s = leg_calc["raw_time_s"]
            leg.dwell_used_s = leg_calc["dwell_s"]
            leg.padding_s = leg_calc["padding_s"]

            # Per-edge timing breakdown
            leg.edge_calculations = [
                self.calculator.calculate_edge_travel_time(edge, profile)
                for edge in leg.inbound_path_edges
            ]

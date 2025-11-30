from railcontrol.application.utils.scale_conversion import travel_time_seconds
from railcontrol.application.timetable.timetable_profile import TimetableProfile
from railcontrol.domain.timetable.expanded_passenger_leg import ExpandedPassengerLeg


class RunningTimeCalculator:

    def calculate_leg_travel_time(self, leg: ExpandedPassengerLeg, profile: str) -> dict:
        leg_length = (
            sum(edge.length_mm for edge in leg.inbound_path_edges)
            + leg.platform_length_mm
        )

        if leg.inbound_path_edges:
            effective_max_speed = min(edge.max_speed for edge in leg.inbound_path_edges)
        else:
            effective_max_speed = leg.platform_max_speed

        speed_profile = TimetableProfile.get_profile(profile)
        effective_speed = max(1, int(effective_max_speed * speed_profile["speed_factor"]))

        raw_time = travel_time_seconds(leg_length, effective_speed)

        dwell_used = max(leg.dwell_time, speed_profile["minimum_dwell"])
        total = int(raw_time + dwell_used + speed_profile["padding_seconds"])

        return {
            "time_s": total,
            "effective_speed_mph": effective_speed,
            "raw_time_s": raw_time,
            "dwell_s": dwell_used,
            "padding_s": speed_profile["padding_seconds"],
        }

    def calculate_edge_travel_time(self, edge, profile: str) -> dict:
        speed_profile = TimetableProfile.get_profile(profile)
        effective_speed = max(1, int(edge.max_speed * speed_profile["speed_factor"]))

        raw_time = travel_time_seconds(edge.length_mm, effective_speed)

        return {
            "time_s": int(raw_time),
            "effective_speed_mph": effective_speed,
            "raw_time_s": raw_time,
            "length_mm": edge.length_mm,
            "block_id": edge.track_block_id,
        }

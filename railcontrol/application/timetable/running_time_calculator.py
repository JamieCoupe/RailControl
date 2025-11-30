from railcontrol.application.timetable.timetable_profile import TimeTableProfile
from railcontrol.application.utils.scale_conversion import travel_time_seconds
from railcontrol.domain.timetable.expanded_passenger_leg import ExpandedPassengerLeg


class RunningTimeCalculator:
    def __init__(self):
        pass

    def calculate_leg_travel_time(self, leg: ExpandedPassengerLeg, profile: str) -> int:
        leg_length = (
                sum(edge.length_mm for edge in leg.inbound_path_edges)
                + leg.platform_length_mm
        )

        if leg.inbound_path_edges:
            effective_max_speed = min(edge.max_speed for edge in leg.inbound_path_edges)
        else:
            effective_max_speed = leg.platform_max_speed


        speed_profile = TimeTableProfile.get_profile(profile_type=profile)

        effective_speed = max(
            1,
            int(effective_max_speed * speed_profile["speed_factor"])
        )


        raw_time = travel_time_seconds(leg_length, effective_speed)
        leg_travel_time = raw_time + speed_profile["padding_seconds"]

        return int(leg_travel_time)

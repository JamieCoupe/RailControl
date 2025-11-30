from railcontrol.domain.timetable.timetable_row import TimetableRow


class TimetableEngine:
    """
    Generates a fully timestamped timetable for an ExpandedPassengerRoute.
    """

    def generate_timetable(self, expanded_route, start_time_seconds: int):
        """
        Returns a list of TimetableRow objects with:
            - station_id
            - arrival_time_s
            - departure_time_s (None for the last station)
            - dwell_s
            - runtime_from_prev_s
        """

        legs = expanded_route.legs
        if not legs:
            raise ValueError("Expanded route contains no legs")

        timetable = []
        current_time = start_time_seconds

        # --- FIRST STATION ---
        first_leg = legs[0]

        arrival_s = current_time
        departure_s = arrival_s + first_leg.dwell_used_s

        timetable.append(
            TimetableRow(
                station_id=first_leg.station_id,
                arrival_s=arrival_s,
                departure_s=departure_s,
                dwell_s=first_leg.dwell_used_s,
                runtime_s=0  # no previous runtime
            )
        )

        current_time = departure_s

        # --- INTERMEDIATE STATIONS ---
        for leg in legs[1:-1]:  # everything except last station
            arrival_s = current_time + leg.running_time_s
            departure_s = arrival_s + leg.dwell_used_s

            timetable.append(
                TimetableRow(
                    station_id=leg.station_id,
                    arrival_s=arrival_s,
                    departure_s=departure_s,
                    dwell_s=leg.dwell_used_s,
                    runtime_s=leg.running_time_s,
                )
            )

            current_time = departure_s

        # --- LAST STATION ---
        last_leg = legs[-1]

        arrival_s = current_time + last_leg.running_time_s

        timetable.append(
            TimetableRow(
                station_id=last_leg.station_id,
                arrival_s=arrival_s,
                departure_s=None,     # terminating service
                dwell_s=0,
                runtime_s=last_leg.running_time_s,
            )
        )

        return timetable

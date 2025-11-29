class PassengerTimetableService:
    """
    Generates a fully timestamped timetable for an ExpandedPassengerRoute.
    """

    def generate_timetable(self, expanded_route, start_time_seconds: int):
        """
        Return a list of dicts, each containing:
            - station_id
            - arrival_time
            - departure_time
            - platform_block_id
        """

        timetable_rows = []
        current_time = start_time_seconds

        legs = expanded_route.legs
        if not legs:
            raise ValueError("Expanded route contains no legs")

        # --- Handle first station ---
        first_leg = legs[0]

        arrival_time = current_time
        departure_time = arrival_time + first_leg.dwell_time

        timetable_rows.append({
            "station_id": first_leg.station_id,
            "arrival_time": arrival_time,
            "departure_time": departure_time,
            "platform_block_id": first_leg.platform_block_id,
        })

        current_time = departure_time

        # --- Handle subsequent stations ---
        for leg in legs[1:]:
            # inbound_path_edges contain full path from previous stop
            travel_time = sum(edge.weight for edge in leg.inbound_path_edges)

            arrival_time = current_time + travel_time
            departure_time = arrival_time + leg.dwell_time

            timetable_rows.append({
                "station_id": leg.station_id,
                "arrival_time": arrival_time,
                "departure_time": departure_time,
                "platform_block_id": leg.platform_block_id,
            })

            current_time = departure_time

        return timetable_rows

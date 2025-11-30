class TimetableValidator:

    @staticmethod
    def validate(rows):
        if not rows:
            raise ValueError("Empty timetable")

        prev_arr = None
        for row in rows:
            if prev_arr is not None:
                if row.arrival_s < prev_arr:
                    raise ValueError("Non-monotonic timetable: times go backwards")

            if row.departure_s is not None:
                if row.departure_s < row.arrival_s:
                    raise ValueError("Departure before arrival")

            prev_arr = row.arrival_s
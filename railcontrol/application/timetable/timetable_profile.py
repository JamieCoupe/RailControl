class TimeTableProfile:

    @staticmethod
    def get_profile(profile_type: str) -> dict:
        if profile_type == "express":
            return {
                "speed_factor": 1.1,
                "minimum_dwell": 10,
                "padding_seconds": 3,
            }

        elif profile_type == "stopping":
            return {
                "speed_factor": 0.9,
                "minimum_dwell": 20,
                "padding_seconds": 5,
            }

        else:
            raise KeyError(f"{profile_type} is not a defined profile type")
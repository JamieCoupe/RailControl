from railcontrol.application.application_enums import TimetableProfileTypes


class TimetableProfile:

    @staticmethod
    def get_profile(profile_type: str) -> dict:
        match profile_type:
            case TimetableProfileTypes.EXPRESS.value:
                return {
                    "speed_factor": 1.05,
                    "minimum_dwell": 15,
                    "padding_seconds": 3,
                }
            case TimetableProfileTypes.STOPPING.value:
                return {
                    "speed_factor": 0.85,
                    "minimum_dwell": 30,
                    "padding_seconds": 8,
                }

            case TimetableProfileTypes.ECS.value:
                return {
                    "speed_factor": 0.9,
                    "minimum_dwell": 5,
                    "padding_seconds": 3,
                }
            case TimetableProfileTypes.LIGHT_ENGINE.value:
                return {
                    "speed_factor": 1,
                    "minimum_dwell": 5,
                    "padding_seconds": 2,
                }
            case _:
                raise KeyError(f"{profile_type} is not a defined profile type")
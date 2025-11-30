from railcontrol.application.application_enums import TimetableProfileTypes
from railcontrol.application.dto.route_result import RouteResult
from railcontrol.domain.domain_enums import Direction
from railcontrol.domain.timetable.expanded_passenger_route import ExpandedPassengerRoute

class ServiceIDGenerator:
    def __init__(self):
        self.counter = 1

    def train_class_from_profile(self, profile: str) -> int:
        match profile:
            case TimetableProfileTypes.EXPRESS.value:
                return 1
            case TimetableProfileTypes.STOPPING.value:
                return 2
            case TimetableProfileTypes.ECS.value:
                return 5
            case TimetableProfileTypes.LIGHT_ENGINE.value:
                return 0
            case TimetableProfileTypes.FREIGHT_SLOW.value:
                return 7
            case TimetableProfileTypes.FREIGHT_FAST.value:
                return 4
            case TimetableProfileTypes.FREIGHT_HEAVY.value:
                return 6
            case _:
                raise KeyError(f"Invalid profile {profile}")

    def region_code_from_route(self,route: ExpandedPassengerRoute) -> str:
        region_code = "-"
        if route.direction in (Direction.UP, Direction.DOWN):
            region_code =  "S"

        return region_code

    def next_number(self) -> str:
        n = self.counter
        self.counter = (self.counter % 99) + 1
        return f"{n:02d}"

    def generate_headcode(self, profile: str, route, region_override=None):
        cls = self.train_class_from_profile(profile)
        region = region_override or self.region_code_from_route(route)
        num = self.next_number()
        return f"{cls}{region}{num}"


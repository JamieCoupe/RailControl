from railcontrol.application.routing.routing_edge import RoutingEdge

class ExpandedPassengerLeg:
    def __init__(
        self,
        station_id: str,
        platform_block_id: str | None,
        arrival_junction_id: str | None,
        departure_junction_id: str | None,
        inbound_path_edges: list[RoutingEdge],
        dwell_time: int,
        is_request_stop: bool,
        platform_length_mm: int,
        platform_max_speed: int,
    ):
        self.station_id = station_id
        self.platform_block_id = platform_block_id
        self.arrival_junction_id = arrival_junction_id
        self.departure_junction_id = departure_junction_id
        self.inbound_path_edges = inbound_path_edges
        self.dwell_time = max(0, dwell_time)
        self.is_request_stop = is_request_stop
        self.platform_length_mm = platform_length_mm
        self.platform_max_speed = platform_max_speed
        self.total_length_mm: int | None = None
        self.running_time_s: int | None = None
        self.effective_speed_mph: int | None = None

    def __repr__(self):
        return f"<Leg {self.station_id} platform={self.platform_block_id}>"

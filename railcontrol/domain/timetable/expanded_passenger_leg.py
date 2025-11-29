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
        is_request_stop: bool
    ):
        self.station_id = station_id
        self.platform_block_id = platform_block_id
        self.arrival_junction_id = arrival_junction_id
        self.departure_junction_id = departure_junction_id
        self.inbound_path_edges = inbound_path_edges  # path from previous station
        self.dwell_time = dwell_time
        self.is_request_stop = is_request_stop

    def __repr__(self):
        return f"<Leg {self.station_id} platform={self.platform_block_id}>"

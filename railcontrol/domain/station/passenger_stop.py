class PassengerStop:
    def __init__(
            self,
            station_id: str,
            dwell_time: int | None = None,
            platform_preference: int | None = None,
            is_request_stop:bool = False
    ):
        self.station_id = station_id
        self.dwell_time = dwell_time
        self.platform_preference = platform_preference
        self.is_request_stop = is_request_stop
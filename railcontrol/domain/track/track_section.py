class TrackSection:
    def __init__(
            self,
            id:str,
            block_id: str,
            start_junction_id: str,
            end_junction_id: str,
            length_mm: int,
            max_speed: int
        ):

        self.id = id
        self.block_id = block_id
        self.start_junction_id = start_junction_id
        self.end_junction_id = end_junction_id
        self.length_mm = length_mm
        self.max_speed = max_speed

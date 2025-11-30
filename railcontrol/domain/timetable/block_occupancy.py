from railcontrol.domain.domain_enums import Direction
from datetime import datetime

class BlockOccupancy:
    def __init__(
            self,
            block_id: str,
            t_entry: datetime,
            t_exit: datetime,
            service_id: str,
            direction: Direction,
            length_mm: int,
            max_speed: int,
            source_start_junction: str,
            source_end_junction: str
    ):
        self.block_id = block_id
        self.t_entry = t_entry
        self.t_exit = t_exit
        self.service_id = service_id
        self.direction = direction
        self.length_mm = length_mm
        self.max_speed = max_speed
        self.source_start_junction = source_start_junction
        self.source_end_junction = source_end_junction
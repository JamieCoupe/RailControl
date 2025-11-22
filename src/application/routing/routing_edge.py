class RoutingEdge:
    def __init__(
            self,
            from_node: str,
            to_node: str,
            track_section_id: str,
            track_block_id: str,
            length_mm: int,
            max_speed: int,
            weight:float,
            block_class: str,
            block_type: str
        ):

        self.from_node= from_node
        self.to_node = to_node
        self.track_section_id = track_section_id
        self.track_block_id = track_block_id
        self.length_mm = length_mm
        self.max_speed = max_speed
        self.weight = weight
        self.block_class = block_class
        self.block_type = block_type
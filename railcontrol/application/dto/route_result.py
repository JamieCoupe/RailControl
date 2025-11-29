class RouteResult:
    def __init__(
            self,
            node_ids: list[str],
            edge_ids: list[str],
            total_time_seconds: float,
            total_length_mm: int,
            block_ids:list[str],
            success: bool = True,
            message: str | None = None
            ):
        self.node_ids = node_ids
        self.edge_ids = edge_ids
        self.total_time_seconds = total_time_seconds
        self.total_length_mm = total_length_mm
        self.block_ids = block_ids
        self.success = success
        self.message = message
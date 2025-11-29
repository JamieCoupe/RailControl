from railcontrol.application.application_enums import RouteMode

class RouteRequest:
    def __init__(
        self,
        start_id: str,
        end_id: str,
        routing_mode: RouteMode,
        avoid_blocks: list[str] | None = None,
        avoid_block_types: list[str] | None = None,
        prefer_block_types: list[str] | None = None,
        max_train_speed: int | None = None,
        allow_reverse: bool = False,
        include_platforms: bool = True,
    ):
        self.start_id = start_id
        self.end_id = end_id
        self.routing_mode = routing_mode
        self.avoid_blocks = avoid_blocks or []
        self.avoid_block_types = avoid_block_types or []
        self.prefer_block_types = prefer_block_types or []
        self.max_train_speed = max_train_speed
        self.allow_reverse = allow_reverse
        self.include_platforms = include_platforms
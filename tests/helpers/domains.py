from src.domain.domain_enums import TrackBlockType, TurnoutType, TurnoutState


class StubJunction:
    def __init__(self, junction_id: str):
        self.junction_id = junction_id


class StubTrackSection:
    def __init__(self, section_id, start, end, block_id, length_mm=1000, max_speed=100):
        self.id = section_id
        self.start_junction_id = start
        self.end_junction_id = end
        self.block_id = block_id
        self.length_mm = length_mm
        self.max_speed = max_speed


class StubTrackBlock:
    def __init__(self, block_id, block_type=TrackBlockType.MAINLINE):
        self.block_id = block_id
        self.track_block_type = block_type


class StubTurnout:
    def __init__(self, turnout_id, straight_id, diverging_id, state=TurnoutState.STRAIGHT):
        from src.domain.domain_enums import TurnoutType
        self.id = turnout_id
        self.name = turnout_id
        self.turnout_type = TurnoutType.STANDARD_LEFT  # arbitrary
        self.straight_section_id = straight_id
        self.diverging_section_id = diverging_id
        self.current_state = state

    def get_active_section_id(self):
        return (
            self.straight_section_id
            if self.current_state == TurnoutState.STRAIGHT
            else self.diverging_section_id
        )

    def set_state(self, state):
        self.current_state = state

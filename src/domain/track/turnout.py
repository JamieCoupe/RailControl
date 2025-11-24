from src.domain.domain_enums import TurnoutType, TurnoutState

class Turnout:
    def __init__(self,
                 id: str,
                 name: str,
                 turnout_type: TurnoutType,
                 straight_section_id: str,
                 diverging_section_id: str,
                 current_state: TurnoutState
                 ):
        self.id = id
        self.name = name
        self.turnout_type = turnout_type
        self.straight_section_id = straight_section_id
        self.diverging_section_id = diverging_section_id
        self.current_state = current_state

    def get_active_section_id(self) -> str:
        """Returns the active section ID"""
        return (
            self.straight_section_id
            if self.current_state == TurnoutState.STRAIGHT
            else self.diverging_section_id
        )

    def set_state(self, new_state: TurnoutState):
        self.current_state = new_state
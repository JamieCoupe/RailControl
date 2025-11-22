from src.domain.track.turnout import Turnout

class TurnoutRepository:
    def get(self, turnout_id: str) -> Turnout:
        raise NotImplementedError
    def list_all(self) -> list[Turnout]:
        raise NotImplementedError

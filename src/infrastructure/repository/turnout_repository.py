from src.domain.track.turnout import Turnout

class TurnoutRepository:
    def get(self, turnout_id: str) -> Turnout:
        raise NotImplementedError
    def get_all(self) -> list[Turnout]:
        raise NotImplementedError
    def get_by_junction_id(self, junction_id: str) -> Turnout:
        raise NotImplementedError
    def get_by_block(self, block_id: str):
        raise NotImplementedError

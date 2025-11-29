from tests.helpers.domains import (
    StubJunction, StubTrackSection, StubTrackBlock, StubTurnout
)
from railcontrol.domain.domain_enums import TrackBlockType, TurnoutState


class StubJunctionRepository:
    """
    Provides:
      J1, J2, J3
    """
    def get_all(self):
        return [
            StubJunction("J1"),
            StubJunction("J2"),
            StubJunction("J3")
        ]


class StubTrackBlockRepository:
    """
    Provides:
      B1 as MAINLINE
    """
    def __init__(self):
        self.block = StubTrackBlock("B1", TrackBlockType.MAINLINE)

    def get(self, block_id):
        return self.block


class StubTrackSectionRepository:
    """
    Provides:
      S1: J1 -> J2 (straight leg)
      S2: J1 -> J3 (diverging leg)
    """
    def get_all(self):
        return [
            StubTrackSection("S1", "J1", "J2", "B1"),
            StubTrackSection("S2", "J1", "J3", "B1"),
        ]


class StubTurnoutRepository:
    """
    Provides turnout T1 controlling S1 (straight) and S2 (diverging)
    """
    def __init__(self, state: TurnoutState):
        self.turnout = StubTurnout("T1", "S1", "S2", state)

    def get_all(self):
        return [self.turnout]

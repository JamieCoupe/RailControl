from src.domain.domain_enums import TurnoutType, TurnoutState
from src.domain.track.turnout import Turnout
from src.infrastructure.repository.turnout_repository import TurnoutRepository
from src.infrastructure.data_sources.yaml.turnout_loader import TurnoutYamlLoader


class YamlTurnoutRepository(TurnoutRepository):

    def __init__(self, loader: TurnoutYamlLoader):
        raw = loader.load()

        self._turnouts: dict[str, Turnout] = {}
        self._by_section: dict[str, Turnout] = {}

        for raw_turnout in raw["turnouts"]:
            turnout = Turnout(
                raw_turnout['id'],
                raw_turnout['name'],
                TurnoutType[raw_turnout['turnout_type'].upper()],
                raw_turnout['straight_section_id'],
                raw_turnout['diverging_section_id'],
                TurnoutState[raw_turnout['current_state'].upper()]
                )
            self._turnouts[raw_turnout['id']] = turnout
            self._by_section[raw_turnout['straight_section_id']] = turnout
            self._by_section[raw_turnout['diverging_section_id']] = turnout

    def get(self, turnout_id: str) -> Turnout:
        return self._turnouts[turnout_id]

    def get_all(self) -> list[Turnout]:
        return list(self._turnouts.values())

    def get_by_section(self, section_id) -> Turnout | None:
        return self._by_section.get(section_id)
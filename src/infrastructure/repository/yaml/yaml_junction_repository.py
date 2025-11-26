from src.domain.domain_enums import JunctionType
from src.domain.track.junction import Junction
from src.infrastructure.data_sources.yaml.junction_loader import JunctionYamlLoader
from src.infrastructure.repository.junction_repository import JunctionRepository


class YamlJunctionRepository(JunctionRepository):
    def __init__(self, loader: JunctionYamlLoader):
        raw = loader.load()

        self._junctions = {}

        for j in raw["junctions"]:
            junction = Junction(
                j["id"],
                j["name"],
                JunctionType[j["type"].upper()]
            )
            self._junctions[j["id"]] = junction

    def get(self, junction_id: str) -> Junction:
        return self._junctions[junction_id]

    def get_all(self) -> list[Junction]:
        return list(self._junctions.values())

from src.domain.domain_enums import WagonType


class Commodity:
    def __init__(self, id: str, name:str, unit: str, default_wagon_type: WagonType):
        self.id = id
        self.name = name
        self.unit = unit
        self.default_wagon_type = default_wagon_type

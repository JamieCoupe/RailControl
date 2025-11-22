from src.domain.domain_enums import JunctionType

class Junction:
    def __init__(
            self,
            junction_id:str,
            name: str,
            junction_type: JunctionType
    ):
        self.junction_id = junction_id
        self.name = name
        self.junction_type = junction_type
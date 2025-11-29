from railcontrol.domain.domain_enums import IndustryType


class Industry:
    def __init__(self, id: str, name: str, industry_type: IndustryType):
        self.id = id
        self.name = name
        self.industry_type = industry_type
from enum import Enum

class RouteMode(Enum):
    FASTEST = "fastest"
    SHORTEST = "shortest"
    MAINLINE_ONLY = "mainline_only"
    AVOID_INDUSTRY = "avoid_industry"
    CUSTOM_WEIGHT = "custom_weight"
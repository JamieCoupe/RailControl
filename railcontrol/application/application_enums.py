from enum import Enum

class RouteMode(Enum):
    FASTEST = "fastest"
    SHORTEST = "shortest"
    MAINLINE_ONLY = "mainline_only"
    AVOID_INDUSTRY = "avoid_industry"
    CUSTOM_WEIGHT = "custom_weight"

class TimetableProfileTypes(Enum):
    EXPRESS = "express"
    STOPPING = "stopping"
    ECS = "ecs"
    LIGHT_ENGINE = "light_engine"
    FREIGHT_SLOW = "freight_slow"
    FREIGHT_FAST = "freight_fast"
    FREIGHT_HEAVY = "freight_heavy"

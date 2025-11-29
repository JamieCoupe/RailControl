from enum import Enum

class JunctionType(Enum):
    STANDARD = "standard"
    TURNOUT = "turnout"
    CROSSOVER = "crossover"
    BUFFER = "buffer"

class TrackBlockType(Enum):
    MAINLINE = "mainline"
    PASSING_LOOP = "passing_loop"
    BRANCH = "branch"
    SIDING = "siding"
    SHED = "shed"
    HEADSHUNT = "headshunt"
    PLATFORM_TRACK = "platform_track"
    LOADING = "loading_unloading"

class TrackBlockClass(Enum):
    PLATFORM = "platform"
    INDUSTRY = "industry"
    LOADING = "loading"
    STORAGE = "storage"
    MAINLINE = "mainline"

class TurnoutState(Enum):
    STRAIGHT = "straight"
    DIVERGING = "diverging"

class TurnoutType(Enum):
    STANDARD_LEFT = "standard_left"
    STANDARD_RIGHT = "standard_right"
    Y_TURNOUT = "y_turnout"
    DOUBLE_SLIP = "double_slip"
    SINGLE_SLIP = "single_slip"
    SCISSOR_CROSSING = "scissor_crossing"

class IndustryType(Enum):
    TERMINAL = "terminal"
    DISTRIBUTION = "distribution"
    FACTORY = "factory"
    MINE = "mine"
    REPAIR = "repair"

class WagonType(Enum):
    TANKER = "tanker"
    OPEN = "open"
    HOPPER = "hopper"
    FLAT = "flat"

class Direction(Enum):
    UP = "up"
    DOWN = "down"
    CIRCULAR = "circular"
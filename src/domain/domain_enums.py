from enum import Enum

class JunctionType(Enum):
    PLAIN = "plain"
    TURNOUT = "turnout"
    CROSSING = "crossing"
    BUFFER = "buffer"

class TrackBlockType(Enum):
    MAINLINE = "mainline"
    PASSING_LOOP = "passing_loop"
    BRANCH = "branch"
    SIDING = "siding"
    SHED = "shed"
    HEADSHUNT = "headshunt"
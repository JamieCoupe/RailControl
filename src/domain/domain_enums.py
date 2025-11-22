from enum import Enum

class JunctionType(Enum):
    PLAIN = "plain"
    TURNOUT = "turnout"
    CROSSING = "crossing"
    BUFFER = "buffer"

class TrackBlockType(Enum):
    MAINLINE = "mainline"
    BRANCH = "branch"
    SIDING = "siding"
    SHED = "shed"
    HEADSHUNT = "headshunt"
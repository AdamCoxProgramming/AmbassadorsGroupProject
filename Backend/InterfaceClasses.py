from enum import Enum

class ShuttleType(Enum):
    """Represents types of a shuttle"""
    MANNED = 1,
    UN_MANNED = 2


class ShuttleState:
    """Represents the states of a shuttle"""
    def __init__(self,shuttleId, isFlying, destination, flightPercent, location,shuttleType):
        self.shuttleId = shuttleId
        self.isFlying = isFlying
        self.flightPercent = flightPercent
        self.destination = destination
        self.location = location
        self.type = shuttleType
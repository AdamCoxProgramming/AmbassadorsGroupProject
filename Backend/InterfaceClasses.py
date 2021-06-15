class ShuttleState:
    def __init__(self,shuttleId, isFlying, destination, flightPercent):
        self.shuttleId = shuttleId
        self.isFlying = isFlying
        self.flightPercent = flightPercent
        self.destination = destination
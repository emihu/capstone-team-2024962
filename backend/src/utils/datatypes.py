import uuid
class ProcessedFlightInfo:
    def __init__(self, id: uuid.UUID, flightNumber: int, latitude: float, 
                 longitude: float, altitude: float, speed: float, heading: float):
        self.id = id
        self.flightNumber = flightNumber
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude # in feet
        self.speed = speed # in knots
        self.heading = heading # 0 is north, 90 is east, 180 is south, 270 is west

        self.RA = -1 # init to -1 to indicate not set
        self.Dec = -1 # caution, declination can also be -1

    def __str__(self):
        return f"{self.id} {self.flightNumber} {self.latitude} {self.longitude} {self.altitude} {self.speed} {self.heading}"
        
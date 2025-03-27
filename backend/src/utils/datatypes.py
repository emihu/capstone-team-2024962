import uuid
from datetime import datetime
from dataclasses import dataclass

class ProcessedFlightInfo:
    """
    ProcessedFlightInfo class to represent a flight with processed
    information.
    """
    def __init__(self, id: uuid.UUID, flightNumber: str, latitude: float, 
                 longitude: float, altitude: float, speed: float, heading: float):
        self.id = id
        self.flightNumber = flightNumber
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude # in feet
        self.speed = speed # in knots
        self.heading = heading # 0 is north, 90 is east, 180 is south, 270 is west
        
        self.entry : datetime = 0
        self.exit : datetime = 0
        self.RA = -1 # init to -1 to indicate not set
        self.Dec = -1 # caution, declination can also be -1

    def __str__(self):
        return f"{self.id} {self.flightNumber} {self.latitude} {self.longitude} {self.altitude} {self.speed} {self.heading}"
    
    def to_dict(self):
        """ Convert object to JSON-serializable dictionary. """
        return {
            "id": self.id,
            "flight_number": self.flightNumber,
            "altitude": self.altitude,
            "heading": self.heading,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "speed": self.speed,
            "entry": self.entry.isoformat() if self.entry else None,  # Convert datetime to string
            "exit": self.exit.isoformat() if self.exit else None,  # Convert datetime to string
        }

@dataclass
class HMS:
    """
    HMS class to represent an angle in hours, minutes, and seconds.
    """
    hours: int
    minutes: int
    seconds: float

    def __post_init__(self):
        if not (0 <= self.hours < 24):
            raise ValueError("Hours must be in the range 0-23.")
        if not (0 <= self.minutes < 60):
            raise ValueError("Minutes must be in the range 0-59.")
        if not (0 <= self.seconds < 60):
            raise ValueError("Seconds must be in the range 0-59.")

    def to_degrees(self):
        """
        Convert the HMS angle to degrees.
        (1 hour = 15 degrees)
        """
        deg = (self.hours + self.minutes / 60.0 + self.seconds / 3600.0) * 15.0
        return deg
        
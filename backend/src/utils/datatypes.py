from dataclasses import dataclass

@dataclass
class FlightInfo:
    flight_number: int
    latitude: float
    longitude: float
    altitude: float
    speed: float
    heading: float

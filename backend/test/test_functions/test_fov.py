import pytest
from utils.datatypes import ProcessedFlightInfo
from utils import fov
import uuid

def test_remove_ground_flights():
    # Create a list of flight data with some ground flights
    flight_data = [
        ProcessedFlightInfo(id=uuid.uuid4(), flightNumber="123", latitude=43.58962, longitude=-79.64439, altitude=5000, speed=200, heading=180),
        ProcessedFlightInfo(id=uuid.uuid4(), flightNumber="123",latitude=43.58962, longitude=-79.64439, altitude=0, speed=0, heading=0),
        ProcessedFlightInfo(id=uuid.uuid4(), flightNumber="123",latitude=43.58962, longitude=-79.64439, altitude=10000, speed=500, heading=90),
    ]

    # Call the function to remove ground flights
    filtered_flights = fov.remove_ground_flights(flight_data)

    # Check that the ground flight was removed
    assert len(filtered_flights) == 2
    assert all(flight.altitude > 0 for flight in filtered_flights)
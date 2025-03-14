import random
import pytest
from astropy.time import Time
from collections import deque

# Import functions from your script
from src.utils.integration import find_flights_intersecting
from src.utils.datatypes import flightInfo  # Assuming this exists

def generate_mock_flights():
    """
    Generate a list of mock flights for testing.
    Returns a list of flightInfo objects.
    """
    return [
        flightInfo(
            flightNumber="FLT100",
            latitude=43.705,    # Close to observer
            longitude=-79.395,  # Close to observer
            altitude=12000,     # Within horizon altitude
            speed=800,          # Typical jet speed in km/h
            heading=45          # Moving NE
        ),
        flightInfo(
            flightNumber="FLT200",
            latitude=45.000,    # Far from observer
            longitude=-80.000,  # Outside FOV
            altitude=12000,     # Within horizon altitude
            speed=750,
            heading=90
        ),
        flightInfo(
            flightNumber="FLT300",
            latitude=43.700,    # Directly overhead
            longitude=-79.400,
            altitude=11000,     # Within horizon altitude
            speed=700,
            heading=180
        )
    ]

@pytest.fixture
def mock_flights():
    return generate_mock_flights()

def test_find_flights_in_horizon(mock_flights):
    """
    Test the function to detect flights within the observer's horizon.
    """
    observer_lat = 43.7
    observer_lon = -79.4

    # Simulate API function
    def mock_find_flights_in_circ_boundary(lat, lon, radius):
        return [flight for flight in mock_flights if abs(flight.latitude - lat) < radius and abs(flight.longitude - lon) < radius]

    # Replace API function in the test
    flight_data = mock_find_flights_in_circ_boundary(observer_lat, observer_lon, radius=0.043)

    assert len(flight_data) > 0, "No flights detected, check calculation"

def test_find_flights_intersecting(mock_flights):
    """
    Test the intersection detection logic.
    """
    observer_lat = 43.7
    observer_lon = -79.4
    observer_time = Time.now()

    user_gps = {"latitude": observer_lat, "longitude": observer_lon}
    fov_size = 1.5  # In degrees
    fov_center = {"RA": 120.0, "Dec": 30.0}

    # Call intersection detection function
    flight_intersections_queue = find_flights_intersecting(
        flight_data=mock_flights,
        user_gps=user_gps,
        observer_time=observer_time,
        fov_size=fov_size,
        fov_center=fov_center,
        observer_lat=observer_lat,
        observer_lon=observer_lon
    )

    assert isinstance(flight_intersections_queue, deque), "Output should be a deque"
    assert len(flight_intersections_queue) > 0, "No intersections detected"
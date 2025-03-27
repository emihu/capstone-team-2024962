import pytest
from utils import constants
from utils import conversion
import math


@pytest.mark.parametrize("lat, lon, expected", [
    # Test 1: Latitude and longitude are both 0
    (0, 0, (0, constants.EARTH_RADIUS_METER, 0)),
    
])
def test_gps_cartesian(lat, lon, expected):
    result = conversion.gps_cartesian(lat, lon, 0)
    # round to 2 decimal places
    assert pytest.approx(result, abs=1e-3) == expected

@pytest.mark.parametrize("lat, lon, alt, expected", [
    # Test 1: Latitude and longitude are both 0
    (0, 0, 0, (0, constants.EARTH_RADIUS_METER, 0)),
])
def test_aircraft_theta_phi_to_cartesian(lat, lon, alt, expected):
    pass

def test_aircraft_vector_from_gps():
    pass

def test_aircraft_vector_from_gps_aligned():
    pass

def test_azimuth_elevation_from_vector():
    pass

def test_aziele_to_radec():
    pass


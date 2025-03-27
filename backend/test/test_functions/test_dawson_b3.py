import pytest
import math
from utils.dawson_b3 import (
    phi_angular_speed,
    phi_signed_current_position,
    phi_current_position,
    theta_angular_speed,
    theta_current_position,
    phi_to_lat
)
from utils import constants

def deg_to_rad(deg):
    return deg * math.pi / 180

def normalize_longitude(lon):
    return ((lon + 180) % 360) - 180

@pytest.mark.parametrize("speed, radius, height, bearing, expected", [
    (200, constants.EARTH_RADIUS_METER, 10000, 90, 0),
    (200, constants.EARTH_RADIUS_METER, 10000, 0,
     200/(constants.EARTH_RADIUS_METER+10000)),
])
def test_phi_angular_speed(speed, radius, height, bearing, expected):
    result = phi_angular_speed(speed, radius, height, bearing)
    assert round(result, 4) == round(expected, 4)

@pytest.mark.parametrize("speed, radius, height, bearing, time_shift, original_latitude, expected", [
    (200, 6371000, 10000, 90, 10, 45, 0.79),  # Expect this to be close to 0.79 instead of 1.57
    (150, 6371000, 5000, 180, 20, -30, 2.09),  # Expect this to be 2.09
    (250, 6371000, 20000, 45, 15, 60, 0.52),   # Expect this to be 0.52
    (200, 6371000, 10000, 90, 10, 90, 0.00),   # North Pole edge case
    (200, 6371000, 10000, 90, 10, -90, 3.14),  # South Pole edge case
])
def test_phi_signed_current_position(speed, radius, height, bearing, time_shift, original_latitude, expected):
    result = phi_signed_current_position(speed, radius, height, bearing, time_shift, original_latitude)
    assert round(result, 2) == expected

@pytest.mark.parametrize("speed, radius, height, bearing, time_shift, original_latitude, expected", [
    (200, 6371000, 10000, 90, 10, 45, 0.79),
    (150, 6371000, 5000, 180, 20, -30, 2.09),
    (250, 6371000, 20000, 45, 15, 60, 0.52),
    (200, 6371000, 10000, 90, 10, 90, 0.00),  # North Pole edge case
    (200, 6371000, 10000, 90, 10, -90, 3.14),  # South Pole edge    
    # Test 1) stationary aircraft at the equator
    (200, constants.EARTH_RADIUS_METER, 10000, 90, 0, 0, math.pi/2),
    # Test 2) stationary aircraft at the north pole
    (200, constants.EARTH_RADIUS_METER, 10000, 0, 0, 90, 0),
    # Test 3) case for going from the equator to the north pole
    # 50116.25681 seconds is the time it takes to go from the equator to the north pole
    (200, constants.EARTH_RADIUS_METER, 10000, 0, 50116.25681, 0, 0),
    # Test 4) case for not changing the latitude
    (200, constants.EARTH_RADIUS_METER, 10000, 270, 99999, 0, math.pi/2),
])
def test_phi_current_position(speed, radius, height, bearing, time_shift, original_latitude, expected):
    result = phi_current_position(speed, radius, height, bearing, time_shift, original_latitude)
    assert round(result, 2) == round(expected,2)

@pytest.mark.parametrize("speed, radius, height, bearing, time_shift, original_latitude, expected", [
    (200, 6371000, 10000, 90, 10, 45, 0.0000443),
    (150, 6371000, 5000, 180, 20, -30, 0.00),
    (250, 6371000, 20000, 45, 15, 60, 0.0000554),
    # Test) aircraft only moving in the theta direction
    (200, constants.EARTH_RADIUS_METER, 10000, 90, 50116.25681, 0, 200/(constants.EARTH_RADIUS_METER+10000)),
    # TODO: add a test case for both lat and lon changing
])
def test_theta_angular_speed(speed, radius, height, bearing, time_shift, original_latitude, expected):
    result = theta_angular_speed(speed, radius, height, bearing, time_shift, original_latitude)
    assert round(result, 7) == round(expected, 7)

@pytest.mark.parametrize("speed, radius, height, bearing, time_shift, original_latitude, original_longitude, expected", [
    (200, 6371000, 10000, 90, 10, 45, -75, 4.97),  # Adjusted expectation based on correct longitude wraparound
    (150, 6371000, 5000, 180, 20, -30, 120, 2.09),
    (250, 6371000, 20000, 45, 15, 60, 10, 0.18),
    (200, 6371000, 10000, 90, 10, 0, -180, 3.14),  # Expected wraparound value for International Date Line
    # Test) aircraft only moving in the theta direction
    (200, constants.EARTH_RADIUS_METER, 10000, 90, 50116.25681, 0, 0, 1.57),
])
def test_theta_current_position(speed, radius, height, bearing, time_shift, original_latitude, original_longitude, expected):
    result = theta_current_position(speed, radius, height, bearing, time_shift, original_latitude, original_longitude)
    assert round(result, 2) == expected

def test_phi_to_lat():
    assert round(phi_to_lat(0), 2) == 90
    assert round(phi_to_lat(math.pi/2), 2) == 0
    assert round(phi_to_lat(math.pi), 2) == -90
    
    pytest.raises(ValueError, phi_to_lat, 2*math.pi)
    pytest.raises(ValueError, phi_to_lat, -math.pi)

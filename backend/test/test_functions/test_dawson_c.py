import pytest
from src.utils import constants
from src.utils import dawson_c
import math


@pytest.mark.parametrize("lat, lon, expected", [
    (0, 0, (6371000, 0, 0)),
    (90, 0, (6371000, 0, 0)),
    (-90, 0, (6371000, 0, 0)),
    (0, 90, (6371000, 0, 0)),
    (0, -90, (6371000, 0, 0)),
    (45, 45, (6371000, 0, 0)),
    (-45, -45, (6371000, 0, 0)),
    (0, 180, (6371000, 0, 0)),
    (0, -180, (6371000, 0, 0)),
    (90, 180, (6371000, 0, 0)),
    (-90, 180, (6371000, 0, 0)),
    (90, -180, (6371000, 0, 0)),
    (-90, -180, (6371000, 0, 0)),
    (45, 180, (6371000, 0, 0)),
    (-45, 180, (6371000, 0, 0)),
    (45, -180, (6371000, 0, 0)),
    (-45, -180, (6371000, 0, 0)),
    (45, 90, (6371000, 0, 0)),
    (-45, 90, (6371000, 0, 0)),
    (45, -90, (6371000, 0, 0)),
    (-45, -90, (6371000, 0, 0)),
])
def test_gps_cartesian(lat, lon, expected):
    assert dawson_c.gps_cartesian(lat, lon) == expected

def test_aircraft_theta_phi_to_cartesian():
    pass

def test_aircraft_vector_from_gps():
    pass

def test_aircraft_vector_from_gps_aligned():
    pass

def test_azimuth_elevation_from_vector():
    pass

def test_aziele_to_radec():
    pass


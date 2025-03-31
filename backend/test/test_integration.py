
import pytest


import sys
from datetime import datetime, timezone
from astropy.time import Time
import uuid


from utils.integration import find_flights_intersecting
import utils.fov as fov


def test_integration():
    # Telescope settings
    focal_length = 20
    camera_sensor_size = 10
    barlow_reducer_factor = 0.5
    exposure = 250
    fov_center_ra_h = 1
    fov_center_ra_m = 51
    fov_center_ra_s = 5
    fov_center_dec = 43.58962
    time = Time(datetime(2025,3,30,14,38,0,tzinfo=timezone.utc))

    # observer and Flight information
    observer_lat = 43.58962
    observer_lon = -79.64439
    observer_elev = 0

    simulated_flights = [{
        "flightNumber": "123",
        "latitude": 43.9002,
        "longitude": -80.2114,
        "altitude": 35000,
        "speed": 490,
        "heading": 111,
    }]

    fov_size = fov.calculate_fov_size(focal_length, camera_sensor_size, barlow_reducer_factor)

    # Run
    flights_position, flight_data = find_flights_intersecting(fov_size, exposure, fov_center_ra_h, fov_center_ra_m, fov_center_ra_s, fov_center_dec,
                                                                            observer_lat, observer_lon, observer_elev, 
                                                                            flight_data_type="simulated", simulated_flights=simulated_flights, simulated_time=time)
    for flight in flight_data:
        print(flight.entry, flight.exit)

    for fp in flights_position:
        print(fp)
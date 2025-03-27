
import pytest


import sys
from datetime import datetime, timezone
from astropy.time import Time
import uuid


from utils.integration import find_flights_intersecting
from utils.fov import check_flights_in_fov
from utils.datatypes import ProcessedFlightInfo


def test_integration():
    # Telescope settings
    focal_length = 6000
    camera_sensor_size = 50
    barlow_reducer_factor = 1
    exposure = 300
    fov_center_ra_h = 1
    fov_center_ra_m = 16
    fov_center_ra_s = 0
    fov_center_dec = 14.63
    time = Time(datetime(2025,3,13,12,34,22,tzinfo=timezone.utc))

    # observer and Flight information
    observer_lat = 0
    observer_lon = 0
    observer_elev = 0

    simulated_flights = [{
        "latitude": 0,
        "longitude": 0,
        "altitude": 30000,
        "speed": 800,
        "heading": 180,
    }]

    # Run
    flights_position, flight_data = find_flights_intersecting(focal_length, camera_sensor_size, barlow_reducer_factor,
                                                                            exposure, fov_center_ra_h, fov_center_ra_m, fov_center_ra_s, fov_center_dec,
                                                                            observer_lat, observer_lon, observer_elev, 
                                                                            flight_data_type="simulated", simulated_flights=simulated_flights, simulated_time=time)
    for flight in flight_data:
        print(flight.entry, flight.exit)

    for fp in flights_position:
        print(fp)
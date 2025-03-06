
import math
from datatypes import flightInfo
from astropy.time import Time
import dawson_b3
import dawson_c
import dawson_d
import coord 
import fov
from constants import EARTH_RADIUS_METER
from datetime import timedelta
from collections import deque
# todo: create data class
def find_flights_intersecting (focal_length: float, camera_sensor_size: float, barlow_reducer_factor: float, exposure: float, 
                               fov_center_ra_h: float, fov_center_ra_m: float, fov_center_ra_s: float, fov_center_dec: float, 
                               observer_lon: float, observer_lat: float, altitude: float, flight_data_type: str, simulated_flights):
    # get fov
    fov_size = fov.calculate_fov_size(focal_length, camera_sensor_size, barlow_reducer_factor)
    fov_center_lat, fov_center_lon = coord.convert_ra_dec_to_lat_lon(ra=(fov_center_ra_h,fov_center_ra_m,fov_center_ra_s), dec = fov_center_dec, ra_format="hms")

    # get horizon
    if flight_data_type == "live":
        flight_data = fov.find_live_flights_in_horizon(observer_lat, observer_lon)
    else:
        flight_data = fov.find_simulated_flights_in_horizon(observer_lat, observer_lon, simulated_flights)

    # loop through flights to check for intersections
    user_gps = {"latitude": observer_lat, "longitude": observer_lon}
    fov_center_ra = coord.HMS(fov_center_ra_h, fov_center_ra_m, fov_center_ra_s)
    fov_center = {"RA": fov_center_ra.to_degrees(), "Dec": fov_center_dec} 

    flights_in_fov = set()
    flights_position = list()
    for time_delta in range(0, 180, 5): 
        check_intersection(flight_data, user_gps, None, time_delta, fov_size, fov_center, flights_in_fov, flights_position)    

    return flights_position, flight_data


def check_intersection(flight_data: list[flightInfo], user_gps: dict[str, float], observer_time: Time | None, \
                       elapsed_time: float, fov_size: float, fov_center: dict[str, float], flights_in_fov: set, flights_position: list):
    if observer_time is None:
        observer_time = Time.now()

    curr_flight_positions = list()
        
    for flight in flight_data:
        
        phi = dawson_b3.phi_current_position(flight.speed, EARTH_RADIUS_METER, flight.altitude, flight.heading, elapsed_time, flight.latitude)
        theta = dawson_b3.theta_current_position(flight.speed, EARTH_RADIUS_METER, flight.altitude, flight.heading, elapsed_time, flight.latitude, flight.longitude)

        user_gps_cartesian = dawson_c.gps_cartesian(
            user_gps['latitude'], user_gps['longitude'])

        aircraft_gps_cartesian = dawson_c.aircraft_theta_phi_to_cartesian(
            EARTH_RADIUS_METER + flight.altitude, theta, phi)
        
        vector = dawson_c.aircraft_vector_from_gps(
            user_gps_cartesian, aircraft_gps_cartesian)

        flight.RA, flight.Dec = dawson_c.aziele_to_radec(dawson_c.azimuth_elevation_from_vector(vector), user_gps['latitude'])

        intersection_check = dawson_d.d2(fov_size, flight.RA, flight.Dec, fov_center["RA"], fov_center["Dec"]) # change return

        # add flight if entering/exiting the fov
        if intersection_check:
            if flight.flightNumber not in flights_in_fov:
                flights_in_fov.add(flight.flightNumber)
                flight.entry = observer_time.to_datetime() + timedelta(seconds=elapsed_time)
            else:
                flights_in_fov.discard(flight.flightNumber)
                flight.exit = observer_time.to_datetime() + timedelta(seconds=elapsed_time)

        # add position of the flight if in fov
        if flight.flightNumber in flights_in_fov:
            curr_flight_positions.append({"flightNumber": flight.flightNumber, "RA": flight.RA, "Dec": flight.Dec})

    # add all of the flight positions of flights within the fov at this timestamp
    flights_position.append(curr_flight_positions)

        


        
        
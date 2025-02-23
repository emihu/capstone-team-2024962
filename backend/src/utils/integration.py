
import math
from datatypes import flightInfo
from astropy.time import Time
import dawson_b3
import dawson_c
import dawson_d
import utils.flight_api as fa
import utils.coord 
import fov
from constants import EARTH_RADIUS
import datetime
from collections import deque

def find_flights_in_horizon (observer_lat, observer_lon):
    """
    Find flights within the observer's horizon.

    Parameters:
        observer_lat (float): Observer's latitude in degrees.
        observer_lon (float): Observer's longitude in degrees.
        observer_alt (float): Observer's altitude in meters.

    Returns:
        list: Flight data from the API within the calculated horizon.
    """
    # Earth's radius in meters
    EARTH_RADIUS = 6371000  

    # based on max alt of plane
    horizon_distance = 12801.6

    # Convert horizon radius from meters to degrees (approximate conversion)
    radius_deg = (horizon_distance / EARTH_RADIUS) * (180 / math.pi)

    # Query API with calculated circular boundary
    flight_data = fa.find_flights_in_circ_boundary(observer_lat, observer_lon, radius_deg)

    #return flight_data
    return flight_data

def find_flights_intersecting (flight_data: list[flightInfo], user_gps: dict[str, float], observer_time: Time | None,
                               fov_size: float, fov_center: dict[str, float], observer_lat, observer_lon):
    flight_data = find_flights_in_horizon(observer_lat, observer_lon, observer_alt=12801.6) 

    flight_intersections_queue = deque()

    for time_delta in range(0, 180, 5): 
        flight_intersections_queue = check_intersection(flight_data, user_gps, observer_time, time_delta, fov_size, fov_center, flight_intersections_queue)    

    return flight_intersections_queue

def check_intersection(flight_data: list[flightInfo], user_gps: dict[str, float], observer_time: Time | None, \
                       elapsed_time: float, fov_size: float, fov_center: dict[str, float], flight_intersections_queue: deque):
    if observer_time is None:
        observer_time = Time.now()
        
    for flight in flight_data:
        
        phi = dawson_b3.phi_current_position(flight.speed, EARTH_RADIUS, flight.altitude, flight.bearing, elapsed_time, flight.latitude)
        theta = dawson_b3.theta_current_position(flight.speed, EARTH_RADIUS, flight.altitude, flight.bearing, elapsed_time, flight.latitude, flight.longitude)

        user_gps_cartesian = dawson_c.gps_cartesian(
            user_gps['latitude'], user_gps['longitude'])

        aircraft_gps_cartesian = dawson_c.aircraft_theta_phi_to_cartesian(
            EARTH_RADIUS + flight.altitude, theta, phi)
        
        vector = dawson_c.aircraft_vector_from_gps(
            user_gps_cartesian, aircraft_gps_cartesian)

        flight.RA, flight.Dec = dawson_c.altele_to_radec(dawson_c.azimuth_elevation_from_vector(vector), user_gps['latitude'])

        intersection_check = dawson_d.d2(fov_size, flight.RA, flight.Dec, fov_center["RA"], fov_center["Dec"]) # change return

        if intersection_check:
            if not any(flight[1] == flight.flightNumber for flight in flight_intersections_queue): # check if the plane is entering or exiting
                flight_intersections_queue.append((elapsed_time, flight.flightNumber, 0))
            else:
                flight_intersections_queue.append((elapsed_time, flight.flightNumber, 1))
    
    return flight_intersections_queue
        


        
        
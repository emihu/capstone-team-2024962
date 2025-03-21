
import math
from datatypes import ProcessedFlightInfo
from astropy.time import Time, TimeDelta
import dawson_b3
import dawson_c
import dawson_d
import coord 
import fov
from constants import EARTH_RADIUS_METER
from coord2 import convert_lat_lon_to_ra_dec
from datetime import timedelta, datetime
from collections import deque
# todo: create data class
def find_flights_intersecting (focal_length: float, camera_sensor_size: float, barlow_reducer_factor: float, exposure: float, 
                               fov_center_ra_h: float, fov_center_ra_m: float, fov_center_ra_s: float, fov_center_dec: float, 
                               observer_lon: float, observer_lat: float, altitude: float, flight_data_type: str, simulated_flights, simulated_time: datetime | None = None):
    
    # get fov
    fov_size = fov.calculate_fov_size(focal_length, camera_sensor_size, barlow_reducer_factor)
    fov_center_lat, fov_center_lon = coord.convert_ra_dec_to_lat_lon(ra=(fov_center_ra_h,fov_center_ra_m,fov_center_ra_s), dec = fov_center_dec, ra_format="hms")

    # get horizon
    if flight_data_type == "live":
        flight_data = fov.find_live_flights_in_horizon(observer_lat, observer_lon)
    else:
        #TODO: check return type of flight_data, don't see anywhere that converts it to a list of ProcessedFlightInfo
        flight_data = fov.find_simulated_flights_in_horizon(observer_lat, observer_lon, simulated_flights)

    user_gps = {"latitude": observer_lat, "longitude": observer_lon}
    fov_center_ra = coord.HMS(fov_center_ra_h, fov_center_ra_m, fov_center_ra_s) 
    fov_center = {"RA": fov_center_ra.to_degrees(), "Dec": fov_center_dec} 
    observer_time = Time.now()

    # loop through flights to check for intersections
    flights_in_fov = set()
    flights_position = list()
    #TODO: play around with the timestep
    observer_time = None if simulated_time is None else simulated_time
    for elapsed_time in range(0, exposure, 5): 
        check_intersection(flight_data, user_gps, observer_time, elapsed_time, fov_size, fov_center, flights_in_fov, flights_position)    

    return flights_position, flight_data


def check_intersection(flight_data: list[ProcessedFlightInfo], user_gps: dict[str, float], observer_time: Time | None, \
                       elapsed_time: int, fov_size: float, fov_center: dict[str, float], flights_in_fov: set, flights_position: list):
    if observer_time is None:
        observer_time = Time.now()

    curr_flight_positions = list()
        

    for flight in flight_data:

        speed: float = flight.speed * 0.514444 # convert speed from knots to m/s

        phi: float = dawson_b3.phi_current_position(
            speed, EARTH_RADIUS_METER, flight.altitude, flight.heading, elapsed_time, flight.latitude)
        theta: float = dawson_b3.theta_current_position(
            speed, EARTH_RADIUS_METER, flight.altitude, flight.heading, elapsed_time, flight.latitude, flight.longitude)

        lat: float = dawson_b3.phi_to_lat(phi)
        lon: float = dawson_b3.theta_to_lon(theta)
        alt: float = flight.altitude / 3.28084 # convert altitude from feet to meters

        # TODO: check if this is the correct way to calculate the observer time
        # TODO: test the timezone
        delta = TimeDelta(elapsed_time, format='sec')
        observer_time = observer_time + delta

        print(f"lat, lon: {lat}, {lon}")

        # TODO: get user altitude from frontend
        flight.RA, flight.Dec = convert_lat_lon_to_ra_dec(
            sky_obj_lat=lat,
            sky_obj_lon=lon,
            sky_obj_alt=alt,
            obs_lat=user_gps["latitude"],
            obs_lon=user_gps["longitude"],
            obs_alt=0,
            observer_time=observer_time)
        
        print(f"RA, Dec: {flight.RA}, {flight.Dec}")

        is_intersecting = dawson_d.is_intersecting(flight.RA, flight.Dec, fov_center["RA"], fov_center["Dec"], fov_size)

        # add flight if entering/exiting the fov
        if is_intersecting:
            if flight.id not in flights_in_fov: # enter time
                flights_in_fov.add(flight.id)
                flight.entry = observer_time.to_datetime() + timedelta(seconds=elapsed_time)
        else:
            if flight.id in flights_in_fov: # exit time
                flights_in_fov.discard(flight.id)
                flight.exit = observer_time.to_datetime() + timedelta(seconds=elapsed_time)

        # add position of the flight if in fov
        if flight.id in flights_in_fov:
            curr_flight_positions.append({"ID": flight.id, "RA": flight.RA, "Dec": flight.Dec})

    # add all of the flight positions of flights within the fov at this timestamp
    flights_position.append(curr_flight_positions)

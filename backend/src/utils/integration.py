
from utils.datatypes import ProcessedFlightInfo, HMS
from astropy.time import Time, TimeDelta
import utils.dawson_b3 as dawson_b3
import utils.dawson_c as dawson_c
import utils.dawson_d as dawson_d
import utils.fov as fov
from utils.constants import EARTH_RADIUS_METER

from datetime import datetime
# todo: create data class
#TODO: HMS should directly be input to this class to get type checkings
def find_flights_intersecting (focal_length: float, camera_sensor_size: float, barlow_reducer_factor: float, exposure: float, 
                               fov_center_ra_h: float, fov_center_ra_m: float, fov_center_ra_s: float, fov_center_dec: float,
                               observer_lon: float, observer_lat: float, altitude: float, flight_data_type: str, simulated_flights, simulated_time: datetime | None = None):
    """
    Function to find flights intersecting the field of view of the telescope.
    :param focal_length: The focal length of the telescope.
    :param camera_sensor_size: The size of the camera sensor.
    :param barlow_reducer_factor: The barlow reducer factor.
    :param exposure: The exposure time.
    :param fov_center_ra_h: The Right Ascension of the center of the field of view in hours.
    :param fov_center_ra_m: The Right Ascension of the center of the field of view in minutes.
    :param fov_center_ra_s: The Right Ascension of the center of the field of view in seconds.
    :param fov_center_dec: The Declination of the center of the field of view.
    :param observer_lon: The observer's longitude.
    :param observer_lat: The observer's latitude.
    :param altitude: The observer's altitude.
    :param flight_data_type: The type of flight data (live or simulated).
    :param simulated_flights: The simulated flights.
    :param simulated_time: The simulated time.
    :return: The list of flight positions and the flight data.
    :raise ValueError: If the input values are invalid.
    """
    # check input values
    if observer_lat < -90 or observer_lat > 90:
        raise ValueError("Observer latitude must be in the range [-90, 90].")
    if observer_lon < -180 or observer_lon > 180:
        raise ValueError("Observer longitude must be in the range [-180, 180].")
    if fov_center_dec < -90 or fov_center_dec > 90:
        raise ValueError("FOV center declination must be in the range [-90, 90].")
    if flight_data_type == "simulated" and simulated_flights is None:
        raise ValueError("Simulated flights must be provided")
    
    # get fov
    fov_size = fov.calculate_fov_size(focal_length, camera_sensor_size, barlow_reducer_factor)
    print("fov size: ", fov_size)

    # get horizon
    if flight_data_type == "live":
        flight_data = fov.find_live_flights_in_horizon(observer_lat, observer_lon)
    else:
        #TODO: check return type of flight_data, don't see anywhere that converts it to a list of ProcessedFlightInfo
        flight_data = fov.find_simulated_flights_in_horizon(observer_lat, observer_lon, simulated_flights)

    print("flight_data", flight_data)
    user_gps = {"latitude": observer_lat, "longitude": observer_lon}
    # the ra already have type checkings
    fov_center_ra = HMS(fov_center_ra_h, fov_center_ra_m, fov_center_ra_s) 
    fov_center = {"RA": fov_center_ra.to_degrees(), "Dec": fov_center_dec} 

    # loop through flights to check for intersections
    flights_in_fov = set()
    flights_position = list()

    #TODO: play around with the timestep
    observer_time = None if simulated_time is None else simulated_time
    for elapsed_time in range(0, int(exposure), 5): 
        check_intersection(flight_data, user_gps, observer_time, elapsed_time, fov_size, fov_center, flights_in_fov, flights_position)    

    print("done:", flights_position, flight_data)
    return flights_position, flight_data


# helper function to convert flight's lat, lon, alt to RA, Dec
def convert_flight_lat_lon_to_ra_dec(flight: ProcessedFlightInfo, updated_observer_time: Time, elapsed_time: int, user_gps: dict[str, float]) -> tuple[float, float]:
    """
        Convert the flight's latitude, longitude, altitude to Right Ascension and Declination.
        :param flight: The flight to convert.
        :param updated_observer_time: The updated observer time.
        :param elapsed_time: The elapsed time.
        :param user_gps: The user's GPS coordinates.
        :return: The flight's Right Ascension and Declination.
        :raise ValueError: If the observer time is not provided.
    """
    if updated_observer_time is None:
        raise ValueError("updated observer time must be provided.")

    flight_speed: float = flight.speed * 0.514444 # convert speed from knots to m/s
    flight_alt: float = flight.altitude / 3.28084 # convert altitude from feet to meters

    phi: float = dawson_b3.phi_current_position(
        flight_speed, EARTH_RADIUS_METER, flight_alt, flight.heading, elapsed_time, flight.latitude)
    theta: float = dawson_b3.theta_current_position(
        flight_speed, EARTH_RADIUS_METER, flight_alt, flight.heading, elapsed_time, flight.latitude, flight.longitude)

    # TODO: get user altitude from frontend
    return dawson_c.aircraft_theta_phi_to_radec(
        theta, phi, flight_alt, user_gps["latitude"], user_gps["longitude"], 0, updated_observer_time)

    

def check_intersection(flight_data: list[ProcessedFlightInfo], user_gps: dict[str, float], observer_time: Time | None, \
                       elapsed_time: int, fov_size: float, fov_center: dict[str, float], flights_in_fov: set, flights_position: list):
    if observer_time is None:
        observer_time = Time.now()
    #calculate the updated time after the elapsed time
    delta = TimeDelta(elapsed_time, format='sec')
    updated_time = observer_time + delta

    curr_flight_positions = list()
        
    for flight in flight_data:

        flight.RA, flight.Dec = convert_flight_lat_lon_to_ra_dec(flight, updated_time, elapsed_time, user_gps)
        print(flight.RA, flight.Dec)
        
        is_intersecting = dawson_d.is_intersecting(flight.RA, flight.Dec, fov_center["RA"], fov_center["Dec"], fov_size)

        # add flight if entering/exiting the fov
        if is_intersecting:
            if flight.id not in flights_in_fov: # enter time
                flights_in_fov.add(flight.id)
                flight.entry = updated_time.to_datetime()
        else:
            if flight.id in flights_in_fov: # exit time
                flights_in_fov.discard(flight.id)
                flight.exit = updated_time.to_datetime()

        # add position of the flight if in fov
        if flight.id in flights_in_fov:
            curr_flight_positions.append({"ID": flight.id, "RA": flight.RA, "Dec": flight.Dec, "Heading": flight.heading})

    # add all of the flight positions of flights within the fov at this timestamp
    flights_position.append(curr_flight_positions)

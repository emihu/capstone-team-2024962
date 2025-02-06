
from datatypes import flightInfo
from astropy.time import Time
import dawson_b3
import dawson_c
from constants import EARTH_RADIUS

def set_ra_dec_for_flights(flight_data: list[flightInfo], user_gps: dict[str, float], observer_time: Time | None, elapsed_time: float):
    """
    Set the RA and Dec for each flight in the flight data.
    
    Parameters
    ----------
    flight_data : list of flightInfo
        The flight data to update.
    observer_time : astropy.time.Time
        The time of the observer.
    """
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
    
    return flight_data
        


        
        
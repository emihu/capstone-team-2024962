
from datatypes import ProcessedFlightInfo
from astropy.time import Time, TimeDelta
import dawson_b3
from constants import EARTH_RADIUS

from coord2 import convert_lat_lon_to_ra_dec


def set_ra_dec_for_flights(flight_data: list[ProcessedFlightInfo], user_gps: dict[str, float], observer_time: Time | None, elapsed_time: float):
    """
    Set the RA and Dec for each flight in the flight data.

    Parameters
    ----------
    flight_data : list of ProcessedFlightInfo
        The flight data to update.
    observer_time : astropy.time.Time
        The time of the observer.
    """
    if observer_time is None:
        observer_time = Time.now()

    for flight in flight_data:

        phi: float = dawson_b3.phi_current_position(
            flight.speed, EARTH_RADIUS, flight.altitude, flight.bearing, elapsed_time, flight.latitude)
        theta: float = dawson_b3.theta_current_position(
            flight.speed, EARTH_RADIUS, flight.altitude, flight.bearing, elapsed_time, flight.latitude, flight.longitude)

        lat: float = dawson_b3.phi_to_lat(phi)
        lon: float = dawson_b3.theta_to_lon(theta)
        alt: float = flight.altitude / 3.28084 # convert altitude from feet to meters

        # TODO: check if this is the correct way to calculate the observer time
        # TODO: test the timezone
        delta = TimeDelta(elapsed_time, format='sec')
        observer_time = observer_time + delta

        # TODO: get user altitude from frontend
        flight.RA, flight.Dec = convert_lat_lon_to_ra_dec(
            lat, lon, alt, user_gps["latitude"], user_gps["longitude"], 0, observer_time)

    return flight_data

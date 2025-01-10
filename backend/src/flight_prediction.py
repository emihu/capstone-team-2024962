from utils.datatypes import FlightInfo
from utils.constants import EARTH_RADIUS_KM, AVERAGE_FLIGHT_ALTITUDE_METERS
from utils.coord import get_distance_from_lat_lon_pair

# TODO: refine all calculation to take in the time difference between
# the time stamp of the request and the exeuction time

def get_list_of_predicted_flight_intersections(flight_info_list: list[FlightInfo],
                                           fov_center_latlon: tuple[float, float], 
                                           fov_radius: float,
                                           exposure_time: float) -> list[FlightInfo]:
    return list(filter(lambda flightinfo: is_flight_entering_fov_during_exposure
        (flightinfo, fov_center_latlon, fov_radius, exposure_time), flight_info_list))




# TODO: account the entire area of the plane covers in the sky - use the lights on the plane
def is_flight_entering_fov_during_exposure(flight_info: FlightInfo, 
                                           fov_center_latlon: tuple[float, float], 
                                           fov_radius: float,
                                           exposure_time: float) -> bool:

    distance = get_distance_from_lat_lon_pair(
        (flight_info.latitude, flight_info.longitude), 
        fov_center_latlon,
        EARTH_RADIUS_KM + AVERAGE_FLIGHT_ALTITUDE_METERS)

    # Step 1
    # if flight is in the FOV, return true
    if distance < fov_radius:
        return True

    # step 2
    # if flight straight line * exposure time is in FOV
    # return true
    if distance - flight_info.speed * exposure_time < fov_radius:
        return True

    return False

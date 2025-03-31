import math
import utils.flight_api as fa
from utils.datatypes import ProcessedFlightInfo
import uuid
from utils.constants import EARTH_RADIUS_METER, AIRPLANE_MAX_ALT

def calculate_fov_size(focal_length : float, camera_sensor_size : float, barlow_reducer_factor : float) -> float:
    """
    Calculate the field of view size of a telescope.
    """
    # calculate the FOV size
    fov_size = ((180/math.pi)/(focal_length*barlow_reducer_factor))*camera_sensor_size

    return fov_size

# what distance to use? typical altitude of planes?
def fov_degrees_to_meters(fov_degrees, distance_meters):    
    # convert FOV from degrees to radians
    fov_radians = math.radians(fov_degrees)
    
    # calculate the FOV in meters
    fov_meters = 2 * distance_meters * math.tan(fov_radians / 2)
    
    return fov_meters

# Haversine formula to calculate the distance between a pair of lat/lon
# Output is in meters
def haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon1 - lon2
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return c * EARTH_RADIUS_METER

# Determines which simulated flights are inside the boundary.
def find_simulated_flights_in_horizon(observer_lat, observer_lon, simulated_flights):
    simulated_flights = [convert_to_processed_flight(flight, idx) for idx, flight in enumerate(simulated_flights)]

    flight_data = []
    query_radius = math.sqrt(math.pow(EARTH_RADIUS_METER + AIRPLANE_MAX_ALT, 2) - math.pow(EARTH_RADIUS_METER, 2))
    
    for flight in simulated_flights:
        flight_lat = flight.latitude
        flight_lon = flight.longitude
        distance = haversine(observer_lat, observer_lon, flight_lat, flight_lon)
        
        # If the distance is less than or equal to the radius, the flight is in the horizon
        if distance <= query_radius:
            flight_data.append(flight)
        
    return flight_data

def find_live_flights_in_horizon (observer_lat, observer_lon):
    query_radius = math.sqrt(math.pow(EARTH_RADIUS_METER + AIRPLANE_MAX_ALT, 2) - math.pow(EARTH_RADIUS_METER, 2))
    flight_data = fa.find_flights_in_circ_boundary(observer_lat, observer_lon, query_radius)

    return flight_data

def convert_to_processed_flight(flight_data, flight_number=0):
    return ProcessedFlightInfo(
        id=uuid.uuid4(),  # Generate a unique ID
        flightNumber=flight_data["flightNumber"],
        latitude=float(flight_data["latitude"]),
        longitude=float(flight_data["longitude"]),
        altitude=float(flight_data["altitude"]),  # Already in feet
        speed=float(flight_data["speed"]),  # Already in knots
        heading=float(flight_data["heading"])  # Convert string to float
    )


def angular_distance(ra1, dec1, ra2, dec2):
    """
    Calculate the angular distance between two celestial points using the haversine formula.
    
    Parameters:
        ra1 (float): Right Ascension of the first point (in degrees)
        dec1 (float): Declination of the first point (in degrees)
        ra2 (float): Right Ascension of the second point (in degrees)
        dec2 (float): Declination of the second point (in degrees)
    Raise:
        ValueError: If ra1, dec1, ra2, or dec2 are out of range
        
    Returns:
        float: Angular distance between the two points (in degrees)
    """
    # Check if the coordinates are within the valid range
    if not (-90 <= dec1 <= 90) or not (-90 <= dec2 <= 90) or not (0 <= ra1 <= 360) or not (0 <= ra2 <= 360):
        raise ValueError("Coordinates out of range")

    # Convert degrees to radians
    ra1_rad, dec1_rad = math.radians(ra1), math.radians(dec1)
    ra2_rad, dec2_rad = math.radians(ra2), math.radians(dec2)
    
    # Differences in coordinates
    delta_ra = ra2_rad - ra1_rad
    delta_dec = dec2_rad - dec1_rad
    
    # Haversine formula
    a = math.sin(delta_dec / 2)**2 + math.cos(dec1_rad) * math.cos(dec2_rad) * math.sin(delta_ra / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Convert the result from radians to degrees
    return math.degrees(c)

    
def is_intersecting(ra1, dec1, ra2, dec2, fov_size) -> bool:
    """
    Check if the line of sight between two celestial points intersects with the field of view.
    
    Parameters:
        ra1 (float): Right Ascension of the first point (in degrees)
        dec1 (float): Declination of the first point (in degrees)
        ra2 (float): Right Ascension of the second point (in degrees)
        dec2 (float): Declination of the second point (in degrees)
        fov_size (float): Field of view size (in degrees), this is the angle from one end of the FOV to the other end
        
    Returns:
        bool: True if the line of sight intersects with the field of view, False otherwise
    """
    # Calculate the angular distance between the two points
    angle = angular_distance(ra1, dec1, ra2, dec2)
    
    # Check if the angular distance is within the field of view
    # fov should be divided by 2, since fov_size is the angle from one end of the FOV to the other end
    return angle < (fov_size/2)
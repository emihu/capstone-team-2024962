import math
import utils.flight_api as fa
import utils.coord2 as co
from utils.datatypes import ProcessedFlightInfo
import uuid
from utils.constants import EARTH_RADIUS_METER, AIRPLANE_MAX_ALT

def calculate_fov_size(focal_length, camera_sensor_size, barlow_reducer_factor):
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

# Determines which simulated flights are inside the telescope FOV.
#TODO: refactor this function to use processed flight info
def find_simulated_flights_in_fov(fov_center_lat, fov_center_lon, radius, simulated_flights) -> list[ProcessedFlightInfo]:
    flights_in_fov : list[ProcessedFlightInfo] = []
    
    for flight in simulated_flights:
        flight_lat = flight['latitude']
        flight_lon = flight['longitude']
        distance = haversine(float(fov_center_lat), float(fov_center_lon), float(flight_lat), float(flight_lon))
        
        # If the distance is less than or equal to the radius, the flight is in the circular FOV
        # TODO: Lawrence please confirm if this is the correct way to populate the data
        if distance <= radius:
            flights_in_fov.append(ProcessedFlightInfo(
                id=uuid.uuid4(),
                flightNumber=flight['flightNumber'],
                latitude=flight_lat,
                longitude=flight_lon,
                altitude=flight['altitude'],
                speed=flight['speed'],
                heading=flight['heading']
            ))
        
    return flights_in_fov


def check_flights_in_fov(focal_length, camera_sensor_size, barlow_reducer_factor, \
                         fov_center_ra_h, fov_center_ra_m, fov_center_ra_s, \
                         fov_center_dec, flight_data_type, simulated_flights, time=None):
    # find radius of the fov
    fov_size = calculate_fov_size(focal_length, camera_sensor_size, barlow_reducer_factor)
    radius = abs(fov_degrees_to_meters(fov_size, distance_meters=12801.6))

    # convert to lat lon
    result = co.convert_ra_dec_to_lat_lon(ra=(fov_center_ra_h,fov_center_ra_m,fov_center_ra_s), dec = fov_center_dec, ra_format="hms", time=time)
    fov_center_lat = result[0]
    fov_center_lon = result[1]

    print("input: ", fov_center_lat, fov_center_lon, radius)

    # TODO: put the integration function here
    if flight_data_type == "live":
        flight_info : list[ProcessedFlightInfo] = fa.find_flights_in_circ_boundary(fov_center_lat, fov_center_lon, radius)
    else:
        flight_info: list[ProcessedFlightInfo] = find_simulated_flights_in_fov(
            fov_center_lat, fov_center_lon, radius, simulated_flights)

    #return flight_info
    return {
        "flight_info": flight_info,
        "fov_border": {"lat": fov_center_lat, "lon": fov_center_lon, "radius": radius}
    }

# Determines which simulated flights are inside the boundary.
def find_simulated_flights_in_horizon(observer_lat, observer_lon, simulated_flights):
    simulated_flights = [convert_to_processed_flight(flight, idx) for idx, flight in enumerate(simulated_flights)]
    print("processed flights: ", simulated_flights, type(simulated_flights))
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
        flightNumber=0,
        latitude=float(flight_data["latitude"]),
        longitude=float(flight_data["longitude"]),
        altitude=float(flight_data["altitude"]),  # Already in feet
        speed=float(flight_data["speed"]),  # Already in knots
        heading=float(flight_data["heading"])  # Convert string to float
    )
import math
import utils.flight_api as fa
import utils.coord as co

EARTH_RADIUS = 6371000 # in meters

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
    
    return c * EARTH_RADIUS

# Determines which simulated flights are inside the telescope FOV.
def find_simulated_flights_in_fov(fov_center_lat, fov_center_lon, radius, simulated_flights):
    flights_in_fov = []
    
    for flight in simulated_flights:
        flight_lat = flight['latitude']
        flight_lon = flight['longitude']
        distance = haversine(float(fov_center_lat), float(fov_center_lon), float(flight_lat), float(flight_lon))
        
        # If the distance is less than or equal to the radius, the flight is in the circular FOV
        if distance <= radius:
            flights_in_fov.append(flight)
        
    return flights_in_fov


def check_flights_in_fov(focal_length, camera_sensor_size, barlow_reducer_factor, \
                         fov_center_ra_h, fov_center_ra_m, fov_center_ra_s, \
                         fov_center_dec, flight_data_type, simulated_flights):
    # find radius of the fov
    fov_size = calculate_fov_size(focal_length, camera_sensor_size, barlow_reducer_factor)
    radius = abs(fov_degrees_to_meters(fov_size, distance_meters=12801.6))

    # convert to lat lon
    result = co.convert_ra_dec_to_lat_lon(ra=(fov_center_ra_h,fov_center_ra_m,fov_center_ra_s), dec = fov_center_dec, ra_format="hms")
    fov_center_lat = result[0].value
    fov_center_lon = result[1].value

    print("input: ", fov_center_lat, fov_center_lon, radius)

    if flight_data_type == "live":
        flight_info = fa.find_flights_in_circ_boundary(fov_center_lat, fov_center_lon, radius)
    else:
        flight_info = find_simulated_flights_in_fov(fov_center_lat, fov_center_lon, radius, simulated_flights)

    #return flight_info
    return {
        "flight_info": flight_info,
        "fov_border": {"lat": fov_center_lat, "lon": fov_center_lon, "radius": radius}
    }

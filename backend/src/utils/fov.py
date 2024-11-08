import math
import flight_api as fa
import coord as co

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

def check_flights_in_fov(focal_length, camera_sensor_size, barlow_reducer_factor, fov_center_ra, fov_center_dec):
    # find radius of the fov
    fov_size = calculate_fov_size(focal_length, camera_sensor_size, barlow_reducer_factor)
    radius = fov_degrees_to_meters(fov_size, distance_meters=12801.6)

    # use Andrew's function in coord.py  
    fov_center_lat, fov_center_lon = co.convert_ra_dec_to_lat_lon(fov_center_ra, fov_center_dec)

    flight_info = fa.find_flights_in_circ_boundary(fov_center_lat, fov_center_lon, radius)

    if flight_info:
        return True
    else:
        return False

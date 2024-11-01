import math
from FlightRadar24 import FlightRadar24API
fr_api = FlightRadar24API()

def calculate_fov_size(focal_length, camera_sensor_size, barlow_reducer_factor):
    # calculate the FOV size
    fov = ((180/math.pi)/(focal_length*barlow_reducer_factor))*camera_sensor_size

    return fov

# what distance to use? typical altitude of planes?
def fov_degrees_to_meters(fov_degrees, distance_meters):    
    # convert FOV from degrees to radians
    fov_radians = math.radians(fov_degrees)
    
    # calculate the FOV in meters
    fov_meters = 2 * distance_meters * math.tan(fov_radians / 2)
    
    return fov_meters

def calculate_fov_boundary(fov_size, fov_center_ra, fov_center_dec):  
    # use Andrew's function in coord.py  
    fov_center_lat, fov_center_lon = convert_ra_dec_to_lat_lon(fov_center_ra, fov_center_dec)

    # latitude and longitude for your position and radius for the distance in meters
    bounds = fr_api.get_bounds_by_point(fov_center_lat, fov_center_lon, fov_size)
    
    return bounds


import math
import utils.flight_api as fa
import utils.coord as co

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

def check_flights_in_fov(focal_length, camera_sensor_size, barlow_reducer_factor, fov_center_ra_h, fov_center_ra_m, fov_center_ra_s, fov_center_dec):
    # find radius of the fov
    fov_size = calculate_fov_size(focal_length, camera_sensor_size, barlow_reducer_factor)
    radius = abs(fov_degrees_to_meters(fov_size, distance_meters=12801.6))

    # convert to lat lon
    result = co.convert_ra_dec_to_lat_lon(ra=(fov_center_ra_h,fov_center_ra_m,fov_center_ra_s), dec = fov_center_dec, ra_format="hms")
    fov_center_lat = result[0].value
    fov_center_lon = result[1].value

    print("input: ", fov_center_lat, fov_center_lon, radius)

    flight_info = fa.find_flights_in_circ_boundary(fov_center_lat, fov_center_lon, radius)

    #return flight_info
    return {
        "flight_info": flight_info,
        "fov_border": {"lat": fov_center_lat, "lon": fov_center_lon, "radius": radius}
    }

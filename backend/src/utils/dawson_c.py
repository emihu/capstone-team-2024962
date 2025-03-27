import math
from utils.localsidereal import get_local_sidereal_time
from utils.dawson_b3 import deg_to_rad, rad_to_deg, lat_to_phi, normalize_longitude, lon_to_theta
from utils.constants import EARTH_RADIUS_METER


def spherical_to_cartesian(r, theta, phi) -> tuple[float, float, float]:
    """
    Convert spherical coordinates to cartesian coordinates.
    :param r: The radius.
    :param theta: The theta angle in spherical coordinates in radians.
    :param phi: The phi angle in spherical coordinates in radians.
    :raise ValueError: If phi is not in the range of [0, pi] or theta is not in the range of [0, 2pi].
    :return: The cartesian coordinates.
    """
    if (phi > math.pi or phi < 0):
        raise ValueError("Phi angle must be less than or equal to pi.")
    if (theta > 2 * math.pi or theta < 0):
        raise ValueError("Theta angle must be less than or equal to 2pi.")

    x = r * math.sin(phi) * math.cos(theta)
    y = r * math.sin(phi) * math.sin(theta)
    z = r * math.cos(phi)

    return (x, y, z)

def gps_cartesian(lat, lon, alt)-> tuple[float, float, float]:
    """
    Calculate the cartesian coordinates of the GPS location.
    :param lat: The latitude in degrees.
    :param lon: The longitude in degrees.
    :param alt: The altitude in meters.
    :return: The cartesian coordinates of the GPS location.
    :raise ValueError: If the latitude or longitude is out of range.
    """
    if (lat > 90 or lat < -90):
        raise ValueError("Latitude must be between -90 and 90 degrees.")
    if (lon > 180 or lon < -180):
        raise ValueError("Longitude must be between -180 and 180 degrees.")
    # Get phi in radians
    phi = lat_to_phi(lat)

    # Get theta in radians, rotated by 90 degrees
    theta = (lon_to_theta(lon) + math.pi/2) % (2*math.pi)

    return spherical_to_cartesian(EARTH_RADIUS_METER + alt, theta, phi)


def aircraft_theta_phi_to_cartesian(theta, phi, alt) -> tuple[float, float, float]:
    """
    Convert the aircraft's theta and phi to cartesian coordinates.
    Rotate the theta by 90 degrees.
    Need to add 90 Degrees to align with the GPS coordinates.
    :param theta: The theta angle in radians.
    :param phi: The phi angle in radians.
    :param alt: The altitude of the aircraft.
    raise ValueError: If phi is not in the range of [0, pi] or theta is not in the range of [0, 2pi].
    """
    if (phi > math.pi or phi < 0):
        raise ValueError("Phi angle must be less than or equal to pi.")
    if (theta > 2 * math.pi or theta < 0):
        raise ValueError("Theta angle must be less than or equal to 2pi.")
        
    theta = (theta + math.pi/2) % (2*math.pi)
    return spherical_to_cartesian(alt + EARTH_RADIUS_METER, theta, phi)

def aircraft_vector_from_gps(gps_cartesian: tuple, aircraft_cartesian: tuple) -> tuple[float, float, float]:
    """
    Calculate the vector from the GPS location to the aircraft.
    Note that this vector needs to be further processed so that x-axis aligns with the direction of longitude, and z points to up.
    """
    gps_x, gps_y, gps_z = gps_cartesian
    aircraft_x, aircraft_y, aircraft_z = aircraft_cartesian

    return (aircraft_x - gps_x, aircraft_y - gps_y, aircraft_z - gps_z)

def aircraft_vector_from_gps_aligned(aircraft_vector, gps_lat, gps_lon)->tuple[float, float, float]:
    """
    Get the aircraft vector aligned with longitude and latitude, with z pointing up.
    """
    # Get theta in radians, rotated by 90 degrees
    theta = lon_to_theta(gps_lon)
    phi = lat_to_phi(gps_lat)
    print("theta", theta)
    print("phi", phi)

    aircraft_x, aircraft_y, aircraft_z = aircraft_vector
    x = math.cos(theta) * aircraft_x + math.sin(theta) * aircraft_y
    y = -math.sin(theta) * math.cos(phi) * aircraft_x + math.cos(theta) * math.cos(phi) * aircraft_y - math.sin(phi) * aircraft_z
    z = -math.sin(theta) * math.sin(phi) * aircraft_x + math.cos(theta) * math.sin(phi) * aircraft_y + math.cos(phi) * aircraft_z
    return (x, y, z)


def azimuth_elevation_from_vector(vector: tuple)->tuple[float, float]:
    """
    Calculate the azimuth and elevation from the vector.
    :param vector: The vector from the GPS location to aircraft, aligned with longitude and latitude.
    :return: Azimuth in radians, Elevation in radians.
    """
    x, y, z = vector

    east = -x
    north = -y

    theta = math.atan2(north, east)
    azimuth = (deg_to_rad(450) - theta) % (2*math.pi)
    
    elevation = math.atan2(z, math.sqrt(x**2 + y**2))

    return (azimuth, elevation)

def aziele_to_radec(azele: tuple[float, float], gps_lat: float, gps_lon: float, time=None)->tuple[float, float]:
    """
    Convert the azimuth and elevation to right ascension and declination.
    :return: Right Ascension in degrees, Declination in degrees.
    :raise ValueError: If the latitude or longitude is out of range.
    :raise ValueError: If the azimuth or elevation is out of range.
    """
    if (gps_lat > 90 or gps_lat < -90):
        raise ValueError("Latitude must be between -90 and 90 degrees.")
    if (gps_lon > 180 or gps_lon < -180):
        raise ValueError("Longitude must be between -180 and 180 degrees.")

    # Get the azimuth and elevation
    azimuth, elevation = azele

    if (azimuth > 2*math.pi or azimuth < 0):
        raise ValueError("Azimuth must be between 0 and 2pi.")
    if (elevation > math.pi/2 or elevation < -math.pi/2):
        raise ValueError("Elevation must be between -pi/2 and pi/2.")


    lat_rad = deg_to_rad(gps_lat)

    # right ascension calculation
    # Step 1: calculate the x and y component of the hour angle
    ha_y = -math.sin(azimuth)*math.cos(elevation)
    ha_x = -math.cos(azimuth)*math.sin(lat_rad)*math.cos(elevation) + math.sin(elevation)*math.cos(lat_rad)
    
    # Step 2: calculate the hour angle between the two components
    hour_angle = math.atan2(ha_y, ha_x)

    # step 3: calculate the right ascension
    right_ascension = get_local_sidereal_time(gps_lat, gps_lon, time) - hour_angle
    right_ascension = right_ascension % (2*math.pi)

    # Declination calculation
    declination = math.asin(math.sin(lat_rad)*math.sin(elevation) + math.cos(lat_rad)*math.cos(elevation)*math.cos(azimuth))

  
    right_ascension = rad_to_deg(right_ascension)
    declination = rad_to_deg(declination)

    return (right_ascension, declination)

    
def aircraft_theta_phi_to_radec(aircraft_theta, aircraft_phi, aircraft_alt, gps_lat, gps_lon, gps_alt, time=None)->tuple[float, float]:
    """
    Convert the aircraft's latitude and longitude to right ascension and declination.
    :param aircraft_theta: The theta angle in radians.
    :param aircraft_phi: The phi angle in radians.
    :param aircraft_alt: The altitude of the aircraft in meters.
    :param gps_lat: The latitude of the GPS location in degrees.
    :param gps_lon: The longitude of the GPS location in degrees.
    :param gps_alt: The altitude of the GPS location in meters.
    :param time: The time of observation.
    :return: Right Ascension in degrees, Declination in degrees.

    The following exceptions are raised from the called functions:
    :raise ValueError: If the latitude or longitude is out of range.
    :raise ValueError: If the azimuth or elevation is out of range.
    :raise ValueError: If phi is not in the range of [0, pi] or theta is not in the range of [0, 2pi].
    """
    print("====================")
    gps_cart = gps_cartesian(gps_lat, gps_lon, gps_alt)
    aircraft_cart = aircraft_theta_phi_to_cartesian(aircraft_theta, aircraft_phi, aircraft_alt)
    aircraft_vector = aircraft_vector_from_gps(gps_cart, aircraft_cart)
    aircraft_vector_aligned = aircraft_vector_from_gps_aligned(aircraft_vector, gps_lat, gps_lon)
    print("aircraft_vector_aligned", aircraft_vector_aligned)
    azele = azimuth_elevation_from_vector(aircraft_vector_aligned)
    print("azimuth, elevation", azele)
    print("====================")
    return aziele_to_radec(azele, gps_lat, gps_lon, time)
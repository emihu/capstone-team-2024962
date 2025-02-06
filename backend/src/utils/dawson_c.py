import math
from dawsonv2 import get_local_sidereal_time

from latlon_helper import deg_to_rad, rad_to_deg, lat_to_phi, normalize_longitude, EARTH_RADIUS_METER


def spherical_to_cartesian(r, theta, phi) -> tuple[float, float, float]:
    """
    Convert spherical coordinates to cartesian coordinates.
    """
    x = r * math.sin(phi) * math.cos(theta)
    y = r * math.sin(phi) * math.sin(theta)
    z = r * math.cos(phi)

    return (x, y, z)

def gps_cartesian(lat, lon)-> tuple[float, float, float]:
    """
    Calculate the cartesian coordinates of the GPS location.
    """
    # Get phi in radians
    phi = lat_to_phi(lat)

    # Get theta in radians, rotated by 90 degrees
    theta = deg_to_rad(normalize_longitude(lon)) + math.pi/2

    return spherical_to_cartesian(EARTH_RADIUS_METER, theta, phi)


def aircraft_theta_phi_to_cartesian(radius, theta, phi) -> tuple[float, float, float]:
    """
    Convert the aircraft's theta and phi to cartesian coordinates.
    Rotate the theta by 90 degrees.
    Need to add 90 Degrees to align with the GPS coordinates.
    """
    theta = theta + math.pi/2
    return spherical_to_cartesian(radius, theta, phi)

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
    theta = deg_to_rad(normalize_longitude(gps_lon))
    phi = lat_to_phi(gps_lat)

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

    theta = math.atan2(y, x)
    azimuth = (deg_to_rad(450) - theta) % 360
    
    elevation = math.atan2(z, math.sqrt(x**2 + y**2))
    return (azimuth, elevation)

def altele_to_radec(azele: tuple[float, float], gps_lat)->tuple[float, float]:
    """
    Convert the azimuth and elevation to right ascension and declination.
    :return: Right Ascension in degrees, Declination in degrees.
    """
    azimuth, elevation = azele

    lat_rad = deg_to_rad(gps_lat)

    # right ascension calculation
    # Step 1: calculate the x and y component of the hour angle
    ha_y = -math.sin(azimuth)*math.cos(elevation)
    ha_x = -math.cos(azimuth)*math.sin(lat_rad)*math.cos(elevation) + math.sin(elevation)*math.cos(lat_rad)
    
    # Step 2: calculate the hour angle between the two components
    hour_angle = math.atan2(ha_y, ha_x)

    # step 3: calculate the right ascension
    right_ascension = get_local_sidereal_time(gps_lat, 0) - hour_angle
    right_ascension = right_ascension % (2*math.pi)

    # Declination calculation
    declination = math.asin(math.sin(lat_rad)*math.sin(elevation) + math.cos(lat_rad)*math.cos(elevation)*math.cos(azimuth))

  
    right_ascension = rad_to_deg(right_ascension)
    declination = rad_to_deg(declination)

    return (right_ascension, declination)
"""
This file contains lat lon helper functions for the Dawson Math 3D library.
"""
import math

EARTH_RADIUS_METER = 6371000 # in meters

def deg_to_rad(deg) -> float:
    """
    Convert degrees to radians.
    """
    return deg * math.pi / 180

def rad_to_deg(rad) -> float:
    """
    Convert radians to degrees.
    """
    return rad * 180 / math.pi 

def lat_to_phi(lat) -> float:
    """
    Convert the latitude to phi angle.
    param: lat Latitude in degrees.
    return: phi angle in radians.
    """
    return deg_to_rad(90 - lat)

def theta_to_lon(theta) -> float:
    """
    Convert the theta angle to longitude.
    """
    return unconvert_longitude(rad_to_deg(theta))

def normalize_longitude(lon) -> float:
    """
    Normalize the longitude to be in the range [-180, 180].
    Cooreponds to the theta_ref in the Dawson Math 3D library.
    """
    return (lon + 180) % 360 - 180

def unconvert_longitude(lon) -> float:
    """
    Unconvert the longitude to be in the range of (-180, 180]
    """
    return lon if lon <= 180 else lon - 360;
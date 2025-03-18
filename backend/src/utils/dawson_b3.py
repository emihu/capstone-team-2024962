"""
This file contains the implementation of the Dawson Math 3D library.
"""
import math

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

def phi_to_lat(phi) -> float:
    """
    Convert the phi angle to latitude.
    phi: The angle in radians.
    return: The latitude in degrees.
    """
    return rad_to_deg(math.pi / 2 - phi)

def theta_to_lon(theta) -> float:
    """
    Convert the theta angle to longitude.
    theta: The angle in radians.
    return: The longitude in degrees.
    """
    return unconvert_longitude(rad_to_deg(theta))

def normalize_longitude(lon) -> float:
    """
    Normalize the longitude to be in the range of [0, 360).
    """
    return (lon + 360) % 360

def unconvert_longitude(lon) -> float:
    """
    convert the longitude to be in the range of (-180, 180]
    """
    return lon if lon <= 180 else lon - 360

def phi_angular_speed(speed, radius, height, bearing) -> float:
    """
    Calculate the angular speed of the aircraft in the phi direction.
    :param bearing: The bearing of the aircraft in degrees. North is 0 degrees, East is 90 degrees, South is 180 degrees, and West is 270 degrees.
    """
    return speed / (radius + height) *math.cos(deg_to_rad(bearing))

def phi_signed_current_position(speed, radius, height, bearing, time_shift, original_latitude) -> float:
    """
    Calculate the current position of the aircraft in the phi direction.
    Corresponds to phi-direction in the Dawson Math 3D library B3.
    :param bearing: The bearing of the aircraft in degrees. North is 0 degrees, East is 90 degrees, South is 180 degrees, and West is 270 degrees.
    """
    return -phi_angular_speed(speed, radius, height, bearing) * time_shift + math.pi / 2 - deg_to_rad(original_latitude)

def phi_current_position(speed, radius, height, bearing, time_shift, original_latitude) -> float:
    """
    Calculate the current position of the aircraft in the phi direction.
    Corresponds phi-direction(modulo) in the Dawson Math 3D library B3.
    :param bearing: The bearing of the aircraft in degrees. North is 0 degrees, East is 90 degrees, South is 180 degrees, and West is 270 degrees.
    """
    ret = phi_signed_current_position(speed, radius, height, bearing, time_shift, original_latitude)
    ret = abs(ret % (2 * math.pi))
    if ret > math.pi:
        return 2 * math.pi - ret
    return ret

def theta_angular_speed(speed, radius, height, bearing, time_shift, original_latitude) -> float:
    """
    Calculate the angular speed of the aircraft in the theta direction.
    :param bearing: The bearing of the aircraft in degrees. North is 0 degrees, East is 90 degrees, South is 180 degrees, and West is 270 degrees.
    """
    return (speed * math.sin(deg_to_rad(bearing)))/((radius + height) * math.sin(phi_current_position(speed, radius, height, bearing, time_shift, original_latitude)))

def theta_current_position(speed, radius, height, bearing, time_shift, original_latitude, original_longitude) -> float:
    """
    Calculate the current position of the aircraft in the theta direction.
    :param bearing: The bearing of the aircraft in degrees. North is 0 degrees, East is 90 degrees, South is 180 degrees, and West is 270 degrees.
    """
    ret = theta_angular_speed(speed, radius, height, bearing, time_shift, original_latitude) * time_shift + deg_to_rad(normalize_longitude(original_longitude))
    ret = ret % (2 * math.pi)
    if (phi_signed_current_position(speed, radius, height, bearing, time_shift, original_latitude) < 0):
        return (ret + math.pi) % (2 * math.pi)
    return ret



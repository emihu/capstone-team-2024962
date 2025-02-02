import math

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
    """
    gps_x, gps_y, gps_z = gps_cartesian
    aircraft_x, aircraft_y, aircraft_z = aircraft_cartesian


    return (aircraft_x - gps_x, aircraft_y - gps_y, aircraft_z - gps_z)
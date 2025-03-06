import math
from latlon_helper import deg_to_rad, rad_to_deg, lat_to_phi, normalize_longitude, EARTH_RADIUS_METER

def RA_hour_to_deg(RA_hour):
    """
    Convert Right Ascension from hours to degrees.
    """
    return RA_hour * 15

def cartesian_celestial_coord(RA, Dec) -> tuple[float, float, float]:
    """
    Calculate the x component of the celestial coordinates.
    :param RA: Right Ascension in degrees.
    :param Dec: Declination in degrees.
    """
    RA = deg_to_rad(RA)
    Dec = deg_to_rad(Dec)
    x = -1 * math.sin(RA) * math.sin(math.pi/2 - Dec) # TODO: Ensure RA given is measured eastward from the vernal equinox - require testing
    y = math.cos(RA) * math.sin(math.pi/2 - Dec)
    z = math.cos(math.pi/2 - Dec)
    return (x, y, z)


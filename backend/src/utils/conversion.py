"""
File to handle conversion between coordinate systems.
"""
from astropy.time import Time
from astropy import units as u
from astropy.coordinates import SkyCoord

import math

from utils.datatypes import HMS
from utils.localsidereal import get_local_sidereal_time
from utils.constants import EARTH_RADIUS_METER

def deg_to_rad(deg) -> float:
    """
    Convert degrees to radians.
    """
    angle =  deg * math.pi / 180
    return angle

def rad_to_deg(rad) -> float:
    """
    Convert radians to degrees.
    """
    return rad * 180 / math.pi 

def lat_to_phi(lat) -> float:
    """
    Convert latitude to phi angle.
    lat: The latitude in degrees.
    return: The angle in radians.
    """
    if (lat > 90 or lat < -90):
        raise ValueError("Latitude must be between -90 and 90 degrees.")
    return math.pi / 2 - deg_to_rad(lat)

def lon_to_theta(lon) -> float:
    """
    Convert longitude to theta angle.
    lon: The longitude in degrees.
    return: The angle in radians.
    """
    if (lon > 180 or lon < -180):
        raise ValueError("Longitude must be between -180 and 180 degrees.")
    return deg_to_rad(normalize_longitude(lon))

def phi_to_lat(phi) -> float:
    """
    Convert the phi angle to latitude.
    phi: The angle in radians.
    return: The latitude in degrees.
    """
    if (phi > math.pi or phi < 0):
        raise ValueError("Phi angle must be less than or equal to pi.")
    return rad_to_deg(math.pi / 2 - phi)

def theta_to_lon(theta) -> float:
    """
    Convert the theta angle to longitude.
    theta: The angle in radians.
    return: The longitude in degrees.
    """
    if (theta > 2 * math.pi or theta < 0):
        raise ValueError("Theta angle must be less than or equal to 2pi.")
    return unconvert_longitude(rad_to_deg(theta))

def normalize_longitude(lon) -> float:
    """
    Normalize the longitude to be in the range of [0, 360).
    """
    if lon < 0:
        return lon + 360
    return lon

def unconvert_longitude(lon) -> float:
    """
    convert the longitude to be in the range of (-180, 180]
    """
    return lon if lon <= 180 else lon - 360


def convert_ra_dec_to_lat_lon(*, ra: float | HMS, dec, time=None, ra_format="deg"):
    """
    Convert Right Ascension (RA) and Declination (DEC) to an Earth “subpoint” 
    (latitude, longitude) where the object would be at the zenith.
    
    This conversion assumes that the object is effectively at an infinite
    distance so that the subpoint is defined by:
        - latitude = declination
        - longitude = RA (in degrees) - Greenwich Sidereal Time (in degrees)
    
    Parameters
    ----------
    ra : float or HMS
    dec : float, declination in degrees
    time : astropy.time.Time or str or None, optional
        The observation time. If None, Time.now() is used.
    ra_format : str, optional
        Format of the RA input. Either "deg" (default) or "hms".
    return: (lat, lon) : tuple of astropy.coordinates.Angle
    raise ValueError: If the input values are invalid.
    """
    # Handle the time input
    if time is None:
        time = Time.now()
    elif isinstance(time, str):
        try:
            time = Time(time)
        except Exception as e:
            raise ValueError(f"Invalid time format: {e}")

    # Convert RA to degrees
    if ra_format.lower() == "hms":
        if isinstance(ra, HMS):
            ra_deg = ra.to_degrees()
        else:
            raise ValueError("For 'hms' format, RA must be an HMS object or a tuple/list (hours, minutes, seconds).")
    elif ra_format.lower() == "deg":
        try:
            ra_deg = float(ra)
        except Exception as e:
            raise ValueError("For 'deg' format, RA must be convertible to a float.")
    else:
        raise ValueError("Invalid 'ra_format'. Use 'deg' or 'hms'.")

    # Create a SkyCoord for the celestial object in ICRS (equatorial) coordinates
    sky_coord = SkyCoord(ra=ra_deg * u.deg, dec=dec * u.deg, frame="icrs")

    # Get Greenwich Sidereal Time as an Angle, then convert it to degrees.
    # Note: time.sidereal_time() returns an angle in hour units by default.
    gst = time.sidereal_time('mean', 'greenwich').to(u.deg)

    # Compute the subpoint's longitude: RA (in degrees) minus GST
    sub_lon = (sky_coord.ra - gst).wrap_at(180 * u.deg)

    # The subpoint's latitude is simply the declination.
    sub_lat = sky_coord.dec

    return (sub_lat, sub_lon)

    

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
    gps_cart = gps_cartesian(gps_lat, gps_lon, gps_alt)
    aircraft_cart = aircraft_theta_phi_to_cartesian(aircraft_theta, aircraft_phi, aircraft_alt)
    aircraft_vector = aircraft_vector_from_gps(gps_cart, aircraft_cart)
    aircraft_vector_aligned = aircraft_vector_from_gps_aligned(aircraft_vector, gps_lat, gps_lon)
    azele = azimuth_elevation_from_vector(aircraft_vector_aligned)
    return aziele_to_radec(azele, gps_lat, gps_lon, time)
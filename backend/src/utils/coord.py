from astropy.time import Time
from astropy import units as u
from astropy.coordinates import EarthLocation, ICRS, AltAz, SkyCoord, Longitude, Latitude
from dataclasses import dataclass
import numpy as np
import sys


"""
Dataclass to represent angles in hours, minutes and seconds (HMS) format
"""
@dataclass
class HMS:
    hours: int
    minutes:int
    seconds:float
    
    """
    Validate the hours, minutes, and seconds upon initialization.
    """
    def __post_init__(self):
        if not (0 <= self.hours < 24):
            raise ValueError("Hours must be in the range 0-23.")
        if not (0 <= self.minutes < 60):
            raise ValueError("Minutes must be in the range 0-59.")
        if not (0 <= self.seconds < 60):
            raise ValueError("Seconds must be in the range 0-59.")

    """
    Convert the HMS angle to degrees.
    
    Returns:
        float: The angle in degrees.
    """
    def to_degrees(self):
        # Convert to degrees
        deg = (self.hours + self.minutes / 60 + self.seconds / 3600) * 15  # 1 hour = 15 degrees
        print(deg)
        return deg

"""
Convert Right Ascension (RA) and Declination (DEC) to Latitude and Longitude.

Parameters:
    ra: Right Ascension in degrees or HMS format. If `ra_format` is "hms",
        provide RA as a tuple or list (hours, minutes, seconds).
    dec: Declination in degrees.
    time: Observation time as an astropy Time object. Defaults to the current UTC time.
    ra_format: The format of RA. Either "deg" for degrees or "hms" for hours-minutes-seconds.

Returns:
    A tuple (lat, lon) where:
    - lat is the latitude (corresponding to declination) as an astropy Latitude object.
    - lon is the longitude (corresponding to RA adjusted for sidereal time) as an astropy Longitude object.
"""
def convert_ra_dec_to_lat_lon(*, ra, dec, time=None, ra_format="deg"):
    
    if time == None:
        time = Time.now()
    elif isinstance(time, str):
        try:
            time = Time(time)
        except ValueError as e:
            raise ValueError(f"Invalid time format: {e}")

    if ra_format == "hms":
        if isinstance(ra, HMS):
            ra_deg = ra.to_degrees()
        elif isinstance(ra, (tuple, list)) and len(ra) == 3:
            try:
                ra_deg = HMS(*ra).to_degrees()
            except ValueError as e:
                raise ValueError("Invalid RA in HMS format: {e}")
        else:
            raise ValueError("For 'hms' format, RA must be an HMS object, tuple or list (hours, minutes, seconds).")
    elif ra_format == "deg":
        if isinstance(ra, (float, int)):
            ra_deg = ra
        else:
            raise(ValueError("For 'deg' format, RA must be a float or int."))
    else:
        raise ValueError("Invalid 'ra_format'. Use 'deg' or 'hms'.")

    sky_obj_icrs = SkyCoord(ra=ra_deg * u.deg, dec=dec * u.deg, frame="icrs")

    gst_deg = time.sidereal_time('mean', 'greenwich')

    lon = Longitude(sky_obj_icrs.ra - gst_deg)
    lon.wrap_angle = 180 * u.deg

    lat = Latitude(dec * u.deg)


    return (lat.value, lon.value)


"""
Covert a object's lat lon and alt to right ascention and declination, relative to the observer's location
"""


def convert_lat_lon_to_ra_dec(
    *,
    sky_obj_lat,
    sky_obj_lon,
    sky_obj_alt,
    obs_lat,
    obs_lon,
    obs_alt,
    observer_time=Time.now()
):
    observer_location = EarthLocation(
        lat=obs_lat * u.deg, lon=obs_lon * u.deg, height=obs_alt * u.m
    )
    sky_object_location = EarthLocation(
        lat=sky_obj_lat * u.deg, lon=sky_obj_lon * u.deg, height=sky_obj_alt * u.m
    )

    # https://docs.astropy.org/en/stable/coordinates/common_errors.html
    sky_obj_itrs = sky_object_location.get_itrs(obstime=observer_time, location=observer_location)

    # Convert vector to AltAz frame
    altaz_frame = AltAz(obstime=observer_time, location=observer_location)

    print(f"altaz frame location: {altaz_frame.location}, time: {altaz_frame.obstime}")
    sky_obj_altaz = sky_obj_itrs.transform_to(altaz_frame)
    
    print(f"az, alt - {sky_obj_altaz.az} , {sky_obj_altaz.alt}")

    sky_obj_alt = sky_obj_altaz.alt.rad
    sky_obj_az = sky_obj_altaz.az.rad
    sky_obj_lat_rad = sky_obj_lat * np.pi / 180

    declination = np.arcsin(np.sin(sky_obj_alt) * np.sin(sky_obj_lat_rad) + 
        np.cos(sky_obj_alt) * np.cos(sky_obj_az) * np.cos(sky_obj_lat_rad))


    hour_angle = np.arccos((np.sin(sky_obj_alt) - np.sin(sky_obj_lat_rad) * np.sin(declination))/
                           (np.cos(sky_obj_lat_rad) * np.cos(declination))) * 180 / np.pi


    if not np.sin(hour_angle) < 0:
        hour_angle = 360 - hour_angle

    lst = observer_time.sidereal_time('mean', longitude=sky_obj_lon)

    right_ascention = lst - hour_angle * u.deg

    return (right_ascention, declination * 180 / np.pi)


def get_distance_from_lat_lon_pair(first_latlon, second_latlon, radius):
    """
    Calculates the great-circle distance between two points on a sphere given their latitude and longitude.

    Parameters:
    - first_latlon (tuple of float): A tuple `(lat1, lon1)` representing the latitude and longitude of the first point in decimal degrees.
    - second_latlon (tuple of float): A tuple `(lat2, lon2)` representing the latitude and longitude of the second point in decimal degrees.
    - radius (float): The radius of the sphere in kilometers.
      - For Earth, this is typically the Earth's radius plus the altitude of the flights, as aircraft fly above the Earth's surface.

    Returns:
    - distance (float): The distance between the two points along the surface of the sphere in kilometers.

    Notes:
    - The function uses the Haversine formula to calculate the great-circle distance between two points on the sphere.
    - The Earth's mean radius is approximately 6,371 km. When calculating distances involving aircraft, you may add the cruising altitude (e.g., 10 km) to the Earth's radius to get a more accurate result.
    - Ensure that the latitude values are within the range [-90, 90] and longitude values are within the range [-180, 180].

    Example:
    ```python
    # Coordinates of two points (latitude and longitude in degrees)
    point_a = (51.5074, -0.1278)  # London
    point_b = (40.7128, -74.0060)  # New York City

    # Earth's radius plus average cruising altitude of a flight (~10 km)
    earth_radius_km = 6371.0 + 10.0

    distance = get_distance_from_lat_lon_pair(point_a, point_b, earth_radius_km)
    print(f"The distance between London and New York City is approximately {distance:.2f} km.")
    ```
    """

    lat1, lon1 = first_latlon
    lat2, lon2 = second_latlon


    delta_lat = np.radians(lat2) - np.radians(lat1)
    delta_lon = np.radians(lon2) - np.radians(lon1)

    # https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
    a = np.sin(delta_lat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(delta_lon/2)**2
    c = 2 * np.asin(np.sqrt(a)) 
    return radius * c



if __name__ == "__main__":


    result = convert_lat_lon_to_ra_dec(sky_obj_lat=43.6798, sky_obj_lon=-79.6284, sky_obj_alt=10000, obs_lat=43.6798, obs_lon=-79.6284, obs_alt=0)

    print(result)

    print(convert_ra_dec_to_lat_lon(ra=result[0].deg, dec=result[1]))

    sys.exit(0)
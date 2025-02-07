
from astropy.time import Time
from astropy import units as u
from astropy.coordinates import SkyCoord, Longitude, Latitude
from dataclasses import dataclass
import dawson_b3
import dawson_c
from constants import EARTH_RADIUS_METER

@dataclass
class HMS:
    hours: int
    minutes: int
    seconds: float

    def __post_init__(self):
        if not (0 <= self.hours < 24):
            raise ValueError("Hours must be in the range 0-23.")
        if not (0 <= self.minutes < 60):
            raise ValueError("Minutes must be in the range 0-59.")
        if not (0 <= self.seconds < 60):
            raise ValueError("Seconds must be in the range 0-59.")

    def to_degrees(self):
        """
        Convert the HMS angle to degrees.
        (1 hour = 15 degrees)
        """
        deg = (self.hours + self.minutes / 60.0 + self.seconds / 3600.0) * 15.0
        return deg

def convert_ra_dec_to_lat_lon(*, ra, dec, time=None, ra_format="deg"):
    """
    Convert Right Ascension (RA) and Declination (DEC) to an Earth “subpoint” 
    (latitude, longitude) where the object would be at the zenith.
    
    This conversion assumes that the object is effectively at an infinite
    distance so that the subpoint is defined by:
        - latitude = declination
        - longitude = RA (in degrees) - Greenwich Sidereal Time (in degrees)
    
    Parameters
    ----------
    ra : float, tuple, list, or HMS
        The right ascension. If `ra_format` is "deg", this should be a number in degrees.
        If `ra_format` is "hms", this should be either an HMS instance or a tuple/list 
        of (hours, minutes, seconds).
    dec : float
        Declination in degrees.
    time : astropy.time.Time or str or None, optional
        The observation time. If None, Time.now() is used.
    ra_format : str, optional
        Format of the RA input. Either "deg" (default) or "hms".
    
    Returns
    -------
    (lat, lon) : tuple of astropy.coordinates.Angle
        - lat is the latitude (equal to dec).
        - lon is the longitude (computed as RA - GST) wrapped to [-180, 180] degrees.
    
    Raises
    ------
    ValueError
        If inputs are not of the expected type or format.
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
        elif isinstance(ra, (tuple, list)) and len(ra) == 3:
            try:
                ra_deg = HMS(*ra).to_degrees()
            except ValueError as e:
                raise ValueError(f"Invalid RA in HMS format: {e}")
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

# Example usage:
if __name__ == "__main__":
    # Example: Using RA in HMS format
    ra_hms = (6, 15, 0)  # 10h 30m 00s
    dec_deg = 43        # 20 degrees declination
    observation_time = "2025-02-06T00:00:00"  # ISO time string

    lat, lon = convert_ra_dec_to_lat_lon(ra=ra_hms, dec=dec_deg, ra_format="hms")
    print(f"Subpoint Latitude: {lat}")
    print(f"Subpoint Longitude: {lon}")

    # Example: Using RA in degrees directly
    ra_deg = 113.5  # degrees
    lat, lon = convert_ra_dec_to_lat_lon(ra=ra_deg, dec=dec_deg, ra_format="deg")
    print(f"Subpoint Latitude: {lat}")
    print(f"Subpoint Longitude: {lon}")

    
    
    
    test_lon = -79.3832
    test_lat = 43.6532
    test_time = Time.now()
    speed = 0
    bearing = 0
    elapsed_time = 0
    altitude = 10000
    
    phi = dawson_b3.phi_current_position(speed, EARTH_RADIUS_METER, altitude, bearing, elapsed_time, test_lat)
    theta = dawson_b3.theta_current_position(speed, EARTH_RADIUS_METER, altitude, bearing, elapsed_time, test_lat, test_lon)

    user_gps_cartesian = dawson_c.gps_cartesian(
        test_lat, test_lon)

    aircraft_gps_cartesian = dawson_c.aircraft_theta_phi_to_cartesian(
        EARTH_RADIUS_METER + altitude, theta, phi)
    
    vector = dawson_c.aircraft_vector_from_gps(
        user_gps_cartesian, aircraft_gps_cartesian)

    RA, Dec = dawson_c.altele_to_radec(dawson_c.azimuth_elevation_from_vector(vector), test_lat)

    print(f"{RA}, {Dec}")

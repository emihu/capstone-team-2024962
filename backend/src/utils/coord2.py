
from astropy.time import Time
from astropy import units as u
from astropy.coordinates import EarthLocation, ICRS, AltAz, ITRS, SkyCoord, Longitude, Latitude
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


def convert_lat_lon_to_ra_dec(
    *,
    sky_obj_lat,
    sky_obj_lon,
    sky_obj_alt,
    obs_lat,
    obs_lon,
    obs_alt,
    observer_time=None
) -> tuple[float, float]:
    # Use the current time if no observer_time is provided.
    if observer_time is None:
        observer_time = Time.now()
    
    # Define the observer's and object's locations.
    observer_location = EarthLocation(lat=obs_lat * u.deg,
                                      lon=obs_lon * u.deg,
                                      height=obs_alt * u.m)
    
    object_location = EarthLocation(lat=sky_obj_lat * u.deg,
                                    lon=sky_obj_lon * u.deg,
                                    height=sky_obj_alt * u.m)
    
    # Get the ITRS coordinates for both the object and observer.
    itrs_obj = object_location.get_itrs(obstime=observer_time)
    itrs_obs = observer_location.get_itrs(obstime=observer_time)
    
    # Compute the topocentric vector: the object's position relative to the observer.
    topo_vector = itrs_obj.cartesian - itrs_obs.cartesian
    
    # Create a SkyCoord from the topocentric vector in the ITRS frame.
    topo_coord = SkyCoord(topo_vector, frame=ITRS(obstime=observer_time))
    
    # Transform the topocentric coordinate into the AltAz frame.
    altaz_frame = AltAz(obstime=observer_time, location=observer_location)
    obj_altaz = topo_coord.transform_to(altaz_frame)
    
    # Finally, transform from AltAz to ICRS to obtain RA and Dec.
    obj_icrs = obj_altaz.transform_to(ICRS())
    
    return (obj_icrs.ra.deg, obj_icrs.dec.deg)


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

    # Define a fixed observation time for repeatability
    obs_time = Time("2025-03-01T12:00:00")

    # Observer's location (e.g., somewhere in Toronto)
    obs_lat = 43.65      # in degrees
    obs_lon = -79.38     # in degrees
    obs_alt = 0          # in meters

    # Flight is directly overhead: same lat and lon but at altitude 10,000 m (10 km)
    flight_lat = obs_lat
    flight_lon = obs_lon
    flight_alt = 10000   # in meters

    # Convert the flight's Earth coordinates to RA/Dec as seen by the observer.
    flight_ra_dec = convert_lat_lon_to_ra_dec(
        sky_obj_lat=flight_lat,
        sky_obj_lon=flight_lon,
        sky_obj_alt=flight_alt,
        obs_lat=obs_lat,
        obs_lon=obs_lon,
        obs_alt=obs_alt,
        observer_time=obs_time
    )
    print("=== Flight RA/Dec (ICRS) ===")
    print("RA:  ", flight_ra_dec[0])
    print("Dec: ", flight_ra_dec[1])
    print("")

    # Now convert the RA/Dec back to the Earth subpoint (lat, lon).
    subpoint_lat_lon = convert_ra_dec_to_lat_lon(
        ra=flight_ra_dec[0].deg,   # pass RA in degrees
        dec=flight_ra_dec[1].deg,  # pass Dec in degrees
        time=obs_time,
        ra_format="deg"
    )
    print("=== Subpoint (lat, lon) from RA/Dec ===")
    print("Latitude:  ", subpoint_lat_lon[0])
    print("Longitude: ", subpoint_lat_lon[1])
    print("")

    # For a flight directly overhead, we expect the subpoint to match the observer's location.
    print("=== Observer's Location ===")
    print("Latitude:  ", obs_lat * u.deg)
    print("Longitude: ", obs_lon * u.deg)
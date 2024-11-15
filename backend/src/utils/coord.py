from astropy.time import Time
from astropy import units as u
from astropy.coordinates import EarthLocation, ITRS, AltAz, SkyCoord, Longitude, Latitude
from dataclasses import dataclass
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
        raise ValueError("Invalid 'ra_format'. Use 'deg' or 'hms'.")

    sky_obj_icrs = SkyCoord(ra=ra_deg * u.deg, dec=dec * u.deg, frame="icrs")

    gst_deg = time.sidereal_time('mean', 'greenwich')

    lon = Longitude(sky_obj_icrs.ra - gst_deg)
    lon.wrap_angle = 180 * u.deg

    lat = Latitude(dec * u.deg)


    return (lat, lon)


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

    observer_itrs = observer_location.get_itrs(obstime=observer_time)
    sky_obj_itrs = sky_object_location.get_itrs(obstime=observer_time)

    vector_observer_to_object = sky_obj_itrs.cartesian - observer_itrs.cartesian

    # Convert vector to AltAz frame
    altaz_frame = AltAz(obstime=observer_time, location=observer_location)
    sky_obj_altaz = SkyCoord(vector_observer_to_object, frame=altaz_frame)

    # Convert AltAz to ICRS (equatorial coordinates)
    sky_obj_icrs = sky_obj_altaz.transform_to("icrs")

    return (sky_obj_icrs.ra, sky_obj_icrs.dec)


if __name__ == "__main__":

    print(convert_ra_dec_to_lat_lon(ra=(1,1,30), dec = 50, ra_format="hms"))

    sys.exit(0)

    # Define observer's location
    observer_location = EarthLocation(
        lat=45.5017, lon=-73.5673, height=10
    )  # Montreal, QC

    # Define aircraft's location
    aircraft_location = EarthLocation(
        lat=46.0, lon=-74.0, height=10000
    )  # Example coordinates

    # Define observation time
    observation_time = Time("2024-10-31 18:00:00")  # UTC

    # Convert to ITRS coordinates
    observer_itrs = observer_location.get_itrs(obstime=observation_time)
    aircraft_itrs = aircraft_location.get_itrs(obstime=observation_time)

    vector_observer_to_aircraft = aircraft_itrs.cartesian - observer_itrs.cartesian

    print(vector_observer_to_aircraft)

    # Convert vector to AltAz frame
    altaz_frame = AltAz(obstime=observation_time, location=observer_location)
    aircraft_altaz = SkyCoord(vector_observer_to_aircraft, frame=altaz_frame)

    # Convert AltAz to ICRS (equatorial coordinates)
    aircraft_icrs = aircraft_altaz.transform_to("icrs")

    # Output Right Ascension and Declination
    ra = aircraft_icrs.ra
    dec = aircraft_icrs.dec

    print((ra, dec))

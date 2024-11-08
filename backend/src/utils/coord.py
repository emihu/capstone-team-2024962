from astropy.time import Time
from astropy import units as u
from astropy.coordinates import EarthLocation, ITRS, AltAz, SkyCoord, Longitude, Latitude
import sys


def convert_ra_dec_to_lat_lon(ra, dec):
    observation_time = Time.now() #UTC time

    gst = observation_time.sidereal_time('mean', 'greenwich')

    lon = Longitude(ra * u.deg - gst)
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
    observation_time = Time.now() #UTC time

    sky_obj_icrs = SkyCoord(ra =10 * u.deg, dec = 20 * u.deg, frame="icrs")

    gst = observation_time.sidereal_time('mean', 'greenwich')
    print(gst.to(u.degree))

    long = Longitude(10 * u.deg - gst)
    long.wrap_angle = 180*u.deg
    print (long.degree)

    print(convert_ra_dec_to_lat_lon(ra = 10, dec = 20))
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

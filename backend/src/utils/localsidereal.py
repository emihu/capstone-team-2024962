from astropy.coordinates import EarthLocation
from astropy.time import Time
from astropy import units as u

from datetime import datetime

from timezonefinder import TimezoneFinder
from pytz import timezone

import src.utils.coord as coord

# my current lat lon
myLat = 43.665417
myLon = -79.387198

def get_local_sidereal_time(lat: float, lon: float, time: datetime = None) -> float:
    """
    Get the local sidereal time at a given gps location
    :param lat: latitude
    :param lon: longitude
    :param time: time to calculate LST in datetime format, default is now
    :return: LST
    """
    if not time:
        # step 1: get the timezone
        tf = TimezoneFinder()
        tz = tf.timezone_at(lng=lon, lat=lat)
        tz_target = timezone(tz)
        today = datetime.now()
        time = tz_target.localize(today)

    # step 2: get the LST
    observing_location = EarthLocation(lat=lat*u.deg, lon=lon*u.deg)
    observing_time = Time(time, scale='utc', location=observing_location)
    LST = observing_time.sidereal_time('mean')
    return LST.rad

if __name__ == "__main__":
    print("local sidereal time")
    print(get_local_sidereal_time(myLat, myLon))
    print(coord.convert_lat_lon_to_ra_dec(sky_obj_lat=myLat, sky_obj_lon=myLon, sky_obj_alt=0, obs_lat=myLat, obs_lon=myLon, obs_alt=0, observer_time=Time.now()))
    ra, dec = coord.convert_lat_lon_to_ra_dec(sky_obj_lat=myLat, sky_obj_lon=myLon, sky_obj_alt=0, obs_lat=myLat, obs_lon=myLon, obs_alt=0, observer_time=Time.now()) 
    lat, lon = coord.convert_ra_dec_to_lat_lon(ra=6*15, dec=dec, time=Time.now(), ra_format="deg")
    print(lat, lon)
    


    
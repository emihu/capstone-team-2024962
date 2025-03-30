from astropy.coordinates import EarthLocation
from astropy.time import Time
from astropy import units as u

from datetime import datetime

from timezonefinder import TimezoneFinder
from pytz import timezone

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

def get_local_time(lat: float, lon: float) -> float:
    tf = TimezoneFinder()
    tz = tf.timezone_at(lng=lon, lat=lat)
    tz_target = timezone(tz)
    today = datetime.now()
    local_time = tz_target.localize(today)
    return Time(local_time)
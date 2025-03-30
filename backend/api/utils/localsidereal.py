import pytz
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

def get_utc_time(lat: float, lon: float, local_time: str) -> float:
    # Convert string to datetime
    local_time = datetime.strptime(local_time, "%Y-%m-%dT%H:%M")

    # Get the timezone for the given latitude and longitude
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lng=lon, lat=lat)  # Find timezone name
    if tz_name is None:
        raise ValueError(f"Could not determine timezone for lat: {lat}, lon: {lon}")
    
    # Get the target timezone
    tz_target = timezone(tz_name)
    
    # Localize the local time (if it's naive)
    if local_time.tzinfo is None:
        local_time = tz_target.localize(local_time)  # Localize if naive time is passed

    # Convert local time to UTC
    utc_time = local_time.astimezone(pytz.utc)

    # Convert to astropy Time object
    utc_astropy_time = Time(utc_time, scale='utc')

    return utc_astropy_time
from datetime import datetime, timezone
from astropy.time import Time
import pytest
import utils.dawson_c as dawson_c
import utils.dawson_b3 as dawson_b


def test_lat_lon_to_ra_dec():
    lat = 37.7749
    lon = -2.4194
    alt = 30000
    theta = dawson_b.lon_to_theta(lon)
    print(theta)
    phi = dawson_b.lat_to_phi(lat)
    
    user_lat = 37.7749
    user_lon = 47.4194
    time = Time(datetime(2020, 3, 13, 12, 34, 24, tzinfo=timezone.utc))

    user_gps_cartesian = dawson_c.gps_cartesian(user_lat, user_lon, 0)

    aircraft_gps_cartesian = dawson_c.aircraft_theta_phi_to_cartesian(
        theta, phi, alt)
    
    vector = dawson_c.aircraft_vector_from_gps(
        user_gps_cartesian, aircraft_gps_cartesian)

    vector = dawson_c.aircraft_vector_from_gps_aligned(vector, user_lat, user_lon)

    azele = dawson_c.azimuth_elevation_from_vector(vector)

    ra, dec = dawson_c.aziele_to_radec(azele, user_lat, user_lon, time)
    returned_ra, returned_dec = dawson_c.aircraft_theta_phi_to_radec(theta, phi, alt, user_lat, user_lon, 0, time)
    print(ra, dec)
    assert ra == returned_ra
    assert dec == returned_dec








from src.utils import coord
import pytest
from astropy.time import Time
from astropy.coordinates import Latitude, Longitude
import astropy.units as u




@pytest.mark.parametrize(
    "ra, dec, time, ra_format, expected_lat_deg, expected_lon_deg",
    [
        # Test Case 1: RA in HMS
        ((1, 1, 30), 50, "2024-11-15T05:47:00", "hms", 50, None),
        # Test Case 2: RA in degrees
        (15.375, 50, "2024-11-15T05:47:00", "deg", 50, None),
        # Add more test cases as needed
    ]
)
def test_convert_ra_dec_to_lat_lon(ra, dec, time, ra_format, expected_lat_deg, expected_lon_deg):
    # Run the function
    time_gst = Time(time)

    if expected_lon_deg is None:
        gst = time_gst.sidereal_time('mean', 'greenwich').deg
        
        if isinstance(ra, tuple):
            ra_deg = coord.HMS(*ra).to_degrees()
        else:
            ra_deg = ra
        expected_lon_deg = ra_deg - gst

        # Adjust longitude to range [-180, 180]
        if expected_lon_deg > 180:
            expected_lon_deg -= 360
        elif expected_lon_deg < -180:
            expected_lon_deg += 360

    lat, lon = coord.convert_ra_dec_to_lat_lon(ra=ra, dec=dec, time=time, ra_format=ra_format)

    # Validate latitude
    assert pytest.approx(lat.degree, abs=1e-3) == expected_lat_deg
    # Validate longitude
    assert pytest.approx(lon.degree, abs=1e-3) == expected_lon_deg



import pytest
import src.utils.dawson_d as dawson_d


def generate_flight_coordinates(flight_start_ra, flight_start_dec, flight_end_ra, flight_end_dec, num_points):
    flightRa = []
    flightDec = []

    # Generate flight coordinates using linear interpolation
    for n in range(num_points):
        t = n / (num_points - 1)  # normalized parameter from 0 to 1
        ra = flight_start_ra + (flight_end_ra - flight_start_ra) * t
        dec = flight_start_dec + (flight_end_dec - flight_start_dec) * t
        flightRa.append(ra)
        flightDec.append(dec)

    return list(zip(flightRa, flightDec))

@pytest.mark.parametrize(
    "fov_size, fov_ra, fov_dec, flight_start_ra, flight_start_dec, flight_end_ra, flight_end_dec, expected",
    [
        # Test case 1: flight path from (0, 0) to (0, 1) with the field of view centered at (0, 5)
        (4.77464829, 0, 5, 0, 0, 0, 5, True),
        # Test case 2: Flight path from (10, 10) to (10, 20) with the FOV centered at (10, 0) -> expected no intersection
        (4.77464829, 10, 0, 10, 10, 10, 20, False),
        # Test case 3: Diagonal flight crossing the FOV center (0,0) from (-10,-10) to (10,10) -> expected intersection
        (5, 5, 5, 0, 0, 10, 10, True),
        # Test case 4: Flight path from (10, 0) to (20, 0) with the FOV centered at (0, 0) -> expected no intersection
        (5, 0, 0, 10, 0, 20, 0, False),
        # Test case 5: Diagonal flight near FOV centered at (30,30) from (29,29) to (31,31) -> expected intersection
        (2, 30, 30, 29, 29, 31, 31, True),
        # Test case 6: Flight path from (1,1) to (2,2) with the FOV centered at (0,0) -> expected no intersection
        (1, 0, 0, 1, 1, 2, 2, False),
    ]
)
def test_dawson_d2(fov_size, fov_ra, fov_dec, flight_start_ra, flight_start_dec, flight_end_ra, flight_end_dec, expected):
    num_points = 100

    flightRaDec = generate_flight_coordinates(flight_start_ra, flight_start_dec, flight_end_ra, flight_end_dec, num_points)

    ret = False
    for info in flightRaDec:
        ret = dawson_d.is_intersecting(info[0], info[1], fov_ra, fov_dec, fov_size)
        if ret:
            break

    assert ret == expected

@pytest.mark.parametrize(
    "fov_size, fov_ra, fov_dec, flight_start_ra, flight_start_dec, flight_end_ra, flight_end_dec",
    [
        # RA negative: RA should be within 0 to 360 degrees.
        (4.77464829, 0, 5, -1, 0, 0, 5),
        # RA too high: values above 360 are invalid.
        (4.77464829, 0, 5, 0, 0, 361, 5),
        # Dec too high: declination must be between -90 and 90 degrees.
        (4.77464829, 0, 5, 0, 0, 0, 91),
        # Dec too low: values below -90 are invalid.
        (4.77464829, 0, 5, 0, -91, 0, 5)
    ]
)
def test_dawson_d_out_of_bounds(fov_size, fov_ra, fov_dec,
                                flight_start_ra, flight_start_dec,
                                flight_end_ra, flight_end_dec):
    num_points = 10

    flightRaDec = generate_flight_coordinates(flight_start_ra, flight_start_dec, flight_end_ra, flight_end_dec, num_points)

    # Expecting a ValueError to be raised if any coordinate is out-of-bound
    with pytest.raises(ValueError):
        for info in flightRaDec:
            _ = dawson_d.is_intersecting(info[0], info[1], fov_ra, fov_dec, fov_size)
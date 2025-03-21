import math
import pytest
from src.utils.dawson_d import (
    distance_to_fov_path_1, distance_to_fov_path_2, puo, guo, check_within_fov,
    intersection_time, intersection_time_endpoint, start_end_intersection_time,
    d2, xacel, yacel, zacel, xaax, yaay, zaaz, d3
)

def test_xacel():
    assert xacel(0, 0) == pytest.approx(0.0)
    assert xacel(90, 0) == pytest.approx(-1.0)
    assert xacel(0, 90) == pytest.approx(0.0)

def test_yacel():
    assert yacel(0, 0) == pytest.approx(1.0)
    assert yacel(90, 0) == pytest.approx(0.0)
    assert yacel(45, 45) == pytest.approx(0.5)

def test_zacel():
    assert zacel(0) == pytest.approx(0.0)
    assert zacel(90) == pytest.approx(1.0)
    assert zacel(45) == pytest.approx(0.707107)

def test_xaax():
    assert xaax(0, 0, 0) == pytest.approx(0.0)
    assert xaax(90, 0, 0) == pytest.approx(-1.0)

def test_yaay():
    assert yaay(0, 0, 0, 0) == pytest.approx(0.0)

def test_zaaz():
    assert zaaz(0, 0, 0, 0) == pytest.approx(1.0)

def test_distance_to_fov_path_1():
    assert distance_to_fov_path_1(math.radians(10), 0, 0, 0, 0, 1) >= 0.0

def test_distance_to_fov_path_2():
    assert distance_to_fov_path_2(math.radians(10), 0, 0, 0, 0, 1) >= 0.0

def test_puo():
    assert puo(0, 0, 0, 0, 0) == 1
    assert puo(0, 0, 0, 0, 90) == 0

def test_guo():
    assert guo(0, 0, 0, 0, 0) == 1
    assert guo(0, 0, 0, 0, 90) == 0

def test_check_within_fov():
    assert check_within_fov(math.radians(10), 0, 0, 0, 0) == 1
    assert check_within_fov(math.radians(10), 90, 90, 0, 0) == 0

def test_intersection_time():
    assert intersection_time(0, 1) == 1
    assert intersection_time(2, 1) == 0

def test_intersection_time_endpoint():
    assert intersection_time_endpoint(1, 1) == 1
    assert intersection_time_endpoint(1, 0) == 0

def test_start_end_intersection_time():
    assert start_end_intersection_time(1, 0, 0) == True
    assert start_end_intersection_time(1, 1, 1) == True
    assert start_end_intersection_time(0, 0, 0) == False

def test_d2():
    assert d2(1, 90, 90, 0, 0) == True
    assert d2(1.0, 10.0, 10.0, 0.5, 0.5) == False
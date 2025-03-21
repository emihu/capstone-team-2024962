import math

# d2
# distance to fov for path 1
def distance_to_fov_path_1(bb, NN, MM, RA, Dec, gg):
    return math.sqrt(math.pow((xaax(NN, MM, RA) - math.sqrt(math.sin(bb)*math.sin(bb) - \
        gg*yaay(NN, MM, RA, Dec)*yaay(NN, MM, RA, Dec))), 2) + math.pow(math.cos(bb)*zaaz(NN, MM, RA, Dec), 2))

# distance to fov for path 2
def distance_to_fov_path_2(bb, NN, MM, RA, Dec, gg):
    return math.sqrt(math.pow((xaax(NN, MM, RA) + math.sqrt(math.sin(bb)*math.sin(bb) - \
        gg*yaay(NN, MM, RA, Dec)*yaay(NN, MM, RA, Dec))), 2) + math.pow(math.cos(bb)*zaaz(NN, MM, RA, Dec), 2))

# produces a 1 when yaay(tt) = +sin(bb)
def puo(NN, MM, RA, Dec, bb):
    if (yaay(NN, MM, RA, Dec) == math.sin(bb)):
        return 1
    else:
        return 0

# produces 1 when yaay(tt) = -sin(bb)
def guo(NN, MM, RA, Dec, bb):
    if (yaay(NN, MM, RA, Dec) == -math.sin(bb)):
        return 1
    else:
        return 0

# check if y coord is within fov
def check_within_fov(bb, NN, MM, RA, Dec):
    if -math.sin(bb) <= yaay(NN, MM, RA, Dec) <= math.sin(bb):
        return 1
    else:
        return 0

# detect intersection time for path
def intersection_time(d, ddis):
    if 0 <= d <= ddis:
        return 1
    else:
        return 0

# logic for double counting at endpoints
def intersection_time_endpoint(tint1, tint2):
    if (tint1 + tint2) == 2:
        return 1
    else:
        return 0

# return the time if it intersects
def start_end_intersection_time(tint1, tint2, tintem):
    if (tint1 or tint2) and (1 - tintem):
        return True
    elif ((tint1 + tint2) / 2) and (tintem):
        return True
    else:
        return False

def d2(fov, NN, MM, RA, Dec):
    # vars
    # NN, MM is RA, dec of the plane
    # RA, Dec is RA, dec of the star
    # bb is fov in rad
    bb = math.radians(fov)
    ddis = 0.01 # window of tolerance

    # check if y coordinate is within fov bounds
    gg = check_within_fov(bb, NN, MM, RA, Dec) # chatgpt logic

    # calculate distances
    d1 = distance_to_fov_path_1(bb, NN, MM, RA, Dec, gg)
    d2 = distance_to_fov_path_2(bb, NN, MM, RA, Dec, gg)
    print(f"gg:{gg}")
    print(f"d1:{d1}")
    print(f"d2:{d2}")

    # find intersection time
    tint1 = intersection_time(d1, ddis)
    tint2 = intersection_time(d2, ddis)
    tintem = intersection_time_endpoint(tint1, tint2)
    intersection_check = start_end_intersection_time(tint1, tint2, tintem) 

    return intersection_check

#d3
# x component of aircraft
def xacel(NN, MM):
    return -math.sin(math.radians(NN)) * math.sin(math.pi / 2 - math.radians(MM))

# y component of aircraft
def yacel(NN, MM):
    return math.cos(math.radians(NN)) * math.sin(math.pi / 2 - math.radians(MM))

# z component of aircraft
def zacel(MM):
    return math.cos(math.pi / 2 - math.radians(MM))

# x component of aircraft projected
def xaax(NN, MM, RA):
    return math.cos(math.radians(RA)) * xacel(NN, MM) + math.sin(math.radians(RA)) * yacel(NN, MM)

# y component of aircraft projected
def yaay(NN, MM, RA, Dec):
    cos_dec = math.cos(math.pi / 2 - math.radians(Dec))
    sin_dec = math.sin(math.pi / 2 - math.radians(Dec))

    return (-math.sin(math.radians(RA)) * cos_dec * xacel(NN, MM) + 
            math.cos(math.radians(RA)) * cos_dec * yacel(NN, MM) - 
            sin_dec * zacel(MM))

# z component of aircraft projected
def zaaz(NN, MM, RA, Dec):
    cos_dec = math.cos(math.pi / 2 - math.radians(Dec))
    sin_dec = math.sin(math.pi / 2 - math.radians(Dec))

    return (-math.sin(math.radians(RA)) * sin_dec * xacel(NN, MM) + 
            math.cos(math.radians(RA)) * sin_dec * yacel(NN, MM) + 
            cos_dec * zacel(MM))

def d3(NN, MM, RA, Dec):
    ftt = 10 * [xaax(NN, MM, RA), yaay(NN, MM, RA, Dec), zaaz(NN, MM, RA, Dec)]

def angular_distance(ra1, dec1, ra2, dec2):
    """
    Calculate the angular distance between two celestial points using the haversine formula.
    
    Parameters:
        ra1 (float): Right Ascension of the first point (in degrees)
        dec1 (float): Declination of the first point (in degrees)
        ra2 (float): Right Ascension of the second point (in degrees)
        dec2 (float): Declination of the second point (in degrees)
    Raise:
        ValueError: If ra1, dec1, ra2, or dec2 are out of range
        
    Returns:
        float: Angular distance between the two points (in degrees)
    """
    # Check if the coordinates are within the valid range
    if not (-90 <= dec1 <= 90) or not (-90 <= dec2 <= 90) or not (0 <= ra1 <= 360) or not (0 <= ra2 <= 360):
        raise ValueError("Coordinates out of range")

    # Convert degrees to radians
    ra1_rad, dec1_rad = math.radians(ra1), math.radians(dec1)
    ra2_rad, dec2_rad = math.radians(ra2), math.radians(dec2)
    
    # Differences in coordinates
    delta_ra = ra2_rad - ra1_rad
    delta_dec = dec2_rad - dec1_rad
    
    # Haversine formula
    a = math.sin(delta_dec / 2)**2 + math.cos(dec1_rad) * math.cos(dec2_rad) * math.sin(delta_ra / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Convert the result from radians to degrees
    return math.degrees(c)
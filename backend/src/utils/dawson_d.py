import math

# variables and functions defined elsewhere
RA = 1 # placeholder
Dec = 1 # placeholder

def NN(tt):
    return

def MM(tt):
    return

# d2
# distance to fov for path 1
def distance_to_fov_path_1(bb, tt, gg):
    return math.sqrt(math.pow((xaax(tt) - math.sqrt(math.sin(bb)*math.sin(bb) - gg*yaay(tt)*yaay(tt))), 2) + math.pow(math.cos(bb)*zaaz(tt), 2))

# distance to fov for path 2
def distance_to_fov_path_2(bb, tt, gg):
    return math.sqrt(math.pow((xaax(tt) + math.sqrt(math.sin(bb)*math.sin(bb) - gg*yaay(tt)*yaay(tt))), 2) + math.pow(math.cos(bb)*zaaz(tt), 2))

# produces a 1 when yaay(tt) = +sin(bb)
def puo(tt, bb):
    if (yaay(tt) == math.sin(bb)):
        return 1
    else:
        return 0

# produces 1 when yaay(tt) = -sin(bb)
def guo(tt, bb):
    if (yaay(tt) == -math.sin(bb)):
        return 1
    else:
        return 0

# check if y coord is within fov
def check_within_fov(bb, tt):
    if -math.sin(bb) <= yaay(tt) <= math.sin(bb):
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
def start_end_intersection_time(tt, tint1, tint2, tintem):
    if (tint1 or tint2) and (1 - tintem):
        return tt
    elif ((tint1 + tint2) / 2) and (tintem):
        return tt
    else:
        return 0

def d2():
    # vars
    ddis = 0.01 # window of tolerance
    bb = 1 # filler
    tt = 1 # filler

    # check if y coordinate is within fov bounds
    gg = check_within_fov(bb, tt) # chatgpt logic

    # calculate distances
    d1 = distance_to_fov_path_1(bb, tt, gg)
    d2 = distance_to_fov_path_2(bb, tt, gg)

    # find intersection time
    tint1 = intersection_time(d1, ddis)
    tint2 = intersection_time(d2, ddis)
    tintem = intersection_time_endpoint(tint1, tint2)
    tintse = start_end_intersection_time(tt, tint1, tint2, tintem) # time of intersection

#d3
# x component of aircraft
def xacel(tt):
    return -math.sin(math.radians(NN(tt))) * math.sin(math.pi / 2 - math.radians(MM(tt)))

# y component of aircraft
def yacel(tt):
    return math.cos(math.radians(NN(tt))) * math.sin(math.pi / 2 - math.radians(MM(tt)))

# z component of aircraft
def zacel(tt):
    return math.cos(math.pi / 2 - math.radians(MM(tt)))

# x component of aircraft projected
def xaax(tt):
    return math.cos(math.radians(RA)) * xacel(tt) + math.sin(math.radians(RA)) * yacel(tt)

# y component of aircraft projected
def yaay(tt):
    cos_dec = math.cos(math.pi / 2 - math.radians(Dec))
    sin_dec = math.sin(math.pi / 2 - math.radians(Dec))

    return (-math.sin(math.radians(RA)) * cos_dec * xacel(tt) + 
            math.cos(math.radians(RA)) * cos_dec * yacel(tt) - 
            sin_dec * zacel(tt))

# z component of aircraft projected
def zaaz(tt):
    cos_dec = math.cos(math.pi / 2 - math.radians(Dec))
    sin_dec = math.sin(math.pi / 2 - math.radians(Dec))

    return (-math.sin(math.radians(RA)) * sin_dec * xacel(tt) + 
            math.cos(math.radians(RA)) * sin_dec * yacel(tt) + 
            cos_dec * zacel(tt))

def d3():
    tt = 1 # filler
    ftt = 10 * [xaax(tt), yaay(tt), zaaz(tt)]
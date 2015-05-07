import math
# start and end are tuples in the form (lat, lon)
def get_circle_distance(start, end):
    x = start
    y = end

    degrees_to_radians = math.pi / 180.0
    d_2_r = degrees_to_radians  # for brevity
    radius_of_earth = 6371  # in km

    # phi = 90 - latitude
    phi = ((90.0 - x[0]) * d_2_r, (90 - y[0]) * d_2_r)

    # theta = longitude
    theta = (x[1] * d_2_r, y[1] * d_2_r)

    # Spherical distance from spherical coordinates.
    cos = (math.sin(phi[0]) * math.sin(phi[1]) * math.cos(theta[0] - theta[1]) + math.cos(phi[0]) * math.cos(phi[1]))
    arc = math.acos(cos)

    return arc * radius_of_earth
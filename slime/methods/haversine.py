from math import radians, degrees, sin, cos, asin, atan2, pow, sqrt, pi

def calculate_distance(pos1: dict, pos2: dict, R = 6371, use_eucl = True):
    # get lat and lon from nodes
    lat = (pos1["latitude"], pos2["latitude"], pos1["latitude"] - pos2["latitude"])
    lon = (pos1["longitude"], pos2["longitude"], pos1["longitude"] - pos2["longitude"])
    
    # euclidean distance
    if use_eucl: 
        return sqrt(pow(lat[2], 2) + pow(lon[2], 2))
    
    # haversine
    else: # http://www.movable-type.co.uk/scripts/latlong.html#distance 
        # convert to radians
        lat = [radians(l) for l in lat]
        lon = [radians(l) for l in lon]

        # calc distance
        a = pow(sin(lat[2]/2), 2) + cos(lat[1]) * cos(lat[2]) * pow(sin(lon[2]/2),2)
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        d = R * c

        return d

def calculate_bearing(pos1: dict, pos2: dict, R = 6371, use_eucl = False):
    """
        Calculate the bearing between the two positions (from pos2 to pos1)
    """
    # get lat and lon from nodes
    lat = (pos1["latitude"], pos2["latitude"], pos2["latitude"] - pos1["latitude"])
    lon = (pos1["longitude"], pos2["longitude"], pos2["longitude"] - pos1["longitude"])

    # euclidean distance
    if use_eucl: 
        raise Exception("Not implemented")
    
    # haversine
    else:  # http://www.movable-type.co.uk/scripts/latlong.html#bearing
        lat = [radians(l) for l in lat]
        lon = [radians(l) for l in lon]

        bearing = atan2(sin(lon[2])*cos(lat[1]), cos(lat[0])*sin(lat[1]) - sin(lat[0])*cos(lat[1])*cos(lon[2]))
        return (bearing + 2 * pi) % (2 * pi)

def calculate_position(pos: dict, dist: float, bearing: float, acc = 5, R = 6371, use_eucl = False):
    """
        Calculate the new position based on travelling dist along bearing
    """
    # euclidean distance
    if use_eucl: 
        ll = {"latitude": round(pos["latitude"] + sin(bearing) * dist, acc),
              "longitude": round(pos["longitude"] + cos(bearing) * dist, acc)}

    # haversine
    else:  # http://www.movable-type.co.uk/scripts/latlong.html#dest-point
        # convert to radians
        lat = radians(pos["latitude"])
        lon = radians(pos["longitude"])
        delta = dist / R

        # calculate new positions
        lat2 = asin(sin(lat)*cos(delta) + cos(lat)*sin(delta)*cos(bearing))
        lon2 = lon + atan2(sin(bearing)*sin(delta)*cos(lat), cos(delta) - sin(lat)*sin(lat2))

        # round
        lat2 = round(lat2, acc)
        lon2 = round(lon2, acc)

        # convert, ensure correct range, and create dict
        lon2 = (degrees(lon2) + 540) % 360 - 180
        ll = {"latitude": degrees(lat2), "longitude": lon2}
    return ll
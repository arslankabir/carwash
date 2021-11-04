from geopy import Point
from geopy.distance import distance


def get_coordinates(start_point=33.5999, end_point=73.0217, distance_meters=17.2):
    """
    Calculates the new coordinates between two points depending
    of the specified distance and the calculated bearing.

    Parameters
    ----------
    start_point: geopy.Point
    end_point: geopy.Point
    distance_meters: float

    Returns
    -------
    point: geopy.Point
        A new point between the start and the end points.
    """
    bearing = (start_point, end_point)

    # distance_km = distance_meters / 1000
    # d = distance.VincentyDistance(kilometers=distance_km)
    destination = distance.destination(point=start_point, bearing=bearing)

    return Point(destination.latitude, destination.longitude) 

cords = get_coordinates
print(cords)

# # given: lat1, lon1, bearing, distMiles
# lat2, lon2 = VincentyDistance(miles=distMiles).destination(Point(lat1, lon1), bearing)
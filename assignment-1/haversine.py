# Code is modified version of base code by Chitra Nayal of GeeksforGeeks on the Haversine formula
# https://www.geeksforgeeks.org/haversine-formula-to-find-distance-between-two-points-on-a-sphere/

import math

def haversine(lat1, lon1, lat2, lon2):
    # Calculate the great-circle distance between two points on the Earth
    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (lon2 - lon1) * math.pi / 180.0

    # Convert latitudes to radians
    lat1 = lat1 * math.pi / 180.0
    lat2 = lat2 * math.pi / 180.0

    # Apply Haversine formula
    a = (pow(math.sin(dLat / 2), 2) +
         pow(math.sin(dLon / 2), 2) *
         math.cos(lat1) * math.cos(lat2))
    rad = 6371  # Earth's radius in kilometers
    c = 2 * math.asin(math.sqrt(a))
    return rad * c

def find_closest_points(array1, array2):
    closest_points = []

    for lat1, lon1 in array1:
        min_distance = float('inf')
        closest_point = None

        for lat2, lon2 in array2:
            distance = haversine(lat1, lon1, lat2, lon2)

            if distance < min_distance:
                min_distance = distance
                closest_point = (lat2, lon2)

        closest_points.append((lat1, lon1, closest_point, min_distance))

    return closest_points

if __name__ == "__main__":
    # Example input: two arrays of geo locations
    array1 = [
        (51.5007, 0.1246),  # London
        (48.8566, 2.3522)   # Paris
    ]

    array2 = [
        (34.0522, -118.2437), # Los Angeles
        (35.6895, 139.6917)   # Tokyo
    ]

    results = find_closest_points(array1, array2)

    for lat1, lon1, closest_point, distance in results:
        print(f"Point ({lat1}, {lon1}) is closest to {closest_point} with a distance of {distance:.2f} K.M.")

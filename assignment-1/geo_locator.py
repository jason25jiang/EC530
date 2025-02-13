# Code is modified version of base code by Chitra Nayal of GeeksforGeeks on the Haversine formula
# https://www.geeksforgeeks.org/haversine-formula-to-find-distance-between-two-points-on-a-sphere/

# import pandas as pd
import csv
import math

# function to read in columns of latitude and longitude from csv files
def is_valid_coordinate(lat, lon):
    return -90 <= lat <= 90 and -180 <= lon <= 180

def decimal_to_dms(degrees):
    d = int(degrees)
    m = int((abs(degrees) - abs(d)) * 60)
    s = (abs(degrees) - abs(d) - m / 60) * 3600
    return f"{d}°{m}'{s:.2f}\""

def read_csv(filename):
    coordinates = []
    with open(filename, "r") as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames

        for col in headers:
            if col.lower() in ["latitude", "lat"]:
                lat_col = col
            elif col.lower() in ["longitude", "lng", "lon"]:
                lon_col = col
                
        for row in reader:
                if row[lat_col] and row[lon_col]:
                    lat = float(row[lat_col])
                    lon = float(row[lon_col])
                    if is_valid_coordinate(lat, lon):
                        coordinates.append((lat,lon))
    return coordinates



def haversine(lat1, lon1, lat2, lon2):
    # Calculate distance between two points on the Earth
    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (lon2 - lon1) * math.pi / 180.0

    # Convert latitudes to radians
    lat1 = lat1 * math.pi / 180.0
    lat2 = lat2 * math.pi / 180.0

    # Haversine formula
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
    # test 1
    # array1 = [(42.454962, -71.107704)]
    # array2 = read_csv("test-1/Boston_311_012225.csv")
    # results = find_closest_points(array1, array2)
    
    #test 2
    array1 = read_csv("test-2/world_cities.csv")
    array2 = read_csv("test-2/iata-icao.csv")
    results = find_closest_points(array1, array2)

    #test 3
    # array1 = read_csv("test-3/cities.csv")
    # array2 = read_csv("test-3/iata-icao.csv")
    # results = find_closest_points(array1, array2)

    for lat1, lon1, closest_point, distance in results:
            lat_dms = decimal_to_dms(lat1)
            lon_dms = decimal_to_dms(lon1)
            closest_lat_dms = decimal_to_dms(closest_point[0])
            closest_lon_dms = decimal_to_dms(closest_point[1])
            print(f"Point ({lat_dms}, {lon_dms}) is closest to ({closest_lat_dms}, {closest_lon_dms}) with a distance of {distance:.2f} KM")

# ec-530-assignment-1
After condcuting some brief research on finding the distance between two GPS locations, it was discovered that the Haversine formula exists to "calculate the shortest distance between two points on a sphere using their latitudes and longitudes measured along the surface." (GeeksforGeeks) The surface they are describing would be the Earth which is attributed as being a perfect sphere.

Code Explanation:
- haversine(lat1, lon1, lat2, lon2): Implements the Haversine formula to calculate the shortest distance (in kilometers) between two geographical points on Earth, given their latitudes and longitudes.
- find_closest_points(array1, array2): Takes two arrays of geographical coordinates (latitude and longitude). For each point in array1, it calculates the distance to every point in array2 using the haversine function. Identifies and stores the closest point from array2 along with the corresponding distance. Returns a list of tuples, where each tuple contains: the point from array1, the closest point from array2, and the minimum distance.

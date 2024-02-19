import numpy as np
from scipy.spatial import ConvexHull, Voronoi
from shapely.geometry import Point, Polygon
import math
import random

def generate_random_list_of_points():
    """ Returns a random list of points """
    MAXPOINTS = 20  # Max number of points for the points list
    MAXVALUE = 10   # Max numerical value of a point
    MINVALUE = -10  # Min numerical value of a point

    list_of_points = []

    for _ in range(MAXPOINTS):
        # Generate two random numbers to create a Point object
        x = random.randint(MINVALUE, MAXVALUE)
        y = random.randint(MINVALUE, MAXVALUE)
        point = (x,y)
        list_of_points.append(point)

    return np.array(list_of_points)

def intersection(line1, line2):

    denom = ((line1[0][0] - line1[1][0]) * (line2[0][1] - line2[1][1]) - (line1[0][1] - line1[1][1]) * (line2[0][0] - line2[1][0]))

    if denom != 0:
        t = (((line1[0][0] - line2[0][0]) * (line2[0][1] - line2[1][1]) - (line1[0][1] - line2[0][1]) * (line2[0][0] - line2[1][0])) / 
            ((line1[0][0] - line1[1][0]) * (line2[0][1] - line2[1][1]) - (line1[0][1] - line1[1][1]) * (line2[0][0] - line2[1][0])))
        u = (((line1[0][0] - line2[0][0]) * (line1[0][1] - line1[1][1]) - (line1[0][1] - line2[0][1]) * (line1[0][0] - line1[1][0])) /
            ((line1[0][0] - line1[1][0]) * (line2[0][1] - line2[1][1]) - (line1[0][1] - line1[1][1]) * (line2[0][0] - line2[1][0])))

        # check if line actually intersect
        if (0 <= t and t <= 1 and 0 <= u and u <= 1):
            return [(line1[0][0] + t * (line1[1][0] - line1[0][0])), (line1[0][1] + t * (line1[1][1] - line1[0][1]))]
        else:
            return 0

    return 0

def find_intersections(list_of_lines):
    intersection_list = []
    tried_pairs = []
    for line1 in list_of_lines:
        for line2 in list_of_lines:
            if line1 != line2:
                i = intersection(line1, line2)
                if i != 0:
                    if (line1, line2) not in tried_pairs:
                        intersection_list.append(i)
                        tried_pairs.append((line1, line2))
                        tried_pairs.append((line2, line1))

    return intersection_list

def find_distance_between_points(p1, p2):
    """ Find distance between two points """
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]

    dist = math.sqrt((x2-x1)**2 + (y2-y1)**2)

    return dist, p1, p2

def find_closest_pair_of_points(list_of_points):
    """ Finds closest pair of points """
    # list_of_points  # Passes in our list (tuple) of points
    min_distance_found = 0
    final_points = []
    distances = []

    # # Check for all points list
    for point1 in list_of_points:
        for point2 in list_of_points:
            if np.array_equal(point1, point2) == False:
                distance, _, _ = find_distance_between_points(point1, point2)
                if min_distance_found == 0:
                    min_distance_found = distance
                    final_points.append(point1)
                    final_points.append(point2)
                elif distance < min_distance_found:
                    min_distance_found = distance
                    final_points[0] = point1
                    final_points[1] = point2

    return final_points[0], final_points[1]

def find_convex_hull(list_of_points):
    hull = ConvexHull(list_of_points)
    return hull

def find_voronoi_points(list_of_points):
    vor = Voronoi(list_of_points)
    return vor

def extract_points(points_list):
    """ Given an Point object, return a list of all x and y values """
    x_values = [point[0] for point in points_list]
    y_values = [point[1] for point in points_list]
    
    return x_values, y_values # Returns a list of x values, and a list of y values, for graphing

def largest_empty_circle(convex_hull, voronoi_points, random_points):

    convex_hull = Polygon([random_points[vertex] for vertex in convex_hull.vertices])

    # Filter Voronoi vertices within convex hull
    vor_points = []
    for vertex in voronoi_points.vertices:
        point = Point(vertex)
        if convex_hull.contains(point):
            vor_points.append(vertex)


    max_radius = 0
    max_center = None

    for point in vor_points:
        center = Point(point)
        if not convex_hull.contains(center):
            continue

        # Calculate maximum possible radius
        min_distance_to_boundary = convex_hull.exterior.distance(center)
        min_distance_to_point = min(center.distance(Point(p)) for p in random_points)
        radius = min(min_distance_to_boundary, min_distance_to_point)

        if radius > max_radius:
            max_radius = radius
            max_center = center

    return max_center, max_radius

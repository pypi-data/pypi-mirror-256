from matplotlib import pyplot as plt
from new_math import *


def show_convex_hull(list_of_points):
    """ Graphs a convex hull """
    hull = find_convex_hull(list_of_points)

    # Plotting
    fig, ax = plt.subplots()

    # Plot random points
    ax.scatter(list_of_points[:,0], list_of_points[:,1], color='blue', label='Random Points')

    # Plot convex hull
    for simplex in hull.simplices:
        ax.plot(list_of_points[simplex, 0], list_of_points[simplex, 1], color='black')

    plt.show()

    return 

def add_points(list_of_points):
    """ Adds a point to a graph """
    for point in list_of_points:
        plt.plot(point[0], point[1], 'ro')
    plt.show()

def show_closest_pair(list_of_points):
    """ Adds a point to a graph """
    p1, p2 = find_closest_pair_of_points(list_of_points)
    for point in list_of_points:
        plt.plot(point[0], point[1], 'bo')

    x_values = [p1[0], p2[0]]
    y_values = [p1[1], p2[1]]
    plt.plot(x_values, y_values, 'ro', linestyle = 'solid')

    plt.show()

def extract_points(points_list):
    """ Given an Point object, return a list of all x and y values """
    x_values = [point.x for point in points_list]
    y_values = [point.y for point in points_list]

    return x_values, y_values # Returns a list of x values, and a list of y values, for graphing

def get_line_segment_points(line):
    point1 = (line.point1.x, line.point1.y)
    point2 = (line.point2.x, line.point2.y)

    return point1, point2

def show_all_lines_and_intersections(list_of_lines):
    """ Given tuple of lines, graphs intersections between them"""
    for line in list_of_lines:
        x_values = [line[0][0], line[1][0]]
        y_values = [line[0][1], line[1][1]]
        plt.plot(x_values, y_values, 'bo', linestyle = 'solid')
    
    intersections = find_intersections(list_of_lines)
    for point in intersections:
        plt.plot(point[0], point[1], 'ro')
    plt.show()
    return

def show_largest_inside_circle(list_of_points):
    
    
    hull = find_convex_hull(list_of_points)
    vor = find_voronoi_points(list_of_points)
    
    # Calculate largest empty circle
    center, radius = largest_empty_circle(hull, vor, list_of_points)

    # Plotting
    fig, ax = plt.subplots()

    # Plot random points
    ax.scatter(list_of_points[:,0], list_of_points[:,1], color='blue', label='Random Points')

    # Plot convex hull
    for simplex in hull.simplices:
        ax.plot(list_of_points[simplex, 0], list_of_points[simplex, 1], color='black')

    # Plot largest empty circle
    if center is not None:
        circle = plt.Circle((center.x, center.y), radius, color='green', fill=False, label='Largest Empty Circle')
        ax.add_artist(circle)
        ax.plot(center.x, center.y, 'go', label='Center')
    
    plt.show()
    return

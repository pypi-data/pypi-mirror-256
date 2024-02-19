# Team 1 4900 first project

Computational Geometry package for Python. 

# This package grants functionality on a 2-d euclidean plane.
# Functionalities include:

- Line segment intersection: Find the intersections between a given set of line segments.
- Closest pair of points: Given a set of points, find the two with the smallest distance from each other.
- Convex hull: Given a set of points, find the smallest convex polyhedron/polygon containing all the points, represented as the set of points on the polygon edge.
- Largest empty circle: Given a set of points, find a largest circle with its center inside of their convex hull and enclosing none of them.
- graphing all of the above listed functionalities

## How to Call new_math.py functions: 

generate_random_list_of_points(): Returns a tuple of x,y points

Line segment intersection:        show_all_line_intersections(list_of_your_lines) 

Closest pair of points:           find_closest_pair_of_points(list_of_points)

Convex hull:                      show_convex_hull(list_of_your_points)

Largest empty circle:       l     largest_inside_circle(list_of_your_points) 


## How to Call graphing.py functions - use tuples

add_points(list_of_points)

show_closest_pair(list_of_points)               - shows all points, and the closest pair of points.

show_all_lines_and_intersections(list_of_lines) - Shows all intersections between lines

show_largest_inside_circle(list_of_points)      - Shows largest empty circle

show_convex_hull(list_of_points)                - Shows convex hull

# TEAM REFERENCES:

- HOW TO CREATE PACKAGES - https://packaging.python.org/en/latest/tutorials/packaging-projects/
- Alex's example package - https://test.pypi.org/project/test-cs-4900-package-creation/0.0.1/
- Convex Polygon incircle - https://observablehq.com/@mbostock/convex-polygon-incircle
- Closest pair of points example algorithm: https://www.geeksforgeeks.org/closest-pair-of-points-using-divide-and-conquer-algorithm/
- Two line intersection example 1: https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
- Two line intersection example 2: https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
- Convex Hull algorithms, I think we should use Grahm Scan: https://en.wikipedia.org/wiki/Convex_hull_algorithms
- For largest circle find the max point, find the min point and the use the circle equation to draw the circle
- For line intersection: https://stackoverflow.com/questions/20677795/how-do-i-compute-the-intersection-point-of-two-lines

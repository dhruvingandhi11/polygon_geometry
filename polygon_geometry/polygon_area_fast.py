from functools import cmp_to_key
# from helper.polygon_geometry.geometry_orientation import orientation

from geometry_orientation import orientation


p0 = (0,0)

def get_polygon_area(points):
    """Returns the polygon area of ordered points"""
    X, Y = zip(*[(point[0], point[1]) for point in points])
    n = len(X)
    area = 0.0
    j = n - 1
    for i in range(n):
        area += (X[j] + X[i]) * (Y[j] - Y[i])
        j = i  # j is previous vertex to i

    return int(abs(area / 2.0))


def find_lowest_point(points):
    """Returns the lowest point in unordered points of polygon"""
    ymin = points[0][1]
    min = 0
    
    for i in range(1, len(points)):
        y = points[i][1]
        if ((y < ymin) or
            (ymin == y and points[i][0] < points[min][0])):     # if y same, sort by x
            ymin = points[i][1]
            min = i
    
    return min


def distSq(p1, p2):
    """A utility function to return square of distance between p1 and p2"""
    return ((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]))


def compare_via_orientation(p1, p2):
    """A function used by cmp_to_key function to sort an array of points with respect to the first point"""
    # Find orientation
    o = orientation(p0, p1, p2)
    val = 0
    if o == 0:      # Colinear
        if distSq(p0, p2) >= distSq(p0, p1):
            val = -1
        else:
            val = 1
    else:
        if o == 2:  # Anti-clock
            val = -1
        else:       # Clock
            val = 1
    # print(f"comparing {p0}, {p1}, {p2} -> {o} -> {val}")
    return val


def get_Ordered_points(polygon_points: list):
    """Returns the Ordered Points"""
    # Get index of lowest point
    min_index = find_lowest_point(polygon_points)
    # print(f"{min_index} , {polygon_points[min_index]}")

    # Put lowest point to start of array
    polygon_points.insert(0, polygon_points.pop(min_index))
    # print(f"{polygon_points = }")
    
    global p0
    p0 = polygon_points[0]
    ordered_polygon_points = sorted(polygon_points, key=cmp_to_key(compare_via_orientation))
    # print(f"{ordered_polygon_points = }")

    return ordered_polygon_points


if __name__ == "__main__":
    import timeit
    # polygon_points = [(2586, 664), (2586, 270), (2586, 269), (2105, 664), (2105, 270)]
    # # print(timeit.timeit(lambda : get_Ordered_points(polygon_points), number=10_000))
    # get_Ordered_points(polygon_points)
    # print(timeit.timeit(lambda : find_lowest_point(polygon_points), number=10_000))

    # polygon_points = [(32, 15), (4, 19), (30, 20), (19, 25), (7, 25)]
    polygon_points = [[514,453], [1313, 488],[1329,589], [493,564]]
    #  [[802,500],]
    ordered_polygon_points = get_Ordered_points(polygon_points)
    print(get_polygon_area(ordered_polygon_points))



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




polygon_points = [[800,500], [800+50, 500],[800+50,500+60], [800,500+60] ]
print(get_polygon_area(polygon_points))
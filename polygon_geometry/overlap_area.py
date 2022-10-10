import json
# from helper.polygon_geometry.geometry_orientation import isInsidePolygon, doIntersect, onSegment
# from helper.polygon_geometry.polygon_area_fast import get_polygon_area, get_Ordered_points
import math
import cv2
import numpy as np

from polygon_area_fast import get_polygon_area, get_Ordered_points
from geometry_orientation import isInsidePolygon, doIntersect, onSegment



class Point:
    x: int
    y: int

    def __init__(self, point_tuple: tuple):
        self.x = point_tuple[0]
        self.y = point_tuple[1]


# Returns the intersection point of 2 line segments
def find_intersection_point(p1: tuple, p2: tuple, p3: tuple, p4: tuple):

    # print()
    # print(f"{p1 = }")
    # print(f"{p2 = }")
    # print(f"{p3 = }")
    # print(f"{p4 = }")

    p1 = Point(p1)
    p2 = Point(p2)
    p3 = Point(p3)
    p4 = Point(p4)

    x = None
    c1 = None
    c2 = None

    # Parameters of line1
    m1 = math.atan2((p1.y - p2.y), (p1.x - p2.x))
    if abs(m1) == math.pi / 2:      # Vertical lines
        x = p1.x
        # print("got x from line1")
    else:
        c1 = p1.y - math.tan(m1) * p1.x

    # Parameters of line2
    m2 = math.atan2((p3.y - p4.y), (p3.x - p4.x))
    if abs(m2) == math.pi / 2:      # Vertical lines
        x = p3.x
        # print("got x from line2")
    else:
        c2 = p3.y - math.tan(m2) * p3.x

    # print(f"{m1 = }")
    # print(f"{c1 = }")
    # print(f"{m2 = }")
    # print(f"{c2 = }")

    # print(f"{x = }")
    # Compute intersection point
    if (abs(m1 - m2) == math.pi) or (m1 == m2):               # Colinearity
        # print("Handling colinearity")
        points: list = [(p1.x, p1.y), (p2.x, p2.y), (p3.x, p3.y), (p4.x, p4.y)]
        points.sort(key=lambda x: x[0])  # Sort along x-axis
        points.sort(key=lambda x: x[1])  # Sort along y-axis
        # print(points[1:3])
        return (points[1:3])

    if x is None:
        x = -1 * (c1 - c2) / (math.tan(m1) - math.tan(m2))
        y = int(math.tan(m1) * x + c1)
        x = int(x)
    else:
        if c1 is None:                      # line 1 is perpendicular
            y = int(math.tan(m2) * x + c2)
        elif c2 is None:                    # line 2 is perpendicular
            y = int(math.tan(m1) * x + c1)

    # print ((x, y))
    # return (x, y)
    return (x, y)


# Returns overlapping area
def find_overlapping_area(quad1: list, quad2: list):
    img = np.zeros(shape=(1944, 2592, 3))
    """Get inside points"""
    inside_points = []

    # Find if edges are inside another quad
    # Quad1 edges lies inside Quad2
    for i, point in enumerate(quad1):
        # cv2.circle(img, point, 2, (0, 255, 0), -1)
        # cv2.putText(img, str(point), point, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
        # cv2.line(img, quad1[i], quad1[(i + 1) % len(quad1)], (0, 255, 0), 1)
        if isInsidePolygon(points=quad2, p=point , INT_MAX = 10000 , INT_MIN = -10000):
            inside_points.append(point)
            # print('inside_points1:-',inside_points)
    # Quad2 edges lies inside Quad1
    for i, point in enumerate(quad2):
        # cv2.circle(img, point, 2, (0, 0, 255), -1)
        # cv2.putText(img, str(point), point, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), 1)
        # cv2.line(img, quad2[i], quad2[(i + 1) % len(quad2)], (0, 0, 255), 1)
        if isInsidePolygon(points=quad1, p=point, INT_MAX = 10000 , INT_MIN = -10000):
            inside_points.append(point)
            # print('inside_points2:-',inside_points)
    # cv2.imshow("test", img)
    # cv2.imshow("test", cv2.resize(img, (img.shape[0] // 2, img.shape[1] // 2)))

    print(f"{inside_points = }")
    # Draw inside points
    for CenterCoordinates in inside_points:
        # cv2.circle(img, CenterCoordinates, 2, (255, 255, 255), -1)
        pass

    """Get intersection points"""
    intersection_points = []

    for i in range(len(quad1)):
        for j in range(len(quad2)):
            # Line Segment Points
            lsp = [quad1[i], quad1[(i + 1) % len(quad1)],
                   quad2[j], quad2[(j + 1) % len(quad2)]]
            if doIntersect(lsp[0], lsp[1], lsp[2], lsp[3]):
                # print("Intersecting line segments", lsp[0], lsp[1], lsp[2], lsp[3])
                points = find_intersection_point(lsp[0], lsp[1], lsp[2], lsp[3])
                if type(points) == tuple:
                    intersection_points.append(points)
                else:
                    intersection_points += points

    print(f"{intersection_points = }")
    # Draw intersection points
    for CenterCoordinates in intersection_points:
        # cv2.circle(img, CenterCoordinates, 2, (255, 0, 255), -1)
        # cv2.putText(img, str(CenterCoordinates), CenterCoordinates, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 0, 255), 1)
        pass
    k = inside_points+intersection_points
    print(k)
    k = set(k)
    print(k)
    k = list(k)
    print(k)
    polygon_points = list(set(inside_points + intersection_points))
    print(f"{polygon_points = }")
    if len(polygon_points) < 3:
        return 0

    """Order polygon points"""
    ordered_polygon_points = get_Ordered_points(polygon_points)
    print(f"{ordered_polygon_points = }")

    # Draw overlapping polygon
    #comment by jigar
    # for i in range(len(ordered_polygon_points)):
    #     cv2.line(img, ordered_polygon_points[i], ordered_polygon_points[(i + 1) % len(ordered_polygon_points)],
    #              (0, 255, 255), 3)

    # cv2.imwrite("tets.jpg", img)#comment ny jigar
    # cv2.imshow("img.png", img)
    # cv2.waitKey(0)
    # cv2.imshow("img.png", cv2.resize(img, (img.shape[0] // 2, img.shape[1] // 2)))

    if len(ordered_polygon_points) < 3:
        return 0

    """Calulate area"""
    polygon_area = get_polygon_area(ordered_polygon_points)

    print(f"{polygon_area = }")

    return polygon_area


# Driver code
if __name__ == '__main__':
    # polygon1 = {
    #     "top_left": (65, 181),
    #     "top_right": (118, 194),
    #     "bottom_left": (65, 253),
    #     "bottom_right": (118, 274)
    # }
    # polygon2 = {
    #     "top_left": [85, 215],
    #     "top_right": [42, 214],
    #     "bottom_left": [116, 229],
    #     "bottom_right": [61, 276]
    # }

    # Oredered polygon, Dict doesn't preserve order
    # polygon1 = [
    #     [
    #       1030,
    #       266
    #     ],
    #     [
    #       1014,
    #       708
    #     ],
    #     [
    #       1610,
    #       728
    #     ],
    #     [
    #       1686,
    #       576
    #     ],
    #     [
    #       1604,
    #       328
    #     ]
    #   ]
    polygon1 = [(2028, 216), (1994, 828), (2586, 864), (2586, 230)]
    # polygon1 = [
    #     [
    #       502,
    #       826
    #     ],
    #     [
    #       514,
    #       1494
    #     ],
    #     [
    #       830,
    #       1598
    #     ],
    #     [
    #       1172,
    #       1594
    #     ],
    #     [
    #       1334,
    #       1530
    #     ],
    #     [
    #       1408,
    #       1098
    #     ],
    #     [
    #       1404,
    #       690
    #     ],
    #     [
    #       748,
    #       680
    #     ],
    #     [
    #       670,
    #       802
    #     ]
    #   ]
    # polygon1 = [
    #     [
    #       544,
    #       696
    #     ],
    #     [
    #       520,
    #       1358
    #     ],
    #     [
    #       710,
    #       1540
    #     ],
    #     [
    #       1042,
    #       1568
    #     ],
    #     [
    #       1466,
    #       1474
    #     ],
    #     [
    #       1486,
    #       834
    #     ],
    #     [
    #       1304,
    #       802
    #     ],
    #     [
    #       1294,
    #       724
    #     ]
    #   ]
    # x1, y1, x2, y2 = 6485, 1572, 8776, 3648
    # x1, y1, x2, y2 = 6465, 2264, 7815, 3556
    # x1, y1, x2, y2 = 7417, 1779, 7904, 2187
    # x1, y1, x2, y2 = 7238, 1274, 7836, 1905
    # x1, y1, x2, y2 =5341, 534, 6111, 1394
    # x1, y1, x2, y2 = 0, 2824, 705, 4335
    # x1, y1, x2, y2 = 2105, 270, 2586, 664
    # new_x1 = (x1 * 2592) // 10000
    # new_x2 = (x2 * 2592) // 10000
    # new_y1 = (y1 * 1944) // 10000
    # new_y2 = (y2 * 1944) // 10000

    # polygon1 = [(10, 10), (20, 40), (40, 30), (30, 10)]
    # polygon2 = [(20, 20), (30, 20), (30, 0), (20, 0)]

    # for i, (point1, point2) in enumerate(zip(polygon1, polygon2)):
    #     polygon1[i] = (point1[0] + 20, point1[1])
    #     polygon2[i] = (point2[0] + 20, point2[1])


    polygon1 = [(514,453), (1313, 488),(1329,589), (493,564) ]
    polygon2 = [(800,500), (800+50, 500),(800+50,500+60), (800,500+60) ]
    

    print("polygon points1", polygon1)
    print("polygon points2", polygon2)
    # print("bbox", x1, y1, x2, y2)
    # print("bbox rect", new_x1, new_y1, new_x2, new_y2)
    # new_x1, new_y1, new_x2, new_y2 = 0, 548, 182, 842
    # polygon2 = [(new_x1, new_y1), (new_x2, new_y1), (new_x2, new_y2), (new_x1, new_y2)]
    # polygon2 = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
    area = find_overlapping_area(polygon1, polygon2)
    # k = timeit.timeit(find_overlapping_area(polygon1, polygon2), 1200)
    print("over lapped", area)
    # print("polygon total", get_polygon_area(polygon1))
    # print("bbox area", (new_x2 - new_x1) * (new_y2 - new_y1))

    # with open("roi_polygon_points.json", "r") as f:
    #     rois_data = json.load(f)
    #     f.close()
    #
    # for k, data in rois_data.items():
    #     for camera in data:
    #         # area = get_polygon_area(data[camera]["points"])
    #         # rois_data[k][camera]['area'] = area
    #         print(rois_data[k][camera]['points'])
    #         rois_data[k][camera]['points'] = [tuple(x) for x in rois_data[k][camera]['points']]
    #         print(rois_data[k][camera]['points'])
    # #     break
    # # exit()
    # with open("roi_polygon_points.json", "w") as f:
    #     json.dump(rois_data, f)
    #     f.close()

# A Python3 program to check if a given point
# lies inside a given polygon
# Refer https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
# for explanation of functions onSegment(),
# orientation() and doIntersect()

# Define Infinite (Using INT_MAX
# caused overflow problems)
INT_MAX = 10000
def onSegment(p: tuple, q: tuple, r: tuple) -> bool:
    """Given three colinear points p, q, r,

    the function checks if point q lies
    on line segment 'pr'
    """

    if ((q[0] <= max(p[0], r[0])) &
        (q[0] >= min(p[0], r[0])) &
        (q[1] <= max(p[1], r[1])) &
        (q[1] >= min(p[1], r[1]))):
        return True
    return False

def orientation(p: tuple, q: tuple, r: tuple) -> int:
    """
    To find orientation of ordered triplet (p, q, r).

    The function returns following values

    0 --> p, q and r are colinear
    
    1 --> Clockwise
    
    2 --> Counterclockwise
    """

    val = (((q[1] - p[1]) * (r[0] - q[0])) -
           ((q[0] - p[0]) * (r[1] - q[1])))

    if val == 0:    # Collinear
        return 0
    if val > 0:     # Clock
        return 1  
    else:           # Counterclock           
        return 2

def doIntersect(p1, q1, p2, q2) -> bool:
    """
    Given 2 line segments points p1, q1, p2, q2

    the function checks if the line segment intersects
    """

    # Find the four orientations needed for
    # general and special cases
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # General case
    if (o1 != o2) and (o3 != o4):
        return True

    # Special Cases
    # p1, q1 and p2 are colinear and
    # p2 lies on segment p1q1
    if (o1 == 0) and (onSegment(p1, p2, q1)):
        return True

    # p1, q1 and p2 are colinear and
    # q2 lies on segment p1q1
    if (o2 == 0) and (onSegment(p1, q2, q1)):
        return True

    # p2, q2 and p1 are colinear and
    # p1 lies on segment p2q2
    if (o3 == 0) and (onSegment(p2, p1, q2)):
        return True

    # p2, q2 and q1 are colinear and
    # q1 lies on segment p2q2
    if (o4 == 0) and (onSegment(p2, q1, q2)):
        return True

    return False

def is_inside_polygon(points: list, p: tuple) -> bool:
    """
    Do not use this, has some bug cases
    Returns true if the point p lies
    inside the polygon[] with n vertices
    """
    n = len(points)

    # There must be at least 3 vertices
    # in polygon
    if n < 3:
        return False

    # Create a point for line segment
    # from p to infinite
    extreme = (INT_MAX, p[1])
    count = i = 0

    while True:
        next = (i + 1) % n

        # Check if the line segment from 'p' to
        # 'extreme' intersects with the line
        # segment from 'polygon[i]' to 'polygon[next]'
        if (doIntersect(points[i], points[next], p, extreme)):

            # If the point 'p' is colinear with line
            # segment 'i-next', then check if it lies
            # on segment. If it lies, return true, otherwise false
            if orientation(points[i], p, points[next]) == 0:
                return onSegment(points[i], p, points[next])

            count += 1

        i = next

        if (i == 0):
            break

    # Return true if count is odd, false otherwise
    return (count % 2 == 1)

def isInsidePolygon(points: list, p: tuple, INT_MAX, INT_MIN=0) -> bool:
    """Version 2.0 to remove discrepancies of Version 1.0

    Returns:
        bool: if the point lies inside polygon
    """

    n = len(points)
    r_extreme = (INT_MAX, p[1])
    l_extreme = (INT_MIN, p[1])
    i = 0
    r_flag = False
    l_flag = False

    while True:
        next = (i + 1) % n
        
        if r_flag == False:
            if (doIntersect(points[i], points[next], p, r_extreme)):

                if orientation(points[i], p, points[next]) == 0:
                    return onSegment(points[i], p, points[next])              
                r_flag = True
            
        if l_flag == False:
            if (doIntersect(points[i], points[next], p, l_extreme)):

                if orientation(points[i], p, points[next]) == 0:
                    return onSegment(points[i], p, points[next])              
                l_flag = True

        if r_flag and l_flag:
            return True
            
        i = next
        if (i == 0):
            return False


# Driver code
if __name__ == '__main__':

    # polygon1 = [(0, 0), (10, 0), (10, 10), (0, 10)]

    # p = (20, 20)
    # if (is_inside_polygon(points=polygon1, p=p)):
    #     print('Yes')
    # else:
    #     print('No')

    # p = (5, 5)
    # if (is_inside_polygon(points=polygon1, p=p)):
    #     print('Yes')
    # else:
    #     print('No')

    # polygon2 = [(0, 0), (5, 0), (5, 5), (3, 3)]

    # p = (3, 3)
    # if (is_inside_polygon(points=polygon2, p=p)):
    #     print('Yes')
    # else:
    #     print('No')

    # p = (5, 1)
    # if (is_inside_polygon(points=polygon2, p=p)):
    #     print('Yes')
    # else:
    #     print('No')

    # p = (8, 1)
    # if (is_inside_polygon(points=polygon2, p=p)):
    #     print('Yes')
    # else:
    #     print('No')

    # polygon3 = [(0, 0), (10, 0), (10, 10), (0, 10)]

    # p = (-1, 10)
    # if (is_inside_polygon(points=polygon3, p=p)):
    #     print('Yes')
    # else:
    #     print('No')


    # print(orientation(p=(4,0), r=(2,0), q=(10,5)))
    # print(orientation(p=(2,5), r=(4,0), q=(10,5)))


    print(orientation(p=(1,0), q=(2,0), r=(3,0)))
    print(orientation(p=(1,0), r=(2,0), q=(3,0)))


# P1 = [(-30, 25)]
P1 = [(0, 27)]
P2 = [(-20, 25), (0, 30), (15, 20), (-20, 20)]

inside_points = []
        
def onSegment(p, q, r):
    if ( (q[0] <= max(p[0], r[0])) and (q[0] >= min(p[0], r[0])) and
           (q[1] <= max(p[1], r[1])) and (q[1] >= min(p[1], r[1]))):
        return True
    return False
 
def orientation(p, q, r):
     
    val = (float(q[1] - p[1]) * (r[0] - q[0])) - (float(q[0] - p[0]) * (r[1] - q[1]))
    if (val > 0):
        # Clockwise orientation
        return 1
    elif (val < 0):
        # Counterclockwise orientation
        return 2
    else:
        # Collinear orientation
        return 0

def doIntersect(p1,q1,p2,q2):

    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)
 
    # General case
    if ((o1 != o2) and (o3 != o4)):
        return 1
 
    # Special Cases
    if ((o1 == 0) and onSegment(p1, p2, q1)):
        return 1
 
    if ((o2 == 0) and onSegment(p1, q2, q1)):
        return 1
 
    if ((o3 == 0) and onSegment(p2, p1, q2)):
        return 1

    if ((o4 == 0) and onSegment(p2, q1, q2)):
        return 1

    return False

def isInside(points, p):
     
    INT_MAX = 10000
    INT_MIN = -10000

    
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


if __name__ == "__main__":
    for pt in P1:
        if isInside(P2, pt):
            if pt not in inside_points:
                inside_points.append(pt)

    print('\nInside Points:\n', inside_points)

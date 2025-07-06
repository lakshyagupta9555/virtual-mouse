import numpy as np

# def get_angle(a, b, c):
#     radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
#     angle = np.abs(np.degrees(radians))
#     return angle


# def get_distance(landmark_list):
#     if len(landmark_list) < 2:
#         return
#     (x1, y1), (x2, y2) = landmark_list[0], landmark_list[1]
#     L = np.hypot(x2 - x1, y2 - y1)
#     return np.interp(L, [0, 1], [0, 1000])
import math

def get_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.hypot(x2 - x1, y2 - y1)

def get_angle(a, b, c):
    """Calculates angle ABC (in degrees)"""
    ax, ay = a
    bx, by = b
    cx, cy = c

    ab = (ax - bx, ay - by)
    cb = (cx - bx, cy - by)

    dot = ab[0] * cb[0] + ab[1] * cb[1]
    cross = ab[0] * cb[1] - ab[1] * cb[0]

    angle = math.atan2(cross, dot)
    angle = abs(math.degrees(angle))
    if angle > 180:
        angle = 360 - angle
    return angle

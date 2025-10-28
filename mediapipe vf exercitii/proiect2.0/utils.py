import numpy as np
import math

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    dist_ab = np.linalg.norm(a - b)
    dist_bc = np.linalg.norm(b - c)
    dist_ac = np.linalg.norm(a - c)

    if dist_ab == 0 or dist_bc == 0:
        return 0

    cos_angle = (dist_ab ** 2 + dist_bc ** 2 - dist_ac ** 2) / (2 * dist_ab * dist_bc)
    cos_angle = np.clip(cos_angle, -1.0, 1.0)
    angle = np.degrees(np.arccos(cos_angle))
    return angle


def distance_points(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def transformTuple(landmark):
    return (landmark.x, landmark.y)
from pygame.math import Vector2 as Vector
import sys


def seperate_point(static, to_move, length):
    seperation_vector = to_move - static
    if int(seperation_vector.length() * 100) == int(length * 100):
        return to_move
    seperation_vector = seperation_vector.normalize()
    return static + seperation_vector * length

# TODO useless might need to remove


def check_if_parallel(first, second):
    return abs((first * second) / (
        first.length() * second.length())) > 1 - sys.float_info.epsilon

# Used only once


def point_in_same_diraction(first, second):
    """
    The function does not assumes that the two vectors are parallel.
    If the dot product is >= 0 then the angle between the vectors is in the
    (270, 90) range, therefor if parallel they point in the same diraction.
    """
    return first * second >= 0


def get_closest_point(point, vertex_1, vertex_2):
    """
    Finds a point on a line segment which is the closest to another point.
    vertex_1, vertex_2 - endpoints of the line segment.
    Using a mathematically proven algorithm.
    """
    altitude_foot = calculate_altitude_foot(point, vertex_1, vertex_2)
    if point_in_same_diraction(altitude_foot - vertex_1,
                               altitude_foot - vertex_2):
        if (vertex_1 - point).length() > (vertex_2 - point).length():
            return vertex_2
        return vertex_1
    else:
        return altitude_foot


def calculate_altitude_foot(point, vertex_1, vertex_2):
    """
    Finds a point on a line which is foot of an altitude through
    another point to the line.
    vertex_1, vertex_2 - endpoints of the line segment.
    Using a mathematically proven algorithm.
    """
    if vertex_1.x == vertex_2.x:
        return Vector((vertex_1.x, point.y))
    if vertex_1.y == vertex_2.y:
        return Vector((point.x, vertex_1.y))
    m1 = (vertex_2.y - vertex_1.y) / (vertex_2.x - vertex_1.x)
    m2 = - 1 / m1
    x = (m1 * vertex_1.x - m2 * point.x + point.y - vertex_1.y) / (m1 - m2)
    y = m2 * (x - point.x) + point.y
    return Vector((x, y))


def calculate_centroid(vertices):
    return sum(vertices, Vector((0, 0))) / len(vertices)

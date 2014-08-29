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
    The function assumes that the two vectors are parallel.
    If the dot product is >= 0 then the angle between the vectors is in the
    (270, 90) range, therefor if parallel they point in the same diraction.
    """
    return first * second >= 0


def calculate_centroid(vertices):
    return sum(vertices, Vector((0, 0))) / len(vertices)


class Line:

    def __init__(self, vertex_1, vertex_2, is_segment=False):
        self.vertices = (vertex_1, vertex_2)
        self.is_segment = is_segment
        self.direction = (self.vertices[1] - self.vertices[0]).normalize()
        self.line_equation = self.calculate_line_equation()

    def calculate_line_equation(self):
        if self.vertices[0].x - self.vertices[1].x == 0:
            a = 0
        else:
            a = ((self.vertices[0].y - self.vertices[1].y) /
                (self.vertices[0].x - self.vertices[1].x))
        b = self.vertices[0].y - a * self.vertices[0].x
        return (a, b)

    def calculate_point_of_intersection(self, other):
        if self.check_if_parallel(other):
            return None
        a = self.line_equation
        b = other.line_equation
        x = (b[1] - a[1]) / (a[0] - b[0])
        y = (a[0] * b[1] - b[0] * a[1]) / (a[0] - b[0])
        point_of_intersection = Vector(x, y)
        if self.is_segment and point_in_same_diraction(
                point_of_intersection - self.vertices[0],
                point_of_intersection - self.vertices[1]):
            return None
        return Vector(x, y)

    def check_if_parallel(self, other):
        return self.line_equation[0] - other.line_equation[0] \
            <= sys.float_info.epsilon

    def get_closest_point(self, point):
        altitude_foot = self.calculate_altitude_foot(point)
        if self.is_segment and point_in_same_diraction(
                altitude_foot - self.vertices[0],
                altitude_foot - self.vertices[1]):
            if (self.vertices[0] - point).length() > (
                    self.vertices[1] - point).length():
                return self.vertices[1]
            return self.vertices[0]
        else:
            return altitude_foot

    def calculate_altitude_foot(self, point):
        if self.vertices[0].x == self.vertices[1].x:
            return Vector(self.vertices[0].x, point.y)
        if self.vertices[0].y == self.vertices[1].y:
            return Vector(point.x, self.vertices[0].y)
        m1 = ((self.vertices[1].y - self.vertices[0].y) /
              (self.vertices[1].x - self.vertices[0].x))
        m2 = - 1 / m1
        x = (m1 * self.vertices[0].x - m2 * point.x +
             point.y - self.vertices[0].y) / (m1 - m2)
        y = m2 * (x - point.x) + point.y
        return Vector((x, y))

    def get_normal(self):
        return Vector(self.direction.x, - self.direction.y).normalize()

    def check_if_intersects_line(self, line):
        return self.calculate_point_of_intersection(line) is not None

    def check_if_point_belongs(self, point):
        on_line = point.x * self.line_equation[0] + self.line_equation[1] - \
            point.y <= sys.float_info.epsilon
        if on_line and self.is_segment and point_in_same_diraction(
                point - self.vertices[0], point - self.vertices[1]):
            return False
        return on_line

    def reflect_point(self, point):
        altitude_foot = self.calculate_altitude_foot(point)
        reflection_vector = (altitude_foot - point) * 2
        return point + reflection_vector

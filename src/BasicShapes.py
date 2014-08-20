from itertools import combinations

import pygame

from pygame.math import Vector2 as Vector

from VectorMath import get_closest_point
from VectorMath import calculate_centroid


class RigitBody:

    """
    This class contains the basic functionality every basic shape needs.
    The class is hashable which is being achieved by counting its objects.
    """
    __counter = 0

    def __init__(self, position_m=Vector((0, 0)), mass_kg=0):
        """
        position is the position of the center of mass
        """
        self.__position_m = position_m
        self.__direction = Vector((1, 0))
        self.__mass_kg = mass_kg
        self.velocity_mps = Vector((0.0, 0.0))
        self.joints = []
        self.__hash_count = RigitBody.__counter
        RigitBody.__counter += 1

    @property
    def position_m(self):
        return self.__position_m

    @position_m.setter
    def position_m(self, value):
        self.__position_m = value
        self.sync_position()

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, value):
        self.__direction = value
        self.sync_position()

    @property
    def mass_kg(self):
        return self.__mass_kg

    def __hash__(self):
        return self.__hash_count

    def __str__(self):
        return self.__class__.__name__

    def fix_joints(self):
        for joint in self.joints:
            joint.apply_constraints(self)

    def rotate(self, angle):
        self.direction = self.direction.rotate(angle)

    def move(self, movement_m):
        self.position_m = self.position_m + movement_m

    def position_in_world(self, position_on_body):
        return position_on_body.rotate(round(Vector((1, 0)).angle_to(
            self.direction), 5)) + self.position_m

    def rotate_around(self, pivot, angle):
        pivot_position = self.position_in_world(pivot)
        self.rotate(angle)
        self.move(pivot_position - self.position_in_world(pivot))

    def pull_on_anchor(self, anchor, movement_m):
        new_anchor = anchor + movement_m
        magic = self.pivot_m.rotate(
            Vector((1, 0)).angle_to(self.direction)) + self.position_m
        rotation = round((anchor - magic).angle_to(new_anchor - magic), 5)
        self.rotate(rotation)
        anchor = (anchor - self.position_m).rotate(
            rotation) + self.position_m
        translation = new_anchor - anchor
        self.move(translation)
        self.fix_joints()

    def scale_avatar(self, width_m, height_m):
        self.imageMaster = pygame.transform.scale(self.imageMaster,
                                                  (int(width_m),
                                                   int(height_m)))

    def display_avatar(self, surface):
        self.image = pygame.transform.rotate(
            self.imageMaster, self.direction.angle_to(Vector((1, 0))))
        self.rect = self.image.get_rect()
        self.rect.center = self.position_m
        surface.blit(self.image, self.rect)

    def box_collide(self, other):
        first_box = self.calculate_box()
        second_box = other.calculate_box()
        return (first_box[0][0] <= second_box[0][1] and
                first_box[0][1] >= second_box[0][0]) and \
            (first_box[1][0] <= second_box[1][1] and
             first_box[1][1] >= second_box[1][0])

    def check_if_collide(self, other):
        if self.box_collide(other):
            return getattr(self, "collides_{0}".format(
                str(other).lower()))(other) or\
                getattr(other, "collides_{0}".format(str(self).lower()))(self)
        return False


class Circle(RigitBody):

    def __init__(self, radius_m, position_m=Vector((0, 0)), mass_kg=0):
        RigitBody.__init__(self, position_m, mass_kg)
        self.__radius_m = radius_m

    def __hash__(self):
        return RigitBody.__hash__(self)

    def __eq__(self, other):
        return self.position_m == other.position_m and \
            self.radius_m == other.radius_m and \
            self.mass_kg == other.mass_kg and \
            self.direction == other.direction and \
            self.pivot_m == other.pivot_m

    @property
    def radius_m(self):
        return self.__radius_m

    def is_point_in_body(self, point):
        if abs((point - self.position_m).length()) < self.radius_m:
            return True
        return False

    def sync_position(self):
        pass

    def calculate_box(self):
        return ((self.position_m.x - self.radius_m,
                 self.position_m.x + self.radius_m),
                (self.position_m.y - self.radius_m,
                 self.position_m.y + self.radius_m))

    def collides_triangle(self, other):
        return any(map(self.is_point_in_body, other.vertices.values()))

    def collides_rectangle(self, other):
        return any(map(self.is_point_in_body, other.vertices))

    def collides_circle(self, other):
        return (self.position_m - other.position_m).length() <=  \
            self.radius_m + other.radius_m

    def draw(self, surface, colour=(0, 0, 0)):
        pygame.draw.circle(surface, colour,
                           (int(self.position_m.x), int(self.position_m.y)),
                           int(self.radius_m))


class Triangle(RigitBody):

    def __init__(self, three_elements, position_m=Vector((0, 0)), mass_kg=0):
        RigitBody.__init__(self, position_m, mass_kg)
        if isinstance(three_elements[0],
                      Vector) or isinstance(three_elements[0], tuple):
            three_elements = [Vector(element) for element in three_elements]
            self.vertices = dict(zip(["A", "B", "C"], three_elements))
            self.calculate_edges()
        else:
            self.edge_lenghts = dict(zip(["AB", "AC", "BC"], three_elements))
            self.calculate_vertices()
        self.sync_centroid()
        self.sync_position()

    def __hash__(self):
        return RigitBody.__hash__(self)

    def __eq__(self, other):
        result = self.position_m == other.position_m
        result &= all([self.edge_lenghts[key] == other.edge_lenghts[key]
                       for key in self.edge_lenghts.keys()])
        result &= self.mass_kg == other.mass_kg
        result &= self.direction == other.direction
        result &= self.pivot_m == other.pivot_m
        return result

    def calculate_edges(self):
        self.edge_lenghts = {"".join(sorted(pair[0] + pair[1])): (
            self.vertices[pair[0]] - self.vertices[pair[1]]).length()
            for pair in combinations(self.vertices.keys(), 2)}

    def sync_position(self):
        self.vertices = {key: self.generic_vertices[key].rotate(round(
            Vector((1, 0)).angle_to(self.direction), 5)) + self.position_m
            for key in self.generic_vertices.keys()}

    def sync_centroid(self):
        current_centroid = calculate_centroid(self.vertices.values())
        self.generic_vertices = {key: self.vertices[key] - current_centroid
                                 for key in self.vertices}

    def calculate_vertices(self):
        self.vertices = {
            "A": Vector((0, 0)), "B": Vector((self.edge_lenghts["AB"], 0))}
        x_c = (self.edge_lenghts["AB"] ** 2 + self.edge_lenghts["AC"] ** 2 -
               self.edge_lenghts["BC"] ** 2) / (2 * self.edge_lenghts["AB"])
        y_c = (self.edge_lenghts["AB"] ** 2 - x_c ** 2) ** 0.5
        self.vertices["C"] = Vector((x_c, y_c))

    def is_point_in_body(self, point):
        """
        Method uses "Barycentric Coordinates Point in Triangle Test"
        """
        p2 = Vector(point) - self.vertices['A']
        p1 = self.vertices['B'] - self.vertices['A']
        p0 = self.vertices['C'] - self.vertices['A']
        u = (((p1 * p1) * (p2 * p0) - (p1 * p0) * (p2 * p1)) /
            ((p0 * p0) * (p1 * p1) - (p0 * p1) * (p1 * p0)))
        v = (((p0 * p0) * (p2 * p1) - (p0 * p1) * (p2 * p0)) /
            ((p0 * p0) * (p1 * p1) - (p0 * p1) * (p1 * p0)))
        return u >= 0 and v >= 0 and (u + v) <= 1

    def calculate_box(self):
        x_coordinates = [self.vertices[_].x for _ in self.vertices]
        y_coordinates = [self.vertices[_].y for _ in self.vertices]
        return ((min(x_coordinates), max(x_coordinates)),
                (min(y_coordinates), max(y_coordinates)))

    def collides_triangle(self, other):
        return any(map(self.is_point_in_body, other.vertices.values()))

    def collides_rectangle(self, other):
        return any(map(self.is_point_in_body, other.vertices))

    def collides_circle(self, other):
        distances = [(other.position_m - get_closest_point(
            other.position_m, *combination)).length()
            for combination in combinations(self.vertices.values(), 2)]
        return any([_ <= other.radius_m for _ in distances])

    def draw(self, surface, colour=(255, 0, 0)):
        self.sync_position()
        pygame.draw.polygon(surface, colour, list((_.x, _.y)
                            for _ in self.vertices.values()))


class Rectangle(RigitBody):

    def __init__(self, width_m, height_m,
                 position_m=Vector((0, 0)), mass_kg=0):
        RigitBody.__init__(self, position_m, mass_kg)
        self.__width_m = width_m
        self.__height_m = height_m
        self.sync_position()

    def __hash__(self):
        return RigitBody.__hash__(self)

    def __eq__(self, other):
        result = self.position_m == other.position_m
        result &= self.width_m == other.width_m
        result &= self.height_m == other.height_m
        result &= self.mass_kg == other.mass_kg
        result &= self.direction == other.direction
        result &= self.pivot_m == other.pivot_m
        return result

    @property
    def height_m(self):
        return self.__height_m

    @property
    def width_m(self):
        return self.__width_m

    def sync_position(self):
        perpendicular = self.direction.rotate(90)
        vertices = []
        vertices.append(perpendicular * self.height_m / 2 +
                        self.direction * self.width_m / -2 + self.position_m)
        vertices.append(perpendicular * self.height_m / 2 +
                        self.direction * self.width_m / 2 + self.position_m)
        vertices.append(perpendicular * self.height_m / -2 +
                        self.direction * self.width_m / 2 + self.position_m)
        vertices.append(perpendicular * self.height_m / -2 +
                        self.direction * self.width_m / -2 + self.position_m)
        self.vertices = vertices

    def is_point_in_body(self, point_location_m):
        centroid_to_point = point_location_m - self.position_m
        centroid_to_point = centroid_to_point.rotate(
            self.direction.angle_to(Vector((1, 0))))
        return abs(centroid_to_point.x) <= self.width_m / 2 and \
            abs(centroid_to_point.y) <= self.height_m / 2

    def calculate_box(self):
        x_coordinates = [_.x for _ in self.vertices]
        y_coordinates = [_.y for _ in self.vertices]
        return ((min(x_coordinates), max(x_coordinates)),
                (min(y_coordinates), max(y_coordinates)))

    def collides_triangle(self, other):
        return any(map(self.is_point_in_body, other.vertices.values()))

    def collides_rectangle(self, other):
        return any(map(self.is_point_in_body, other.calculate_vertices))

    def collides_circle(self, other):
        distances = [(other.position_m - get_closest_point(
            other.position_m, self.vertices[index],
            self.vertices[(index + 1) % 4])).length() for index in range(0, 4)]
        return any([_ <= other.radius_m for _ in distances])

    def draw(self, surface, colour=(255, 0, 0)):
        pygame.draw.polygon(surface, colour, self.vertices)


SHAPES = {"Triangle": Triangle, "Circle": Circle, "Rectangle": Rectangle}

from itertools import combinations
from math import pi

import pygame

from pygame.math import Vector2 as Vector

from VectorMath import calculate_centroid
from VectorMath import Line


class RigitBody:

    """
    This class contains the basic functionality every basic shape needs.
    The class is hashable which is being achieved by counting its objects.
    """
    __counter = 0

    def __init__(self, position_m=Vector(0, 0), density=0):
        """
        position is the position of the center of mass
        """
        self.__position_m = position_m
        self.__direction = Vector(1, 0)
        self.__density = density
        self.velocity = Vector(0.0, 0.0)
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
    def mass(self):
        return self.__mass

    def __hash__(self):
        return self.__hash_count

    def __str__(self):
        return self.__class__.__name__

    def calculate_mass(self):
        self.__mass = self.calculate_surface() * self.__density

    def fix_joints(self):
        for joint in self.joints:
            joint.apply_constraints(self)

    def reflect(self, line):
        new_joint_positions = {}
        for joint in self.joints:
            new_joint_positions[joint] = line.reflect_point(
                joint.calculate_world_position(self))
        self.__position_m = line.reflect_point(self.position_m)
        self.__direction = self.direction.reflect(line.direction)
        self.imageMaster = pygame.transform.flip(self.imageMaster, True, False)
        if isinstance(self, Triangle):
            centroid_to_line = line.get_closest_point(Vector(0, 0))
            self.generic_vertices = {key: line.reflect_point(
                self.generic_vertices[key] + centroid_to_line) -
                centroid_to_line for key in self.vertices}
        self.sync_position()
        for joint in self.joints:
            joint._bodies_positions[self] = self.position_on_body(
                new_joint_positions[joint])

    def rotate(self, angle):
        self.direction = self.direction.rotate(angle)

    def move(self, movement_m):
        self.position_m = self.position_m + movement_m

    def position_in_world(self, position_on_body):
        return position_on_body.rotate(round(Vector(1, 0).angle_to(
            self.direction), 5)) + self.position_m

    def position_on_body(self, position_in_world):
        return (position_in_world - self.position_m).rotate(
            round(self.direction.angle_to(Vector(1, 0)), 5))

    def rotate_around(self, pivot, angle):
        pivot_position = self.position_in_world(pivot)
        self.rotate(round(angle, 5))
        self.move(pivot_position - self.position_in_world(pivot))

    def pull_on_anchor(self, anchor, movement_m):
        new_anchor = anchor + movement_m
        magic = self.pivot_m.rotate(
            Vector(1, 0).angle_to(self.direction)) + self.position_m
        rotation = round((anchor - magic).angle_to(new_anchor - magic), 5)
        self.rotate(rotation)
        anchor = (anchor - self.position_m).rotate(
            rotation) + self.position_m
        translation = new_anchor - anchor
        self.move(translation)
        self.fix_joints()

    def load_avatar(self, path):
        try:
            self.imageMaster = pygame.image.load(r"../ArtWork/{0}".format(
                path)).convert_alpha()
        except pygame.error:
            self.imageMaster = None

    def scale_avatar(self, width_m, height_m):
        if self.imageMaster is None:
            return
        self.imageMaster = pygame.transform.scale(self.imageMaster,
                                                  (int(width_m),
                                                   int(height_m)))

    def display_avatar(self, surface, camera=0):
        centre = self.position_m
        if camera != 0:
            centre = camera.apply([centre])[0]
        if self.imageMaster is None:
            Rectangle.draw(self, surface)
            return
        image = pygame.transform.rotate(
            self.imageMaster, self.direction.angle_to(Vector(1, 0)))
        rect = image.get_rect()
        rect.center = centre
        surface.blit(image, rect)


        #  def box_collide(self, other):
        #      first_box = self.calculate_box()
        #      second_box = other.calculate_box()
        #      return (first_box[0][0] <= second_box[0][1] and
        #              first_box[0][1] >= second_box[0][0]) and \
        #          (first_box[1][0] <= second_box[1][1] and
        #           first_box[1][1] >= second_box[1][0])

        #  def check_if_collide(self, other):
        #      if self.box_collide(other):
        #          return getattr(self, "collides_{0}".format(
        #              str(other).lower()))(other) or\
        #              getattr(other, "collides_{0}".format(str(self).lower()))(self)
        #      return False

    def check_if_collide(self, other):
        if isinstance(self, Circle) and isinstance(other, Circle):
            return self.collide_circle(other)
        collide = True
        axis = self.get_SAT_axis()
        axis.extend(other.get_SAT_axis())
        magnitudes = {}
        for axes in axis:
            self_projections = self.get_SAT_projections(axes)
            other_projections = other.get_SAT_projections(axes)
            if self_projections[1] <= other_projections[0] or \
               self_projections[0] >= other_projections[1]:
                collide = False
            magnitudes[min([
                self_projections[1] - other_projections[0],
                other_projections[1] - self_projections[0]])] = axes
        minimal_magnitude = min(magnitudes)
        direction = 1
        if magnitudes[minimal_magnitude].direction * (
                other.position_m - self.position_m) < 0:
            direction = -1
        return (collide, magnitudes[minimal_magnitude].direction *
                minimal_magnitude * direction)


class Circle(RigitBody):

    def __init__(self, radius_m, position_m=Vector(0, 0), density=0):
        RigitBody.__init__(self, position_m, density)
        self.__radius_m = radius_m
        self.calculate_mass()

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

    def calculate_surface(self):
        return pi * pow(self.radius_m, 2)

  #  def calculate_box(self):
  #      return ((self.position_m.x - self.radius_m,
  #               self.position_m.x + self.radius_m),
  #              (self.position_m.y - self.radius_m,
  #               self.position_m.y + self.radius_m))

  #  def collides_triangle(self, other):
  #      return any(map(self.is_point_in_body, other.vertices.values()))

  #  def collides_rectangle(self, other):
  #      return any(map(self.is_point_in_body, other.vertices))

    def collide_circle(self, other):
        collide = True
        centre_difference = other.position_m - self.position_m
        separation = centre_difference.length()
        if separation >= self.radius_m + other.radius_m:
            collide = False
        return (collide, centre_difference.normalize() * (
            self.radius_m + other.radius_m - separation))

    def draw(self, surface, colour=(0, 0, 0)):
        pygame.draw.circle(surface, colour,
                           (int(self.position_m.x), int(self.position_m.y)),
                           int(self.radius_m))

    def get_SAT_axis(self):
        return []

    def get_SAT_projections(self, axes):
        centre_projection = axes.direction * self.position_m
        return (centre_projection - self.radius_m,
                centre_projection + self.radius_m)


class Triangle(RigitBody):

    def __init__(self, three_elements, position_m=Vector(0, 0), density=0):
        RigitBody.__init__(self, position_m, density)
        if isinstance(three_elements[0], Vector):
            three_elements = [element for element in three_elements]
            self.vertices = dict(zip(["A", "B", "C"], three_elements))
            self.calculate_edges()
        else:
            self.edge_lenghts = dict(zip(["AB", "AC", "BC"], three_elements))
            self.calculate_vertices()
        self.sync_centroid()
        self.sync_position()
        self.calculate_mass()

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

    def calculate_surface(self):
        return ((self.vertices["A"].x - self.vertices["C"].x) *
               (self.vertices["B"].y - self.vertices["A"].y) -
               (self.vertices["A"].x - self.vertices["B"].x) *
               (self.vertices["C"].y - self.vertices["A"].y)) / 2

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
        y_c = (self.edge_lenghts["AC"] ** 2 - x_c ** 2) ** 0.5
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

  #  def calculate_box(self):
  #      x_coordinates = [self.vertices[_].x for _ in self.vertices]
  #      y_coordinates = [self.vertices[_].y for _ in self.vertices]
  #      return ((min(x_coordinates), max(x_coordinates)),
  #              (min(y_coordinates), max(y_coordinates)))

  #  def collides_triangle(self, other):
  #      return any(map(self.is_point_in_body, other.vertices.values()))

  #  def collides_rectangle(self, other):
  #      return any(map(self.is_point_in_body, other.vertices))

  #  def collides_circle(self, other):
  #      distances = [(other.position_m - Line(
  #          combination[0], combination[1], True).get_closest_point(
  #          other.position_m)).length() for combination in combinations(
  #          self.vertices.values(), 2)]
  #      return any([_ <= other.radius_m for _ in distances]) or\
  #          self.is_point_in_body(other.position_m)

    def draw(self, surface, colour=(255, 0, 0)):
        self.sync_position()
        pygame.draw.polygon(surface, colour, list((_.x, _.y)
                            for _ in self.vertices.values()))

    def get_SAT_axis(self):
        return [Line(combination[0], (combination[1] - combination[0]).rotate(
            90) + combination[0])
            for combination in combinations(self.vertices.values(), 2)]

    def get_SAT_projections(self, axes):
        projections = [vertex * axes.direction
                       for vertex in self.vertices.values()]
        return (min(projections), max(projections))


class Rectangle(RigitBody):

    def __init__(self, width_m, height_m,
                 position_m=Vector(0, 0), density=0):
        RigitBody.__init__(self, position_m, density)
        self.__width_m = width_m
        self.__height_m = height_m
        #self.sync_position()
        #topleft position
        self.sync_position()
        self.x = self.vertices[3].x
        self.y = self.vertices[3].y
        self.calculate_mass()

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

    @property
    def center(self):
        return self.position_m

    @center.setter
    def center(self, value):

        self.position_m = value
        self.sync_position()
        self.x = self.vertices[3].x
        self.y = self.vertices[3].y

    def advance(self, amount_x, amount_y):
        self.position_m = (self.center[0] + amount_x, self.center[1] + amount_y)
        self.sync_position()
        self.x = self.vertices[3].x
        self.y = self.vertices[3].y

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

    def is_point_in_body(self, point_location_m, camera=0):
        if camera != 0:
            centroid_to_point = point_location_m - camera.apply(Vector(self.position_m))
        else:
            centroid_to_point = point_location_m - Vector(self.position_m)
        centroid_to_point = centroid_to_point.rotate(
            self.direction.angle_to(Vector((1, 0))))
        return abs(centroid_to_point.x) <= self.width_m / 2 and \
            abs(centroid_to_point.y) <= self.height_m / 2

    def calculate_surface(self):
        return self.width_m * self.height_m

  #  def calculate_box(self):
  #      x_coordinates = [_.x for _ in self.vertices]
  #      y_coordinates = [_.y for _ in self.vertices]
  #      return ((min(x_coordinates), max(x_coordinates)),
  #              (min(y_coordinates), max(y_coordinates)))

  #  def collides_triangle(self, other):
  #      return any(map(self.is_point_in_body, other.vertices.values()))

    def collides_rectangle(self, other):
        return any(map(self.is_point_in_body, other.vertices))

  #  def collides_circle(self, other):
  #      distances = [(other.position_m - Line(self.vertices[
  #          index], self.vertices[(index + 1) % 4], True).get_closest_point(
  #          other.position_m)).length() for index in range(0, 4)]
  #      return any([_ <= other.radius_m for _ in distances]) or\
  #          self.is_point_in_body(other.position_m)

    def draw(self, surface, colour=(255, 0, 0), camera=0):
        if camera != 0:
            pygame.draw.polygon(surface, colour, camera.apply(self.vertices))
        else:
            pygame.draw.polygon(surface, colour, self.vertices)

    def get_SAT_axis(self):
        return [Line(self.vertices[0], self.vertices[1]),
                Line(self.vertices[1], self.vertices[2])]

    def get_SAT_projections(self, axes):
        projections = [vertex * axes.direction for vertex in self.vertices]
        return (min(projections), max(projections))

    def intersect(self, other):
        '''
        use only when direction is parallel to Ox
        '''
        if not self.collides_rectangle(other):
            return Rectangle(0, 0, (0, 0))

        other_vertices = other.vertices
        this_vertices = self.vertices
        clipped_vertices = [0 for i in range(4)]
        for i in range(4):
            if self.is_point_in_body(other_vertices[i]):
                clipped_vertices[i] = other_vertices[i]
                if i >= 2:
                    clipped_vertices[i - 2] = this_vertices[i - 2]
                else:
                    clipped_vertices[i + 2] = this_vertices[i + 2]

        matrix = []
        for i in range(4):
            if isinstance(clipped_vertices[i], Vector):
                matrix.append(1)
        if not any(matrix):
            return Rectangle(0, 0, (0, 0))

        if isinstance(clipped_vertices[3], Vector):
            clipped_vertices[0] = Vector(clipped_vertices[3].x, clipped_vertices[1].y)
            clipped_vertices[2] = Vector(clipped_vertices[1].y, clipped_vertices[3].y)
        elif isinstance(clipped_vertices[2], Vector):
            clipped_vertices[3] = Vector(clipped_vertices[0].x, clipped_vertices[2].y)
            clipped_vertices[1] = Vector(clipped_vertices[2].x, clipped_vertices[0].y)

        clipped_height = clipped_vertices[0].distance_to(clipped_vertices[3])
        clipped_width = clipped_vertices[0].distance_to(clipped_vertices[1])
        clipped_center = (clipped_vertices[0].x + clipped_width / 2, clipped_vertices[0].y - clipped_height / 2)

        return Rectangle(clipped_width, clipped_height, clipped_center)

    @staticmethod
    def get_rect(image, old_center):
        height = image.get_height()
        width = image.get_width()

        return Rectangle(width, height, Vector(old_center))

SHAPES = {"Triangle": Triangle, "Circle": Circle, "Rectangle": Rectangle}

import pygame

from pygame.math import Vector2 as Vector
from itertools import combinations


def m_to_px(value_m):
    return value_m * 1


def px_to_m(value_px):
    return value_px * 1


class Circle:

    def __init__(self, radius_m, position_m=Vector((0, 0))):
        """
        position_m is the position of the center of mass
        """
        self.radius_m = radius_m
        self.position_m = Vector(position_m)
        self.joints = []

        self.direction = Vector((1, 0))

    def rotate(self, rotation):
        self.direction = self.direction.rotate(rotation)
        self.joints = [(joint, position_on_body.rotate(rotation))
                       for joint, position_on_body in self.joints]
        for joint, _ in self.joints:
            joint.update(self)

    def move(self, movement_m):
        self.position_m = self.position_m + movement_m
        for joint, _ in self.joints:
            joint.update(self)

    def move_to_joint(self, current_joint):  # unresolved problem
        joint_position_on_body = sum([vec for _, vec in self.joints
                                      if _ is current_joint], Vector((0, 0)))
        new_position = current_joint.position_m - joint_position_on_body
        translation = new_position - self.position_m
        rotation = (joint_position_on_body).angle_to(
            translation + joint_position_on_body)
        if translation.x > 0.27 or translation.x < -0.27 or \
           translation.y > 0.27 or translation.y < -0.27 or \
           rotation < -0.07 or rotation > 0.07:
            self.direction = self.direction.rotate(rotation)
            self.joints = [(joint, position_on_body.rotate(rotation))
                           for joint, position_on_body in self.joints]
            joint_position_on_body = joint_position_on_body.rotate(rotation)
            new_position = current_joint.position_m - joint_position_on_body
            translation = new_position - self.position_m
            self.position_m = self.position_m + translation
            for joint, _ in self.joints:
                joint.update(self)

    def add_joint(self, new_joint):
        position_on_body = (new_joint.position_m - self.position_m) +\
            (Vector((1, 0)) - self.direction)
        self.joints.append((new_joint, position_on_body))

    def draw(self, surface):
        pygame.draw.circle(surface, (0, 0, 0), self.position_m, self.radius_m)


class Triangle:

    def __init__(self, edges, position_m=Vector((0, 0))):
        self.direction = (Vector((1, 0)), Vector((0, 1)))
        self.position_m = position_m
        self.edge_lenghts = dict(zip(["AB", "AC", "BC"], edges))
        self.calculate_vertices()

        self.joints = []

  #  def __init__(self, vertices, lol, position_m=Vector((0, 0))):
  #      self.direction = (Vector((1, 0)), Vector((0, 1)))
  #      self.position_m = position_m
  #      self.vertices = dict(zip(["A", "B", "C"], vertices))
  #      self.calculate_edges()

    def calculate_edges(self):
        self.edge_lenghts = {sorted(pair[0] + pair[1]): (
            self.vertices[pair[0]] - self.vertices[pair[1]]).length()
            for pair in combinations(self.vertices.keys(), 2)}

    def sinc_vertices_with_median(self):
        current_centroid = sum(self.vertices.values(), Vector((0, 0))) / 3
        translation_vector = self.position_m - current_centroid
        self.vertices = {key: self.vertices[key] +
                         translation_vector for key in self.vertices.keys()}

    def calculate_vertices(self):
        self.vertices = {
            "A": Vector((0, 0)), "B": Vector((self.edge_lenghts["AB"], 0))}
        x_c = (self.edge_lenghts["AB"] ** 2 + self.edge_lenghts["AC"] ** 2 -
               self.edge_lenghts["BC"] ** 2) / (2 * self.edge_lenghts["AB"])
        y_c = (self.edge_lenghts["AB"] ** 2 - x_c ** 2) ** 0.5
        self.vertices["C"] = Vector((x_c, y_c))
        self.sinc_vertices_with_median()

    def rotate(self, rotation):
        for key in self.vertices:
            self.vertices[key] = (self.vertices[key] - self.position_m).rotate(
                rotation) + self.position_m

    def move(self, movement_m):
        self.position_m = self.position_m + movement_m
        self.vertices = {key: self.vertices[key] + movement_m
                         for key in self.vertices.keys()}

    def draw(self, surface):
        pygame.draw.polygon(surface, (0, 0, 0), list((_.x, _.y)
                            for _ in self.vertices.values()))
   # def collide_triangle(self, triangle):
   #     if


class Rectangle(pygame.sprite.Sprite):

    def __init__(self, width_m, height_m, position_m):
        """
        position_m is the position of the center of mass
        """
        pygame.sprite.Sprite.__init__(self)
        self.width_m = width_m
        self.height_m = height_m
        self.position_m = Vector(position_m)
        self.joints = []

        self.direction = Vector((1, 0))

    def calculate_vertices(self):
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

        return vertices

    def rotate(self, rotation):
        self.direction = self.direction.rotate(rotation)
        self.joints = [(joint, position_on_body.rotate(rotation))
                       for joint, position_on_body in self.joints]
        for joint, _ in self.joints:
            joint.update(self)

    def move(self, movement_m):
        self.position_m = self.position_m + movement_m
        for joint, _ in self.joints:
            joint.update(self)

    def pull_on_anchor(self, anchor, movement_m):
        new_anchor_position = anchor + movement_m
        rotation = (anchor).angle_to(
            movement_m + anchor)
        # work around a pygame bug
        rotation = int(rotation * 100000) / 100000
        self.direction = self.direction.rotate(rotation)
        self.joints = [(joint, position_on_body.rotate(rotation))
                       for joint, position_on_body in self.joints]
        anchor = anchor.rotate(rotation)
        translation = new_anchor_position - anchor
        self.position_m = self.position_m + translation
        for joint, _ in self.joints:
            joint.update(self)

    def move_to_joint(self, current_joint):  # might need to fix recursion
        joint_position_on_body = sum([vec for _, vec in self.joints
                                      if _ is current_joint], Vector((0, 0)))
        new_position = current_joint.position_m - joint_position_on_body
        movement = new_position - self.position_m
        if abs(movement.x) > 0.27 or abs(movement.y) > 0.27:
            # The is statement stops the recursion
            self.move(movement)

    def add_joint(self, new_joint):
        position_on_body = (new_joint.position_m - self.position_m) +\
            (Vector((1, 0)) - self.direction)
        self.joints.append((new_joint, position_on_body))

    def is_under_cursor(self, cursor_location_px):
        cursor_location_m = Vector((
            px_to_m(cursor_location_px.x), px_to_m(cursor_location_px.y)))
        centroid_to_cursor = cursor_location_m - self.position_m
        centroid_to_cursor = centroid_to_cursor.rotate(
            self.direction.angle_to(Vector((1, 0))))
        return abs(centroid_to_cursor.x) <= self.width_m / 2 and \
            abs(centroid_to_cursor.y) <= self.height_m / 2
            
    def scale_avatar(self):
        self.imageMaster = pygame.transform.scale(self.imageMaster, 
                                                                        (int(self.width_m), int(self.height_m)))
        
    def display_avatar(self, surface):
        self.image = pygame.transform.rotate(self.imageMaster, 
                                                                Vector((1, 0)).angle_to(self.direction))
        self.rect = self.image.get_rect()
        self.rect.center = self.position_m
        surface.blit(self.image, self.rect)
            
    def draw(self, surface):
        pygame.draw.polygon(surface, (0, 0, 0), self.calculate_vertices())

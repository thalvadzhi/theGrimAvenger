import math
import sys
import pygame

from VectorMath import seperate_point

from pygame.math import Vector2 as Vector

from collections import OrderedDict
from _collections import defaultdict
from itertools import combinations


pygame.init()

screen = pygame.display.set_mode((500, 500))

clock = pygame.time.Clock()


class Triangle:

    def __init__(self, edges, position_m=Vector((0, 0))):
        self.diraction = (Vector((1, 0)), Vector((0, 1)))
        self.position_m = position_m
        self.edge_lenghts = dict(zip(["AB", "AC", "BC"], edges))
        self.calculate_vertices()

  #  def __init__(self, vertices, lol, position_m=Vector((0, 0))):
  #      self.diraction = (Vector((1, 0)), Vector((0, 1)))
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

    def draw(self):
        pygame.draw.polygon(screen, (0, 0, 0), list((_.x, _.y)
                            for _ in self.vertices.values()))
   # def collide_triangle(self, triangle):
   #     if

triangle = Triangle([50, 50, 50], (25, 250))

while True:
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        triangle.move(Vector((1, 0)))

        screen.fill((55, 155, 255))
        triangle.draw()

    elif keys[pygame.K_RIGHT]:
        triangle.move(Vector((-1, 0)))

        screen.fill((55, 155, 255))
        triangle.draw()

    elif keys[pygame.K_UP]:
        triangle.rotate(1)

        screen.fill((55, 155, 255))
        triangle.draw()

    elif keys[pygame.K_DOWN]:
        triangle.rotate(-1)

        screen.fill((55, 155, 255))
        triangle.draw()

    else:
        screen.fill((55, 155, 255))
        triangle.draw()

    # pygame.draw.polygon(screen, (255, 255, 255),
    #                    [(0, 0), (0, 50), (50, 50), (50, 0)])
    pygame.display.update()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

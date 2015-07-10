import pygame
import math
from Environment import Block
from light_cast_v3 import LightSource, Point
from gradients import radial
from pygame import gfxdraw
from Constants import BLOCK_SIZE
import pygame
class Light:

    SHADOW_SURFACE = 0
    LIGHT_SURFACE = 0
    WIDTH = 0
    HEIGHT = 0

    @classmethod
    def set_up_surfaces(cls, width, height):
        Light.SHADOW_SURFACE = pygame.Surface((width, height), pygame.HWSURFACE).convert_alpha()
        Light.LIGHT_SURFACE = pygame.Surface((width, height), pygame.HWSURFACE).convert_alpha()
        Light.WIDTH = width
        Light.HEIGHT = height

    def __init__(self, x, y, radius, obstacles=[]):
        #expect that obstacles are blocks
        self.x = x
        self.y = y
        self.radius = radius
        self.obstacles = obstacles

        self.shadow_surface = pygame.Surface((1500, 1500)).convert_alpha()
        self.light_surface = pygame.Surface((1500, 1500)).convert_alpha()


        self.light_image = pygame.Surface((Light.WIDTH, Light.HEIGHT), pygame.HWSURFACE).convert_alpha()
        self.light_surface = pygame.Surface((Light.WIDTH, Light.HEIGHT), pygame.HWSURFACE).convert_alpha()
        self.light_texture = radial(radius, (255, 255, 255, 255), (0, 0, 0, 100))

        self.lightSource = LightSource(self.x, self.y, self.generate_points_from_rects())
        self.visibility = self.lightSource.cast()

    def update_local_surfaces(self):
        self.light_image = pygame.Surface((Light.WIDTH, Light.HEIGHT), pygame.HWSURFACE).convert_alpha()
        self.light_surface = pygame.Surface((Light.WIDTH, Light.HEIGHT), pygame.HWSURFACE).convert_alpha()

    @classmethod
    def update_surfaces(cls, width, height):
        Light.SHADOW_SURFACE = pygame.Surface((width, height), pygame.HWSURFACE).convert_alpha()
        Light.LIGHT_SURFACE = pygame.Surface((width, height), pygame.HWSURFACE).convert_alpha()
        Light.WIDTH = width
        Light.HEIGHT = height

    def generate_points_from_rects(self):
        all_points = []
        for obstacle in self.obstacles:
            current_points = []
            if isinstance(obstacle, Block):
                for vertex in obstacle.rect.vertices:
                    current_points.append(Point(vertex.x, vertex.y))
                all_points.append(current_points)
        #also add dimensions of screen
        all_points.append([Point(BLOCK_SIZE, BLOCK_SIZE), Point(self.WIDTH - BLOCK_SIZE, BLOCK_SIZE),
                           Point(self.WIDTH - BLOCK_SIZE, self.HEIGHT - BLOCK_SIZE), Point(BLOCK_SIZE, self.HEIGHT - BLOCK_SIZE)])
        return all_points

    def update(self):
        self.visibility = self.lightSource.cast()

    def update_light_position(self, x, y):
        self.x = x
        self.y = y
        self.lightSource.update_light_source_position(self.x, self.y)
        self.update()

    def update_obstacles(self, obstacles):
        self.obstacles = obstacles
        self.lightSource.update_obstacles(self.generate_points_from_rects())
        self.update()

    # def draw(self, surface, camera):
    #     #light surface is the visibility polygon
    #     #bg image is the gradient
    #     self.light_image.fill((255, 255, 255, 255))
    #     pygame.draw.polygon(self.light_image, (0, 0, 0, 0), camera.apply(self.visibility))
    #     self.light_surface.fill((0, 0, 0, 255))
    #     self.light_surface.blit(self.light_image, (0, 0), None, pygame.BLEND_RGBA_MIN)
    #
    #     self.bg_surface.fill((0, 0, 0))
    #     self.bg_surface.blit(self.light_texture, (self.x - 400, self.y - 400), None, pygame.BLEND_RGB_MAX)
    #
    #     #surface.blit(self.bg_surface, (0, 0))
    #     surface.blit(self.light_surface, (0, 0))
    #     gfxdraw.aapolygon(surface, camera.apply(self.visibility), (0, 0, 0))

    @classmethod
    def nullify_light(cls):
        Light.LIGHT_SURFACE.fill((0, 0, 0, 150))

    @classmethod
    def nullify_shadow(cls):
        Light.SHADOW_SURFACE.fill((0, 0, 0, 100))

    def draw_shadow(self, camera):
        self.light_image.fill((255, 255, 255, 255))
        pygame.draw.polygon(self.light_image, (0, 0, 0, 0), camera.apply(self.visibility))
        Light.SHADOW_SURFACE.blit(self.light_image, (0, 0), None, pygame.BLEND_RGBA_MIN)

    def draw_light(self, camera):
        Light.LIGHT_SURFACE.blit(self.light_texture, camera.apply((self.x - self.radius, self.y - self.radius)), None, pygame.BLEND_RGB_MAX)

    @classmethod
    def draw_everything(cls, surface):
        surface.blit(Light.LIGHT_SURFACE, (0, 0))
        surface.blit(Light.SHADOW_SURFACE, (0, 0))

    def draw_be(self, camera, surface):
        self.light_surface.fill((0, 0, 0, 150))
        self.shadow_surface.fill((0, 0, 0, 100))

        self.light_image.fill((255, 255, 255, 255))
        pygame.draw.polygon(self.light_image, (0, 0, 0, 0), camera.apply(self.visibility))
        self.shadow_surface.blit(self.light_image, (0, 0), None, pygame.BLEND_RGBA_MIN)

        self.light_surface.blit(self.light_texture, camera.apply((self.x - self.radius, self.y - self.radius)), None, pygame.BLEND_RGB_MAX)

        surface.blit(self.light_surface, (0, 0))
        surface.blit(self.shadow_surface, (0, 0))

    def collide(self, position):
       #for moving purposes
       return math.sqrt((self.x - position[0]) ** 2 + (self.y - position[1]) ** 2) <= 30
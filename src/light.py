import math
from pygame import draw, Surface, HWSURFACE, BLEND_RGBA_MIN, BLEND_RGB_MAX
from environment import Block
from lightcaster import LightSource, Point
from gradients import radial
from constants import BLOCK_SIZE


class Light:

    SHADOW_SURFACE = 0
    LIGHT_SURFACE = 0
    WIDTH = 0
    HEIGHT = 0

    @classmethod
    def set_up_surfaces(cls, width, height):
        Light.SHADOW_SURFACE = Surface((width, height),
                                       HWSURFACE).convert_alpha()
        Light.LIGHT_SURFACE = Surface((width, height),
                                      HWSURFACE).convert_alpha()
        Light.WIDTH = width
        Light.HEIGHT = height

    def __init__(self, x, y, radius, obstacles=[]):
        # expect that obstacles are blocks
        self.x = x
        self.y = y
        self.radius = radius
        self.obstacles = obstacles

        self.shadow_surface = Surface((1500, 1500)).convert_alpha()
        self.light_surface = Surface((1500, 1500)).convert_alpha()

        self.light_image = Surface((Light.WIDTH, Light.HEIGHT),
                                   HWSURFACE).convert_alpha()
        self.light_surface = Surface((Light.WIDTH, Light.HEIGHT),
                                     HWSURFACE).convert_alpha()
        self.light_texture = radial(radius, (255, 255, 255, 255),
                                    (0, 0, 0, 100))

        self.lightSource = LightSource(self.x, self.y,
                                       self.generate_points_from_rects())
        self.visibility = self.lightSource.cast()

    def update_local_surfaces(self):
        self.light_image = Surface((Light.WIDTH, Light.HEIGHT),
                                   HWSURFACE).convert_alpha()
        self.light_surface = Surface((Light.WIDTH, Light.HEIGHT),
                                     HWSURFACE).convert_alpha()

    @classmethod
    def update_surfaces(cls, width, height):
        Light.SHADOW_SURFACE = Surface((width, height),
                                       HWSURFACE).convert_alpha()
        Light.LIGHT_SURFACE = Surface((width, height),
                                      HWSURFACE).convert_alpha()
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
        # also add dimensions of screen
        all_points.append([Point(BLOCK_SIZE, BLOCK_SIZE),
                           Point(self.WIDTH - BLOCK_SIZE, BLOCK_SIZE),
                           Point(self.WIDTH - BLOCK_SIZE,
                                 self.HEIGHT - BLOCK_SIZE),
                           Point(BLOCK_SIZE, self.HEIGHT - BLOCK_SIZE)])
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

    @classmethod
    def nullify_light(cls):
        Light.LIGHT_SURFACE.fill((0, 0, 0, 150))

    @classmethod
    def nullify_shadow(cls):
        Light.SHADOW_SURFACE.fill((0, 0, 0, 100))

    def draw_shadow(self, camera):
        self.light_image.fill((255, 255, 255, 255))
        draw.polygon(self.light_image, (0, 0, 0, 0),
                     camera.apply(self.visibility))
        Light.SHADOW_SURFACE.blit(self.light_image, (0, 0),
                                  None, BLEND_RGBA_MIN)

    def draw_light(self, camera):
        Light.LIGHT_SURFACE.blit(self.light_texture,
                                 camera.apply((self.x - self.radius,
                                               self.y - self.radius)),
                                 None, BLEND_RGB_MAX)

    @classmethod
    def draw_everything(cls, surface):
        surface.blit(Light.LIGHT_SURFACE, (0, 0))
        surface.blit(Light.SHADOW_SURFACE, (0, 0))

    def collide(self, position):
        # for moving purposes
        return math.sqrt((self.x - position[0]) ** 2 +
                         (self.y - position[1]) ** 2) <= 30

    def is_illuminated(self, points):
        """ returns true if every point is in the light """
        shadow_coordinates = self.visibility
        length = len(shadow_coordinates)
        all_points = []
        for coordinate in points:
            inside = False
            # for coordinates in player:
            point_1_x, point_1_y = shadow_coordinates[0]
            for i in range(length + 1):
                point_2_x, point_2_y = shadow_coordinates[i % length]
                if coordinate[1] > min(point_1_y, point_2_y):
                    if coordinate[1] <= max(point_1_y, point_2_y):
                        if coordinate[0] <= max(point_1_x, point_2_x):
                            if point_1_y != point_2_y:
                                x_intersection = \
                                    (coordinate[1] - point_1_y) * \
                                    (point_2_x - point_1_x) / \
                                    (point_2_y - point_1_y) + \
                                    point_1_x
                            if point_1_x == point_2_x or \
                                    coordinate[0] <= x_intersection:
                                inside = not inside
                point_1_x, point_1_y = point_2_x, point_2_y
            all_points.append(inside)
        return all(all_points)

import pygame
from light_cast_v3 import LightSource, Point
from gradients import radial
from pygame import gfxdraw
class Light:
    def __init__(self, x, y, obstacles, screen_x, screen_y):
        self.x = x
        self.y = y
        self.obstacles = obstacles
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.light_image = pygame.Surface((self.screen_x, self.screen_y), pygame.HWSURFACE).convert_alpha()
        self.light_surface = pygame.Surface((self.screen_x, self.screen_y), pygame.HWSURFACE).convert_alpha()
        self.light_texture = radial(400, (255, 255, 255, 255), (0, 0, 0, 255))
        self.bg_surface = pygame.Surface((800, 600), pygame.HWSURFACE)
        self.lightSource = LightSource(self.x, self.y, self.generate_points_from_rects())
        self.visibility = self.lightSource.cast()

    def generate_points_from_rects(self):
        all_points = []
        for obstacle in self.obstacles:
            current_points = []
            for vertex in obstacle.vertices:
                current_points.append(Point(vertex.x, vertex.y))
            all_points.append(current_points)
        #also add dimensions of screen
        all_points.append([Point(0, 0), Point(self.screen_x, 0),
                           Point(self.screen_x, self.screen_y), Point(0, self.screen_y)])
        return all_points

    def update(self):
        self.visibility = self.lightSource.cast()

    def update_light_position(self, x, y):
        self.x = x
        self.y = y
        self.lightSource.update_light_source_position(self.x, self.y)

    def update_obstacles(self, obstacles):
        self.obstacles = obstacles
        self.lightSource.update_obstacles(self.generate_points_from_rects())

    def draw(self, surface, camera):
        self.light_image.fill((255, 255, 255, 255))
        pygame.draw.polygon(self.light_image, (0, 0, 0, 0), camera.apply(self.visibility))
        self.light_surface.fill((0, 0, 0, 255))
        self.light_surface.blit(self.light_image, (0, 0), None, pygame.BLEND_RGBA_MIN)
        surface.blit(self.light_surface, (0, 0))



        self.bg_surface.fill((0, 0, 0))
        self.bg_surface.blit(self.light_texture, (self.x - 400, self.y - 400), None, pygame.BLEND_RGB_MAX)

        surface.blit(self.bg_surface, (0, 0))
        surface.blit(self.light_surface, (0, 0))
        gfxdraw.aapolygon(surface, camera.apply(self.visibility), (0, 0, 0))

#        pygame.draw.aalines(surface, (0, 0, 0), True, camera.apply(self.visibility))
        # ####EXPERIMENTAL
        # #get mask
        # mask = pygame.Surface((800, 600), depth=8)
        # pygame.draw.polygon(mask, 255, self.visibility, 0)
        # #get texture
        # texture = radial(300, (50, 50, 50, 0), (50, 50, 50, 150))
        # texture = self.tile_texture(texture, (800, 600))
        # self.stamp(surface, texture, mask)


    #experimental
    def apply_alpha(self, texture, mask):
        texture = texture.convert_alpha()
        target = pygame.surfarray.pixels_alpha(texture)
        target[:] = pygame.surfarray.array2d(mask)
        # surfarray objets usually lock the Surface.
        # it is a good idea to dispose of them explicitly
        # as soon as the work is done.
        del target
        return texture

    def stamp(self, image, texture, mask):
        image.blit(self.apply_alpha(texture, mask), (0,0))

    def tile_texture(self, texture, size):
        result = pygame.Surface(size, depth=32)
        for x in range(0, size[0], texture.get_width()):
            for y in range(0, size[1], texture.get_height()):
                result.blit(texture, (x, y))
        return result
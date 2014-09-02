import pygame, sys
from pygame import *
from Vec2D import Vec2d as Vector
import pygame.gfxdraw
import math
from Camera import Camera
from Pendulum import Pendulum
from BasicShapes import Rectangle
from pixelperfect import get_hitmask
from Batarangs import Batarang
from pixelperfect import get_hitmask

class Block():
    #just the basic class for any obstacle
    def __init__(self, colour, width, height, x, y):
        self.image = pygame.Surface((width, height))
        self.image.fill(colour)
        self.rect = Rectangle(width, height, Vector(x + width / 2, y + height / 2))
        self.mask = get_hitmask(self, 0)
        self.colour = colour

    def draw(self, screen, camera=0):
        self.rect.draw(screen, self.colour, camera)


class SawBlock():
    def __init__(self, x, y, length):
        ''' x and y should be the coordinates from the point at which the rope would be hanging '''
        self.rope_width = 10
        self.rope_height = length
        self.saw_image_master = pygame.image.load("saw.png").convert_alpha()
        self.saw_image_master = pygame.transform.scale(self.saw_image_master, (50, 50))
        self.image = self.saw_image_master

        self.rect_center = (x, y + self.rope_height + 15)
        self.rect = Rectangle.get_rect(self.image, self.rect_center)
        self.mask = get_hitmask(self, 0)
        #self.rect = self.rect
        #self.collide_rect = Rectangle(self.rect.width, self.rect.height, self.rect.center)
        self.x = x
        self.y = y

        self.step = 40
        self.swing_step = 1
        self.rotation = 0
        self.is_severed = False
        self.angle = 45
        self.bob = Pendulum(self.angle, self.rope_height, (self.x, self.y))
        self.time = 0
        self.tick_time = 0
        self.entrances = 0
        self.last_time = 0
        self.current_time = 0

    def rotate_saw(self, time):
        self.image = pygame.transform.rotate(self.saw_image_master, self.rotation)
        self.rect = Rectangle.get_rect(self.image, self.rect_center)
        self.rotation += 300 * time / 1000
        self.mask = get_hitmask(self, 0)
        if self.rotation > 360:
            self.rotation = self.step


    def swing_rope(self):
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.last_time >= 17:
            self.bob.recompute_angle()
            self.rect_center = self.bob.rect.center
            self.rect.center = self.rect_center

            self.last_time = self.current_time


    def deploy(self):
        self.is_severed = True

        self.direction = Vector((self.x, self.y)) - Vector(self.rect_center[0], self.rect_center[1])
        self.direction = self.direction.normalize()

        #pseudo velocity vector - defines only direction no speed
        self.velocity = self.direction.rotate(-90 * self.sign(self.bob.dtheta))
        self.velocity = self.velocity.normalize()

       # self.top_part_length = destroyer_rect.center[1] - self.y

        #this is the top part of the rope
        # self.cut_rope_top = (self.x, self.y)
        # self.cut_rope_bottom = (destroyer_rect[0], destroyer_rect[1])
        # self.cut_rope_bob = Pendulum(self.bob.theta, self.top_part_length, (self.x, self.y))

       # self.x, self.y = destroyer_rect[0], destroyer_rect[1]
        #self.angle = self.cut_rope_bob.theta
       # self.collide_rect.position_m = self.rect.center


    def sign(self, number):
        if number > 0:
            return 1
        else:
            return -1

    def set_up(self, name):
        self.saw_image_master = pygame.image.load(name).convert_alpha()
        self.saw_image_master = pygame.transform.scale(self.saw_image_master, (50, 50))
        self.image = self.saw_image_master

    def update(self, time):
        #remember to implement timer
        if self.is_severed:
            self.time += 0.5

            self.rect.advance((self.velocity.x * 10 + math.sin(math.fabs(self.bob.theta))),
                              (self.velocity.y * 8 * Vector(0, 1).x * 10 + self.time))
            self.rect_center = self.rect.center
        else:
            self.rotate_saw(time)
            self.swing_rope()

    def draw(self, surface, camera):
        if self.is_severed:
            surface.blit(self.image, camera.apply_to_tuple((self.rect.x, self.rect.y)))

        else:
            surface.blit(self.image, camera.apply_to_tuple((self.rect.x, self.rect.y)))
            pygame.draw.line(surface, (0, 0, 0),
                             camera.apply_to_tuple((self.x, self.y)),
                             camera.apply_to_tuple((self.rect.center[0], self.rect.center[1])),
                             self.rope_width)


    def collide_line(self, point_x, point_y):
        #y = kx + c
        if int(self.rect.center[0]) - self.x != 0:
            k = (self.rect.center[1] - self.y) / (self.rect.center[0] - self.x)
            c = self.y - k * self.x
        else:
            return point_x in range(self.x - 10, self.x + 10) \
                and point_y in range(self.y, self.rect.center[1])

        #add room for error due to batarangs teleportational tendencies
        for i in range(0, 30):
            if int(point_y) == int(k * point_x + c) - i or int(point_y) == int(k * point_x + c) + i:
                return True
        return False


    def collide(self, bat):
        #implement list of bats
        if self.collide_line(bat.x, bat.y) and not self.is_severed:
            self.deploy()



class Shadow:
    #this class needs 4 points to use as coordinates
    SHADOW_SURFACE = pygame.Surface((800, 600))
    SHADOW_SURFACE.fill((0, 0, 0))
    SHADOW_SURFACE.set_colorkey((0, 0, 0))
    SHADOW_SURFACE.set_alpha(200)
    SHADOWS = []

    def __init__(self, topleft, topright, bottomright, bottomleft):
        self.topleft = topleft
        self.topright = topright
        self.bottomleft = bottomleft
        self.bottomright = bottomright

        Shadow.SHADOWS.append((self.topleft, self.topright, self.bottomright, self.bottomleft))

    @staticmethod
    def set_up(width, height):
        Shadow.SHADOW_SURFACE = pygame.Surface((width, height))
        Shadow.SHADOW_SURFACE.set_colorkey((0, 0, 0))
        Shadow.SHADOW_SURFACE.set_alpha(200)
        Shadow.SHADOWS = []

    def collide(self, player):
        #def point_inside_polygon(x,y,poly):
        #some raycasting algorithm here
        shadow_coordinates = [self.topleft, self.topright, self.bottomright, self.bottomleft]
        length = len(shadow_coordinates)
        allpoints = []
        for coordinate in player:
            inside = False
            #for coordinates in player:
            point1X, point1Y = shadow_coordinates[0]
            for i in range(length + 1):
                point2X, point2Y = shadow_coordinates[i % length]
                if coordinate[1] > min(point1Y, point2Y):
                    if coordinate[1] <= max(point1Y, point2Y):
                        if coordinate[0] <= max(point1X, point2X):
                            if point1Y != point2Y:
                                xintersection = (coordinate[1]-point1Y) * (point2X-point1X) / (point2Y-point1Y) + point1X
                            if point1X == point2X or coordinate[0] <= xintersection:
                                inside = not inside
                point1X, point1Y = point2X, point2Y
            allpoints.append(inside)
        return all(allpoints)

    def draw(self, surface, camera):
        Shadow.SHADOW_SURFACE.fill((0, 0, 0))
        # pygame.draw.aalines(Shadow.SHADOW_SURFACE, (0, 0, 0, 100), True, [camera.apply_to_tuple(self.topleft), camera.apply_to_tuple(self.topright),
        #                                                             camera.apply_to_tuple(self.bottomright), camera.apply_to_tuple(self.bottomleft)], 50)
        # surface.blit(Shadow.SHADOW_SURFACE, (0, 0))
        pygame.gfxdraw.filled_polygon(Shadow.SHADOW_SURFACE, [camera.apply_to_tuple(self.topleft), camera.apply_to_tuple(self.topright),
                                                          camera.apply_to_tuple(self.bottomright), camera.apply_to_tuple(self.bottomleft)],
        (10, 10, 10))
        pygame.gfxdraw.aapolygon(Shadow.SHADOW_SURFACE, [camera.apply_to_tuple(self.topleft), camera.apply_to_tuple(self.topright),
                                                          camera.apply_to_tuple(self.bottomright), camera.apply_to_tuple(self.bottomleft)],
        (10, 10, 10))
        surface.blit(Shadow.SHADOW_SURFACE, (0, 0))


#
# pygame.init()
# window_width = 800
# window_height = 600
#
# screen = pygame.display.set_mode((window_width, window_height))
# collide_blocks_top = pygame.sprite.Group()
# collide_blocks_bottom = pygame.sprite.Group()
# collide_blocks_right = pygame.sprite.Group()
# collide_blocks_left = pygame.sprite.Group()
# entities = pygame.sprite.Group()
# timer = pygame.time.Clock()
# bat = Batarang(50, 50)
# #X marks the Block
# level = ["XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
#          "X             XXXX   XX X              X",
#          "X         X                            X",
#          "X         S                            X",
#          "X         12            X              X",
#          "X                                      X",
#          "X         4 3                          X",
#          "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"]
# # def level_creator():
# #     x = y = 0
# #     shadows = [[], [], [], []]
# #     for row in level:
# #         for element in row:
# #             if element == "X":
# #                 #entities.add(Block((255, 0, 123), 64, 64, x, y))
# #                 pass
# #             elif element == "S":
# #                 #entities.add(SawBlock(x + 32, y, 100))
# #                 pass
# #             elif element == "1":
# #                 shadows[0].append((x, y))
# #             elif element == "2":
# #                 shadows[1].append((x, y))
# #             elif element == "3":
# #                 shadows[2].append((x, y + 64 ))
# #             elif element == "4":
# #                 shadows[3].append((x, y + 64))
# #
# #             if(y == (len(level) - 1) * 64):
# #                 collide_blocks_bottom.add(Block((255, 0, 123), 64, 64, x, y))
# #             if(y == 0):
# #                 collide_blocks_top.add(Block((255, 0, 123), 64, 64, x, y))
# #             if x == (len(level[0]) - 1) * 32:
# #                 collide_blocks_right.add(Block((255, 0, 123), 64, 64, x, y))
# #             if x == 0:
# #                 collide_blocks_left.add(Block((255, 0, 123), 32, 32, x, y))
# #             x += 64
# #         y += 64
# #         x = 0
# #     #shadows = list(zip(shadows))
# #     sth = []
# #     for shadow in shadows:
# #         for coord in shadow:
# #             sth.append(coord)
# #     Shadow(*sth)
#
# level_width = len(level[0]) * 64
# level_height = len(level) * 64
#
# player = Block((255, 0, 0), 64, 64, 64, 64)
#
# saw = SawBlock(400, 10, 200)
# camera = Camera(level_width, level_height, window_width, window_height)
# #level_creator()
# player = Block((255, 0, 0), 50, 50, 500, 500)
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             sys.exit()
#         if event.type == pygame.MOUSEBUTTONUP:
#             bat.control()
# #
# #
#     time = timer.tick(120)
#
#     screen.fill((255, 255, 255))
#     saw.update(time)
#     saw.draw(screen, camera)
#     bat.update(time)
#     bat.draw(screen, camera)
#     saw.collide(bat)
# #     for entity in entities:
# #         if isinstance(entity, SawBlock):
# #            entity.draw(screen, camera)
# #         else:
# #            screen.blit(entity.image, camera.apply(entity))
# #
# #     keys = pygame.key.get_pressed()
# #
# #     if keys[pygame.K_LEFT]:
# #         player.rect.x -= 5
# #
# #     if keys[pygame.K_RIGHT]:
# #         player.rect.x += 5
# #
# #     if keys[pygame.K_UP]:
# #         player.rect.y -= 5
# #
# #     if keys[pygame.K_DOWN]:
# #         player.rect.y += 5
# #
# #
# #     camera.update(player)
# #
# #     screen.blit(player.image, camera.apply(player))
# #     Shadow.draw(camera)
# #     screen.blit(Shadow.SHADOW_SURFACE, (0, 0))
#     pygame.display.update()
# #
# #
# #
# #

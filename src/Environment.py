import pygame
from pygame import *
from pygame.math import Vector2 as Vector
from Camera import Camera


class Block(pygame.sprite.Sprite):
    #just the basic class for any obstacle
    def __init__(self, colour, width, height, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(colour)
        self.rect = Rect(x, y, width, height)


class SawBlock(pygame.sprite.Sprite):
    #a swinging saw
    def __init__(self, x, y, length):
        pygame.sprite.Sprite.__init__(self)
        #x and y should be the coordinates from the point at which the rope would be hanging
        #self.image = "import saw image here"
        #this is the rope by which the saw would be swinging
        self.saw_image_master = pygame.image.load("saw.png").convert_alpha()
        self.saw_image_master = pygame.transform.scale(self.saw_image_master, (60, 60))
        self.saw_image = self.saw_image_master
        self.saw_rect = self.saw_image.get_rect()
        self.rope_width = 10
        self.rope_height = length
        self.rope_master = pygame.Surface((self.rope_width, self.rope_height)).convert_alpha()
        self.rope = self.rope_master
        self.rope_rect = self.rope.get_rect()
        self.rope_rect.center = (x, y + int(self.rope_height / 2))
        pygame.Surface.fill(self.rope, (255, 0, 0))
        self.x = x
        self.y = y
        self.swinged = 0
       # self.rect = Rect(x, y + 200, 30, 30)
        self.saw_rect.center = (x, y + self.rope_height + 15)
        self.step = 40
        self.swing_step = 1
        self.rotation = 0
        self.is_severed = False
        self.rect = self.saw_rect

    def rotate_saw(self):
        old_center = self.saw_rect.center
        self.saw_image = pygame.transform.rotate(self.saw_image_master, self.rotation)
        self.saw_rect = self.saw_image.get_rect()
        self.saw_rect.center = old_center
        self.rotation += self.step
        if self.rotation > 360:
            self.rotation = self.step

    def swing_rope(self):
        self.swinged += self.swing_step
        self.rope = pygame.transform.rotate(self.rope_master, self.swinged)
        if self.swinged > 40 or self.swinged < -40:
            self.swing_step *= -1

    def deploy(self, destroyer_rect):
        self.is_severed = True
        top_part_length = destroyer_rect.center[1] - self.y
        bottom_part_length = self.rope_height - top_part_length
        #cut_rope is the top part
        self.cut_rope = pygame.Surface((10, top_part_length))
        pygame.Surface.fill(self.cut_rope, (255, 0, 0))
        self.cut_rope_rect = self.cut_rope.get_rect()
        self.cut_rope_rect.center = (self.rope_rect.center[0], self.y + int(top_part_length / 2))
        self.rope = pygame.Surface((10, bottom_part_length))
        self.rope_rect = self.rope.get_rect()
        self.rope_rect.center = (self.cut_rope_rect.center[0], self.y + top_part_length + int(bottom_part_length / 2))
        pygame.Surface.fill(self.rope, (0, 255, 0))

    def move(self, to_move, increment):
        #expected tuple
        to_move = (to_move[0] + increment[0], to_move[1] + increment[1])
        return to_move

    def draw(self, surface, camera):
        if self.is_severed:
            surface.blit(self.cut_rope, camera.apply_to_rect(self.cut_rope_rect))
            surface.blit(self.rope, camera.apply_to_rect(self.rope_rect))
            surface.blit(self.saw_image, camera.apply_to_rect(self.saw_rect))
            self.rope_rect.center = self.move(self.rope_rect.center, (0, 4))
            self.saw_rect = self.saw_rect.move([0, 4])
            self.rotate_saw()
        else:
            self.rotate_saw()
            surface.blit(self.rope, camera.apply_to_rect(self.rope_rect))
            surface.blit(self.saw_image, camera.apply_to_rect(self.saw_rect))

    def collide(self, bat):
        if bat.rect.colliderect(self.rope_rect) and not self.is_severed:
            self.deploy(bat.rect)


class Shadow:
    #this class needs 4 points to use as coordinates
    SHADOW_SURFACE = pygame.Surface((800, 600))
    SHADOW_SURFACE.fill((255, 0, 0))
    SHADOW_SURFACE.set_colorkey((255, 0, 0))
    SHADOW_SURFACE.set_alpha(200)

    def __init__(self, topleft, topright, bottomleft, bottomright):
        self.topleft = topleft
        self.topright = topright
        self.bottomleft = bottomleft
        self.bottomright = bottomright

    def draw(self):
        pygame.draw.polygon(Shadow.SHADOW_SURFACE, (0, 0, 0, 100), [self.topleft, self.topright, self.bottomright, self.bottomleft])

    def collide(self, player, shadow_coordinates):
        #def point_inside_polygon(x,y,poly):
        #some raycasting algorithm here
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

    @staticmethod
    def draw_to_screen(surface):
        surface.blit(Shadow.SHADOW_SURFACE, (0, 0))




pygame.init()
window_width = 800
window_height = 600

screen = pygame.display.set_mode((window_width, window_height))
collide_blocks_top = pygame.sprite.Group()
collide_blocks_bottom = pygame.sprite.Group()
collide_blocks_right = pygame.sprite.Group()
collide_blocks_left = pygame.sprite.Group() 
entities = pygame.sprite.Group()
timer = pygame.time.Clock()

#X marks the Block
level = ["XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
         "X             XXXX   XX X              X",
         "X         X                            X",
         "X         S                            X",
         "X                                      X",
         "X                                      X",
         "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"]
   
x = y = 0
for row in level:
    for element in row:
        if element == "X":
            entities.add(Block((255, 0, 123), 64, 64, x, y))
        elif element == "S":
            entities.add(SawBlock(x + 32, y, 100))

        if(y == (len(level) - 1) * 64):
            collide_blocks_bottom.add(Block((255, 0, 123), 64, 64, x, y))
        if(y == 0):
            collide_blocks_top.add(Block((255, 0, 123), 64, 64, x, y))
        if x == (len(level[0]) - 1) * 32:
            collide_blocks_right.add(Block((255, 0, 123), 64, 64, x, y))
        if x == 0:
            collide_blocks_left.add(Block((255, 0, 123), 32, 32, x, y))
        x += 64
    y += 64
    x = 0

level_width = len(level[0]) * 64
level_height = len(level) * 64

player = Block((255, 0, 0), 64, 64, 64, 64)

camera = Camera(level_width, level_height, window_width, window_height)

    


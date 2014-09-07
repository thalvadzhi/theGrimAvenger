import pygame
from pygame.math import Vector2 as Vector
from BasicShapes import Rectangle
from pixelperfect import get_hitmask


class Batarang():
    def __init__(self, x, y):
        #x and y are the coordinates of player's hand
        self.width = 25
        self.height = 15
        self.image_master = pygame.image.load("batarang2.png").convert_alpha()
        self.image_master = pygame.transform.scale(self.image_master,
                                                   (self.width, self.height))
        self.image = self.image_master
        self.rect_center = (x, y)
        self.rect = Rectangle.get_rect(self.image, self.rect_center)
        self.hitmask = get_hitmask(self.rect, self.image, 0)
        #coordinates of topleft vertex
        self.x = x - self.width // 2
        self.y = y - self.height // 2
        self.direction = Vector(0, 0)
        self.rotation = 0
        self.gravity = 0
        self.frames = 0
        self.step = 40
        self.should_fly = False

    def rotate(self, timer):
        self.image = pygame.transform.rotate(self.image_master,
                                             self.rotation * (1000 / timer))
        self.rect = Rectangle.get_rect(self.image, self.rect.center)

        self.hitmask = get_hitmask(self.rect, self.image, 0)

        self.rotation += self.step
        if self.rotation > 360:
            self.rotation = self.step

    def move(self, timer):
        speed = 50 * 10 * (timer / 1000)
        self.x += self.direction.x * speed
        self.y += self.direction.y * speed

        old_center = self.rect_center
        self.rect_center = (old_center[0] + self.direction.x * speed,
                            old_center[1] + self.direction.y * speed)
        self.rect.center = self.rect_center
        self.rect.center = (self.x + self.rect.width / 2,
                            self.y + self.rect.height / 2)
        self.hitmask = get_hitmask(self.rect, self.image, 0)

    def direct(self, mouse_x, mouse_y):
        #get coordinates of player hand
        #get coordinates of mouse
        #run vector between the two to determine the direction of the batarang
        self.direction = Vector(mouse_x - self.x, mouse_y - self.y)
        self.direction = self.direction.normalize()

    def take_action(self):
        self.mouse_position = pygame.mouse.get_pos()
        self.direct(self.mouse_position[0], self.mouse_position[1])
        self.should_fly = True

    def update(self, timer):
        if self.should_fly:
            self.move(timer)
            self.rotate(timer)
        self.hitmask = get_hitmask(self.rect, self.image, 0)

    def draw(self, surface, camera=0):
        if camera != 0:
            surface.blit(self.image, camera.apply((self.x, self.y)))

        else:
            surface.blit(self.image, (self.x, self.y))

    def reposition(self, coordinates, direction):
        self.rect.center = Vector(coordinates)
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.rotation = direction.angle_to(Vector(1, 0))
        self.image = pygame.transform.rotate(self.image_master,
                                             self.rotation)
        self.rect = Rectangle.get_rect(self.image, self.rect.center)

        self.hitmask = get_hitmask(self.rect, self.image, 0)

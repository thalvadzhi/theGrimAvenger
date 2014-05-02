import math
import sys
import pygame



pygame.init()

screen = pygame.display.set_mode((1000, 500))

clock = pygame.time.Clock()

class Batarang(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #=======================================================================
        # self.imageMaster = pygame.Surface((50,100))
        # self.imageMaster.fill((255,0,0))
        #=======================================================================
        self.imageMaster = pygame.image.load("batman.png")
        self.imageMaster = self.imageMaster.convert()
        self.imageMaster = pygame.transform.scale(self.imageMaster, (50, 100))
        #self.imageMaster = self.imageMaster.convert()
        self.image = self.imageMaster
        self.rect = self.image.get_rect()
        self.image.set_colorkey((255, 255, 255))
        self.rect.center = (320, 240)
        self.dir = 10
        self.gravity = 0
        self.frames = 0
        
    def rotate(self):
        oldCenter = self.rect.center
        self.image = pygame.transform.rotate(self.imageMaster, self.dir)
        self.rect = self.image.get_rect()
        self.rect.center = oldCenter
        self.dir += 40
        if self.dir > 360:
            self.dir = 40


    def move(self, orientation):
        #orientation 1 or -1
        #introduce second parameter to implement gravity
        self.frames += 1
        #after some time gravity starts to take effect
        if(self.frames >= 15):
            self.gravity += 0.5
        self.rect = self.rect.move([20 * orientation, self.gravity])

a = Batarang()
allSprites = pygame.sprite.Group(a)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.fill((255, 255, 255))
    screen.blit(a.image, a.rect)
    a.move(1)
    a.rotate()
    pygame.display.update()
    clock.tick(30)



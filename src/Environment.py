import pygame
from pygame import *

from pygame.locals import KEYDOWN
from tkinter.constants import LEFT
   
   
class Block(pygame.sprite.Sprite):
    #just the basic class for any obstacle
    def __init__(self, colour, width, height, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(colour)
        self.rect = Rect(x, y, width, height)


class Camera():
    def __init__(self, width, height):
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.functionality(target.rect)

    def functionality(self, target):
        left, top = target[0], target[1]
        left = half_width - left
        top = half_height - top
        #this is so as to not scroll the camera outside the borders of the level
        left = min(0, left)
        left = max((window_width - self.state.width), left)
        top = max((window_height - self.state.height), top)
        top = min(0, top)
        return Rect(left, top, self.state[2], self.state[3])


pygame.init()
window_width = 800
window_height = 600
half_width = window_width // 2
half_height = window_height // 2
screen = pygame.display.set_mode((window_width, window_height))
collide_blocks_top = pygame.sprite.Group()
collide_blocks_bottom = pygame.sprite.Group()
collide_blocks_right = pygame.sprite.Group()
collide_blocks_left = pygame.sprite.Group() 
entities = pygame.sprite.Group()
timer = pygame.time.Clock()

level = ["XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
         "X             XXXX   XX X              X",
         "X                                      X",
         "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"]
   
x = y = 0
for row in level:
    for element in row:
        if element == "X":
            entities.add(Block((255, 0, 123), 32, 32, x, y))
        if(y == (len(level) - 1) * 32):
            collide_blocks_bottom.add(Block((255, 0, 123), 32, 32, x, y))
        if(y == 0):
            collide_blocks_top.add(Block((255, 0, 123), 32, 32, x, y))
        if x == (len(level[0]) - 1) * 32:
            collide_blocks_right.add(Block((255, 0, 123), 32, 32, x, y))
        if x == 0:
            collide_blocks_left.add(Block((255, 0, 123), 32, 32, x, y))
        x += 32
    y += 32
    x = 0

level_width = len(level[0]) * 32
level_height = len(level) * 32

player = Block((255, 0, 0), 32, 32, 32, 32)

camera = Camera(level_width, level_height)

    
while True:
    
    events = pygame.event.get()        
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.type == pygame.MOUSEBUTTONUP:
            print(event.button)
        if event.type == pygame.MOUSEMOTION:
            print(event.pos, event.rel)
        if event.type == pygame.QUIT:
            exit(0)
    #implement gravity

    if not bool(pygame.sprite.spritecollideany(player, collide_blocks_bottom)):
        player.rect = player.rect.move([0, 3])
        
           
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and not bool(pygame.sprite.spritecollideany(player, collide_blocks_left)):
        player.rect.x -= 5
        
       
    if keys[pygame.K_RIGHT] and not bool(pygame.sprite.spritecollideany(player, collide_blocks_right)):
        player.rect.x += 5
    
    if keys[pygame.K_UP] and not bool(pygame.sprite.spritecollideany(player, collide_blocks_top)):
        player.rect.y -= 5
            
  
    screen.fill(Color("#500011"))
    camera.update(player)
    
    for entity in entities:
        screen.blit(entity.image, camera.apply(entity))
    screen.blit(player.image, camera.apply(player))   
    timer.tick(60)
    pygame.display.update()

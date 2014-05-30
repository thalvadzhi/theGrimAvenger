import pygame
from pygame import *
from pygame.math import Vector2 as Vector
from Camera import Camera


class Block(pygame.sprite.Sprite):
    #just the basic class for any obstacle
    def __init__(self, colour, width, height, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.saw_image = pygame.Surface((width, height))
        self.saw_image.fill(colour)
        self.saw_rect = Rect(x, y, width, height)

class SawBlock(Block):
    #a swinging saw
    def __init__(self, x, y):
        #x and y should be the coordinates from the point at which the rope would be hanging
        #self.image = "import saw image here"
        #this is the rope by which the saw would be swinging
        self.saw_image_master = pygame.image.load("saw.png").convert_alpha()
        self.saw_image_master = pygame.transform.scale(self.saw_image_master, (60, 60))
        self.saw_image = self.saw_image_master
        self.saw_rect = self.saw_image.get_rect()
        self.rope_width = 10
        self.rope_height = 250
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
        print(top_part_length, bottom_part_length)

        self.cut_rope = pygame.Surface((10, top_part_length))
        pygame.Surface.fill(self.cut_rope, (255, 0, 0))
        self.cut_rope_rect = self.cut_rope.get_rect()
        print("self y: ", self.y)
        self.cut_rope_rect.center = (self.rope_rect.center[0], self.y + int(top_part_length / 2))
        print("self y: ", self.y)
        self.rope = pygame.Surface((10, bottom_part_length))
        self.rope_rect = self.rope.get_rect()
        self.rope_rect.center = (self.cut_rope_rect.center[0], self.y + top_part_length + int(bottom_part_length / 2))

        pygame.Surface.fill(self.rope, (0, 255, 0))
        print(self.cut_rope_rect.center, self.rope_rect.center)

    def move(self, to_move, increment):
        #expected tuple
        to_move = (to_move[0] + increment[0], to_move[1] + increment[1])
        return to_move

    def draw(self, surface):
        if self.is_severed:
            surface.blit(self.cut_rope, self.cut_rope_rect)
            surface.blit(self.rope, self.rope_rect)
            surface.blit(self.saw_image, self.saw_rect)
            self.rope_rect.center = self.move(self.rope_rect.center, (0, 4))
            self.saw_rect = self.saw_rect.move([0, 4])
            self.rotate_saw()
        else:
            self.rotate_saw()
            surface.blit(self.rope, self.rope_rect)
            surface.blit(self.saw_image, self.saw_rect)

    def collide(self, bat):
        if bat.rect.colliderect(self.rope_rect) and not self.is_severed:
            self.deploy(bat.rect)


class Shadow(Block):
    pass





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

camera = Camera(level_width, level_height, window_width, window_height)

    
<<<<<<< HEAD
#===============================================================================
# while True:
#     
#     events = pygame.event.get()        
#     for event in events:
#         if event.type == pygame.QUIT:
#             exit(0)
#     #implement gravity
# 
#     if not bool(pygame.sprite.spritecollideany(player, collide_blocks_bottom)):
#         player.rect = player.rect.move([0, 3])
#         
#            
#     keys = pygame.key.get_pressed()
#     if keys[pygame.K_LEFT] and not bool(pygame.sprite.spritecollideany(player, collide_blocks_left)):
#         player.rect.x -= 5
#         
#        
#     if keys[pygame.K_RIGHT] and not bool(pygame.sprite.spritecollideany(player, collide_blocks_right)):
#         player.rect.x += 5
#     
#     if keys[pygame.K_UP] and not bool(pygame.sprite.spritecollideany(player, collide_blocks_top)):
#         player.rect.y -= 5
#             
#   
#     screen.fill(Color("#500011"))
#     camera.update(player)
#     
#     for entity in entities:
#         screen.blit(entity.image, camera.apply(entity))
#     screen.blit(player.image, camera.apply(player))   
#     timer.tick(60)
#     pygame.display.update()
#===============================================================================
=======
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
>>>>>>> c8a646e751d0abe8d1f69fe0fbcd42a3edd89e8b

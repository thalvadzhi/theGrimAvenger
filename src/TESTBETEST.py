import pygame, sys
from Camera import Camera
from Environment import Block
pygame.init()
window_width = 800
window_height = 500
screen = pygame.display.set_mode((window_width, window_height))

colliders = []
level = ["XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
         "X                                      X",
         "X                                      X",
         "X                                      X",
         "X                                      X",
         "X                                      X",
         "X                                      X",
         "X                                      X",
         "X                                      X",
         "X                                      X",
         "X                                      X",
         "X                                      X",
         "X                                      X",
         "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"]


x = y = 0
for row in level:
    for element in row:
        if element == "X":
            colliders.append(Block((255, 0, 0), 64, 64, x + 64, y + 64))
        x += 64
    y += 64
    x = 0

level_width = len(level[0]) * 64
level_height = len(level) * 64

camera = Camera(level_width, level_height, window_width, window_height)
timer = pygame.time.Clock()
while True:
    for event in pygame.event.get():
     if event.type == pygame.QUIT:
         sys.exit()
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
       pass

    if keys[pygame.K_RIGHT]:
       pass



    timer.tick(60)

    screen.fill((255, 255, 255))
    for collider in colliders:
        collider.draw(screen, camera)
    pygame.display.update()
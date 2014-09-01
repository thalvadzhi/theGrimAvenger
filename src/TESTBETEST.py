import pygame, sys
from Camera import Camera
from Vec2D import Vec2d as Vector
from Environment import Block, SawBlock, Shadow

import pickle

level = pickle.load(open("level.btmn", "rb"))
world = level["world"]
pygame.init()
window_width = level["constants"][0]
window_height = level["constants"][1]
level_width = level["game measures"][0]
level_height = level["game measures"][1]
print(level_width)
screen = pygame.display.set_mode((window_width, window_height), pygame.FULLSCREEN)
camera = Camera(level_width, level_height, window_width, window_height)
timer = pygame.time.Clock()
Shadow.set_up(level_width, level_height)
for item in world:
    if isinstance(item, SawBlock):
        item.set_up("saw.png")
    if isinstance(item, Shadow):
        pass
        print(item.bottomright, item.bottomright, "YEAH")
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            break

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        pass

    if keys[pygame.K_RIGHT]:
        pass



    time = timer.tick(120)

    screen.fill((255, 255, 255))
    #x.draw(screen, camera)
    #world[4].update(time)
    for collider in world:

        collider.draw(screen, camera)
    pygame.display.update()

import pygame, sys, time, math, gradients
import pygame.gfxdraw
from pygame import surfarray
from basicshapes import Rectangle
from light import Light
from pygame.math import Vector2 as Vector
from camera import Camera
pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.HWSURFACE)
timer = pygame.time.Clock()
camera = Camera(800, 600, 800, 600)
one = Rectangle(100, 100, Vector(200, 200))
two = Rectangle(100, 100, Vector(500, 400))
pos = Vector(600, 100)
moving = Rectangle(100, 100, pos)
rects = [one, two, moving]
x = 410
y = 290
l = Light(x, y, rects, 800, 600)
light = pygame.Rect(l.x, l.y, 30, 30)



while True:


    events = pygame.event.get()
    screen.fill((255, 255, 255))
    l.draw(screen, camera)
    # #this is the magic
    for rect in rects:
        rect.draw(screen, (0, 0, 0), camera)
    l.update()
    # light_image.fill((255, 255, 255, 255))
    # pygame.draw.polygon(light_image, (0, 0, 0, 0), visibility)
    # # pygame.gfxdraw.filled_polygon(light_image, visibility, (0, 0, 0, 0))
    # # pygame.gfxdraw.aapolygon(light_image, visibility, (0, 0, 0, 0))
    # light_surface.fill((50, 50, 50, 150))
    # light_surface.blit(light_image, (0, 0), None, pygame.BLEND_RGBA_MIN)



    #pygame.draw.polygon(screen, (0, 255, 0), visibility)

    #pygame.gfxdraw.textured_polygon(light_surface, visibility, light_image, l.x - 150, -l.y + 150)

    pygame.draw.rect(screen, (255, 255, 255), [l.x, l.y, 30, 30])


    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        #time.sleep(0.2)
        l.update_light_position(l.x + 5, l.y)




    if keys[pygame.K_LEFT]:
       # time.sleep(0.2)


       l.update_light_position(l.x - 5, l.y)



    if keys[pygame.K_UP]:

        #time.sleep(0.2)

        l.update_light_position(l.x, l.y - 5)


    if keys[pygame.K_DOWN]:
       # time.sleep(0.2)
       #  pos = Vector(pos.x, pos.y + 10)
       #  rects[2].position = pos
       #  l.update_obstacles(rects)
       #  l.update()
        l.update_light_position(l.x, l.y + 5)


    pygame.display.flip()


    #TODO screw angles, rotate the line a little if it stops intersecting in one direction let ray through

import pygame

from pygame.math import Vector2 as Vector
from Control import Control
from Motions import Motion
from RagDoll import HumanRagdoll
from BasicShapes import Rectangle
import sys
import time

pygame.init()

screen = pygame.display.set_mode((1000, 1000))

clock = pygame.time.Clock()

ragdoll = HumanRagdoll("Batman")
ragdoll.move(Vector((500, 500)))
motion = Motion(ragdoll)

ground = Rectangle(1000, 70, Vector(500, 1000))

#for body_part in list(ragdoll.body_parts.values())[::-1]:
#    control.left_button_selectable.append(body_part)
anchor = Vector(0, 0)
# def cursor_controll(body, anchor):
#     body.pull_on_anchor(anchor, cursor_location - anchor)
#     anchor = cursor_location

ragdoll_velosity = Vector(0, 0)
cursor_left_button_is_down = False
cursor_selected_body = None

current_frame = 0
current_part = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                cursor_left_button_is_down = True
                for body_part in ragdoll.body_parts.values():
                    if body_part.is_point_in_body(Vector(event.pos)):
                        anchor = Vector(event.pos)
                        cursor_selected_body = body_part
                        break
                    cursor_selected_body = None
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                cursor_left_button_is_down = False

    keys = pygame.key.get_pressed()
    if cursor_left_button_is_down and cursor_selected_body is not None:
        cursor_location = Vector(pygame.mouse.get_pos())
        cursor_selected_body.pull_on_anchor(anchor, cursor_location - anchor)
        anchor = cursor_location
    
    if keys[pygame.K_UP] and current_part:
        ragdoll.joints[current_part].bent_keeping_angles(1)

    if keys[pygame.K_DOWN] and current_part:
        ragdoll.joints[current_part].bent_keeping_angles(-1)    
        
    if keys[pygame.K_RIGHT] and motion.frames:
        if len(motion.frames) - 1 > current_frame:
            current_frame += 1
        ragdoll.set_frame(motion.frames[current_frame])
        time.sleep(0.1)
       
    if keys[pygame.K_LEFT] and motion.frames:
        if current_frame > 0:
            current_frame -= 1
        ragdoll.set_frame(motion.frames[current_frame])
        time.sleep(0.3) 


    if keys[pygame.K_b]:
        current_part = input("joint: ")

    if keys[pygame.K_f]:
        print("current frame: {0}".format(current_frame))

    if keys[pygame.K_e]:
        motion.is_repetitive = True

    if keys[pygame.K_r]:
        motion.current_motion = motion.play_motion(pygame.time)

    if keys[pygame.K_p]:
        motion.play()

    if keys[pygame.K_o]:
        ragdoll.turn("right")
        ragdoll.move(Vector((2, 0)))

    if keys[pygame.K_i]:
        ragdoll.turn("left")
        ragdoll.move(Vector((-2, 0)))

    if keys[pygame.K_d]:
        frame = int(input("frame: "))
        duration = int(input("duration: "))
        motion.set_duration(frame, duration)

    if keys[pygame.K_c]:
        frame = int(input("frame: "))
        motion.capture_frame(frame)

    if keys[pygame.K_s]:
        motion_name = input("motion name: ")
        motion.save_motion(motion_name)

    if keys[pygame.K_l]:
        motion_name = input("motion name: ")
        motion.load_motion(motion_name)

    ragdoll_velosity = ragdoll_velosity + Vector(0, 2)

    ragdoll.move(ragdoll_velosity)
    collide = [ground.check_if_collide(body_part)
               for body_part in ragdoll.body_parts.values()]
    if any(_[0] for _ in collide):
        max_MTV = [_[1] for _ in collide if _[0]][0]
        for MTV in collide:
            if MTV[0]:
                if max_MTV.length() < MTV[1].length():
                    max_MTV = MTV[1]
        ragdoll.move(max_MTV)
        ragdoll_velosity[1] = 0

    screen.fill((55, 155, 255))

    ground.draw(screen)
    ragdoll.draw(screen, (255, 0, 0))
    ragdoll.display_avatar(screen)

    pygame.display.update()
    timer = clock.tick(120)

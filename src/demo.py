import pygame

from pygame.math import Vector2 as Vector
from Batarangs import Batarang
from Control import Control
from Motions import Motion
from RagDoll import HumanRagdoll
from BasicShapes import Rectangle
from Environment import Block
from pixelperfect import collide as collision
import sys

pygame.init()

screen = pygame.display.set_mode((500, 500))

clock = pygame.time.Clock()

#control = Control()
ragdoll = HumanRagdoll("Batman")
#NPC = HumanRagdoll("NPC")
ragdoll.move(Vector((250, 250)))
#NPC.move(Vector((100, 250)))

ground = Rectangle(500, 70, Vector(250, 500))
ground = Block((0, 0, 0), 500, 70, 0, 450)
collider = Block((255, 0, 0), 50, 50, 450, 250)
#for body_part in list(ragdoll.body_parts.values())[::-1]:
#    control.left_button_selectable.append(body_part)
anchor = Vector(0, 0)
# def cursor_controll(body, anchor):
#     body.pull_on_anchor(anchor, cursor_location - anchor)
#     anchor = cursor_location

play = 1
motion = Motion(ragdoll)
ragdoll_velosity = Vector(0, 0)
cursor_left_button_is_down = False
cursor_selected_body = None
utilitites = [Batarang(ragdoll.hand_position("right")[0], ragdoll.hand_position("right")[1])]
world = [collider]
formal_frame = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            utilitites[0].take_action()
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
    timer = clock.tick(60)

    keys = pygame.key.get_pressed()
    if cursor_left_button_is_down and cursor_selected_body is not None:
        cursor_location = Vector(pygame.mouse.get_pos())
        cursor_selected_body.pull_on_anchor(anchor, cursor_location - anchor)
        anchor = cursor_location
    if keys[pygame.K_RIGHT]:
        try:
            next(play)
        except StopIteration:
            play = motion.play_motion()
        ragdoll.turn("right")
        #ragdoll.move(Vector((2, 0)))

    if utilitites[0].should_fly:
        try:
            current_frame = next(play)
        except:
            pass
        if current_frame < 3:
            utilitites[0].reposition((ragdoll.hand_position("right")[0], ragdoll.hand_position("right")[1]), ragdoll.body_parts["right_forearm"].direction)

        if current_frame >= 3 and not utilitites[0].rect.collides_rectangle(collider.rect):
            utilitites[0].update(timer)
        formal_frame = current_frame
    if keys[pygame.K_LEFT]:
        try:
            next(play)
        except StopIteration:
            play = motion.play_motion()
        ragdoll.turn("left")
       # ragdoll.move(Vector((-2, 0)))

    if keys[pygame.K_b]:
         play = motion.play_motion()

    if keys[pygame.K_UP]:
        ragdoll_velosity = ragdoll_velosity + Vector((0, -4))

    if keys[pygame.K_DOWN]:
        # ragdoll.move(Vector((0, 1)))
        ragdoll.joints["right_hip"].bent_keeping_angles(-1)

    if keys[pygame.K_r]:
        ragdoll.rotate(1)

    if keys[pygame.K_c]:
        motion.capture_frame()
        for a in range(100000000):
            pass
        print("ready")

    if keys[pygame.K_s]:
        motion.save_motion("throw_batarang")
        pass

    if keys[pygame.K_l]:
        motion.load_motion("throw_batarang")
        play = motion.play_motion()

    ragdoll_velosity = ragdoll_velosity + Vector(0, 2)

    ragdoll.move(ragdoll_velosity)
    collide = [ground.rect.check_if_collide(body_part)
               for body_part in ragdoll.body_parts.values()]
    if any(_[0] for _ in collide):
        max_MTV = [_[1] for _ in collide if _[0]][0]
        for MTV in collide:
            if MTV[0]:
                if max_MTV.length() < MTV[1].length():
                    max_MTV = MTV[1]
        ragdoll.move(max_MTV)
        ragdoll_velosity = ragdoll_velosity + max_MTV
    screen.fill((55, 155, 255))

    #    for part in ragdoll.body_parts.values():
    #        part.draw(screen)
    ground.draw(screen)

    ragdoll.draw(screen, (255, 0, 0))
    ragdoll.display_avatar(screen)
    for collider in world:
        collider.draw(screen)
    utilitites[0].draw(screen)

    #   NPC.display_avatar(screen)

    pygame.display.update()

    # control.handle_user_input()

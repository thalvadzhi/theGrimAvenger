import pygame

from pygame.math import Vector2 as Vector
from Batarangs import Batarang
from control import Control
from motions import Motion
from ragdoll import HumanRagdoll
from basicshapes import Rectangle
from Camera import Camera
from Environment import Block, SawBlock
from pixelperfect import collide as pixel
import sys

pygame.init()

screen = pygame.display.set_mode((800, 500))

clock = pygame.time.Clock()

#control = Control()
ragdoll = HumanRagdoll("Batman")
#NPC = HumanRagdoll("NPC")
ragdoll.move(Vector((250, 250)))
#NPC.move(Vector((100, 250)))
camera = Camera(800, 500, 800, 500)
ground = Rectangle(500, 70, Vector(250, 500))
ground = Block((0, 0, 0), 500, 70, 0, 450)
block = Block((255, 0, 0), 50, 50, 350, 100)
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
saw = SawBlock(600, 50, 150)
world = [block]
formal_frame = 0
take_coordinates = True

################################################
#make the batarang take coordinates only once
def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper
@run_once
def direct():
    utilitites[0].direct(utilitites[0].mouse_position[0], utilitites[0].mouse_position[1])
##################################################

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            ###########################################
            #otherwise you can reposition batarang's direction on click
            if not utilitites[0].should_fly:
                utilitites[0].take_action()
            ###########################################
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
    timer = clock.tick(120)

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


##########################################
    #this moves is the deal with the batarangs
    if utilitites[0].should_fly:
        try:
            current_frame = next(play)
        except:
            pass
        if current_frame < 3:
            utilitites[0].reposition((ragdoll.hand_position("right")[0], ragdoll.hand_position("right")[1]), ragdoll.body_parts["right_forearm"].direction)

        if current_frame >= 3 and not pixel(utilitites[0], world[0]):
            direct()
            utilitites[0].update(timer)
##########################################

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
#########################################
    #this is all that's needed to cut the saw
    saw.draw(screen, camera)
    saw.update(timer)
    saw.collide(utilitites[0])
##########################################
    #   NPC.display_avatar(screen)

    pygame.display.update()

    # control.handle_user_input()

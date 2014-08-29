import pygame

from pygame.math import Vector2 as Vector

from Control import Control
from Motions import Motion
from RagDoll import HumanRagdoll
from BasicShapes import Rectangle

pygame.init()

screen = pygame.display.set_mode((500, 500))

clock = pygame.time.Clock()

control = Control(2)
ragdoll = HumanRagdoll("Batman")
ragdoll.move(Vector((250, 250)))

ground = Rectangle(500, 70, Vector(250, 500))

for body_part in list(ragdoll.body_parts.values())[::-1]:
    control.left_button_selectable.append(body_part)

play = 1
motion = Motion(ragdoll)
ragdoll_velosity = Vector(0, 0)

while True:
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        try:
            next(play)
        except StopIteration:
            play = motion.play_motion()
        ragdoll.turn("right")
        ragdoll.move(Vector((2, 0)))

    if keys[pygame.K_LEFT]:
        try:
            next(play)
        except StopIteration:
            play = motion.play_motion()
        ragdoll.turn("left")
        ragdoll.move(Vector((-2, 0)))

    if keys[pygame.K_UP]:
        ragdoll_velosity = ragdoll_velosity + Vector((0, -4))

    if keys[pygame.K_DOWN]:
       # ragdoll.move(Vector((0, 1)))
        ragdoll.joints["right_hip"].bent_keeping_angles(-1)

    if keys[pygame.K_r]:
        ragdoll.set_slope(100)

    if keys[pygame.K_c]:
       # motion.capture_frame()
        print(motion.frames)
        for a in range(100000000):
            pass
        print("ready")

    if keys[pygame.K_s]:
       # motion.save_motion("walk")
        pass

    if keys[pygame.K_l]:
        motion.load_motion("walk")
        play = motion.play_motion()

    ragdoll_velosity = ragdoll_velosity + Vector(0, 2)

    ragdoll.move(ragdoll_velosity)
    collide = [ground.check_if_collide(body_part)
               for body_part in ragdoll.body_parts.values()]
    if any(collide):
        max_MTV = [_ for _ in collide if _][0]
        for MTV in collide:
            if MTV:
                if max_MTV.length() < MTV.length():
                    max_MTV = MTV
        ragdoll.move(max_MTV)
        ragdoll_velosity = ragdoll_velosity + max_MTV
    screen.fill((55, 155, 255))

#    for part in ragdoll.body_parts.values():
#        part.draw(screen)
    ground.draw(screen)

    ragdoll.display_avatar(screen)

    pygame.display.update()
    clock.tick(60)

    control.handle_user_input()

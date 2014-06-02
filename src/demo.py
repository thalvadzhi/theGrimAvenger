import pygame

from pygame.math import Vector2 as Vector

from Control import Control

from RagDoll import HumanRagdoll

pygame.init()

screen = pygame.display.set_mode((500, 500))

clock = pygame.time.Clock()

control = Control(2)
ragdoll = HumanRagdoll(190, Vector((250, 250)))
ragdoll.load_avatars("Batma")

for body_part in ragdoll.body_parts:
    control.left_button_selectable.append(body_part)

ragdoll.left_arm.pull_on_anchor(Vector((0, 0)), Vector((250, 250)))

while True:
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        ragdoll.head.move(Vector((-1, 0)))

    elif keys[pygame.K_RIGHT]:
        ragdoll.head.move(Vector((1, 0)))

    elif keys[pygame.K_UP]:
        ragdoll.head.rotate(1)

    elif keys[pygame.K_DOWN]:
        ragdoll.head.rotate(-1)

    screen.fill((55, 155, 255))
    ragdoll.display_avatar(screen)

    pygame.display.update()
    clock.tick(60)

    control.handle_user_input()

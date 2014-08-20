import pygame

from pygame.math import Vector2 as Vector

from Control import Control

from RagDoll import HumanRagdoll

pygame.init()

screen = pygame.display.set_mode((500, 500))

clock = pygame.time.Clock()

control = Control(2)
ragdoll = HumanRagdoll("Batman")
ragdoll.move(Vector((250, 250)))

for body_part in list(ragdoll.body_parts.values())[::-1]:
    control.left_button_selectable.append(body_part.shape)


def play_frame(body, states, state, frames):
    for number in range(frames):
        body.shift_to_next_state({key: (states[(state - 1) % 
                                 (max([num for num in states]) + 1)][1][key] - 
                                        states[state][1][key])
            for key in states[state][1]}, frames)
        yield False
    return True

frames = {}
number_of_frames = 0
current_frame = 0
motion = 1
first = True

frames[number_of_frames] = (ragdoll.save_state(), 
                            ragdoll.calculate_state())
number_of_frames += 1

while True:
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        if first:
            motion = play_frame(ragdoll, frames, 1, 200)
            ragdoll.set_state(frames[0][0])
            first = False
        try:
            next(motion)
        except StopIteration:
            current_frame += 1
            ragdoll.set_state(frames[current_frame % number_of_frames][0])
            motion = play_frame(ragdoll, frames, current_frame % number_of_frames, 200)
        ragdoll.move(Vector((1, 0)))

    elif keys[pygame.K_LEFT]:
        ragdoll.move(Vector((-1, 0)))

    elif keys[pygame.K_UP]:
        ragdoll.move(Vector((0, -1)))

    elif keys[pygame.K_DOWN]:
       # ragdoll.move(Vector((0, 1)))
        ragdoll.body_parts["right_hip"].bent_keeping_angles(-1)

    elif keys[pygame.K_s]:
        frames[number_of_frames] = (ragdoll.save_state(), 
                                    ragdoll.calculate_state())
        number_of_frames += 1

    screen.fill((55, 155, 255))

    for part in ragdoll.body_parts.values():
        part.shape.draw(screen)

    ragdoll.display_avatar(screen)

    pygame.display.update()
    clock.tick(60)

    control.handle_user_input()

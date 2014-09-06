import pygame, sys
from Camera import Camera
from Vec2D import Vec2d as Vector
from Environment import Block, SawBlock, Shadow
from Motions import Motion
from RagDoll import HumanRagdoll

import pickle

level = pickle.load(open("level.btmn", "rb"))
#world = level["world"]
pygame.init()
window_width = level["constants"][0]
window_height = level["constants"][1]
level_width = level["game measures"][0]
level_height = level["game measures"][1]
screen = pygame.display.set_mode((window_width, window_height))
camera = Camera(level_width, level_height, window_width, window_height)
timer = pygame.time.Clock()
Shadow.set_up(level_width, level_height)
saw = SawBlock(50, 50, 150)
#saw.load_texture("saw.png")
# for item in world:
#     if isinstance(item, SawBlock):
#
#     if isinstance(item, Shadow):
#         pass
#         print(item.bottomright, item.bottomright, "YEAH")
world = []
for item in level["sawblocks"]:
    world.append(SawBlock(item[0], item[1], item[2]))
for item in level["blocks"]:
    world.append(Block(item[0], item[1], item[2], item[3], item[4]))
for item in level["shadows"]:
    world.append(Shadow(item[0], item[1], item[2], item[3]))
ragdoll = HumanRagdoll("Batman")
ragdoll.move(Vector(500, 100))
ragdoll_velosity = Vector(0, 0)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            break

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        ragdoll.turn("right")
        ragdoll.move(Vector((2, 0)))

    if keys[pygame.K_LEFT]:
        ragdoll.turn("left")
        ragdoll.move(Vector((-2, 0)))

    if keys[pygame.K_UP]:
        ragdoll_velosity = ragdoll_velosity + Vector((0, -4))

    if keys[pygame.K_DOWN]:
        ragdoll.move(Vector((0, 2)))


    if keys[pygame.K_l]:
        motion.load_motion("walk")
        play = motion.play_motion()

    #ragdoll_velosity = ragdoll_velosity + Vector(0, 2)

    ragdoll.move(ragdoll_velosity)
    collide = []
    for ground in world:
        if isinstance(ground, Block):
            collide.extend([ground.rect.check_if_collide(body_part)
                            for body_part in [ragdoll.body_parts["left_boot"]]])
    #print(collide)

    if any(_[0] for _ in collide):
        max_MTV = [_[1] for _ in collide if _[0]][0]
        for MTV in collide:
            if MTV[0]:
                if max_MTV.length() < MTV[1].length():
                    max_MTV = MTV[1]
        print("YEAAAAAAAH")
        ragdoll.move(max_MTV)




    time = timer.tick(60)
    screen.fill((255, 255, 255))
    #x.draw(screen, camera)
    #world[4].update(time)
    # for collider in world:
    #     if isinstance(collider, SawBlock):
    #         collider.update(time, camera)
    camera.update(ragdoll.position)
    for collider in world:
        if isinstance(collider, SawBlock):
            collider.update(time)
        collider.draw(screen, camera)
    ragdoll.display_avatar(screen, camera)

    pygame.display.update()

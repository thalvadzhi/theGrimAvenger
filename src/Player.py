import pygame
from pygame.math import Vector2 as Vector

from RagDoll import HumanRagdoll
from Motions import Motion

class Player(HumanRagdoll):

    def __init__(self, position=Vector(0, 0)):
        HumanRagdoll.__init__(self, "Batman")
        self.move(position)
        #self.motions = {}
        #for motion in ["walk", "throw_batarang"]:
         #   self.motions[motion] = Motion(self)
          #  self.motions[motion].load_motion(motion)
        self.utilities = {
                "Batarangs" : 0
                }
        self.moving = None

    def equip(self, utility, amount):
        self.utilities[utility] += amount

    def handle_input(self, control):
        for keyboard_input in control.keyboard_input:
            if keyboard_input[2]:
                if keyboard_input[0] in [pygame.K_RIGHT, pygame.K_d]:
                    self.moving = "right"
                    self.turn("right")
                    if self.motion.name is not "walk":
                        self.motion.set_motion("walk")
                        self.motion.current_motion = self.motion.play_motion(control.time)
                elif keyboard_input[0] in [pygame.K_LEFT, pygame.K_a]:
                    self.moving = "left"
                    self.turn("left")
                    if self.motion.name is not "walk":
                        self.motion.set_motion("walk")
                        self.motion.current_motion = self.motion.play_motion(control.time)
                elif keyboard_input[0] in [pygame.K_UP, pygame.K_w]:
                    if self.ground is not None:
                        self.velocity[1] -= 20
                
            else:
                if keyboard_input[0] in [pygame.K_RIGHT, pygame.K_d]:
                    if self.moving is "right":
                        self.moving = None
                elif keyboard_input[0] in [pygame.K_LEFT, pygame.K_a]:
                    if self.moving is "left":
                        self.moving = None
        control.camera.update((self.position.x, self.position.y))
        self.update(control)

    def update(self, control):
        if self.moving:
            self.motion.play()
           # if self.current_motion.name is not "walk":
           #     self.current_motion
            self.turn(self.moving)
            self.move(Vector({"left": (-1, 0), "right": (1, 0)}[self.moving]))

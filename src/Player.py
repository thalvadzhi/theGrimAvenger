import pygame
from collections import OrderedDict
from pygame.math import Vector2 as Vector

from BasicShapes import Circle
from GUI import GUI_SETTINGS
from RagDoll import HumanRagdoll
from Motions import Motion

class Player(HumanRagdoll):

    def __init__(self, position=Vector(0, 0)):
        HumanRagdoll.__init__(self, "Batman")
        self.move(position)
        self._moving = None
        self.equipment = Equipment()

    @property
    def moving(self):
        return self._moving

    @moving.setter
    def moving(self, value):
        self._moving = value
        if value is None:
            self.motion.paused = True
        else:
            self.motion.paused = False
    
    def handle_input(self, control):
        for keyboard_input in control.keyboard_input:
            if keyboard_input[2]:
                if keyboard_input[0] in [pygame.K_RIGHT, pygame.K_d]:
                    self.moving = "right"
                    self.turn("right")
                    if self.motion.name is not "walk":
                        self.motion.set_motion("walk", 2.5)
                        self.motion.current_motion = self.motion.play_motion()
                elif keyboard_input[0] in [pygame.K_LEFT, pygame.K_a]:
                    self.moving = "left"
                    self.turn("left")
                    if self.motion.name is not "walk":
                        self.motion.set_motion("walk", 2.5)
                        self.motion.current_motion = self.motion.play_motion()
                elif keyboard_input[0] in [pygame.K_UP, pygame.K_w]:
                    if self.ground is not None:
                        self.velocity[1] -= 20
                elif keyboard_input[0] >= pygame.K_0 and keyboard_input[0] <= pygame.K_9:
                    self.equipment.equipped = keyboard_input[0] - pygame.K_0
                
            else:
                if keyboard_input[0] in [pygame.K_RIGHT, pygame.K_d]:
                    if self.moving is "right":
                        self.moving = None
                elif keyboard_input[0] in [pygame.K_LEFT, pygame.K_a]:
                    if self.moving is "left":
                        self.moving = None

        for mouse_input in control.mouse_input:
            if mouse_input[2]:
                if mouse_input[0] == 4:
                    self.equipment.switch_right()
                elif mouse_input[0] == 5:
                    self.equipment.switch_left()
            else:
                if mouse_input[0] == 1:
                    if self.equipment.equipped == "Batarang" and self.moving != "throw_batarang":
                        self.turn("left" if self.position[0] > mouse_input[1][0] else "right")
                        self.moving = "throw_batarang"
                        self.motion.set_motion("throw_batarang", 1)
                        self.motion.on_action_frame = lambda : print("yes")
                        self.motion.current_motion = self.motion.play_motion()
                
        control.camera.update((self.position.x, self.position.y))
        self.update(control)

    def update(self, control):
        self.motion.play()
        if self.moving == "left":
            self.move(Vector(-3, 0))
        elif self.moving == "right":
            self.move(Vector(3, 0))
        elif self.moving == "throw_batarang":
            pass

class Equipment:

    def __init__(self):
        self.background = Circle(45, Vector(GUI_SETTINGS["resolution"][0] - 75, 75))
        self.background.load_avatar(r"../ArtWork/GUI/InGame/equipped.png")
        self.background.scale_avatar(90, 90)
        self._equipped = 0
        self.utilities = OrderedDict([
                ("Nothing", 0),
                ("Batarang", 0)
                ])

    @property
    def equipped(self):
        return list(self.utilities.keys())[self._equipped]

    @equipped.setter
    def equipped(self, value):
        if value >= 0 and value < len(self.utilities):
            self._equipped = value

    def switch_left(self):
        self.equipped = self._equipped - 1

    def switch_right(self):
        self.equipped = self._equipped + 1

    def equip(self, utility, amount):
        self.utilities[utility] += amount

    def draw(self, screen):
        self.background.display_avatar(screen)

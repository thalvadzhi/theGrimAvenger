import pygame
import GUI
from Vec2D import Vec2d as Vector

from Control import Control

pygame.init()
control = Control()

menu = GUI.Menu(600, 450, Vector(500,500), "SOUND",
                 (0, 0, 0), (None, 50), 400, 50)
menu.add_element(
    0, GUI.Slider, 10, [0, 100], 400, 5, 15,
    "EFFECTS", (0, 0, 0), (None, 30), 200, 40)
menu.add_element(
    0, GUI.Slider,  10, [0, 100], 400, 5, 15,
    "MUSIC", (0, 0, 0), (None, 30), 200, 40)
menu.add_element(
    20, GUI.Button, 400, 50, "LOAD DEFAULT", (0, 0, 0), (None, 50))
menu.add_element(
    20, GUI.Button, 400, 50, "SAVE", (0, 0, 0), (None, 50))
menu.add_element(
    20, GUI.Button, 400, 50, "BACK", (0, 0, 0), (None, 50))

while True:
    control.screen.fill((255, 255, 255))
    menu.draw(control.screen)
    control.get_user_input()
    menu.handle_input(control)
    pygame.display.update()
    control.clock.tick(60)

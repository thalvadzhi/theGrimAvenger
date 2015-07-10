import pygame

from control import Control

pygame.init()
while True:
    control = Control()
    while True:
        control.next_step()
        control.timer = control.clock.tick(control.gui_settings["fps"])

from BasicShapes import Rectangle
import eztext
from Button import Button
from Camera import Camera
from Environment import Block, SawBlock, Shadow
from pygame.math import Vector2 as Vector
import pygame, sys, math
HEIGHT = 600
WIDTH = 900
FPS = 60
GAME_HEIGHT = HEIGHT
GAME_WIDTH = WIDTH * 2
Shadow.set_up(GAME_WIDTH, GAME_HEIGHT)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
timer = pygame.time.Clock()
camera = Camera(GAME_WIDTH, GAME_HEIGHT, WIDTH, HEIGHT)
moving = Rectangle(WIDTH, HEIGHT, (WIDTH//2, HEIGHT//2))

#this is the menu bar
menu = Rectangle(WIDTH // 4, HEIGHT, (WIDTH - WIDTH // 4 + (WIDTH // 4) // 2, HEIGHT // 2))

##############################
##########text boxes##########
block_textbox = eztext.Input(maxlength=15, color=(255, 0, 0), prompt='w, h, c: ',
                             x=WIDTH - WIDTH // 4 + 10, y=0, font=pygame.font.Font(None, 30))
sawblock_textbox = eztext.Input(maxlength=5, color=(255, 0, 0), prompt='l: ',
                                x=WIDTH - WIDTH // 4 + 10, y=70, font=pygame.font.Font(None, 30))

textboxes = [block_textbox, sawblock_textbox]
##############################


##############################
##########butttons############
rectangle_button = Button((WIDTH - WIDTH // 4 + 10, 30), (150, 30), "Spawn Rect", (0, 0, 0), (255, 0, 0))
sawblock_button = Button((WIDTH - WIDTH // 4 + 10, 100), (150, 30), "Spawn Saw", (0, 0, 0), (255, 0, 0))
shadow_button = Button((WIDTH - WIDTH // 4 + 10, 140), (180, 30), "Spawn Shadow", (0, 0, 0), (255, 0, 0))
expand_button = Button((WIDTH - WIDTH // 4 + 10, 30), (75, 30), "Expand", (0, 0, 0), (255, 255, 255))

buttons = [rectangle_button, sawblock_button, shadow_button]
##############################
def spawn(figure="none", size=(0, 0), colour=(0, 0, 0)):
    if figure == "none":
        return
    elif figure == "block":
        world.append(Block(colour, size[0], size[1], 0, 0))
    elif figure == "sawblock":
        world.append(SawBlock(50, 0, size))
    elif figure == "shadow":
        world.append(Shadow(size[0], size[1], size[2], size[3]))

def convert_to_integer(textbox_input):
    value = textbox_input.value.split()
    if len(value) == 1:
        return int(value[0])
    elif len(value) == 2:
        return int(value[0]), int(value[1])
    else:
        return int(value[0]), int(value[1]), value[2]


def what_to_move(mouse_position, events):
    '''determine which object to move'''
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            for index, piece in enumerate(world):
                if isinstance(piece, Shadow):
                    if piece.collide([mouse_position]):
                        return index
                elif piece.rect.is_point_in_body(mouse_position, camera):
                    return index
    return -1

def resize_shadow(shadow, mouse_position):
    top_left_rect = Rectangle(20, 20, Vector(shadow.topleft))
    top_right_rect = Rectangle(20, 20, Vector(shadow.topright))
    bottom_left_rect = Rectangle(20, 20, Vector(shadow.bottomleft))
    bottom_right_rect = Rectangle(20, 20, Vector(shadow.bottomright))
    rects = [top_left_rect, top_right_rect, bottom_left_rect, bottom_right_rect]
    for rect in rects:
        if rect.is_point_in_body(mouse_position, camera):
            rect.center = Vector(mouse_position)
            shadow.topleft = top_left_rect.center
            shadow.topright = top_right_rect.center
            shadow.bottomleft = bottom_left_rect.center
            shadow.bottomright = bottom_right_rect.center

def move_shadow(shadow):
    # shadow.topleft = shadow.topleft[0] + factor[0], shadow.topleft[1] + factor[1]
    # shadow.topright = shadow.topright[0] + factor[0], shadow.topright[1] + factor[1]
    # shadow.bottomleft = shadow.bottomleft[0] + factor[0], shadow.bottomleft[1] + factor[1]
    # shadow.bottomright = shadow.bottomright[0] + factor[0], shadow.bottomright[1] + factor[1]
    pass

def draw():
    screen.fill((255, 0, 0))
    for piece in world:
        piece.draw(screen, camera)
    menu.draw(screen, (0, 255, 0))

    for button in buttons:
        button.draw(screen)
    for textbox in textboxes:
        textbox.draw(screen)

   #rectangle_button.draw(screen)
    block_textbox.draw(screen)
    pygame.display.update()

def move(index):
    '''do the moving itself'''
    if index == -1:
        return
    while True:
        draw()
        events = pygame.event.get()
        mouse_position = pygame.mouse.get_pos()

        if isinstance(world[index], Block):
            world[index].rect.position_m = Vector(camera.reverse_apply(mouse_position))
        elif isinstance(world[index], SawBlock):
            world[index].rect.center = Vector(camera.reverse_apply(mouse_position))
            world[index].x = mouse_position[0]
            world[index].y = world[index].rect.position_m[1] - world[index].rope_height - 15
        elif isinstance(world[index], Shadow):
            resize_shadow(world[index], mouse_position)
            move_shadow(world[index])

        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                return

def set_focus(mouse_position):
    '''set focus to a textbox so you write only in that one'''
    for textbox in textboxes:
        textbox.is_focused = False
        if textbox.rect.is_point_in_body(mouse_position, camera):
            textbox.is_focused = True


#these are all the printables
world = []
while True:

    mouse_position = pygame.mouse.get_pos()
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            set_focus(mouse_position)
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        moving.center = (moving.center[0] + 5, moving.center[1])
    if keys[pygame.K_LEFT]:
        moving.center = (moving.center[0] - 5, moving.center[1])

    camera.update_rect(moving)
    if rectangle_button.is_pressed(mouse_position, events):
        spawn("block", convert_to_integer(block_textbox))
    elif sawblock_button.is_pressed(mouse_position, events):
        spawn("sawblock", convert_to_integer(sawblock_textbox))
    elif shadow_button.is_pressed(mouse_position, events):
        number_of_clicks = 0
        coordinates = []
        while number_of_clicks < 4:
            mouse_position = pygame.mouse.get_pos()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    coordinates.append(mouse_position)
                    number_of_clicks += 1
        spawn("shadow", coordinates)

    for textbox in textboxes:
        if textbox.is_focused:
            textbox.update(events)

    move(what_to_move(mouse_position, events))
    #resize_shadow(what_to_move(mouse_position, events), mouse_position)
    draw()
    moving.draw(screen, (0, 0, 0))
    timer.tick(FPS)

from BasicShapes import Rectangle
import eztext
import pickle
from Button import Button
from Camera import Camera
from Environment import Block, SawBlock, Shadow
from Vec2D import Vec2d as Vector
import pygame
import sys

HEIGHT = 600
WIDTH = 800
FPS = 60


GAME_MEASURES = [WIDTH, HEIGHT, WIDTH - WIDTH // 4, HEIGHT]
CONSTANTS = [WIDTH, HEIGHT, FPS]
#these are all the printables
world = []

Shadow.set_up(GAME_MEASURES[0], GAME_MEASURES[1])

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
timer = pygame.time.Clock()
moving = Block((0, 0, 0), WIDTH, HEIGHT, 0, 0)

#this is the menu bar
menu = Rectangle(WIDTH // 4, HEIGHT,
                 (WIDTH - WIDTH // 4 + (WIDTH // 4) // 2, HEIGHT // 2))
camera = [Camera(GAME_MEASURES[0], GAME_MEASURES[1],
                 WIDTH - WIDTH // 4, HEIGHT)]

##############################
##########text boxes##########
block_textbox = eztext.Input(maxlength=15, color=(255, 0, 0),
                             prompt='w, h, c: ', x=WIDTH - WIDTH // 4 + 10,
                             y=0, font=pygame.font.Font(None, 30))
sawblock_textbox = eztext.Input(maxlength=5, color=(255, 0, 0), prompt='l: ',
                                x=WIDTH - WIDTH // 4 + 10,
                                y=70, font=pygame.font.Font(None, 30))

textboxes = [block_textbox, sawblock_textbox]
##############################


##############################
##########butttons############
rectangle_button = Button((WIDTH - WIDTH // 4 + 10, 30),
                          (150, 30), "Spawn Rect", (0, 0, 0), (255, 0, 0))
sawblock_button = Button((WIDTH - WIDTH // 4 + 10, 100),
                         (150, 30), "Spawn Saw", (0, 0, 0), (255, 0, 0))
shadow_button = Button((WIDTH - WIDTH // 4 + 10, 140),
                       (180, 30), "Spawn Shadow", (0, 0, 0), (255, 0, 0))
expand_up = Button((WIDTH - WIDTH // 4 + 10, HEIGHT - 90),
                   (100, 30), "Expand^", (0, 0, 0), (255, 255, 255))
expand_right = Button((WIDTH - WIDTH // 4 + 10, HEIGHT - 30),
                      (100, 30), "Expand>", (0, 0, 0), (255, 255, 255))

retract_left = Button((WIDTH - WIDTH // 4 + 110, HEIGHT - 30),
                      (100, 30), "Retract<", (0, 0, 0), (255, 255, 255))
retract_down = Button((WIDTH - WIDTH // 4 + 110, HEIGHT - 90),
                      (100, 30), "Retract\/", (0, 0, 0), (255, 255, 255))

delete_button = Button((WIDTH - WIDTH // 4 + 65, HEIGHT - 140),
                       (100, 30), "Despawn", (0, 0, 0), (255, 255, 255))
save_button = Button((WIDTH - WIDTH // 4 + 65, HEIGHT - 200),
                     (100, 30), "Save", (0, 0, 0), (255, 255, 255))
load_button = Button((WIDTH - WIDTH // 4 + 65, HEIGHT - 280),
                     (100, 30), "Load", (0, 0, 0), (255, 255, 255))

quit = Button((WIDTH - WIDTH // 4 + 65, HEIGHT - 340),
              (100, 30), "Quit", (0, 0, 0), (255, 255, 255))

buttons = [rectangle_button, sawblock_button, shadow_button, expand_up,
           expand_right, retract_down, retract_left, delete_button,
           save_button, load_button, quit]
##############################


def load():
    level = pickle.load(open("level.btmn", "rb"))
    return level


def construct():
    world.clear()
    for item in load()["world"]:
        if isinstance(item, SawBlock):
            item.set_up("saw.png")
        world.append(item)
    CONSTANTS.clear()
    GAME_MEASURES.clear()
    for item in load()["constants"]:
        CONSTANTS.append(item)
    for item in load()["game measures"]:
        GAME_MEASURES.append(item)
    camera.clear()
    camera.append(Camera(GAME_MEASURES[0], GAME_MEASURES[1],
                         WIDTH - WIDTH // 4, HEIGHT))
    Shadow.set_up(GAME_MEASURES[0], GAME_MEASURES[1])


def set_up():
    Shadow.set_up(GAME_MEASURES[0], GAME_MEASURES[1])
    world.append(Block((0, 0, 0), GAME_MEASURES[0],
                       32, 0, 0))
    world.append(Block((0, 0, 0), GAME_MEASURES[0],
                       32, 0, GAME_MEASURES[1] - 32))
    world.append(Block((0, 0, 0), 32, GAME_MEASURES[1],
                       0, 0))
    world.append(Block((0, 0, 0), 32, GAME_MEASURES[1],
                       GAME_MEASURES[0] - 32, 0))


def move_down():
    for index, item in enumerate(world):
        if index >= 4:
            if isinstance(item, Block):
                item.rect.center = Vector(item.rect.center[0],
                                          item.rect.center[1] + 32)
            elif isinstance(item, SawBlock):
                item.y += 32
                item.rect.center = Vector(item.rect.center[0],
                                          item.rect.center[1] + 32)
            elif isinstance(item, Shadow):
                item.topleft = (item.topleft[0], item.topleft[1] + 32)
                item.topright = (item.topright[0], item.topright[1] + 32)
                item.bottomleft = (item.bottomleft[0],
                                   item.bottomleft[1] + 32)
                item.bottomright = (item.bottomright[0],
                                    item.bottomright[1] + 32)


def resize_game_field(action):
    if action == "expand right":
        GAME_MEASURES[0] += 32
    elif action == "expand up":
        GAME_MEASURES[1] += 32
        move_down()
    elif action == "retract left":
        GAME_MEASURES[0] -= 32
    elif action == "retract down":
        GAME_MEASURES[1] -= 32
    else:
        return
    #game_height += 0
    camera[0] = Camera(GAME_MEASURES[0], GAME_MEASURES[1],
                       GAME_MEASURES[2], GAME_MEASURES[3])
    set_up()
    for i in range(4):
        world[i] = world[len(world) - 1]
        world.pop(len(world) - 1)


def save():
    level = {"constants": CONSTANTS,
             "game measures": GAME_MEASURES, "world": world}
    pickle.dump(level, open("level.btmn", "wb"))


def spawn(figure="none", size=(0, 0, (0, 0, 0))):
    if size == -1:
        return
    elif figure == "none":
        return
    elif figure == "block":
        world.append(Block((0, 0, 0), size[0], size[1],
                           camera[0].reverse_apply((32, 32))[0],
                           camera[0].reverse_apply((32, 32))[1]))
    elif figure == "sawblock":
        world.append(SawBlock(camera[0].reverse_apply((50, 0))[0],
                              camera[0].reverse_apply((50, 0))[1], size))
    elif figure == "shadow":
        world.append(Shadow(camera[0].reverse_apply(size[0]),
                            camera[0].reverse_apply(size[1]),
                            camera[0].reverse_apply(size[2]),
                            camera[0].reverse_apply(size[3])))


def de_spawn(index):
    if index == -1:
        return False
    world.pop(index)
    return True


def decode_textbox(textbox_input):
    value = textbox_input.value.split()
    if len(value) == 0:
        return -1
    elif len(value) == 1:
        return int(value[0])
    elif len(value) == 2:
        return int(value[0]), int(value[1])
    else:
        return int(value[0]), int(value[1]), eval(value[2])


def selector(mouse_position, events):
    '''determine which object is selected'''
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            for index, piece in enumerate(world):
                if isinstance(piece, Shadow):
                    if piece.collide(
                            [camera[0].reverse_apply(mouse_position)]):
                        return index
                elif piece.rect.is_point_in_body(mouse_position, camera[0]):
                    return index
    return -1


def resize_shadow(shadow, mouse_position):
    top_left_rect = Rectangle(20, 20, Vector(shadow.topleft))
    top_right_rect = Rectangle(20, 20, Vector(shadow.topright))
    bottom_left_rect = Rectangle(20, 20, Vector(shadow.bottomleft))
    bottom_right_rect = Rectangle(20, 20, Vector(shadow.bottomright))
    rects = [top_left_rect, top_right_rect,
             bottom_left_rect, bottom_right_rect]
    for rect in rects:
        if rect.is_point_in_body(mouse_position, camera[0]):
            rect.center = Vector(camera[0].reverse_apply(mouse_position))
            shadow.topleft = top_left_rect.center[0], top_left_rect.center[1]
            shadow.topright = top_right_rect.center[0], \
                top_right_rect.center[1]
            shadow.bottomleft = bottom_left_rect.center[0], \
                bottom_left_rect.center[1]
            shadow.bottomright = bottom_right_rect.center[0], \
                bottom_right_rect.center[1]


def draw():
    screen.fill((51, 171, 240))
    for piece in world:
        piece.draw(screen, camera[0])
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
    # first four block are the border
    if index <= 3:
        return

    while True:
        draw()
        events = pygame.event.get()
        mouse_position = pygame.mouse.get_pos()

        if isinstance(world[index], Block):
            world[index].rect.position_m = \
                Vector(camera[0].reverse_apply(mouse_position))
        elif isinstance(world[index], SawBlock):
            world[index].rect.center = \
                Vector(camera[0].reverse_apply(mouse_position))
            world[index].x = camera[0].reverse_apply(mouse_position)[0]
            world[index].y = world[index].rect.position_m[1] - \
                world[index].rope_height - 15
        elif isinstance(world[index], Shadow):
            resize_shadow(world[index], mouse_position)

        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                return


def set_focus(mouse_position):
    '''set focus to a textbox so you write only in that one'''
    for textbox in textboxes:
        textbox.is_focused = False
        if textbox.rect.is_point_in_body(mouse_position):
            textbox.is_focused = True


def button_management(mouse_position, events):
    if rectangle_button.is_pressed(mouse_position, events):
        spawn("block", decode_textbox(block_textbox))
    elif sawblock_button.is_pressed(mouse_position, events):
        spawn("sawblock", decode_textbox(sawblock_textbox))
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
    elif expand_up.is_pressed(mouse_position, events):
        resize_game_field("expand up")
    elif expand_right.is_pressed(mouse_position, events):
        resize_game_field("expand right")
    elif retract_down.is_pressed(mouse_position, events):
        resize_game_field("retract down")
    elif retract_left.is_pressed(mouse_position, events):
        resize_game_field("retract left")
    elif quit.is_pressed(mouse_position, events):
        sys.exit()
    elif delete_button.is_pressed(mouse_position, events):
        while True:
            mouse_position = pygame.mouse.get_pos()
            events = pygame.event.get()
            if de_spawn(selector(mouse_position, events)):
                return
    elif save_button.is_pressed(mouse_position, events):
        save()
    elif load_button.is_pressed(mouse_position, events):
        construct()

events = pygame.event.get()
set_up()
while True:

    mouse_position = pygame.mouse.get_pos()
    events = pygame.event.get()
    draw()

    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            set_focus(mouse_position)
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        moving.rect.center = (moving.rect.center[0] + 5, moving.rect.center[1])
    if keys[pygame.K_LEFT]:
        moving.rect.center = (moving.rect.center[0] - 5, moving.rect.center[1])
    if keys[pygame.K_UP]:
        moving.rect.center = (moving.rect.center[0], moving.rect.center[1] - 5)
    if keys[pygame.K_DOWN]:
        moving.rect.center = (moving.rect.center[0], moving.rect.center[1] + 5)

    button_management(mouse_position, events)

    camera[0].update(moving.rect)

    for textbox in textboxes:
        if textbox.is_focused:
            textbox.update(events)

    move(selector(mouse_position, events))
    timer.tick(FPS)

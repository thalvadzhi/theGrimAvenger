from BasicShapes import Rectangle
from Constants import *
import eztext
from Light import Light
from Button import Button
from Camera import Camera
from Environment import Block, SawBlock
import pygame
import sys
from Serialize import *
import json


class DecodingFailure(Exception):
    def __init__(self, message):
        super(DecodingFailure, self).__init__(message)


class LevelDesign:
    GAME_MEASURES = [WIDTH, HEIGHT, WIDTH - WIDTH // 4, HEIGHT]
    def __init__(self):
        self.world = []
        self.lights = []
        #this is the block according to which the view will move
        self.observer = Block((0, 0, 0), WIDTH, HEIGHT, 0, 0)
        self.setup_menu_camera()
        self.setup_text_boxes()
        self.setup_buttons()
        self.set_up_boundaries()
        Light.set_up_surfaces(LevelDesign.GAME_MEASURES[0], LevelDesign.GAME_MEASURES[1])

    def setup_menu_camera(self):
        #this is the menu bar
        self.menu = Rectangle(WIDTH // 4, HEIGHT,
                              (WIDTH - WIDTH // 4 + (WIDTH // 4) // 2, HEIGHT // 2))
        self.camera = Camera(LevelDesign.GAME_MEASURES[0], LevelDesign.GAME_MEASURES[1],
                             WIDTH - WIDTH // 4, HEIGHT)

    def setup_text_boxes(self):
        self.block_textbox = eztext.Input(maxlength=15, color=(255, 0, 0),
                                          prompt='w, h, c: ', x=WIDTH - WIDTH // 4 + 10,
                                          y=0, font=pygame.font.Font(None, 30))
        self.sawblock_textbox = eztext.Input(maxlength=5, color=(255, 0, 0), prompt='l: ',
                                             x=WIDTH - WIDTH // 4 + 10,
                                             y=70, font=pygame.font.Font(None, 30))

        self.textboxes = [self.block_textbox, self.sawblock_textbox]

    def setup_buttons(self):
        self.rectangle_button = Button((WIDTH - WIDTH // 4 + 10, 30),
                                       (150, 30), "Spawn Rect", (0, 0, 0), (255, 0, 0))
        self.sawblock_button = Button((WIDTH - WIDTH // 4 + 10, 100),
                                      (150, 30), "Spawn Saw", (0, 0, 0), (255, 0, 0))
        self.light_button = Button((WIDTH - WIDTH // 4 + 10, 140),
                                   (180, 30), "Spawn Light", (0, 0, 0), (255, 0, 0))
        self.expand_up = Button((WIDTH - WIDTH // 4 + 10, HEIGHT - 90),
                                (100, 30), "Expand^", (0, 0, 0), (255, 255, 255))
        self.expand_right = Button((WIDTH - WIDTH // 4 + 10, HEIGHT - 30),
                                   (100, 30), "Expand>", (0, 0, 0), (255, 255, 255))

        self.retract_left = Button((WIDTH - WIDTH // 4 + 110, HEIGHT - 30),
                                   (100, 30), "Retract<", (0, 0, 0), (255, 255, 255))
        self.retract_down = Button((WIDTH - WIDTH // 4 + 110, HEIGHT - 90),
                                   (100, 30), "Retract\/", (0, 0, 0), (255, 255, 255))

        self.delete_button = Button((WIDTH - WIDTH // 4 + 65, HEIGHT - 140),
                                    (100, 30), "Despawn", (0, 0, 0), (255, 255, 255))
        self.save_button = Button((WIDTH - WIDTH // 4 + 65, HEIGHT - 200),
                                  (100, 30), "Save", (0, 0, 0), (255, 255, 255))
        self.load_button = Button((WIDTH - WIDTH // 4 + 65, HEIGHT - 280),
                                  (100, 30), "Load", (0, 0, 0), (255, 255, 255))

        self.quit = Button((WIDTH - WIDTH // 4 + 65, HEIGHT - 340),
                           (100, 30), "Quit", (0, 0, 0), (255, 255, 255))

        self.buttons = [self.rectangle_button, self.sawblock_button, self.light_button, self.expand_up,
                        self.expand_right, self.retract_down, self.retract_left, self.delete_button,
                        self.save_button, self.load_button, self.quit]


    def move_blocks_down(self):
        for index, item in enumerate(self.world):
            if index >= 4:
                if isinstance(item, Block):
                    item.rect.center = Vector(item.rect.center[0],
                                              item.rect.center[1] + 32)
                elif isinstance(item, SawBlock):
                    item.y += 32
                    item.rect.center = Vector(item.rect.center[0],
                                              item.rect.center[1] + 32)
                elif isinstance(item, Light):
                    item.update_light_position(item.x, item.y + 32)


    def resize_game_field(self, action):
        if action == EXPAND_FIELD_RIGHT:
            LevelDesign.GAME_MEASURES[0] += 32
        elif action == EXPAND_FIELD_UP:
            LevelDesign.GAME_MEASURES[1] += 32
            self.move_blocks_down()
        elif action == RETRACT_FIELD_LEFT:
            LevelDesign.GAME_MEASURES[0] -= 32
        elif action == RETRACT_FIELD_DOWN:
            LevelDesign.GAME_MEASURES[1] -= 32
        else:
            return

        self.camera = Camera(LevelDesign.GAME_MEASURES[0], LevelDesign.GAME_MEASURES[1],
                             LevelDesign.GAME_MEASURES[2], LevelDesign.GAME_MEASURES[3])

        #TODO FIX RETRACTION
        #set_up()
        # for i in range(4):
        #     self.world[i] = self.world[len(self.world) - 1]
        #     self.world.pop(len(self.world) - 1)


    def save(self):
        world = json.dumps(self.world, cls=Encoder)
        light = json.dumps(self.lights, cls=Encoder)

        try:
            with open("level2.btmn", "w") as level:
                level.write(world)
                level.write("\n")
                level.write(light)
        except FileNotFoundError:
            return

    def load(self):
        try:
            with open("level2.btmn", "r") as level:
                world = level.readline()
                light = level.readline()
                self.world = json.loads(world, cls=Decoder)
                self.lights = json.loads(light, cls=Decoder)
        except FileNotFoundError:
            return

    def spawn_block(self, information, camera, colour=(0, 0, 0)):
        #information contains, width, height, tag
        self.world.append(Block(colour, information[0], information[1], camera.reverse_apply((32, 32))[0],
                                camera.reverse_apply((32, 32))[1], information[2]))
        for light in self.lights:
            light.update_obstacles(self.world)

    def spawn_saw_block(self, length, camera):
        self.world.append(SawBlock(camera.reverse_apply((50, 0))[0],
                                   camera.reverse_apply((50, 0))[1], length))

    def spawn_light(self, radius, camera):
        self.lights.append(Light(camera.reverse_apply((50, 50))[0],
                                 camera.reverse_apply((50, 50))[1],
                                 radius, self.world))


    def de_spawn(self, index_object):
        if index_object == NO_OBJECT_SELECTED:
            return False
        index = index_object[0]
        object = index_object[1]
        if object == OBJECT:
            self.world.pop(index)
        else:
            self.lights.pop(index)
        return True


    def decode_textbox(self, textbox_input, context):
        try:
            value = textbox_input.value.split()
            if context == OBJECT_BLOCK:
                if len(value) == 3:
                    return int(value[0]), int(value[1]), TAG_WALL
                else:
                    return int(value[0]), int(value[1]), TAG_GROUND
            elif context == OBJECT_SAW_BLOCK or context == OBJECT_LIGHT:
                return int(value[0])
                #if we can't decode it
        except ValueError:
            raise DecodingFailure



    def selector(self, mouse_position, events):
        '''determine which object is selected'''
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for index, piece in enumerate(self.world):
                    if index < 3:
                        #first four are always boundaries
                        continue
                    if isinstance(piece, Light):
                        if piece.collide(
                                self.camera.reverse_apply(mouse_position)):
                            return index, OBJECT
                    elif piece.rect.is_point_in_body(mouse_position, self.camera):
                        return index, OBJECT
                for index, light in enumerate(self.lights):
                    if light.collide(self.camera.reverse_apply(mouse_position)):
                        return index, OBJECT_LIGHT
        return NO_OBJECT_SELECTED


    def draw_light(self, screen):
        Light.nullify_shadow()
        Light.nullify_light()
        for light in self.lights:
            light.draw_shadow(self.camera)
            light.draw_light(self.camera)
        Light.draw_everything(screen)

    def draw(self, screen):
        screen.fill((51, 171, 240))

        self.draw_light(screen)
        for piece in self.world:
            piece.draw(screen, self.camera)
        self.menu.draw(screen, (0, 255, 0))
        for button in self.buttons:
            button.draw(screen)
        for textbox in self.textboxes:
            textbox.draw(screen)

            #rectangle_button.draw(screen)
        self.block_textbox.draw(screen)
        pygame.display.update()

    def set_up_boundaries(self):
        self.world.append(Block((0, 0, 0), LevelDesign.GAME_MEASURES[0], 32, 0, 0, TAG_GROUND))
        self.world.append(Block((0, 0, 0), LevelDesign.GAME_MEASURES[0],
                           32, 0, LevelDesign.GAME_MEASURES[1] - 32, TAG_GROUND))
        self.world.append(Block((0, 0, 0), 32, LevelDesign.GAME_MEASURES[1],
                       0, 0, TAG_WALL))
        self.world.append(Block((0, 0, 0), 32, LevelDesign.GAME_MEASURES[1],
                       LevelDesign.GAME_MEASURES[0] - 32, 0, TAG_WALL))


    def move_block(self, index, position):
        self.world[index].rect.position = \
            Vector(self.camera.reverse_apply(position))
        self.world[index].x = self.camera.reverse_apply(position)[0] - self.world[index].width / 2
        self.world[index].y = self.camera.reverse_apply(position)[1] - self.world[index].height / 2

        for light in self.lights:
            light.update_obstacles(self.world)

    def move_saw_block(self, index, position):
        self.world[index].rect.center = Vector(self.camera.reverse_apply(position))
        self.world[index].x = self.camera.reverse_apply(position)[0]
        self.world[index].y = self.world[index].rect.position[1] - self.world[index].rope_height - 15

    def move_lights(self, index, position):
        self.lights[index].update_light_position(self.camera.reverse_apply(position)[0],
                                                 self.camera.reverse_apply(position)[1])

    def move(self, index_object, screen):
        '''do the moving itself'''
        if index_object == NO_OBJECT_SELECTED:
            return
        index = index_object[0]
        object = index_object[1]
        while True:
            self.draw(screen)
            events = pygame.event.get()
            mouse_position = pygame.mouse.get_pos()

            if object == OBJECT:
                if isinstance(self.world[index], Block):
                    self.move_block(index, mouse_position)
                elif isinstance(self.world[index], SawBlock):
                    self.move_saw_block(index, mouse_position)
            else:
                self.move_lights(index, mouse_position)
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP:
                    return

    def set_focus(self, mouse_position):
        '''set focus to a textbox so you write only in that one'''
        for textbox in self.textboxes:
            textbox.is_focused = False
            if textbox.rect.is_point_in_body(mouse_position):
                textbox.is_focused = True


    def button_management(self, mouse_position, events):
        try:
            if self.rectangle_button.is_pressed(mouse_position, events):
                self.spawn_block(self.decode_textbox(self.block_textbox, OBJECT_BLOCK), self.camera)
            elif self.sawblock_button.is_pressed(mouse_position, events):
                self.spawn_saw_block(self.decode_textbox(self.sawblock_textbox, OBJECT_SAW_BLOCK), self.camera)
            elif self.light_button.is_pressed(mouse_position, events):
                self.spawn_light(400, self.camera)
            elif self.expand_up.is_pressed(mouse_position, events):
                self.resize_game_field(EXPAND_FIELD_UP)
            elif self.expand_right.is_pressed(mouse_position, events):
                self.resize_game_field(EXPAND_FIELD_RIGHT)
            elif self.retract_down.is_pressed(mouse_position, events):
                self.resize_game_field(RETRACT_FIELD_DOWN)
            elif self.retract_left.is_pressed(mouse_position, events):
                self.resize_game_field(RETRACT_FIELD_LEFT)
            elif self.quit.is_pressed(mouse_position, events):
                sys.exit()
            elif self.delete_button.is_pressed(mouse_position, events):
                while True:
                    mouse_position = pygame.mouse.get_pos()
                    events = pygame.event.get()
                    if self.de_spawn(self.selector(mouse_position, events)):
                        return
            elif self.save_button.is_pressed(mouse_position, events):
                    self.save()
            elif self.load_button.is_pressed(mouse_position, events):
                    self.load()
        except DecodingFailure:
            return

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
timer = pygame.time.Clock()
design = LevelDesign()
while True:

    mouse_position = pygame.mouse.get_pos()
    events = pygame.event.get()
    design.draw(screen)

    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            design.set_focus(mouse_position)
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        design.observer.rect.center = (design.observer.rect.center[0] + 5, design.observer.rect.center[1])
    if keys[pygame.K_LEFT]:
        design.observer.rect.center = (design.observer.rect.center[0] - 5, design.observer.rect.center[1])
    if keys[pygame.K_UP]:
        design.observer.rect.center = (design.observer.rect.center[0], design.observer.rect.center[1] - 5)
    if keys[pygame.K_DOWN]:
        design.observer.rect.center = (design.observer.rect.center[0], design.observer.rect.center[1] + 5)

    design.button_management(mouse_position, events)

    design.camera.update(design.observer.rect)

    for textbox in design.textboxes:
        if textbox.is_focused:
            textbox.update(events)

    design.move(design.selector(mouse_position, events), screen)
    timer.tick(FPS)

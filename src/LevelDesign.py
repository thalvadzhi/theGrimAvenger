import pygame
import json
import sys
from pygame.math import Vector2 as Vector
import eztext
from BasicShapes import Rectangle
from Constants import WIDTH, HEIGHT, MUSIC_IN_GAME1, EXPAND_FIELD_RIGHT, \
    EXPAND_FIELD_UP, RETRACT_FIELD_LEFT, RETRACT_FIELD_DOWN, NO_OBJECT_SELECTED, \
    OBJECT, OBJECT_BLOCK, TAG_WALL, TAG_GROUND, OBJECT_SAW_BLOCK, OBJECT_LIGHT, \
    OBJECT_SWINGING_LIGHT, FPS, DEFAULT_START_POSITION, LIGHT_RADIUS
from SwingingLight import SwingingLight
from Light import Light
from Button import Button
from Camera import Camera
from Environment import Block, SawBlock
from Serialize import Encoder, Decoder
from Settings import Settings


class DecodingFailure(Exception):
    def __init__(self, message):
        super(DecodingFailure, self).__init__(message)


class LevelDesign:
    GAME_MEASURES = [WIDTH, HEIGHT, WIDTH - WIDTH // 4, HEIGHT]

    def __init__(self):
        self.world = []
        self.lights = []
        self.swinging_lights = []
        # this is the block according to which the view will move
        self.observer = Block((0, 0, 0), WIDTH, HEIGHT, 0, 0)
        self.setup_menu_camera()
        self.setup_text_boxes()
        self.setup_buttons()
        self.set_up_boundaries()
        Light.set_up_surfaces(LevelDesign.GAME_MEASURES[0],
                              LevelDesign.GAME_MEASURES[1])
        self.settings = Settings(LevelDesign.GAME_MEASURES[0],
                                 LevelDesign.GAME_MEASURES[1],
                                 MUSIC_IN_GAME1, DEFAULT_START_POSITION)

    def setup_menu_camera(self):
        # this is the menu bar
        self.menu = Rectangle(WIDTH // 4, HEIGHT,
                              (WIDTH - WIDTH // 4 + (WIDTH // 4) // 2,
                               HEIGHT // 2))
        self.camera = Camera(LevelDesign.GAME_MEASURES[0],
                             LevelDesign.GAME_MEASURES[1],
                             WIDTH - WIDTH // 4, HEIGHT)

    def setup_text_boxes(self):
        self.block_textbox = eztext.Input(maxlength=15, color=(255, 0, 0),
                                          prompt='w, h, c: ',
                                          x=WIDTH - WIDTH // 4 + 10,
                                          y=0, font=pygame.font.Font(None, 30))
        self.sawblock_textbox = eztext.Input(maxlength=5, color=(255, 0, 0),
                                             prompt='l: ',
                                             x=WIDTH - WIDTH // 4 + 10, y=70,
                                             font=pygame.font.Font(None, 30))

        self.textboxes = [self.block_textbox, self.sawblock_textbox]

    def setup_buttons(self):
        self.rectangle_button = Button((WIDTH - WIDTH // 4 + 10, 30),
                                       (150, 30), "Spawn Rect",
                                       (0, 0, 0), (255, 0, 0))

        self.sawblock_button = Button((WIDTH - WIDTH // 4 + 10, 100),
                                      (150, 30), "Spawn Saw",
                                      (0, 0, 0), (255, 0, 0))

        self.light_button = Button((WIDTH - WIDTH // 4 + 10, 140),
                                   (180, 30), "Spawn Light",
                                   (0, 0, 0), (255, 0, 0))

        self.swinginglight_button = Button((WIDTH - WIDTH // 4 + 10, 180),
                                           (180, 30), "Swinging Light",
                                           (0, 0, 0), (255, 0, 0))

        self.expand_up = Button((WIDTH - WIDTH // 4 + 10, HEIGHT - 90),
                                (100, 30), "Expand^",
                                (0, 0, 0), (255, 255, 255))

        self.expand_right = Button((WIDTH - WIDTH // 4 + 10, HEIGHT - 30),
                                   (100, 30), "Expand>",
                                   (0, 0, 0), (255, 255, 255))

        self.retract_left = Button((WIDTH - WIDTH // 4 + 110, HEIGHT - 30),
                                   (100, 30), "Retract<",
                                   (0, 0, 0), (255, 255, 255))

        self.retract_down = Button((WIDTH - WIDTH // 4 + 110, HEIGHT - 90),
                                   (100, 30), "Retract\/",
                                   (0, 0, 0), (255, 255, 255))

        self.delete_button = Button((WIDTH - WIDTH // 4 + 65, HEIGHT - 140),
                                    (100, 30), "Despawn",
                                    (0, 0, 0), (255, 255, 255))

        self.save_button = Button((WIDTH - WIDTH // 4 + 65, HEIGHT - 200),
                                  (100, 30), "Save",
                                  (0, 0, 0), (255, 255, 255))

        self.load_button = Button((WIDTH - WIDTH // 4 + 65, HEIGHT - 280),
                                  (100, 30), "Load",
                                  (0, 0, 0), (255, 255, 255))

        self.quit = Button((WIDTH - WIDTH // 4 + 65, HEIGHT - 340),
                           (100, 30), "Quit",
                           (0, 0, 0), (255, 255, 255))

        self.buttons = [self.rectangle_button, self.sawblock_button,
                        self.light_button, self.expand_up, self.expand_right,
                        self.retract_down, self.retract_left,
                        self.delete_button, self.save_button, self.load_button,
                        self.quit, self.swinginglight_button]

    def move_blocks_down(self):
        """first 4 blocks are always the boundaries"""
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

        self.camera = Camera(LevelDesign.GAME_MEASURES[0],
                             LevelDesign.GAME_MEASURES[1],
                             LevelDesign.GAME_MEASURES[2],
                             LevelDesign.GAME_MEASURES[3])

        self.settings.width = LevelDesign.GAME_MEASURES[0]
        self.settings.height = LevelDesign.GAME_MEASURES[1]

        self.set_up_boundaries()

        self.world = self.world[-4:] + self.world[4:-4]

        Light.update_surfaces(LevelDesign.GAME_MEASURES[0],
                              LevelDesign.GAME_MEASURES[1])

        for light in self.lights:
            light.update_obstacles(self.world)
            light.update_local_surfaces()

    def save(self):
        world = json.dumps(self.world, cls=Encoder)
        light = json.dumps(self.lights, cls=Encoder)
        settings = json.dumps(self.settings, cls=Encoder)
        swinging_lights = json.dumps(self.swinging_lights, cls=Encoder)
        with open("../Files/Levels/level2.btmn", "w") as level:
            print(world, file=level)
            print(light, file=level)
            print(settings, file=level)
            print(swinging_lights, file=level)

    def load(self):
        with open("../Files/Levels/level2.btmn", "r") as level:
            world = level.readline()
            light = level.readline()
            settings = level.readline()
            swinging_lights = level.readline()

            self.settings = json.loads(settings, cls=Decoder)
            LevelDesign.GAME_MEASURES[0] = self.settings.width
            LevelDesign.GAME_MEASURES[1] = self.settings.height
            Light.set_up_surfaces(LevelDesign.GAME_MEASURES[0],
                                  LevelDesign.GAME_MEASURES[1])
            self.camera = Camera(LevelDesign.GAME_MEASURES[0],
                                 LevelDesign.GAME_MEASURES[1],
                                 LevelDesign.GAME_MEASURES[2],
                                 LevelDesign.GAME_MEASURES[3])
            self.world = json.loads(world, cls=Decoder)
            self.lights = json.loads(light, cls=Decoder)
            self.swinging_lights = json.loads(swinging_lights, cls=Decoder)

        for light in self.lights + self.swinging_lights:
            light.update_obstacles(self.world)

    def spawn_block(self, information, camera, colour=(0, 0, 0)):
        """information contains, width, height, tag"""
        self.world.append(Block(colour, information[0], information[1],
                                camera.reverse_apply((32, 32))[0],
                                camera.reverse_apply((32, 32))[1],
                                information[2]))
        for light in self.lights:
            light.update_obstacles(self.world)

    def spawn_saw_block(self, length, camera):
        self.world.append(SawBlock(camera.reverse_apply((50, 0))[0],
                                   camera.reverse_apply((50, 0))[1], length))

    def spawn_light(self, radius, camera):
        self.lights.append(Light(camera.reverse_apply((50, 50))[0],
                                 camera.reverse_apply((50, 50))[1],
                                 radius, self.world))

    def spawn_swinging_light(self, rope_length, camera):
        coordinates = camera.reverse_apply((50, 50))
        self.swinging_lights.append(SwingingLight(coordinates[0],
                                                  coordinates[1],
                                                  rope_length,
                                                  self.world))

    def de_spawn(self, index_object):
        if index_object == NO_OBJECT_SELECTED:
            return False
        index, object_type = index_object
        if object_type == OBJECT:
            self.world.pop(index)
        elif object_type == OBJECT_LIGHT:
            self.lights.pop(index)
        elif object_type == OBJECT_SWINGING_LIGHT:
            self.swinging_lights.pop(index)
        return True

    def decode_textbox(self, textbox_input, context):
        try:
            value = textbox_input.value.split()
            if context == OBJECT_BLOCK:
                if len(value) == 3:
                    return int(value[0]), int(value[1]), TAG_WALL
                else:
                    return int(value[0]), int(value[1]), TAG_GROUND
            elif context == OBJECT_SAW_BLOCK or context == OBJECT_LIGHT or\
                    context == OBJECT_SWINGING_LIGHT:
                return int(value[0])
                # if we can't decode it
        except ValueError:
            raise DecodingFailure
        except IndexError:
            return

    def selector(self, mouse_position, events):
        """determine which object is selected"""
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for index, piece in enumerate(self.world):
                    if index < 3:
                        continue
                    elif piece.rect.is_point_in_body(mouse_position,
                                                     self.camera):
                        return index, OBJECT
                for index, light in enumerate(self.lights):
                    if light.collide(
                            self.camera.reverse_apply(mouse_position)):
                        return index, OBJECT_LIGHT
                for index, swinging_light in enumerate(self.swinging_lights):
                    if swinging_light.collide(
                            self.camera.reverse_apply(mouse_position)):
                        return index, OBJECT_SWINGING_LIGHT
        return NO_OBJECT_SELECTED

    def draw_light(self, screen):
        for light in self.lights:
            light.draw_shadow(self.camera)
            light.draw_light(self.camera)

    def draw(self, screen):
        screen.fill((255, 255, 255))
        Light.nullify_shadow()
        Light.nullify_light()
        self.draw_light(screen)
        for piece in self.world:
            piece.draw(screen, self.camera)
        for swinging_light in self.swinging_lights:
            swinging_light.draw(screen, self.camera)
        Light.draw_everything(screen)
        self.menu.draw(screen, (0, 255, 0))
        for button in self.buttons:
            button.draw(screen)
        for text_box in self.textboxes:
            text_box.draw(screen)
        self.block_textbox.draw(screen)
        pygame.display.update()

    def set_up_boundaries(self):
        self.world.append(Block((0, 0, 0),
                                LevelDesign.GAME_MEASURES[0], 32,
                                0, 0, TAG_GROUND))
        self.world.append(Block((0, 0, 0),
                                LevelDesign.GAME_MEASURES[0],
                                32, 0, LevelDesign.GAME_MEASURES[1] - 32,
                                TAG_GROUND))
        self.world.append(Block((0, 0, 0), 32,
                                LevelDesign.GAME_MEASURES[1],
                                0, 0, TAG_WALL))
        self.world.append(Block((0, 0, 0), 32,
                                LevelDesign.GAME_MEASURES[1],
                                LevelDesign.GAME_MEASURES[0] - 32,
                                0, TAG_WALL))

    def move_block(self, index, position):
        self.world[index].rect.position = \
            Vector(self.camera.reverse_apply(position))
        self.world[index].x = self.camera.reverse_apply(position)[0] -\
            self.world[index].width / 2
        self.world[index].y = self.camera.reverse_apply(position)[1] -\
            self.world[index].height / 2

        for light in self.lights + self.swinging_lights:
            light.update_obstacles(self.world)

    def move_saw_block(self, index, position):
        self.world[index].rect.center = \
            Vector(self.camera.reverse_apply(position))
        self.world[index].x = self.camera.reverse_apply(position)[0]
        self.world[index].y = self.world[index].rect.position[1] - \
            self.world[index].rope_height - 15

    def move_lights(self, index, position):
        self.lights[index].\
            update_light_position(self.camera.reverse_apply(position)[0],
                                  self.camera.reverse_apply(position)[1])

    def move_swinging_lights(self, index, position):
        self.swinging_lights[index].\
            update_position(self.camera.reverse_apply(position)[0],
                            self.camera.reverse_apply(position)[1])

    def move(self, index_object, screen):
        """do the moving itself"""
        if index_object == NO_OBJECT_SELECTED:
            return
        index, object = index_object
        while True:
            self.draw(screen)
            events = pygame.event.get()
            mouse_position = pygame.mouse.get_pos()

            if object == OBJECT:
                if isinstance(self.world[index], Block):
                    self.move_block(index, mouse_position)
                elif isinstance(self.world[index], SawBlock):
                    self.move_saw_block(index, mouse_position)
            elif object == OBJECT_LIGHT:
                self.move_lights(index, mouse_position)
            elif object == OBJECT_SWINGING_LIGHT:
                self.move_swinging_lights(index, mouse_position)
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP:
                    return

    def set_focus(self, mouse_position):
        """set focus to a textbox so you write only in that one"""
        for text_box in self.textboxes:
            text_box.is_focused = False
            if text_box.rect.is_point_in_body(mouse_position):
                text_box.is_focused = True

    def update(self):
        for swinging_light in self.swinging_lights:
            swinging_light.update()

    def button_management(self, mouse_position, events):
        try:
            if self.rectangle_button.is_pressed(mouse_position, events):
                decoded = self.decode_textbox(self.block_textbox, OBJECT_BLOCK)
                if decoded is not None:
                    self.spawn_block(decoded, self.camera)
            elif self.sawblock_button.is_pressed(mouse_position, events):
                decoded = self.decode_textbox(self.sawblock_textbox,
                                              OBJECT_SAW_BLOCK)
                if decoded is not None:
                    self.spawn_saw_block(decoded, self.camera)
            elif self.swinginglight_button.is_pressed(mouse_position, events):
                decoded = self.decode_textbox(self.sawblock_textbox,
                                              OBJECT_SAW_BLOCK)
                if decoded is not None:
                    self.spawn_swinging_light(decoded, self.camera)
            elif self.light_button.is_pressed(mouse_position, events):
                self.spawn_light(LIGHT_RADIUS, self.camera)
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
        design.observer.rect.center = (design.observer.rect.center[0] + 5,
                                       design.observer.rect.center[1])
    if keys[pygame.K_LEFT]:
        design.observer.rect.center = (design.observer.rect.center[0] - 5,
                                       design.observer.rect.center[1])
    if keys[pygame.K_UP]:
        design.observer.rect.center = (design.observer.rect.center[0],
                                       design.observer.rect.center[1] - 5)
    if keys[pygame.K_DOWN]:
        design.observer.rect.center = (design.observer.rect.center[0],
                                       design.observer.rect.center[1] + 5)

    design.button_management(mouse_position, events)

    design.camera.update(design.observer.rect)

    for textbox in design.textboxes:
        if textbox.is_focused:
            textbox.update(events)
    # design.update()
    design.move(design.selector(mouse_position, events), screen)
    timer.tick(FPS)

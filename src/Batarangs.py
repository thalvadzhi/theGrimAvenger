from pygame import time, mouse
from pygame.math import Vector2 as Vector
from BasicShapes import Triangle
from light_cast_v3 import Line, Point
from Constants import ROTATION_STEP, BATARANG_IMAGE, \
    BATARANG_HEIGHT, BATARANG_WIDTH


class Batarang():
    def __init__(self, x, y, world):
        """x and y are the coordinates of player's hand,
        world are all objects batarang can collide with
        """
        self.width = BATARANG_WIDTH
        self.height = BATARANG_HEIGHT
        self.world = world.level_blocks
        self.saws = world.level_saws
        self.x, self.y = x, y
        self.triangle = Triangle([Vector(self.x, self.y),
                                  Vector(self.x + self.width, self.y),
                                  Vector(self.x + self.width // 2,
                                         self.y + self.height)],
                                 (self.x, self.y))
        self.triangle.load_avatar("/Environment/{0}".format(BATARANG_IMAGE))
        self.triangle.scale_avatar(self.width, self.height)
        self.direction = Vector(0, 0)
        self.rotation = 0
        self.step = ROTATION_STEP
        self.speed = 0
        self.last_update = 0
        self.mouse_position = 0
        self.should_fly = False

    def rotate(self, timer):
        self.triangle.rotate(self.rotation * (1000 / timer))
        self.triangle.move(Vector((self.x, self.y)) - self.triangle.position)
        self.rotation += self.step
        if self.rotation > 360:
            self.rotation = self.step

    def move(self, timer):
        self.speed = 50 * 10 * (timer / 1000)
        self.x += self.direction.x * self.speed
        self.y += self.direction.y * self.speed
        self.triangle.move(self.direction * self.speed)

    def get_next_position(self):
        return self.x + self.direction.x * self.speed, \
            self.y + self.direction.y * self.speed

    def direct(self, mouse_x, mouse_y):
        self.direction = Vector(mouse_x - self.x, mouse_y - self.y)
        self.direction = self.direction.normalize()

    def take_action(self, camera):
        self.last_update = time.get_ticks()
        self.mouse_position = camera.reverse_apply(mouse.get_pos())
        self.direct(self.mouse_position[0], self.mouse_position[1])
        self.should_fly = True

    def update(self):
        timer = time.get_ticks() - self.last_update + 1
        self.last_update += timer
        if self.should_fly:
            self.move(timer)
            self.rotate(timer)
            self.collides(self.world)
        return self.should_fly

    def draw(self, surface, camera=0):
        if camera != 0:
            self.triangle.display_avatar(surface, camera)
        else:
            return

    def collide_saw(self, saw):
        rope = Line(Point(saw.x, saw.y),
                    Point(saw.collision_circle.position.x,
                          saw.collision_circle.position.y))
        next_position = self.get_next_position()
        path = Line(Point(self.x, self.y),
                    Point(next_position[0], next_position[1]))
        intersection = Line.get_intersection(rope, path)
        return bool(intersection)

    def collides(self, world):
        for obstacle in world:
            if self.triangle.check_if_collide(obstacle.rect)[0]:
                self.should_fly = False
                break
        for saw in self.saws:
            if not saw.is_severed and self.collide_saw(saw):
                saw.deploy()

    def reposition(self, coordinates, orientation):
        self.x, self.y = coordinates
        self.triangle.move(Vector(coordinates) - self.triangle.position)
        self.triangle.direction = orientation.normalize()

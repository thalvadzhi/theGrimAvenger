from pygame.math import Vector2 as Vector


def seperate_point(static, to_move, length):
    seperation_vector = to_move - static
    if int(seperation_vector.length() * 100) == int(length * 100):
        return to_move
    seperation_vector = seperation_vector.normalize()
    return static + seperation_vector * length

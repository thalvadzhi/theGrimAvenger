from pygame.math import Vector2 as Vector


def seperate_point(static, to_move, length):
    seperation_vector = to_move - static
    seperation_vector = seperation_vector.scale_to_length(length)
    return static + seperation_vector

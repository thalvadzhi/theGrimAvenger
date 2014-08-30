def get_hitmask(object, alpha):
    mask = []
    for x in range(object.rect.width_m):
        mask.append([])
        for y in range(object.rect.height_m):
            mask[x].append(not object.image.get_at((x, y))[3] == alpha)
    return mask


def collide(sprite_a, sprite_b):
    #if the two rects don't overlap return false

    section_rect = sprite_a.rect.intersect(sprite_b.rect)
    hitmask_a = sprite_a.mask
    hitmask_b = sprite_b.mask

    if section_rect.width_m == 0 or section_rect.height_m == 0:
        return False

    collision_x_a, collision_y_a = int(section_rect.x) - int(sprite_a.rect.x), int(section_rect.y) - int(sprite_a.rect.y)
    collision_x_b, collision_y_b = int(section_rect.x) - int(sprite_b.rect.x), int(section_rect.y) - int(sprite_b.rect.y)

    for x in range(int(section_rect.width_m)):
        for y in range(int(section_rect.height_m)):
            if hitmask_a[collision_x_a + x][collision_y_a + y] and hitmask_b[collision_x_b + x][collision_y_b + y]:
                return True
    return False


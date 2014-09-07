def get_hitmask(rect, image, alpha):
    mask = []
    for x in range(rect.width):
        mask.append([])
        for y in range(rect.height):
            mask[x].append(not image.get_at((x, y))[3] == alpha)
    return mask


def collide(sprite_a, sprite_b):
    '''
    both sprites should have rects and hitmasks
    '''
    #if the two rects don't overlap return false
    section_rect = sprite_a.rect.intersect(sprite_b.rect)
    hitmask_a = sprite_a.hitmask
    hitmask_b = sprite_b.hitmask
    #print(section_rect.width, section_rect.height)
    if section_rect.width == 0 or section_rect.height == 0:
        return False
    collision_x_a = int(section_rect.x) - int(sprite_a.rect.x)
    collision_y_a = int(section_rect.y) - int(sprite_a.rect.y)
    collision_x_b = int(section_rect.x) - int(sprite_b.rect.x)
    collision_y_b = int(section_rect.y) - int(sprite_b.rect.y)
    for x in range(int(section_rect.width)):
        for y in range(int(section_rect.height)):
            if hitmask_a[collision_x_a + x][collision_y_a + y] and hitmask_b[collision_x_b + x][collision_y_b + y]:
                return True
    return False

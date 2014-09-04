def get_hitmask(rect, image, alpha):
    mask = []
    for x in range(rect.width_m):
        mask.append([])
        for y in range(rect.height_m):
            mask[x].append(not image.get_at((x, y))[3] == alpha)
    return mask


def collide(rect1, hitmask1, rect2, hitmask2):
    #if the two rects don't overlap return false
    section_rect = rect1.intersect(rect2)
    hitmask_a = hitmask1
    hitmask_b = hitmask2
    if section_rect.width_m == 0 or section_rect.height_m == 0:
        return False
    collision_x_a = int(section_rect.x) - int(rect1.x)
    collision_y_a = int(section_rect.y) - int(rect1.y)
    collision_x_b = int(section_rect.x) - int(rect2.x)
    collision_y_b = int(section_rect.y) - int(rect2.y)

    for x in range(int(section_rect.width_m)):
        for y in range(int(section_rect.height_m)):
            if hitmask_a[collision_x_a + x][collision_y_a + y] and \
                    hitmask_b[collision_x_b + x][collision_y_b + y]:
                return True
    return False

# Copyright 2006 DR0ID <dr0id@bluewin.ch> http://mypage.bluewin.ch/DR0ID
#
#
#
"""
Allow to draw some gradients relatively easy.
"""

__author__ = "$Author: DR0ID $"
__version__ = "$Revision: 109 $"
__date__ = "$Date: 2007-08-09 20:33:32 +0200 (Do, 09 Aug 2007) $"

import pygame
import math

BLEND_MODES_AVAILABLE = False
vernum = pygame.vernum
if vernum[0] >= 1 and vernum[1] >= 8:
    BLEND_MODES_AVAILABLE = True


class ColorInterpolator(object):

    """
    ColorInterpolator(distance, color1, color2, rfunc, gfunc, bfunc, afunc)

    interpolates a color over the distance using different functions for
    r,g,b,a separately (a= alpha).
    """

    def __init__(self, distance, color1, color2, rfunc, gfunc, bfunc, afunc):
        object.__init__(self)

        self.r_interpolator = FunctionInterpolator(color1[0], color2[0],
                                                   distance, rfunc)
        self.g_interpolator = FunctionInterpolator(color1[1], color2[1],
                                                   distance, gfunc)
        self.b_interpolator = FunctionInterpolator(color1[2], color2[2],
                                                   distance, bfunc)
        if len(color1) == 4 and len(color2) == 4:
            self.a_interpolator = FunctionInterpolator(color1[3], color2[3],
                                                       distance, afunc)
        else:
            self.a_interpolator = FunctionInterpolator(255, 255,
                                                       distance, afunc)

    def eval(self, x):
        """
        returns the color at the position 0<=x<=d (actually not bound to this
        interval).
        """
        return [self.r_interpolator.eval(x),
                self.g_interpolator.eval(x),
                self.b_interpolator.eval(x),
                self.a_interpolator.eval(x)]


class FunctionInterpolator(object):

    """
    FunctionINterpolator(startvalue, endvalue, trange, func)
    interpolates a function y=f(x) in the range trange with
    startvalue = f(0)
    endvalue   = f(trange)
    using the function func
    """

    def __init__(self, startvalue, endvalue, trange, func):
        object.__init__(self)
        # function
        self.func = func
        # y-scaling
        self.a = endvalue - startvalue
        if self.a == 0:
            self.a = 1.
        # x-scaling
        if trange != 0:
            self.b = 1. / abs(trange)
        else:
            self.b = 1.
        # x-displacement
        self.c = 0
        # y-displacement
        self.d = min(max(startvalue, 0), 255)

    def eval(self, x):
        """
        eval(x)->float

        return value at position x
        """
        # make sure that the returned value is in [0,255]
        return int(min(max(self.a * self.func(self.b *
                                              (x + self.c)) + self.d, 0), 255))


def vertical(size, startcolor, endcolor):
    """
    Draws a vertical linear gradient filling the entire surface. Returns a
    surface filled with the gradient (numeric is only 2-3 times faster).
    """
    height = size[1]
    bigSurf = pygame.Surface((1, height)).convert_alpha()
    dd = 1.0 / height
    sr, sg, sb, sa = startcolor
    er, eg, eb, ea = endcolor
    rm = (er - sr) * dd
    gm = (eg - sg) * dd
    bm = (eb - sb) * dd
    am = (ea - sa) * dd
    for y in range(height):
        bigSurf.set_at((0, y), (int(sr + rm * y), int(sg + gm * y),
                                int(sb + bm * y), int(sa + am * y)))
    return pygame.transform.scale(bigSurf, size)


def horizontal(size, startcolor, endcolor):
    """
    Draws a horizontal linear gradient filling the entire surface. Returns a
    surface filled with the gradient (numeric is only 2-3 times faster).
    """
    width = size[0]
    bigSurf = pygame.Surface((width, 1)).convert_alpha()
    dd = 1.0 / width
    sr, sg, sb, sa = startcolor
    er, eg, eb, ea = endcolor
    rm = (er - sr) * dd
    gm = (eg - sg) * dd
    bm = (eb - sb) * dd
    am = (ea - sa) * dd
    for y in range(width):
        bigSurf.set_at((y, 0),
                       (int(sr + rm * y),
                        int(sg + gm * y),
                        int(sb + bm * y),
                        int(sa + am * y))
                       )
    return pygame.transform.scale(bigSurf, size)


def radial(radius, startcolor, endcolor):
    """
    Draws a linear raidal gradient on a square sized surface and returns
    that surface.
    """
    bigSurf = pygame.Surface(
        (2 * radius,
         2 * radius),
        pygame.HWSURFACE)  # .convert_alpha()
    bigSurf.fill((0, 0, 0, 0))
    dd = -1.0 / radius
    sr, sg, sb, sa = endcolor
    er, eg, eb, ea = startcolor
    rm = (er - sr) * dd
    gm = (eg - sg) * dd
    bm = (eb - sb) * dd
    am = (ea - sa) * dd

    draw_circle = pygame.draw.circle
    for rad in range(radius, 0, -1):
        draw_circle(bigSurf, (er + int(rm * rad),
                              eg + int(gm * rad),
                              eb + int(bm * rad),
                              ea + int(am * rad)), (radius, radius), rad)
    return bigSurf


def squared(width, startcolor, endcolor):
    """
    Draws a linear sqared gradient on a square sized surface and returns
    that surface.
    """
    bigSurf = pygame.Surface((width, width)).convert_alpha()
    bigSurf.fill((0, 0, 0, 0))
    dd = -1.0 / (width / 2)
    sr, sg, sb, sa = endcolor
    er, eg, eb, ea = startcolor
    rm = (er - sr) * dd
    gm = (eg - sg) * dd
    bm = (eb - sb) * dd
    am = (ea - sa) * dd

    draw_rect = pygame.draw.rect
    for currentw in range((width // 2), 0, -1):
        pos = (width / 2) - currentw
        draw_rect(bigSurf,
                  (er + int(rm * currentw),
                   eg + int(gm * currentw),
                      eb + int(bm * currentw),
                      ea + int(am * currentw)),
                  pygame.Rect(pos,
                              pos,
                              2 * currentw,
                              2 * currentw))
    return bigSurf


def vertical_func(
    size, startcolor, endcolor, Rfunc=(
        lambda x: x), Gfunc = (
            lambda x: x), Bfunc = (
                lambda x: x), Afunc = (
                    lambda x: 1)):
    """
    Draws a vertical linear gradient filling the entire surface. Returns a
    surface filled with the gradient (numeric is only 2x faster).
    Rfunc, Gfunc, Bfunc and Afunc are function like y = f(x). They define
    how the color changes.
    """
    height = size[1]
    bigSurf = pygame.Surface((1, height)).convert_alpha()
    color = ColorInterpolator(
        height,
        startcolor,
        endcolor,
        Rfunc,
        Gfunc,
        Bfunc,
        Afunc)
    for y in range(0, height):
        bigSurf.set_at((0, y), color.eval(y + 0.1))
    return pygame.transform.scale(bigSurf, size)


def horizontal_func(
    size, startcolor, endcolor, Rfunc=(
        lambda x: x), Gfunc = (
            lambda x: x), Bfunc = (
                lambda x: x), Afunc = (
                    lambda x: 1)):
    """
    Draws a horizontal linear gradient filling the entire surface. Returns a
    surface filled with the gradient (numeric is only 2x faster).
    Rfunc, Gfunc, Bfunc and Afunc are function like y = f(x). They define
    how the color changes.
    """
    width = size[0]
    bigSurf = pygame.Surface((width, 1)).convert_alpha()
    color = ColorInterpolator(
        width,
        startcolor,
        endcolor,
        Rfunc,
        Gfunc,
        Bfunc,
        Afunc)
    for y in range(0, width):
        bigSurf.set_at((y, 0), color.eval(y + 0.1))
    return pygame.transform.scale(bigSurf, size)


def radial_func(
    radius, startcolor, endcolor, Rfunc=(
        lambda x: x), Gfunc = (
            lambda x: x), Bfunc = (
                lambda x: x), Afunc = (
                    lambda x: 1), colorkey=(
                        0, 0, 0, 0)):
    """
    Draws a linear raidal gradient on a square sized surface and returns
    that surface.
    """
    bigSurf = pygame.Surface((2 * radius, 2 * radius)).convert_alpha()
    if len(colorkey) == 3:
        colorkey += (0,)
    bigSurf.fill(colorkey)
    color = ColorInterpolator(
        radius,
        startcolor,
        endcolor,
        Rfunc,
        Gfunc,
        Bfunc,
        Afunc)
    draw_circle = pygame.draw.circle
    for rad in range(radius, 0, -1):
        draw_circle(bigSurf, color.eval(rad), (radius, radius), rad)
    return bigSurf


def radial_func_offset(
    radius, startcolor, endcolor, Rfunc=(
        lambda x: x), Gfunc = (
            lambda x: x), Bfunc = (
                lambda x: x), Afunc = (
                    lambda x: 1), colorkey=(
                        0, 0, 0, 0), offset=(
                            0, 0)):
    """
    Draws a linear raidal gradient on a square sized surface and returns
    that surface.
    offset is the amount the center of the gradient is displaced of the center
    of the image.
    Unfotunately this function ignores alpha.
    """
    bigSurf = pygame.Surface((2 * radius, 2 * radius))  # .convert_alpha()

    mask = pygame.Surface(
        (2 * radius,
         2 * radius),
        pygame.SRCALPHA)  # .convert_alpha()
    mask.fill(colorkey)
    mask.set_colorkey((255, 0, 255))
    pygame.draw.circle(mask, (255, 0, 255), (radius, radius), radius)

    if len(colorkey) == 3:
        colorkey += (0,)
    bigSurf.fill(colorkey)

    color = ColorInterpolator(
        radius,
        startcolor,
        endcolor,
        Rfunc,
        Gfunc,
        Bfunc,
        Afunc)
    draw_circle = pygame.draw.circle
    radi = radius + int(math.hypot(offset[0], offset[1]) + 1)
    for rad in range(radi, 0, -1):
        draw_circle(
            bigSurf,
            color.eval(rad),
            (radius +
             offset[0],
                radius +
                offset[1]),
            rad)

    bigSurf.blit(mask, (0, 0))
    bigSurf.set_colorkey(colorkey)
    return bigSurf


def squared_func(
    width, startcolor, endcolor, Rfunc=(
        lambda x: x), Gfunc = (
            lambda x: x), Bfunc = (
                lambda x: x), Afunc = (
                    lambda x: 1), offset=(
                        0, 0)):
    """
    Draws a linear sqared gradient on a square sized surface and returns
    that surface.
    """
    bigSurf = pygame.Surface((width, width)).convert_alpha()
    bigSurf.fill((0, 0, 0, 0))
    color = ColorInterpolator(
        width / 2,
        startcolor,
        endcolor,
        Rfunc,
        Gfunc,
        Bfunc,
        Afunc)
    draw_rect = pygame.draw.rect
    widthh = width + 2 * int(max(abs(offset[0]), abs(offset[1])))
    for currentw in range((widthh // 2), 0, -1):
        # pos = (width/2)-currentw
        rect = pygame.Rect(0, 0, 2 * currentw, 2 * currentw)
        rect.center = (width / 2 + offset[0], width / 2 + offset[1])
        draw_rect(bigSurf, color.eval(currentw), rect)
    return bigSurf


def draw_gradient(
    surface, startpoint, endpoint, startcolor, endcolor, Rfunc=(
        lambda x: x), Gfunc = (
            lambda x: x), Bfunc = (
                lambda x: x), Afunc = (
                    lambda x: 1), mode=0):
    """
    Instead of returning an Surface, this function draw it directy onto the
    given Surface and returns the rect.
    """
    dx = endpoint[0] - startpoint[0]
    dy = endpoint[1] - startpoint[1]
    d = int(round(math.hypot(dx, dy)))
    angle = math.degrees(math.atan2(dy, dx))

    h = int(2. * math.hypot(*surface.get_size()))

    bigSurf = horizontal_func(
        (d,
         h),
        startcolor,
        endcolor,
        Rfunc,
        Gfunc,
        Bfunc,
        Afunc)

# bigSurf = pygame.transform.rotate(bigSurf, -angle) #rotozoom(bigSurf,
# -angle, 1)
    bigSurf = pygame.transform.rotozoom(bigSurf, -angle, 1)
#    bigSurf.set_colorkey((0,0,0, 0))
    rect = bigSurf.get_rect()
    srect = pygame.Rect(rect)
    dx = d / 2. * math.cos(math.radians(angle))
    dy = d / 2. * math.sin(math.radians(angle))
    rect.center = startpoint
    rect.move_ip(dx, dy)
    if BLEND_MODES_AVAILABLE:
        return surface.blit(bigSurf, rect, None, mode)
    else:
        return surface.blit(bigSurf, rect)


def draw_circle(
    surface, startpoint, endpoint, startcolor, endcolor, Rfunc=(
        lambda x: x), Gfunc = (
            lambda x: x), Bfunc = (
                lambda x: x), Afunc = (
                    lambda x: 1), mode=0):
    """
    Instead of returning an Surface, this function draw it directy onto the
    given Surface and returns the rect.
    """
    dx = endpoint[0] - startpoint[0]
    dy = endpoint[1] - startpoint[1]
    radius = int(round(math.hypot(dx, dy)))
    pos = (startpoint[0] - radius, startpoint[1] - radius)
    if BLEND_MODES_AVAILABLE:
        return surface.blit(
            radial_func(
                radius,
                startcolor,
                endcolor,
                Rfunc,
                Gfunc,
                Bfunc,
                Afunc),
            pos,
            None,
            mode)
    else:
        return surface.blit(
            radial_func(
                radius,
                startcolor,
                endcolor,
                Rfunc,
                Gfunc,
                Bfunc,
                Afunc),
            pos)


def draw_squared(
    surface, startpoint, endpoint, startcolor, endcolor, Rfunc=(
        lambda x: x), Gfunc = (
            lambda x: x), Bfunc = (
                lambda x: x), Afunc = (
                    lambda x: 1), mode=0):
    """
    Instead of returning an Surface, this function draw it directy onto the
    given Surface and returns the rect.
    """
    dx = endpoint[0] - startpoint[0]
    dy = endpoint[1] - startpoint[1]
    angle = math.degrees(math.atan2(dy, dx))
    width = 2 * int(round(math.hypot(dx, dy)))

    bigSurf = squared_func(
        width,
        startcolor,
        endcolor,
        Rfunc,
        Gfunc,
        Bfunc,
        Afunc)

    bigSurf = pygame.transform.rotozoom(bigSurf, -angle, 1)
#    bigSurf.set_colorkey((0,0,0, 0))
    rect = bigSurf.get_rect()
    rect.center = startpoint
    if BLEND_MODES_AVAILABLE:
        return surface.blit(bigSurf, rect, None, mode)
    else:
        return surface.blit(bigSurf, rect)


def chart(
    startpoint, endpoint, startcolor, endcolor, Rfunc=(
        lambda x: x), Gfunc = (
            lambda x: x), Bfunc = (
                lambda x: x), Afunc = (
                    lambda x: 1), scale=None):
    """
    This returns a Surface where the change of the colors over the distance
    (the width of the image) is showen as a line.
    scale: a float, 1 is not scaling
    """
    dx = endpoint[0] - startpoint[0]
    dy = endpoint[1] - startpoint[1]
    distance = int(round(math.hypot(dx, dy)))
    color = ColorInterpolator(
        distance,
        startcolor,
        endcolor,
        Rfunc,
        Gfunc,
        Bfunc,
        Afunc)
    bigSurf = pygame.Surface((distance, 256))
    bigSurf.fill((0,) * 3)
    oldcol = color.eval(0)
    for x in range(distance):
        r, g, b, a = color.eval(x)
        pygame.draw.line(bigSurf, (255, 0, 0, 128), (x - 1, oldcol[0]), (x, r))
        pygame.draw.line(bigSurf, (0, 255, 0, 128), (x - 1, oldcol[1]), (x, g))
        pygame.draw.line(bigSurf, (0, 0, 255, 128), (x - 1, oldcol[2]), (x, b))
        pygame.draw.line(
            bigSurf, (255, 255, 255, 128), (x - 1, oldcol[3]), (x, a))
        oldcol = (r, g, b, a)
    if scale:
        # return pygame.transform.scale(bigSurf, size)
        return pygame.transform.rotozoom(bigSurf, 0, scale)
    return pygame.transform.flip(bigSurf, 0, 1)
# -----------------------------------------------------------------------------


def genericFxyGradient(
        surf,
        clip,
        color1,
        color2,
        func,
        intx,
        yint,
        zint=None):
    """
    genericFxyGradient(size, color1, color2,func, intx, yint, zint=None)

    some sort of highfield drawer :-)

    surf   : surface to draw
    clip   : rect on surf to draw in
    color1 : start color
    color2 : end color
    func   : function z = func(x,y)
    xint   : interval in x direction where the function is evaluated
    yint   : interval in y direction where the function is evaluated
    zint   : if not none same as yint or xint, if None then the max and min
     value of func is taken as z-interval

    color = a*func(b*(x+c), d*(y+e))+f
    """
    # make shure that x1<x2 and y1<y2 and z1<z2
    w, h = clip.size
    x1 = min(intx)
    x2 = max(intx)
    y1 = min(yint)
    y2 = max(yint)
    if zint:  # if user give us z intervall, then use it
        z1 = min(zint)
        z2 = max(zint)
    else:  # look for extrema of function (not best algorithme)
        z1 = func(x1, y1)
        z2 = z1
        for i in range(w):
            for j in range(h):
                r = func(i, j)
                z1 = min(z1, r)
                z2 = max(z2, r)

    x1 = float(x1)
    x2 = float(x2)
    y1 = float(y1)
    y2 = float(y2)
    z1 = float(z1)
    z2 = float(z2)
    if len(color1) == 3:
        color1 = list(color1)
        color1.append(255)
    if len(color2) == 3:
        color2 = list(color2)
        color2.append(255)

    # calculate streching and displacement variables
    a = ((color2[0] - color1[0]) / (z2 - z1),
         (color2[1] - color1[1]) / (z2 - z1),
         (color2[2] - color1[2]) / (z2 - z1),
         (color2[3] - color1[3]) / (z2 - z1))  # streching in z direction
    b = (x2 - x1) / float(w)  # streching in x direction
    d = (y2 - y1) / float(h)  # streching in y direction
    f = (color1[0] - a[0] * z1,
         color1[1] - a[1] * z1,
         color1[2] - a[2] * z1,
         color1[3] - a[3] * z1)  # z displacement
    c = x1 / b
    e = y1 / d

    surff = pygame.surface.Surface((w, h)).convert_alpha()
    # generate values
    for i in range(h):
        for j in range(w):
            val = func(b * (j + c), d * (i + e))
            # clip color
            color = (max(min(a[0] * val + f[0], 255), 0),
                     max(min(a[1] * val + f[1], 255), 0),
                     max(min(a[2] * val + f[2], 255), 0),
                     max(min(a[3] * val + f[3], 255), 0))
            surff.set_at((j, i), color)
    surf.blit(surff, clip)

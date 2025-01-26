import pygame
from pygame import *

pygame.init()

def DrawRoundedRect(surface, rect, color, radiustopleft=0, radiustopright=0, radiusbottomleft=0, radiusbottomright=0, width=0):
    rect = Rect(rect)
    color = Color(*color)
    alpha = color.a
    color.a = 0
    pos = rect.topleft
    rect.topleft = 0, 0
    rectangle = Surface(rect.size, SRCALPHA)

    # draw 4 circles that act as rounded corners
    if radiustopleft > 0:
        circle = Surface([min(rect.size) * 3] * 2, SRCALPHA)
        draw.ellipse(circle, (0, 0, 0), circle.get_rect(), int(width/radiustopleft)*3)
        circle = transform.smoothscale(circle, [radiustopleft] * 2)
        c1 = rectangle.blit(circle, (rect.topleft[0], rect.topleft[1]))
    else:
        c1 = Rect((0,0,0,0))
        c1.topleft = rect.topleft

    if radiustopright > 0:
        circle = Surface([min(rect.size) * 3] * 2, SRCALPHA)
        draw.ellipse(circle, (0, 0, 0), circle.get_rect(), int(width/radiustopright)*3)
        circle = transform.smoothscale(circle,  [radiustopright] * 2)
        c2 = rectangle.blit(circle, (rect.topright[0]-circle.get_rect().w, rect.topright[1]))
    else:
        c2 = Rect((0, 0, 0, 0))
        c2.topright = rect.topright

    if radiusbottomleft > 0:
        circle = Surface([min(rect.size) * 3] * 2, SRCALPHA)
        draw.ellipse(circle, (0, 0, 0), circle.get_rect(), int(width/radiusbottomleft))
        circle = transform.smoothscale(circle, [radiusbottomleft] * 2)
        c3 = rectangle.blit(circle, (rect.bottomleft[0], rect.bottomleft[1] -circle.get_rect().h))
    else:
        c3 = Rect((0, 0, 0, 0))
        c3.bottomleft = rect.bottomleft

    if radiusbottomright > 0:
        circle = Surface([min(rect.size) * 3] * 2, SRCALPHA)
        draw.ellipse(circle, (0, 0, 0), circle.get_rect(), int(width/radiusbottomright))
        circle = transform.smoothscale(circle, [radiusbottomright] * 2)
        c4 = rectangle.blit(circle, (rect.bottomright[0]-circle.get_rect().w, rect.bottomright[1]-circle.get_rect().w))
    else:
        c4 = Rect((0, 0, 0, 0))
        c4.bottomright = rect.bottomright

    # draw 4 rectangles that connect the circles, making edges
    # this is stupid
    draw.rect(rectangle, (0,0,0), (c1.center[0], 0, c2.center[0]-c1.center[0], max(c1.h, c2.h)), width)
    draw.rect(rectangle, (0,0,0), (0, c1.center[1], max(c1.h, c3.h),c3.center[1]-c1.center[1]), width)
    draw.rect(rectangle, (0,0,0), (c3.center[0], min(rect.h-c3.h, rect.h-c4.h), c4.center[0] - c3.center[0], max(c3.h, c4.h)), width)
    draw.rect(rectangle, (0, 0, 0), (min(c2.center[0], c4.center[0]),c2.center[1], max(rect.w-c2.center[0], rect.w-c4.center[0]), c4.center[1]-c2.center[1]), width)

    # fill the gap in the middle
    draw.rect(rectangle, (0,0,0), (max(c1.center[0], c3.center[0]), max(c1.center[1], c2.center[1]), min(c2.center[0], c4.center[0]) - max(c1.center[0], c3.center[0]), min(c3.center[1], c4.center[1])), width)

    # fill with color
    rectangle.fill(color, special_flags=BLEND_RGBA_MAX)
    rectangle.fill((255, 255, 255, alpha), special_flags=BLEND_RGBA_MIN)

    surface.blit(rectangle, pos)

    return Rect(pos[0], pos[1], rect.width, rect.height), rectangle


def DrawText(surface, text, fnt, rect, color, anchor="topleft", shadowRect=(0,0), shadowAlpha=100):
    # draw the shadow under text
    if shadowRect != (0,0):
        text_surface = fnt.render(text, True, color)
        text_surface.set_alpha(shadowAlpha)
        r = text_surface.get_rect()
        surface.blit(text_surface, (r.topleft[0]-r.__getattribute__(anchor)[0]+rect[0]+shadowRect[0], r.topleft[1]-r.__getattribute__(anchor)[1]+rect[1]+shadowRect[1]))

    text_surface = fnt.render(text, True, color)
    r = text_surface.get_rect()
    surface.blit(text_surface, (r.topleft[0]-r.__getattribute__(anchor)[0]+rect[0], r.topleft[1]-r.__getattribute__(anchor)[1]+rect[1]))


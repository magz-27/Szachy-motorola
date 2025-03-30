import math as pymath

import pygame
from pygame import *

pygame.init()
mouseDown = False
mouseUp = False
mousePressed = False
mousePos = (0,0)
useHandCursor = False
isSoundOn = True


soundButton = pygame.mixer.Sound("sounds/sound_button_click.mp3")
soundMoveWhite = pygame.mixer.Sound("sounds/sound_move1.mp3")
soundMoveBlack = pygame.mixer.Sound("sounds/sound_move2.mp3")
soundCapture = pygame.mixer.Sound("sounds/sound_capture.mp3")
soundCheck = pygame.mixer.Sound("sounds/sound_check.mp3")
soundCheckMate = pygame.mixer.Sound("sounds/sound_checkmate.mp3")

iconSoundOn = pygame.image.load("graphics/icon_sound_on.png")
iconSoundOff = pygame.image.load("graphics/icon_sound_off.png")

framesPassed = 0


def drawRoundedRect(surface, rect, color, radiustopleft=0, radiustopright=0, radiusbottomleft=0, radiusbottomright=0, width=0):
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


def drawText(surface, text, fnt, rect, color, anchor="topleft", shadowRect=(2, 2), shadowAlpha=66):
    # draw the shadow under text
    if shadowRect != (0,0):
        text_surface = fnt.render(text, True, color)
        text_surface.set_alpha(shadowAlpha)
        r = text_surface.get_rect()
        surface.blit(text_surface, (r.topleft[0]-r.__getattribute__(anchor)[0]+rect[0]+shadowRect[0], r.topleft[1]-r.__getattribute__(anchor)[1]+rect[1]+shadowRect[1]))

    text_surface = fnt.render(text, True, color)
    r = text_surface.get_rect()
    surface.blit(text_surface, (r.topleft[0]-r.__getattribute__(anchor)[0]+rect[0], r.topleft[1]-r.__getattribute__(anchor)[1]+rect[1]))


currentButtons = []
currentToggleButtons = []


def clearButtons():
    global currentButtons, currentToggleButtons
    currentButtons = []
    currentToggleButtons = []


def SineRect(rect, secondsPassed, sineAmplitude, sineSpeed):
    return (rect[0], rect[1]+pymath.sin(secondsPassed*sineSpeed) *sineAmplitude)


class Button:
    hover = False
    clicked = False

    def __init__(self, surface, rect: pygame.Rect, onClick=None):
        global currentButtons, renderButtons, buttonSurface
        self.surface = surface
        self.rect = Rect(rect)
        self.onClick = onClick
        self.image = None
        self.disabled = False

        self.defaultColor = (0,0,0,0)
        self.hoverColor = (0,0,0,0)
        self.clickColor = (0,0,0,0)
        self.radius = 16

        self.text = ""
        self.font = None
        self.textColor = (255, 255, 255)
        self.textHoverColor = (255, 255, 255)
        self.textClickColor = (255, 255, 255)
        self.textShadowRect = (2, 2)
        self.shadowAlpha = 50

        currentButtons.append(self)


class ToggleButton:
    hover = False
    clicked = False

    def __init__(self, surface, rect: pygame.Rect):
        global currentButtons, renderButtons, buttonSurface
        self.surface = surface
        self.rect = Rect(rect)
        self.currentState = 0
        self.states = [""]

        self.font = None
        self.textColor = (255, 255, 255)
        self.textHoverColor = (255, 255, 255)
        self.textClickColor = (255, 255, 255)
        self.textShadowRect = (2, 2)
        self.shadowAlpha = 50

        currentToggleButtons.append(self)


def renderButtons():
    for b in currentButtons:
        b.surface.fill((0,0,0,0))
    for b in currentToggleButtons:
        b.surface.fill((0,0,0,0))

    for b in currentButtons:
        b : Button
        color = b.hoverColor if b.hover else b.defaultColor
        color = Color(b.clickColor if b.clicked and b.hover else color)

        textColor = b.textHoverColor if b.hover else b.textColor
        textColor = Color(b.textClickColor if b.clicked and b.hover else textColor)

        if color.r != 0:drawRoundedRect(b.surface, (b.rect[0], b.rect[1], b.rect[2], b.rect[3]), color, b.radius, b.radius, b.radius, b.radius)
        if b.font != None: drawText(b.surface, b.text, b.font, (b.rect[0]+b.rect[2]/2, b.rect[1]+b.rect[3]/2, b.rect[2], b.rect[3]), textColor, "center" , b.textShadowRect, b.shadowAlpha)
        if b.image != None:
            img = b.surface.blit(b.image, (b.rect[0], b.rect[1]))
            b.surface.fill(textColor, img, special_flags=BLEND_RGB_ADD)
            if b.disabled: b.surface.fill((0,0,0,175), img, special_flags=BLEND_RGBA_SUB)

    for b in currentToggleButtons:
        b: ToggleButton
        textColor = b.textHoverColor if b.hover else b.textColor
        textColor = Color(b.textClickColor if b.clicked and b.hover else textColor)


        if b.font != None:
            drawText(b.surface, b.states[b.currentState], b.font, (b.rect[0] + b.rect[2] / 2, b.rect[1] + b.rect[3] / 2, b.rect[2], b.rect[3]),textColor, "center", b.textShadowRect, b.shadowAlpha)


def handleButtonLogic():
    global mousePos, mousePressed, mouseDown, mouseUp, currentButtons, useHandCursor

    for b in currentButtons:
        if b.rect.collidepoint(mousePos):
            if b.disabled: return
            h = b.hover
            b.hover = True
            useHandCursor = True
            if not h:
                renderButtons()
            if mousePressed:
                b.clicked = True
            else:
                b.clicked = False
            if mouseDown:
                playSound(soundButton)
                b.onClick()
                mouseDown = False
                renderButtons()
            if mouseUp:
                renderButtons()
        else:
            h = b.hover
            b.hover = False
            if h:
                renderButtons()

    for b in currentToggleButtons:
        if b.rect.collidepoint(mousePos):
            h = b.hover
            b.hover = True
            useHandCursor = True
            if not h:
                renderButtons()
            if mousePressed:
                b.clicked = True
            else:
                b.clicked = False
            if mouseDown:
                playSound(soundButton)
                b.currentState = (b.currentState + 1) % len(b.states)
                renderButtons()
            if mouseUp:
                renderButtons()
        else:
            h = b.hover
            b.hover = False
            if h:
                renderButtons()

    return useHandCursor


def handleMouseLogic():
    # mousePressed is true if mouse button is currently pressed
    # mouseClick is true for a single frame when mouse is clicked
    global mouseDown, mouseUp, mousePressed

    if pygame.mouse.get_pressed()[0]:
        if mousePressed:
            mouseDown = False
        else:
            mouseDown = True
        mousePressed = True
        mouseUp = False
    else:
        if mousePressed:
            mouseUp = True
        else:
            mouseUp = False
        mousePressed = False
        mouseDown = False
    return mouseDown, mouseUp, mousePressed

def clickSound(btn):
    global isSoundOn
    isSoundOn = not isSoundOn
    if isSoundOn:
        btn.image = iconSoundOn
    else:
        btn.image = iconSoundOff


def playSound(sound, volume = 1):
    if not isSoundOn: return
    sound.set_volume(volume)
    sound.play()


def update():
    global mouseDown, mouseUp, mousePressed, mousePos, useHandCursor, framesPassed
    mousePos = pygame.mouse.get_pos()

    handleButtonLogic()
    framesPassed += 1
    if useHandCursor: pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else: pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


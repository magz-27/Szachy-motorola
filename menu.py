import sys

import pygame
from pygame.locals import *
import util

logo = pygame.image.load("graphics/logo.png")


class Menu:

    def __init__(self, screen):
        self.screen = screen
        self.fnt56 = pygame.font.Font("font.otf", 56)
        self.fnt48 = pygame.font.Font("font.otf", 48)
        self.fnt36 = pygame.font.Font("font.otf", 36)
        self.fnt32 = pygame.font.Font("font.otf", 32)
        self.color_gray = (74, 73, 71)
        self.color_hover = (96, 94, 90)
        self.color_click = (128, 124, 118)
        self.color_white = (255, 255, 255)
        self.selected_option = None
        self.secondsPassed = 0
        self.buttonSurface = pygame.Surface((self.screen.get_width(), self.screen.get_height()), SRCALPHA)
        self.logoSurface = pygame.Surface((self.screen.get_width(), self.screen.get_height()), SRCALPHA)

        self.running = True

        self.lengthBtn = None
        self.notationBtn = None
        self.algorithmBtn = None
        self.difficultyBtn = None

        self.gameMode = "computer"
        self.gameLength = False
        self.notationType = ""
        self.algorithm = "minimax"
        self.difficulty = 1


        def pressButton(option):
            if self.lengthBtn:
                self.gameLength = [False, True][self.lengthBtn.currentState]

            if self.notationBtn:
                self.notationType = [False, True][self.notationBtn.currentState]

            if self.algorithmBtn:
                self.algorithm = ["minimax", "montecarlo"][self.algorithmBtn.currentState]

            if self.difficultyBtn:
                self.difficulty = [1, 2, 3][self.difficultyBtn.currentState]

            if option == "quit":
                pygame.quit()
                sys.exit()

            self.gameMode = option
            self.running = False

        def initComputerMenu():
            util.clearButtons()
            self.soundBtn = util.Button(self.buttonSurface, Rect(830, 15, 48, 48), lambda: util.clickSound(self.soundBtn))
            if util.isSoundOn:
                self.soundBtn.image = util.iconSoundOn
            else:
                self.soundBtn.image = util.iconSoundOff
            self.soundBtn.textColor, self.soundBtn.textHoverColor, self.soundBtn.textClickColor = (0, 0, 0), (40, 40, 40), (80, 80, 80)

            self.lengthBtn = util.ToggleButton(self.buttonSurface, Rect(300, 345, 300, 40))
            self.lengthBtn.states, self.lengthBtn.font = ["Czas gry: Zwykly", "Czas gry: Blyskawiczny"], self.fnt36
            self.lengthBtn.textShadowRect = (1,1)
            self.lengthBtn.textColor, self.lengthBtn.textHoverColor, self.lengthBtn.textClickColor = self.color_gray, (107, 105, 100), (128, 124, 118)

            self.notationBtn = util.ToggleButton(self.buttonSurface, Rect(300, 395, 300, 40))
            self.notationBtn.states, self.notationBtn.font = ["Notacja: Klasyczna", "Notacja: Dluga"], self.fnt36
            self.notationBtn.textShadowRect = (1,1)
            self.notationBtn.textColor, self.notationBtn.textHoverColor, self.notationBtn.textClickColor = self.color_gray, (107, 105, 100), (128, 124, 118)

            self.algorithmBtn = util.ToggleButton(self.buttonSurface, Rect(300, 445, 300, 40))
            self.algorithmBtn.states, self.algorithmBtn.font = ["Algorytm: MiniMax", "Algorytm: Monte Carlo"], self.fnt36
            self.algorithmBtn.textShadowRect = (1,1)
            self.algorithmBtn.textColor, self.algorithmBtn.textHoverColor, self.algorithmBtn.textClickColor = self.color_gray, (107, 105, 100), (128, 124, 118)

            self.difficultyBtn = util.ToggleButton(self.buttonSurface, Rect(300, 495, 300, 40))
            self.difficultyBtn.states, self.difficultyBtn.font = ["Poziom: Latwy", "Poziom: Sredni", "Poziom: Trudny"], self.fnt36
            self.difficultyBtn.textShadowRect = (1,1)
            self.difficultyBtn.textColor, self.difficultyBtn.textHoverColor, self.difficultyBtn.textClickColor = self.color_gray, (107, 105, 100), (128, 124, 118)

            b = util.Button(self.buttonSurface, Rect(300, 600, 300, 55), lambda: pressButton("computer"))
            b.text, b.font = "Graj", self.fnt48
            b.textColor, b.textHoverColor, b.textClickColor = self.color_gray, (107, 105, 100), (128, 124, 118)
            b.shadowAlpha = 66

        def initOnlineMenu():
            util.clearButtons()
            self.soundBtn = util.Button(self.buttonSurface, Rect(830, 15, 48, 48), lambda: util.clickSound(self.soundBtn))
            if util.isSoundOn:
                self.soundBtn.image = util.iconSoundOn
            else:
                self.soundBtn.image = util.iconSoundOff
            self.soundBtn.textColor, self.soundBtn.textHoverColor, self.soundBtn.textClickColor = (0, 0, 0), (40, 40, 40), (80, 80, 80)

            ###
            # DO ZMIANY
            ###

            self.lengthBtn = util.ToggleButton(self.buttonSurface, Rect(300, 395, 300, 40))
            self.lengthBtn.states, self.lengthBtn.font = ["Czas gry: Zwykly", "Czas gry: Blyskawiczny"], self.fnt36
            self.lengthBtn.textShadowRect = (1, 1)
            self.lengthBtn.textColor, self.lengthBtn.textHoverColor, self.lengthBtn.textClickColor = self.color_gray, (107, 105, 100), (128, 124, 118)

            self.notationBtn = util.ToggleButton(self.buttonSurface, Rect(300, 445, 300, 40))
            self.notationBtn.states, self.notationBtn.font = ["Notacja: Klasyczna", "Notacja: Dluga"], self.fnt36
            self.notationBtn.textShadowRect = (1, 1)
            self.notationBtn.textColor, self.notationBtn.textHoverColor, self.notationBtn.textClickColor = self.color_gray, (107, 105, 100), (128, 124, 118)

            b = util.Button(self.buttonSurface, Rect(300, 600, 300, 55), lambda: pressButton("online"))
            b.text, b.font = "Graj", self.fnt48
            b.textColor, b.textHoverColor, b.textClickColor = self.color_gray, (107, 105, 100), (128, 124, 118)
            b.shadowAlpha = 66

        def initPlayerMenu():
            util.clearButtons()
            self.soundBtn = util.Button(self.buttonSurface, Rect(830, 15, 48, 48), lambda: util.clickSound(self.soundBtn))
            if util.isSoundOn:
                self.soundBtn.image = util.iconSoundOn
            else:
                self.soundBtn.image = util.iconSoundOff
            self.soundBtn.textColor, self.soundBtn.textHoverColor, self.soundBtn.textClickColor = (0, 0, 0), (40, 40, 40), (80, 80, 80)

            self.lengthBtn = util.ToggleButton(self.buttonSurface, Rect(300, 395, 300, 40))
            self.lengthBtn.states, self.lengthBtn.font = ["Czas gry: Zwykly", "Czas gry: Blyskawiczny"], self.fnt36
            self.lengthBtn.textShadowRect = (1, 1)
            self.lengthBtn.textColor, self.lengthBtn.textHoverColor, self.lengthBtn.textClickColor = self.color_gray, (107, 105, 100), (128, 124, 118)

            self.notationBtn = util.ToggleButton(self.buttonSurface, Rect(300, 445, 300, 40))
            self.notationBtn.states, self.notationBtn.font = ["Notacja: Klasyczna", "Notacja: Dluga"], self.fnt36
            self.notationBtn.textShadowRect = (1, 1)
            self.notationBtn.textColor, self.notationBtn.textHoverColor, self.notationBtn.textClickColor = self.color_gray, (107, 105, 100), (128, 124, 118)

            b = util.Button(self.buttonSurface, Rect(300, 600, 300, 55), lambda: pressButton("player"))
            b.text, b.font = "Graj", self.fnt48
            b.textColor, b.textHoverColor, b.textClickColor = self.color_gray, (107, 105, 100), (128, 124, 118)
            b.shadowAlpha = 66


        self.soundBtn = util.Button(self.buttonSurface, Rect(830, 15, 48, 48), lambda: util.clickSound(self.soundBtn))
        if util.isSoundOn:
            self.soundBtn.image = util.iconSoundOn
        else:
            self.soundBtn.image = util.iconSoundOff
        self.soundBtn.textColor, self.soundBtn.textHoverColor, self.soundBtn.textClickColor = (0, 0, 0), (40, 40, 40), (80, 80, 80)

        b = util.Button(self.buttonSurface, Rect(300, 360, 300, 55), lambda: initComputerMenu())
        b.text, b.font = "Vs. Komputer", self.fnt48
        b.textColor, b.textHoverColor, b.textClickColor = self.color_gray, (107, 105, 100), (128, 124, 118)
        b.shadowAlpha = 66

        b = util.Button(self.buttonSurface, Rect(300, 420, 300, 55), lambda: initOnlineMenu())
        b.text, b.font = "Przez siec", self.fnt48
        b.textColor, b.textHoverColor, b.textClickColor = self.color_gray, (107, 105, 100), (128, 124, 118)
        b.shadowAlpha = 66

        b = util.Button(self.buttonSurface, Rect(250, 480, 400, 55), lambda: initPlayerMenu())
        b.text, b.font = "Lokalne PvP", self.fnt48
        b.textColor, b.textHoverColor, b.textClickColor = self.color_gray, (107, 105, 100), (128, 124, 118)
        b.shadowAlpha = 66

        b = util.Button(self.buttonSurface, Rect(300, 600, 300, 55), lambda: pressButton("quit"))
        b.text, b.font = "Wyjdz", self.fnt48
        b.textColor, b.textHoverColor, b.textClickColor = self.color_gray, (107, 105, 100), (128, 124, 118)
        b.shadowAlpha = 66

        util.renderButtons()

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            deltaTime = clock.tick(60) / 1000
            util.useHandCursor = False
            util.handleMouseLogic()

            self.secondsPassed += deltaTime

            for event in pygame.event.get():
                if event.type == QUIT:
                    return "quit"

            self.screen.fill((250, 247, 240))
            self.logoSurface.fill((0,0,0,0))

            self.logoSurface.blit(logo, util.SineRect((130, 96), self.secondsPassed, 4, 5))
            self.screen.blit(self.buttonSurface, (0,0))
            self.screen.blit(self.logoSurface, (0,0))

            util.update()
            pygame.display.flip()

        util.clearButtons()
        return self.gameMode, self.gameLength, self.notationType, self.algorithm, self.difficulty


def show_menu(screen):
    menu = Menu(screen)
    return menu.run()
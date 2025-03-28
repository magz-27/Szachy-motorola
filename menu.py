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

        self.state = {
            "algoritm": "minimax",
            "difficulty": "hard"
        }

        def pressButton(option):
            setState("selected_option", option)
            if option == "quit":
                pygame.quit()
                sys.exit()
            self.running = False

        def setState(key, value):
            self.state[key] = value

        def initComputerMenu():
            util.currentButtons = []

            b = util.Button(self.buttonSurface, Rect(150, 360, 300, 55), lambda: setState("algorithm", "minimax"))
            b.text, b.font = "Minimax AB", self.fnt32
            b.textColor, b.textHoverColor, b.textClickColor = self.color_gray, (107, 105, 100), (128, 124, 118)
            b.shadowAlpha = 66

            b = util.Button(self.buttonSurface, Rect(450, 360, 300, 55), lambda: setState("algorithm", "mcts"))
            b.text, b.font = "Monte Carlo Tree Search", self.fnt32
            b.textColor, b.textHoverColor, b.textClickColor = self.color_gray, (107, 105, 100), (128, 124, 118)
            b.shadowAlpha = 66

            b = util.Button(self.buttonSurface, Rect(150, 400, 300, 55), lambda: setState("difficulty", "easy"))
            b.text, b.font = "Latwy", self.fnt32
            b.textColor, b.textHoverColor, b.textClickColor = self.color_gray, (107, 105, 100), (128, 124, 118)
            b.shadowAlpha = 66

            b = util.Button(self.buttonSurface, Rect(450, 400, 300, 55), lambda: setState("difficulty", "hard"))
            b.text, b.font = "Trudny", self.fnt32
            b.textColor, b.textHoverColor, b.textClickColor = self.color_gray, (107, 105, 100), (128, 124, 118)
            b.shadowAlpha = 66

            b = util.Button(self.buttonSurface, Rect(250, 480, 400, 55), lambda: pressButton("computer"))
            b.text, b.font = "Graj", self.fnt48
            b.textColor, b.textHoverColor, b.textClickColor = self.color_gray, (107, 105, 100), (128, 124, 118)
            b.shadowAlpha = 66

        b = util.Button(self.buttonSurface, Rect(300, 360, 300, 55), lambda: initComputerMenu())
        b.text, b.font = "Vs. Komputer", self.fnt48
        b.textColor, b.textHoverColor, b.textClickColor = self.color_gray, (107, 105, 100), (128, 124, 118)
        b.shadowAlpha = 66

        b = util.Button(self.buttonSurface, Rect(300, 420, 300, 55), lambda: pressButton("online"))
        b.text, b.font = "Przez siec", self.fnt48
        b.textColor, b.textHoverColor, b.textClickColor = self.color_gray, (107, 105, 100), (128, 124, 118)
        b.shadowAlpha = 66

        b = util.Button(self.buttonSurface, Rect(250, 480, 400, 55), lambda: pressButton("player"))
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

        util.currentButtons = []
        return self.state
    
    



def show_menu(screen):
    menu = Menu(screen)
    return menu.run()
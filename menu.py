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
        self.notationType = False
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

            self.lengthBtn = util.ToggleButton(self.buttonSurface, Rect(300, 325, 300, 40))
            self.lengthBtn.states, self.lengthBtn.font = ["Czas gry: Zwykly", "Czas gry: Blyskawiczny"], self.fnt36
            self.lengthBtn.textColor, self.lengthBtn.textHoverColor, self.lengthBtn.textClickColor = self.color_gray, (107, 105, 100), (128, 124, 118)

            self.notationBtn = util.ToggleButton(self.buttonSurface, Rect(300, 375, 300, 40))
            self.notationBtn.states, self.notationBtn.font = ["Notacja: Klasyczna", "Notacja: Dluga"], self.fnt36
            self.notationBtn.textColor, self.notationBtn.textHoverColor, self.notationBtn.textClickColor = self.color_gray, (107, 105, 100), (128, 124, 118)

            self.algorithmBtn = util.ToggleButton(self.buttonSurface, Rect(300, 450, 300, 40))
            self.algorithmBtn.states, self.algorithmBtn.font = ["Algorytm: MiniMax", "Algorytm: Monte Carlo"], self.fnt36
            self.algorithmBtn.textColor, self.algorithmBtn.textHoverColor, self.algorithmBtn.textClickColor = self.color_gray, (107, 105, 100), (128, 124, 118)

            self.difficultyBtn = util.ToggleButton(self.buttonSurface, Rect(300, 500, 300, 40))
            self.difficultyBtn.states, self.difficultyBtn.font = ["Poziom: Latwy", "Poziom: Sredni", "Poziom: Trudny"], self.fnt36
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

            self.lengthBtn = util.ToggleButton(self.buttonSurface, Rect(300, 385, 300, 40))
            self.lengthBtn.states, self.lengthBtn.font = ["Czas gry: Zwykly", "Czas gry: Blyskawiczny"], self.fnt36
            self.lengthBtn.textColor, self.lengthBtn.textHoverColor, self.lengthBtn.textClickColor = self.color_gray, (107, 105, 100), (128, 124, 118)

            self.notationBtn = util.ToggleButton(self.buttonSurface, Rect(300, 435, 300, 40))
            self.notationBtn.states, self.notationBtn.font = ["Notacja: Klasyczna", "Notacja: Dluga"], self.fnt36
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

            self.lengthBtn = util.ToggleButton(self.buttonSurface, Rect(300, 385, 300, 40))
            self.lengthBtn.states, self.lengthBtn.font = ["Czas gry: Zwykly", "Czas gry: Blyskawiczny"], self.fnt36
            self.lengthBtn.textColor, self.lengthBtn.textHoverColor, self.lengthBtn.textClickColor = self.color_gray, (107, 105, 100), (128, 124, 118)

            self.notationBtn = util.ToggleButton(self.buttonSurface, Rect(300, 435, 300, 40))
            self.notationBtn.states, self.notationBtn.font = ["Notacja: Klasyczna", "Notacja: Dluga"], self.fnt36
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

        b = util.Button(self.buttonSurface, Rect(300, 350, 300, 55), lambda: initComputerMenu())
        b.text, b.font = "Vs. Komputer", self.fnt48
        b.textColor, b.textHoverColor, b.textClickColor = self.color_gray, (107, 105, 100), (128, 124, 118)
        b.shadowAlpha = 66

        b = util.Button(self.buttonSurface, Rect(300, 410, 300, 55), lambda: pressButton("online"))
        b.text, b.font = "Przez siec", self.fnt48
        b.textColor, b.textHoverColor, b.textClickColor = self.color_gray, (107, 105, 100), (128, 124, 118)
        b.shadowAlpha = 66

        b = util.Button(self.buttonSurface, Rect(250, 470, 400, 55), lambda: initPlayerMenu())
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
                    return "quit", self.gameLength, self.notationType, self.algorithm, self.difficulty

            self.screen.fill((250, 247, 240))
            self.logoSurface.fill((0,0,0,0))

            self.logoSurface.blit(logo, util.SineRect((130, 90), self.secondsPassed, 4, 5))
            self.screen.blit(self.buttonSurface, (0,0))
            self.screen.blit(self.logoSurface, (0,0))

            util.update()
            pygame.display.flip()

        util.clearButtons()
        return self.gameMode, self.gameLength, self.notationType, self.algorithm, self.difficulty


class HostMenu:
    def __init__(self, screen):
        self.screen = screen
        self.fnt56 = pygame.font.Font("font.otf", 56)
        self.fnt48 = pygame.font.Font("font.otf", 48)
        self.fnt36 = pygame.font.Font("font.otf", 36)
        self.fnt32 = pygame.font.Font("font.otf", 32)
        self.fnt24 = pygame.font.Font("font.otf", 24)
        self.color_gray = (74, 73, 71)
        self.color_hover = (96, 94, 90)
        self.color_click = (128, 124, 118)
        self.color_white = (255, 255, 255)
        self.selected_option = None
        self.ip_address = "localhost"
        self.port = "5000"
        self.ip_input_active = False
        self.port_input_active = False
        self.secondsPassed = 0
        self.buttonSurface = pygame.Surface((self.screen.get_width(), self.screen.get_height()), SRCALPHA)
        self.textSurface = pygame.Surface((self.screen.get_width(), self.screen.get_height()), SRCALPHA)
        self.inputSurface = pygame.Surface((self.screen.get_width(), self.screen.get_height()), SRCALPHA)

        self.running = True

        def pressButton(option):
            self.selected_option = option
            if option == "back":
                self.selected_option = None
            elif option == "host":
                self.selected_option = {"mode": "host", "host": "0.0.0.0", "port": int(self.port)}
            elif option == "client":
                self.selected_option = {"mode": "client", "host": self.ip_address, "port": int(self.port)}
            self.running = False

        def activate_ip_input():
            self.ip_input_active = True
            self.port_input_active = False

        def activate_port_input():
            self.port_input_active = True
            self.ip_input_active = False

        # Menu title
        util.drawText(self.textSurface, "Tryb sieciowy", self.fnt56, (450, 140), self.color_gray, "center")
        
        # IP Address input
        util.drawText(self.textSurface, "Adres IP:", self.fnt32, (300, 230), self.color_gray)
        self.ip_input_rect = pygame.Rect(420, 230, 200, 40)
        
        b = util.Button(self.buttonSurface, self.ip_input_rect, lambda: activate_ip_input())
        b.defaultColor, b.hoverColor, b.clickColor = (240, 240, 240), (230, 230, 230), (220, 220, 220)
        b.radius = 10
        
        # Port input
        util.drawText(self.textSurface, "Port:", self.fnt32, (300, 280), self.color_gray)
        self.port_input_rect = pygame.Rect(420, 280, 100, 40)
        
        b = util.Button(self.buttonSurface, self.port_input_rect, lambda: activate_port_input())
        b.defaultColor, b.hoverColor, b.clickColor = (240, 240, 240), (230, 230, 230), (220, 220, 220)
        b.radius = 10

        # Start game/return buttons
        b = util.Button(self.buttonSurface, Rect(300, 390, 300, 55), lambda: pressButton("host"))
        b.text, b.font = "Hostuj gre", self.fnt36
        b.textColor, b.textHoverColor, b.textClickColor = self.color_gray, (107, 105, 100), (128, 124, 118)
        b.shadowAlpha = 66

        b = util.Button(self.buttonSurface, Rect(280, 440, 340, 55), lambda: pressButton("client"))
        b.text, b.font = "Dolacz do gry", self.fnt36
        b.textColor, b.textHoverColor, b.textClickColor = self.color_gray, (107, 105, 100), (128, 124, 118)
        b.shadowAlpha = 66

        b = util.Button(self.buttonSurface, Rect(300, 600, 300, 55), lambda: pressButton("back"))
        b.text, b.font = "Powrot", self.fnt48
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
            self.inputSurface.fill((0, 0, 0, 0))

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.ip_input_active = False
                        self.port_input_active = False
                    elif event.key == K_RETURN:
                        self.ip_input_active = False
                        self.port_input_active = False
                    elif event.key == K_BACKSPACE:
                        if self.ip_input_active:
                            self.ip_address = self.ip_address[:-1]
                        elif self.port_input_active:
                            self.port = self.port[:-1]
                    else:
                        if self.ip_input_active:
                            # Only allow valid IP characters
                            if event.unicode.isdigit() or event.unicode == '.' or event.unicode.isalpha():
                                self.ip_address += event.unicode
                        elif self.port_input_active:
                            # Only allow digits for port
                            if event.unicode.isdigit() and len(self.port) < 5:
                                self.port += event.unicode

            self.screen.fill((250, 247, 240))
            
            # Draw input boxes
            if self.ip_input_active:
                pygame.draw.rect(self.inputSurface, (180, 180, 180), self.ip_input_rect, 2, border_radius=10)
            else:
                pygame.draw.rect(self.inputSurface, (210, 210, 210), self.ip_input_rect, 1, border_radius=10)
                
            if self.port_input_active:
                pygame.draw.rect(self.inputSurface, (180, 180, 180), self.port_input_rect, 2, border_radius=10)
            else:
                pygame.draw.rect(self.inputSurface, (210, 210, 210), self.port_input_rect, 1, border_radius=10)
            
            # Draw input text
            util.drawText(self.inputSurface, self.ip_address, self.fnt24, 
                         (self.ip_input_rect.x + 10, self.ip_input_rect.y + 8), self.color_gray)
            util.drawText(self.inputSurface, self.port, self.fnt24, 
                         (self.port_input_rect.x + 10, self.port_input_rect.y + 8), self.color_gray)
            
            self.screen.blit(self.textSurface, (0,0))
            self.screen.blit(self.buttonSurface, (0,0))
            self.screen.blit(self.inputSurface, (0,0))

            util.update()
            pygame.display.flip()

        util.currentButtons = []
        
        # Go back to main menu if clicked "back"
        if self.selected_option is None:
            return show_menu(self.screen)
            
        return self.selected_option


def show_host_menu(screen):
    host_menu = HostMenu(screen)
    return host_menu.run()


def show_menu(screen):
    menu = Menu(screen)
    return menu.run()

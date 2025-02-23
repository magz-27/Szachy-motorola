import pygame
from pygame.locals import *

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font("font.otf", 56)
        self.small_font = pygame.font.Font("font.otf", 32)
        self.color_gray = (74, 73, 71)
        self.color_hover = (96, 94, 90)
        self.color_click = (128, 124, 118)
        self.color_white = (255, 255, 255)
        self.color_red = (236, 70, 70)
        self.color_red_hover = (255, 90, 90)
        self.color_red_click = (200, 50, 50)
        self.selected_option = None

        self.vs_computer_rect = pygame.Rect(300, 250, 300, 80)
        self.vs_online_rect = pygame.Rect(300, 350, 300, 80)
        self.vs_player_rect = pygame.Rect(250, 450, 400, 80)
        self.quit_rect = pygame.Rect(20, 20, 150, 60)

    def draw_button(self, surface, rect, text, is_hovered, is_clicked, is_red=False):
        if is_red:
            color = self.color_red
            if is_clicked:
                color = self.color_red_click
            elif is_hovered:
                color = self.color_red_hover
        else:
            color = self.color_gray
            if is_clicked:
                color = self.color_click
            elif is_hovered:
                color = self.color_hover

        pygame.draw.rect(surface, color, rect, border_radius=16)
        text_surface = self.small_font if rect == self.quit_rect else self.font
        text_render = text_surface.render(text, True, self.color_white)
        text_rect = text_render.get_rect(center=rect.center)
        surface.blit(text_render, text_rect)

    def run(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()[0]

            computer_hover = self.vs_computer_rect.collidepoint(mouse_pos)
            online_hover = self.vs_online_rect.collidepoint(mouse_pos)
            player_hover = self.vs_player_rect.collidepoint(mouse_pos)
            quit_hover = self.quit_rect.collidepoint(mouse_pos)

            for event in pygame.event.get():
                if event.type == QUIT:
                    return "quit"
                if event.type == MOUSEBUTTONDOWN:
                    if computer_hover:
                        self.selected_option = "computer"
                        running = False
                    elif online_hover:
                        self.selected_option = "online"
                        running = False
                    elif player_hover:
                        self.selected_option = "player"
                        running = False
                    elif quit_hover:
                        self.selected_option = "quit"
                        running = False

            self.screen.fill((250, 247, 240))

            title = self.font.render("Chess", True, self.color_gray)
            title_rect = title.get_rect(center=(self.screen.get_width() // 2, 150))
            self.screen.blit(title, title_rect)

            self.draw_button(self.screen, self.vs_computer_rect, "Vs Computer",
                            computer_hover, computer_hover and mouse_pressed)
            self.draw_button(self.screen, self.vs_online_rect, "Online",
                            online_hover, online_hover and mouse_pressed)
            self.draw_button(self.screen, self.vs_player_rect, "Player vs Player",
                            player_hover, player_hover and mouse_pressed)
            self.draw_button(self.screen, self.quit_rect, "Quit",
                            quit_hover, quit_hover and mouse_pressed, is_red=True)

            pygame.display.flip()
            clock.tick(60)

        return self.selected_option

def show_menu(screen):
    menu = Menu(screen)
    return menu.run()
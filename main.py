import pygame

pygame.init()
WIDTH = 1000
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Gra w Szachy dla 2 graczy w pygame')
font = pygame.font.Font('freesansbold.ttf', 20)
big_font = pygame.font.Font('freesansbold.ttf', 50)

timer = pygame.time.Clock()
fps = 60

#zmienne dotyczące gry i zdjęć
pionki_biale = ['wieza', 'skoczek', 'goniec', 'krol', 'hetman', 'goniec', 'skoczek', 'wieza'
                , 'pion', 'pion', 'pion', 'pion', 'pion', 'pion', 'pion', 'pion']
pionki_biale_lokalizacje = [(0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (7,0), (0,1), (1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1)]
pionki_czarne = ['wieza', 'skoczek', 'goniec', 'krol', 'hetman', 'goniec', 'skoczek', 'wieza'
                , 'pion', 'pion', 'pion', 'pion', 'pion', 'pion', 'pion', 'pion']
pionki_czarne_lokalizacje = [(0,7), (1,7), (2,7), (3,7), (4,7), (5,7), (6,7), (7,7), (0,6), (1,6), (2,6), (3,6), (4,6), (5,6), (6,6), (7,6)]

zbite_biale_pionki = []
zbite_czarne_pionki = []
# 0 - ruch białego, nie wybrano figury: 1 - ruch białego, wybrano figure: 2 - ruch czarnego, nie wybrano figury: 3 - ruch czarnego, wybrano figure
kogo_kolej = 0

wybor = 1000
poprawne_ruchy = []

#główna pętla gry
run = True;
while run:
    timer.tick(fps)
    screen.fill('dark gray')
    #obsługa zdarzeń
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()
pygame.quit()
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
#import grafik
czarny_hetman = pygame.image.load('assets/images/queen_dark.png')
czarny_hetman = pygame.transform.scale(czarny_hetman, (80, 80))
czarny_hetman_maly = pygame.transform.scale(czarny_hetman, (45, 45))

czarny_krol = pygame.image.load('assets/images/king_dark.png')
czarny_krol = pygame.transform.scale(czarny_krol, (80, 80))
czarny_krol_maly = pygame.transform.scale(czarny_krol, (45, 45))

czarna_wieza = pygame.image.load('assets/images/rook_dark.png')
czarna_wieza = pygame.transform.scale(czarna_wieza, (80, 80))
czarna_wieza_mala = pygame.transform.scale(czarna_wieza, (45, 45))

czarny_goniec = pygame.image.load('assets/images/bishop_dark.png')
czarny_goniec = pygame.transform.scale(czarny_goniec, (80, 80))
czarny_goniec_maly = pygame.transform.scale(czarny_goniec, (45, 45))

czarny_skoczek = pygame.image.load('assets/images/knight_dark.png')
czarny_skoczek = pygame.transform.scale(czarny_skoczek, (80, 80))
czarny_skoczek_maly = pygame.transform.scale(czarny_skoczek, (45, 45))

czarny_pionek = pygame.image.load('assets/images/pawn_dark.png')
czarny_pionek = pygame.transform.scale(czarny_pionek, (65, 65))
czarny_pionek_maly = pygame.transform.scale(czarny_pionek, (45, 45))

bialy_hetman = pygame.image.load('assets/images/queen_light.png')
bialy_hetman = pygame.transform.scale(bialy_hetman, (80, 80))
bialy_hetman_maly = pygame.transform.scale(bialy_hetman, (45, 45))

bialy_krol = pygame.image.load('assets/images/king_light.png')
bialy_krol = pygame.transform.scale(bialy_krol, (80, 80))
bialy_krol_maly = pygame.transform.scale(bialy_krol, (45, 45))

biala_wieza = pygame.image.load('assets/images/rook_light.png')
biala_wieza = pygame.transform.scale(biala_wieza, (80, 80))
biala_wieza_mala = pygame.transform.scale(biala_wieza, (45, 45))

bialy_goniec = pygame.image.load('assets/images/bishop_light.png')
bialy_goniec = pygame.transform.scale(bialy_goniec, (80, 80))
bialy_goniec_maly = pygame.transform.scale(bialy_goniec, (45, 45))

bialy_skoczek = pygame.image.load('assets/images/knight_light.png')
bialy_skoczek = pygame.transform.scale(bialy_skoczek, (80, 80))
bialy_skoczek_maly = pygame.transform.scale(bialy_skoczek, (45, 45))

bialy_pionek = pygame.image.load('assets/images/pawn_light.png')
bialy_pionek = pygame.transform.scale(bialy_pionek, (65, 65))
bialy_pionek_maly = pygame.transform.scale(bialy_pionek, (45, 45))

biale_obrazki = [bialy_pionek, bialy_hetman, bialy_krol, bialy_skoczek, biala_wieza, bialy_goniec]
male_biale_obrazki = [bialy_pionek_maly, bialy_hetman_maly, bialy_krol_maly, bialy_skoczek_maly,
                      biala_wieza_mala, bialy_goniec_maly]

czarne_obrazki = [czarny_pionek, czarny_hetman, czarny_krol, czarny_skoczek, czarna_wieza, czarny_goniec]
male_czarne_obrazki = [czarny_pionek_maly, czarny_hetman_maly, czarny_krol_maly, czarny_skoczek_maly,
                       czarna_wieza_mala, czarny_goniec_maly]

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
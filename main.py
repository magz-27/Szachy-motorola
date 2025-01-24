import math as pymath
import pygame
from pygame.locals import *
import util
from engine import *

pygame.init()
WIDTH = 1000
HEIGHT = 700
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Chess")
timer = pygame.time.Clock()
fps = 500

icon_pygame = pygame.image.load('icon.png')
selectMarker = pygame.image.load("select.png")
dotMarker = pygame.image.load("dot.png")

pygame.display.set_icon(icon_pygame)

fnt56 = pygame.font.Font("font.otf", 56)
fnt42 = pygame.font.Font("font.otf", 42)
fnt32 = pygame.font.Font("font.otf", 32)
fnt16 = pygame.font.Font("font.otf", 16)
fnt12 = pygame.font.Font("font.otf", 12)


pieceImages = {"Pawn Light": pygame.image.load('chessPieces/Pawn Light.png').convert_alpha(), "Rook Light": pygame.image.load(
    'chessPieces/Rook Light.png').convert_alpha(),
               "Knight Light": pygame.image.load('chessPieces/Knight Light.png').convert_alpha(), "Bishop Light": pygame.image.load(
        'chessPieces/Bishop Light.png').convert_alpha(),
               "Queen Light": pygame.image.load('chessPieces/Queen Light.png').convert_alpha(), "King Light": pygame.image.load(
        'chessPieces/King Light.png').convert_alpha(),
               "Pawn Dark": pygame.image.load('chessPieces/Pawn Dark.png').convert_alpha(), "Rook Dark": pygame.image.load(
        'chessPieces/Rook Dark.png').convert_alpha(),
               "Knight Dark": pygame.image.load('chessPieces/Knight Dark.png').convert_alpha(), "Bishop Dark": pygame.image.load(
        'chessPieces/Bishop Dark.png').convert_alpha(),
               "Queen Dark": pygame.image.load('chessPieces/Queen Dark.png').convert_alpha(), "King Dark": pygame.image.load(
        'chessPieces/King Dark.png').convert_alpha(),
               }

color_gray = (74, 73, 71)
color_checkerwhite = (231, 225, 209)
color_checkerblack = (194, 189, 174)

color_bluetest = (0, 188, 212)
color_redtest = (236, 70, 70)

timePassed = 0
drawCoords = False
boardCoords = (50, 90)
squareSize = 64
mousePressed = False
mouseClick = False

hover: Square = None
selected: Square = None

possibleMoves = []

initSurface = pygame.Surface((screen.get_width(), screen.get_height()), SRCALPHA)
boardSurface = pygame.Surface((screen.get_width(), screen.get_height()), SRCALPHA)

# Convert board from strings to Squares
for i in range(8):
    for j in range(8):
        current = j+i*8
        if board[current] == "": board[current] = Square(Rect(boardCoords[0] + j * squareSize, boardCoords[1] + i * squareSize, squareSize, squareSize), (j, i), Type(None, None))
        else: board[current] = Square(Rect(boardCoords[0] + j * squareSize, boardCoords[1] + i * squareSize, squareSize, squareSize), (j,i), Type(board[current][1].lower(), board[current][0]))


def handleMouseLogic():
    global mouseClick, mousePressed
    if pygame.mouse.get_pressed()[0]:
        if mousePressed:
            mouseClick = False
        else:
            mouseClick = True
        mousePressed = True
    else:
        mousePressed = False
        mouseClick = False


def renderBoard():
    global boardSurface
    # Clear the board
    boardSurface.fill((0, 0, 0, 0))

    # Render pieces
    for sq in board:
        if drawCoords:
            util.DrawText(boardSurface, str(sq.coord), fnt12, (sq.rect[0], sq.rect[1], squareSize, squareSize), color_gray)
        if sq.type.name is None: continue
        else: boardSurface.blit(pieceImages[sq.type.getName()+" "+sq.type.getColor()], sq.rect)

    # Render possible squares to move to
    for m in possibleMoves:
        boardSurface.blit(dotMarker, m.rect)


def hoverSquare():
    global hover
    hover = None
    for sq in board:
        rds = (0, 0, 0, 0)
        if sq.coord == (0, 0):
            rds = (16, 0, 0, 0)
        elif sq.coord == (7, 0):
            rds = (0, 16, 0, 0)
        elif sq.coord == (0, 7):
            rds = (0, 0, 16, 0)
        elif sq.coord == (7, 7):
            rds = (0, 0, 0, 16)

        if sq.rect.collidepoint(mousePos):
            thisMove = None
            for m in possibleMoves:
                if m.coord == sq.coord: thisMove = m
            if sq.type.color == playerColor or thisMove != None:
                util.DrawRoundedRect(screen, sq.rect, (250,247,240, 60), rds[0], rds[1], rds[2], rds[3])
                hover = sq
    if hover:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


def clickSquare():
    global board, selected, possibleMoves
    for sq in board:
        # Draw a select marker
        if sq == selected:
            screen.blit(selectMarker, sq.rect)
        if mouseClick:
            if sq.rect.collidepoint(mousePos):
                # Select a piece
                if sq.type.color == playerColor:
                    possibleMoves = []
                    if sq == selected:
                        selected = None
                    else:
                        selected = sq
                        possibleMoves = calculateMoves(board, sq.coord, sq.type.name, sq.type.color, 0)
                    renderBoard()
                # Move a piece
                else:
                    if possibleMoves.__contains__(hover) and selected is not None:
                        board = movePiece(board, selected, hover)
                        possibleMoves = []
                        renderBoard()


def drawInit():
    global initSurface
    boardborder = util.DrawRoundedRect(initSurface,(boardCoords[0] - 4, boardCoords[1] - 4, squareSize * 8 + 8, squareSize * 8 + 8), color_gray, 20, 20, 20, 20)
    playername1 = util.DrawText(initSurface, "Komputer", fnt56, (60, 20), color_gray)
    playername2 = util.DrawText(initSurface, "Gracz 1", fnt56, (60, 615), color_gray)

    #Draw the board squares
    for sq in board:
        sq.rect.w = squareSize
        sq.rect.h = squareSize

        clr = (sq.coord[0]+sq.coord[1]*7)%2
        if clr == 0:
            clr = color_checkerwhite
        else:
            clr = color_checkerblack

        # rounds the squares in the corners
        rds = (0, 0, 0, 0)
        if sq.coord == (0, 0):
            rds = (16, 0, 0, 0)
        elif sq.coord == (7, 0):
            rds = (0, 16, 0, 0)
        elif sq.coord == (0, 7):
            rds = (0, 0, 16, 0)
        elif sq.coord == (7, 7):
            rds = (0, 0, 0, 16)

        square = util.DrawRoundedRect(initSurface, sq.rect, clr, rds[0], rds[1], rds[2], rds[3])


run = True

drawInit()
renderBoard()

while run:
    deltaTime = timer.tick(fps) / 1000
    timePassed += deltaTime
    mousePos = pygame.mouse.get_pos()
    screen.fill((250, 247, 240))
    handleMouseLogic()

    # Timers
    util.DrawRoundedRect(screen, (430, 25, 110, 50), color_gray, 20, 20, 2, 2)
    util.DrawText(screen, f'{str(pymath.floor(timePassed)//60).zfill(2)}:{str(pymath.floor(timePassed)%60).zfill(2)}', fnt42, (484,50), (255,255,255), "center",(2,2), 80)
    util.DrawText(screen, f'TURA', fnt32, (390,60), color_gray, "center")
    util.DrawRoundedRect(screen, (430, 624, 110, 50), color_checkerwhite, 2, 2, 20, 20)
    util.DrawText(screen,f'00:00',fnt42, (484, 648), color_gray, "center", (2, 2), 80)

    # Debug
    # util.DrawText(screen, "click: "+str(mouseClick), fnt16, (screen.get_width()-4, screen.get_height()-122), color_gray, "topright")
    # util.DrawText(screen, "press: "+str(mousePressed), fnt16, (screen.get_width()-4, screen.get_height()-102), color_gray, "topright")
    util.DrawText(screen, "Selected: "+str(selected), fnt16, (screen.get_width()-4, screen.get_height()-82), color_gray, "topright")
    util.DrawText(screen, "Hover: "+str(hover), fnt16, (screen.get_width()-4, screen.get_height()-62), color_gray, "topright")
    util.DrawText(screen, "Fps: "+str(round(timer.get_fps())), fnt16, (screen.get_width()-4, screen.get_height()-42),  color_gray,"topright")
    util.DrawText(screen, "Mouse Pos: "+str(mousePos), fnt16, (screen.get_width()-4, screen.get_height()-22),  color_gray,"topright")

    # Board
    screen.blit(initSurface, (0,0))
    screen.blit(boardSurface, (0,0))
    hoverSquare()
    clickSquare()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.flip()

pygame.quit()

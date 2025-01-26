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

icon_pygame = pygame.image.load('graphics/icon.png')
selectMarker = pygame.image.load("graphics/select.png")

dotMarkerLight = pygame.image.load("graphics/dotlight.png")
captureMarkerLight = pygame.image.load("graphics/capturelight.png")
dotMarkerDark = pygame.image.load("graphics/dotdark.png")
captureMarkerDark = pygame.image.load("graphics/capturedark.png")

pygame.display.set_icon(icon_pygame)

fnt56 = pygame.font.Font("font.otf", 56)
fnt42 = pygame.font.Font("font.otf", 42)
fnt32 = pygame.font.Font("font.otf", 32)
fnt26 = pygame.font.Font("font.otf", 26)
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
player1 = "Gracz 1"
player2 = "Komputer"
hover: Square = None
selected: Square = None
timer1 = 15 * 60 + 0.99
timer2 = 15 * 60 + 0.99

currentPlayer = 'w'
allMoves = []
possibleMoves = []
isCheck = None
checkMate = None
isGameOver = False

initSurface = pygame.Surface((screen.get_width(), screen.get_height()), SRCALPHA)
boardSurface = pygame.Surface((screen.get_width(), screen.get_height()), SRCALPHA)


board = ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR",
         "bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP",
         "", "", "", "", "", "", "", "",
         "", "", "", "", "", "", "", "",
         "", "", "", "", "", "", "", "",
         "", "", "", "", "", "", "", "",
         "wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP",
         "wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]

# Convert board from strings to Squares
for i in range(8):
    for j in range(8):
        current = j+i*8
        if board[current] == "": board[current] = Square(Rect(boardCoords[0] + j * squareSize, boardCoords[1] + i * squareSize, squareSize, squareSize), (j, i), Type(None, None))
        else: board[current] = Square(Rect(boardCoords[0] + j * squareSize, boardCoords[1] + i * squareSize, squareSize, squareSize), (j,i), Type(board[current][1].lower(), board[current][0]))


def handleMouseLogic():
    # mousePressed is true if mouse button is currently pressed
    # mouseClick is true for a single frame when mouse is clicked
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

    # draw a colored square to show the last move
    if len(allMoves) > 0:
        m = allMoves[len(allMoves)-1]
        drawColorSquare(boardSurface, m[0].coord, (255, 235, 85, 40))
        drawColorSquare(boardSurface, m[1].coord, (255, 235, 85, 40))

    # draw a red square if check
    if isCheck: drawColorSquare(boardSurface, isCheck.coord, (255, 90, 84, 64))

    # Render pieces
    for sq in board:
        if drawCoords:
            util.DrawText(boardSurface, str(sq.coord), fnt12, (sq.rect[0], sq.rect[1], squareSize, squareSize), color_gray)
        if sq.type.name is None: continue
        else: boardSurface.blit(pieceImages[sq.type.getName()+" "+sq.type.getColor()], sq.rect)

    # make the board darker if game is over
    if isGameOver: util.DrawRoundedRect(boardSurface, (boardCoords[0], boardCoords[1], 64*8, 64*8), (47,45,41,40), 16, 16, 16, 16)

    # Render possible squares to move to
    for m in possibleMoves:
        # Render a different marker if capturing a piece
        if m.type.name == None:
            if currentPlayer == "w":
                boardSurface.blit(dotMarkerLight, m.rect)
            else:
                boardSurface.blit(dotMarkerDark, m.rect)
        else:
            if currentPlayer == "w":
                boardSurface.blit(captureMarkerLight, m.rect)
            else:
                boardSurface.blit(captureMarkerDark, m.rect)


def hoverSquare():
    global hover
    hover = None

    for sq in board:
        if sq.rect.collidepoint(mousePos):
            thisMove = None
            for m in possibleMoves:
                if m.coord == sq.coord: thisMove = m
            if sq.type.color == currentPlayer or thisMove != None:
                drawColorSquare(screen, sq.coord, (250, 247, 240, 60))
                hover = sq
    if hover:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


def clickSquare():
    global board, selected, possibleMoves, currentPlayer, isCheck, checkMate, isGameOver
    for sq in board:
        # Draw a select marker
        if sq == selected:
            screen.blit(selectMarker, sq.rect)
        if mouseClick:
            if sq.rect.collidepoint(mousePos):
                # Select a piece
                if sq.type.color == currentPlayer:
                    possibleMoves = []
                    if sq == selected:
                        selected = None
                    else:
                        selected = sq
                        dir = 1 if currentPlayer == "w" else -1
                        possibleMoves = calculateMoves(board, sq.coord, sq.type.name, sq.type.color, dir, True)
                    renderBoard()
                # Move a piece
                else:
                    if possibleMoves.__contains__(hover) and selected is not None:
                        allMoves.append((selected, hover))
                        board = movePiece(board, selected, hover)
                        possibleMoves = []
                        selected = None

                        currentPlayer = "w" if currentPlayer == "b" else "b"
                        dir = 1 if currentPlayer == "w" else -1

                        #check
                        isCheck = check(board)

                        #checkmate
                        print(getAllMoves(board, currentPlayer, dir, True))
                        if getAllMoves(board, currentPlayer, dir, True) == []:
                            checkMate = currentPlayer
                            isGameOver = True
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        renderBoard()


def drawColorSquare(surface, coord, color):
    rds = (0, 0, 0, 0)
    if coord == (0, 0):
        rds = (16, 0, 0, 0)
    elif coord == (7, 0):
        rds = (0, 16, 0, 0)
    elif coord == (0, 7):
        rds = (0, 0, 16, 0)
    elif coord == (7, 7):
        rds = (0, 0, 0, 16)

    util.DrawRoundedRect(surface, Rect(boardCoords[0]+coord[0]*squareSize, boardCoords[1]+coord[1]*squareSize, squareSize, squareSize), color, rds[0], rds[1], rds[2], rds[3])


def drawInit():
    global initSurface

    util.DrawRoundedRect(initSurface,(boardCoords[0] - 4, boardCoords[1] - 4, squareSize * 8 + 8, squareSize * 8 + 8), color_gray, 20, 20, 20, 20)
    util.DrawText(initSurface, player1, fnt56, (60, 615), color_gray)
    util.DrawText(initSurface, player2, fnt56, (60, 20), color_gray)

    # Draw the board squares
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
    mousePos = pygame.mouse.get_pos()
    screen.fill((250, 247, 240))
    handleMouseLogic()

    if not isGameOver:
        if currentPlayer == "w": timer2 -= deltaTime
        else: timer1 -= deltaTime

    # Timers
    if currentPlayer == "w":
        util.DrawRoundedRect(screen, (430, 25, 110, 50), color_checkerwhite, 20, 20, 2, 2)
        util.DrawRoundedRect(screen, (430, 624, 110, 50), color_gray, 2, 2, 20, 20)
        util.DrawText(screen, f'{str(pymath.floor(timer1) // 60).zfill(2)}:{str(pymath.floor(timer1) % 60).zfill(2)}', fnt42, (484, 50), color_gray, "center", (2, 2), 80)
        util.DrawText(screen, f'{str(pymath.floor(timer2) // 60).zfill(2)}:{str(pymath.floor(timer2) % 60).zfill(2)}', fnt42, (484, 648), (255, 255, 255), "center", (2, 2), 80)
    else:
        util.DrawRoundedRect(screen, (430, 25, 110, 50), color_gray, 20, 20, 2, 2)
        util.DrawRoundedRect(screen, (430, 624, 110, 50), color_checkerwhite, 2, 2, 20, 20)
        util.DrawText(screen, f'{str(pymath.floor(timer1) // 60).zfill(2)}:{str(pymath.floor(timer1) % 60).zfill(2)}', fnt42, (484, 50), (255, 255, 255), "center", (2, 2), 80)
        util.DrawText(screen, f'{str(pymath.floor(timer2) // 60).zfill(2)}:{str(pymath.floor(timer2) % 60).zfill(2)}', fnt42, (484, 648), color_gray, "center", (2, 2), 80)

    if currentPlayer == "w": util.DrawText(screen, f'TURA', fnt32, (390, 655), color_gray, "center")
    else: util.DrawText(screen, f'TURA', fnt32, (390,60), color_gray, "center")

    if checkMate != None:
        if checkMate == "w":
            util.DrawText(screen, "Szach mat!", fnt56, (screen.get_width() - 220, screen.get_height() - 590), color_gray, "center")
            util.DrawText(screen, f"Wygrywa {player2}!", fnt26, (screen.get_width() - 220, screen.get_height() - 550), color_gray, "center")

        if checkMate == "b":
            util.DrawText(screen, "Szach mat!", fnt56, (screen.get_width() - 220, screen.get_height() - 590), color_gray, "center")
            util.DrawText(screen, f"Wygrywa {player1}!", fnt26, (screen.get_width() - 220, screen.get_height() - 550), color_gray, "center")

    # Debug
    util.DrawText(screen, "Selected: "+str(selected), fnt16, (screen.get_width()-4, screen.get_height()-82), color_gray, "topright")
    util.DrawText(screen, "Hover: "+str(hover), fnt16, (screen.get_width()-4, screen.get_height()-62), color_gray, "topright")
    util.DrawText(screen, "Fps: "+str(round(timer.get_fps())), fnt16, (screen.get_width()-4, screen.get_height()-42),  color_gray,"topright")
    util.DrawText(screen, "Mouse Pos: "+str(mousePos), fnt16, (screen.get_width()-4, screen.get_height()-22),  color_gray,"topright")

    # Board
    screen.blit(initSurface, (0,0))
    screen.blit(boardSurface, (0,0))
    if not isGameOver:
        hoverSquare()
        clickSquare()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.flip()

pygame.quit()

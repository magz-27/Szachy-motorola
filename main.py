import math as pymath
import pygame
from pygame.locals import *
import util

from engine import *
from minimax import *



pygame.init()
WIDTH = 900
HEIGHT = 700
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Chess")
timer = pygame.time.Clock()
fps = 60

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

timePassedThisMove = 0
drawCoords = False
boardCoords = (50, 90)
squareSize = 64
mousePressed = False
mouseDown = False
mouseUp = False
player1 = "Gracz 1"
player2 = "Komputer"
hover: Square = None
selected: Square = None
timer1 = 15 * 60 + 0.95
timer2 = 15 * 60 + 0.95
actualTimer1 = 0
actualTimer2 = 0

currentPlayer = 'w'
allMoves = []
possibleMoves = []
isCheck = None
checkMate = None
isGameOver = False
useHandCursor = False
minimaxSearchDepth = 1

initSurface = pygame.Surface((screen.get_width(), screen.get_height()), SRCALPHA)
boardSurface = pygame.Surface((screen.get_width(), screen.get_height()), SRCALPHA)
buttonSurface = pygame.Surface((screen.get_width(), screen.get_height()), SRCALPHA)
timerSurface = pygame.Surface((screen.get_width(), screen.get_height()), SRCALPHA)
notesSurface = pygame.Surface((230, 110), SRCALPHA)

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

initBoard = [i for i in board]

currentButtons = []

class Button:
    hover = False
    clicked = False
    def __init__(self, rect: pygame.Rect, text, font, defaultColor, hoverColor, clickColor, fontColor, radius, onClick):
        global currentButtons
        self.rect = Rect(rect)
        self.text = text
        self.font = font
        self.defaultColor = defaultColor
        self.hoverColor = hoverColor
        self.clickColor = clickColor
        self.fontColor = fontColor
        self.radius = radius
        self.onClick = onClick
        currentButtons.append(self)
        renderButtons()


def handleButtonLogic():
    global currentButtons, useHandCursor
    for b in currentButtons:
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
                b.onClick()
                renderButtons()
            if mouseUp:
                renderButtons()
        else:
            h = b.hover
            b.hover = False
            if h:
                renderButtons()

def renderButtons():
    global buttonSurface, currentButtons, timePassed, screen
    buttonSurface.fill((0,0,0,0))
    for b in currentButtons:
        b:Button
        color = b.hoverColor if b.hover else b.defaultColor
        color = b.clickColor if b.clicked and b.hover else color

        util.drawRoundedRect(buttonSurface, (b.rect[0], b.rect[1], b.rect[2], b.rect[3]), color, b.radius, b.radius, b.radius, b.radius)
        util.drawText(buttonSurface, b.text, b.font, (b.rect[0]+b.rect[2]/2, b.rect[1]+b.rect[3]/2, b.rect[2], b.rect[3]), b.fontColor, "center")


def handleMouseLogic():
    # mousePressed is true if mouse button is currently pressed
    # mouseClick is true for a single frame when mouse is clicked
    global mouseDown, mouseUp, mousePressed
    mouseUp = False
    if pygame.mouse.get_pressed()[0]:
        if mousePressed:
            mouseDown = False
        else:
            mouseDown = True
        mousePressed = True
    else:
        if mousePressed:mouseUp = True
        mousePressed = False
        mouseDown = False


def renderBoard():
    global boardSurface
    # Clear the board
    boardSurface.fill((0, 0, 0, 0))

    if isGameOver: util.drawRoundedRect(boardSurface, (boardCoords[0], boardCoords[1], 64 * 8, 64 * 8), (47, 45, 41, 40), 16, 16, 16, 16)
    # draw a colored square to show the last move
    if len(allMoves) > 0:
        m = allMoves[len(allMoves)-1]
        drawColorSquare(boardSurface, m[0].coord, (255, 235, 85, 40))
        drawColorSquare(boardSurface, m[1].coord, (255, 235, 85, 40))

    # draw a red square if check
    if isCheck: drawColorSquare(boardSurface, isCheck.coord, (255, 90, 84, 64))

    if isCheck and not isGameOver: util.drawText(boardSurface, "Szach!", fnt56, (screen.get_width() - 173, screen.get_height() - 360), color_gray,
                  "center")
    # Render pieces
    for sq in board:
        if drawCoords:
            util.drawText(boardSurface, str(sq.coord), fnt12, (sq.rect[0], sq.rect[1], squareSize, squareSize), color_gray)
        if sq.type.name is None: continue
        else: boardSurface.blit(pieceImages[sq.type.getName()+" "+sq.type.getColor()], sq.rect)

    # make the board darker if game is over

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
    global hover, useHandCursor
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
        useHandCursor = True


def clickSquare():
    global board, selected, possibleMoves, currentPlayer, isCheck, checkMate, isGameOver, timePassedThisMove
    for sq in board:
        # Draw a select marker
        if sq == selected:
            screen.blit(selectMarker, sq.rect)
        if mouseDown:
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
                        allMoves.append((selected, hover, timePassedThisMove))
                        timePassedThisMove = 0
                        board = movePiece(board, selected, hover)
                        possibleMoves = []
                        selected = None

                        currentPlayer = "w" if currentPlayer == "b" else "b"
                        dir = 1 if currentPlayer == "w" else -1
                        drawTimers()
                        drawNotes()

                        print(minimax(board, currentPlayer, 3))

                        #check
                        isCheck = check(board)

                        #checkmate
                        #print(getAllMoves(board, currentPlayer, dir, True))
                        if getAllMoves(board, currentPlayer, dir, True) == []:
                            checkMate = currentPlayer
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

    util.drawRoundedRect(surface, Rect(boardCoords[0] + coord[0] * squareSize, boardCoords[1] + coord[1] * squareSize, squareSize, squareSize), color, rds[0], rds[1], rds[2], rds[3])


def drawInit():
    global initSurface

    # Border
    util.drawRoundedRect(initSurface, (boardCoords[0] - 4, boardCoords[1] - 4, squareSize * 8 + 8, squareSize * 8 + 8), color_gray, 20, 20, 20, 20)

    # Draw the timers on start
    drawTimers()
    drawNotes()

    # Player names
    util.drawText(initSurface, player1, fnt56, (60, 615), color_gray)
    util.drawText(initSurface, player2, fnt56, (60, 20), color_gray)

    # Algebraic notes
    util.drawRoundedRect(initSurface, (605, 100, 250, 125), color_checkerwhite, 16, 16, 16, 16)

    # Buttons
    def reset():
        global board, initBoard, allMoves, timer1, timer2, currentPlayer, isCheck, checkMate, isGameOver, selected, possibleMoves, timePassedThisMove
        allMoves = []
        board = initBoard
        timer1 = 15 * 60 + 0.95
        timer2 = 15 * 60 + 0.95
        timePassedThisMove = 0

        currentPlayer = "w"

        # Reset game over
        checkMate = None
        isGameOver = False
        isCheck = False

        # Reset selection
        selected = None
        possibleMoves = []

        drawTimers()
        drawNotes()
        renderBoard()

    def undo():
        global allMoves, board, isCheck, currentPlayer, checkMate, isGameOver, timer1, timer2, timePassedThisMove, selected, possibleMoves
        if len(allMoves) != 0:
            m = allMoves[len(allMoves)-1]
            for i, sq in enumerate(board):
                if sq.coord == m[0].coord: board[i] = m[0]
                if sq.coord == m[1].coord: board[i] = m[1]

            if m[0].type.color == "w":
                #timer2 += m[2]
                timer1 += timePassedThisMove
            else:
                #timer1 += m[2]
                timer2 += timePassedThisMove
            timePassedThisMove = 0

            allMoves.remove(m)
            currentPlayer = "w" if currentPlayer == "b" else "b"

            # Reset game over
            checkMate = None
            isGameOver = False
            isCheck = check(board)

            # Reset selection
            selected = None
            possibleMoves = []

            drawTimers()
            drawNotes()
            renderBoard()

    b = Button(Rect(605, 250, 115, 45), "Cofnij", fnt32, color_gray, (96, 94, 90), (128, 124, 118), (255,255,255), 16, lambda:undo())
    b = Button(Rect(740, 250, 115, 45), "Reset", fnt32, color_gray, (96, 94, 90), (128, 124, 118), (255,255,255), 16, lambda:reset())

    #util.drawRoundedRect(initSurface, (605, 250, 115, 45), color_gray, 16, 16, 16, 16)
    #util.drawText(initSurface, "Cofnij", fnt32, (663,273,20,20), (255,255,255), "center")
    #util.drawRoundedRect(initSurface, (740, 250, 115, 45), color_gray, 16, 16, 16, 16)
    #util.drawText(initSurface, "Reset", fnt32, (800,273,20,20), (255,255,255), "center")

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

        square = util.drawRoundedRect(initSurface, sq.rect, clr, rds[0], rds[1], rds[2], rds[3])


def drawTimers():
    global timerSurface
    timerSurface.fill((0,0,0,0))
    if currentPlayer == "w":
        util.drawText(timerSurface, f'TURA', fnt32, (390, 655), color_gray, "center")
        util.drawRoundedRect(timerSurface, (430, 25, 110, 50), color_checkerwhite, 20, 20, 2, 2)
        util.drawRoundedRect(timerSurface, (430, 624, 110, 50), color_gray, 2, 2, 20, 20)
        util.drawText(timerSurface, f'{str(pymath.floor(timer1) // 60).zfill(2)}:{str(pymath.floor(timer1) % 60).zfill(2)}', fnt42, (484, 50), color_gray, "center", (2, 2), 80)
        util.drawText(timerSurface, f'{str(pymath.floor(timer2) // 60).zfill(2)}:{str(pymath.floor(timer2) % 60).zfill(2)}', fnt42, (484, 648), (255, 255, 255), "center", (2, 2), 80)
    else:
        util.drawText(timerSurface, f'TURA', fnt32, (390, 60), color_gray, "center")
        util.drawRoundedRect(timerSurface, (430, 25, 110, 50), color_gray, 20, 20, 2, 2)
        util.drawRoundedRect(timerSurface, (430, 624, 110, 50), color_checkerwhite, 2, 2, 20, 20)
        util.drawText(timerSurface, f'{str(pymath.floor(timer1) // 60).zfill(2)}:{str(pymath.floor(timer1) % 60).zfill(2)}', fnt42, (484, 50), (255, 255, 255), "center", (2, 2), 80)
        util.drawText(timerSurface, f'{str(pymath.floor(timer2) // 60).zfill(2)}:{str(pymath.floor(timer2) % 60).zfill(2)}', fnt42, (484, 648), color_gray, "center", (2, 2), 80)


def drawNotes():
    global notesSurface
    notesSurface.fill((0, 0, 0, 0))
    last = -1
    for i, m in enumerate(allMoves):
        absolute = (len(allMoves) - 7) // 2
        if absolute < 0: absolute = 0
        count = i // 2
        pos = i % 2
        if count != last:
            util.drawText(notesSurface, f"{count + 1}.", fnt26, (5, (count - absolute) * 25, 20, 20), color_gray)

        strg = ""
        letters = ["a", "b", "c", "d", "e", "f", "g", "h"]

        if m[0].type.name == "p":
            # Pawn normal move
            if m[1].type.name == None:
                strg += letters[m[1].coord[0]]
                strg += str(8 - m[1].coord[1])
            # Pawn capture
            else:
                strg += letters[m[0].coord[0]]
                strg += "x"
                strg += letters[m[1].coord[0]]
                strg += str(8 - m[1].coord[1])
        else:
            strg += m[0].type.name.upper()
            if m[1].type.name != None: strg += "x"
            strg += letters[m[1].coord[0]]
            strg += str(8 - m[1].coord[1])

        if pos == 0:
            pos = 85
        else:
            pos = 180
        util.drawText(notesSurface, f"{strg}", fnt26,(pos, 15 + (count - absolute) * 25, 20, 20), color_gray, "center")
        last = count

run = True

drawInit()

renderBoard()

while run:
    deltaTime = timer.tick(fps) / 1000
    mousePos = pygame.mouse.get_pos()
    screen.fill((250, 247, 240))
    useHandCursor = False
    handleMouseLogic()

    if not isGameOver:
        if currentPlayer == "w": timer2 -= deltaTime
        else: timer1 -= deltaTime
    if timer1 < 0: timer1 = 0
    if timer2 < 0: timer2 = 0
    if not isGameOver: timePassedThisMove += deltaTime

    # Timers
    # Draw the timers only when they actually change, to save fps
    if actualTimer1 != pymath.floor(timer1) % 60 and not isGameOver: drawTimers()
    if actualTimer2 != pymath.floor(timer2) % 60 and not isGameOver: drawTimers()
    actualTimer1 = pymath.floor(timer1) % 60
    actualTimer2 = pymath.floor(timer2) % 60

    # End game by checkmate
    if checkMate != None and not isGameOver:
        isGameOver = True
        selected = None
        possibleMoves = []
        renderBoard()
        if checkMate == "w":
            util.drawText(boardSurface, "Szach mat!", fnt56, (screen.get_width() - 173, screen.get_height() - 360), color_gray, "center")
            util.drawText(boardSurface, f"Wygrywa {player2}!", fnt26, (screen.get_width() - 173, screen.get_height() - 320), color_gray, "center")

        if checkMate == "b":
            util.drawText(boardSurface, "Szach mat!", fnt56, (screen.get_width() - 173, screen.get_height() - 360), color_gray, "center")
            util.drawText(boardSurface, f"Wygrywa {player1}!", fnt26, (screen.get_width() - 173, screen.get_height() - 320), color_gray, "center")

    # End game by time over
    if timer1 <= 0 and not isGameOver:
        isGameOver = True
        selected = None
        possibleMoves = []
        renderBoard()
        util.drawText(boardSurface, "Koniec czasu!", fnt56, (screen.get_width() - 173, screen.get_height() - 360), color_gray,
                      "center")
        util.drawText(boardSurface, f"Wygrywa {player1}!", fnt26, (screen.get_width() - 173, screen.get_height() - 320),
                      color_gray, "center")

    if timer2 <= 0 and not isGameOver:
        isGameOver = True
        selected = None
        possibleMoves = []
        renderBoard()
        util.drawText(boardSurface, "Koniec czasu!", fnt56, (screen.get_width() - 173, screen.get_height() - 360), color_gray,
                      "center")
        util.drawText(boardSurface, f"Wygrywa {player2}!", fnt26, (screen.get_width() - 173, screen.get_height() - 320),
                      color_gray, "center")

    # Debug
    # util.drawText(screen, "MouseUp: " + str(mouseUp), fnt16, (screen.get_width() - 4, screen.get_height() - 102), color_gray, "topright")
    # util.drawText(screen, "Selected: " + str(selected), fnt16, (screen.get_width() - 4, screen.get_height() - 82), color_gray, "topright")
    # util.drawText(screen, "Hover: " + str(hover), fnt16, (screen.get_width() - 4, screen.get_height() - 62), color_gray, "topright")
    # util.drawText(screen, "Mouse Pos: " + str(mousePos), fnt16, (screen.get_width() - 4, screen.get_height() - 42), color_gray, "topright")
    #util.drawText(screen, "Time Passed: " + str(round(timePassedThisMove, 4)), fnt32, (screen.get_width() - 4, screen.get_height() - 112), color_gray, "topright")
    #util.drawText(screen, "Timer1: " + str(round(timer1, 4)), fnt32, (screen.get_width() - 4, screen.get_height() - 82), color_gray, "topright")
    #util.drawText(screen, "Timer2: " + str(round(timer2, 4)), fnt32, (screen.get_width() - 4, screen.get_height() - 52), color_gray, "topright")
    util.drawText(screen, "Fps: " + str(round(timer.get_fps())), fnt16, (screen.get_width() - 4, screen.get_height() - 22), color_gray, "topright")

    # Board
    screen.blit(initSurface, (0,0))
    screen.blit(boardSurface, (0,0))
    screen.blit(buttonSurface, (0,0))
    screen.blit(timerSurface, (0,0))
    screen.blit(notesSurface, (615, 110))
    if not isGameOver:
        hoverSquare()
        clickSquare()

    handleButtonLogic()

    events = pygame.event.get()

    if useHandCursor: pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else: pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    for event in events:
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()

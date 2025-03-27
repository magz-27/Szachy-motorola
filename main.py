import cProfile
import math as pymath
import pygame
#import pyperclip
from pygame.locals import *
import threading
import util
import copy

from engine import *

from ai_algorithms import *
import menu


pygame.init()
WIDTH = 900
HEIGHT = 700
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Chess")
timer = pygame.time.Clock()
fps = 60

icon_pygame = pygame.image.load('graphics/icon.png')
selectMarker = pygame.image.load("graphics/select.png")

dotMarkerLight = pygame.image.load("graphics/marker_dot_white.png")
captureMarkerLight = pygame.image.load("graphics/marker_capture_white.png")
specialMarkerLight = pygame.image.load("graphics/marker_special_white.png")
dotMarkerDark = pygame.image.load("graphics/marker_dot_black.png")
captureMarkerDark = pygame.image.load("graphics/marker_capture_black.png")
specialMarkerDark = pygame.image.load("graphics/marker_special_black.png")

iconExit = pygame.image.load("graphics/icon_exit.png")
iconSound = pygame.image.load("graphics/icon_sound.png")
iconStats = pygame.image.load("graphics/icon_stats.png")
iconCopy = pygame.image.load("graphics/icon_copy.png")

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
secondsPassed = 0
framesPassed = 0

currentPlayer = 'w'
computerColor = "b"
allMoves = []
possibleMoves = []
whiteInCheck = False
blackInCheck = False
checkMate = None
isGameOver = False
kingWhiteCoord = None
kingBlackCoord = None

minimaxSearchDepth = 3
awaitingMove = False
minimaxThread = None

nerdViewVisible = False
lastMinimaxScore = 0
lastSearchDurationMiliseconds = 0

initSurface = pygame.Surface((screen.get_width(), screen.get_height()), SRCALPHA)
boardSurface = pygame.Surface((screen.get_width(), screen.get_height()), SRCALPHA)
buttonSurface = pygame.Surface((screen.get_width(), screen.get_height()), SRCALPHA)
timerSurface = pygame.Surface((screen.get_width(), screen.get_height()), SRCALPHA)
turnSurface = pygame.Surface((screen.get_width(), screen.get_height()), SRCALPHA)
gameResultSurface = pygame.Surface((screen.get_width(), screen.get_height()), SRCALPHA)
notesSurface = pygame.Surface((230, 110), SRCALPHA)

# Pawn promotion test board
# board = ["bR", "bN", "bB", "bQ", "bK", "bB", "", "",
#          "bP", "bP", "bP", "bP", "bP", "bP", "wP", "wP",
#          "", "", "", "", "", "", "", "",
#          "", "", "", "", "", "", "", "",
#          "", "", "", "", "", "", "", "",
#          "", "", "", "", "", "", "", "",
#          "wP", "wP", "wP", "wP", "wP", "wP", "", "bP",
#          "wR", "wN", "wB", "wQ", "wK", "wB", "", ""]


board = ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR",
         "bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP",
         "", "", "", "", "", "", "", "",
         "", "", "", "", "", "", "", "",
         "", "", "", "", "", "", "", "",
         "", "", "", "", "", "", "", "",
         "wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP",
         "wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]

game_mode = None

run = True


def showMenu():
    global player1, player2, vs_computer, game_mode
    game_mode = None
    game_mode = menu.show_menu(screen)

    if game_mode == "quit":
        pygame.quit()
        exit()
    elif game_mode == "computer":
        player1 = "Player 1"
        player2 = "Computer"
        vs_computer = True
    elif game_mode == "online":
        player1 = "Player 1"
        player2 = "Online Player"
        vs_computer = False
    elif game_mode == "player":
        player1 = "Player 1"
        player2 = "Player 2"
        vs_computer = False


showMenu()

for i in range(8):
    for j in range(8):
        current = j+i*8
        if board[current] == "": board[current] = Square(Rect(boardCoords[0] + j * squareSize, boardCoords[1] + i * squareSize, squareSize, squareSize), (j, i), Type(None, None))
        else: board[current] = Square(Rect(boardCoords[0] + j * squareSize, boardCoords[1] + i * squareSize, squareSize, squareSize), (j,i), Type(board[current][1].lower(), board[current][0]))

initBoard = copy.deepcopy(board)

initPieceDictionary(board)


def handleMinimax(board, color, depth):
    global awaitingMove, lastMinimaxScore

    startTime = pygame.time.get_ticks()

    result = minimax(board, color, kingWhiteCoord, kingBlackCoord, depth)
    lastMinimaxScore = result[0]
    move = result[1]

    startSquare = getBoardFromCoord(board, move[0])
    endSquare = getBoardFromCoord(board, move[1])
    handlePieceMove(startSquare, endSquare, startTime)

    awaitingMove = False

    return


def renderBoard():
    global boardSurface
    # Clear the board
    boardSurface.fill((0, 0, 0, 0))
    gameResultSurface.fill((0,0,0,0))

    # make the board darker if game is over
    if isGameOver:
        util.drawRoundedRect(boardSurface, (boardCoords[0], boardCoords[1], 64 * 8, 64 * 8), (47, 45, 41, 40), 16, 16, 16, 16)

    # draw a colored square to show the last move
    if len(allMoves) > 0:
        m = allMoves[len(allMoves)-1]
        drawColorSquare(boardSurface, m[0].coord, (255, 235, 85, 40))
        drawColorSquare(boardSurface, m[1].coord, (255, 235, 85, 40))

    # draw a red square if check
    if whiteInCheck: drawColorSquare(boardSurface, kingWhiteCoord, (255, 90, 84, 64))
    if blackInCheck: drawColorSquare(boardSurface, kingBlackCoord, (255, 90, 84, 64))

    if (whiteInCheck or blackInCheck) and not isGameOver:
        util.drawText(gameResultSurface, "Szach!", fnt56, (screen.get_width() - 173, screen.get_height() - 360), color_gray,"center")

    # Render pieces
    for sq in board:
        if drawCoords:
            util.drawText(boardSurface, str(sq.coord), fnt12, (sq.rect[0], sq.rect[1], squareSize, squareSize), color_gray)
        if sq.type.name is None: continue
        else: boardSurface.blit(pieceImages[sq.type.getName()+" "+sq.type.getColor()], sq.rect)

    # Render possible squares to move to
    for m in possibleMoves:
        # Render a different marker if capturing a piece

        # KINGPOSIOTOIN UNDO

        # Pawn promotion
        if selected.type.name == "p" and m.type.name == None:
            if m.coord[1] == 0 and currentPlayer == "w":
                boardSurface.blit(specialMarkerLight, m.rect)
                continue
            elif m.coord[1] == 7 and currentPlayer == "b":
                boardSurface.blit(specialMarkerDark, m.rect)
                continue

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
        util.useHandCursor = True


def handlePieceMove(startSquare, endSquare, startTime = None):
    global board, possibleMoves, currentPlayer, checkMate, whiteInCheck, blackInCheck, lastSearchDurationMiliseconds, selected, timePassedThisMove, kingWhiteCoord, kingBlackCoord

    if not startTime == None:
        timeElapsed = pygame.time.get_ticks() - startTime
        if currentPlayer == computerColor:
            lastSearchDurationMiliseconds = timeElapsed
        timePassedThisMove = timeElapsed / 1000

    timePassedThisMove = 0
    allMoves.append((copy.deepcopy(startSquare), copy.deepcopy(endSquare), timePassedThisMove))

    # Pawn promotion
    if startSquare.type.name == "p":
        if (endSquare.coord[1] == 0 and startSquare.type.color == "w") or (endSquare.coord[1] == 7 and startSquare.type.color == "b"):
            del pieceDictionary[startSquare.type.color + startSquare.type.name][startSquare.coord]
            pieceDictionary[startSquare.type.color + "q"][startSquare.coord] = startSquare
            startSquare.type.name = "q"

    if startSquare.type.name == "k":
        if startSquare.type.color == "w": kingWhiteCoord = endSquare.coord
        else: kingBlackCoord = endSquare.coord

    board = movePiece(board, startSquare, endSquare, True)
    possibleMoves = []
    selected = None

    currentPlayer = "w" if currentPlayer == "b" else "b"
    dir = 1 if currentPlayer == "w" else -1
    drawTimers()
    drawNotes()

    # check
    whiteInCheck = check(board, "w", kingWhiteCoord)
    blackInCheck = check(board, "b", kingBlackCoord)

    kingCoord = kingWhiteCoord if currentPlayer == "w" else kingBlackCoord

    #checkmate
    #print(getAllMoves(board, currentPlayer, dir, True))
    if not getAllMoves(board, currentPlayer, dir, kingCoord, True):
        checkMate = currentPlayer
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    renderBoard()


def clickSquare():
    global awaitingMove, board, selected, possibleMoves, currentPlayer, whiteInCheck, blackInCheck, checkMate, isGameOver, minimaxThread, timePassedThisMove
    for sq in board:
        # Draw a select marker
        if sq == selected:
            screen.blit(selectMarker, sq.rect)
        if mouseDown and not awaitingMove:
            if sq.rect.collidepoint(mousePos):
                # Select a piece
                if sq.type.color == currentPlayer:
                    possibleMoves = []
                    if sq == selected:
                        selected = None
                    else:
                        selected = sq
                        dir = 1 if currentPlayer == "w" else -1

                        kingCoord = kingWhiteCoord if currentPlayer == "w" else kingBlackCoord
                        possibleMoves = calculateMoves(board, sq.coord, sq.type.name, sq.type.color, dir, kingCoord, True)
                    renderBoard()
                # Move a piece
                else:
                    if possibleMoves.__contains__(hover) and selected is not None:
                        handlePieceMove(selected, hover)

                        if game_mode == "computer":
                            if checkMate: return
                            awaitingMove = True
                            minimaxThread = threading.Thread(
                                target=handleMinimax,
                                name="minimax",
                                args=(board, currentPlayer, minimaxSearchDepth)
                            )
                            minimaxThread.daemon = True
                            minimaxThread.start()
                            #cProfile.run("handleMinimax(board,currentPlayer, minimaxSearchDepth)")


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


def resetBoard():
    global awaitingMove, board, initBoard, allMoves, timer1, timer2, currentPlayer, whiteInCheck, blackInCheck, checkMate, isGameOver, selected, possibleMoves, timePassedThisMove
    if awaitingMove:
        return

    allMoves = []
    board = copy.deepcopy(initBoard)
    initPieceDictionary(board)
    timer1 = 15 * 60 + 0.95
    timer2 = 15 * 60 + 0.95
    timePassedThisMove = 0

    currentPlayer = "w"

    # Reset game over
    checkMate = None
    isGameOver = False
    whiteInCheck = None
    blackInCheck = None

    # Reset selection
    selected = None
    possibleMoves = []

    drawTimers()
    drawNotes()
    renderBoard()


def restartGame():
    if awaitingMove:
        return
    global framesPassed
    resetBoard()
    framesPassed = 0
    util.currentButtons = []

    showMenu()
    drawInit()


def drawInit():
    global initSurface, kingWhiteCoord, kingBlackCoord

    initSurface.fill((0,0,0,0))
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
    def undo(final = False):
        global allMoves, awaitingMove, board, whiteInCheck, blackInCheck, currentPlayer, checkMate, isGameOver, timer1, timer2, timePassedThisMove, selected, possibleMoves, kingWhiteCoord, kingBlackCoord

        if awaitingMove:
            return

        if len(allMoves) != 0:
            m = allMoves[len(allMoves)-1]

            # Pawn promotion
            pieceName = m[0].type.name
            if m[0].type.name == "p":
                if (m[1].coord[1] == 0 and m[0].type.color == "w") or (m[1].coord[1] == 7 and m[0].type.color == "b"):
                    pieceName = "q"

            # Undo the move in the dictionary
            pieceDictionary[m[0].type.color + m[0].type.name][m[0].coord] = m[0]
            del pieceDictionary[m[0].type.color + pieceName][m[1].coord]
            if m[1].type.name != None: pieceDictionary[m[1].type.color + m[1].type.name][m[1].coord] = m[1]

            for i, sq in enumerate(board):
                if sq.coord == m[0].coord: board[i] = m[0]
                if sq.coord == m[1].coord: board[i] = m[1]

            # Undo king position
            if m[0].type.name == "k":
                if m[0].type.color == "w": kingWhiteCoord = m[0].coord
                else: kingBlackCoord = m[0].coord

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
            whiteInCheck = check(board, "w", kingWhiteCoord)
            blackInCheck = check(board, "b", kingBlackCoord)

            # Reset selection
            selected = None
            possibleMoves = []

            drawTimers()
            drawNotes()
            renderBoard()


            # Undo computer's and own move
            if game_mode == "computer" and not final:
                undo(True)

    def toggleNerdView():
        global nerdViewVisible
        nerdViewVisible = not nerdViewVisible

    # def copyBoard():
    #     boardTxt = "["
    #     for sq in board:
    #         if sq.type.name == None: boardTxt += '""'
    #         else: boardTxt += '"'+sq.type.color+sq.type.name.upper()+'"'
    #         boardTxt += ", "
    #         if sq.coord[0] == 7 and sq.coord[1] != 7: boardTxt += "\n"
    #     boardTxt += "]"
    #     pyperclip.copy(boardTxt)

    b = util.Button(buttonSurface, Rect(605, 250, 115, 45), lambda: undo())
    b.text, b.font = "Cofnij", fnt32
    b.radius = 16
    b.defaultColor, b.hoverColor, b.clickColor = color_gray, (96, 94, 90), (128, 124, 118)

    b = util.Button(buttonSurface, Rect(740, 250, 115, 45), lambda: resetBoard())
    b.text, b.font = "Reset", fnt32
    b.radius = 16
    b.defaultColor, b.hoverColor, b.clickColor = color_gray, (96, 94, 90), (128, 124, 118)

    # Top buttons
    b = util.Button(buttonSurface, Rect(810, 30, 48, 48), lambda: restartGame())
    b.image = iconExit
    b.textColor, b.textHoverColor, b.textClickColor = (0, 0, 0), (40, 40, 40), (80, 80, 80)

    b = util.Button(buttonSurface, Rect(750, 30, 48, 48), lambda: print("Test"))
    b.image = iconSound
    b.textColor, b.textHoverColor, b.textClickColor = (0, 0, 0), (40, 40, 40), (80, 80, 80)

    b = util.Button(buttonSurface, Rect(685, 30, 48, 48), lambda: toggleNerdView())
    b.image = iconStats
    b.textColor, b.textHoverColor, b.textClickColor = (0, 0, 0), (40, 40, 40), (80, 80, 80)

    # b = util.Button(buttonSurface, Rect(627, 30, 48, 48), lambda: copyBoard())
    # b.image = iconCopy
    # b.textColor, b.textHoverColor, b.textClickColor = (0,0,0), (40, 40, 40), (80, 80, 80)

    util.renderButtons()

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

        # Change the king coordinates
        if sq.type.name == "k":
            if sq.type.color == "w":
                kingWhiteCoord = sq.coord
            else:
                kingBlackCoord = sq.coord

        square = util.drawRoundedRect(initSurface, sq.rect, clr, rds[0], rds[1], rds[2], rds[3])

    renderBoard()


def drawTimers():
    global timerSurface
    timerSurface.fill((0,0,0,0))
    turnSurface.fill((0,0,0,0))

    if not isGameOver:
        if currentPlayer == "w":
            util.drawText(turnSurface, f'TURA', fnt32, (385, 650), color_gray, "center")
            util.drawRoundedRect(timerSurface, (430, 25, 110, 50), color_checkerwhite, 20, 20, 2, 2)
            util.drawRoundedRect(timerSurface, (430, 624, 110, 50), color_gray, 2, 2, 20, 20)
            util.drawText(timerSurface,f'{str(pymath.floor(timer1) // 60).zfill(2)}:{str(pymath.floor(timer1) % 60).zfill(2)}', fnt42, (484, 50), color_gray, "center", (2, 2), 80)
            util.drawText(timerSurface,f'{str(pymath.floor(timer2) // 60).zfill(2)}:{str(pymath.floor(timer2) % 60).zfill(2)}', fnt42, (484, 648), (255, 255, 255), "center", (2, 2), 80)
        else:
            if not isGameOver: util.drawText(turnSurface, f'TURA', fnt32, (385, 50), color_gray, "center")
            util.drawRoundedRect(timerSurface, (430, 25, 110, 50), color_gray, 20, 20, 2, 2)
            util.drawRoundedRect(timerSurface, (430, 624, 110, 50), color_checkerwhite, 2, 2, 20, 20)
            util.drawText(timerSurface, f'{str(pymath.floor(timer1) // 60).zfill(2)}:{str(pymath.floor(timer1) % 60).zfill(2)}',fnt42, (484, 50), (255, 255, 255), "center", (2, 2), 80)
            util.drawText(timerSurface, f'{str(pymath.floor(timer2) // 60).zfill(2)}:{str(pymath.floor(timer2) % 60).zfill(2)}', fnt42, (484, 648), color_gray, "center", (2, 2), 80)
    else:
        util.drawRoundedRect(timerSurface, (430, 25, 110, 50), color_checkerwhite, 20, 20, 2, 2)
        util.drawRoundedRect(timerSurface, (430, 624, 110, 50), color_checkerwhite, 2, 2, 20, 20)
        util.drawText(timerSurface,
                      f'{str(pymath.floor(timer1) // 60).zfill(2)}:{str(pymath.floor(timer1) % 60).zfill(2)}', fnt42,
                      (484, 50), color_gray, "center", (2, 2), 80)
        util.drawText(timerSurface,
                      f'{str(pymath.floor(timer2) // 60).zfill(2)}:{str(pymath.floor(timer2) % 60).zfill(2)}', fnt42,
                      (484, 648), color_gray, "center", (2, 2), 80)


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


drawInit()

while run:
    if not game_mode: continue
    deltaTime = timer.tick(fps) / 1000
    mousePos = pygame.mouse.get_pos()
    screen.fill((250, 247, 240))
    mouseDown, mouseUp, mousePressed = util.handleMouseLogic()
    framesPassed += 1

    # Prevents clicking on piece immediately after beginning the game
    # and timers counting down
    if framesPassed == 1:
        mouseDown = False
        deltaTime = 0

    util.useHandCursor = False
    secondsPassed += deltaTime


    if not isGameOver:
        if currentPlayer == "w": timer2 -= deltaTime
        else: timer1 -= deltaTime
    if timer1 < 0: timer1 = 0
    if timer2 < 0: timer2 = 0
    if not isGameOver: timePassedThisMove += deltaTime

    # Join the minimax thread after it finishes
    if minimaxThread != None and not minimaxThread.is_alive():
        minimaxThread.join()
        minimaxThread = None

    # Timers
    # Draw the timers only when they actually change, to save fps
    if actualTimer1 != pymath.floor(timer1) % 60 and not isGameOver: drawTimers()
    if actualTimer2 != pymath.floor(timer2) % 60 and not isGameOver: drawTimers()
    actualTimer1 = pymath.floor(timer1) % 60
    actualTimer2 = pymath.floor(timer2) % 60

    # End game by checkmate
    if checkMate != None and not isGameOver:
        isGameOver = True
        drawTimers()
        selected = None
        possibleMoves = []
        renderBoard()
        if checkMate == "w":
            util.drawText(gameResultSurface, "Szach mat!", fnt56, (screen.get_width() - 173, screen.get_height() - 355), color_gray, "center")
            util.drawText(gameResultSurface, f"Wygrywa {player2}!", fnt26, (screen.get_width() - 173, screen.get_height() - 315), color_gray, "center")

        if checkMate == "b":
            util.drawText(gameResultSurface, "Szach mat!", fnt56, (screen.get_width() - 173, screen.get_height() - 355), color_gray, "center")
            util.drawText(gameResultSurface, f"Wygrywa {player1}!", fnt26, (screen.get_width() - 173, screen.get_height() - 315), color_gray, "center")

    # End game by time over
    if timer1 <= 0 and not isGameOver:
        isGameOver = True
        selected = None
        possibleMoves = []
        renderBoard()
        util.drawText(gameResultSurface, "Koniec czasu!", fnt56, (screen.get_width() - 173, screen.get_height() - 355),
                      color_gray,"center")
        util.drawText(gameResultSurface, f"Wygrywa {player1}!", fnt26,
                      (screen.get_width() - 173, screen.get_height() - 315),
                      color_gray, "center")

    if timer2 <= 0 and not isGameOver:
        isGameOver = True
        selected = None
        possibleMoves = []
        renderBoard()
        util.drawText(gameResultSurface, "Koniec czasu!", fnt56, (screen.get_width() - 173, screen.get_height() - 355),
                      color_gray,
                      "center")
        util.drawText(gameResultSurface, f"Wygrywa {player2}!", fnt26,
                      (screen.get_width() - 173, screen.get_height() - 315),
                      color_gray, "center")

    # Nerd View
    if nerdViewVisible:
        if game_mode == "computer":
            util.drawText(screen, "Wynik minimax: " + str(round(lastMinimaxScore, 2)), fnt16, (screen.get_width() - 4, screen.get_height() - 82), color_gray, "topright", (0,0))
            util.drawText(screen, "Czas minimax: " + str(lastSearchDurationMiliseconds) + "ms", fnt16, (screen.get_width() - 4, screen.get_height() - 62), color_gray, "topright", (0,0))
        util.drawText(screen, "Mouse Pos: " + str(mousePos), fnt16, (screen.get_width() - 4, screen.get_height() - 42), color_gray, "topright", (0,0))
        util.drawText(screen, "Fps: " + str(round(timer.get_fps())), fnt16, (screen.get_width() - 4, screen.get_height() - 22), color_gray, "topright", (0,0))


    # Board
    screen.blit(initSurface, (0,0))
    screen.blit(boardSurface, (0,0))
    screen.blit(buttonSurface, (0,0))
    screen.blit(timerSurface, (0,0))
    screen.blit(turnSurface, util.SineRect((0, 0), secondsPassed, 2, 8))
    screen.blit(gameResultSurface, util.SineRect((0, 0), secondsPassed, 3, 8))
    screen.blit(notesSurface, (615, 110))
    if not isGameOver:
        hoverSquare()
        clickSquare()

    util.update()

    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()

import pygame
from pygame.locals import *
import sys
import math as pymath
import select
import time
import threading
import util
from engine import *
import menu
from ai_algorithms import *
from networkchess import *

pygame.init()
WIDTH = 900
HEIGHT = 700
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Chess")
timer = pygame.time.Clock()
fps = 60

# Loading the icons
icon_pygame = pygame.image.load('graphics/icon.png')
selectMarker = pygame.image.load("graphics/select.png")

dotMarkerLight = pygame.image.load("graphics/marker_dot_white.png")
captureMarkerLight = pygame.image.load("graphics/marker_capture_white.png")
specialMarkerLight = pygame.image.load("graphics/marker_special_white.png")
dotMarkerDark = pygame.image.load("graphics/marker_dot_black.png")
captureMarkerDark = pygame.image.load("graphics/marker_capture_black.png")
specialMarkerDark = pygame.image.load("graphics/marker_special_black.png")

iconExit = pygame.image.load("graphics/icon_exit.png")
iconSoundOn = pygame.image.load("graphics/icon_sound_on.png")
iconSoundOff = pygame.image.load("graphics/icon_sound_off.png")
iconStats = pygame.image.load("graphics/icon_stats.png")
iconCopy = pygame.image.load("graphics/icon_copy.png")
iconScrollUp = pygame.image.load("graphics/icon_scrollup.png")
iconScrollDown = pygame.image.load("graphics/icon_scrolldown.png")

pygame.display.set_icon(icon_pygame)

fnt56 = pygame.font.Font("font.otf", 56)
fnt42 = pygame.font.Font("font.otf", 42)
fnt32 = pygame.font.Font("font.otf", 32)
fnt26 = pygame.font.Font("font.otf", 26)
fnt18 = pygame.font.Font("font.otf", 18)
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

# game variables
timePassedThisMove = 0
boardCoords = (50, 90)
squareSize = 64
mousePressed = False
mouseDown = False
mouseUp = False
player1 = "Gracz 1"
player2 = "Komputer"
hover: Square = None
selected: Square = None
scrollUpBtn = None
scrollDownBtn = None
timer1 = 15 * 60 + 0.95
timer2 = 15 * 60 + 0.95
actualTimer1 = 0
actualTimer2 = 0
secondsPassed = 0
framesPassed = 0
scroll = 0

drawCoords = False
isSpeedGame = False
useLongNotation = False
nerdViewVisible = False
gameMode = None
algorithm = None

# engine variables
currentPlayer = 'w'
computerColor = "b"
kingWhiteCoord = None
kingBlackCoord = None
allMoves = []
possibleMoves = []
whiteInCheck = False
blackInCheck = False
checkMate = None
isGameOver = False

network_game = None
network_nerd_view_visible = False

# algorithm variables
minimaxSearchDepth = None
minimaxEasySearchDepth = 2
minimaxHardSearchDepth = 3
awaitingMove = False
minimaxThread = None
lastMinimaxScore = 0
lastSearchDurationMiliseconds = 0
mctsTimeLimitMiliseconds = 0
mctsEasyTimeLimitMiliseconds = 1000
mctsHardTimeLimitMiliseconds = 2000
lastMctsSearchSize = 0

initSurface = pygame.Surface((screen.get_width(), screen.get_height()), SRCALPHA)
boardSurface = pygame.Surface((screen.get_width(), screen.get_height()), SRCALPHA)
buttonSurface = pygame.Surface((screen.get_width(), screen.get_height()), SRCALPHA)
timerSurface = pygame.Surface((screen.get_width(), screen.get_height()), SRCALPHA)
turnSurface = pygame.Surface((screen.get_width(), screen.get_height()), SRCALPHA)
gameResultSurface = pygame.Surface((screen.get_width(), screen.get_height()), SRCALPHA)
notesSurface = pygame.Surface((615, 110), SRCALPHA)

#Pawn promotion test board
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


def showMenu():
    global player1, player2, vs_computer, gameMode, minimaxSearchDepth, mctsTimeLimitMiliseconds, useLongNotation, algorithm, isSpeedGame, network_game, computerColor

    gameMode, isSpeedGame, useLongNotation, algorithm, difficulty = menu.show_menu(screen)

    if difficulty == 1:
        minimaxSearchDepth = 1
        mctsTimeLimitMiliseconds = 1000
    elif difficulty == 2:
        minimaxSearchDepth = 2
        mctsTimeLimitMiliseconds = 2000
    elif difficulty == 3:
        minimaxSearchDepth = 3
        mctsTimeLimitMiliseconds = 3000

    if gameMode == "quit":
        pygame.quit()
        sys.exit()
    elif gameMode == "computer":
        player1 = "Gracz 1"
        player2 = "Komputer"
        vs_computer = True
    elif gameMode == "online":
        player1 = "Gracz 1"
        player2 = "Gracz 2"
        vs_computer = False
    elif gameMode == "player":
        player1 = "Gracz 1"
        player2 = "Gracz 2"
        vs_computer = False

    if gameMode == "online":
        # Get network configuration from the host menu
        network_config = menu.show_host_menu(screen)

        if isinstance(network_config, dict):
            if network_config["mode"] == "host":
                network_game = ChessNetworkGame(
                    is_host=True,
                    host=network_config["host"],
                    port=network_config["port"]
                )
                player1 = "Host"
                player2 = "Client"
                computerColor = None  # No computer player in network mode
            else:
                network_game = ChessNetworkGame(
                    is_host=False,
                    host=network_config["host"],
                    port=network_config["port"]
                )
                player1 = "Client"
                player2 = "Host"
                computerColor = None  # No computer player in network mode
        else:
            # User selected back or quit, return to main menu
            gameMode = menu.show_menu(screen)


def show_network_dialog(screen, message, option1="Yes", option2="No"):
    dialog_surface = pygame.Surface((400, 200), pygame.SRCALPHA)
    util.drawRoundedRect(dialog_surface, pygame.Rect(0, 0, 400, 200), (240, 240, 240, 240), 20, 20, 20, 20)

    # Message
    util.drawText(dialog_surface, message, fnt32, (200, 50), color_gray, "center")

    # Buttons
    button_surface = pygame.Surface((400, 200), pygame.SRCALPHA)

    yes_rect = pygame.Rect(50, 120, 140, 50)
    no_rect = pygame.Rect(210, 120, 140, 50)

    b1 = util.Button(button_surface, yes_rect, lambda: None)
    b1.text, b1.font = option1, fnt32
    b1.radius = 16
    b1.defaultColor, b1.hoverColor, b1.clickColor = color_gray, (96, 94, 90), (128, 124, 118)

    b2 = util.Button(button_surface, no_rect, lambda: None)
    b2.text, b2.font = option2, fnt32
    b2.radius = 16
    b2.defaultColor, b2.hoverColor, b2.clickColor = color_gray, (96, 94, 90), (128, 124, 118)

    util.renderButtons()

    # Center the dialog on screen
    x = (screen.get_width() - 400) // 2
    y = (screen.get_height() - 200) // 2

    # Event loop for the dialog
    dialog_running = True
    result = False

    while dialog_running:
        mousePos = pygame.mouse.get_pos()
        mouseDown, mouseUp, mousePressed = util.handleMouseLogic()

        # Check for button clicks
        if mouseUp:
            if yes_rect.collidepoint((mousePos[0] - x, mousePos[1] - y)):
                result = True
                dialog_running = False
            elif no_rect.collidepoint((mousePos[0] - x, mousePos[1] - y)):
                result = False
                dialog_running = False

        # Draw dialog
        screen.blit(dialog_surface, (x, y))
        screen.blit(button_surface, (x, y))

        # Ensure the cursor changes when hovering over buttons
        util.useHandCursor = False
        if yes_rect.collidepoint((mousePos[0] - x, mousePos[1] - y)) or \
           no_rect.collidepoint((mousePos[0] - x, mousePos[1] - y)):
            util.useHandCursor = True

        util.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    dialog_running = False
                    result = False

        pygame.display.flip()

    # Reset buttons
    util.currentButtons = []
    return result


def draw_network_nerd_view(screen, network_game, font_small, font_medium):
    if not network_game or not network_game.connected:
        return

    stats = network_game.get_network_stats()
    nerd_surface = pygame.Surface((250, 220), pygame.SRCALPHA)

    # Background with transparency
    util.drawRoundedRect(nerd_surface, pygame.Rect(0, 0, 250, 220), (240, 240, 240, 220), 10, 10, 10, 10)

    # Title
    util.drawText(nerd_surface, "Network Stats", font_medium, (125, 15), color_gray, "center")

    # Status indicators
    status_color = (50, 200, 50) if stats['connected'] else (200, 50, 50)
    pygame.draw.circle(nerd_surface, status_color, (20, 50), 8)
    util.drawText(nerd_surface, "Connected" if stats['connected'] else "Disconnected", font_small, (35, 43), color_gray, "left")

    # Connection type
    role = "Host" if stats['is_host'] else "Client"
    util.drawText(nerd_surface, f"Role: {role}", font_small, (20, 75), color_gray)

    # IP Address
    if stats['opponent_address']:
        ip_text = f"Peer: {stats['opponent_address'][0]}:{stats['opponent_address'][1]}"
        util.drawText(nerd_surface, ip_text, font_small, (20, 95), color_gray)

    # Ping
    util.drawText(nerd_surface, f"Ping: {stats['ping']}", font_small, (20, 115), color_gray)

    # Response time
    util.drawText(nerd_surface, f"Response: {stats['response_time']}", font_small, (20, 135), color_gray)

    # Connection duration
    minutes, seconds = divmod(int(stats['connection_time']), 60)
    hours, minutes = divmod(minutes, 60)
    time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    util.drawText(nerd_surface, f"Connected for: {time_str}", font_small, (20, 155), color_gray)

    # Packet count
    util.drawText(nerd_surface, f"Packets: {stats['packet_count']}", font_small, (20, 175), color_gray)

    # Draw the surface
    screen.blit(nerd_surface, (605, 300))


def handleComputerMove(board, color, depth):
    global awaitingMove, lastMinimaxScore, lastMctsSearchSize

    startTime = pygame.time.get_ticks()

    if algorithm == "minimax":
        result = minimax(board, color, kingWhiteCoord, kingBlackCoord, depth)
        lastMinimaxScore = result[0]
    else:
        result = monteCarloTS(board, color, mctsTimeLimitMiliseconds)
        lastMctsSearchSize = result[0]

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
        util.drawText(gameResultSurface, "Szach!", fnt56, (screen.get_width() - 173, screen.get_height() - 350), color_gray,"center")

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
    global board, possibleMoves, currentPlayer, checkMate, whiteInCheck, blackInCheck, lastSearchDurationMiliseconds, selected, timePassedThisMove, kingWhiteCoord, kingBlackCoord, scroll

    if not startTime == None:
        timeElapsed = pygame.time.get_ticks() - startTime
        if currentPlayer == computerColor:
            lastSearchDurationMiliseconds = timeElapsed
        timePassedThisMove = timeElapsed / 1000
    if gameMode == "online" and network_game and network_game.connected:
        # Only send move if it's our turn
        if (network_game.is_host and currentPlayer == "w") or (not network_game.is_host and currentPlayer == "b"):
            network_game.send_move(startSquare, endSquare)

    timePassedThisMove = 0
    allMoves.append((copy.deepcopy(startSquare), copy.deepcopy(endSquare), timePassedThisMove, False))

    if startSquare.type.name == "k":
        if startSquare.type.color == "w": kingWhiteCoord = endSquare.coord
        else: kingBlackCoord = endSquare.coord

    board = movePiece(board, startSquare, endSquare, True, True)
    possibleMoves = []
    selected = None

    currentPlayer = "w" if currentPlayer == "b" else "b"
    dir = 1 if currentPlayer == "w" else -1

    drawTimers()
    drawNotes()


    scroll = 0


    # check
    whiteInCheck = check(board, "w", kingWhiteCoord)
    blackInCheck = check(board, "b", kingBlackCoord)

    kingCoord = kingWhiteCoord if currentPlayer == "w" else kingBlackCoord

    if whiteInCheck or blackInCheck:
        lastMove = allMoves[len(allMoves)-1]
        allMoves[len(allMoves)-1] = (lastMove[0], lastMove[1], lastMove[2], True)

    #checkmate
    if not getAllMoves(board, currentPlayer, dir, kingCoord, True):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        if currentPlayer == "b" and not blackInCheck or currentPlayer == "w" and not whiteInCheck:
            # Stalemate
            checkMate = "s"
        else:
            checkMate = currentPlayer

    # Play sound
    if checkMate:
        util.playSound(util.soundCheckMate)
    elif whiteInCheck or blackInCheck:
        util.playSound(util.soundCheck)
    elif endSquare.type.name != None:
        util.playSound(util.soundCapture)
    else:
        if startSquare.type.color == "w":
            util.playSound(util.soundMoveWhite)
        else:
            util.playSound(util.soundMoveBlack)

    drawTimers()
    drawNotes()
    renderBoard()


def clickSquare():
    global awaitingMove, board, selected, possibleMoves, currentPlayer, whiteInCheck, blackInCheck, checkMate, isGameOver, minimaxThread, timePassedThisMove
    for sq in board:
        # Draw a select marker
        if gameMode == "online" and network_game:
        # Host może ruszać się tylko białymi figurami
            if network_game.is_host and currentPlayer != "w":
                return
            # Klient może ruszać się tylko czarnymi figurami
            if not network_game.is_host and currentPlayer != "b":
                return
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

                        if gameMode == "computer":
                            if checkMate: return
                            awaitingMove = True
                            minimaxThread = threading.Thread(
                                target=handleComputerMove,
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
    global awaitingMove, board, initBoard, allMoves, timer1, timer2, currentPlayer, whiteInCheck, blackInCheck, \
        checkMate, isGameOver, selected, possibleMoves, timePassedThisMove, scroll, isSpeedGame

    if awaitingMove:
        return

    allMoves = []
    board = copy.deepcopy(initBoard)
    initPieceDictionary(board)
    if isSpeedGame:
        timer1 = 5 * 60 + 0.95
        timer2 = 5 * 60 + 0.95
    else:
        timer1 = 10 * 60 + 0.95
        timer2 = 10 * 60 + 0.95
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

    scroll = 0

    drawTimers()
    drawNotes()
    renderBoard()


def restartGame():
    if awaitingMove:
        return
    global framesPassed
    resetBoard()
    framesPassed = 0
    util.clearButtons()

    showMenu()
    drawInit()


def undo(final = False):
        global allMoves, awaitingMove, board, whiteInCheck, blackInCheck, currentPlayer, checkMate, isGameOver, timer1,\
            timer2, timePassedThisMove, selected, possibleMoves, kingWhiteCoord, kingBlackCoord, scroll

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

            scroll = 0

            drawTimers()
            drawNotes()
            renderBoard()


            # Undo computer's and own move
            if gameMode == "computer" and not final:
                undo(True)
            if gameMode=="online":
                undo(True)


def drawInit():
    global initSurface, kingWhiteCoord, kingBlackCoord, scrollUpBtn, scrollDownBtn, timer1, timer2

    initSurface.fill((0,0,0,0))
    # Border
    util.drawRoundedRect(initSurface, (boardCoords[0] - 4, boardCoords[1] - 4, squareSize * 8 + 8, squareSize * 8 + 8), color_gray, 20, 20, 20, 20)

    if isSpeedGame:
        timer1 = 5 * 60 + 0.95
        timer2 = 5 * 60 + 0.95
    else:
        timer1 = 10 * 60 + 0.95
        timer2 = 10 * 60 + 0.95

    # Draw the timers on start
    drawTimers()
    drawNotes()

    # Player names
    util.drawText(initSurface, player1, fnt56, (60, 615), color_gray)
    util.drawText(initSurface, player2, fnt56, (60, 20), color_gray)

    # Algebraic notes
    util.drawRoundedRect(initSurface, (605, 100, 250, 125), color_checkerwhite, 16, 16, 16, 16)

    # Buttons

    def toggleNerdView():
        global nerdViewVisible
        nerdViewVisible = not nerdViewVisible

    def scrollNotesUp():
        global scroll
        scroll += 1
        drawNotes()

    def scrollNotesDown():
        global scroll
        scroll -= 1
        drawNotes()

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

    soundBtn = util.Button(buttonSurface, Rect(750, 30, 48, 48), lambda: util.clickSound(soundBtn))
    if util.isSoundOn:
        soundBtn.image = iconSoundOn
    else:
        soundBtn.image = iconSoundOff
    soundBtn.textColor, soundBtn.textHoverColor, soundBtn.textClickColor = (0, 0, 0), (40, 40, 40), (80, 80, 80)

    b = util.Button(buttonSurface, Rect(685, 30, 48, 48), lambda: toggleNerdView())
    b.image = iconStats
    b.textColor, b.textHoverColor, b.textClickColor = (0, 0, 0), (40, 40, 40), (80, 80, 80)

    # b = util.Button(buttonSurface, Rect(627, 30, 48, 48), lambda: copyBoard())
    # b.image = iconCopy
    # b.textColor, b.textHoverColor, b.textClickColor = (0,0,0), (40, 40, 40), (80, 80, 80)

    scrollUpBtn = util.Button(buttonSurface, Rect(828, 108, 20, 20), lambda: scrollNotesUp())
    scrollUpBtn.image = iconScrollUp
    scrollUpBtn.disabled = True
    scrollUpBtn.textColor, scrollUpBtn.textHoverColor, scrollUpBtn.textClickColor = (0, 0, 0), (40, 40, 40), (80, 80, 80)

    scrollDownBtn = util.Button(buttonSurface, Rect(828, 198, 20, 20), lambda: scrollNotesDown())
    scrollDownBtn.image = iconScrollDown
    scrollDownBtn.disabled = True
    scrollDownBtn.textColor, scrollDownBtn.textHoverColor, scrollDownBtn.textClickColor = (0, 0, 0), (40, 40, 40), (80, 80, 80)

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
            util.drawText(notesSurface, f"{count + 1}.", fnt26, (5, (count - absolute + scroll) * 25, 20, 20), color_gray)

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
                if not useLongNotation:
                    strg += "x"
                    strg += letters[m[1].coord[0]]
                strg += str(8 - m[1].coord[1])
        else:
            strg += m[0].type.name.upper()
            if m[1].type.name != None and not useLongNotation: strg += "x"
            strg += letters[m[1].coord[0]]
            strg += str(8 - m[1].coord[1])

        if useLongNotation:
            if m[1].type.name == None:
                strg += "-"
            else:
                strg += "x"
            strg += letters[m[1].coord[0]]
            strg += str(8 - m[1].coord[1])

        if m[3] and not checkMate:
            strg += "+"
        if pos == 0:
            pos = 75
        else:
            pos = 160

        if checkMate and i == len(allMoves)-1: strg += "#"
        if useLongNotation:
            util.drawText(notesSurface, f"{strg}", fnt18, (pos, 15 + (count - absolute + scroll) * 25, 20, 20), color_gray, "center", (1, 1))
        else:
            util.drawText(notesSurface, f"{strg}", fnt26,(pos, 15 + (count - absolute + scroll) * 25, 20, 20), color_gray, "center", (2,2))
        last = count







        if scroll+1 > absolute: scrollUpBtn.disabled = True
        else: scrollUpBtn.disabled = False

        if -scroll+1 > 0: scrollDownBtn.disabled = True
        else: scrollDownBtn.disabled = False

    util.renderButtons()


# Pre-game initialization
showMenu()

# change the board from a list of strings to a list of Squares
for i in range(8):
    for j in range(8):
        current = j+i*8
        if board[current] == "": board[current] = Square(Rect(boardCoords[0] + j * squareSize, boardCoords[1] + i * squareSize, squareSize, squareSize), (j, i), Type(None, None))
        else: board[current] = Square(Rect(boardCoords[0] + j * squareSize, boardCoords[1] + i * squareSize, squareSize, squareSize), (j,i), Type(board[current][1].lower(), board[current][0]))

initBoard = copy.deepcopy(board)

initPieceDictionary(board)

run = True

print("Inicjalizacja szachownicy")
drawInit()
print("Szachownica zainicjalizowana")

print("Renderowanie szachownicy")
renderBoard()
print("Szachownica wyrenderowana")

# Game loop
while run:
    if not gameMode: continue
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
            util.drawText(gameResultSurface, "Szach mat!", fnt56, (screen.get_width() - 173, screen.get_height() - 345), color_gray, "center")
            util.drawText(gameResultSurface, f"Wygrywa {player2}!", fnt26, (screen.get_width() - 173, screen.get_height() - 305), color_gray, "center")

        if checkMate == "b":
            util.drawText(gameResultSurface, "Szach mat!", fnt56, (screen.get_width() - 173, screen.get_height() - 345), color_gray, "center")
            util.drawText(gameResultSurface, f"Wygrywa {player1}!", fnt26, (screen.get_width() - 173, screen.get_height() - 305), color_gray, "center")

        if checkMate == "s":
            util.drawText(gameResultSurface, "Pat!", fnt56, (screen.get_width() - 173, screen.get_height() - 345), color_gray, "center")
            util.drawText(gameResultSurface, f"Remis!", fnt26, (screen.get_width() - 173, screen.get_height() - 305), color_gray, "center")

    # End game by time over
    if timer1 <= 0 and not isGameOver:
        isGameOver = True
        selected = None
        possibleMoves = []
        renderBoard()
        util.drawText(gameResultSurface, "Koniec czasu!", fnt56, (screen.get_width() - 173, screen.get_height() - 345),
                      color_gray,"center")
        util.drawText(gameResultSurface, f"Wygrywa {player1}!", fnt26,
                      (screen.get_width() - 173, screen.get_height() - 305),
                      color_gray, "center")

    if timer2 <= 0 and not isGameOver:
        isGameOver = True
        selected = None
        possibleMoves = []
        renderBoard()
        util.drawText(gameResultSurface, "Koniec czasu!", fnt56, (screen.get_width() - 173, screen.get_height() - 345), color_gray,"center")
        util.drawText(gameResultSurface, f"Wygrywa {player2}!", fnt26,(screen.get_width() - 173, screen.get_height() - 305), color_gray, "center")

    # Handle network events
    if gameMode == "online" and network_game:
        network_event = network_game.handle_network_events(board)

        if network_event == "UNDO_REQUEST":
            # Show dialog asking player for permission
            undo_accepted = show_network_dialog(
                screen,
                "Opponent requests to undo last move",
                "Accept",
                "Decline"
            )
            network_game.send_undo_response(undo_accepted)
            if undo_accepted:
                undo(final=True)  # Undo the last move

        elif network_event == "UNDO_ACCEPTED":
            # Opponent accepted our undo request
            undo(final=True)

        elif network_event == "UNDO_REJECTED":
            # Opponent rejected our undo request
            show_network_dialog(screen, "Undo request declined", "OK", "")

        elif network_event == "CONNECTION_LOST":
            # Connection lost - show message
            show_network_dialog(screen, "Connection lost", "OK", "")

        elif isinstance(network_event, tuple):
            # Received a move from opponent
            start_square, end_square = network_event
            handlePieceMove(start_square, end_square)

    # Draw network nerd view if enabled
    if gameMode == "online" and network_game and network_nerd_view_visible:
        draw_network_nerd_view(screen, network_game, fnt16, fnt26, color_gray)

    # Clean up network connection on exit
    if gameMode == "online" and network_game:
        network_game.close_connection()

    # Nerd View
    if nerdViewVisible:
        if gameMode == "computer":
            difficulties = {1: "Latwy", 2:"Sredni", 3:"Trudny"}
            if algorithm == "minimax":
                util.drawText(screen, "Wynik minimax: " + str(round(lastMinimaxScore, 2)), fnt16, (screen.get_width() - 4, screen.get_height() - 122), color_gray, "topright", (0,0))
                util.drawText(screen, "Czas minimax: " + str(lastSearchDurationMiliseconds) + "ms", fnt16, (screen.get_width() - 4, screen.get_height() - 102), color_gray, "topright", (0,0))
            else:
                util.drawText(screen, "Ostatnio przeszukanych opcji: " + str(lastMctsSearchSize), fnt16, (screen.get_width() - 4, screen.get_height() - 102), color_gray, "topright", (0,0))
            util.drawText(screen, "Poziom trudnosci: " + str(minimaxSearchDepth)+" ("+difficulties[minimaxSearchDepth]+")", fnt16,(screen.get_width() - 4, screen.get_height() - 82), color_gray, "topright", (0, 0))

        util.drawText(screen, "Tryb gry: " + str(gameMode), fnt16, (screen.get_width() - 4, screen.get_height() - 62), color_gray, "topright", (0,0))
        util.drawText(screen, "Kursor: " + str(mousePos), fnt16, (screen.get_width() - 4, screen.get_height() - 42), color_gray, "topright", (0,0))
        util.drawText(screen, "Fps: " + str(round(timer.get_fps())), fnt16, (screen.get_width() - 4, screen.get_height() - 22), color_gray, "topright", (0,0))

    # Handle events
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                event.y = 1
                if not scrollUpBtn.disabled:
                    scroll += event.y
            else:
                event.y = -1
                if not scrollDownBtn.disabled:
                    scroll += event.y

            drawNotes()

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

    pygame.display.flip()

pygame.quit()

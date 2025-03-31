import math as pymath
import pygame
import pyperclip
import select
import time
import networkchess

from pygame.locals import *
import threading
import util
from networkchess import*
from engine import *

from minimax import *
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
secondsPassed = 0
framesPassed = 0
serwer = True

currentPlayer = 'w'
computerColor = "b"
allMoves = []
possibleMoves = []
isCheck = None
checkMate = None
isGameOver = False
network_game = None
network_nerd_view_visible = False
network_game = None

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

board = ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR",
         "bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP",
         "", "", "", "", "", "", "", "",
         "", "", "", "", "", "", "", "",
         "", "", "", "", "", "", "", "",
         "", "", "", "", "", "", "", "",
         "wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP",
         "wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]


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
if game_mode == "online":
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
        game_mode = menu.show_menu(screen)

# if game_mode == "online" and not host_choice:
#     # Odwróć planszę dla klienta (grającego czarnymi)
#     board = ["wR", "wN", "wB", "wK", "wQ", "wB", "wN", "wR",
#              "wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP",
#              "", "", "", "", "", "", "", "",
#              "", "", "", "", "", "", "", "",
#              "", "", "", "", "", "", "", "",
#              "", "", "", "", "", "", "", "",
#              "bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP",
#              "bR", "bN", "bB", "bK", "bQ", "bB", "bN", "bR"]


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

# Add a toggle button for network nerd view
if game_mode == "online" and network_game:
    b = util.Button(buttonSurface, Rect(605, 625, 180, 25), lambda: toggle_network_nerd_view())
    b.text, b.font = "Network Stats", fnt16
    b.radius = 8
    b.textShadowRect = (1, 1)
    b.defaultColor, b.hoverColor, b.clickColor = color_gray, (96, 94, 90), (128, 124, 118)
    
    def toggle_network_nerd_view():
        global network_nerd_view_visible
        network_nerd_view_visible = not network_nerd_view_visible
    
    util.renderButtons()



for i in range(8):
    for j in range(8):
        current = j+i*8
        if board[current] == "": board[current] = Square(Rect(boardCoords[0] + j * squareSize, boardCoords[1] + i * squareSize, squareSize, squareSize), (j, i), Type(None, None))
        else: board[current] = Square(Rect(boardCoords[0] + j * squareSize, boardCoords[1] + i * squareSize, squareSize, squareSize), (j,i), Type(board[current][1].lower(), board[current][0]))

initBoard = [i for i in board]

initPieceDictionary(board)

def draw_network_nerd_view(screen, network_game, font_small, font_medium, color_gray):
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
    util.drawText(nerd_surface, "Connected" if stats['connected'] else "Disconnected", 
                 font_small, (35, 43), color_gray, "left")
    
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
def handleMinimax(board, color, depth):
    global awaitingMove, lastMinimaxScore

    startTime = pygame.time.get_ticks()

    result = minimax(board, color, depth)
    lastMinimaxScore = result[0]
    move = result[1]

    startSquare = getBoardFromCoord(board, move[0])
    endSquare = getBoardFromCoord(board, move[1])
    handlePieceMove(startSquare, endSquare, startTime)

    awaitingMove = False

    return


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
    if isCheck:
        drawColorSquare(boardSurface, isCheck.coord, (255, 90, 84, 64))

    if isCheck and not isGameOver:
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
    global board, possibleMoves, currentPlayer, checkMate, isCheck, lastSearchDurationMiliseconds, selected, timePassedThisMove

    if not startTime == None:
        timeElapsed = pygame.time.get_ticks() - startTime
        if currentPlayer == computerColor:
            lastSearchDurationMiliseconds = timeElapsed
        timePassedThisMove = timeElapsed / 1000

    allMoves.append((startSquare, endSquare, timePassedThisMove))
    timePassedThisMove = 0
    board = movePiece(board, startSquare, endSquare, True)
    possibleMoves = []
    selected = None

    currentPlayer = "w" if currentPlayer == "b" else "b"
    dir = 1 if currentPlayer == "w" else -1
    drawTimers()
    drawNotes()
    if game_mode == "online" and network_game and network_game.connected:
        # Only send move if it's our turn
        if (network_game.is_host and currentPlayer == "w") or (not network_game.is_host and currentPlayer == "b"):
            network_game.send_move(startSquare, endSquare)

    #check
    isCheck = check(board)

    #checkmate
    #print(getAllMoves(board, currentPlayer, dir, True))
    if getAllMoves(board, currentPlayer, dir, True) == []:
        checkMate = currentPlayer
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    renderBoard()


def clickSquare():
    global awaitingMove, board, selected, possibleMoves, currentPlayer, isCheck, checkMate, isGameOver, minimaxThread, timePassedThisMove
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
                        possibleMoves = calculateMoves(board, sq.coord, sq.type.name, sq.type.color, dir, True)
                    renderBoard()
                
                # Move a piece
                else:
                    if possibleMoves.__contains__(hover) and selected is not None:
                        handlePieceMove(selected, hover)

                        if game_mode == "computer":
                            awaitingMove = True
                            minimaxThread = threading.Thread(
                                target=handleMinimax,
                                name="minimax",
                                args=(board, currentPlayer, minimaxSearchDepth)
                            )
                            minimaxThread.daemon = True
                            minimaxThread.start()


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
        global awaitingMove, board, initBoard, allMoves, timer1, timer2, currentPlayer, isCheck, checkMate, isGameOver, selected, possibleMoves, timePassedThisMove
        if awaitingMove:
            return

        allMoves = []
        board = initBoard
        initPieceDictionary(board)
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

    def undo(final = False):
        global allMoves, awaitingMove, board, isCheck, currentPlayer, checkMate, isGameOver, timer1, timer2, timePassedThisMove, selected, possibleMoves

        if awaitingMove:
            return

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

            # Undo the move in the dictionary
            pieceDictionary[m[0].type.color + m[0].type.name][m[0].coord] = m[0]
            del pieceDictionary[m[0].type.color + m[0].type.name][m[1].coord]
            if m[1].type.name != None: pieceDictionary[m[1].type.color + m[1].type.name][m[1].coord] = m[1]

            # Undo computer's and own move
            if game_mode == "computer" and not final:
                undo(True)
            if game_mode=="online":
                undo(True)

    def toggleNerdView():
        global nerdViewVisible
        nerdViewVisible = not nerdViewVisible

    def copyBoard():
        boardTxt = "["
        for sq in board:
            if sq.type.name == None: boardTxt += '""'
            else: boardTxt += '"'+sq.type.color+sq.type.name.upper()+'"'
            boardTxt += ", "
            if sq.coord[0] == 7 and sq.coord[1] != 7: boardTxt += "\n"
        boardTxt += "]"
        pyperclip.copy(boardTxt)

    b = util.Button(buttonSurface, Rect(605, 250, 115, 45), lambda: undo())
    b.text, b.font = "Cofnij", fnt32
    b.radius = 16
    b.defaultColor, b.hoverColor, b.clickColor = color_gray, (96, 94, 90), (128, 124, 118)

    b = util.Button(buttonSurface, Rect(740, 250, 115, 45), lambda: reset())
    b.text, b.font = "Reset", fnt32
    b.radius = 16
    b.defaultColor, b.hoverColor, b.clickColor = color_gray, (96, 94, 90), (128, 124, 118)

    b = util.Button(buttonSurface, Rect(605, 655, 115, 25), lambda: copyBoard())
    b.text, b.font = "Kopiuj tablice", fnt16
    b.radius = 8
    b.textShadowRect = (1,1)
    b.defaultColor, b.hoverColor, b.clickColor = color_gray, (96, 94, 90), (128, 124, 118)

    if game_mode == "computer":
        b = util.Button(buttonSurface, Rect(605, 625, 115, 25), lambda: toggleNerdView())
        b.text, b.font = "Statystyki", fnt16
        b.radius = 8
        b.textShadowRect = (1, 1)
        b.defaultColor, b.hoverColor, b.clickColor = color_gray, (96, 94, 90), (128, 124, 118)

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

        square = util.drawRoundedRect(initSurface, sq.rect, clr, rds[0], rds[1], rds[2], rds[3])


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




run = True

print("Inicjalizacja szachownicy")
drawInit()
print("Szachownica zainicjalizowana")

print("Renderowanie szachownicy")
renderBoard()
print("Szachownica wyrenderowana")

while run:
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
    if game_mode == "online" and network_game:
        print(f"Obecny stan: {currentPlayer}, Host: {network_game.is_host}")
        network_event = network_game.handle_network_events(board)
        print(f"Odebrane zdarzenie: {network_event}")

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

    # Debug
    # util.drawText(screen, "MouseUp: " + str(mouseUp), fnt16, (screen.get_width() - 4, screen.get_height() - 102), color_gray, "topright")
    # util.drawText(screen, "Selected: " + str(selected), fnt16, (screen.get_width() - 4, screen.get_height() - 82), color_gray, "topright")
    # util.drawText(screen, "Hover: " + str(hover), fnt16, (screen.get_width() - 4, screen.get_height() - 62), color_gray, "topright")
    # util.drawText(screen, "Mouse Pos: " + str(mousePos), fnt16, (screen.get_width() - 4, screen.get_height() - 42), color_gray, "topright")
    # util.drawText(screen, "Time Passed: " + str(round(timePassedThisMove, 4)), fnt32, (screen.get_width() - 4, screen.get_height() - 112), color_gray, "topright")
    # util.drawText(screen, "Timer1: " + str(round(timer1, 4)), fnt32, (screen.get_width() - 4, screen.get_height() - 82), color_gray, "topright")
    # util.drawText(screen, "Timer2: " + str(round(timer2, 4)), fnt32, (screen.get_width() - 4, screen.get_height() - 52), color_gray, "topright")
    util.drawText(screen, "Fps: " + str(round(timer.get_fps())), fnt16, (screen.get_width() - 28, screen.get_height() - 36), color_gray, "topright", (0,0))
   
    if game_mode == "online" and network_game:
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
if game_mode == "online" and network_game and network_nerd_view_visible:
    draw_network_nerd_view(screen, network_game, fnt16, fnt26, color_gray)

# Clean up network connection on exit
if game_mode == "online" and network_game:
    network_game.close_connection()
    # Nerd View
    if nerdViewVisible:
        util.drawText(screen, "Wynik minimax: " + str(round(lastMinimaxScore, 2)), fnt16, (screen.get_width() - 28, screen.get_height() - 72), color_gray, "topright", (0,0))
        util.drawText(screen, "Czas minimax: " + str(lastSearchDurationMiliseconds) + "ms", fnt16, (screen.get_width() - 28, screen.get_height() - 54), color_gray, "topright", (0,0))

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
    pygame.draw.rect(screen, (255, 0, 0), (100, 100, 200, 200))
pygame.quit()

import math
from engine import *

def scoreBlack(board, kingWhiteCoord, kingBlackCoord, currentPlayer = "b"):
    global pieceDictionary

    # parameters
    VALUE_WEIGHT = 4.0
    DISTANCE_FROM_CENTER_WEIGHT = 1.0
    KING_SAFETY_WEIGHT = 0.5
    CONTROL_WEIGHT = 0.05

    # check for checkmate and stalemate
    dir = 1 if currentPlayer == "w" else -1
    kingCoord = kingWhiteCoord if currentPlayer == "w" else kingBlackCoord
    enemyPlayer = "b" if currentPlayer == "w" else "w"
    enemyKingCoord = kingWhiteCoord if currentPlayer == "b" else kingBlackCoord

    avaibleMoves = dictGetAllMoves(board, currentPlayer, dir, kingCoord, True)
    hasMoves = len(avaibleMoves) != 0
    if (not hasMoves):
        playerInCheck = check(board, currentPlayer, kingCoord)
        enemyInCheck = check(board, enemyPlayer, enemyKingCoord)

        if playerInCheck and enemyInCheck:
            # stalemate
            return 0
        elif playerInCheck:
            return math.inf
        else:
            return -math.inf

    # create an array with pieces only:
    pieceSquares = [square for square in board if square.type.name != None]

    # score based on piece values:
    pieceValues = 0
    for key in pieceDictionary.keys():
        if not pieceDictionary[key]:
            continue

        value = 0
        match key[1]:
            case "p": # pawn
                value = 1
            case "n": # knight
                value = 3
            case "b": # bishop
                value = 3
            case "r": # rook
                value = 5
            case "q": # queen
                value = 9

        value *= len(pieceDictionary[key])
        
        if key[0] == "w":
            value = -value
        
        pieceValues += value

    # score based on distance from centre:
    distanceScore = 0
    for piece in pieceSquares:
        if piece.type.name == "k" or piece.type.name == "p":
            # ignore kings and pawns
            continue
        
        score = 5 - math.dist(piece.coord, (3.5, 3.5))
        if piece.type.color == "w":
            score = -score
        
        distanceScore += score

    # score based on king safety:
    kingSafety = 0

    # iterate over neighbouring squares:
    for i in range(3):
        for j in range(3):
            checkedPosition = (kingCoord[0] + i, kingCoord[1] + j)
            checkedSquare = getBoardFromCoord(board,checkedPosition)
            if checkedSquare == None:
                kingSafety += 0.11
                continue

            if checkedSquare.type.color == "w":
                kingSafety += 0.11

    # score based on board control:
    controlScore = 0
    for move in avaibleMoves:
        controlScore += 10 - math.dist(move.coord, (3.5, 3.5))
    controlScore / 64


    return VALUE_WEIGHT * pieceValues + DISTANCE_FROM_CENTER_WEIGHT * distanceScore + KING_SAFETY_WEIGHT * kingSafety + CONTROL_WEIGHT * controlScore

# returns best score found and corresponding move, formatted as:
# [moveScore, [(StartX, StartY), (EndX, EndY)] ]
def minimax(board, color, kingWhiteCoord, kingBlackCoord, recursionsLeft, alphaBetaLimit = None):
    if (recursionsLeft == 0):
        return [scoreBlack(board, kingWhiteCoord, kingBlackCoord), None]

    kingCoord = kingWhiteCoord if color == "w" else kingBlackCoord
    
    # create an array of possible moves formatted as:
    # [start position, end position]
    moves = []
    for square in board:
        if (square.type.color != color):
            continue

        dir = 1 if color == "w" else -1
        possibleMoves = calculateMoves(board, square.coord, square.type.name, square.type.color, dir, kingCoord, True)
        for possibleMove in possibleMoves:
            moves.append([square.coord, possibleMove.coord])

    bestMove = None

    if (color == 'b'):
        # calculate for black:
        maxValue = -math.inf
        
        for move in moves:
            value = minimax(overridingMovePiece(board, move[0], move[1]), 'w', kingWhiteCoord, kingBlackCoord, recursionsLeft - 1, maxValue)[0]
            undoLastOverride()

            if (alphaBetaLimit != None and value > alphaBetaLimit):
                return [value, move]
            if (value > maxValue):
                maxValue = value
                bestMove = move

        return [maxValue, bestMove]
    
    else:
        # calculate for white:
        minValue = math.inf

        for move in moves:
            value = minimax(overridingMovePiece(board, move[0], move[1]), 'b', kingWhiteCoord, kingBlackCoord, recursionsLeft - 1, minValue)[0]
            undoLastOverride()

            if (alphaBetaLimit != None and value < alphaBetaLimit):
                return [value, move]
            if (value < minValue):
                minValue = value
                bestMove = move
        
        return [minValue, bestMove]
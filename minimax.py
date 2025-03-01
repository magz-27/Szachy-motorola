import math
from engine import movePiece, calculateMoves, getAllMoves, check, coordToBoardIndex

def scoreBlack(board, currentPlayer = "b"):
    # parameters
    VALUE_WEIGHT = 4.0
    DISTANCE_FROM_CENTER_WEIGHT = 1.0
    KING_SAFETY_WEIGHT = 0.5
    CONTROL_WEIGHT = 2.0

    # check for checkmate and stalemate
    dir = 1 if currentPlayer == "w" else -1
    avaibleMoves = getAllMoves(board, currentPlayer, dir)
    hasMoves = len(avaibleMoves) != 0
    if (not hasMoves):
        checkedSquare = check(board)

        if (checkedSquare != None):
            # checkmate
            return math.inf if checkedSquare.type.color == currentPlayer else -math.inf
        else:
            # stale mate
            return 0

    # create an array with pieces only:
    pieceSquares = [square for square in board if square.type.name != None]

    # score based on piece values:
    pieceValues = 0
    for piece in pieceSquares:
        value = 0
        match piece.type.name:
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
        
        if piece.type.color == "w":
            value = -value
        
        pieceValues += value

    # score based on distance from centre:
    distanceScore = 0
    for piece in pieceSquares:
        if (piece.type.name == "k" or piece.type.name == "p"):
            # ignore kings and pawns
            continue
        
        score = 5 - math.dist(piece.coord, (3.5, 3.5))
        if piece.type.color == "w":
            score = -score
        
        distanceScore += score

    # score based on king safety:
    kingSafety = 0
    kingPosition = (0,0)
    for piece in pieceSquares:
        if piece.type.name == "k" and piece.type.color == currentPlayer:
            kingPosition = piece.coord
            kingPosition[0] -= 1
            kingPosition[1] -= 1
            break

    # iterate over neighbouring squares:
    for i in range(3):
        for j in range(3):
            checkedPosition = (kingPosition[0] + i, kingPosition[1] + j)
            index = coordToBoardIndex(checkedPosition)
            if checkedPosition[0] > 7 or checkedPosition[0] < 0 or checkedPosition[1] > 7 or checkedPosition[0] < 0:
                kingSafety += 0.11
                continue

            if board[index].type.color == "w":
                kingSafety += 0.11

    # score based on board control:
    controlScore = 0
    for move in avaibleMoves:
        controlScore += 10 - math.dist(move.coord, (3.5, 3.5))


    return VALUE_WEIGHT * pieceValues + DISTANCE_FROM_CENTER_WEIGHT * distanceScore + KING_SAFETY_WEIGHT * kingSafety + CONTROL_WEIGHT * controlScore

def minimax(board, color, recursionsLeft):
    if (recursionsLeft == 0):
        return [scoreBlack(board), None]
    
    # create an array of possible moves formatted as:
    # [start position, end position]
    moves = []
    for square in board:
        if (square.type.color != color):
            continue

        dir = 1 if color == "w" else -1
        possibleMoves = calculateMoves(board, square.coord, square.type.name, square.type.color, dir)
        for possibleMove in possibleMoves:
            moves.append([square.coord, possibleMove.coord])

    bestMove = None

    if (color == 'b'):
        # calculate for black:
        maxValue = -math.inf
        
        for move in moves:
            value = minimax(movePiece(board, move[0], move[1]), 'w', recursionsLeft - 1)[0]
            if (value > maxValue):
                maxValue = value
                bestMove = move

        return [maxValue, bestMove]
    
    else:
        # calculate for white:
        minValue = math.inf

        for move in moves:
            value = minimax(movePiece(board, move[0], move[1]), 'b', recursionsLeft - 1)[0]
            if (value < minValue):
                minValue = value
                bestMove = move
        
        return [minValue, bestMove]

def minimaxMove(board, color, depth):
    move = minimax(board, color, depth)[1]
    return movePiece(board, move[0], move[1])

def printSquares(squares):
    for square in squares:
        print(square.coord)
import math
from engine import movePiece, calculateMoves

def scoreBlack(board):
    # TODO: Evaluate black's position:
    return 0

def minimax(board, color, recursionsLeft):
    if (recursionsLeft == 1):
        pass

    if (recursionsLeft == 0):
        return [scoreBlack(board), None]
    
    # Create an array of possible moves formatted as:
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
        # Calculate for black:
        maxValue = -math.inf
        
        for move in moves:
            value = minimax(movePiece(board, move[0], move[1]), 'w', recursionsLeft - 1)[0]
            if (value > maxValue):
                maxValue = value
                bestMove = move
        return [maxValue, bestMove]
    else:
        # Calculate for white:
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
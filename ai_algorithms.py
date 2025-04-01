import copy
import math
import random
from engine import *


###########
# MINIMAX 
############


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

    # TODO: correct 
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
            moves.append(copy.deepcopy([square.coord, possibleMove.coord]))

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
    

###########
# MONTE CARLO TREE SEARCH 
############

MCTS_UCT_CONSTANT = 1.5

# (in a simulation) how many moves without captures to allow before declaring a draw.
MCTS_PEACEFUL_MOVE_LIMIT = 15

class mctsNode:
    def __init__(self, parent, move = None, blacksTurn = True):
        self.parent = parent
        self.children = []

        self.move = move
        self.blacksTurn = blacksTurn

        self.wins = 0
        self.simulations = 0

COPY = 0
def monteCarloTS(board, color, timeLimitMiliseconds):
    global COPY
    startTime = pygame.time.get_ticks()

    root = mctsNode(None)
    root.blacksTurn = color == "b"
    nodesSearched = 0

    while (pygame.time.get_ticks() - startTime < timeLimitMiliseconds):
        traversingResult = mctsTraverse(board,root)
        simulationResult = mctsSimulate(traversingResult[0], traversingResult[1])
        newLeaf = traversingResult[1].children[-1]
        mctsBackpropagate(newLeaf, simulationResult)
        nodesSearched += 1

    bestFoundMove = None
    mostSimulations = 0

    print(COPY)

    for child in root.children:
        if (child.simulations > mostSimulations):
            mostSimulations = child.simulations
            bestFoundMove = child.move

    return [nodesSearched, bestFoundMove]

def mctsUCT(node: mctsNode):
    global MCTS_UCT_CONSTANT

    maxScore = 0
    bestId = 0
    for i, child in enumerate(node.children):
        childScore = (child.wins/child.simulations) + MCTS_UCT_CONSTANT * math.sqrt((math.log(node.simulations))/child.simulations)
        if childScore > maxScore:
            maxScore = childScore
            bestId = i

    return node.children[bestId]

def findKingPosition(color):
    global pieceDictionary
    key = color + "k"
    for pos in pieceDictionary[key].keys():
        return pos
    
def resetDictionary(sourceDictionary: dict):
    global pieceDictionary

    pieceDictionary.clear()
    for key, value in sourceDictionary.items():
        pieceDictionary[key] = value

def mctsTraverse(board,node):
    global pieceDictionary

    boardCopy = copy.deepcopy(board)
    color = "b" if node.blacksTurn else "w"

    availableMoves = mctsGetAllMoves(boardCopy, color, findKingPosition(color))

    dictSave = copy.deepcopy(pieceDictionary)

    while len(node.children) >= len(availableMoves):
        if node.move != None:
            boardCopy = movePiece(boardCopy, node.move[0], node.move[1], updateDict=True)
        
        if len(node.children) == 0:
            resetDictionary(dictSave)
            return [boardCopy, node]
        
        node = mctsUCT(node)

        color = "b" if node.blacksTurn else "w"

        availableMoves = mctsGetAllMoves(boardCopy, color, findKingPosition(color))

    resetDictionary(dictSave)

    return [boardCopy,node]


def mctsRandomPieceMoves(board, color):
    global pieceDictionary

    pieces = []


    types = list(pieceDictionary.keys())
    for type in types:
        if type[0] == color:
            pieces.extend(list(pieceDictionary[type].values()))

    pieces = randomPermutation(pieces)

    for piece in pieces:
        moves = calculateMoves(board, piece.coord, piece.type.name, color, 1 if color == "w" else -1, findKingPosition(color), True)
        if len(moves) > 0:
            return [piece, moves]

def mctsSimulate(board,node):
    global changesStack, pieceDictionary
    global COPY

    dictSave = copy.deepcopy(pieceDictionary)
    stackSave = copy.deepcopy(changesStack)

    if node.move != None:
        board = overridingMovePiece(board, node.move[0], node.move[1])

    color = "b" if node.blacksTurn else "w"

    availableMoves = mctsGetAllMoves(board, color, findKingPosition(color))

    state = 0

    movesSinceLastCapture = 0

    if len(availableMoves) != 0:
        initialMoveSquare = availableMoves[len(node.children)]
        initialMove = [initialMoveSquare[0].coord, initialMoveSquare[1].coord]

        # expansion
        childNode = mctsNode(node, initialMove, not node.blacksTurn)
        node.children.append(childNode)
        board = overridingMovePiece(board, initialMove[0], initialMove[1])

        # simulation
        blacksTurn = childNode.blacksTurn
        state = gameState(board, findKingPosition("w"), findKingPosition("b"), blacksTurn)[0]

        availableMoves = None
        while (state == "0"):
            color = "b" if blacksTurn else "w"
            if availableMoves == None:
                availableMoves = mctsGetAllMoves(board, color, findKingPosition(color))
            
            if len(availableMoves) == 0:
                if color == "b":
                    state = gameState(board, findKingPosition("w"), findKingPosition("b"), blacksTurn, blackMoveCount=len(availableMoves))[0]
                else:
                    state = gameState(board, findKingPosition("w"), findKingPosition("b"), blacksTurn, whiteMoveCount=len(availableMoves))[0]
                break
            
            # perform random moves
            moveSquare = random.choice(availableMoves)
            move = [moveSquare[0].coord, moveSquare[1].coord]


            movesSinceLastCapture += 1
            if (getBoardFromCoord(board, move[1]).type.color != None):
                movesSinceLastCapture = 0
            if movesSinceLastCapture == MCTS_PEACEFUL_MOVE_LIMIT:
                # declare a draw after a given amount of moves without piece captures
                state = "d"
                break

            board = overridingMovePiece(board, move[0], move[1])
            blacksTurn = not blacksTurn
            if color == "b":
                state, availableMoves = gameState(board, findKingPosition("w"), findKingPosition("b"), blacksTurn, blackMoveCount=len(availableMoves))
            else:
                state, availableMoves = gameState(board, findKingPosition("w"), findKingPosition("b"), blacksTurn, whiteMoveCount=len(availableMoves))


    else:
        state = gameState(board, findKingPosition("w"), findKingPosition("b"), node.blacksTurn)[0]


    # reverse made changes:
    resetDictionary(dictSave)
    changesStack.clear()
    changesStack.extend(stackSave)


    if state == "d":
        return 0
    
    if state == "b":
        return 1 if node.blacksTurn else -1
    else:
        return -1 if node.blacksTurn else 1

def mctsBackpropagate(node, result):
    while(node.parent != None):
        node.simulations += 1
        node.wins += result
        
        result = -result
        node = node.parent

    node.simulations += 1
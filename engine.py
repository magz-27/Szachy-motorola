import pygame
from pygame.locals import *

# stores lists of existing pieces sorted by color and type,
# with keys formatted as "color" + "name":
# eg. pieceDictionary["wp"] is a list of all white pawns on board
pieceDictionary = {}


def initPieceDictionary(board):
    global pieceDictionary
    
    for square in board:
        if square == None or square.type.color == None or square.type.name == None:
            continue
        
        key = square.type.color + square.type.name

        if key in pieceDictionary:
            pieceDictionary[key][square.coord] = square
            continue

        pieceDictionary[key] = {square.coord: square}


def getBoardFromCoord(board, coord):
    if coord[0] > 7 or coord[0] < 0 or coord[1] > 7 or coord[1] < 0:
        return None
    index = coord[0] + coord[1] * 8
    return board[index]
   

def invertBoard(board):
    newBoard = []
    for sq in board:
        newBoard.append(Square(Rect(-64+50+8*64-64*sq.coord[0], -64+90+8*64-64*sq.coord[1], 64, 64), (7-sq.coord[0], 7-sq.coord[1]), sq.type))
    newBoard.reverse()
    return newBoard


class Square:
    def __init__(self, rect: pygame.Rect, coord, type):
        self.rect = rect
        self.coord = coord
        self.type = type

    def __str__(self):
        return f'{self.type.getColor()} {self.type.getName()}, {self.coord}'

    def getName(self):
        return f'{self.type.getColor()} {self.type.getName()}, {self.coord}'

    def __eq__(self, other):
        if not isinstance(other, Square):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.rect == other.rect and self.coord == other.coord and self.type == other.type


class Type:
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def getName(self):
        if self.name == "p":
            return "Pawn"
        elif self.name == "r":
            return "Rook"
        elif self.name == "n":
            return "Knight"
        elif self.name == "b":
            return "Bishop"
        elif self.name == "q":
            return "Queen"
        elif self.name == "k":
            return "King"

    def getColor(self):
        if self.color == "w":
            return "Light"
        elif self.color == "b":
            return "Dark"

    def invertColor(self, color):
        if color == "w":
            return "b"
        elif color == "b":
            return "w"

    def __eq__(self, other):
        if not isinstance(other, Type):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.color == other.color and self.name == other.name


def getAllMoves(board, color, direction, kingCoord, onlyLegal=False):
    moves = []
    for sq in board:
        if sq.type.color == color:
            moves.extend(calculateMoves(board, sq.coord, sq.type.name, sq.type.color, direction, kingCoord, onlyLegal))
    return moves


def dictGetAllMoves(globalBoard, color, direction, kingCoord, onlyLegal=False):
    global pieceDictionary

    moves = []
    for key in pieceDictionary.keys():
        if key[0] != color:
            continue
        for sq in pieceDictionary[key].values():
            moves.extend(calculateMoves(globalBoard, sq.coord, sq.type.name, sq.type.color, direction, kingCoord, onlyLegal))
    return moves


def mctsGetAllMoves(globalBoard, color, kingCoord):
    global pieceDictionary

    moves = []
    direction = 1 if color == "w" else -1
    for key in pieceDictionary.keys():
        if key[0] != color:
            continue
        for sq in pieceDictionary[key].values():
            moves.extend([sq, move] for move in calculateMoves(globalBoard, sq.coord, sq.type.name, sq.type.color, direction, kingCoord, True))
    return moves


def check(board, color, kingCoord):
    # Checks only the squares that can attack the king, instead of every square on the board.
    # Checks every direction from the king, if there's a piece in the way, stops checking in that direction
    # Knights are checked separately, because they don't attack in a straight line

    orthogonalDir = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    diagonalDir = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
    knightDir = [(1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1)]
    x = kingCoord[0]
    y = kingCoord[1]
    enem = "b" if color == "w" else "w"

    isSafe = True

    for d in orthogonalDir:
        i = 1
        while True:
            testSq = getBoardFromCoord(board, (x + d[0] * i, y + d[1] * i))

            # Stops checking if the square is off the board
            if testSq == None: break

            if testSq.type.color == color:
                break
            if testSq.type.color == enem and (testSq.type.name == "r" or testSq.type.name == "q"):
                isSafe = False
                break
            if testSq.type.color == enem and (testSq.type.name == "k" and i == 1):
                isSafe = False
                break
            if testSq.type.name != None:
                break
            i += 1

    for d in diagonalDir:
        i = 1
        while True:
            testSq = getBoardFromCoord(board, (x + d[0] * i, y + d[1] * i))

            # Stops checking if the square is off the board
            if testSq == None: break

            if testSq.type.color == color:
                break
            if testSq.type.color == enem and (testSq.type.name == "b" or testSq.type.name == "q"):
                isSafe = False
                break
            if testSq.type.color == enem and (testSq.type.name == "k" or testSq.type.name == "p") and i == 1:
                isSafe = False
                break
            if testSq.type.name != None:
                break
            i += 1

    for d in knightDir:
        testSq = getBoardFromCoord(board, (x + d[0], y + d[1]))

        # Stops checking if the square is off the board
        if testSq == None: continue

        if testSq.type.color == enem and testSq.type.name == "n":
            isSafe = False

    return not isSafe


def calculateMoves(board, coord, name, color, direction, kingCoord, onlyLegal=False):
    moves = []

    # Pawn movement
    if name == "p":
        # Single
        sq = getBoardFromCoord(board, (coord[0], coord[1] - 1 * direction))
        if sq != None:
            if sq.type.name is None: moves.append(sq)

        # Double
        sq = getBoardFromCoord(board, (coord[0], coord[1] - 2 * direction))
        if sq != None:
            if sq.type.name is None and ((coord[1] == 6 and direction == 1) or (coord[1] == 1 and direction == -1)): moves.append(sq)

        # Left Capture
        sq = getBoardFromCoord(board, (coord[0] - 1 * direction, coord[1] - 1 * direction))
        if sq != None:
            if sq.type.invertColor(sq.type.color) == color: moves.append(sq)

        # Right Capture
        sq = getBoardFromCoord(board, (coord[0] + 1 * direction, coord[1] - 1 * direction))
        if sq != None:
            if sq.type.invertColor(sq.type.color) == color: moves.append(sq)

    # Rook movement
    if name == "r":
        # Up
        i = 0
        while True:
            sq = getBoardFromCoord(board, (coord[0], coord[1] - i - 1))
            if sq == None: break
            if sq.type.invertColor(sq.type.color) == color:
                moves.append(sq)
                break
            if sq.type.color == color:
                break
            moves.append(sq)
            i += 1

        # Down
        i = 0
        while True:
            sq = getBoardFromCoord(board, (coord[0], coord[1] + i + 1))
            if sq == None: break
            if sq.type.invertColor(sq.type.color) == color:
                moves.append(sq)
                break
            if sq.type.color == color:
                break
            moves.append(sq)
            i += 1

        # Left
        i = 0
        while True:
            sq = getBoardFromCoord(board, (coord[0] - i - 1, coord[1]))
            if sq == None: break
            if sq.type.invertColor(sq.type.color) == color:
                moves.append(sq)
                break
            if sq.type.color == color:
                break
            moves.append(sq)
            i += 1

        # Right
        i = 0
        while True:
            sq = getBoardFromCoord(board, (coord[0] + i + 1, coord[1]))
            if sq == None: break
            if sq.type.invertColor(sq.type.color) == color:
                moves.append(sq)
                break
            if sq.type.color == color:
                break
            moves.append(sq)
            i += 1

    # Knight movement
    if name == "n":

        sq = getBoardFromCoord(board, (coord[0] - 1, coord[1] - 2))
        if sq != None:
            if sq.type.color != color: moves.append(sq)

        sq = getBoardFromCoord(board, (coord[0] + 1, coord[1] - 2))
        if sq != None:
            if sq.type.color != color: moves.append(sq)

        sq = getBoardFromCoord(board, (coord[0] - 1, coord[1] + 2))
        if sq != None:
            if sq.type.color != color: moves.append(sq)

        sq = getBoardFromCoord(board, (coord[0] + 1, coord[1] + 2))
        if sq != None:
            if sq.type.color != color: moves.append(sq)

        sq = getBoardFromCoord(board, (coord[0] - 2, coord[1] - 1))
        if sq != None:
            if sq.type.color != color: moves.append(sq)

        sq = getBoardFromCoord(board, (coord[0] + 2, coord[1] - 1))
        if sq != None:
            if sq.type.color != color: moves.append(sq)

        sq = getBoardFromCoord(board, (coord[0] - 2, coord[1] + 1))
        if sq != None:
            if sq.type.color != color: moves.append(sq)

        sq = getBoardFromCoord(board, (coord[0] + 2, coord[1] + 1))
        if sq != None:
            if sq.type.color != color: moves.append(sq)

    # Bishop movement
    if name == "b":
        # Top left
        i = 0
        while True:
            sq = getBoardFromCoord(board, (coord[0] - i - 1, coord[1] - i - 1))
            if sq == None: break
            if sq.type.invertColor(sq.type.color) == color:
                moves.append(sq)
                break
            if sq.type.color == color:
                break
            moves.append(sq)
            i+=1

        # Top right
        i = 0
        while True:
            sq = getBoardFromCoord(board, (coord[0] + i + 1, coord[1] - i - 1))
            if sq == None: break
            if sq.type.invertColor(sq.type.color) == color:
                moves.append(sq)
                break
            if sq.type.color == color:
                break
            moves.append(sq)
            i += 1

        # Bottom left
        i = 0
        while True:
            sq = getBoardFromCoord(board, (coord[0] - i - 1, coord[1] + i + 1))
            if sq == None: break
            if sq.type.invertColor(sq.type.color) == color:
                moves.append(sq)
                break
            if sq.type.color == color:
                break
            moves.append(sq)
            i += 1

        # Bottom right
        i = 0
        while True:
            sq = getBoardFromCoord(board, (coord[0] + i + 1, coord[1] + i + 1))
            if sq == None: break
            if sq.type.invertColor(sq.type.color) == color:
                moves.append(sq)
                break
            if sq.type.color == color:
                break
            moves.append(sq)
            i += 1

    # Queen movement
    if name == "q":
        moves.extend(calculateMoves(board, coord,"r", color, direction, kingCoord))
        moves.extend(calculateMoves(board, coord, "b", color, direction, kingCoord))

    # King movement
    if name == "k":
        # Top left
        sq = getBoardFromCoord(board, (coord[0] - 1, coord[1] - 1))
        if sq != None:
            if sq.type.color != color: moves.append(sq)

        # Top middle
        sq = getBoardFromCoord(board, (coord[0], coord[1] - 1))
        if sq != None:
            if sq.type.color != color: moves.append(sq)

        # Top right
        sq = getBoardFromCoord(board, (coord[0] + 1, coord[1] - 1))
        if sq != None:
            if sq.type.color != color: moves.append(sq)

        # Middle right
        sq = getBoardFromCoord(board, (coord[0] + 1, coord[1]))
        if sq != None:
            if sq.type.color != color: moves.append(sq)

        # Bottom right
        sq = getBoardFromCoord(board, (coord[0] + 1, coord[1] + 1))
        if sq != None:
            if sq.type.color != color: moves.append(sq)

        # Bottom middle
        sq = getBoardFromCoord(board, (coord[0], coord[1] + 1))
        if sq != None:
            if sq.type.color != color: moves.append(sq)

        # Bottom left
        sq = getBoardFromCoord(board, (coord[0] - 1, coord[1] + 1))
        if sq != None:
            if sq.type.color != color: moves.append(sq)

        # Middle left
        sq = getBoardFromCoord(board, (coord[0] - 1, coord[1]))
        if sq != None:
            if sq.type.color != color: moves.append(sq)

    newMoves = []
    if onlyLegal:
        for m in moves:
            b = movePiece(board, getBoardFromCoord(board, coord), m)
            if name == "k":
                kingCoord = m.coord

            if not check(b, color, kingCoord): newMoves.append(m)

    else: newMoves = moves
    return newMoves


def movePiece(sourceBoard, sq1, sq2, updateDict = False, pawnPromotion = False):
    global pieceDictionary
    board = [Square(i.rect, i.coord, i.type) for i in sourceBoard]

    startPosition = sq1.coord if isinstance(sq1, Square) else sq1 
    endPosition = sq2.coord if isinstance(sq1, Square) else sq2 

    startSquare = getBoardFromCoord(board, startPosition)
    endSquare = getBoardFromCoord(board, endPosition)

    if updateDict and (endSquare.type.name != None):
        # remove piece from global dictionary:
        key = endSquare.type.color + endSquare.type.name
        del pieceDictionary[key][endPosition]

    if updateDict:
        key = startSquare.type.color + startSquare.type.name
        # log piece move
        pieceDictionary[key][startPosition].coord = endPosition
        pieceDictionary[key][endPosition] = pieceDictionary[key][startPosition]
        del pieceDictionary[key][startPosition]

    # pawn promotion
    if pawnPromotion and startSquare.type.name == "p":
        if (endSquare.coord[1] == 0 and startSquare.type.color == "w") or (endSquare.coord[1] == 7 and startSquare.type.color == "b"):
            if updateDict:
                del pieceDictionary[key][endPosition]
                pieceDictionary[startSquare.type.color + "q"][endPosition] = startSquare
            startSquare.type.name = "q"

    # move a piece to its destination
    endSquare.type = startSquare.type
    startSquare.type = Type(None, None)

    return board


# logs changes done with overridingMovePiece() in format:
# [ [startSquare, endSquare, endType], ... ]
changesStack = []


# moves given piece without creating a new board, modifies the current one instead.
# always updates the piece dictionary
def overridingMovePiece(board, sq1, sq2):
    global pieceDictionary
    global changesStack

    startPosition = sq1.coord if isinstance(sq1, Square) else sq1 
    endPosition = sq2.coord if isinstance(sq1, Square) else sq2 

    startSquare = getBoardFromCoord(board, startPosition)
    endSquare = getBoardFromCoord(board, endPosition)

    changesStack.append([startSquare, endSquare, endSquare.type])


    # if a piece is taken:
    if (endSquare.type.name != None):
        # remove piece from the piece dictionary:
        key = endSquare.type.color + endSquare.type.name
        del pieceDictionary[key][endPosition]

    key = startSquare.type.color + startSquare.type.name

    # remove piece from starting square
    if (startPosition != endPosition):
        del pieceDictionary[key][startPosition]

    
    # pawn promotion:
    if startSquare.type.name == "p" and ((endSquare.coord[1] == 0 and startSquare.type.color == "w") or (endSquare.coord[1] == 7 and startSquare.type.color == "b")):
        changesStack.append([startSquare, startSquare, Type("promotion", startSquare.type.color)])

        pieceDictionary[startSquare.type.color + "q"][endPosition] = Square(endSquare.rect, endPosition, Type("q", startSquare.type.color))

        endSquare.type = Type("q", startSquare.type.color)
    else:
        # put piece in the end square
        pieceDictionary[key][endPosition] = endSquare
        endSquare.type = startSquare.type
    
    startSquare.type = Type(None, None)

    return board


def undoLastOverride():
    global pieceDictionary
    global changesStack

    # change = [startSquare, endSquare, endType]
    change = changesStack.pop()

    undoPawnPromotion = False
    if change[2].name == "promotion":
        undoPawnPromotion = True
        change[2] = Type("q", change[2].type.color)


    change[0].type = change[1].type
    change[1].type = change[2]

    # update the piece dictionary
    key = change[0].type.color + change[0].type.name
    del pieceDictionary[key][change[1].coord]
    pieceDictionary[key][change[0].coord] = change[1]

    if change[2] != Type(None, None):
        key = change[2].color + change[2].name
        pieceDictionary[key][change[1].coord] = change[1]

    if undoPawnPromotion:
        # after undoing the change of piece type, undo change of piece position
        undoLastOverride()


def gameState(board, kingWhiteCoord, kingBlackCoord, blacksTurn: bool, reverseDirection = False):
    isWhiteInCheck = check(board, "w", kingWhiteCoord)
    isBlackInCheck = check(board, "b", kingBlackCoord)
    whiteMoveCount = len(getAllMoves(board, "w", -1 if reverseDirection else 1, kingWhiteCoord, True))
    blackMoveCount = len(getAllMoves(board, "b", 1 if reverseDirection else -1, kingBlackCoord, True))

    if blacksTurn:
        if blackMoveCount == 0:
            if isBlackInCheck:
                # white won
                return "w"
            
            # draw by stalemate
            return "d"
    else:
        if whiteMoveCount == 0:
            if isWhiteInCheck:
                # black won
                return "b"
            
            # draw by stalemate
            return "d"
    
    # game has not ended yet
    return "0"


def debugPreviewBoard(board):
    for i in range(8):
        str = ""
        for j in range(8):
            piece = board[8*i + j]
            if piece.type.color == None:
                str += "__ "
            else:
                str += piece.type.name + piece.type.color + " "
        print(str)
    print("-------------------------")
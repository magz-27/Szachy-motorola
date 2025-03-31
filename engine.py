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


def getAllMoves(board, color, direction, actual=False):
    moves = []
    for sq in board:
        if sq.type.color == color:
            moves.extend(calculateMoves(board, sq.coord, sq.type.name, sq.type.color, direction, actual))
    return moves

def dictGetAllMoves(globalBoard, color, direction, actual=False):
    moves = []
    for key in pieceDictionary.keys():
        if key[0] != color:
            continue
        for sq in pieceDictionary[key].values():
            moves.extend(calculateMoves(globalBoard, sq.coord, sq.type.name, sq.type.color, direction, actual))
    return moves

def check(board):
    light = getAllMoves(board, 'w', 1)
    dark = getAllMoves(board, 'b', -1)

    l = None
    d = None

    for m in light:
        if m.type.name == "k":
            l = m
    for m in dark:
        if m.type.name == "k":
            d = m
    if l and d: return l,d
    elif l: return l
    elif d: return d
    return None


def calculateMoves(board, coord, name, color, direction, actual=False):
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
        moves.extend(calculateMoves(board, coord,"r", color, direction))
        moves.extend(calculateMoves(board, coord, "b", color, direction))

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
    if actual:
        for m in moves:
            b = movePiece(board, getBoardFromCoord(board, coord), m)
            ch = check(b)
            if ch == None: newMoves.append(m)
            else:
                if type(ch) is not tuple:
                    if ch.type.color != color: newMoves.append(m)
    else: newMoves = moves
    return newMoves


def movePiece(sourceBoard, sq1, sq2, updateDict = False):
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
        # log piece move
        key = startSquare.type.color + startSquare.type.name
        pieceDictionary[key][endPosition] = pieceDictionary[key][startPosition]
        del pieceDictionary[key][startPosition]

    # move a piece to its destination
    getBoardFromCoord(board, endPosition).type = startSquare.type
    startSquare.type = Type(None, None)

    return board

# logs changes done with overridingMovePiece() in format:
# [ [startSquare, endSquare, endType], ... ]
changesStack = []

# moves given piece without creating a new board, modifies the current one instead.
def overridingMovePiece(board, sq1, sq2):
    global pieceDictionary
    global changesStack

    startPosition = sq1.coord if isinstance(sq1, Square) else sq1 
    endPosition = sq2.coord if isinstance(sq1, Square) else sq2 

    startSquare = getBoardFromCoord(board, startPosition)
    endSquare = getBoardFromCoord(board, endPosition)

    changesStack.append([startSquare, endSquare, endSquare.type])

    # always update dictionary
    if (endSquare.type.name != None):
        # remove piece from global dictionary:
        key = endSquare.type.color + endSquare.type.name
        del pieceDictionary[key][endSquare.coord]
        
    key = startSquare.type.color + startSquare.type.name
    pieceDictionary[key][endPosition] = pieceDictionary[key][startPosition]
    del pieceDictionary[key][startPosition]

    endSquare.type = startSquare.type
    startSquare.type = Type(None, None)

    return board


def undoLastOverride():
    global pieceDictionary
    global changesStack

    # change = [startSquare, endSquare, endType]
    change = changesStack.pop()

    change[0].type = change[1].type
    change[1].type = change[2]

    # update piece dictionary
    key = change[0].type.color + change[0].type.name
    pieceDictionary[key][change[0].coord] = change[1]
    del pieceDictionary[key][change[1].coord]

    if change[2] != Type(None, None):
        key = change[2].color + change[2].name
        pieceDictionary[key][change[1].coord] = change[1]

import pygame
from pygame.locals import *


def getBoardFromCoord(board, coord):
    for sq in board:
        if sq.coord == coord: return sq
    return None


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


def check(board):
    light = getAllMoves(board, 'w', 1)
    dark = getAllMoves(board, 'b', -1)

    for m in light:
        if m.type.name == "k":
            return m
    for m in dark:
        if m.type.name == "k":
            return m
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
                if ch.type.color != color: newMoves.append(m)
    else: newMoves = moves
    return newMoves


def movePiece(board1, sq1, sq2):
    board = [Square(i.rect, i.coord, i.type) for i in board1]
    for i, sq in enumerate(board):
        if sq == sq1:
            board[i] = Square(sq1.rect, sq1.coord, Type(None, None))
        elif sq == sq2:
            board[i] = Square(sq2.rect, sq2.coord, sq1.type)
    return board

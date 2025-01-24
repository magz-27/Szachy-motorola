import pygame
from pygame.locals import *

board = ["bR", "bN", "bB", "bK", "bQ", "bB", "bN", "bR",
         "bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP",
         "", "", "", "", "", "", "", "",
         "", "", "", "", "", "", "", "",
         "", "", "", "", "", "", "", "",
         "", "", "", "", "", "", "", "",
         "wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP",
         "wR", "wN", "wB", "wK", "wQ", "wB", "wN", "wR"]

playerColor = 'w'


def getBoardFromCoord(coord):
    for sq in board:
        if sq.coord == coord: return sq
    return None


class Square:
    def __init__(self, rect: pygame.Rect, coord, type):
        self.rect = rect
        self.coord = coord
        self.type = type

    def __str__(self):
        return f'{self.type.getColor()} {self.type.getName()}, {self.coord}'


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

    def invertColor(self):
        if self.color == "w":
            return "b"
        elif self.color == "b":
            return "w"


def calculateMoves(board, coord, name, color, dir):
    moves = []

    # Pawn movement
    if name == "p":
        # Single
        sq = getBoardFromCoord((coord[0], coord[1] - 1))
        if sq != None:
            if sq.type.name is None: moves.append(sq)

        # Double
        sq = getBoardFromCoord((coord[0], coord[1] - 2))
        if sq != None:
            if sq.type.name is None and coord[1] == 6: moves.append(sq)

        # Left Capture
        sq = getBoardFromCoord((coord[0] - 1, coord[1] - 1))
        if sq != None:
            if sq.type.invertColor() == color: moves.append(sq)

        # Right Capture
        sq = getBoardFromCoord((coord[0] + 1, coord[1] - 1))
        if sq != None:
            if sq.type.invertColor() == color: moves.append(sq)

    # Rook movement
    if name == "r":
        # Up
        i = 0
        while True:
            sq = getBoardFromCoord((coord[0], coord[1] - i - 1))
            if sq == None: break
            if sq.type.invertColor() == color:
                moves.append(sq)
                break
            if sq.type.color == color:
                break
            moves.append(sq)
            i += 1

        # Down
        i = 0
        while True:
            sq = getBoardFromCoord((coord[0], coord[1] + i + 1))
            if sq == None: break
            if sq.type.invertColor() == color:
                moves.append(sq)
                break
            if sq.type.color == color:
                break
            moves.append(sq)
            i += 1

        # Left
        i = 0
        while True:
            sq = getBoardFromCoord((coord[0]-i-1, coord[1]))
            if sq == None: break
            if sq.type.invertColor() == color:
                moves.append(sq)
                break
            if sq.type.color == color:
                break
            moves.append(sq)
            i += 1

        # Right
        i = 0
        while True:
            sq = getBoardFromCoord((coord[0]+i+1, coord[1]))
            if sq == None: break
            if sq.type.invertColor() == color:
                moves.append(sq)
                break
            if sq.type.color == color:
                break
            moves.append(sq)
            i += 1

    # Knight movement
    if name == "n":

        sq = getBoardFromCoord((coord[0]-1, coord[1] - 2))
        if sq != None:
            if sq.type.color != color: moves.append(sq)

        sq = getBoardFromCoord((coord[0]+1, coord[1] - 2))
        if sq != None:
            if sq.type.color != color: moves.append(sq)

        sq = getBoardFromCoord((coord[0] - 1, coord[1] + 2))
        if sq != None:
            if sq.type.color != color: moves.append(sq)

        sq = getBoardFromCoord((coord[0] + 1, coord[1] + 2))
        if sq != None:
            if sq.type.color != color: moves.append(sq)

        sq = getBoardFromCoord((coord[0] - 2, coord[1] -1))
        if sq != None:
            if sq.type.color != color: moves.append(sq)

        sq = getBoardFromCoord((coord[0] + 2, coord[1] - 1))
        if sq != None:
            if sq.type.color != color: moves.append(sq)

        sq = getBoardFromCoord((coord[0] - 2, coord[1] + 1))
        if sq != None:
            if sq.type.color != color: moves.append(sq)

        sq = getBoardFromCoord((coord[0] + 2, coord[1] + 1))
        if sq != None:
            if sq.type.color != color: moves.append(sq)

    # Bishop movement
    if name == "b":
        # Top left
        i = 0
        while True:
            sq = getBoardFromCoord((coord[0]-i-1, coord[1]-i-1))
            if sq == None: break
            if sq.type.invertColor() == color:
                moves.append(sq)
                break
            if sq.type.color == color:
                break
            moves.append(sq)
            i+=1

        # Top right
        i = 0
        while True:
            sq = getBoardFromCoord((coord[0] + i + 1, coord[1] - i - 1))
            if sq == None: break
            if sq.type.invertColor() == color:
                moves.append(sq)
                break
            if sq.type.color == color:
                break
            moves.append(sq)
            i += 1

        # Bottom left
        i = 0
        while True:
            sq = getBoardFromCoord((coord[0] - i - 1, coord[1] + i + 1))
            if sq == None: break
            if sq.type.invertColor() == color:
                moves.append(sq)
                break
            if sq.type.color == color:
                break
            moves.append(sq)
            i += 1

        # Bottom right
        i = 0
        while True:
            sq = getBoardFromCoord((coord[0] + i + 1, coord[1] + i + 1))
            if sq == None: break
            if sq.type.invertColor() == color:
                moves.append(sq)
                break
            if sq.type.color == color:
                break
            moves.append(sq)
            i += 1

    # Queen movement
    if name == "q":
        moves.extend(calculateMoves(board,coord,"r", color, dir))
        moves.extend(calculateMoves(board,coord, "b", color, dir))

    # King movement
    if name == "k":
        # Top left
        sq = getBoardFromCoord((coord[0] -1, coord[1] - 1))
        if sq != None:
            if sq.type.color != color: moves.append(sq)

        # Top middle
        sq = getBoardFromCoord((coord[0], coord[1] - 1))
        if sq != None:
            if sq.type.color != color: moves.append(sq)

        # Top right
        sq = getBoardFromCoord((coord[0] + 1, coord[1] - 1))
        if sq != None:
            if sq.type.color != color: moves.append(sq)

        # Middle right
        sq = getBoardFromCoord((coord[0] +1, coord[1]))
        if sq != None:
            if sq.type.color != color: moves.append(sq)

        # Bottom right
        sq = getBoardFromCoord((coord[0] +1, coord[1] + 1))
        if sq != None:
            if sq.type.color != color: moves.append(sq)

        # Bottom middle
        sq = getBoardFromCoord((coord[0], coord[1] + 1))
        if sq != None:
            if sq.type.color != color: moves.append(sq)

        # Bottom left
        sq = getBoardFromCoord((coord[0] - 1, coord[1] + 1))
        if sq != None:
            if sq.type.color != color: moves.append(sq)

        # Middle left
        sq = getBoardFromCoord((coord[0] - 1, coord[1]))
        if sq != None:
            if sq.type.color != color: moves.append(sq)


    return moves


def movePiece(board, sq1, sq2):
    for i, sq in enumerate(board):
        if sq == sq1:
            board[i] = Square(sq1.rect, sq1.coord, Type(None, None))
        elif sq == sq2:
            board[i] = Square(sq2.rect, sq2.coord, sq1.type)
    return board

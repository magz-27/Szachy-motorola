import pygame

board = ["bR", "bN", "bB", "bK", "bQ", "bB", "bN", "bR",
         "bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP",
         "", "", "", "", "", "", "", "",
         "", "", "", "", "", "", "", "",
         "", "", "", "", "", "", "", "",
         "", "", "", "", "", "", "", "",
         "wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP",
         "wR", "wN", "wB", "wK", "wQ", "wB", "wN", "wR"]

class Square:
    def __init__(self, rect:pygame.Rect, coord, type):
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
        if self.name == "p": return "Pawn"
        elif self.name == "r": return "Rook"
        elif self.name == "n": return "Knight"
        elif self.name == "b": return "Bishop"
        elif self.name == "q": return "Queen"
        elif self.name == "k": return "King"
    def getColor(self):
        if self.color == "w": return "Light"
        elif self.color == "b": return "Dark"


def calculateMoves(board, coord, name, color, dir):
    moves = []
    for sq in board:
        sq: Square
        if name == "p":
            if sq.coord[0] == coord[0] and sq.coord[1] == coord[1]-2 and coord[1]==6: moves.append(sq)
            if sq.coord[0] == coord[0] and sq.coord[1] == coord[1]-1: moves.append(sq)
    return moves


def movePiece(board, sq1, sq2):
    for i, sq in enumerate(board):
        if sq == sq1:
            board[i] = Square(sq1.rect, sq1.coord, sq2.type)
        elif sq == sq2:
            board[i] = Square(sq2.rect, sq2.coord, sq1.type)
    return board
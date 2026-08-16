from .piece import Piece

class Board:
    def __init__(self):
        self.position = [
            [
                Piece("black", "rook"),
                Piece("black", "knight"),
                Piece("black", "bishop"),
                Piece("black", "queen"),
                Piece("black", "king"),
                Piece("black", "bishop"),
                Piece("black", "knight"),
                Piece("black", "rook")
            ],

            [Piece("black", "pawn") for _ in range(8)],

            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],

            [Piece("white", "pawn") for _ in range(8)],
            
            [
                Piece("white", "rook"),
                Piece("white", "knight"),
                Piece("white", "bishop"),
                Piece("white", "queen"),
                Piece("white", "king"),
                Piece("white", "bishop"),
                Piece("white", "knight"),
                Piece("white", "rook")
            ]
        ]
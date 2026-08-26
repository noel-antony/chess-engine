from .piece import Piece
from .move_generator import MoveGenerator

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

        self.move_generator = MoveGenerator(self)
        self.move_history = []

    def make_move(self, move):
        start_row, start_col = move.start
        end_row, end_col = move.end

        move.captured_piece = self.position[end_row][end_col]
        piece = self.position[start_row][start_col]

        self.position[end_row][end_col] = piece
        self.position[start_row][start_col] = None

        self.move_history.append(move)

    def undo_move(self):
        move = self.move_history.pop()
        start_row, start_col = move.start
        end_row, end_col = move.end

        piece = self.position[end_row][end_col]

        self.position[start_row][start_col] = piece
        self.position[end_row][end_col] = move.captured_piece

    def is_valid_position(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8


    def generate_legal_moves(self, row, col):
        if not self.is_valid_position(row, col):
            return []

        piece = self.position[row][col]

        if piece is None:
            return []

        pseudo_legal_moves = self.generate_moves(row, col)
        legal_moves = []

        for move in pseudo_legal_moves:
            self.make_move(move)

            if not self.is_in_check(piece.color):
                legal_moves.append(move)

            self.undo_move()

        return legal_moves

    def generate_moves(self, row, col):
        return self.move_generator.generate_moves(row, col)

    def is_in_check(self, color):
        return self.move_generator.is_in_check(color)
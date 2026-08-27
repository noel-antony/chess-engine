from .piece import Piece
from .move import Move
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

        move.moved_piece = self.position[start_row][start_col]
        move.captured_piece = self.position[end_row][end_col]
        move.captured_position = move.end

        move.moved_piece_previous_has_moved = move.moved_piece.has_moved
        move.moved_piece.has_moved = True

        if move.promotion is not None:
            promoted_piece = Piece(move.moved_piece.color, move.promotion)
            promoted_piece.has_moved = True
            
            self.position[end_row][end_col] = promoted_piece
        else:
            self.position[end_row][end_col] = move.moved_piece

        if move.special == "castle_kingside":
            rook_start = (start_row, 7)
            rook_end = (start_row, 5)

            rook = self.position[rook_start[0]][rook_start[1]]
            move.castle_rook = rook
            move.castle_rook_previous_has_moved = rook.has_moved
            rook.has_moved = True

            self.position[rook_end[0]][rook_end[1]] = rook
            self.position[rook_start[0]][rook_start[1]] = None

        elif move.special == "castle_queenside":
            rook_start = (start_row, 0)
            rook_end = (start_row, 3)

            rook = self.position[rook_start[0]][rook_start[1]]
            move.castle_rook = rook
            move.castle_rook_previous_has_moved = rook.has_moved
            rook.has_moved = True

            self.position[rook_end[0]][rook_end[1]] = rook
            self.position[rook_start[0]][rook_start[1]] = None

        elif move.special == "en_passant":
            capt_row, capt_col = start_row, end_col

            move.captured_position = (capt_row, capt_col)
            move.captured_piece = self.position[capt_row][capt_col]

            self.position[capt_row][capt_col] = None


        self.move_history.append(move)

    def undo_move(self):
        move = self.move_history.pop()
        start_row, start_col = move.start
        end_row, end_col = move.end

        move.moved_piece.has_moved = move.moved_piece_previous_has_moved

        self.position[start_row][start_col] = move.moved_piece
        self.position[end_row][end_col] = move.captured_piece

        if move.special == "castle_kingside":
            rook_start = (start_row, 7)
            rook_end = (start_row, 5)

            self.position[rook_start[0]][rook_start[1]] = move.castle_rook
            self.position[rook_end[0]][rook_end[1]] = None

            move.castle_rook.has_moved = move.castle_rook_previous_has_moved

        elif move.special == "castle_queenside":
            rook_start = (start_row, 0)
            rook_end = (start_row, 3)

            self.position[rook_start[0]][rook_start[1]] = move.castle_rook
            self.position[rook_end[0]][rook_end[1]] = None

            move.castle_rook.has_moved = move.castle_rook_previous_has_moved

        elif move.special == "en_passant":
            capt_row, capt_col = move.captured_position

            self.position[capt_row][capt_col] = move.captured_piece
            self.position[end_row][end_col] = None

    def is_valid_position(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8

    def get_all_legal_moves(self, color):
        moves = []

        for row in range(8):
            for col in range(8):
                piece = self.position[row][col]

                if piece is not None and piece.color == color:
                    moves.extend(self.generate_legal_moves(row, col))

        return moves

    def is_checkmate(self, color):
        return self.is_in_check(color) and not self.get_all_legal_moves(color)

    def is_stalemate(self, color):
        return not self.is_in_check(color) and not self.get_all_legal_moves(color)
    
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

    def can_castle_kingside(self, color):
        if color == "white":
            row = 7
            opponent = "black"
        else:
            row = 0
            opponent = "white"

        king = self.position[row][4]
        rook = self.position[row][7]

        if king is None or rook is None:
            return False
        if king.has_moved or rook.has_moved:
            return False

        if king.piece_type != "king" or king.color != color:
            return False
        if rook.piece_type != "rook" or rook.color != color:
            return False

        if self.position[row][5] is not None or self.position[row][6] is not None:
            return False

        for col in (4, 5, 6):
            if self.move_generator.is_square_attacked(row, col, opponent):
                return False

        return True

    def can_castle_queenside(self, color):
        if color == "white":
            row = 7
            opponent = "black"
        else:
            row = 0
            opponent = "white"

        king = self.position[row][4]
        rook = self.position[row][0]

        if king is None or rook is None:
            return False
        if king.has_moved or rook.has_moved:
            return False

        if king.piece_type != "king" or king.color != color:
            return False
        if rook.piece_type != "rook" or rook.color != color:
            return False

        if self.position[row][1] is not None or self.position[row][2] is not None or self.position[row][3] is not None:
            return False

        for col in (4, 3, 2):
            if self.move_generator.is_square_attacked(row, col, opponent):
                return False

        return True
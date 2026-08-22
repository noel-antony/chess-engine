from .piece import Piece
from .move import Move

ROOK_DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
BISHOP_DIRECTIONS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
QUEEN_DIRECTIONS = ROOK_DIRECTIONS + BISHOP_DIRECTIONS

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
    
    def generate_moves(self, position):
        row, col = position

        if not self.is_valid_position(row, col):
            return []
        piece = self.position[row][col]
        if piece is None:
            return []
        
        if piece.piece_type == "knight":
            return self.get_knight_moves(row, col)
        elif piece.piece_type == "pawn":
            return self.get_pawn_moves(row, col)
        elif piece.piece_type == "rook":
            return self.get_sliding_moves(row, col, ROOK_DIRECTIONS)
        elif piece.piece_type == "bishop":
            return self.get_sliding_moves(row, col, BISHOP_DIRECTIONS)
        elif piece.piece_type == "queen":
            return self.get_sliding_moves(row, col, QUEEN_DIRECTIONS)
        elif piece.piece_type == "king":
            return self.get_king_moves(row, col)
        return []
        
    def get_knight_moves(self, row, col):
        offsets = [
            (+2, +1), (+2, -1),
            (-2, +1), (-2, -1),
            (+1, +2), (+1, -2),
            (-1, +2), (-1, -2)
        ]
        moves = []
        piece = self.position[row][col]

        for row_offset, col_offset in offsets:
            new_row = row + row_offset
            new_col = col + col_offset

            if self.is_valid_position(new_row, new_col):
                destination = self.position[new_row][new_col]

                if destination is None or destination.color != piece.color:
                    move = Move((row, col), (new_row, new_col))
                    moves.append(move)

        return moves

    def get_pawn_moves(self, row, col):
        piece = self.position[row][col]
        forward = []
        captures = []
        moves = []

        if piece.color == "black":
            forward.append((row + 1, col))

            if row == 1 and self.position[2][col] is None:
                forward.append((row + 2, col))
            if col < 7:
                captures.append((row + 1, col + 1))
            if col > 0:
                captures.append((row + 1, col - 1))

        elif piece.color == "white":
            forward.append((row - 1, col))

            if row == 6 and self.position[5][col] is None:
                forward.append((row - 2, col))
            if col < 7:
                captures.append((row - 1, col + 1))
            if col > 0:
                captures.append((row - 1, col - 1))  

        for new_row, new_col in forward:
            if self.is_valid_position(new_row, new_col):
                destination = self.position[new_row][new_col]

                if destination is None:
                    move = Move((row, col), (new_row, new_col))
                    moves.append(move)

        for new_row, new_col in captures:
            if self.is_valid_position(new_row, new_col):
                destination = self.position[new_row][new_col]

                if destination is not None and destination.color != piece.color:
                    move = Move((row, col), (new_row, new_col))
                    moves.append(move)

        return moves

    def get_sliding_moves(self, row, col, directions):
        piece = self.position[row][col]
        moves = []

        for row_dir, col_dir in directions:
            cur_row = row + row_dir
            cur_col = col + col_dir

            while self.is_valid_position(cur_row, cur_col):
                destination = self.position[cur_row][cur_col]

                if destination is None:
                    moves.append(Move((row, col), (cur_row, cur_col)))
                else:
                    if destination.color != piece.color:
                        moves.append(Move((row, col), (cur_row, cur_col)))
                    break

                cur_row += row_dir
                cur_col += col_dir

        return moves

    def get_king_moves(self, row, col):
        offsets = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        moves = []
        piece = self.position[row][col]

        for row_offset, col_offset in offsets:
            new_row = row + row_offset
            new_col = col + col_offset

            if self.is_valid_position(new_row, new_col):
                destination = self.position[new_row][new_col]

                if destination is None or destination.color != piece.color:
                    move = Move((row, col), (new_row, new_col))
                    moves.append(move)

        return moves
from .move import Move

ROOK_DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
BISHOP_DIRECTIONS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
QUEEN_DIRECTIONS = ROOK_DIRECTIONS + BISHOP_DIRECTIONS
KNIGHT_OFFSETS = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
KING_OFFSETS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

class MoveGenerator:
    def __init__(self, board):
        self.board = board

    def generate_moves(self, row, col):

        if not self.board.is_valid_position(row, col):
            return []
        piece = self.board.position[row][col]
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
        moves = []
        piece = self.board.position[row][col]

        for row_offset, col_offset in KNIGHT_OFFSETS:
            new_row = row + row_offset
            new_col = col + col_offset

            if self.board.is_valid_position(new_row, new_col):
                destination = self.board.position[new_row][new_col]

                if destination is None or destination.color != piece.color:
                    move = Move((row, col), (new_row, new_col))
                    moves.append(move)

        return moves

    def get_pawn_moves(self, row, col):
        piece = self.board.position[row][col]
        forward = []
        captures = []
        moves = []
        
        if piece.color == "black":
            forward.append((row + 1, col))

            if row == 1 and self.board.position[2][col] is None:
                forward.append((row + 2, col))
            if col < 7:
                captures.append((row + 1, col + 1))
            if col > 0:
                captures.append((row + 1, col - 1))

        elif piece.color == "white":
            forward.append((row - 1, col))

            if row == 6 and self.board.position[5][col] is None:
                forward.append((row - 2, col))
            if col < 7:
                captures.append((row - 1, col + 1))
            if col > 0:
                captures.append((row - 1, col - 1))  

        for new_row, new_col in forward:
            if self.board.is_valid_position(new_row, new_col):

                destination = self.board.position[new_row][new_col]
                is_promotion = (piece.color == "white" and new_row == 0) or (piece.color == "black" and new_row == 7)

                if destination is None:
                    if is_promotion:
                        for promotion_piece in ("queen", "rook", "bishop", "knight"):
                            moves.append(Move((row, col), (new_row, new_col), promotion=promotion_piece))
                    else:
                        moves.append(Move((row, col), (new_row, new_col)))

        for new_row, new_col in captures:
            if self.board.is_valid_position(new_row, new_col):

                destination = self.board.position[new_row][new_col]
                is_promotion = (piece.color == "white" and new_row == 0) or (piece.color == "black" and new_row == 7)

                if destination is not None and destination.color != piece.color:
                    if is_promotion:
                        for promotion_piece in ("queen", "rook", "bishop", "knight"):
                            moves.append(Move((row, col), (new_row, new_col), promotion=promotion_piece))
                    else:
                        moves.append(Move((row, col), (new_row, new_col)))

        if self.board.move_history:
            last_move = self.board.move_history[-1]

            moved_pawn = last_move.moved_piece.piece_type == "pawn"
            enemy_pawn = last_move.moved_piece.color != piece.color
            double_move = abs(last_move.start[0] - last_move.end[0]) == 2
            beside_pawn = (last_move.end[0] == row and abs(last_move.end[1] - col) == 1)

            if moved_pawn and enemy_pawn and double_move and beside_pawn:
                new_row = row - 1 if piece.color == "white" else row + 1
                new_col = last_move.end[1]

                move = Move((row, col), (new_row, new_col), special="en_passant")
                moves.append(move)

        return moves

    def get_sliding_moves(self, row, col, directions):
        piece = self.board.position[row][col]
        moves = []

        for row_dir, col_dir in directions:
            cur_row = row + row_dir
            cur_col = col + col_dir

            while self.board.is_valid_position(cur_row, cur_col):
                destination = self.board.position[cur_row][cur_col]

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
        moves = []
        piece = self.board.position[row][col]

        if self.board.can_castle_kingside(piece.color):
            move = Move((row, col), (row, col+2), special="castle_kingside")
            moves.append(move)

        if self.board.can_castle_queenside(piece.color):
            move = Move((row, col), (row, col-2), special="castle_queenside")
            moves.append(move)

        for row_offset, col_offset in KING_OFFSETS:
            new_row = row + row_offset
            new_col = col + col_offset

            if self.board.is_valid_position(new_row, new_col):
                destination = self.board.position[new_row][new_col]

                if destination is None or destination.color != piece.color:
                    move = Move((row, col), (new_row, new_col))
                    moves.append(move)

        return moves

    def is_square_attacked(self, row, col, by_color):

        for row_offset, col_offset in KNIGHT_OFFSETS:
            check_row = row + row_offset
            check_col = col + col_offset

            if self.board.is_valid_position(check_row, check_col):
                piece = self.board.position[check_row][check_col]

                if (piece is not None and piece.color == by_color and piece.piece_type == "knight"):
                    return True


        for row_dir, col_dir in ROOK_DIRECTIONS:

            check_row = row + row_dir
            check_col = col + col_dir

            while self.board.is_valid_position(check_row, check_col):
                piece = self.board.position[check_row][check_col]

                if piece is None:
                    check_row += row_dir
                    check_col += col_dir
                    continue

                if piece.color == by_color:
                    if piece.piece_type in ("rook", "queen"):
                        return True

                break

        for row_dir, col_dir in BISHOP_DIRECTIONS:

            check_row = row + row_dir
            check_col = col + col_dir

            while self.board.is_valid_position(check_row, check_col):
                piece = self.board.position[check_row][check_col]

                if piece is None:
                    check_row += row_dir
                    check_col += col_dir
                    continue

                if piece.color == by_color:
                    if piece.piece_type in ("bishop", "queen"):
                        return True

                break

        for row_offset, col_offset in KING_OFFSETS:
            new_row = row + row_offset
            new_col = col + col_offset

            if self.board.is_valid_position(new_row, new_col):
                piece = self.board.position[new_row][new_col]

                if piece is not None and piece.color == by_color and piece.piece_type == "king":
                    return True
                
        if by_color == "black":
            pawn_row = row - 1
        else:
            pawn_row = row + 1

        for pawn_col in (col - 1, col + 1):
            if self.board.is_valid_position(pawn_row, pawn_col):
                piece = self.board.position[pawn_row][pawn_col]

                if piece is not None and piece.color == by_color and piece.piece_type == "pawn":
                    return True

        return False

    def is_in_check(self, color):
        for row in range(8):
            for col in range(8):
                piece = self.board.position[row][col]

                if piece is not None and piece.color == color and piece.piece_type == "king":
                    opponent = "black" if color == "white" else "white"
                    return self.is_square_attacked(row, col, opponent)

        return False
class Evaluator:

    PIECE_VALUES = {
        "pawn": 100,
        "knight": 320,
        "bishop": 330,
        "rook": 500,
        "queen": 900,
        "king": 0
    }

    PAWN_TABLE = [
          0,   0,   0,   0,   0,   0,   0,   0,
         50,  50,  50,  50,  50,  50,  50,  50,
         10,  10,  20,  30,  30,  20,  10,  10,
          5,   5,  10,  25,  25,  10,   5,   5,
          0,   0,   0,  20,  20,   0,   0,   0,
          5,  -5, -10,   0,   0, -10,  -5,   5,
          5,  10,  10, -20, -20,  10,  10,   5,
          0,   0,   0,   0,   0,   0,   0,   0
    ]

    KNIGHT_TABLE = [
        -50, -40, -30, -30, -30, -30, -40, -50,
        -40, -20,   0,   5,   5,   0, -20, -40,
        -30,   5,  10,  15,  15,  10,   5, -30,
        -30,   0,  15,  20,  20,  15,   0, -30,
        -30,   5,  15,  20,  20,  15,   5, -30,
        -30,   0,  10,  15,  15,  10,   0, -30,
        -40, -20,   0,   0,   0,   0, -20, -40,
        -50, -40, -30, -30, -30, -30, -40, -50
    ]

    BISHOP_TABLE = [
        -20, -10, -10, -10, -10, -10, -10, -20,
        -10,   5,   0,   0,   0,   0,   5, -10,
        -10,  10,  10,  10,  10,  10,  10, -10,
        -10,   0,  10,  10,  10,  10,   0, -10,
        -10,   5,   5,  10,  10,   5,   5, -10,
        -10,   0,   5,  10,  10,   5,   0, -10,
        -10,   0,   0,   0,   0,   0,   0, -10,
        -20, -10, -10, -10, -10, -10, -10, -20
    ]

    ROOK_TABLE = [
          0,   0,   0,   5,   5,   0,   0,   0,
         -5,   0,   0,   0,   0,   0,   0,  -5,
         -5,   0,   0,   0,   0,   0,   0,  -5,
         -5,   0,   0,   0,   0,   0,   0,  -5,
         -5,   0,   0,   0,   0,   0,   0,  -5,
         -5,   0,   0,   0,   0,   0,   0,  -5,
          5,  10,  10,  10,  10,  10,  10,   5,
          0,   0,   0,   0,   0,   0,   0,   0
    ]

    QUEEN_TABLE = [
        -20, -10, -10,  -5,  -5, -10, -10, -20,
        -10,   0,   0,   0,   0,   0,   0, -10,
        -10,   0,   5,   5,   5,   5,   0, -10,
         -5,   0,   5,   5,   5,   5,   0,  -5,
          0,   0,   5,   5,   5,   5,   0,  -5,
        -10,   5,   5,   5,   5,   5,   0, -10,
        -10,   0,   5,   0,   0,   0,   0, -10,
        -20, -10, -10,  -5,  -5, -10, -10, -20
    ]

    KING_TABLE = [
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -20, -30, -30, -40, -40, -30, -30, -20,
        -10, -20, -20, -20, -20, -20, -20, -10,
         20,  20,   0,   0,   0,   0,  20,  20,
         20,  30,  10,   0,   0,  10,  30,  20
    ]

    PIECE_TABLES = {
        "pawn": PAWN_TABLE,
        "knight": KNIGHT_TABLE,
        "bishop": BISHOP_TABLE,
        "rook": ROOK_TABLE,
        "queen": QUEEN_TABLE,
        "king": KING_TABLE
    }

    PASSED_PAWN_BONUS = [0, 5, 10, 20, 35, 60, 100]

    def evaluate(self, board):
        score = 0

        score += self.evaluate_material(board)
        score += self.evaluate_piece_square_tables(board)
        score += self.evaluate_mobility(board)
        score += self.evaluate_pawn_structure(board)
        score += self.evaluate_king_safety(board)
        score += self.evaluate_bishop_pair(board)

        return score


    def evaluate_material(self, board):
        score = 0

        for row in range(8):
            for col in range(8):
                piece = board.position[row][col]

                if piece is None:
                    continue

                value = self.PIECE_VALUES[piece.piece_type]

                if piece.color == "white":
                    score += value
                else:
                    score -= value

        return score


    def evaluate_piece_square_tables(self, board):
        score = 0

        for row in range(8):
            for col in range(8):
                piece = board.position[row][col]

                if piece is None:
                    continue

                table = self.PIECE_TABLES[piece.piece_type]

                if piece.color == "white":
                    table_row = 7 - row
                else:
                    table_row = row

                index = table_row * 8 + col
                value = table[index]

                if piece.color == "white":
                    score += value
                else:
                    score -= value

        return score


    def evaluate_mobility(self, board):
        white_moves = len(board.get_all_legal_moves("white"))
        black_moves = len(board.get_all_legal_moves("black"))

        return (white_moves - black_moves) * 5


    def evaluate_pawn_structure(self, board):
        score = 0

        for col in range(8):
            white_pawns = 0
            black_pawns = 0

            for row in range(8):
                piece = board.position[row][col]

                if piece is None:
                    continue

                if piece.piece_type == "pawn":
                    if piece.color == "white":
                        white_pawns += 1
                    else:
                        black_pawns += 1

            # doubled pawns
            if white_pawns > 1:
                score -= (white_pawns - 1) * 20

            if black_pawns > 1:
                score += (black_pawns - 1) * 20

        # isolated and passed pawns
        for row in range(8):
            for col in range(8):
                piece = board.position[row][col]

                if piece is None or piece.piece_type != "pawn":
                    continue

                color = piece.color

                if self.is_isolated_pawn(board, row, col, color):
                    if color == "white":
                        score -= 15
                    else:
                        score += 15

                if self.is_passed_pawn(board, row, col, color):
                    advancement = self.get_pawn_advancement(row, color)

                    bonus = self.PASSED_PAWN_BONUS[advancement]

                    if color == "white":
                        score += bonus
                    else:
                        score -= bonus

        return score


    def is_isolated_pawn(self, board, row, col, color):
        start_col = max(0, col - 1)
        end_col = min(7, col + 1)

        for check_col in range(start_col, end_col + 1):
            if check_col == col:
                continue

            for check_row in range(8):
                piece = board.position[check_row][check_col]

                if piece is not None and piece.color == color and piece.piece_type == "pawn":
                    return False

        return True


    def is_passed_pawn(self, board, row, col, color):
        start_col = max(0, col - 1)
        end_col = min(7, col + 1)

        if color == "white":
            # White moves toward row 0.
            rows = range(row - 1, -1, -1)
            enemy_color = "black"

        else:
            # Black moves toward row 7.
            rows = range(row + 1, 8)
            enemy_color = "white"

        for check_col in range(start_col, end_col + 1):
            for check_row in rows:
                piece = board.position[check_row][check_col]

                if piece is not None and piece.color == enemy_color and piece.piece_type == "pawn":
                    return False

        return True


    def get_pawn_advancement(self, row, color):
        if color == "white":
            return 7 - row
        else:
            return row


    def evaluate_king_safety(self, board):
        score = 0

        for color in ["white", "black"]:
            king_position = self.find_king(board, color)

            if king_position is None:
                continue

            row, col = king_position

            # friendly pawns near the king
            pawn_count = 0

            for r in range(max(0, row - 1), min(8, row + 2)):
                for c in range(max(0, col - 1), min(8, col + 2)):
                    piece = board.position[r][c]

                    if piece is not None and piece.piece_type == "pawn" and piece.color == color:
                        pawn_count += 1

            pawn_safety = pawn_count * 20

            # Count attacked squares around the king.
            enemy_color = ("black" if color == "white" else "white")

            attacked_squares = 0

            for r in range(max(0, row - 1), min(8, row + 2)):
                for c in range(max(0, col - 1), min(8, col + 2)):

                    if board.move_generator.is_square_attacked(r, c, enemy_color):
                        attacked_squares += 1

            attack_penalty = attacked_squares * 10

            safety = pawn_safety - attack_penalty

            if color == "white":
                score += safety
            else:
                score -= safety

        return score


    def find_king(self, board, color):
        for row in range(8):
            for col in range(8):
                piece = board.position[row][col]

                if piece is not None and piece.piece_type == "king" and piece.color == color:
                    return row, col

        return None


    def evaluate_bishop_pair(self, board):
        white_bishops = 0
        black_bishops = 0

        for row in range(8):
            for col in range(8):
                piece = board.position[row][col]

                if piece is None:
                    continue

                if piece.piece_type != "bishop":
                    continue

                if piece.color == "white":
                    white_bishops += 1
                else:
                    black_bishops += 1

        score = 0

        if white_bishops >= 2:
            score += 30

        if black_bishops >= 2:
            score -= 30

        return score
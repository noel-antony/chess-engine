from chess.evaluation import Evaluator

class Minimax:

    MATE_SCORE = 100000

    PIECE_VALUES = {
        "pawn": 100,
        "knight": 320,
        "bishop": 330,
        "rook": 500,
        "queen": 900,
        "king": 20000
    }

    def __init__(self):
        self.evaluator = Evaluator()

    def get_best_move(self, board, depth):
        color = board.current_turn
        legal_moves = board.get_all_legal_moves(color)

        if not legal_moves:
            return None

        legal_moves = self.order_moves(board, legal_moves)
        best_move = None

        if color == "white":
            best_score = float("-inf")
            alpha = float("-inf")
            beta = float("inf")

            for move in legal_moves:
                board.make_move(move)
                score = self.minimax(board, depth - 1, alpha, beta, "black")
                board.undo_move()

                if score > best_score:
                    best_score = score
                    best_move = move

                alpha = max(alpha, best_score)

        else:
            best_score = float("inf")
            alpha = float("-inf")
            beta = float("inf")

            for move in legal_moves:
                board.make_move(move)
                score = self.minimax(board, depth - 1, alpha, beta, "white")
                board.undo_move()

                if score < best_score:
                    best_score = score
                    best_move = move

                beta = min(beta, best_score)

        return best_move

    def minimax(self, board, depth, alpha, beta, color):
        legal_moves = board.get_all_legal_moves(color)

        if not legal_moves:
            if board.is_in_check(color):
                if color == "white":
                    return -self.MATE_SCORE
                else:
                    return self.MATE_SCORE
            return 0

        if depth == 0:
            return self.evaluator.evaluate(board)

        legal_moves = self.order_moves(board, legal_moves)

        if color == "white":
            best_score = float("-inf")

            for move in legal_moves:
                board.make_move(move)
                score = self.minimax(board, depth - 1, alpha, beta, "black")
                board.undo_move()

                best_score = max(best_score, score)
                alpha = max(alpha, best_score)

                if alpha >= beta:
                    break

            return best_score

        else:
            best_score = float("inf")

            for move in legal_moves:
                board.make_move(move)
                score = self.minimax(board, depth - 1, alpha, beta, "white")
                board.undo_move()

                best_score = min(best_score, score)
                beta = min(beta, best_score)

                if alpha >= beta:
                    break

            return best_score

    def order_moves(self, board, moves):
        scored_moves = []

        for move in moves:
            score = self.move_order_score(board, move)
            scored_moves.append((score, move))

        scored_moves.sort(key=lambda item: item[0], reverse=True)

        return [move for score, move in scored_moves]

    def move_order_score(self, board, move):
        score = 0
        captured_piece = move.captured_piece

        if move.special == "en_passant":
            victim_value = self.PIECE_VALUES["pawn"]
            attacker_value = self.PIECE_VALUES[move.moved_piece.piece_type]
            score += 10 * victim_value - attacker_value

        elif captured_piece is not None:
            victim_value = self.PIECE_VALUES[captured_piece.piece_type]
            attacker_value = self.PIECE_VALUES[move.moved_piece.piece_type]
            score += 10 * victim_value - attacker_value

        if move.promotion is not None:
            promotion_value = self.PIECE_VALUES[move.promotion]
            score += promotion_value

        if move.special in ("castle_kingside", "castle_queenside"):
            score += 50

        return score
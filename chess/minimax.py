from chess.evaluation import Evaluator

class Minimax:

    MATE_SCORE = 100000

    def __init__(self):
        self.evaluator = Evaluator()

    def get_best_move(self, board, depth):
        color = board.current_turn
        legal_moves = board.get_all_legal_moves(color)

        if not legal_moves:
            return None

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
        # Checkmate or stalemate
        if not legal_moves:

            if board.is_in_check(color):
                if color == "white":
                    return -self.MATE_SCORE
                else:
                    return self.MATE_SCORE

            return 0

        # Reached search depth
        if depth == 0:
            return self.evaluator.evaluate(board)

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
from chess.minimax import Minimax

class ChessAgent:
    def __init__(self, depth=3):
        self.depth = depth
        self.search = Minimax()

    def get_move(self, board):
        return self.search.get_best_move(board, self.depth)
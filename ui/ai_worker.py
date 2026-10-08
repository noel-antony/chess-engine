from PySide6.QtCore import QThread, Signal
from chess.agent import ChessAgent
from chess.board import Board
import copy

class AIWorker(QThread):
    finished = Signal(object) # Returns the best move

    def __init__(self, board: Board, depth: int):
        super().__init__()
        # We must copy the board so we don't mutate it in the background thread
        # Note: copy.deepcopy might be slow or fail if not set up correctly.
        # Alternatively, we can just run it if we are sure the user can't mutate the board 
        # while the AI is thinking, since we lock the UI. But minimax modifies and undos state.
        # If UI thread just reads the board for painting, it might see intermediate states.
        # It's safer to use a deep copy.
        self.board = copy.deepcopy(board)
        self.depth = depth

    def run(self):
        agent = ChessAgent(depth=self.depth)
        best_move = agent.get_move(self.board)
        
        # We need to map the move back to the original board context if necessary, 
        # but the Move object contains start, end, promotion, special which are enough.
        # The moved_piece and captured_piece references might be to the copied board's pieces.
        # We can reconstruct the move on the main thread using start, end, and promotion.
        if best_move:
            move_data = (best_move.start, best_move.end, best_move.promotion)
            self.finished.emit(move_data)
        else:
            self.finished.emit(None)

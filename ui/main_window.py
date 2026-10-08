from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
    QLabel, QStackedLayout, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeySequence

from chess.board import Board
from chess.evaluation import Evaluator

from ui.chess_board import ChessBoardWidget
from ui.game_panel import GamePanel
from ui.move_history import MoveHistory
from ui.player_card import PlayerCard
from ui.evaluation_bar import EvaluationBar
from ui.ai_worker import AIWorker
from ui.new_game_dialog import NewGameDialog
from ui.game_over_dialog import GameOverDialog
from ui.promotion_dialog import PromotionWidget
from ui.styles import COMMON_STYLE

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chess")
        self.setMinimumSize(900, 700)
        self.setStyleSheet(COMMON_STYLE)
        
        self.board = Board()
        self.evaluator = Evaluator()
        
        self.player_color = "white"
        self.ai_color = "black"
        self.ai_depth = 3
        
        self.ai_worker = None
        self.promotion_move_cache = None
        self.game_active = False  # Start inactive until a new game is started
        
        self.init_ui()
        self.setup_shortcuts()
        self.chess_widget.set_active(False) # Initial disabled state
        self.update_state()
        
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Left side: Eval bar
        self.eval_bar = EvaluationBar()
        main_layout.addWidget(self.eval_bar)
        
        # Center: Player Cards + Board
        center_layout = QVBoxLayout()
        center_layout.setSpacing(10)
        
        self.top_card = PlayerCard(name="AI", color="Black", is_ai=True)
        self.bottom_card = PlayerCard(name="You", color="White", is_ai=False)
        
        self.board_container = QWidget()
        self.board_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.board_layout = QStackedLayout(self.board_container)
        
        self.chess_widget = ChessBoardWidget(self.board)
        self.chess_widget.move_requested.connect(self.handle_human_move)
        
        self.board_layout.addWidget(self.chess_widget)
        
        center_layout.addWidget(self.top_card)
        center_layout.addWidget(self.board_container, 1)
        center_layout.addWidget(self.bottom_card)
        
        main_layout.addLayout(center_layout, 1)
        
        # Right side: Panel + Moves
        right_layout = QVBoxLayout()
        right_layout.setSpacing(20)
        
        self.game_panel = GamePanel()
        self.game_panel.new_game_requested.connect(self.prompt_new_game)
        self.game_panel.undo_requested.connect(self.undo_move)
        self.game_panel.flip_requested.connect(self.flip_board)
        self.game_panel.resign_requested.connect(self.resign)
        self.game_panel.depth_changed.connect(self.set_depth)
        
        self.move_history = MoveHistory()
        
        right_layout.addWidget(self.game_panel)
        right_layout.addWidget(self.move_history, 1)
        
        main_layout.addLayout(right_layout)

    def setup_shortcuts(self):
        new_game_action = QAction("New Game", self)
        new_game_action.setShortcut(QKeySequence("Ctrl+N"))
        new_game_action.triggered.connect(self.prompt_new_game)
        self.addAction(new_game_action)
        
        undo_action = QAction("Undo", self)
        undo_action.setShortcut(QKeySequence("Ctrl+Z"))
        undo_action.triggered.connect(self.undo_move)
        self.addAction(undo_action)
        
        flip_action = QAction("Flip Board", self)
        flip_action.setShortcut(QKeySequence("F"))
        flip_action.triggered.connect(self.flip_board)
        self.addAction(flip_action)
        
        restart_action = QAction("Restart", self)
        restart_action.setShortcut(QKeySequence("Ctrl+R"))
        restart_action.triggered.connect(self.restart_game)
        self.addAction(restart_action)

    def prompt_new_game(self):
        dlg = NewGameDialog(self)
        if dlg.exec():
            self.player_color = dlg.player_color.lower()
            self.ai_color = "black" if self.player_color == "white" else "white"
            self.ai_depth = dlg.depth
            
            self.game_panel.slider_depth.setValue(self.ai_depth)
            
            self.top_card.name = "AI"
            self.top_card.color = self.ai_color.capitalize()
            self.bottom_card.name = "You"
            self.bottom_card.color = self.player_color.capitalize()
            
            self.chess_widget.set_flipped(self.player_color == "black")
            
            self.restart_game()

    def restart_game(self):
        if self.ai_worker and self.ai_worker.isRunning():
            return # Can't restart while AI is calculating easily without thread killing
            
        self.board = Board()
        self.chess_widget.set_board(self.board)
        self.chess_widget.clear_selection()
        self.chess_widget.last_move = None
        self.move_history.clear()
        
        if self.player_color == "black":
            self.chess_widget.set_flipped(True)
        else:
            self.chess_widget.set_flipped(False)
            
        self.game_active = True
        self.chess_widget.set_active(True)
        self.update_state()

    def undo_move(self):
        if self.ai_worker and self.ai_worker.isRunning():
            return
            
        if len(self.board.move_history) == 0:
            return
            
        # Undo AI move
        self.board.undo_move()
        self.board.current_turn = "white" if self.board.current_turn == "black" else "black"
        
        # Undo player move if it was AI's turn or we want to undo the full turn
        if len(self.board.move_history) > 0 and self.board.current_turn == self.ai_color:
            self.board.undo_move()
            self.board.current_turn = "white" if self.board.current_turn == "black" else "black"
            
        # Rebuild move history
        self.rebuild_move_history()
        
        if self.board.move_history:
            last = self.board.move_history[-1]
            self.chess_widget.highlight_last_move(last.start, last.end)
        else:
            self.chess_widget.last_move = None
            
        self.chess_widget.clear_selection()
        self.update_state()

    def rebuild_move_history(self):
        self.move_history.clear()
        moves = list(self.board.move_history)
        
        # Dummy rebuilding without proper SAN generation for now
        turn = "white"
        for move in moves:
            san = self.pseudo_san(move)
            self.move_history.add_move(san, turn)
            turn = "black" if turn == "white" else "white"

    def flip_board(self):
        self.chess_widget.set_flipped(not self.chess_widget.is_flipped)

    def resign(self):
        if self.ai_worker and self.ai_worker.isRunning():
            return
        if not self.game_active:
            return
        self.game_active = False
        self.chess_widget.set_active(False)
        self.show_game_over(f"White Wins" if self.ai_color == "white" else "Black Wins", "You resigned.")

    def set_depth(self, depth):
        self.ai_depth = depth

    def handle_human_move(self, start, end, promotion):
        if self.board.current_turn != self.player_color:
            return
            
        if promotion == "promotion_pending":
            self.promotion_move_cache = (start, end)
            self.show_promotion_dialog()
            return
            
        self.execute_move(start, end, promotion)

    def show_promotion_dialog(self):
        self.chess_widget.setEnabled(False)
        self.promo_widget = PromotionWidget(self.player_color, self.on_promotion_selected)
        self.board_layout.addWidget(self.promo_widget)
        self.board_layout.setCurrentWidget(self.promo_widget)

    def on_promotion_selected(self, piece_type):
        start, end = self.promotion_move_cache
        self.promotion_move_cache = None
        
        self.board_layout.removeWidget(self.promo_widget)
        self.promo_widget.deleteLater()
        self.chess_widget.setEnabled(True)
        
        self.execute_move(start, end, piece_type)

    def execute_move(self, start, end, promotion):
        if promotion == "":
            promotion = None
        moves = self.board.generate_legal_moves(start[0], start[1])
        move = next((m for m in moves if m.end == end and m.promotion == promotion), None)
        
        if move:
            self.board.make_move(move)
            san = self.pseudo_san(move)
            self.board.current_turn = "white" if self.board.current_turn == "black" else "black"
            
            self.chess_widget.highlight_last_move(start, end)
            self.chess_widget.clear_selection()
            self.move_history.add_move(san, move.moved_piece.color)
            
            self.update_state()

    def update_state(self):
        self.chess_widget.update()
        
        # Calculate captured pieces
        white_captured, black_captured = self.calculate_captured_material()
        
        # Update Evaluation
        eval_score = self.evaluator.evaluate(self.board) / 100.0
        self.eval_bar.set_evaluation(eval_score)
        
        # Update cards
        is_player_turn = (self.board.current_turn == self.player_color)
        self.bottom_card.set_active(is_player_turn and self.game_active)
        self.top_card.set_active(not is_player_turn and self.game_active)
        
        if self.player_color == "white":
            self.bottom_card.set_captured_pieces(white_captured)
            self.top_card.set_captured_pieces(black_captured)
        else:
            self.bottom_card.set_captured_pieces(black_captured)
            self.top_card.set_captured_pieces(white_captured)
        
        if not self.game_active:
            return

        
        if self.board.is_checkmate(self.board.current_turn):
            self.game_active = False
            self.chess_widget.set_active(False)
            winner = "White" if self.board.current_turn == "black" else "Black"
            self.show_game_over("Checkmate", f"{winner} wins!")
            return
            
        if self.board.is_stalemate(self.board.current_turn):
            self.game_active = False
            self.chess_widget.set_active(False)
            self.show_game_over("Draw", "Stalemate")
            return
            
        if not is_player_turn:
            self.start_ai_turn()

    def start_ai_turn(self):
        self.chess_widget.setEnabled(False)
        self.game_panel.setEnabled(False)
        
        self.ai_worker = AIWorker(self.board, self.ai_depth)
        self.ai_worker.finished.connect(self.on_ai_finished)
        self.ai_worker.start()

    def on_ai_finished(self, move_data):
        self.chess_widget.setEnabled(True)
        self.game_panel.setEnabled(True)
        
        if move_data:
            start, end, promotion = move_data
            self.execute_move(start, end, promotion)
        else:
            self.show_game_over("Game Over", "AI has no moves left.")

    def show_game_over(self, title, message):
        dlg = GameOverDialog(title, message, self)
        if dlg.exec():
            self.prompt_new_game()

    def calculate_captured_material(self):
        standard = {"pawn": 8, "rook": 2, "knight": 2, "bishop": 2, "queen": 1}
        current_white = {"pawn": 0, "rook": 0, "knight": 0, "bishop": 0, "queen": 0}
        current_black = {"pawn": 0, "rook": 0, "knight": 0, "bishop": 0, "queen": 0}
        
        for r in range(8):
            for c in range(8):
                p = self.board.position[r][c]
                if p and p.piece_type != "king":
                    if p.color == "white":
                        current_white[p.piece_type] += 1
                    else:
                        current_black[p.piece_type] += 1
                        
        white_captured = [] # Pieces white has captured (black pieces)
        black_captured = [] # Pieces black has captured (white pieces)
        
        for p_type, count in standard.items():
            for _ in range(count - current_black.get(p_type, 0)):
                white_captured.append(p_type)
            for _ in range(count - current_white.get(p_type, 0)):
                black_captured.append(p_type)
                
        return white_captured, black_captured

    def pseudo_san(self, move):
        piece = move.moved_piece
        letters = {"pawn": "", "knight": "N", "bishop": "B", "rook": "R", "queen": "Q", "king": "K"}
        
        if move.special == "castle_kingside":
            return "O-O"
        if move.special == "castle_queenside":
            return "O-O-O"
            
        p = letters[piece.piece_type]
        capture = "x" if move.captured_piece or move.special == "en_passant" else ""
        end_sq = f"{chr(ord('a') + move.end[1])}{8 - move.end[0]}"
        
        if piece.piece_type == "pawn" and capture:
            p = chr(ord('a') + move.start[1])
            
        promo = f"={letters.get(move.promotion, '').upper()}" if move.promotion else ""
        
        # Optional: check symbol
        # We don't append '+' here easily without making a move and checking, 
        # but the engine already takes care of the actual move. We can skip '+' for simplicity.
        
        return f"{p}{capture}{end_sq}{promo}"

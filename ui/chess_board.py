from PySide6.QtWidgets import QWidget, QSizePolicy, QMenu
from PySide6.QtGui import QPainter, QPen, QColor, QBrush
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import QRectF, Qt, Signal, QPoint, QTimer
from chess.board import Board
from chess.agent import ChessAgent

pieces = {
    ("white", "pawn"): QSvgRenderer("assets/pieces/Chess_plt45.svg"),
    ("white", "rook"): QSvgRenderer("assets/pieces/Chess_rlt45.svg"),
    ("white", "knight"): QSvgRenderer("assets/pieces/Chess_nlt45.svg"),
    ("white", "bishop"): QSvgRenderer("assets/pieces/Chess_blt45.svg"),
    ("white", "queen"): QSvgRenderer("assets/pieces/Chess_qlt45.svg"),
    ("white", "king"): QSvgRenderer("assets/pieces/Chess_klt45.svg"),
    ("black", "pawn"): QSvgRenderer("assets/pieces/Chess_pdt45.svg"),
    ("black", "rook"): QSvgRenderer("assets/pieces/Chess_rdt45.svg"),
    ("black", "knight"): QSvgRenderer("assets/pieces/Chess_ndt45.svg"),
    ("black", "bishop"): QSvgRenderer("assets/pieces/Chess_bdt45.svg"),
    ("black", "queen"): QSvgRenderer("assets/pieces/Chess_qdt45.svg"),
    ("black", "king"): QSvgRenderer("assets/pieces/Chess_kdt45.svg"),
}

class ChessBoard(QWidget):
    turn_changed = Signal(str)
    status_changed = Signal(str)
    def __init__(self):
        super().__init__()
        self.board = Board()
        self.selected_square = None
        self.legal_moves = []
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.agent = ChessAgent(depth=3)

    def make_ai_move(self):
        move = self.agent.get_move(self.board)

        if move is None:
            return

        self.board.make_move(move)
        self.board.current_turn = ("black" if self.board.current_turn == "white" else "white")

        self.turn_changed.emit(self.board.current_turn)
        self.update()


    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(QColor(255, 195, 0))

        board_size, sq_size, x_offset, y_offset = self.get_board_geometry()

        brushes = [
            QBrush(QColor(238, 238, 210)),
            QBrush(QColor(80, 135, 69))
        ]
        pen.setWidth((board_size * 0.004))
        painter.setPen(pen)

        for row in range(8):
            for col in range(8):
                x = x_offset + col * sq_size
                y = y_offset + row * sq_size

                rect = QRectF(x, y, sq_size, sq_size)
                painter.setBrush(brushes[(row + col) % 2])
                painter.drawRect(x, y, sq_size, sq_size)

                if self.selected_square == (row, col):
                    painter.setBrush(QBrush(QColor(255, 205, 50, 100)))
                    painter.setPen(pen)
                    painter.drawRect(rect)

        for move in self.legal_moves:
            row, col = move.end

            x = x_offset + col * sq_size
            y = y_offset + row * sq_size

            if move.captured_piece is not None or move.special == "en_passant":
                painter.setBrush(QBrush(QColor(170, 60, 60, 120)))
            else:
                painter.setBrush(QBrush(QColor(50, 50, 50, 100)))

            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QRectF(x + sq_size * 0.3, y + sq_size * 0.3, sq_size * 0.4, sq_size * 0.4))

        for row in range(8):
            for col in range(8):
                x = x_offset + col * sq_size
                y = y_offset + row * sq_size
                rect = QRectF(x, y, sq_size, sq_size)

                piece = self.board.position[row][col]
                if piece is not None:
                    renderer = pieces[(piece.color, piece.piece_type)]
                    renderer.render(painter, rect)

    def mousePressEvent(self, event):
        _, sq_size, x_offset, y_offset = self.get_board_geometry()

        x = event.position().x()
        y = event.position().y()

        col = int((x - x_offset) // sq_size)
        row = int((y - y_offset) // sq_size)

        if not (0 <= row < 8 and 0 <= col < 8):
            return

        position = (row, col)

        if self.selected_square is not None:
            matching_moves = [
                move for move in self.legal_moves
                if move.end == position
            ]

            if matching_moves:
                if matching_moves[0].promotion is not None:

                    menu = QMenu(self)
                    menu.addAction("Queen")
                    menu.addAction("Rook")
                    menu.addAction("Bishop")
                    menu.addAction("Knight")

                    action = menu.exec(
                        self.mapToGlobal(
                            QPoint(int(x), int(y))
                        )
                    )

                    if action is None:
                        return

                    choice = action.text().lower()

                    for move in matching_moves:
                        if move.promotion == choice:
                            break

                else:
                    move = matching_moves[0]

                self.board.make_move(move)

                self.board.current_turn = (
                    "black"
                    if self.board.current_turn == "white"
                    else "white"
                )

                self.selected_square = None
                self.legal_moves = []

                self.turn_changed.emit(self.board.current_turn)
                self.update()

                if self.board.current_turn == "black":
                    QTimer.singleShot(50, self.make_ai_move)

                return

            self.selected_square = None
            self.legal_moves = []

        piece = self.board.position[row][col]

        if piece is not None and piece.color == self.board.current_turn:
            self.selected_square = position
            self.legal_moves = self.board.generate_legal_moves(row, col)

        self.update()


    def get_board_geometry(self):
        board_size = min(self.width(), self.height()) - 10
        sq_size = board_size / 8

        x_offset = (self.width() - board_size) / 2
        y_offset = (self.height() - board_size) / 2

        return board_size, sq_size, x_offset, y_offset

    def new_game(self):
        self.board = Board()
        self.selected_square = None
        self.legal_moves = []
        self.update()
        self.turn_changed.emit(self.board.current_turn)

    def undo_move(self):
        if not self.board.move_history:
            return

        self.board.undo_move()
        self.board.current_turn = "black" if self.board.current_turn == "white" else "white"
        self.selected_square = None
        self.legal_moves = []
        self.turn_changed.emit(self.board.current_turn)
        self.update()
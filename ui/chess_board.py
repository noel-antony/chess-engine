from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QBrush
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import QRectF
from chess.board import Board

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

# inherits & overrides QWidget
class ChessBoard(QWidget):
    def __init__(self):
        super().__init__()
        self.board = Board()

    def paintEvent(self, event):
        #painter object
        painter = QPainter(self)
        pen = QPen(QColor(255, 195, 0))

        # alternate fills and setup pen
        brushes = [
            QBrush(QColor(238, 238, 210)),
            QBrush(QColor(80, 135, 69))
        ]
        board_size = min(self.width(), self.height()) - 10
        sq_size = board_size / 8
        pen.setWidth((board_size * 0.0045))
        painter.setPen(pen)

        # offsets to center the board
        x_offset = (self.width() - board_size) / 2
        y_offset = (self.height() - board_size) / 2

        # drawing board
        for row in range(8):
            for col in range(8):
                # calculate cell coords
                x = x_offset + col * sq_size
                y = y_offset + row * sq_size
                # draw cell
                painter.setBrush(brushes[(row + col) % 2])
                painter.drawRect(x, y, sq_size, sq_size)
                # render piece
                rect = QRectF(x, y, sq_size, sq_size)
                piece = self.board.position[row][col]
                if piece is not None:
                    renderer = pieces[(piece.color, piece.piece_type)]
                    renderer.render(painter, rect)

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QBrush
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import QRectF, Qt
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
        self.selected_square = None
        self.legal_moves = []

    def paintEvent(self, event):
        #painter object
        painter = QPainter(self)
        pen = QPen(QColor(255, 195, 0))

        board_size, sq_size, x_offset, y_offset = self.get_board_geometry()

        # alternate fills and setup pen
        brushes = [
            QBrush(QColor(238, 238, 210)),
            QBrush(QColor(80, 135, 69))
        ]
        pen.setWidth((board_size * 0.004))
        painter.setPen(pen)


        # drawing board
        for row in range(8):
            for col in range(8):
                # calculate cell coords
                x = x_offset + col * sq_size
                y = y_offset + row * sq_size

                rect = QRectF(x, y, sq_size, sq_size)
                # draw cell
                painter.setBrush(brushes[(row + col) % 2])
                painter.drawRect(x, y, sq_size, sq_size)

                if self.selected_square == (row, col):
                    painter.setBrush(QBrush(QColor(255, 205, 50, 100)))
                    painter.setPen(pen)
                    painter.drawRect(rect)

                piece = self.board.position[row][col]

                if piece is not None:
                    renderer = pieces[(piece.color, piece.piece_type)]
                    renderer.render(painter, rect)

        for move in self.legal_moves:
            row, col = move.end

            x = x_offset + col * sq_size
            y = y_offset + row * sq_size

            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(QColor(50, 50, 50, 100)))
            painter.drawEllipse(QRectF(x + sq_size * 0.35, y + sq_size * 0.35, sq_size * 0.3, sq_size * 0.3))

    def mousePressEvent(self, event):
        _, sq_size, x_offset, y_offset = self.get_board_geometry()

        x = event.position().x()
        y = event.position().y()

        col = int((x - x_offset) // sq_size)
        row = int((y - y_offset) // sq_size)

        if 0 <= row < 8 and 0 <= col < 8:
            if self.selected_square is not None:
                
                for move in self.legal_moves:
                    if move.end == (row, col):
                        self.board.make_move(move)
                        self.selected_square = None
                        self.legal_moves = []
                        self.update()
                        return
                    
            print("Clicked:", row, col)
            self.selected_square = (row, col)
            self.legal_moves = self.board.generate_legal_moves(row, col)
            print("Moves:", [(m.start, m.end) for m in self.legal_moves])
            self.update()
            
    def get_board_geometry(self):
        board_size = min(self.width(), self.height()) - 10
        sq_size = board_size / 8

        x_offset = (self.width() - board_size) / 2
        y_offset = (self.height() - board_size) / 2

        return board_size, sq_size, x_offset, y_offset
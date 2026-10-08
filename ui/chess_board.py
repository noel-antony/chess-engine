from PySide6.QtWidgets import QWidget, QSizePolicy, QMenu
from PySide6.QtGui import QPainter, QPen, QColor, QBrush, QFont, QFontMetrics
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import QRectF, Qt, Signal, QPoint, QTimer
from chess.board import Board
from ui.styles import BOARD_LIGHT, BOARD_DARK

class ChessBoardWidget(QWidget):
    move_requested = Signal(tuple, tuple, object)  # start, end, promotion
    square_selected = Signal(tuple)
    
    def __init__(self, board: Board):
        super().__init__()
        self.board = board
        self.selected_square = None
        self.legal_moves = []
        self.last_move = None
        self.is_flipped = False
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(400, 400)
        self.setMouseTracking(True)
        self.hovered_square = None
        self.animation_step = 0
        self.is_active = False
        
        self.pieces_svg = {}
        self.load_pieces()

    def load_pieces(self):
        colors = ["white", "black"]
        types = ["pawn", "rook", "knight", "bishop", "queen", "king"]
        codes = {"white": "l", "black": "d"}
        letters = {"pawn": "p", "rook": "r", "knight": "n", "bishop": "b", "queen": "q", "king": "k"}
        
        for c in colors:
            for t in types:
                file_path = f"assets/pieces/Chess_{letters[t]}{codes[c]}t45.svg"
                self.pieces_svg[(c, t)] = QSvgRenderer(file_path)

    def set_board(self, board):
        self.board = board
        self.update()

    def set_flipped(self, flipped):
        self.is_flipped = flipped
        self.update()

    def set_active(self, active):
        self.is_active = active
        self.update()

    def highlight_last_move(self, start, end):
        self.last_move = (start, end)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        board_size, sq_size, x_offset, y_offset = self.get_board_geometry()
        
        # Draw border
        painter.setPen(QPen(QColor("#30353D"), 2))
        painter.drawRect(int(x_offset), int(y_offset), int(board_size), int(board_size))
        
        light_brush = QBrush(QColor(BOARD_LIGHT))
        dark_brush = QBrush(QColor(BOARD_DARK))
        
        font = QFont("Segoe UI", max(8, int(sq_size * 0.15)), QFont.Bold)
        painter.setFont(font)
        
        # Draw squares
        for row in range(8):
            for col in range(8):
                render_row = 7 - row if self.is_flipped else row
                render_col = 7 - col if self.is_flipped else col
                
                x = x_offset + render_col * sq_size
                y = y_offset + render_row * sq_size
                
                rect = QRectF(x, y, sq_size, sq_size)
                
                if (row + col) % 2 == 0:
                    painter.setBrush(light_brush)
                    text_color = QColor(BOARD_DARK)
                else:
                    painter.setBrush(dark_brush)
                    text_color = QColor(BOARD_LIGHT)
                    
                painter.setPen(Qt.NoPen)
                painter.drawRect(rect)
                
                # Last move highlight
                if self.last_move and (row, col) in self.last_move:
                    painter.setBrush(QBrush(QColor(255, 255, 0, 80)))
                    painter.drawRect(rect)
                    
                # Selected square highlight
                if self.selected_square == (row, col):
                    painter.setBrush(QBrush(QColor(79, 140, 255, 100)))
                    painter.drawRect(rect)
                    
                # Hover effect
                if self.hovered_square == (row, col):
                    painter.setPen(QPen(QColor(255, 255, 255, 100), 2))
                    painter.setBrush(Qt.NoBrush)
                    painter.drawRect(rect.adjusted(1, 1, -1, -1))
                
                # Draw coordinates
                painter.setPen(text_color)
                if render_col == 0:  # Ranks
                    rank = str(8 - row)
                    painter.drawText(int(x + 2), int(y + sq_size * 0.2), rank)
                if render_row == 7:  # Files
                    file_name = chr(ord('a') + col)
                    painter.drawText(int(x + sq_size - sq_size * 0.15 - 5), int(y + sq_size - 4), file_name)

        # Highlight king in check
        white_in_check = self.board.is_in_check("white")
        black_in_check = self.board.is_in_check("black")
        
        if white_in_check or black_in_check:
            for r in range(8):
                for c in range(8):
                    piece = self.board.position[r][c]
                    if piece and piece.piece_type == "king":
                        if (piece.color == "white" and white_in_check) or (piece.color == "black" and black_in_check):
                            render_row = 7 - r if self.is_flipped else r
                            render_col = 7 - c if self.is_flipped else c
                            x = x_offset + render_col * sq_size
                            y = y_offset + render_row * sq_size
                            
                            # Radial gradient for check
                            from PySide6.QtGui import QRadialGradient
                            grad = QRadialGradient(x + sq_size/2, y + sq_size/2, sq_size/2)
                            grad.setColorAt(0, QColor(255, 0, 0, 200))
                            grad.setColorAt(1, QColor(255, 0, 0, 0))
                            painter.setBrush(QBrush(grad))
                            painter.setPen(Qt.NoPen)
                            painter.drawRect(QRectF(x, y, sq_size, sq_size))

        # Draw legal move dots
        for move in self.legal_moves:
            r, c = move.end
            render_row = 7 - r if self.is_flipped else r
            render_col = 7 - c if self.is_flipped else c
            
            x = x_offset + render_col * sq_size
            y = y_offset + render_row * sq_size
            
            if move.captured_piece or move.special == "en_passant":
                painter.setPen(QPen(QColor(0, 0, 0, 50), sq_size * 0.1))
                painter.setBrush(Qt.NoBrush)
                painter.drawEllipse(QRectF(x + sq_size * 0.1, y + sq_size * 0.1, sq_size * 0.8, sq_size * 0.8))
            else:
                painter.setBrush(QBrush(QColor(0, 0, 0, 50)))
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(QRectF(x + sq_size * 0.35, y + sq_size * 0.35, sq_size * 0.3, sq_size * 0.3))

        # Draw pieces
        for row in range(8):
            for col in range(8):
                piece = self.board.position[row][col]
                if piece:
                    render_row = 7 - row if self.is_flipped else row
                    render_col = 7 - col if self.is_flipped else col
                    
                    x = x_offset + render_col * sq_size
                    y = y_offset + render_row * sq_size
                    rect = QRectF(x, y, sq_size, sq_size)
                    
                    renderer = self.pieces_svg.get((piece.color, piece.piece_type))
                    if renderer:
                        renderer.render(painter, rect)

        # Inactive overlay
        if not self.is_active:
            painter.setBrush(QBrush(QColor(24, 27, 31, 150)))
            painter.setPen(Qt.NoPen)
            painter.drawRect(int(x_offset), int(y_offset), int(board_size), int(board_size))

    def get_board_geometry(self):
        # Determine the square size based on the smallest dimension
        board_size = min(self.width(), self.height()) - 20
        sq_size = board_size / 8
        
        x_offset = (self.width() - board_size) / 2
        y_offset = (self.height() - board_size) / 2
        
        return board_size, sq_size, x_offset, y_offset

    def mouseMoveEvent(self, event):
        if not self.is_active:
            return
            
        _, sq_size, x_offset, y_offset = self.get_board_geometry()
        x = event.position().x()
        y = event.position().y()
        
        col = int((x - x_offset) // sq_size)
        row = int((y - y_offset) // sq_size)
        
        if self.is_flipped:
            row = 7 - row
            col = 7 - col
            
        if 0 <= row < 8 and 0 <= col < 8:
            if self.hovered_square != (row, col):
                self.hovered_square = (row, col)
                self.update()
        else:
            if self.hovered_square is not None:
                self.hovered_square = None
                self.update()

    def leaveEvent(self, event):
        self.hovered_square = None
        self.update()

    def mousePressEvent(self, event):
        if not self.is_active or event.button() != Qt.LeftButton:
            return
            
        _, sq_size, x_offset, y_offset = self.get_board_geometry()
        x = event.position().x()
        y = event.position().y()
        
        col = int((x - x_offset) // sq_size)
        row = int((y - y_offset) // sq_size)
        
        if self.is_flipped:
            row = 7 - row
            col = 7 - col
            
        if not (0 <= row < 8 and 0 <= col < 8):
            return
            
        position = (row, col)
        
        if self.selected_square is not None:
            matching_moves = [m for m in self.legal_moves if m.end == position]
            if matching_moves:
                if matching_moves[0].promotion:
                    # Notify controller to handle promotion
                    self.move_requested.emit(self.selected_square, position, "promotion_pending")
                else:
                    self.move_requested.emit(self.selected_square, position, None)
                return

        piece = self.board.position[row][col]
        if piece and piece.color == self.board.current_turn:
            self.selected_square = position
            self.legal_moves = self.board.generate_legal_moves(row, col)
            self.square_selected.emit(position)
        else:
            self.selected_square = None
            self.legal_moves = []
            
        self.update()

    def clear_selection(self):
        self.selected_square = None
        self.legal_moves = []
        self.update()
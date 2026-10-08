from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPainter, QColor
from PySide6.QtSvg import QSvgRenderer

class CapturedPiecesWidget(QWidget):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.captured = []
        self.setMinimumWidth(150)
        self.setFixedHeight(30)
        
        self.renderers = {}
        types = ["pawn", "knight", "bishop", "rook", "queen"]
        codes = {"white": "l", "black": "d"}
        letters = {"pawn": "p", "rook": "r", "knight": "n", "bishop": "b", "queen": "q"}
        
        for t in types:
            file_path = f"assets/pieces/Chess_{letters[t]}{codes[color]}t45.svg"
            self.renderers[t] = QSvgRenderer(file_path)

    def set_captured(self, captured_list):
        # Sort pieces by value
        order = {"queen": 0, "rook": 1, "bishop": 2, "knight": 3, "pawn": 4}
        self.captured = sorted(captured_list, key=lambda x: order.get(x, 5))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        x = 0
        y = 5
        size = 20
        overlap = 10
        
        for piece in self.captured:
            renderer = self.renderers.get(piece)
            if renderer:
                renderer.render(painter, f"{x},{y},{size},{size}")
                x += overlap

class PlayerCard(QFrame):
    def __init__(self, name="Player", color="White", is_active=False, is_ai=False):
        super().__init__()
        self.name = name
        self.color = color
        self.is_active = is_active
        self.is_ai = is_ai
        
        self.init_ui()

    def init_ui(self):
        self.setObjectName("playerCard")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        
        # Color indicator
        self.indicator = QLabel()
        self.indicator.setFixedSize(16, 16)
        self.indicator.setStyleSheet(
            f"background-color: {'#FFF' if self.color.lower() == 'white' else '#222'};"
            "border: 1px solid #555; border-radius: 8px;"
        )
        
        # Name and AI indicator
        name_layout = QVBoxLayout()
        self.name_label = QLabel(self.name)
        self.name_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        
        self.status_label = QLabel("Thinking..." if self.is_ai and self.is_active else self.color)
        self.status_label.setObjectName("subtitleLabel")
        
        name_layout.addWidget(self.name_label)
        name_layout.addWidget(self.status_label)
        name_layout.setSpacing(2)
        
        # Captured pieces
        # If this is the White player's card, they capture Black pieces.
        captured_color = "black" if self.color.lower() == "white" else "white"
        self.captured_widget = CapturedPiecesWidget(captured_color)
        
        layout.addWidget(self.indicator)
        layout.addLayout(name_layout)
        layout.addStretch()
        layout.addWidget(self.captured_widget)
        
        self.update_style()

    def set_captured_pieces(self, captured_list):
        self.captured_widget.set_captured(captured_list)
        
    def set_active(self, active):
        self.is_active = active
        if self.is_ai:
            self.status_label.setText("Thinking..." if active else self.color)
        self.update_style()
        
    def update_style(self):
        if self.is_active:
            self.setStyleSheet("QFrame#playerCard { border: 2px solid #4F8CFF; background-color: #20242A; }")
        else:
            self.setStyleSheet("QFrame#playerCard { border: 1px solid #30353D; background-color: #181B1F; }")

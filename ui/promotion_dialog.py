from PySide6.QtWidgets import QWidget, QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtGui import QPainter, QColor, QPen

class PromotionWidget(QWidget):
    def __init__(self, color, callback):
        super().__init__()
        self.color = color
        self.callback = callback
        self.setFixedSize(240, 60)
        self.pieces = ["queen", "rook", "bishop", "knight"]
        
        # Load SVGs
        self.renderers = {}
        codes = {"white": "l", "black": "d"}
        letters = {"queen": "q", "rook": "r", "bishop": "b", "knight": "n"}
        for p in self.pieces:
            self.renderers[p] = QSvgRenderer(f"assets/pieces/Chess_{letters[p]}{codes[color]}t45.svg")
            
        self.hovered_index = -1
        self.setMouseTracking(True)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        painter.setBrush(QColor(24, 27, 31, 230))
        painter.setPen(QPen(QColor(79, 140, 255), 2))
        painter.drawRoundedRect(0, 0, 240, 60, 8, 8)
        
        for i, piece in enumerate(self.pieces):
            x = i * 60
            if i == self.hovered_index:
                painter.setBrush(QColor(79, 140, 255, 80))
                painter.setPen(Qt.NoPen)
                painter.drawRect(x, 0, 60, 60)
                
            renderer = self.renderers[piece]
            renderer.render(painter, f"{x+5},{5},{50},{50}")

    def mouseMoveEvent(self, event):
        x = event.position().x()
        index = int(x // 60)
        if 0 <= index < 4:
            if self.hovered_index != index:
                self.hovered_index = index
                self.update()
        else:
            if self.hovered_index != -1:
                self.hovered_index = -1
                self.update()

    def leaveEvent(self, event):
        self.hovered_index = -1
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            x = event.position().x()
            index = int(x // 60)
            if 0 <= index < 4:
                self.callback(self.pieces[index])

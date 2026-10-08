from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt

class GameOverDialog(QDialog):
    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setFixedSize(300, 180)
        self.setStyleSheet("QDialog { background-color: #181B1F; border: 2px solid #30353D; border-radius: 10px; }")
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        
        lbl_title = QLabel(title)
        lbl_title.setObjectName("titleLabel")
        lbl_title.setAlignment(Qt.AlignCenter)
        
        if "win" in title.lower() or "mate" in title.lower():
            lbl_title.setStyleSheet("color: #3FB950; font-size: 24px; font-weight: bold;")
            
        lbl_msg = QLabel(message)
        lbl_msg.setObjectName("subtitleLabel")
        lbl_msg.setAlignment(Qt.AlignCenter)
        lbl_msg.setWordWrap(True)
        
        layout.addWidget(lbl_title)
        layout.addWidget(lbl_msg)
        
        btn_layout = QHBoxLayout()
        btn_close = QPushButton("Close")
        btn_close.clicked.connect(self.reject)
        
        btn_new = QPushButton("New Game")
        btn_new.setObjectName("accentButton")
        btn_new.clicked.connect(self.accept)
        
        btn_layout.addWidget(btn_close)
        btn_layout.addWidget(btn_new)
        
        layout.addLayout(btn_layout)

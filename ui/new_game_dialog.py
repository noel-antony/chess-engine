from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox
)
from PySide6.QtCore import Qt

class NewGameDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Game")
        self.setFixedSize(320, 260)
        self.setStyleSheet("QDialog { background-color: #181B1F; border: 1px solid #30353D; }")
        
        self.player_color = "White"
        self.difficulty = "Medium"
        self.depth = 3
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        title = QLabel("Start New Game")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Color Selection
        color_layout = QHBoxLayout()
        color_layout.addWidget(QLabel("Play as:"))
        self.combo_color = QComboBox()
        self.combo_color.addItems(["White", "Black"])
        color_layout.addWidget(self.combo_color)
        layout.addLayout(color_layout)
        
        # Difficulty
        diff_layout = QHBoxLayout()
        diff_layout.addWidget(QLabel("AI Level:"))
        self.combo_diff = QComboBox()
        self.combo_diff.addItems(["Easy (Depth 2)", "Medium (Depth 3)", "Hard (Depth 4)", "Expert (Depth 5)"])
        self.combo_diff.setCurrentIndex(1)
        diff_layout.addWidget(self.combo_diff)
        layout.addLayout(diff_layout)
        
        layout.addStretch()
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_cancel = QPushButton("Cancel")
        btn_cancel.clicked.connect(self.reject)
        
        btn_start = QPushButton("Start Game")
        btn_start.setObjectName("accentButton")
        btn_start.clicked.connect(self.accept)
        
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_start)
        
        layout.addLayout(btn_layout)

    def accept(self):
        self.player_color = self.combo_color.currentText()
        diff_text = self.combo_diff.currentText()
        if "2" in diff_text:
            self.depth = 2
        elif "3" in diff_text:
            self.depth = 3
        elif "4" in diff_text:
            self.depth = 4
        else:
            self.depth = 5
            
        super().accept()

import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from ui.chess_board import ChessBoard

# app initialization
app = QApplication(sys.argv)

# main window setup
window = QWidget()
window.setWindowTitle("Chess Engine")
window.resize(1800, 800)

layout = QVBoxLayout()
board = ChessBoard()
layout.addWidget(board)

window.setLayout(layout)
window.show()

# start event loop
sys.exit(app.exec())
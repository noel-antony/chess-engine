import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton
)
from PySide6.QtCore import Qt
from ui.chess_board import ChessBoard

app = QApplication(sys.argv)
app.setStyleSheet("""
    QLabel {
        color: #eeeeee;
        font-size: 18px;
    }

    QPushButton {
        background-color: #2b2b2b;
        color: white;
        font-size: 16px;
        padding: 8px 20px;
        border-radius: 6px;
    }

    QPushButton:hover {
        background-color: #444444;
    }

    QPushButton:pressed {
        background-color: #222222;
    }
""")

window = QWidget()
window.setWindowTitle("Chess Engine")
window.resize(1800, 800)

main_layout = QVBoxLayout()

turn_label = QLabel("White to move")
turn_label.setAlignment(Qt.AlignCenter)

status_label = QLabel("")
status_label.setAlignment(Qt.AlignCenter)

board = ChessBoard()
board.turn_changed.connect(
    lambda turn: turn_label.setText(f"{turn.capitalize()} to move")
)
board.status_changed.connect(status_label.setText)

controls = QHBoxLayout()
controls.setAlignment(Qt.AlignCenter)

new_game_button = QPushButton("New Game")
undo_button = QPushButton("Undo")

game_area = QHBoxLayout()

board_container = QWidget()
board_layout = QVBoxLayout(board_container)
board_layout.addWidget(board)
board_layout.setAlignment(Qt.AlignCenter)

promotion_widget = QWidget()
promotion_widget.setFixedWidth(100)

promotion_layout = QVBoxLayout(promotion_widget)
promotion_layout.setAlignment(Qt.AlignCenter)

game_area.addWidget(board_container, 1)
game_area.addWidget(promotion_widget)

new_game_button.clicked.connect(board.new_game)
undo_button.clicked.connect(board.undo_move)

new_game_button.setFixedWidth(120)
undo_button.setFixedWidth(120)

controls.addWidget(new_game_button)
controls.addWidget(undo_button)

main_layout.addWidget(turn_label)
main_layout.addWidget(status_label) 
main_layout.addWidget(board, 1)
main_layout.addLayout(controls)

window.setLayout(main_layout)
window.show()

sys.exit(app.exec())
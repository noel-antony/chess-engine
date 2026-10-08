from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QLabel
)
from PySide6.QtCore import Qt

class MoveHistory(QWidget):
    def __init__(self):
        super().__init__()
        self.moves = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        header = QLabel("Move History")
        header.setObjectName("titleLabel")
        header.setAlignment(Qt.AlignCenter)
        
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["#", "White", "Black"])
        
        header_view = self.table.horizontalHeader()
        header_view.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header_view.setSectionResizeMode(1, QHeaderView.Stretch)
        header_view.setSectionResizeMode(2, QHeaderView.Stretch)
        
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.NoSelection)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        
        layout.addWidget(header)
        layout.addWidget(self.table)

    def add_move(self, move_str, turn):
        if turn == "white":
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            num_item = QTableWidgetItem(f"{row + 1}.")
            num_item.setTextAlignment(Qt.AlignCenter)
            num_item.setForeground(Qt.gray)
            
            white_item = QTableWidgetItem(move_str)
            white_item.setTextAlignment(Qt.AlignCenter)
            
            self.table.setItem(row, 0, num_item)
            self.table.setItem(row, 1, white_item)
        else:
            row = self.table.rowCount() - 1
            if row < 0:
                self.table.insertRow(0)
                row = 0
                num_item = QTableWidgetItem("1.")
                num_item.setTextAlignment(Qt.AlignCenter)
                num_item.setForeground(Qt.gray)
                self.table.setItem(row, 0, num_item)
                
            black_item = QTableWidgetItem(move_str)
            black_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 2, black_item)
            
        self.table.scrollToBottom()

    def clear(self):
        self.table.setRowCount(0)
        self.moves.clear()

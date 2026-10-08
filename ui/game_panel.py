from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QFrame, QHBoxLayout, QComboBox, QSlider
)
from PySide6.QtCore import Qt, Signal

class GamePanel(QWidget):
    new_game_requested = Signal()
    undo_requested = Signal()
    flip_requested = Signal()
    resign_requested = Signal()
    depth_changed = Signal(int)
    
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setFixedWidth(260)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        # Actions Panel
        actions_frame = QFrame()
        actions_layout = QVBoxLayout(actions_frame)
        actions_layout.setSpacing(10)
        
        lbl_actions = QLabel("GAME")
        lbl_actions.setObjectName("subtitleLabel")
        actions_layout.addWidget(lbl_actions)
        
        self.btn_new = QPushButton("New Game")
        self.btn_new.setObjectName("accentButton")
        self.btn_new.clicked.connect(self.new_game_requested.emit)
        
        self.btn_undo = QPushButton("Undo")
        self.btn_undo.clicked.connect(self.undo_requested.emit)
        
        self.btn_flip = QPushButton("Flip Board")
        self.btn_flip.clicked.connect(self.flip_requested.emit)
        
        self.btn_resign = QPushButton("Resign")
        self.btn_resign.clicked.connect(self.resign_requested.emit)
        
        actions_layout.addWidget(self.btn_new)
        actions_layout.addWidget(self.btn_undo)
        actions_layout.addWidget(self.btn_flip)
        actions_layout.addWidget(self.btn_resign)
        
        # Engine Settings Panel
        engine_frame = QFrame()
        engine_layout = QVBoxLayout(engine_frame)
        engine_layout.setSpacing(10)
        
        lbl_engine = QLabel("ENGINE")
        lbl_engine.setObjectName("subtitleLabel")
        engine_layout.addWidget(lbl_engine)
        
        depth_layout = QHBoxLayout()
        depth_layout.addWidget(QLabel("Search Depth:"))
        self.lbl_depth_val = QLabel("3")
        self.lbl_depth_val.setAlignment(Qt.AlignRight)
        depth_layout.addWidget(self.lbl_depth_val)
        
        self.slider_depth = QSlider(Qt.Horizontal)
        self.slider_depth.setRange(1, 6)
        self.slider_depth.setValue(3)
        self.slider_depth.setTickPosition(QSlider.TicksBelow)
        self.slider_depth.setTickInterval(1)
        self.slider_depth.valueChanged.connect(self.on_depth_changed)
        
        engine_layout.addLayout(depth_layout)
        engine_layout.addWidget(self.slider_depth)

        layout.addWidget(actions_frame)
        layout.addWidget(engine_frame)
        layout.addStretch()

    def on_depth_changed(self, value):
        self.lbl_depth_val.setText(str(value))
        self.depth_changed.emit(value)

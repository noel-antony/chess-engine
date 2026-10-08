

BG_MAIN = "#111315"
BG_PANEL = "#181B1F"
BG_SECONDARY = "#20242A"
BORDER = "#30353D"
TEXT_PRIMARY = "#F2F4F7"
TEXT_SECONDARY = "#9AA3AE"
ACCENT = "#4F8CFF"
SUCCESS = "#3FB950"
WARNING = "#D29922"
DANGER = "#F85149"
HIGHLIGHT = "#283445"

# Board Colors
BOARD_LIGHT = "#E7DCC8"
BOARD_DARK = "#8B6F47"
SQUARE_SELECTED = "rgba(79, 140, 255, 0.4)"
SQUARE_LAST_MOVE = "rgba(255, 255, 0, 0.3)"
SQUARE_CHECK = "rgba(248, 81, 73, 0.7)"

COMMON_STYLE = f"""
QWidget {{
    background-color: {BG_MAIN};
    color: {TEXT_PRIMARY};
    font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
}}

/* Panels */
QFrame, QScrollArea {{
    background-color: {BG_PANEL};
    border: 1px solid {BORDER};
    border-radius: 8px;
}}

/* Secondary Panels */
QListWidget, QTableWidget {{
    background-color: {BG_SECONDARY};
    border: 1px solid {BORDER};
    border-radius: 6px;
    outline: none;
}}

/* Buttons */
QPushButton {{
    background-color: {BG_SECONDARY};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: bold;
    font-size: 14px;
}}
QPushButton:hover {{
    background-color: {HIGHLIGHT};
    border: 1px solid {ACCENT};
}}
QPushButton:pressed {{
    background-color: {ACCENT};
    color: white;
}}
QPushButton:disabled {{
    background-color: {BG_MAIN};
    color: {TEXT_SECONDARY};
    border: 1px solid {BORDER};
}}

/* Accent Button */
QPushButton#accentButton {{
    background-color: {ACCENT};
    color: white;
    border: none;
}}
QPushButton#accentButton:hover {{
    background-color: #3B72DE;
}}
QPushButton#accentButton:pressed {{
    background-color: #2955B5;
}}

/* Labels */
QLabel {{
    background-color: transparent;
    border: none;
}}

QLabel#titleLabel {{
    font-size: 20px;
    font-weight: bold;
    color: {TEXT_PRIMARY};
}}

QLabel#subtitleLabel {{
    font-size: 14px;
    color: {TEXT_SECONDARY};
}}

/* Combo Box */
QComboBox {{
    background-color: {BG_SECONDARY};
    border: 1px solid {BORDER};
    border-radius: 4px;
    padding: 6px 10px;
    color: {TEXT_PRIMARY};
}}
QComboBox:hover {{
    border: 1px solid {ACCENT};
}}
QComboBox::drop-down {{
    border: none;
    width: 24px;
}}

/* Slider */
QSlider::groove:horizontal {{
    border: 1px solid {BORDER};
    height: 6px;
    background: {BG_SECONDARY};
    border-radius: 3px;
}}
QSlider::handle:horizontal {{
    background: {ACCENT};
    width: 16px;
    margin: -5px 0;
    border-radius: 8px;
}}

/* Scrollbar */
QScrollBar:vertical {{
    background-color: {BG_PANEL};
    width: 10px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background-color: {BORDER};
    min-height: 20px;
    border-radius: 5px;
}}
QScrollBar::handle:vertical:hover {{
    background-color: {TEXT_SECONDARY};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
"""

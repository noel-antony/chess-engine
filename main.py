import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
import os

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Ensure current working directory is correct for assets
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

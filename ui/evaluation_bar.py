from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import Qt

class EvaluationBar(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(20)
        self.evaluation = 0.0 # Positive means White is better, Negative means Black is better

    def set_evaluation(self, eval_score):
        # Cap evaluation at +/- 10
        self.evaluation = max(-10.0, min(10.0, eval_score))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()

        # Background (Black part)
        painter.fillRect(0, 0, w, h, QColor(40, 40, 40))

        # Calculate height for white part (50% is 0 eval)
        # We'll map [-10, 10] to [0, h]
        # At eval 0, white_h = h/2.
        # Eval 10 = full white. Eval -10 = full black
        
        # Logistic curve or just linear?
        # A simple non-linear curve to make small differences visible:
        percentage = 0.5 + (self.evaluation / 20.0)
        
        white_h = h * percentage
        
        # Draw White part (from bottom up)
        painter.fillRect(0, int(h - white_h), w, int(white_h), QColor(220, 220, 220))
        
        # Draw border
        painter.setPen(QColor(60, 60, 60))
        painter.drawRect(0, 0, w - 1, h - 1)

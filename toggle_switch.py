from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, Signal, Property
from PySide6.QtGui import QCursor, QPainter, QColor

class ToggleSwitch(QWidget):
    stateChanged = Signal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(50, 25)
        self.checked = False
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self._value = 1.0 if self.checked else 0.0
        self._anim = QPropertyAnimation(self, b"value")
        self._anim.setDuration(200)
        self._anim.valueChanged.connect(self.update)
        
    def setChecked(self, checked):
        self.checked = checked
        self._anim.stop()
        self._anim.setStartValue(self._value)
        self._anim.setEndValue(1.0 if checked else 0.0)
        self._anim.start()
        
    def isChecked(self):
        return self.checked
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setChecked(not self.checked)
            self.stateChanged.emit(self.checked)
            
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw background
        bg_color = QColor("#3498db") if self.checked else QColor("#bdc3c7")
        painter.setBrush(bg_color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 12, 12)
        
        # Draw circle
        circle_x = int(2 + (self.width() - 22 - 2) * self._value)
        painter.setBrush(QColor("white"))
        painter.drawEllipse(circle_x, 2, 20, 20)

    def getValue(self):
        return self._value

    def setValue(self, value):
        self._value = value
        self.update()

    value = Property(float, getValue, setValue)
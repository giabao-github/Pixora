from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt

class OverlayWidget(QWidget):
    def __init__(self, parent, panel):
        super().__init__(parent)
        self.panel = panel
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.setStyleSheet("background: rgba(44, 62, 80, 0.25)")
        self.setGeometry(parent.rect())
        self.raise_()

    def mousePressEvent(self, event):
        # Only close if click is outside the panel
        if not self.panel.geometry().contains(event.pos()) and hasattr(self.parent(), 'close_settings_panel'):
            self.parent().close_settings_panel() 
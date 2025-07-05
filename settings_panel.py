from PySide6.QtWidgets import (
    QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QFrame, QGraphicsDropShadowEffect
)
from PySide6.QtGui import QCursor, QPainter, QColor, QPen, QPainterPath
from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication
from icon_provider import IconProvider
from toggle_switch import ToggleSwitch

class SettingsPanel(QWidget):
    def __init__(self, parent=None, auto_download=False, on_save=None, on_close=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.setContentsMargins(36, 36, 36, 36)
        layout.setSpacing(28)
        # Header with close button
        header_layout = QHBoxLayout()
        title = QLabel(f"{IconProvider.get('settings')} Settings")
        title.setStyleSheet("""
            QLabel {
                color: #222F3E;
                font-size: 26px;
                font-weight: 800;
                margin-bottom: 0px;
                letter-spacing: 0.5px;
            }
        """)
        header_layout.addWidget(title)
        header_layout.addStretch()
        close_btn = QPushButton("✖")
        close_btn.setFixedSize(40, 40)
        close_btn.setStyleSheet("""
            QPushButton {
                background: #F1F2F6;
                color: #E74C3C;
                border: 2px solid #E74C3C;
                border-radius: 20px;
                font-size: 22px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #E74C3C;
                color: #FFF;
            }
        """)
        close_btn.setCursor(QCursor(Qt.PointingHandCursor))
        close_btn.clicked.connect(self.handle_close)
        header_layout.addWidget(close_btn)
        layout.addLayout(header_layout)
        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        divider.setStyleSheet("border: none; background: #E0E0E0; height: 2px; margin: 0 0 12px 0;")
        layout.addWidget(divider)
        # Auto-download toggle
        toggle_row = QHBoxLayout()
        toggle_label = QLabel(f"{IconProvider.get('auto')} Auto-download when valid URL is detected")
        toggle_label.setStyleSheet("""
            QLabel {
                color: #34495E;
                font-size: 17px;
                font-weight: 600;
            }
        """)
        toggle_row.addWidget(toggle_label)
        toggle_row.addStretch()
        self.toggle = ToggleSwitch()
        self.toggle.setChecked(auto_download)
        toggle_row.addWidget(self.toggle)
        layout.addLayout(toggle_row)
        layout.addStretch()
        # Save button
        btn = QPushButton("Save")
        btn.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: bold;
                padding: 16px 36px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #217DBB;
            }
        """)
        btn.setCursor(QCursor(Qt.PointingHandCursor))
        btn.clicked.connect(self.handle_save)
        layout.addWidget(btn)
        self.setLayout(layout)
        self.setFixedWidth(540)
        if screen := QGuiApplication.primaryScreen():
            self.setFixedHeight(screen.geometry().height())
        else:
            self.setFixedHeight(parent.height() if parent else 300)
        self.move(0, 0)
        # Add real drop shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(18)
        shadow.setOffset(-4, 0)
        shadow.setColor(QColor("#87CEFA"))
        self.setGraphicsEffect(shadow)
        self.on_save = on_save
        self.on_close = on_close

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        path = QPainterPath()
        radius = 24
        path.moveTo(rect.left() + radius, rect.top())
        path.arcTo(rect.left(), rect.top(), 2 * radius, 2 * radius, 90, 90)
        path.lineTo(rect.left(), rect.bottom() - radius)
        path.arcTo(rect.left(), rect.bottom() - 2 * radius, 2 * radius, 2*radius, 180, 90)
        path.lineTo(rect.right(), rect.bottom())
        path.lineTo(rect.right(), rect.top())
        path.closeSubpath()
        painter.setBrush(QColor("#FFFAFA"))
        painter.setPen(Qt.NoPen)
        painter.drawPath(path)
        thin_pen = QPen(QColor("#87CEFA"), 2)
        painter.setPen(thin_pen)
        painter.drawLine(rect.left() + radius, rect.top() + 1, rect.right() - 1, rect.top() + 1)
        painter.drawArc(rect.left() + 1, rect.top() + 1, 2*radius - 2, 2*radius - 2, 90*16, 90*16)
        painter.drawLine(rect.left() + 1, rect.top() + radius, rect.left() + 1, rect.bottom() - radius)
        painter.drawArc(rect.left() + 1, rect.bottom() - 2*radius + 1, 2*radius - 2, 2*radius - 2, 180*16, 90*16)
        painter.drawLine(rect.left() + radius, rect.bottom() - 1, rect.right() - 1, rect.bottom() - 1)
        thick_pen = QPen(QColor("#87CEFA"), 8)
        painter.setPen(thick_pen)
        painter.drawLine(rect.right() - 4, rect.top(), rect.right() - 4, rect.bottom())
        super().paintEvent(event)

    def handle_save(self):
        if self.on_save:
            self.on_save(self.toggle.isChecked())

    def handle_close(self):
        if self.on_close:
            self.on_close()

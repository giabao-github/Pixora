from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGraphicsDropShadowEffect,
    QFrame,
)
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtGui import QColor, QPainter, QPainterPath, QCursor, QIcon
from PySide6.QtCore import Qt, QSize
from toggle_switch import ToggleSwitch
from icon_provider import IconProvider


class SettingsPanel(QWidget):
    def __init__(self, parent=None, auto_download=False, on_save=None, on_close=None):
        super().__init__(parent)
        self.on_save = on_save
        self.on_close = on_close

        self.setObjectName("SettingsPanel")
        self.setFixedWidth(500)
        self.setStyleSheet(
            """
            QWidget#SettingsPanel {
                background-color: white;
                border-top-left-radius: 24px;
                border-bottom-left-radius: 24px;
                border-top-right-radius: 0px;
                border-bottom-right-radius: 0px;
            }
        """
        )

        self._init_ui(auto_download)
        self._add_shadow()

    def _init_ui(self, auto_download):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(24)

        layout.addLayout(self._build_header())
        layout.addWidget(self._divider())
        layout.addLayout(self._build_toggle_row(auto_download))
        layout.addStretch()
        layout.addWidget(self._build_save_button())

    def _build_header(self):
        header = QHBoxLayout()
        header.setSpacing(12)

        if icon_path := IconProvider.get_path("settings"):
            icon = self._svg_icon(icon_path, 28)
        else:
            icon = QWidget()
            icon.setFixedSize(28, 28)
        title = QLabel(" Settings")
        title.setStyleSheet("font-size: 24px; font-weight: 800; color: #2C3E50;")
        title.setMinimumHeight(28)

        close_btn = QPushButton()
        if close_icon_path := IconProvider.get_path("delete"):
            close_btn.setIcon(QIcon(close_icon_path))
            close_btn.setIconSize(QSize(32, 32))
        close_btn.setFixedSize(32, 32)
        close_btn.setCursor(QCursor(Qt.PointingHandCursor))
        close_btn.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                color: #7F8C8D;
                border: none;
                font-size: 20px;
            }
            QPushButton:hover {
                color: #E74C3C;
            }
        """
        )
        close_btn.clicked.connect(self.handle_close)

        self._add_icon_and_label_to_layout(header, icon, title)
        header.addWidget(close_btn)
        return header

    def _build_toggle_row(self, auto_download):
        row = QHBoxLayout()
        row.setSpacing(12)

        if icon_path := IconProvider.get_path("download"):
            icon = self._svg_icon(icon_path, 16)
        else:
            icon = QWidget()
            icon.setFixedSize(16, 16)
        label = QLabel("Auto-download when valid URL is detected")
        label.setStyleSheet("font-size: 16px; color: #2C3E50; font-weight: 600;")

        self.toggle = ToggleSwitch()
        self.toggle.setChecked(auto_download)

        self._add_icon_and_label_to_layout(row, icon, label)
        row.addWidget(self.toggle)
        return row

    def _add_icon_and_label_to_layout(self, layout, icon, label):
        layout.addWidget(icon)
        layout.addWidget(label)
        layout.addStretch()

    def _build_save_button(self):
        btn = QPushButton("  Save Settings")
        save_icon_path = IconProvider.get_path("save")
        if save_icon_path:
            btn.setIcon(QIcon(save_icon_path))
            btn.setIconSize(QSize(16, 16))
        btn.setCursor(QCursor(Qt.PointingHandCursor))
        btn.setFixedHeight(44)
        btn.setStyleSheet(
            """
            QPushButton {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498DB, stop:1 #2980B9
                );
                color: white;
                border: none;
                border-radius: 22px;
                font-size: 16px;
                font-weight: bold;
                padding: 0 24px;
            }
            QPushButton:hover {
                background: #2471A3;
            }
        """
        )
        btn.clicked.connect(self.handle_save)
        return btn

    def _divider(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFixedHeight(1)
        line.setStyleSheet("background-color: #E0E0E0;")
        return line

    def _svg_icon(self, path, size):
        import os

        if not os.path.exists(path):
            # Return an empty widget if icon doesn't exist
            widget = QWidget()
            widget.setFixedSize(size, size)
            return widget
        icon = QSvgWidget(path)
        icon.setFixedSize(size, size)
        return icon

    def _add_shadow(self):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(24)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        radius = 24
        path = QPainterPath()
        # Start at top-left, round top-left
        path.moveTo(rect.left() + radius, rect.top())
        path.arcTo(rect.left(), rect.top(), 2 * radius, 2 * radius, 90, 90)
        # Left edge
        path.lineTo(rect.left(), rect.bottom() - radius)
        # Round bottom-left
        path.arcTo(
            rect.left(), rect.bottom() - 2 * radius, 2 * radius, 2 * radius, 180, 90
        )
        # Bottom edge to bottom-right (square)
        path.lineTo(rect.right(), rect.bottom())
        # Top edge to top-right (square)
        path.lineTo(rect.right(), rect.top())
        # Close path
        path.lineTo(rect.left() + radius, rect.top())
        painter.fillPath(path, QColor("white"))
        super().paintEvent(event)

    def handle_save(self):
        if self.on_save:
            self.on_save(self.toggle.isChecked())

    def handle_close(self):
        if self.on_close:
            self.on_close()

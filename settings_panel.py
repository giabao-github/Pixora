from PySide6.QtWidgets import (
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QFrame,
    QGraphicsDropShadowEffect,
)
from PySide6.QtGui import QCursor, QPainter, QColor, QPen, QPainterPath
from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication
from icon_provider import IconProvider
from toggle_switch import ToggleSwitch


class SettingsPanel(QWidget):
    def __init__(self, parent=None, auto_download=False, on_save=None, on_close=None):
        super().__init__(parent)
        self.on_save = on_save
        self.on_close = on_close

        self._setup_layout()
        self._setup_header()
        self._setup_divider()
        self._setup_toggle_section(auto_download)
        self._setup_save_button()
        self._setup_styling_and_effects(parent)

    def _setup_layout(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(36, 36, 36, 36)
        self.layout.setSpacing(28)
        self.setLayout(self.layout)

    def _setup_header(self):
        header_layout = self._extracted_from__setup_toggle_section_2(
            "settings",
            " Settings",
            """
            QLabel {
                color: #222F3E;
                font-size: 26px;
                font-weight: 800;
                margin-bottom: 0px;
                letter-spacing: 0.5px;
            }
        """,
        )
        close_btn = QPushButton("✖")
        close_btn.setFixedSize(40, 40)
        close_btn.setStyleSheet(
            """
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
        """
        )
        close_btn.setCursor(QCursor(Qt.PointingHandCursor))
        close_btn.clicked.connect(self.handle_close)
        header_layout.addWidget(close_btn)

        self.layout.addLayout(header_layout)

    def _setup_divider(self):
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        divider.setStyleSheet(
            "border: none; background: #E0E0E0; height: 2px; margin: 0 0 12px 0;"
        )
        self.layout.addWidget(divider)

    def _setup_toggle_section(self, auto_download):
        toggle_row = self._extracted_from__setup_toggle_section_2(
            "auto",
            " Auto-download when valid URL is detected",
            """
            QLabel {
                color: #34495E;
                font-size: 17px;
                font-weight: 600;
            }
        """,
        )
        self.toggle = ToggleSwitch()
        self.toggle.setChecked(auto_download)
        toggle_row.addWidget(self.toggle)

        self.layout.addLayout(toggle_row)
        self.layout.addStretch()

    # TODO Rename this here and in `_setup_header` and `_setup_toggle_section`
    def _extracted_from__setup_toggle_section_2(self, arg0, arg1, arg2):
        result = QHBoxLayout()
        title = QLabel(f"{IconProvider.get(arg0)}{arg1}")
        title.setStyleSheet(arg2)
        result.addWidget(title)
        result.addStretch()
        return result

    def _setup_save_button(self):
        btn = QPushButton("Save")
        btn.setStyleSheet(
            """
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
        """
        )
        btn.setCursor(QCursor(Qt.PointingHandCursor))
        btn.clicked.connect(self.handle_save)
        self.layout.addWidget(btn)

    def _setup_styling_and_effects(self, parent):
        self.setFixedWidth(540)

        if screen := QGuiApplication.primaryScreen():
            self.setFixedHeight(screen.geometry().height())
        else:
            self.setFixedHeight(parent.height() if parent else 300)

        self.move(0, 0)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(18)
        shadow.setOffset(-4, 0)
        shadow.setColor(QColor("#87CEFA"))
        self.setGraphicsEffect(shadow)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        path = QPainterPath()
        radius = 24
        path.moveTo(rect.left() + radius, rect.top())
        path.arcTo(rect.left(), rect.top(), 2 * radius, 2 * radius, 90, 90)
        path.lineTo(rect.left(), rect.bottom() - radius)
        path.arcTo(
            rect.left(), rect.bottom() - 2 * radius, 2 * radius, 2 * radius, 180, 90
        )
        path.lineTo(rect.right(), rect.bottom())
        path.lineTo(rect.right(), rect.top())
        path.closeSubpath()
        painter.setBrush(QColor("#FFFAFA"))
        painter.setPen(Qt.NoPen)
        painter.drawPath(path)
        thin_pen = QPen(QColor("#87CEFA"), 2)
        painter.setPen(thin_pen)
        painter.drawLine(
            rect.left() + radius, rect.top() + 1, rect.right() - 1, rect.top() + 1
        )
        painter.drawArc(
            rect.left() + 1,
            rect.top() + 1,
            2 * radius - 2,
            2 * radius - 2,
            90 * 16,
            90 * 16,
        )
        painter.drawLine(
            rect.left() + 1,
            rect.top() + radius,
            rect.left() + 1,
            rect.bottom() - radius,
        )
        painter.drawArc(
            rect.left() + 1,
            rect.bottom() - 2 * radius + 1,
            2 * radius - 2,
            2 * radius - 2,
            180 * 16,
            90 * 16,
        )
        painter.drawLine(
            rect.left() + radius, rect.bottom() - 1, rect.right() - 1, rect.bottom() - 1
        )
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

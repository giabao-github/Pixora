from PySide6.QtWidgets import (
    QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QDialog
)
from PySide6.QtGui import QCursor
from PySide6.QtCore import Qt
from icon_provider import IconProvider
from toggle_switch import ToggleSwitch

class SettingsDialog(QDialog):
    def __init__(self, parent=None, auto_download=False):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setFixedSize(500, 200)
        self.setModal(True)
        self.setStyleSheet("""
            QDialog {
                background: #f8f9fa;
                border-radius: 12px;
            }
        """)
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(18)
        title = QLabel(f"{IconProvider.get('settings')} Settings")
        title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 20px;
                font-weight: bold;
                margin-bottom: 8px;
            }
        """)
        layout.addWidget(title)
        # Auto-download toggle
        toggle_row = QHBoxLayout()
        toggle_label = QLabel(f"{IconProvider.get('auto')} Auto-download when valid URL is detected")
        toggle_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 14px;
            }
        """)
        toggle_row.addWidget(toggle_label)
        toggle_row.addStretch()
        self.toggle = ToggleSwitch()
        self.toggle.setChecked(auto_download)
        toggle_row.addWidget(self.toggle)
        layout.addLayout(toggle_row)
        # Spacer
        layout.addStretch()
        # Close button
        btn = QPushButton("Save")
        btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                padding: 10px 18px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        btn.setCursor(QCursor(Qt.PointingHandCursor))
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)
        self.setLayout(layout)

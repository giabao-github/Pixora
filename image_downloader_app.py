import os
import json
import webbrowser
from pathlib import Path
from PySide6.QtWidgets import (
    QMainWindow, QPushButton, QLabel, QLineEdit, QFileDialog,
    QVBoxLayout, QHBoxLayout, QWidget, QGraphicsOpacityEffect,
    QGraphicsDropShadowEffect, QTextEdit, QSplitter,
    QGroupBox, QScrollArea, QMenu, QApplication
)
from PySide6.QtGui import QIcon, QCursor, QTextCursor
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QThread
from icon_provider import IconProvider
from settings_dialog import SettingsDialog
from download_worker import DownloadWorker

CONFIG_PATH = Path.home() / ".image_downloader_config.json"

class ImageDownloaderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{IconProvider.get('image')} Pixora")
        self.setFixedSize(950, 700)

        self.folder_path = ""
        self.downloaded_file_path = ""
        self.download_thread = None
        self.worker = None
        self.auto_download = False

        self.init_ui()
        self.load_settings()

    def init_ui(self):
        # Main widget with clean background
        main_widget = QWidget()
        main_widget.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)
        
        # Create splitter for better layout
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Main controls
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # Right panel - Status and output
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        # Set splitter proportions
        splitter.setSizes([650, 300])
        splitter.setCollapsible(0, False)
        splitter.setCollapsible(1, False)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.addWidget(splitter)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # --- Add Drop Shadow to Settings Button ---
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(8)
        shadow.setOffset(2, 2)
        self.settings_btn.setGraphicsEffect(shadow)

        # --- Add Drop Shadow to Main Window (optional, may not be visible on all OS) ---
        main_shadow = QGraphicsDropShadowEffect()
        main_shadow.setBlurRadius(16)
        main_shadow.setOffset(0, 4)
        self.setGraphicsEffect(main_shadow)

        # --- Add Opacity Effect to Status Label ---
        self.status_opacity = QGraphicsOpacityEffect()
        self.status_label.setGraphicsEffect(self.status_opacity)
        self.status_opacity.setOpacity(1.0)
        self.status_anim = QPropertyAnimation(self.status_opacity, b"opacity")
        self.status_anim.setDuration(350)

        # --- Add Opacity Effect to Download Button ---
        self.download_opacity = QGraphicsOpacityEffect()
        self.download_btn.setGraphicsEffect(self.download_opacity)
        self.download_opacity.setOpacity(1.0)
        self.download_anim = QPropertyAnimation(self.download_opacity, b"opacity")
        self.download_anim.setDuration(350)

    def create_left_panel(self):
        widget = QWidget()
        widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 8px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header with settings button
        header_layout = QHBoxLayout()
        header = QLabel(f"{IconProvider.get('image')} Pixora - Smart Image Downloader")
        header.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        header.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 10px;
                padding: 10px;
            }
        """)
        header_layout.addWidget(header)
        header_layout.addStretch()
        self.settings_btn = QPushButton(f"{IconProvider.get('settings')}")
        self.settings_btn.setFixedSize(36, 36)
        self.settings_btn.setStyleSheet("""
            QPushButton {
                background-color: #34495e;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                padding: 2px 2px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #2c3e50;
            }
            QPushButton:pressed {
                background-color: #1b2631;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #7f8c8d;
            }
        """)
        self.settings_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.settings_btn.clicked.connect(self.open_settings_dialog)
        header_layout.addWidget(self.settings_btn)
        layout.addLayout(header_layout)
        
        # URL Input Group
        url_group = QGroupBox("Image URL")
        url_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: #2c3e50;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        url_layout = QVBoxLayout()
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Paste or enter an image URL here...")
        self.url_input.textChanged.connect(self.on_url_change)
        self.url_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                font-size: 14px;
                background: white;
                color: #2c3e50;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        url_layout.addWidget(self.url_input)
        
        # URL action buttons
        url_buttons = QHBoxLayout()
        
        self.paste_btn = QPushButton(f"{IconProvider.get('paste')} Paste")
        self.paste_btn.clicked.connect(self.paste_clipboard)
        self.paste_btn.setStyleSheet(self.get_button_style("#9b59b6"))
        self.paste_btn.setCursor(QCursor(Qt.PointingHandCursor))
        
        self.clear_btn = QPushButton(f"{IconProvider.get('clear')} Clear")
        self.clear_btn.clicked.connect(self.clear_url)
        self.clear_btn.setStyleSheet(self.get_button_style("#e74c3c"))
        self.clear_btn.setCursor(QCursor(Qt.PointingHandCursor))
        
        url_buttons.addWidget(self.paste_btn)
        url_buttons.addWidget(self.clear_btn)
        url_layout.addLayout(url_buttons)
        
        url_group.setLayout(url_layout)
        layout.addWidget(url_group)
        
        # Custom Filename Group
        filename_group = QGroupBox("Custom Filename (Optional)")
        filename_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: #2c3e50;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        filename_layout = QVBoxLayout()
        
        self.filename_input = QLineEdit()
        self.filename_input.setPlaceholderText("Enter custom filename (optional)...")
        self.filename_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                font-size: 14px;
                background: white;
                color: #2c3e50;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        filename_layout.addWidget(self.filename_input)
        
        # Filename action buttons
        filename_buttons = QHBoxLayout()
        
        self.filename_paste_btn = QPushButton(f"{IconProvider.get('paste')} Paste")
        self.filename_paste_btn.clicked.connect(self.paste_filename)
        self.filename_paste_btn.setStyleSheet(self.get_button_style("#9b59b6"))
        self.filename_paste_btn.setCursor(QCursor(Qt.PointingHandCursor))
        
        self.filename_clear_btn = QPushButton(f"{IconProvider.get('clear')} Clear")
        self.filename_clear_btn.clicked.connect(self.clear_filename)
        self.filename_clear_btn.setStyleSheet(self.get_button_style("#e74c3c"))
        self.filename_clear_btn.setCursor(QCursor(Qt.PointingHandCursor))
        
        filename_buttons.addWidget(self.filename_paste_btn)
        filename_buttons.addWidget(self.filename_clear_btn)
        filename_layout.addLayout(filename_buttons)
        
        filename_group.setLayout(filename_layout)
        layout.addWidget(filename_group)
        
        # Download Location Group
        folder_group = QGroupBox("Download Location")
        folder_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: #2c3e50;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        folder_layout = QVBoxLayout()
        
        self.folder_label = QLabel("No folder selected")
        self.folder_label.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-size: 13px;
                font-weight: 600;
                background: #ecf0f1;
                padding: 10px;
                border-radius: 6px;
                border: 1px solid #bdc3c7;
            }
        """)
        folder_layout.addWidget(self.folder_label)
        
        folder_buttons = QHBoxLayout()
        
        self.folder_btn = QPushButton(f"{IconProvider.get('folder_open')} Choose Folder")
        self.folder_btn.clicked.connect(self.choose_folder)
        self.folder_btn.setStyleSheet(self.get_button_style("#27ae60"))
        self.folder_btn.setCursor(QCursor(Qt.PointingHandCursor))
        
        self.open_btn = QPushButton(f"{IconProvider.get('folder')} Open Folder")
        self.open_btn.clicked.connect(self.open_folder)
        self.open_btn.setEnabled(False)
        self.open_btn.setStyleSheet(self.get_button_style("#34495e"))
        self.open_btn.setCursor(QCursor(Qt.PointingHandCursor))
        
        folder_buttons.addWidget(self.folder_btn)
        folder_buttons.addWidget(self.open_btn)
        folder_layout.addLayout(folder_buttons)
        
        folder_group.setLayout(folder_layout)
        layout.addWidget(folder_group)
        
        # Download button
        self.download_btn = QPushButton(f"{IconProvider.get('download')} Download Image")
        self.download_btn.clicked.connect(self.download_image)
        self.download_btn.setStyleSheet(self.get_button_style("	#FF69B4", large=True))
        self.download_btn.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(self.download_btn)
        
        layout.addStretch()
        content_widget = QWidget()
        content_widget.setLayout(layout)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(content_widget)
        return scroll

    def create_right_panel(self):
        widget = QWidget()
        widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 8px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Status Group
        status_group = QGroupBox("Status")
        status_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: #2c3e50;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        status_layout = QVBoxLayout()
        
        self.status_label = QLabel("Ready to download images")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-size: 14px;
                padding: 12px;
                background: #ecf0f1;
                border-radius: 6px;
                border-left: 4px solid #3498db;
            }
        """)
        self.status_label.setWordWrap(True)
        
        status_layout.addWidget(self.status_label)
        status_group.setLayout(status_layout)
        layout.addWidget(status_group)
        
        # Download History Group
        history_group = QGroupBox(f"{IconProvider.get('history')} Download History")
        history_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: #2c3e50;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        history_layout = QVBoxLayout()
        
        self.history_text = QTextEdit()
        self.history_text.setReadOnly(True)
        self.history_text.setMaximumHeight(200)
        self.history_text.setStyleSheet("""
            QTextEdit {
                background: #f8f9fa;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                padding: 8px;
                font-size: 12px;
                color: #2c3e50;
            }
        """)
        self.history_text.setPlainText("No downloads yet...")
        
        history_layout.addWidget(self.history_text)
        
        clear_history_btn = QPushButton(f"{IconProvider.get('clear')} Clear History")
        clear_history_btn.clicked.connect(self.clear_history)
        clear_history_btn.setStyleSheet(self.get_button_style("#e74c3c", small=True))
        clear_history_btn.setCursor(QCursor(Qt.PointingHandCursor))
        history_layout.addWidget(clear_history_btn)
        
        history_group.setLayout(history_layout)
        layout.addWidget(history_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def get_button_style(self, color, large=False, small=False):
        size = "padding: 15px 20px; font-size: 14px;" if large else "padding: 8px 16px; font-size: 13px;" if small else "padding: 10px 16px; font-size: 13px;"
        # Special hover and pressed color for download button
        if color.strip() == "#FF69B4":
            hover_color = "#C94F8C"  # darker hot pink
            pressed_color = "#A13B6C"  # even darker
        else:
            hover_color = self.darken_color(color)
            pressed_color = self.darken_color(hover_color)
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                {size}
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {pressed_color};
            }}
            QPushButton:disabled {{
                background-color: #bdc3c7;
                color: #7f8c8d;
            }}
        """

    def darken_color(self, color):
        color_map = {
            "#3498db": "#2980b9",
            "#2980b9": "#1f618d",
            "#e74c3c": "#c0392b",
            "#c0392b": "#a93226",
            "#27ae60": "#229954",
            "#229954": "#1e8449",
            "#9b59b6": "#8e44ad",
            "#8e44ad": "#7d3c98",
            "#34495e": "#2c3e50",
            "#2c3e50": "#1b2631"
        }
        return color_map.get(color, "#2c3e50")

    def load_settings(self):
        if CONFIG_PATH.exists():
            try:
                with open(CONFIG_PATH, 'r') as f:
                    config = json.load(f)
                    self.folder_path = config.get("folder_path", "")
                    self.auto_download = config.get("auto_download", False)
                    self.update_folder_label()
            except:
                pass

    def save_settings(self):
        config = {
            "folder_path": self.folder_path,
            "auto_download": self.auto_download
        }
        try:
            with open(CONFIG_PATH, 'w') as f:
                json.dump(config, f)
        except:
            pass

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Download Folder")
        if folder:
            self.folder_path = folder
            self.update_folder_label()
            self.save_settings()

    def update_folder_label(self):
        if self.folder_path:
            # Show full path
            self.folder_label.setText(f"{IconProvider.get('folder')} {self.folder_path}")
            self.folder_label.setToolTip(self.folder_path)
            self.folder_label.setStyleSheet("""
                QLabel {
                    color: #27ae60;
                    font-size: 13px;
                    font-weight: 600;
                    background: #d5f4e6;
                    padding: 10px;
                    border-radius: 6px;
                    border: 1px solid #27ae60;
                }
            """)
            self.open_btn.setEnabled(True)
        else:
            self.folder_label.setText("No folder selected")
            self.folder_label.setStyleSheet("""
                QLabel {
                    color: #7f8c8d;
                    font-size: 13px;
                    background: #ecf0f1;
                    padding: 10px;
                    border-radius: 6px;
                    border: 1px solid #bdc3c7;
                }
            """)
            self.open_btn.setEnabled(False)

    def paste_clipboard(self):
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        if text:
            self.url_input.setText(text)
            self.show_status(f"{IconProvider.get('paste')} URL pasted from clipboard", "info")

    def clear_url(self):
        self.url_input.clear()
        self.show_status(f"{IconProvider.get('clear')} URL cleared", "info")

    def paste_filename(self):
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        if text:
            self.filename_input.setText(text)
            self.show_status(f"{IconProvider.get('paste')} Filename pasted from clipboard", "info")

    def clear_filename(self):
        self.filename_input.clear()
        self.show_status(f"{IconProvider.get('clear')} Filename cleared", "info")

    def clear_history(self):
        self.history_text.setPlainText("No downloads yet...")

    def on_url_change(self):
        if self.url_input.text().strip():
            self.show_status(f"{IconProvider.get('link')} URL entered", "info")
            if self.auto_download:
                QTimer.singleShot(1000, self.download_image)
        else:
            self.show_status("Ready to download images", "info")

    def download_image(self):
        url = self.url_input.text().strip()
        if not url:
            self.show_status(f"{IconProvider.get('warning')} Please enter an image URL", "error")
            return
        if not self.folder_path:
            self.show_status(f"{IconProvider.get('warning')} Please select a download folder", "error")
            return

        # --- Animate download button fade out ---
        self.download_anim.stop()
        self.download_anim.setStartValue(1.0)
        self.download_anim.setEndValue(0.5)
        self.download_anim.start()
        self.download_btn.setEnabled(False)
        self.download_btn.setIcon(QIcon("icons/spinner.svg"))  # Use a spinner SVG/GIF
        self.download_btn.setText(" Downloading...")
        self.paste_btn.setEnabled(False)

        # Get custom filename if provided
        custom_filename = self.filename_input.text().strip() if self.filename_input.text().strip() else None

        # Create worker thread
        self.download_thread = QThread()
        self.worker = DownloadWorker(url, self.folder_path, custom_filename)
        self.worker.moveToThread(self.download_thread)
        
        # Connect signals
        self.download_thread.started.connect(self.worker.download)
        self.worker.progress.connect(self.update_download_progress)
        self.worker.finished.connect(self.download_finished)
        self.worker.finished.connect(self.download_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.download_thread.finished.connect(self.download_thread.deleteLater)
        
        self.download_thread.start()

    def update_download_progress(self, message):
        self.show_status(message, "info")

    def download_finished(self, success, result, filename):
        # --- Animate download button fade in ---
        self.download_anim.stop()
        self.download_anim.setStartValue(0.5)
        self.download_anim.setEndValue(1.0)
        self.download_anim.start()
        self.download_btn.setEnabled(True)
        self.download_btn.setIcon(QIcon("icons/download.svg"))
        self.download_btn.setText(" Download Image")
        self.paste_btn.setEnabled(True)
        
        if success:
            self.downloaded_file_path = result
            self.show_status(f"{IconProvider.get('check')} Successfully downloaded: {filename}", "success")
            self.add_to_history(f"{IconProvider.get('check')} {filename}")
            # Clear custom filename after successful download
            self.filename_input.clear()
        else:
            self.show_status(f"{IconProvider.get('error')} Download failed: {result}", "error")
            self.add_to_history(f"{IconProvider.get('error')} Failed: {result}")

    def add_to_history(self, message):
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        current_text = self.history_text.toPlainText()
        if current_text == "No downloads yet...":
            new_text = f"[{timestamp}] {message}"
        else:
            new_text = f"{current_text}\n[{timestamp}] {message}"
        self.history_text.setPlainText(new_text)
        # Auto-scroll to bottom - Fixed cursor issue
        cursor = self.history_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.history_text.setTextCursor(cursor)

    def show_status(self, message, status_type="info"):
        colors = {
            "info": ("#3498db", "#e3f2fd"),
            "success": ("#27ae60", "#e8f5e8"),
            "error": ("#e74c3c", "#ffeaea"),
            "warning": ("#f39c12", "#fff3e0")
        }
        
        color, bg_color = colors.get(status_type, colors["info"])
        
        self.status_label.setText(message)
        self.status_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 14px;
                padding: 12px;
                background: {bg_color};
                border-radius: 6px;
                border-left: 4px solid {color};
                font-weight: 600;
            }}
        """)
        # --- Animate status label opacity ---
        self.status_anim.stop()
        self.status_opacity.setOpacity(0.0)
        self.status_anim.setStartValue(0.0)
        self.status_anim.setEndValue(1.0)
        self.status_anim.start()

    def open_folder(self):
        if self.folder_path and os.path.exists(self.folder_path):
            webbrowser.open(f"file://{self.folder_path}")
        else:
            self.show_status(f"{IconProvider.get('warning')} Folder not found", "error")

    def add_context_menu(self, widget):
        widget.setContextMenuPolicy(Qt.CustomContextMenu)
        def menu(pos):
            menu = QMenu()
            menu.addAction("Copy", widget.copy)
            menu.addAction("Paste", widget.paste)
            menu.addAction("Clear", widget.clear)
            menu.exec(widget.mapToGlobal(pos))
        widget.customContextMenuRequested.connect(menu)

    def open_settings_dialog(self):
        dlg = SettingsDialog(self, auto_download=self.auto_download)
        if dlg.exec():
            self.auto_download = dlg.toggle.isChecked()
            self.save_settings()
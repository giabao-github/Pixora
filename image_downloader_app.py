import os
import webbrowser
from PySide6.QtWidgets import (
    QMainWindow,  QFileDialog, QVBoxLayout, QWidget, QGraphicsOpacityEffect,
    QGraphicsDropShadowEffect, QSplitter, QMenu, QApplication
)
from PySide6.QtGui import QIcon, QTextCursor
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QThread
from icon_provider import IconProvider
from settings_panel import SettingsPanel
from download_worker import DownloadWorker
from widgets.overlay_widget import OverlayWidget
from widgets.panels import create_left_panel, create_right_panel
from settings.settings_manager import load_settings, save_settings

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
        self.settings_panel = None
        self.overlay = None
        self.custom_filename = ""

        self.init_ui()
        load_settings(self)

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
        left_panel = create_left_panel(self)
        splitter.addWidget(left_panel)
        
        # Right panel - Status and output
        right_panel = create_right_panel(self)
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

        self.settings_panel = SettingsPanel(self, auto_download=self.auto_download, on_save=self.handle_settings_save, on_close=self.close_settings_panel)
        self.settings_panel.hide()
        self.overlay = OverlayWidget(self, self.settings_panel)
        self.overlay.hide()

    def choose_folder(self):
        if folder := QFileDialog.getExistingDirectory(
            self, "Select Download Folder"
        ):
            self.folder_path = folder
            self.update_folder_label()
            save_settings(self)

    def update_folder_label(self):
        if self.folder_path:
            # Show full path
            self.folder_label.setText(f"{IconProvider.get('folder')} {self.folder_path}")
            self.folder_label.setToolTip(self.folder_path)
            self.set_folder_label_style_and_buttons(
                """
                QLabel {
                    color: #27ae60;
                    font-size: 13px;
                    font-weight: 600;
                    background: #d5f4e6;
                    padding: 10px;
                    border-radius: 6px;
                    border: 1px solid #27ae60;
                }
            """,
                True,
                ' Change Folder',
            )
        else:
            self.folder_label.setText("No folder selected")
            self.set_folder_label_style_and_buttons(
                """
                QLabel {
                    color: #7f8c8d;
                    font-size: 13px;
                    background: #ecf0f1;
                    padding: 10px;
                    border-radius: 6px;
                    border: 1px solid #bdc3c7;
                }
            """,
                False,
                ' Choose Folder',
            )

    def set_folder_label_style_and_buttons(self, folder_label, open_btn, folder_btn):
        self.folder_label.setStyleSheet(folder_label)
        self.open_btn.setEnabled(open_btn)
        self.folder_btn.setText(f"{IconProvider.get('folder_open')}{folder_btn}")

    def paste_clipboard(self):
        clipboard = QApplication.clipboard()
        if text := clipboard.text():
            self.url_input.setText(text)
            self.show_status(f"{IconProvider.get('paste')} URL pasted from clipboard", "info")

    def clear_url(self):
        self.url_input.clear()
        self.show_status(f"{IconProvider.get('clear')} URL cleared", "info")

    def paste_filename(self):
        clipboard = QApplication.clipboard()
        if text := clipboard.text():
            self.filename_input.setText(text)
            self.show_status(f"{IconProvider.get('paste')} Filename pasted from clipboard", "info")

    def clear_filename(self):
        self.filename_input.clear()
        self.show_status(f"{IconProvider.get('clear')} Filename cleared", "info")
        # Remove from config
        save_settings(self)

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
        custom_filename = self.filename_input.text().strip() or None

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
        self.show_settings_panel()

    def show_settings_panel(self):
        if not self.settings_panel.isVisible():
            self.settings_panel.toggle.setChecked(self.auto_download)
            self.overlay.show()
            self.overlay.raise_()
            self.settings_panel.setParent(self)
            self.settings_panel.setFixedHeight(self.height())
            self.settings_panel.move(self.width(), 0)
            self.settings_panel.show()
            self.settings_panel.raise_()
            # Animate slide-in
            from PySide6.QtCore import QPropertyAnimation
            anim = QPropertyAnimation(self.settings_panel, b"pos")
            anim.setDuration(250)
            anim.setStartValue(self.settings_panel.pos())
            anim.setEndValue(self.rect().topRight() - self.settings_panel.rect().topRight())
            anim.start()
            self._settings_anim = anim

    def close_settings_panel(self):
        if self.settings_panel.isVisible():
            # Animate slide-out
            from PySide6.QtCore import QPropertyAnimation
            anim = QPropertyAnimation(self.settings_panel, b"pos")
            anim.setDuration(200)
            anim.setStartValue(self.settings_panel.pos())
            anim.setEndValue(self.rect().topRight())
            anim.finished.connect(self.settings_panel.hide)
            anim.finished.connect(self.overlay.hide)
            anim.start()
            self._settings_anim = anim
        else:
            self.overlay.hide()
            self.settings_panel.hide()

    def handle_settings_save(self, auto_download):
        self.auto_download = auto_download
        save_settings(self)
        self.close_settings_panel()
        self.show_status(f"{IconProvider.get('check')} Settings saved", "success")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.overlay:
            self.overlay.setGeometry(self.rect())
        if self.settings_panel:
            self.settings_panel.setFixedHeight(self.height())
            self.settings_panel.move(self.width() - self.settings_panel.width(), 0)

    def on_filename_change(self):
        save_settings(self)
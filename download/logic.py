from PySide6.QtCore import QThread
from PySide6.QtGui import QIcon, QTextCursor
from download_worker import DownloadWorker
from icon_provider import IconProvider

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
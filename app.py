import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from image_downloader_app import ImageDownloaderApp


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = ImageDownloaderApp()
    window.setWindowIcon(QIcon("icons/logo.svg"))
    window.show()
    sys.exit(app.exec())

from PySide6.QtWidgets import QApplication
from image_downloader_app import ImageDownloaderApp


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = ImageDownloaderApp()
    window.show()
    sys.exit(app.exec())

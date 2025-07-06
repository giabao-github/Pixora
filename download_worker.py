import os
import re
import requests
from urllib.parse import urlparse
from PIL import Image
from io import BytesIO
from PySide6.QtCore import QObject, Signal
from icon_provider import IconProvider


class DownloadWorker(QObject):
    progress = Signal(str)
    finished = Signal(bool, str, str)

    def __init__(self, url, folder_path, custom_filename=None):
        super().__init__()
        self.url = url
        self.folder_path = folder_path
        self.custom_filename = custom_filename

    def download(self):
        try:
            self.progress.emit(f"{IconProvider.get('search')} Validating image URL...")
            response = requests.get(self.url, timeout=10, stream=True)

            if not response.ok:
                raise ValueError(
                    f"HTTP {response.status_code}: Unable to access the URL"
                )

            content_type = response.headers.get("Content-Type", "")
            if "image" not in content_type:
                raise ValueError("This URL does not point to a valid image")

            self.progress.emit(f"{IconProvider.get('download')} Downloading image...")
            image = Image.open(BytesIO(response.content))
            ext = image.format.lower() if image.format else "png"

            # Generate filename
            if self.custom_filename:
                # Use custom filename
                filename = self.custom_filename
                if not filename.lower().endswith(
                    (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp")
                ):
                    filename += f".{ext}"
            else:
                # Better filename generation
                parsed = urlparse(self.url)
                original_filename = os.path.basename(parsed.path)
                filename = None
                valid_exts = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp")
                # Only use original filename if it has a valid image extension
                if (
                    original_filename
                    and not original_filename.startswith(".")
                    and original_filename.lower().endswith(valid_exts)
                ):
                    filename = re.sub(r"[^\w\-_\.]", "_", original_filename)
                    filename = re.sub(
                        r"_+", "_", filename
                    )  # Remove multiple underscores
                    filename = filename.strip("_")
                # If still no filename, use default
                if not filename:
                    filename = f"pixora_image.{ext}"

            # Ensure unique filename
            base_name, extension = os.path.splitext(filename)
            counter = 1
            save_path = os.path.join(self.folder_path, filename)
            while os.path.exists(save_path):
                filename = f"{base_name} ({counter}){extension}"
                save_path = os.path.join(self.folder_path, filename)
                counter += 1

            self.progress.emit(f"{IconProvider.get('save')} Saving image...")
            image.save(save_path)

            self.finished.emit(True, save_path, filename)

        except Exception as e:
            self.finished.emit(False, str(e), "")

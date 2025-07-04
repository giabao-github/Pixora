import json
from pathlib import Path

CONFIG_PATH = Path.home() / ".image_downloader_config.json"

def load_settings(self):
    if not CONFIG_PATH.exists():
        return
    try:
        with open(CONFIG_PATH, 'r') as f:
            extracted_from_load_settings(self, f)
    except Exception as e:
        print("Error loading settings:", e)

def extracted_from_load_settings(self, f):
    config = json.load(f)
    self.folder_path = config.get("folder_path", "")
    self.auto_download = config.get("auto_download", False)
    self.custom_filename = config.get("custom_filename", "")
    self.update_folder_label()
    self.filename_input.setText(self.custom_filename)

def save_settings(self):
    config = {
        "folder_path": self.folder_path,
        "auto_download": self.auto_download,
        "custom_filename": self.filename_input.text().strip()
    }
    try:
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config, f)
    except Exception as e:
        print("Error saving settings:", e) 
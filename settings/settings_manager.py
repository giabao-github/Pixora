import json
from pathlib import Path

CONFIG_PATH = Path.home() / ".image_downloader_config.json"

def load_settings(app_instance):
    if not CONFIG_PATH.exists():
        return
    try:
        with open(CONFIG_PATH, 'r') as f:
            apply_loaded_settings(app_instance, f)
    except Exception as e:
        print("Error loading settings:", e)

def apply_loaded_settings(app_instance, f):
    config = json.load(f)
    app_instance.folder_path = config.get("folder_path", "")
    app_instance.auto_download = config.get("auto_download", False)
    app_instance.custom_filename = config.get("custom_filename", "")
    app_instance.update_folder_label()
    app_instance.filename_input.setText(app_instance.custom_filename)

def save_settings(app_instance):
    config = {
        "folder_path": app_instance.folder_path,
        "auto_download": app_instance.auto_download,
        "custom_filename": app_instance.filename_input.text().strip()
    }
    try:
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config, f)
    except Exception as e:
        print("Error saving settings:", e) 
import os


class IconProvider:
    ICONS = {
        "download": "⬇️",
        "folder": "📁",
        "folder_open": "📂",
        "paste": "📋",
        "clear": "🗑️",
        "image": "🖼️",
        "check": "✅",
        "error": "❌",
        "info": "ℹ️",
        "warning": "⚠️",
        "search": "🔍",
        "save": "💾",
        "link": "🔗",
        "settings": "⚙️",
        "history": "📜",
        "auto": "🔄",
        "file": "📄",
    }
    ICON_DIR = os.path.join(os.path.dirname(__file__), "icons")

    @classmethod
    def get(cls, name):
        return cls.ICONS.get(name, "•")

    @classmethod
    def get_path(cls, name, ext="svg"):
        filename = f"{name}.{ext}"
        path = os.path.join(cls.ICON_DIR, filename)
        return path if os.path.exists(path) else None

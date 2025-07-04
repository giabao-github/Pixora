class IconProvider:
    ICONS = {
        'download': '⬇️',
        'folder': '📁',
        'folder_open': '📂',
        'paste': '📋',
        'clear': '🗑️',
        'image': '🖼️',
        'check': '✅',
        'error': '❌',
        'info': 'ℹ️',
        'warning': '⚠️',
        'search': '🔍',
        'save': '💾',
        'link': '🔗',
        'settings': '⚙️',
        'history': '📜',
        'auto': '🔄',
        'file': '📄'
    }
    
    @classmethod
    def get(cls, name):
        return cls.ICONS.get(name, '•')
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGroupBox, QLineEdit, QScrollArea, QTextEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from icon_provider import IconProvider
from utils.ui_helpers import get_button_style

def create_left_panel(main_window):
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
            color: #2C3E50;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
            padding: 10px;
        }
    """)
    header_layout.addWidget(header)
    header_layout.addStretch()
    main_window.settings_btn = QPushButton(f"{IconProvider.get('settings')}")
    main_window.settings_btn.setFixedSize(36, 36)
    main_window.settings_btn.setStyleSheet("""
        QPushButton {
            background-color: #1B2A41;
            color: white;
            border: none;
            border-radius: 6px;
            font-weight: bold;
            padding: 2px 2px;
            font-size: 18px;
        }
        QPushButton:hover {
            background-color: #405066;
        }
        QPushButton:pressed {
            background-color: #66748B;
        }
        QPushButton:disabled {
            background-color: #bdc3c7;
            color: #7f8c8d;
        }
    """)
    main_window.settings_btn.setCursor(QCursor(Qt.PointingHandCursor))
    main_window.settings_btn.clicked.connect(main_window.open_settings_dialog)
    header_layout.addWidget(main_window.settings_btn)
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
    main_window.url_input = QLineEdit()
    main_window.url_input.setPlaceholderText("Paste or enter an image URL here...")
    main_window.url_input.textChanged.connect(main_window.on_url_change)
    main_window.url_input.setStyleSheet("""
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
    url_layout.addWidget(main_window.url_input)
    # URL action buttons
    url_buttons = QHBoxLayout()
    main_window.paste_btn = QPushButton(f"{IconProvider.get('paste')} Paste")
    main_window.paste_btn.clicked.connect(main_window.paste_clipboard)
    main_window.paste_btn.setStyleSheet(get_button_style("#9b59b6"))
    main_window.paste_btn.setCursor(QCursor(Qt.PointingHandCursor))
    main_window.clear_btn = QPushButton(f"{IconProvider.get('clear')} Clear")
    main_window.clear_btn.clicked.connect(main_window.clear_url)
    main_window.clear_btn.setStyleSheet(get_button_style("#e74c3c"))
    main_window.clear_btn.setCursor(QCursor(Qt.PointingHandCursor))
    url_buttons.addWidget(main_window.paste_btn)
    url_buttons.addWidget(main_window.clear_btn)
    url_layout.addLayout(url_buttons)
    url_group.setLayout(url_layout)
    layout.addWidget(url_group)
    # Custom Filename Group
    filename_group = QGroupBox("Custom Filename (Optional)")
    filename_group.setStyleSheet("""
        QGroupBox {
            font-weight: bold;
            color: #2C3E50;
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
    main_window.filename_input = QLineEdit()
    main_window.filename_input.setPlaceholderText("Enter custom filename (optional)...")
    main_window.filename_input.setStyleSheet("""
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
    main_window.filename_input.textChanged.connect(main_window.on_filename_change)
    filename_layout.addWidget(main_window.filename_input)
    # Filename action buttons
    filename_buttons = QHBoxLayout()
    main_window.filename_paste_btn = QPushButton(f"{IconProvider.get('paste')} Paste")
    main_window.filename_paste_btn.clicked.connect(main_window.paste_filename)
    main_window.filename_paste_btn.setStyleSheet(get_button_style("#9b59b6"))
    main_window.filename_paste_btn.setCursor(QCursor(Qt.PointingHandCursor))
    main_window.filename_clear_btn = QPushButton(f"{IconProvider.get('clear')} Clear")
    main_window.filename_clear_btn.clicked.connect(main_window.clear_filename)
    main_window.filename_clear_btn.setStyleSheet(get_button_style("#e74c3c"))
    main_window.filename_clear_btn.setCursor(QCursor(Qt.PointingHandCursor))
    filename_buttons.addWidget(main_window.filename_paste_btn)
    filename_buttons.addWidget(main_window.filename_clear_btn)
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
    main_window.folder_label = QLabel("No folder selected")
    main_window.folder_label.setStyleSheet("""
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
    folder_layout.addWidget(main_window.folder_label)
    folder_buttons = QHBoxLayout()
    main_window.folder_btn = QPushButton(f"{IconProvider.get('folder_open')} Choose Folder")
    main_window.folder_btn.clicked.connect(main_window.choose_folder)
    main_window.folder_btn.setStyleSheet(get_button_style("#27ae60"))
    main_window.folder_btn.setCursor(QCursor(Qt.PointingHandCursor))
    main_window.open_btn = QPushButton(f"{IconProvider.get('folder')} Open Folder")
    main_window.open_btn.clicked.connect(main_window.open_folder)
    main_window.open_btn.setEnabled(False)
    main_window.open_btn.setStyleSheet(get_button_style("#34495e"))
    main_window.open_btn.setCursor(QCursor(Qt.PointingHandCursor))
    folder_buttons.addWidget(main_window.folder_btn)
    folder_buttons.addWidget(main_window.open_btn)
    folder_layout.addLayout(folder_buttons)
    folder_group.setLayout(folder_layout)
    layout.addWidget(folder_group)
    # Download button
    main_window.download_btn = QPushButton(f"{IconProvider.get('download')} Download Image")
    main_window.download_btn.clicked.connect(main_window.download_image)
    main_window.download_btn.setStyleSheet(get_button_style("\t#FF69B4", large=True))
    main_window.download_btn.setCursor(QCursor(Qt.PointingHandCursor))
    layout.addWidget(main_window.download_btn)
    layout.addStretch()
    content_widget = QWidget()
    content_widget.setLayout(layout)
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setWidget(content_widget)
    return scroll

def create_right_panel(main_window):
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
    main_window.status_label = QLabel("Ready to download images")
    main_window.status_label.setStyleSheet("""
        QLabel {
            color: #7f8c8d;
            font-size: 14px;
            padding: 12px;
            background: #ecf0f1;
            border-radius: 6px;
            border-left: 4px solid #3498db;
        }
    """)
    main_window.status_label.setWordWrap(True)
    status_layout.addWidget(main_window.status_label)
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
    main_window.history_text = QTextEdit()
    main_window.history_text.setReadOnly(True)
    main_window.history_text.setMaximumHeight(200)
    main_window.history_text.setStyleSheet("""
        QTextEdit {
            background: #f8f9fa;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            padding: 8px;
            font-size: 12px;
            color: #2c3e50;
        }
    """)
    main_window.history_text.setPlainText("No downloads yet...")
    history_layout.addWidget(main_window.history_text)
    clear_history_btn = QPushButton(f"{IconProvider.get('clear')} Clear History")
    clear_history_btn.clicked.connect(main_window.clear_history)
    clear_history_btn.setStyleSheet(get_button_style("#e74c3c", small=True))
    clear_history_btn.setCursor(QCursor(Qt.PointingHandCursor))
    history_layout.addWidget(clear_history_btn)
    history_group.setLayout(history_layout)
    layout.addWidget(history_group)
    layout.addStretch()
    widget.setLayout(layout)
    return widget 
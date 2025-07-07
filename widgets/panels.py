from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGroupBox,
    QLineEdit,
    QScrollArea,
    QTextEdit,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor, QIcon
from PySide6.QtCore import QSize
from icon_provider import IconProvider
from utils.ui_helpers import get_button_style


def create_left_panel(main_window):
    widget = QWidget()
    widget.setStyleSheet(
        """
        QWidget {
            background-color: white;
            border-radius: 8px;
        }
    """
    )
    layout = QVBoxLayout()
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setSpacing(20)
    layout.addLayout(create_header_section(main_window))
    layout.addWidget(create_url_input_group(main_window))
    layout.addWidget(create_filename_input_group(main_window))
    layout.addWidget(create_folder_group(main_window))
    layout.addWidget(create_download_button(main_window))
    layout.addStretch()
    content_widget = QWidget()
    content_widget.setLayout(layout)
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setWidget(content_widget)
    return scroll


def create_header_section(main_window):
    layout = QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)

    # Settings icon row (left-aligned)
    settings_row = QHBoxLayout()
    settings_row.setContentsMargins(0, 0, 0, 0)
    settings_row.setSpacing(0)
    settings_icon_path = IconProvider.get_path("settings")
    main_window.settings_btn = QPushButton()
    if settings_icon_path:
        main_window.settings_btn.setIcon(QIcon(settings_icon_path))
        main_window.settings_btn.setIconSize(QSize(30, 30))
    main_window.settings_btn.setFixedSize(30, 30)
    main_window.settings_btn.setStyleSheet(
        """
        QPushButton {
            background-color: transparent;
            border: none;
            border-radius: 50%;
            padding: 0;
            min-width: 30px;
            min-height: 30px;
            max-width: 30px;
            max-height: 30px;
        }
        QPushButton::icon {
            margin: 0 auto;
        }
        """
    )
    main_window.settings_btn.setCursor(QCursor(Qt.PointingHandCursor))
    main_window.settings_btn.clicked.connect(main_window.open_settings_dialog)
    settings_row.addWidget(main_window.settings_btn, alignment=Qt.AlignLeft)
    settings_row.addStretch()

    # Title row (centered)
    title_label = QLabel("Pixora - Smart Image Downloader")
    title_label.setStyleSheet(
        "QLabel { color: #2C3E50; font-size: 24px; font-weight: bold; padding: 0 0 4px 0; margin: 0; }"
    )
    title_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

    # Add both to the main layout
    layout.addLayout(settings_row)
    layout.addWidget(title_label, alignment=Qt.AlignHCenter)

    # Add spacing below the title
    layout.addSpacing(24)  # Adjust value as needed for visual comfort

    return layout


def create_url_input_group(main_window):
    url_group = QGroupBox(f"{IconProvider.get('link')} Image URL")
    url_group.setStyleSheet(
        """
        QGroupBox {
            font-weight: bold;
            color: #2C3E50;
            border: 2px solid #E0E0E0;
            border-radius: 8px;
            margin-top: 10px;
            padding-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 8px 0 8px;
            margin-top: 2px;
        }
    """
    )
    url_layout = QVBoxLayout()
    main_window.url_input = QLineEdit()
    main_window.url_input.setPlaceholderText("Paste or enter an image URL here...")
    main_window.url_input.textChanged.connect(main_window.on_url_change)
    main_window.url_input.setStyleSheet(
        """
        QLineEdit {
            padding: 12px;
            border: 2px solid #E0E0E0;
            border-radius: 6px;
            font-size: 14px;
            background: white;
            color: #2C3E50;
        }
        QLineEdit:focus {
            border-color: #3498DB;
        }
    """
    )
    url_layout.addWidget(main_window.url_input)
    url_buttons = QHBoxLayout()
    icon_path = IconProvider.get_path("paste")
    main_window.paste_btn = QPushButton(" Paste")
    if icon_path:
        main_window.paste_btn.setIcon(QIcon(icon_path))
        main_window.paste_btn.setIconSize(QSize(16, 16))
    main_window.paste_btn.clicked.connect(main_window.paste_clipboard)
    main_window.paste_btn.setStyleSheet(get_button_style("#9B59B6"))
    main_window.paste_btn.setCursor(QCursor(Qt.PointingHandCursor))
    icon_path = IconProvider.get_path("delete")
    main_window.clear_btn = QPushButton(" Clear")
    if icon_path:
        main_window.clear_btn.setIcon(QIcon(icon_path))
        main_window.clear_btn.setIconSize(QSize(18, 18))
    main_window.clear_btn.clicked.connect(main_window.clear_url)
    main_window.clear_btn.setStyleSheet(get_button_style("#E74C3C"))
    main_window.clear_btn.setCursor(QCursor(Qt.PointingHandCursor))
    url_buttons.addWidget(main_window.paste_btn)
    url_buttons.addWidget(main_window.clear_btn)
    url_layout.addLayout(url_buttons)
    url_group.setLayout(url_layout)
    return url_group


def create_filename_input_group(main_window):
    filename_group = QGroupBox(
        f"{IconProvider.get('filename')} Custom Filename (Optional)"
    )
    filename_group.setStyleSheet(
        """
        QGroupBox {
            font-weight: bold;
            color: #2C3E50;
            border: 2px solid #E0E0E0;
            border-radius: 8px;
            margin-top: 10px;
            padding-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 8px 0 8px;
            margin-top: 2px;
        }
    """
    )
    filename_layout = QVBoxLayout()
    main_window.filename_input = QLineEdit()
    main_window.filename_input.setPlaceholderText("Enter custom filename (optional)...")
    main_window.filename_input.setStyleSheet(
        """
        QLineEdit {
            padding: 12px;
            border: 2px solid #E0E0E0;
            border-radius: 6px;
            font-size: 14px;
            background: white;
            color: #2C3E50;
        }
        QLineEdit:focus {
            border-color: #3498DB;
        }
    """
    )
    main_window.filename_input.textChanged.connect(main_window.on_filename_change)
    filename_layout.addWidget(main_window.filename_input)
    filename_buttons = QHBoxLayout()
    icon_path = IconProvider.get_path("paste")
    main_window.filename_paste_btn = QPushButton(" Paste")
    if icon_path:
        main_window.filename_paste_btn.setIcon(QIcon(icon_path))
        main_window.filename_paste_btn.setIconSize(QSize(16, 16))
    main_window.filename_paste_btn.clicked.connect(main_window.paste_filename)
    main_window.filename_paste_btn.setStyleSheet(get_button_style("#9B59B6"))
    main_window.filename_paste_btn.setCursor(QCursor(Qt.PointingHandCursor))
    icon_path = IconProvider.get_path("delete")
    main_window.filename_clear_btn = QPushButton(" Clear")
    if icon_path:
        main_window.filename_clear_btn.setIcon(QIcon(icon_path))
        main_window.filename_clear_btn.setIconSize(QSize(18, 18))
    main_window.filename_clear_btn.clicked.connect(main_window.clear_filename)
    main_window.filename_clear_btn.setStyleSheet(get_button_style("#E74C3C"))
    main_window.filename_clear_btn.setCursor(QCursor(Qt.PointingHandCursor))
    filename_buttons.addWidget(main_window.filename_paste_btn)
    filename_buttons.addWidget(main_window.filename_clear_btn)
    filename_layout.addLayout(filename_buttons)
    filename_group.setLayout(filename_layout)
    return filename_group


def create_folder_group(main_window):
    folder_group = QGroupBox(f"{IconProvider.get('folder')} Download Location")
    folder_group.setStyleSheet(
        """
        QGroupBox {
            font-weight: bold;
            color: #2C3E50;
            border: 2px solid #E0E0E0;
            border-radius: 8px;
            margin-top: 10px;
            padding-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 8px 0 8px;
            margin-top: 2px;
        }
    """
    )
    folder_layout = QVBoxLayout()
    main_window.folder_label = QLabel("No folder selected")
    main_window.folder_label.setStyleSheet(
        """
        QLabel {
            color: #7F8C8D;
            font-size: 13px;
            font-weight: 600;
            background: #ECF0F1;
            padding: 10px;
            border-radius: 6px;
            border: 1px solid #BDC3C7;
        }
    """
    )
    folder_layout.addWidget(main_window.folder_label)
    folder_buttons = QHBoxLayout()
    main_window.folder_btn = QPushButton(
        f"{IconProvider.get('folder_open')} Choose Folder"
    )
    main_window.folder_btn.clicked.connect(main_window.choose_folder)
    main_window.folder_btn.setStyleSheet(get_button_style("#27AE60"))
    main_window.folder_btn.setCursor(QCursor(Qt.PointingHandCursor))
    main_window.open_btn = QPushButton(f"{IconProvider.get('folder_open')} Open Folder")
    main_window.open_btn.clicked.connect(main_window.open_folder)
    main_window.open_btn.setEnabled(False)
    main_window.open_btn.setStyleSheet(get_button_style("#34495E"))
    main_window.open_btn.setCursor(QCursor(Qt.PointingHandCursor))
    folder_buttons.addWidget(main_window.folder_btn)
    folder_buttons.addWidget(main_window.open_btn)
    folder_layout.addLayout(folder_buttons)
    folder_group.setLayout(folder_layout)
    return folder_group


def create_download_button(main_window):
    icon_path = IconProvider.get_path("download")
    download_btn = QPushButton(" Download Image")
    if icon_path:
        download_btn.setIcon(QIcon(icon_path))
        download_btn.setIconSize(QSize(24, 24))
    download_btn.clicked.connect(main_window.download_image)
    download_btn.setStyleSheet(get_button_style("#FF69B4", large=True))
    download_btn.setCursor(QCursor(Qt.PointingHandCursor))
    main_window.download_btn = download_btn
    return download_btn


def create_right_panel(main_window):
    widget = QWidget()
    widget.setStyleSheet(
        """
        QWidget {
            background-color: white;
            border-radius: 8px;
        }
    """
    )
    layout = QVBoxLayout()
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setSpacing(15)
    # Status Group
    status_group = QGroupBox(f"{IconProvider.get('check')} Status")
    status_group.setStyleSheet(
        """
        QGroupBox {
            font-weight: bold;
            color: #2C3E50;
            border: 2px solid #E0E0E0;
            border-radius: 8px;
            margin-top: 10px;
            padding-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 8px 0 8px;
            margin-top: 2px;
        }
    """
    )
    status_layout = QVBoxLayout()
    main_window.status_label = QLabel("Ready to download images")
    main_window.status_label.setStyleSheet(
        """
        QLabel {
            color: #7F8C8D;
            font-size: 14px;
            padding: 12px;
            background: #ECF0F1;
            border-radius: 6px;
            border-left: 4px solid #3498DB;
        }
    """
    )
    main_window.status_label.setWordWrap(True)
    status_layout.addWidget(main_window.status_label)
    status_group.setLayout(status_layout)
    layout.addWidget(status_group)
    # Download History Group
    history_group = QGroupBox(f"{IconProvider.get('save')} Download History")
    history_group.setStyleSheet(
        """
        QGroupBox {
            font-weight: bold;
            color: #2C3E50;
            border: 2px solid #E0E0E0;
            border-radius: 8px;
            margin-top: 10px;
            padding-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
    """
    )
    history_layout = QVBoxLayout()
    main_window.history_text = QTextEdit()
    main_window.history_text.setReadOnly(True)
    main_window.history_text.setMaximumHeight(200)
    main_window.history_text.setStyleSheet(
        """
        QTextEdit {
            background: #F8F9FA;
            border: 1px solid #E0E0E0;
            border-radius: 6px;
            padding: 8px;
            font-size: 12px;
            color: #2C3E50;
        }
    """
    )
    main_window.history_text.setPlainText("No downloads yet...")
    history_layout.addWidget(main_window.history_text)
    icon_path = IconProvider.get_path("delete")
    clear_history_btn = QPushButton(" Clear History")
    if icon_path:
        clear_history_btn.setIcon(QIcon(icon_path))
        clear_history_btn.setIconSize(QSize(18, 18))
    clear_history_btn.clicked.connect(main_window.clear_history)
    clear_history_btn.setStyleSheet(
        get_button_style("#E74C3C", small=True)
        + "QPushButton { padding-top: 10px; padding-bottom: 10px; }"
    )
    clear_history_btn.setCursor(QCursor(Qt.PointingHandCursor))
    history_layout.addWidget(clear_history_btn)
    history_group.setLayout(history_layout)
    layout.addWidget(history_group)
    layout.addStretch()
    widget.setLayout(layout)
    return widget

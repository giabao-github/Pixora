def darken_color(color):
    color_map = {
        "#3498DB": "#2980B9",
        "#2980B9": "#1F618D",
        "#E74C3C": "#C0392B",
        "#C0392B": "#A93226",
        "#27AE60": "#229954",
        "#229954": "#1E8449",
        "#9B59B6": "#8E44AD",
        "#8E44AD": "#7D3C98",
        "#34495E": "#2C3E50",
        "#2C3E50": "#1B2631"
    }
    return color_map.get(color, "#2C3E50")

def get_button_style(color, large = False, small = False):
    size = "padding: 15px 20px; font-size: 14px;" if large else "padding: 8px 16px; font-size: 13px;" if small else "padding: 10px 16px; font-size: 13px;"
    # Special hover and pressed color for download button
    if color.strip() == "#FF69B4":
        hover_color = "#C94F8C"
        pressed_color = "#A13B6C"
    else:
        hover_color = darken_color(color)
        pressed_color = darken_color(hover_color)
    return f"""
        QPushButton {{
            background-color: {color};
            color: white;
            border: none;
            border-radius: 6px;
            font-weight: bold;
            {size}
        }}
        QPushButton:hover {{
            background-color: {hover_color};
        }}
        QPushButton:pressed {{
            background-color: {pressed_color};
        }}
        QPushButton:disabled {{
            background-color: #BDC3C7;
            color: #7F8C8D;
        }}
    """

def show_status(status_label, status_anim, status_opacity, message, status_type = "info"):
    colors = {
        "info": ("#3498DB", "#E3F2FD"),
        "success": ("#27AE60", "#E8F5E8"),
        "error": ("#E74C3C", "#FFEEAA"),
        "warning": ("#F39C12", "#FFF3E0")
    }
    color, bg_color = colors.get(status_type, colors["info"])
    status_label.setText(message)
    status_label.setStyleSheet(f"""
        QLabel {{
            color: {color};
            font-size: 14px;
            padding: 12px;
            background: {bg_color};
            border-radius: 6px;
            border-left: 4px solid {color};
            font-weight: 600;
        }}
    """)
    # --- Animate status label opacity ---
    status_anim.stop()
    status_opacity.setOpacity(0.0)
    status_anim.setStartValue(0.0)
    status_anim.setEndValue(1.0)
    status_anim.start()
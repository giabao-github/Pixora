def darken_color(color):
    color_map = {
        "#3498db": "#2980b9",
        "#2980b9": "#1f618d",
        "#e74c3c": "#c0392b",
        "#c0392b": "#a93226",
        "#27ae60": "#229954",
        "#229954": "#1e8449",
        "#9b59b6": "#8e44ad",
        "#8e44ad": "#7d3c98",
        "#34495e": "#2c3e50",
        "#2c3e50": "#1b2631"
    }
    return color_map.get(color, "#2c3e50")

def get_button_style(color, large=False, small=False):
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
            background-color: #bdc3c7;
            color: #7f8c8d;
        }}
    """

def show_status(self, message, status_type="info"):
    colors = {
        "info": ("#3498db", "#e3f2fd"),
        "success": ("#27ae60", "#e8f5e8"),
        "error": ("#e74c3c", "#ffeaea"),
        "warning": ("#f39c12", "#fff3e0")
    }
    color, bg_color = colors.get(status_type, colors["info"])
    self.status_label.setText(message)
    self.status_label.setStyleSheet(f"""
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
    self.status_anim.stop()
    self.status_opacity.setOpacity(0.0)
    self.status_anim.setStartValue(0.0)
    self.status_anim.setEndValue(1.0)
    self.status_anim.start() 
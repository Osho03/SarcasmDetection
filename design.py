from PyQt5.QtGui import QFont

APP_FONT_FAMILY = 'Segoe UI'
APP_FONT_SIZE = 10

ACCENT = '#22d3ee'
ACCENT_BRIGHT = '#67e8f9'
NEON = 'rgba(34, 211, 238, 0.55)'

PRIMARY_GRADIENT = 'qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0891b2, stop:1 #22d3ee)'
PRIMARY_GRADIENT_HOVER = 'qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #06b6d4, stop:1 #67e8f9)'
PRIMARY_GRADIENT_PRESSED = 'qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0e7490, stop:1 #06b6d4)'

TEXT = '#e6edf7'
TEXT_MUTED = '#94a3b8'
TEXT_FAINT = '#5b6b82'
BG_SOFT = '#0a1122'

APP_QSS = """
#MainGUI {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #04060c,
        stop:0.5 #0a1122,
        stop:1 #0b1622);
}

QWidget {
    font-family: "Segoe UI";
    color: #cbd5e1;
}

QLabel {
    background: transparent;
    color: #cbd5e1;
}

QToolTip {
    background-color: #0a1122;
    color: #67e8f9;
    border: 1px solid rgba(34, 211, 238, 0.5);
    border-radius: 6px;
    padding: 6px;
}

QGroupBox {
    background-color: rgba(10, 17, 34, 0.55);
    border: 1px solid rgba(148, 163, 184, 0.18);
    border-top-color: rgba(34, 211, 238, 0.45);
    border-radius: 14px;
    margin-top: 14px;
    padding: 10px 12px 12px 12px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 14px;
    top: 2px;
    padding: 0 8px;
    color: #67e8f9;
    font-family: "Cascadia Code", "JetBrains Mono", "Consolas";
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
}

QPushButton {
    background-color: rgba(15, 26, 48, 0.72);
    border: 1px solid rgba(34, 211, 238, 0.35);
    border-radius: 10px;
    padding: 9px 16px;
    color: #cbd5e1;
    font-weight: 600;
    min-height: 22px;
}

QPushButton:hover {
    background-color: rgba(34, 211, 238, 0.14);
    border: 1px solid rgba(34, 211, 238, 0.75);
    color: #ffffff;
}

QPushButton:pressed {
    background-color: rgba(34, 211, 238, 0.06);
    border: 1px solid rgba(34, 211, 238, 0.9);
}

QPushButton:focus {
    border: 1px solid #22d3ee;
}

QPushButton:disabled {
    background-color: rgba(15, 26, 48, 0.4);
    color: #475569;
    border: 1px solid rgba(71, 85, 105, 0.35);
}

#primaryBtn {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #0891b2, stop:1 #22d3ee);
    border: 1px solid rgba(103, 232, 249, 0.8);
    color: #04141c;
    font-weight: 800;
    letter-spacing: 1px;
}

#primaryBtn:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #06b6d4, stop:1 #67e8f9);
    border: 1px solid #a5f3fc;
    color: #04141c;
}

#primaryBtn:pressed {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #0e7490, stop:1 #06b6d4);
}

#primaryBtn:disabled {
    background: rgba(15, 26, 48, 0.4);
    border: 1px solid rgba(71, 85, 105, 0.35);
    color: #475569;
}

QLineEdit {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 rgba(8, 14, 30, 0.92),
        stop:1 rgba(12, 24, 42, 0.92));
    border: 1.5px solid rgba(34, 211, 238, 0.45);
    border-radius: 12px;
    padding: 8px 12px;
    min-height: 30px;
    color: #ffffff;
    font-size: 12pt;
    font-weight: 500;
    selection-background-color: #22d3ee;
    selection-color: #04141c;
}

QLineEdit:hover {
    border: 1.5px solid rgba(34, 211, 238, 0.75);
}

QLineEdit:focus {
    border: 1.5px solid #22d3ee;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 rgba(10, 20, 40, 0.95),
        stop:1 rgba(14, 32, 54, 0.95));
}

#resultChip {
    background-color: rgba(8, 14, 30, 0.75);
    border: 1px solid rgba(34, 211, 238, 0.35);
    border-radius: 12px;
    padding: 8px 12px;
    min-height: 30px;
    font-size: 15px;
    font-weight: 600;
    color: #cbd5e1;
}

#resultChip:hover {
    border: 1px solid rgba(34, 211, 238, 0.70);
}

QPlainTextEdit {
    background-color: rgba(2, 6, 14, 0.92);
    border: 1px solid rgba(34, 211, 238, 0.22);
    border-radius: 10px;
    padding: 12px;
    color: #9febf5;
    font-family: "Cascadia Code", "JetBrains Mono", "Consolas";
    font-size: 10pt;
    selection-background-color: rgba(34, 211, 238, 0.6);
    selection-color: #04141c;
}

QScrollArea {
    background: transparent;
    border: none;
}

QScrollArea > QWidget > QWidget {
    background: transparent;
}

QTableView {
    background-color: rgba(4, 8, 18, 0.85);
    alternate-background-color: rgba(34, 211, 238, 0.03);
    border: 1px solid rgba(34, 211, 238, 0.25);
    border-radius: 10px;
    color: #cbd5e1;
    gridline-color: rgba(148, 163, 184, 0.08);
    selection-background-color: rgba(34, 211, 238, 0.25);
    selection-color: #ffffff;
}

QTableView::item {
    padding: 4px 8px;
}

QHeaderView::section {
    background-color: rgba(8, 14, 30, 0.95);
    color: #67e8f9;
    border: none;
    border-bottom: 1px solid rgba(34, 211, 238, 0.35);
    padding: 6px 8px;
    font-family: "Cascadia Code", "JetBrains Mono", "Consolas";
    font-size: 10pt;
    font-weight: 700;
}

QTableCornerButton::section {
    background-color: rgba(8, 14, 30, 0.95);
    border: none;
}

QScrollBar:vertical {
    background: transparent;
    width: 10px;
    margin: 4px;
}

QScrollBar::handle:vertical {
    background: rgba(34, 211, 238, 0.30);
    border-radius: 5px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background: rgba(34, 211, 238, 0.60);
}

QScrollBar:horizontal {
    background: transparent;
    height: 10px;
    margin: 4px;
}

QScrollBar::handle:horizontal {
    background: rgba(34, 211, 238, 0.30);
    border-radius: 5px;
    min-width: 30px;
}

QScrollBar::handle:horizontal:hover {
    background: rgba(34, 211, 238, 0.60);
}

QScrollBar::add-line, QScrollBar::sub-line {
    width: 0;
    height: 0;
    background: none;
    border: none;
}

QScrollBar::add-page, QScrollBar::sub-page {
    background: transparent;
}
"""


def apply_design(app):
    app.setFont(QFont(APP_FONT_FAMILY, APP_FONT_SIZE))
    app.setStyleSheet(APP_QSS)


def style_placeholder(widget, color):
    from PyQt5.QtGui import QColor, QPalette
    palette = widget.palette()
    palette.setColor(QPalette.PlaceholderText, QColor(color))
    widget.setPalette(palette)


def add_glow(widget, color=ACCENT, blur=26, alpha=170):
    from PyQt5.QtGui import QColor
    from PyQt5.QtWidgets import QGraphicsDropShadowEffect
    glow_color = QColor(color)
    glow_color.setAlpha(alpha)
    effect = QGraphicsDropShadowEffect(widget)
    effect.setOffset(0, 0)
    effect.setBlurRadius(blur)
    effect.setColor(glow_color)
    widget.setGraphicsEffect(effect)
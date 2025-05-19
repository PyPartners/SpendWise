
DARK_THEME_QSS = """
/* Global settings */
QWidget {
    color: #e0e0e0;
    font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    font-size: 9pt;
}
QMainWindow, QDialog {
    background-color: #262626; 
}
QPushButton {
    background-color: #373737; 
    color: #e0e0e0;
    border: 1px solid #4a4a4a; 
    padding: 7px 15px;
    border-radius: 4px;
    min-height: 22px;
    outline: none;
}
QPushButton:hover {
    background-color: #4a4a4a; 
    border-color: #5c5c5c;
}
QPushButton:pressed {
    background-color: #525252; 
}
QPushButton:disabled {
    background-color: #303030;
    color: #6a6a6a;
    border-color: #404040;
}
QPushButton#PrimaryButton, QPushButton#FilterButton {
    background-color: #5cb3bf; 
    color: #1e1e1e; 
    border: none;
    font-weight: bold;
}
QPushButton#PrimaryButton:hover, QPushButton#FilterButton:hover {
    background-color: #69c0d1; 
}
QPushButton#PrimaryButton:pressed, QPushButton#FilterButton:pressed {
    background-color: #50a0ad; 
}
QLineEdit, QDateEdit, QComboBox, QDoubleSpinBox {
    background-color: #2e2e2e; 
    border: 1px solid #4a4a4a; 
    color: #e0e0e0;
    padding: 7px;
    border-radius: 4px;
    selection-background-color: #5cb3bf; 
    selection-color: #1e1e1e; 
}
QLineEdit:focus, QDateEdit:focus, QComboBox:focus, QDoubleSpinBox:focus {
    border: 1px solid #5cb3bf; 
}
QComboBox::drop-down {
    border-left: 1px solid #4a4a4a;
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 22px;
    border-top-right-radius: 3px;
    border-bottom-right-radius: 3px;
}
QComboBox::down-arrow {
    image: url(:/qt-project.org/styles/commonstyle/images/arrow-down-inverted-16.png); 
    width: 12px;
    height: 12px;
}
 QDateEdit::up-button, QDateEdit::down-button {
     width: 22px;
     border-left: 1px solid #4a4a4a;
}
QSpinBox::up-button, QSpinBox::down-button,
QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
    border-left: 1px solid #4a4a4a;
    width: 22px;
}
QTableView {
    background-color: #2e2e2e;
    border: 1px solid #3c3c3c; 
    gridline-color: #3c3c3c;
    alternate-background-color: #333333; 
    selection-background-color: #428591; 
    selection-color: #e0e0e0; 
    border-radius: 4px;
    font-size: 9pt;
}
QHeaderView::section {
    background-color: #373737; 
    border: none;
    border-bottom: 1px solid #4a4a4a;
    padding: 8px;
    font-weight: 600;
    color: #e0e0e0;
}
 QHeaderView {
    border-top-left-radius: 3px;
    border-top-right-radius: 3px;
}
QLabel {
    color: #e0e0e0;
    background-color: transparent;
}
QLabel#DialogTitleLabel {
    font-size: 14pt;
    font-weight: 600;
    color: #5cb3bf; 
    padding-bottom: 10px;
}
QLabel#AboutAppNameLabel {
     color: #f0f0f0; 
}
QGroupBox {
    font-weight: 600;
    color: #e0e0e0;
    border: 1px solid #4a4a4a;
    border-radius: 6px;
    margin-top: 12px;
    padding: 20px 10px 10px 10px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0px 8px;
    left: 12px;
    background-color: #262626; 
    color: #5cb3bf; 
    font-size: 10pt;
}
QToolBar {
    background-color: #212121; 
    border-bottom: 1px solid #333333;
    padding: 3px;
    spacing: 3px;
}
QToolButton {
    padding: 5px;
    border-radius: 4px;
    color: #e0e0e0;
    background-color: transparent;
    border: 1px solid transparent;
}
QToolButton:hover {
    background-color: #373737;
    border: 1px solid #4a4a4a;
}
QToolButton:pressed {
    background-color: #424242;
}
QToolButton:checked {
    background-color: #428591; 
    border: 1px solid #50a0ad; 
}
QMenuBar {
    background-color: #212121;
    color: #e0e0e0;
    border-bottom: 1px solid #333333;
}
QMenuBar::item {
    padding: 6px 12px;
    color: #e0e0e0;
}
QMenuBar::item:selected {
    background-color: #373737;
}
QMenu {
    background-color: #2e2e2e;
    border: 1px solid #4a4a4a;
    color: #e0e0e0;
    border-radius: 4px;
    padding: 4px;
}
QMenu::item {
     padding: 7px 22px;
     border-radius: 3px;
}
QMenu::item:selected {
    background-color: #5cb3bf; 
    color: #1e1e1e; 
}
QMenu::separator {
    height: 1px;
    background: #4a4a4a;
    margin: 4px 0px;
}
QScrollBar:vertical, QScrollBar:horizontal {
    border: none;
    background: #262626; 
    width: 12px;
    margin: 0px;
}
QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
    background: #525252; 
    min-height: 25px;
    min-width: 25px;
    border-radius: 6px;
}
QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover {
    background: #616161;
}
QScrollBar::add-line, QScrollBar::sub-line {
    height: 0px; width: 0px;
    border: none; background: none;
}
QScrollBar::add-page, QScrollBar::sub-page {
    background: none;
}
QStatusBar {
    background-color: #303030;
    color: #e0e0e0;
    border-top: 1px solid #424242;
}
QSplitter::handle {
    background-color: #3c3c3c; 
    height: 3px; 
    width: 3px;
}
QSplitter::handle:hover {
    background-color: #4a4a4a;
}
QLabel#Link { color: #82c7ff; } 
QLabel#Link:hover { color: #a9d9ff; }
"""

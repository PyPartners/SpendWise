
LIGHT_THEME_QSS = """
/* Global settings */
QWidget {
    color: #212121;
    font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    font-size: 9pt; 
}
QMainWindow, QDialog {
    background-color: #f5f5f5;
}
QPushButton {
    background-color: #e0e0e0; 
    color: #212121;
    border: 1px solid #bdbdbd; 
    padding: 7px 15px; 
    border-radius: 4px;
    min-height: 22px; 
    outline: none; 
}
QPushButton:hover {
    background-color: #d5d5d5; 
    border-color: #ababab;
}
QPushButton:pressed {
    background-color: #bdbdbd; 
}
QPushButton:disabled {
    background-color: #f0f0f0;
    color: #ababab;
}
QPushButton#PrimaryButton, QPushButton#FilterButton { 
    background-color: #4d99a6; 
    color: white;
    border: none;
    font-weight: bold;
}
QPushButton#PrimaryButton:hover, QPushButton#FilterButton:hover {
    background-color: #428591; 
}
QPushButton#PrimaryButton:pressed, QPushButton#FilterButton:pressed {
    background-color: #37707a; 
}
QLineEdit, QDateEdit, QComboBox, QDoubleSpinBox {
    background-color: #ffffff;
    border: 1px solid #bdbdbd; 
    padding: 7px; 
    border-radius: 4px;
    selection-background-color: #4d99a6; 
    selection-color: #ffffff;
}
QLineEdit:focus, QDateEdit:focus, QComboBox:focus, QDoubleSpinBox:focus {
    border: 1px solid #4d99a6; 
}
QComboBox::drop-down {
    border-left: 1px solid #bdbdbd;
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 22px;
    border-top-right-radius: 3px; 
    border-bottom-right-radius: 3px;
}
QComboBox::down-arrow {
    image: url(:/qt-project.org/styles/commonstyle/images/arrow-down-16.png); 
    width: 12px;
    height: 12px;
}
QDateEdit::up-button, QDateEdit::down-button {
     width: 22px;
     border-left: 1px solid #bdbdbd;
}
QSpinBox::up-button, QSpinBox::down-button,
QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
    border-left: 1px solid #bdbdbd;
    width: 22px;
}
QTableView {
    background-color: #ffffff;
    border: 1px solid #e0e0e0; 
    gridline-color: #e0e0e0;
    alternate-background-color: #f9f9f9; 
    selection-background-color: #b3dde3; 
    selection-color: #2a5259; 
    border-radius: 4px;
    font-size: 9pt;
}
QHeaderView::section {
    background-color: #eeeeee; 
    border: none; 
    border-bottom: 1px solid #e0e0e0; 
    padding: 8px; 
    font-weight: 600; 
    color: #333333;
}
QHeaderView { 
    border-top-left-radius: 3px; 
    border-top-right-radius: 3px;
}
QLabel {
    color: #212121;
    background-color: transparent; 
}
QLabel#DialogTitleLabel { 
    font-size: 14pt; 
    font-weight: 600;
    color: #4d99a6; 
    padding-bottom: 10px;
}
QLabel#AboutAppNameLabel {
     color: #333; 
}
QGroupBox {
    font-weight: 600;
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    margin-top: 12px; 
    padding: 20px 10px 10px 10px; 
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0px 8px; 
    left: 12px; 
    background-color: #f5f5f5; 
    color: #4d99a6; 
    font-size: 10pt;
}
QToolBar {
    background-color: #f0f0f0;
    border-bottom: 1px solid #dcdcdc;
    padding: 3px;
    spacing: 3px; 
}
QToolButton { 
    padding: 5px;
    border-radius: 4px;
    background-color: transparent;
    border: 1px solid transparent; 
}
QToolButton:hover {
    background-color: #e0e0e0;
    border: 1px solid #c0c0c0;
}
QToolButton:pressed {
    background-color: #d0d0d0;
}
QToolButton:checked { 
    background-color: #b3dde3; 
    border: 1px solid #9fcfd8; 
}
QMenuBar {
    background-color: #f0f0f0;
    border-bottom: 1px solid #dcdcdc; 
}
QMenuBar::item {
    padding: 6px 12px;
}
QMenuBar::item:selected {
    background-color: #e0e0e0;
}
QMenu {
    background-color: #ffffff;
    border: 1px solid #c0c0c0; 
    border-radius: 4px; 
    padding: 4px; 
}
QMenu::item {
    padding: 7px 22px; 
    border-radius: 3px; 
}
QMenu::item:selected {
    background-color: #4d99a6; 
    color: #ffffff;
}
QMenu::separator {
    height: 1px;
    background: #e0e0e0;
    margin: 4px 0px; 
}
QScrollBar:vertical, QScrollBar:horizontal {
    border: none;
    background: #f0f0f0; 
    width: 12px; 
    margin: 0px;
}
QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
    background: #bdbdbd; 
    min-height: 25px; 
    min-width: 25px;
    border-radius: 6px; 
}
QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover {
    background: #adadad;
}
QScrollBar::add-line, QScrollBar::sub-line {
    height: 0px; width: 0px; 
    border: none; background: none;
}
QScrollBar::add-page, QScrollBar::sub-page {
    background: none;
}
QStatusBar {
    background-color: #e0e0e0;
    border-top: 1px solid #d0d0d0;
}
QSplitter::handle {
    background-color: #dcdcdc; 
    height: 3px; 
    width: 3px; 
}
QSplitter::handle:hover {
    background-color: #c0c0c0;
}
QLabel#Link { color: #007bff; } 
QLabel#Link:hover { color: #0056b3; }
"""

import time
import sys
import os
import base64
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QSettings, Qt, QTimer, pyqtSignal, QObject
from PyQt5.QtGui import QFont, QPixmap, QIcon, QPainter

# --- Path setup ---
_script_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_script_dir)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)
# --- End Path setup ---

from spendwise.main_window import MainWindow
from spendwise.core.data_manager import DataManager
from spendwise.utils.translator import Translator
from spendwise.utils.theme_manager import ThemeManager
from spendwise.widgets.splash_screen import SplashScreen
from resources.i18n.translations import TRANSLATIONS
from resources.styles import light_theme, dark_theme
from resources import images



class SpendWiseApp(QApplication):
    currency_changed = pyqtSignal()  

    def __init__(self, argv):
        super().__init__(argv)
        self.setApplicationName("SpendWise")
        self.setOrganizationName("SpendWiseOrg")
        self.setApplicationVersion("1.0")

        font = QFont("Segoe UI", 9)
        if sys.platform != "win32":
            font.setFamily("Arial")
        self.setFont(font)

def main():
    app = SpendWiseApp(sys.argv)

    # --- Load Logo ---
    logo_path = images.get_logo_path()
    logo_pixmap = QPixmap()
    if logo_path and os.path.exists(logo_path):
        if not logo_pixmap.load(logo_path):
            print(f"Warning: Failed to load logo from {logo_path}. Using fallback.")
            logo_pixmap = QPixmap(64, 64)
            logo_pixmap.fill(Qt.darkGray)
            painter = QPainter(logo_pixmap)
            painter.setPen(Qt.white)
            painter.drawText(logo_pixmap.rect(), Qt.AlignCenter, "SW")
            painter.end()
    else:
        print(f"Warning: Logo file not found at configured path '{logo_path}'. Using fallback.")
        logo_pixmap = QPixmap(64, 64)
        logo_pixmap.fill(Qt.darkCyan)
        painter = QPainter(logo_pixmap)
        painter.setPen(Qt.white)
        painter.drawText(logo_pixmap.rect(), Qt.AlignCenter, "S W")
        painter.end()

    app.setWindowIcon(QIcon(logo_pixmap))
    # --- End Load Logo ---

    splash = SplashScreen(logo_pixmap)
    splash.show()
    QApplication.processEvents()

    settings = QSettings("SpendWiseOrg", "SpendWise")
    initial_lang = settings.value("language", "en", type=str)
    initial_theme = settings.value("theme", "light", type=str)

    translator = Translator(TRANSLATIONS, initial_lang)
    app.translator = translator

    themes = {
        "light": light_theme.LIGHT_THEME_QSS,
        "dark": dark_theme.DARK_THEME_QSS
    }
    theme_manager = ThemeManager(themes, initial_theme)
    app.theme_manager = theme_manager
    theme_manager.apply_theme(app, initial_theme)

    app.setLayoutDirection(Qt.RightToLeft if initial_lang == "ar" else Qt.LeftToRight)

    data_manager = DataManager(settings, app.translator)
    app.data_manager = data_manager

    main_window = MainWindow()

    translator.language_changed.connect(main_window.retranslate_ui_and_components)
    translator.language_changed.connect(
        lambda lang: app.setLayoutDirection(Qt.RightToLeft if lang == "ar" else Qt.LeftToRight)
    )
    app.currency_changed.connect(main_window.on_currency_changed)

    QTimer.singleShot(1500, lambda: show_main_window(splash, main_window))

    sys.exit(app.exec_())

def show_main_window(splash, window):
    splash.finish(window)

if __name__ == "__main__":
    main()

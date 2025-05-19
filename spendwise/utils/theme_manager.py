
from PyQt5.QtCore import QObject

class ThemeManager(QObject):
    def __init__(self, themes_dict, initial_theme='light'):
        super().__init__()
        self._themes = themes_dict 
        self.current_theme = initial_theme
        if self.current_theme not in self._themes:
            self.current_theme = 'light' 

    def apply_theme(self, app_instance, theme_name):
        if theme_name in self._themes:
            qss = self._themes[theme_name]
            app_instance.setStyleSheet(qss)
            self.current_theme = theme_name
        elif theme_name not in self._themes:
            print(f"Warning: Theme '{theme_name}' not found.")

    def get_available_themes(self):
        return list(self._themes.keys())

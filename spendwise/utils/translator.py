
from PyQt5.QtCore import QObject, pyqtSignal

class Translator(QObject):
    language_changed = pyqtSignal(str) 

    def __init__(self, translations_dict, initial_language='en'):
        super().__init__()
        self._translations = translations_dict
        self.current_language = initial_language
        if self.current_language not in self._translations:
            self.current_language = 'en' 

    def set_language(self, lang_code):
        if lang_code in self._translations and lang_code != self.current_language:
            self.current_language = lang_code
            self.language_changed.emit(lang_code) 

    def translate(self, key, default_text=None): 
        lang_dict = self._translations.get(self.current_language, {})
        translation = lang_dict.get(key)

        if translation is None: 
            if self.current_language != 'en':
                en_dict = self._translations.get('en', {})
                translation = en_dict.get(key)

        if translation is None: 
            if default_text is None and key and (' ' in key or key.islower() or '_' in key):
                return key.replace('_', ' ').capitalize() 
            return default_text if default_text is not None else f"[{key.upper()}]"

        return translation

    def get_available_languages(self):
        return list(self._translations.keys())

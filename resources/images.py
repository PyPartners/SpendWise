
import os

_RESOURCES_DIR = os.path.dirname(os.path.abspath(__file__))
APP_LOGO_PATH = os.path.join(_RESOURCES_DIR, "app_icons", "logo.png")

def get_logo_path():
    return APP_LOGO_PATH

import Resources.icons
from PyQt5.QtCore import QDir

def icons():
    return [icon for icon in QDir(":/icons")]

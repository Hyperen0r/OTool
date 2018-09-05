from Windows.MainWindow import MainWindow
from Windows.OSelector import OSelector
from Gui.QuickyGui import *

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout

class AppSelector(MainWindow):

    def __init__(self):
        super().__init__("Choose application")
        self.windowOSelector = OSelector()
        return

    def initUI(self):

        groupBox = create_group_box(self, "Choose an application")

        vbox = QVBoxLayout()

        buttonOSelector = create_button(self, "OSelector", self.actionOpenOSelector)
        vbox.addWidget(buttonOSelector)

        groupBox.setLayout(vbox)

        self.mainLayout.addWidget(groupBox)
        return

    def actionOpenOSelector(self):
        self.hide()
        self.windowOSelector.open()
        return

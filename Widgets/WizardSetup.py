from enum import Enum, auto
from Core.Config import get_config, save_config
from Gui.QuickyGui import *
from PyQt5.QtWidgets import QWizard, QWizardPage, QFileDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton

class PAGES(Enum):
    Page_Intro = 0
    Page_InstallFolder = 1


class WizardSetup(QWizard):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("OSelector - Wizard Setup")
        self.resize(640, 480)

        self.setOption(self.HaveFinishButtonOnEarlyPages, True)
        self.setOption(self.HaveHelpButton, False)

        self.setPage(PAGES.Page_Intro.value, IntroPage())
        self.setPage(PAGES.Page_InstallFolder.value, InstallFolderPage())

        self.button(QWizard.FinishButton).clicked.connect(self.onFinish)

    def onFinish(self):
        get_config().set("CONFIG", "bfirsttime", "False")
        save_config()


class IntroPage(QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Introduction")

        label = QLabel("Hello ! It's seems it is your first time using OSelector. Before, you can use it, "
                       "you have some setup to do. This wizard will guide you through the steps. <br />"
                       "<br />"
                       "<br />"
                       "If you encounter bugs or need some help, please visit : "
                       "<ul>"
                       "    <li><a href='https://www.nexusmods.com/skyrim/mods/93196'>Oldrim Mod Page</a></li>"
                       "    <li><a href='https://www.nexusmods.com/skyrimspecialedition/mods/19528'>SSE Mod Page</a></li>"
                       "    <li><a href='https://github.com/Hyperen0r/OTool'>GitHub Wiki</a></li>"
                       "</ul>")
        label.setOpenExternalLinks(True)
        label.setWordWrap(True)

        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)


class InstallFolderPage(QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Specify install folder")
        self.setSubTitle("Choose where generated plugins will be stored.")

        instructionsLabel = QLabel(self)
        instructionsLabel.setWordWrap(True)
        instructionsLabel.setText("If you use <b>Mod Organizer</b> and specify his <b>mods/</b> folder, then it will "
                                  "automatically be installed. You just have to activate it in <b>Mod organizer's</b> "
                                  "left pane, if you have never activate it before. "
                                  "(Refresh left pane if you don't see it)<br />"
                                  "<br />"
                                  "Or you can also specify your <b>Skyrim/data/</b> folder. In that case, you won't "
                                  "have to do anything. <br />"
                                  "<br />"
                                  "For any other location, you will have to install it manually through "
                                  "your preferred mod managers, or manually in your <b>Skyrim/data/</b> folder.")


        installFolderLabel = create_label(self, "Installation Folder")

        self.installFolderLineEdit = QLineEdit(self)
        currentInstallFolder = get_config().get("PATHS", "installFolder")
        if currentInstallFolder:
            self.installFolderLineEdit.setText(currentInstallFolder)

        installFolderLabel.setBuddy(self.installFolderLineEdit)

        buttonFileDialog = create_button(self, "...", self.getInstallFolder)
        buttonFileDialog.setFixedHeight(self.installFolderLineEdit.height())
        buttonFileDialog.setStyleSheet("padding : 0px")

        installFolderHBox = QHBoxLayout()
        installFolderHBox.addWidget(installFolderLabel)
        installFolderHBox.addWidget(self.installFolderLineEdit)
        installFolderHBox.addWidget(buttonFileDialog)
        installFolderHBox.setSpacing(10)

        self.registerField("installFolder", self.installFolderLineEdit)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(instructionsLabel)
        layout.addStretch()
        layout.addItem(installFolderHBox)
        self.setLayout(layout)

    def getInstallFolder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Mod folder location', '', QFileDialog.ShowDirsOnly)

        if folder:
            self.installFolderLineEdit.setText(str(folder))
            get_config().set("PATHS", "installFolder", str(folder))

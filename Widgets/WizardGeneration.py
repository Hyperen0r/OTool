import xml.etree.ElementTree as ET

from Resources.resources import icons
from Core.Utils import *
from Core.Config import get_config, save_config
from Gui.QuickyGui import *
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWizard, QWizardPage, QFileDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QCompleter

class WizardGeneration(QWizard):
    def __init__(self, widget, parent=None):
        super().__init__(parent)

        self.setWindowTitle("OSelector - Wizard Plugin Generation")
        self.resize(640, 480)

        self.setOption(self.HaveFinishButtonOnEarlyPages, True)
        self.setOption(self.HaveHelpButton, False)

        self.widget = widget

        self.page = GenerationPage()
        self.setPage(0, self.page)
        self.page.setDefaultValues()

        self.button(QWizard.FinishButton).clicked.connect(self.onFinish)

    def onFinish(self):
        folder, name, icon = self.page.getValues()

        if name:
            get_config().set("CONFIG", "lastName", name)
        if icon:
            get_config().set("CONFIG", "lastIcon", icon)
        save_config()

        path_plugin_folder = folder + "/" + \
                             name + "/" + \
                             get_config().get("PATHS", "pluginFolder")

        create_dir(path_plugin_folder)

        logging.info("Plugin destination : " + path_plugin_folder)

        xml_root = self.widget.toXML(name, icon)

        with open(path_plugin_folder + name + ".myo", "w") as file:
            data = ET.tostring(xml_root, "unicode")
            file.write(data)

        msg_box = QMessageBox()
        msg_box.setWindowTitle("Results")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText("Plugin Generation Done !\n"
                        "----- Plugin path -----\n" +
                        path_plugin_folder)
        msg_box.addButton(QPushButton("Open Folder"), QMessageBox.ActionRole)
        msg_box.addButton(QPushButton("Ok"), QMessageBox.YesRole)
        msg_box.exec_()

        if msg_box.buttonRole(msg_box.clickedButton()) == QMessageBox.ActionRole:
            os.startfile(os.path.realpath(path_plugin_folder))


class GenerationPage(QWizardPage):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Plugin generation settings")
        self.labelWidth = 125
        self.lineEditWidth = 350
        self.pixmapSize = QSize(50, 50)

        # INSTALLATION FOLDER
        installFolderLabel = create_label(self, "Installation Folder")
        installFolderLabel.setFixedWidth(self.labelWidth)
        installFolderLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.installFolderLineEdit = QLineEdit(self)
        self.installFolderLineEdit.setFixedWidth(self.lineEditWidth)

        installFolderLabel.setBuddy(self.installFolderLineEdit)

        buttonFileDialog = create_button(self, "...", self.getInstallFolder)
        buttonFileDialog.setFixedHeight(self.installFolderLineEdit.height())
        buttonFileDialog.setStyleSheet("padding : 0px")

        installFolderHBox = QHBoxLayout()
        installFolderHBox.addWidget(installFolderLabel)
        installFolderHBox.addWidget(self.installFolderLineEdit)
        installFolderHBox.addWidget(buttonFileDialog)
        installFolderHBox.setSpacing(10)

        # PLUGIN NAME
        pluginNameLabel = create_label(self, "Plugin Name")
        pluginNameLabel.setFixedWidth(self.labelWidth)
        pluginNameLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.pluginNameLineEdit = QLineEdit(self)
        self.pluginNameLineEdit.setFixedWidth(self.lineEditWidth)

        pluginNameLabel.setBuddy(self.pluginNameLineEdit)

        pluginNameHBox = QHBoxLayout()
        pluginNameHBox.addWidget(pluginNameLabel)
        pluginNameHBox.addWidget(self.pluginNameLineEdit)
        pluginNameHBox.addWidget(QLabel())
        pluginNameHBox.setSpacing(10)

        # PLUGIN ICON
        pluginIconLabel = create_label(self, "Plugin Icon")
        pluginIconLabel.setFixedWidth(self.labelWidth)
        pluginIconLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.pluginIconLineEdit = QLineEdit(self)
        self.pluginIconLineEdit.setFixedWidth(self.lineEditWidth)
        self.pluginIconLineEdit.setCompleter(QCompleter(icons(), self))
        self.pluginIconPixmap = QLabel()
        self.pluginIconLineEdit.textEdited.connect(self.updateImage)
        self.pluginIconLineEdit.textChanged.connect(self.updateImage)
        pluginIconLabel.setBuddy(self.pluginIconLineEdit)


        pluginIconHBox = QHBoxLayout()
        pluginIconHBox.addWidget(pluginIconLabel)
        pluginIconHBox.addWidget(self.pluginIconLineEdit)
        pluginIconHBox.addWidget(self.pluginIconPixmap)
        pluginIconHBox.setSpacing(10)

        self.registerField("installFolder*", self.installFolderLineEdit)
        self.registerField("name*", self.pluginNameLineEdit)
        self.registerField("icon*", self.pluginIconLineEdit)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addItem(installFolderHBox)
        layout.addItem(pluginNameHBox)
        layout.addItem(pluginIconHBox)
        layout.addStretch()
        self.setLayout(layout)

    def getInstallFolder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Mod folder location', '', QFileDialog.ShowDirsOnly)

        if folder:
            self.installFolderLineEdit.setText(str(folder))

    def updateImage(self):
        self.pluginIconPixmap.setPixmap(QPixmap(":/icons/" + self.pluginIconLineEdit.text()))

    def getValues(self):
        return self.installFolderLineEdit.text(), self.pluginNameLineEdit.text(), self.pluginIconLineEdit.text()

    def setDefaultValues(self):
        folder = get_config().get("PATHS", "installFolder")
        self.installFolderLineEdit.setText(folder)

        name = get_config().get("CONFIG", "lastName") or get_config().get("PLUGIN", "name")
        self.pluginNameLineEdit.setText(name)

        icon =  get_config().get("CONFIG", "lastIcon") or get_config().get("PLUGIN", "defaultPackageIcon")
        self.pluginIconLineEdit.setText(icon)

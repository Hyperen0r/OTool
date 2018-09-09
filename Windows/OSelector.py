from Core.Utils import *
from Core.Config import get_config, save_config
from Core.Stage import Stage
from Core.Animation import Animation
from Core.Package import Package
from Core.FNISParser import FNISParser
from Gui.QuickyGui import *
from Widgets.AnimTreeWidget import AnimTreeWidget
from Widgets.IconsViewer import IconsViewer
from Widgets.WizardSetup import WizardSetup
from Widgets.WizardGeneration import WizardGeneration
from Windows.MainWindow import MainWindow
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QTabWidget, QFileDialog

log = logging.getLogger(__name__)

# TODO - Add merge plugin


class OSelector(MainWindow):

    def __init__(self):
        super().__init__("OSelector")
        self.setSize(QSize(1200, 1000))
        self.wizardSetup = WizardSetup()
        return

    def initUI(self):
        mainHBox = QHBoxLayout()
        # ====================== LEFT PANE ======================
        self.groupBoxNavMenu = create_group_box(self, "Navigation Menu")

        self.navMenu = AnimTreeWidget()
        self.navMenu.itemClicked.connect(self.slotLcdAnimChecked)
        self.wizardGeneration = WizardGeneration(self.navMenu)

        hbox = QHBoxLayout()
        hbox.addWidget(self.navMenu)

        self.groupBoxNavMenu.setLayout(hbox)

        mainHBox.addWidget(self.groupBoxNavMenu)
        # ====================== RIGHT PANE ======================
        rightVBox = QVBoxLayout()

        # Statistics
        self.groupBoxAnimStat = create_group_box(self, "Statistics")

        labelAnimChecked = create_label(self, "Animations checked")
        self.lcdAnimChecked = create_lcd(self)

        hbox = QHBoxLayout()
        hbox.addWidget(labelAnimChecked)
        hbox.addWidget(self.lcdAnimChecked)

        self.groupBoxAnimStat.setLayout(hbox)

        # Loading
        self.groupBoxAnimLoad = create_group_box(self, "Load / Add animations")

        buttonScanFolder = create_button(self, "Scan Folder", self.actionScanFolder)
        buttonLoadPlugin = create_button(self, "Load Plugin", self.actionLoadPlugin)

        hbox = QHBoxLayout()
        hbox.addWidget(buttonScanFolder)
        hbox.addWidget(buttonLoadPlugin)

        self.groupBoxAnimLoad.setLayout(hbox)

        # Generation
        self.groupBoxPluginGen = create_group_box(self, "Plugin Generation")

        buttonGeneratePlugin = create_button(self, "Generate Plugin", self.actionGeneratePlugin)
        buttonSetInstallFolder = create_button(self, "Set Install Folder", self.actionSetInstallFolder)

        hbox = QHBoxLayout()
        hbox.addWidget(buttonGeneratePlugin)
        hbox.addWidget(buttonSetInstallFolder)

        self.groupBoxPluginGen.setLayout(hbox)

        # Widget
        self.tabWidget = QTabWidget(self)
        self.tabWidget.addTab(IconsViewer(self), "Icons List")
        self.tabWidget.setCurrentIndex(1)

        rightVBox.setSpacing(50)
        rightVBox.addWidget(self.groupBoxAnimStat)
        rightVBox.addWidget(self.groupBoxAnimLoad)
        rightVBox.addWidget(self.groupBoxPluginGen)
        rightVBox.addWidget(self.tabWidget)

        mainHBox.addItem(rightVBox)
        mainHBox.setStretch(0, 3)
        mainHBox.setStretch(1, 1)
        mainHBox.setSpacing(10)
        self.mainLayout.addItem(mainHBox)
        return

    def actionScanFolder(self):
        log.info("Action: Scan Folder called")
        self.toggleGroupBoxes(False)

        animations = set()
        if self.navMenu.invisibleRootItem().childCount() > 0:
            box = QMessageBox()
            box.setIcon(QMessageBox.Question)
            box.setWindowTitle('Clear or Append ?')
            box.setText("Do you want to append new animations to the tree or build a new one ?")
            box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            buttonY = box.button(QMessageBox.Yes)
            buttonY.setText('Clear')
            buttonN = box.button(QMessageBox.No)
            buttonN.setText('Append')
            box.exec_()

            if box.clickedButton() == buttonY:
                self.navMenu.clear()
            elif box.clickedButton() == buttonN:
                answer = question(None, "Duplicates ?", "Do you want to ignore already existing animations ?")
                if answer == QMessageBox.Yes:
                    animations = self.navMenu.animationsId()

        self.scanFolder(animations)

        self.toggleGroupBoxes(True)
        log.info("Action: Scan Folder done")

    def actionLoadPlugin(self):
        log.info("Action: Load Plugin called")
        self.toggleGroupBoxes(False)

        animations = set()
        if self.navMenu.invisibleRootItem().childCount() > 0:
            box = QMessageBox()
            box.setIcon(QMessageBox.Question)
            box.setWindowTitle('Clear or Append ?')
            box.setText("Do you want to append new animations to the tree or build a new one ?")
            box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            buttonY = box.button(QMessageBox.Yes)
            buttonY.setText('Clear')
            buttonN = box.button(QMessageBox.No)
            buttonN.setText('Append')
            box.exec_()

            if box.clickedButton() == buttonY:
                self.navMenu.clear()
            elif box.clickedButton() == buttonN:
                answer = question(None, "Duplicates ?", "Do you want to ignore already existing animations ?")
                if answer == QMessageBox.Yes:
                    animations = self.navMenu.animationsId()

        self.loadPlugin(animations)

        self.toggleGroupBoxes(True)
        log.info("Action: Load Plugin done")

    def actionGeneratePlugin(self):
        log.info("Action: Generate Plugin called")
        self.toggleGroupBoxes(False)
        self.generatePlugin()
        self.toggleGroupBoxes(True)
        log.info("Action: Generate Plugin done")

    def actionSetInstallFolder(self):
        log.info("Action: Set Install Folder called")
        self.toggleGroupBoxes(False)
        self.setInstallFolder()
        self.toggleGroupBoxes(True)
        log.info("Action: Set Install Folder done")

    def open(self):
        self.show()

        firstTime = get_config().getboolean("CONFIG", "bfirstTime")

        if firstTime:
            self.openWizardSetup()

    def openWizardSetup(self):
        self.wizardSetup.show()

    def loadPlugin(self, animations):
        name = get_config().get("CONFIG", "lastName") or get_config().get("PLUGIN", "name")
        xml_file, _filter = QFileDialog.getOpenFileName(self, "Open file",
                                                        get_config().get("PATHS", "installFolder") + "/" + name + "/" +
                                                        get_config().get("PATHS", "pluginFolder"),
                                                        "MyOsa file (*.myo)")
        if xml_file:
            log.info("Loading xml_file : " + xml_file)
            duplicate = self.navMenu.addXML(xml_file, animations)

            if duplicate > 0:
                QMessageBox.information(self, "Results", str(duplicate) +
                                        " duplicates found (Not added)\n"
                                        "List (INFO Level) available in logs (if activated)")
        self.treeChanged()

    def scanFolder(self, animations):
        scan_dir = QFileDialog.getExistingDirectory(self, 'Folder Location',
                                                    get_config().get("PATHS", "installFolder"),
                                                    QFileDialog.ShowDirsOnly)
        log.info("Scanning directory : " + scan_dir)

        if scan_dir:

            packages = dict()
            package = None
            redundantStrings = set()
            previous_module_name = ""
            duplicate = 0

            for root, dirs, files in os.walk(scan_dir):
                for file in files:
                    if file.startswith("FNIS") and file.endswith("List.txt"):
                        log.info("Found FNIS file : " + file)

                        FNIS_file = os.path.join(root, file)
                        package_name = FNIS_file.replace(scan_dir + '\\', '').split('\\', 1)[0]
                        if not package_name:
                            package_name = "Default Package"
                        package_name = toReadableString(package_name)

                        if package_name not in packages:
                            log.info(indent("Package name : " + package_name, 1))
                            package = Package(package_name)
                            redundantStrings = set()

                        for s in package_name.split():
                            redundantStrings.add(s.lower())

                        module_name = file[5:-9]
                        module_name = removeWords(toReadableString(module_name), redundantStrings)
                        redundantModuleStrings = set(redundantStrings)
                        for s in module_name.split():
                            redundantModuleStrings.add(s.lower())

                        if not module_name:
                            module_name = previous_module_name or package_name

                        log.info(indent("Module name : " + module_name, 2))

                        module = package.getModuleFromName(module_name)
                        if not module:
                            module = dict()
                            package.addModule(module_name, module)

                        with open(FNIS_file, 'r') as f:
                            for line in f:
                                anim_type, anim_options, anim_id, anim_file, anim_obj = FNISParser.parseLine(line)

                                if anim_id in animations:
                                    duplicate += 1
                                    log.info("Duplicate found : " + anim_id)
                                elif anim_type == FNISParser.TYPE.UNKNOWN or not anim_id:
                                    log.debug(indent("Anim type : " + anim_type.name + " || Line : " + line.strip(), 4))
                                else:
                                    log.debug(indent("Adding animation, Type : " + anim_type.name + " || Line : " + line.strip(), 4))

                                    stage = Stage(anim_type, anim_options, anim_id, anim_file, anim_obj)
                                    animation_name = FNISParser.getAnimationNameFrom(anim_id)
                                    animation_name = removeWords(toReadableString(animation_name), redundantModuleStrings)
                                    animation = package.getAnimationFromName(animation_name) or \
                                                package.getAnimationFromName(module_name + " " + animation_name)
                                    if not animation:
                                        animation = Animation()
                                        animation.addStage(stage)
                                        module[animation_name] = animation
                                    else:
                                        animation.addStage(stage)

                        if package.hasAnimation() > 0:
                            packages[package_name] = package

            self.navMenu.addPackages(packages)

            if duplicate > 0:
                QMessageBox.information(self, "Results", str(duplicate) +
                                        " duplicates found (Not added)\n"
                                        "List (INFO Level) available in logs (if activated)")
        self.treeChanged()

    def setInstallFolder(self):
        folder = get_config().get("PATHS", "installFolder")
        if folder:
            answer = question(self, "Overwrite ?", "Install folder already set to :\n" + str(folder) + "\n\n" + "Do you want to overwrite it ?")
            if answer == QMessageBox.No:
                return

        folder = QFileDialog.getExistingDirectory(self, 'Mod folder location', folder, QFileDialog.ShowDirsOnly)

        if folder:
            get_config().set("PATHS", "installFolder", str(folder))
            save_config()

    def slotLcdAnimChecked(self):
        self.lcdAnimChecked.display(self.navMenu.animationsCount())

    def treeChanged(self):
        self.slotLcdAnimChecked()

    def generatePlugin(self):
        logging.info("=============== GENERATING PLUGIN ===============")

        self.wizardGeneration.show()

        return

    def toggleGroupBoxes(self, state):
        self.groupBoxPluginGen.setEnabled(state)
        self.groupBoxAnimStat.setEnabled(state)
        self.groupBoxAnimLoad.setEnabled(state)
        self.groupBoxNavMenu.setEnabled(state)

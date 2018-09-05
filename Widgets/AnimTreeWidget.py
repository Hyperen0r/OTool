import xml.etree.ElementTree as ET

from Core.Utils import create_item
from Core.Config import get_config
from Resources.resources import icons
from PyQt5.QtCore import Qt, QSize, QRect, QEvent, pyqtSignal
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon, QPixmap
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QHeaderView, QStyledItemDelegate, QLineEdit, QCompleter


class AnimTreeWidget(QTreeWidget):

    def __init__(self):
        super().__init__()

        self.header().setDefaultAlignment(Qt.AlignHCenter)
        self.header().setMinimumSectionSize(200)
        self.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.setHeaderLabels(["Name", "Icon", "Id"])

        editIconDelegate = EditIconItemDelegate(self)
        editIconDelegate.iconTextChanged.connect(self.iconTextChanged)
        self.setItemDelegateForColumn(1, editIconDelegate)

        self.setIconSize(QSize(40, 40))
        self.setDragDropMode(self.InternalMove)
        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        #self.customContextMenuRequested.connect(self.open_menu)
        self.setAlternatingRowColors(True)
        self.setEditTriggers(QTreeWidget.DoubleClicked | QTreeWidget.EditKeyPressed)
        self.setSelectionMode(self.ExtendedSelection)

    def iconTextChanged(self, str):
        item = self.currentItem()
        item.setIcon(0, QIcon(":/icons/" + str or item.text(1)))

    def addPackages(self, packages):

        for packageName, package in packages.items():

            packageIcon = get_config().get("PLUGIN", "defaultPackageIcon")
            packageItem = create_item(packageName, packageIcon)

            for moduleName, module in package.modules.items():

                moduleIcon = get_config().get("PLUGIN", "defaultFolderIcon")
                moduleItem = create_item(moduleName, moduleIcon)

                for animationName, animation in module.items():
                    item = animation.toItem()
                    if item:
                        moduleItem.addChild(item)

                if moduleItem.childCount():
                    packageItem.addChild(moduleItem)

            if packageItem.childCount():
                self.addTopLevelItem(packageItem)

        return

    def toXML(self, name, icon):
        root = self.invisibleRootItem()
        folder0 = ET.Element("folder0")
        folder0.set("n", name)
        folder0.set("i", icon)

        self.childToXML(folder0, root, 1)
        return folder0

    def childToXML(self, xml, parent, level):
        for i in range(parent.childCount()):
            child = parent.child(i)
            if child.checkState(0) != Qt.Unchecked:
                if child.text(2):
                    entry = ET.SubElement(xml, "entry")
                    entry.set("n", child.text(0))
                    entry.set("i", child.text(1))
                    entry.set("id", child.text(2))
                else:
                    folder = ET.SubElement(xml, "folder" + str(level))
                    folder.set("n", child.text(0))
                    folder.set("i", child.text(1))
                    self.childToXML(folder, child, level + 1)


class IconDelegate(QStyledItemDelegate):

    def __init__(self, parent):
        super().__init__(parent)
        self.size = QSize(50, 50)

    def paint(self, painter, option, index):
        super().paint(painter, option, index)


class EditIconItemDelegate(QStyledItemDelegate):

    iconTextChanged = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.size = QSize(40, 40)
        self.undo = ""

    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        editor.textChanged.connect(self.updateText)
        editor.textEdited.connect(self.updateText)
        editor.setFrame(True)

        completer = QCompleter(icons(), editor)
        editor.setCompleter(completer)

        return editor

    def setEditorData(self, lineEdit, index):
        value = index.model().data(index, Qt.EditRole)
        self.undo = value
        lineEdit.setText(value)

    def setModelData(self, lineEdit, model, index):
        value = lineEdit.text()
        model.setData(index, value, Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def eventFilter(self, editor, event):
        if (event.type() == QEvent.KeyPress and event.key() == Qt.Key_Escape):
            self.updateText(self.undo)
            self.closeEditor.emit(editor)
            return True
        elif (event.type() == QEvent.KeyPress and ( event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter )):
            self.commitData.emit(editor)
            self.closeEditor.emit(editor)
            return True
        return False

    def updateText(self, string):
        self.iconTextChanged.emit(string)

import logging
import xml.etree.ElementTree as ET

from Core.Utils import create_item
from Core.Config import get_config
from Resources.resources import icons
from PyQt5.QtCore import Qt, QSize, QEvent, pyqtSignal
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import QTreeWidget, QHeaderView, QStyledItemDelegate, QLineEdit, QCompleter,\
                            QMessageBox, QMenu

log = logging.getLogger(__name__)

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
        self.customContextMenuRequested.connect(self.open_menu)
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

    def addXML(self, xml, animations):
        xml = ET.parse(xml)
        root = self.invisibleRootItem()
        return self.addXMLChild(root, xml.getroot(), animations)

    def addXMLChild(self, parent, elt, animations):
        duplicateCounter = 0
        for child in elt:
            name = child.get("n")
            icon = child.get("i") or get_config().get("PLUGIN", "defaultFolderIcon")
            id = child.get("id")
            if not id:
                id = ""

            if id in animations:
                duplicateCounter += 1
                log.info("Duplicate found : " + child.get("n"))
            else:
                item = create_item(name, icon, id)
                parent.addChild(item)
                duplicateCounter += self.addXMLChild(item, child, animations)
        return duplicateCounter

    def animationsCount(self, elt=None, state=Qt.Unchecked):
        if not elt:
            elt = self.invisibleRootItem()

        counter = 0
        for i in range(elt.childCount()):
            child = elt.child(i)
            if child.checkState(0) != state:
                if child.text(2):
                    counter += 1
                else:
                    counter += self.animationsCount(child, state)
        return counter

    def animationsId(self, item=None):
        if item is None:
            item = self.invisibleRootItem()

        animations = set()

        for i in range(item.childCount()):
            child = item.child(i)
            id = child.text(2)
            if id:
                animations.add(id)
            else:
                animations = animations.union(self.animationsId(child))
        return animations


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

    def check_all(self):
        root = self.invisibleRootItem()
        for i in range(root.childCount()):
            self.check_children(root.child(i), Qt.Checked)

    def check_children(self, item, state):
        item.setCheckState(0, state)
        for i in range(item.childCount()):
            self.check_children(item.child(i), state)

    def action_checkAll(self):
        log.info("ACTION : Checking all")
        root = self.invisibleRootItem()
        for i in range(root.childCount()):
            self.check_children(root.child(i), Qt.Checked)

    def action_uncheckAll(self):
        log.info("ACTION : Unchecking all")
        root = self.invisibleRootItem()
        for i in range(root.childCount()):
            self.check_children(root.child(i), Qt.Unchecked)

    def action_insertParent(self):
        log.info("ACTION : Inserting parent")
        items = self.selectedItems()
        newParent = create_item("New Item")

        # We want the lowest parent (Meaning the parent the most close to the root)
        items_parent = []
        for item in items:
            if item in items_parent:
                items_parent.clear()

            item_parent = item.parent()
            if not item_parent:
                item_parent = self.invisibleRootItem()

            if not item_parent in items:
                items_parent.append((item_parent, item))

        parent, item = items_parent[0]

        index = parent.indexOfChild(item)
        parent.insertChild(index, newParent)

        for item in items:
            item_parent = item.parent()
            if not item_parent:
                item_parent = self.invisibleRootItem()

            item_index = item_parent.indexOfChild(item)
            child = item_parent.takeChild(item_index)
            newParent.addChild(child)
        return

    def action_merge(self):
        log.info("ACTION : Merging")
        items = self.selectedItems()

        items_parent = []
        for item in items:
            item_parent = item.parent()
            if not items_parent:
                items_parent = self.invisibleRootItem()

            if item_parent in items:
                QMessageBox.warning(self, "Merge Action", "One selected folder is a parent of another selected folder !\n"
                                                          "Merging folders with both parent and child selected is not supported !\n"
                                                          "Select only folders from the same level")
                return

            if item.text(2):
                QMessageBox.warning(self, "Merge Action", "Merging animations is not allowed !\n"
                                                          "Select only folders from the same level")
                return

        parent = items.pop(0)

        p2 = parent.parent()
        if not p2:
            p2 = self.invisibleRootItem()

        for item in items:
            for child_index in range(item.childCount()):
                child = item.takeChild(0)
                parent.addChild(child)
            p2.removeChild(item)

        return True

    def action_remove(self, item=None):
        log.info("ACTION : Removing")
        if not item:
            items = self.selectedItems()
            for item in items:
                self.action_remove(item)
            return True

        parent = item.parent()
        if not parent:
            parent = self.invisibleRootItem()
        parent.removeChild(item)

    def action_cleanup(self):
        log.info("ACTION : Cleaning")
        self.cleanup()

    def cleanup(self, item=None):
        if not item:
            item = self.invisibleRootItem()

        for i in reversed(range(item.childCount())):
            child = item.child(i)
            if child:
                self.cleanup(child)

        if not item.text(2) and item.childCount() == 0:
            if item is not self.invisibleRootItem():
                parent = item.parent()
                if not parent:
                    parent = self.invisibleRootItem()
                parent.removeChild(item)
        return

    def open_menu(self):
        selection = self.selectedItems()
        if selection:
            menu = QMenu()
            menu.addAction("Check All", self.action_checkAll)
            menu.addAction("Uncheck All", self.action_uncheckAll)
            menu.addAction("Cleanup", self.action_cleanup)
            menu.addSeparator()
            menu.addAction("Insert parent", self.action_insertParent)
            menu.addAction("Merge", self.action_merge)
            menu.addAction("Remove", self.action_remove)
            menu.exec_(QCursor.pos())
        return


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

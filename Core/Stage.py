from Core.Utils import create_item
from Core.Config import get_config
from Core.FNISParser import FNISParser
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidgetItem

class Stage:

    def __init__(self, _type="", _options=[], _id="", _file="", _obj=[], icon=get_config().get("PLUGIN", "defaultStageIcon")):
        self.type = _type
        self.options = _options
        self.id = _id
        self.file = _file
        self.obj = _obj
        self.icon = icon

    def setIcon(self, icon):
        self.icon = icon

    def name(self):
        return FNISParser.getAnimationNameFrom(self.id)

    def actor(self):
        return FNISParser.getActorNumberFrom(self.id)

    def stage(self):
        return FNISParser.getStageNumberFrom(self.id)

    def toItem(self, name=""):
        if not name:
            name = self.name()

        item = create_item(name, get_config().get("PLUGIN", "defaultStageIcon"), self.id)

        return item

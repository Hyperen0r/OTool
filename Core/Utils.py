import re
import os
import logging
from enum import Enum
from Core.Config import get_config
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTreeWidgetItem

log = logging.getLogger(__name__)

INDENT_SIZE = 8
MAX_STRING_LENGTH = get_config().getint("PLUGIN", "maxItemStringLength")

class ITEM_TYPE(Enum):
    ROOT = "Root"
    ANIMATION = "Animation"
    FOLDER = "Folder"
    SET = "Set"

def create_item(name="Default",
                icon=get_config().get("PLUGIN", "defaultFolderIcon"),
                id="",
                itemType=ITEM_TYPE.FOLDER,
                maxChildren=get_config().get("PLUGIN", "maxItemsPerPage")):

    item = QTreeWidgetItem()

    if id:
        name = name[slice(-MAX_STRING_LENGTH, None)]
    else:
        name = name[slice(0, MAX_STRING_LENGTH)]
    item.setText(0, name)
    item.setText(1, icon)
    item.setText(2, id)

    if id:
        itemType = ITEM_TYPE.ANIMATION

    item.setText(3, itemType.value)
    item.setText(4, maxChildren)
    item.setText(5, "0") #SetIndex
    item.setText(6, "0") #SetCounter
    item.setText(7, "0") #LevelTwoCounter

    item.setIcon(0, QIcon(":/icons/" + icon))
    item.setCheckState(0, Qt.Checked)

    flags = item.flags() | Qt.ItemIsAutoTristate | Qt.ItemIsEditable

    if id:
        item.setFlags(flags ^ Qt.ItemIsDropEnabled)
    else:
        item.setFlags(flags)
    return item

def toDefaultItem(item):
    item.setText(0, "")
    item.setText(1, "")
    item.setText(2, "")
    item.setText(3, ITEM_TYPE.ROOT.value)
    item.setText(4, get_config().get("PLUGIN", "maxItemsPerPage"))
    item.setText(5, "0") #SetIndex
    item.setText(6, "0") #SetCounter
    item.setText(7, "0") #LevelTwoCounter


def create_dir(path):
    if os.path.exists(path):
        log.info("Path already exists : " + path)
    else:
        log.info("Creating new directory: " + path)
        os.makedirs(path)


def indent(text, level=0):
    return (" " * INDENT_SIZE)*level + text

def int_filter(list):
    for v in list:
        try:
            int(v)
            continue # Skip these
        except ValueError:
            yield v # Keep these

def toReadableString(string):
    words = " ".join(string.replace("'", " ").replace("-"," ").replace("+"," ").replace("_", " ").split())

    out_string = ""
    for word in words.split():
        if not re.match("^(v|V)?\d+?\.?\d*?$", word) and len(word) > 1:
            out_string += word + " "

    return out_string.strip()

def removeWords(string, list):
    return " ".join([ word for word in string.split() if not word.lower() in list])

def splitIntoWords(string):
    return string.replace("_", " ").split(" ")

def join(list):
    string = ""
    for word in list:
        if string:
            string += " " + word
        else:
            string = word
    return string
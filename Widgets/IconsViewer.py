from Resources.resources import *
from PyQt5.QtCore import QSize, Qt, QRect
from PyQt5.QtGui import QIcon, QFont, QPixmap, QColor
from PyQt5.QtWidgets import QHeaderView, QTableWidget, QTableWidgetItem, QStyledItemDelegate


class IconsViewer(QTableWidget):

    def __init__(self, parent):
        super(IconsViewer, self).__init__(parent)

        font = QFont()
        font.setBold(True)

        self.icons = []
        self.setEditTriggers(self.NoEditTriggers)
        self.setColumnCount(2)
        self.verticalHeader().hide()
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.horizontalHeader().setFont(font)
        self.setAlternatingRowColors(True)
        self.setHorizontalHeaderLabels(["ICON", "NAME"])

        for iconName in icons():
            item = QTableWidgetItem(iconName)
            item.setTextAlignment(Qt.AlignCenter)

            icon = QTableWidgetItem(iconName)
            icon.setTextAlignment(Qt.AlignCenter)

            row = self.rowCount()
            self.insertRow(row)
            self.setItem(row, 0, icon)
            self.setItem(row, 1, item)

            self.icons.append(iconName)

        self.setItemDelegateForColumn(0, IconItemDelegate(self))

        self.setVisible(False)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setVisible(True)
        return

class IconItemDelegate(QStyledItemDelegate):

    def __init__(self, parent):
        super().__init__(parent)
        self.size = QSize(50, 50)

    def paint(self, painter, option, index):
        data = index.data()

        if data:
            pixmap = QPixmap(":/icons/"+data)
            pixmap = pixmap.scaled(self.size.width(), self.size.height(), Qt.KeepAspectRatio)
            x, y = option.rect.x(), option.rect.y()
            w, h = pixmap.width(), pixmap.height()
            if w < option.rect.width():
                x = x + (option.rect.width() - w) // 2
            else:
                y = y + (option.rect.height() - h) // 2
            rect = QRect(x, y, w, h)
            painter.drawPixmap(rect, pixmap)
        else:
            super().paint(painter, option, index)

    def sizeHint(self, option, index):
        return self.size


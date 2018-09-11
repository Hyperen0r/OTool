#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import logging
log = logging.getLogger(__name__)

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QMainWindow, QDesktopWidget, QWidget, QVBoxLayout, QStyle, QStyleFactory, QStatusBar)


class MainWindow(QMainWindow):

    def __init__(self, title):
        super().__init__()

        log.info("Initializing " + title + " window")
        self.setWindowIcon(QIcon('Resources/icon.ico'))
        self.setWindowTitle(title)

        self.mainLayout = QVBoxLayout()
        self.centralWidget = QWidget(self)
        self.centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.centralWidget)

        self.initUI()

        self.setMinimumSize(self.sizeHint())
        self.center()

    def center(self):
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignCenter, self.size(), QDesktopWidget().availableGeometry()))

    def setSize(self, size=None):
        if size is None:
            size = self.sizeHint()
        self.setMinimumSize(size)
        self.center()

    def initUI(self):
        """ To implement in child """
        return

    @staticmethod
    def setAppStyle(app):
        if "WindowsVista" in [st for st in QStyleFactory.keys()]:
            app.setStyle(QStyleFactory.create("WindowsVista"))
        elif "Fusion" in [st for st in QStyleFactory.keys()]:
            app.setStyle(QStyleFactory.create("Fusion"))
        elif sys.platform == "win32":
            app.setStyle(QStyleFactory.create("WindowsVista"))
        elif sys.platform == "linux":
            app.setStyle(QStyleFactory.create("gtk"))
        elif sys.platform == "darwin":
            app.setStyle(QStyleFactory.create("macintosh"))
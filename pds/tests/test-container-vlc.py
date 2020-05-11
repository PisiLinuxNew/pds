#!/usr/bin/python
# -*- coding: utf-8 -*-

# Pardus Desktop Services

# Copyright (C) 2010-2011, TUBITAK/UEKAE
# 2010 - Gökmen Göksel <gokmen:pardus.org.tr>

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

# Qt Libraries
from PyQt5 import QtWidgets 		# Qt
from PyQt5.QtCore import QObject, pyqtSignal

# PDS Container
from pds.container import PApplicationContainer

class PMplayer(PApplicationContainer):
    def __init__(self, parent = None):
        PApplicationContainer.__init__(self, parent)
        
        if parent:
            parent.closeEvent = self.closeEvent

    def openMedia(self, path):
        ret = self.start("vlc", (str(path),))
	
        if ret[0]:
            self.show()

        return ret

class TestUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.layout = QtWidgets.QGridLayout(self)

        self.pushbutton = QtWidgets.QPushButton("Open Media", self)
        self.layout.addWidget(self.pushbutton)

        self.mplayer = PMplayer(self)
        self.layout.addWidget(self.mplayer)

        self.pushbutton.clicked.connect(self.getMedia)
        
        self.setGeometry(self.x(),self.y(),400,200)

    def getMedia(self):
        self.mplayer.openMedia(
                QtWidgets.QFileDialog.getOpenFileName(self,
                    "Open Media", "/", "Media Files (*.ogv *.mov *.avi *.mp4)")[0])

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    ui = TestUI()
    ui.show()

    app.lastWindowClosed.connect(sys.exit)

    app.exec_()

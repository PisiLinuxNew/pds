#!/usr/bin/python
# -*- coding: utf-8 -*-

# Pardus Desktop Services
# Thread Module ~ thread.py

# Copyright (C) 2010, TUBITAK/UEKAE
# 2010 - Gökmen Göksel <gokmen:pardus.org.tr>

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

from PyQt5.QtCore import pyqtSignal
#from PyQt5.QtCore import SLOT
from PyQt5.QtCore import QThread

class PThread(QThread):
    def __init__(self, parent, action, callback=None, \
                 args=[], kwargs={}, exceptionHandler=None):
        QThread.__init__(self,parent)

        self.parent = parent
        if callback:
            parent.finished.connect(callback)

        self.action = action
        self.args = args
        self.kwargs = kwargs
        self.exceptionHandler = exceptionHandler
        self.data = None

    def run(self):
        try:
            self.data = self.action(*self.args, **self.kwargs)
        except Exception as e:
            #print e
            if self.exceptionHandler:
                self.exceptionHandler(e)
        finally:
            try:
                self.parent.cleanUp.connect(deleteLater())
            except:
                pass    #print("parent ögesinin cleanUp özelliği yok.")
            

    def cleanUp(self):
        self.deleteLater()

    def get(self):
        return self.data


#!/usr/bin/python
# -*- coding: utf-8 -*-

# Pardus Desktop Services

# Copyright (C) 2010-2011, TUBITAK/UEKAE
# 2010 - Gökçen Eraslan <gokcen:pardus.org.tr>
# 2010 - Gökmen Göksel <gokmen:pardus.org.tr>

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

# Qt Libraries
from PyQt5 import Qt

import time, os

class PApplicationContainer(Qt.QWidget):
    clientClosed = Qt.pyqtSignal()
    processFinished = Qt.pyqtSignal([int,int])
    
    
    def __init__(self, parent = None, process = None, args = ()):
        Qt.QWidget.__init__(self, parent)
        
        self.layout = Qt.QGridLayout(self)
        self._label = None
        self._proc = None
        self._process = process
        self._args = args
        
        self.parent = parent
        try:
            self.pwinId = parent.winId()
        except:
            self.pwinId = self.winId()
            
            
    def start(self, process = None, args = ()):
        print(process, args)
        process = process or self._process
        args = args or self._args

        if not process:
            return (False, "Executable not given")

        self._process = process
        self._args = args

        self._proc = Qt.QProcess(self)
        self._proc.finished.connect(self._finished)
        self._proc.start(process, args)
        
        print(self._proc.waitForReadyRead())
        print(self._proc.processId())
        winId = self.getWID_width_pid()
        print(winId)
        
        #while winId is None:
                #winId = self.getWID_width_pid()
                #print("winId bulunurken lütfen bekleyin")
        
        # önce işlem winId yi bul
        if winId is not None:
            self.container = Qt.QWindow.fromWinId(int(winId, 16))
            
            self.display = self.createWindowContainer(self.container, self)
            self.layout.addWidget(self.display)
        
        #print self.getWID()
        self.clientClosed.connect(self._proc.close)

        return (True, "'%s' process successfully started with pid = %s" % (process, self._proc.pid()))

    def closeEvent(self, event):
        if self.isRunning():
            self.clientClosed.emit()
            self._proc.terminate()
            self._showMessage("Terminating process %s" % self._process)
            self._proc.waitForFinished()
        event.accept()

    def _finished(self, exitCode, exitStatus):
        self.processFinished.emit(exitCode, exitStatus)
        if exitCode != 0:
            self._showMessage("%s process finished with code %s" % (self._process, exitCode))
        else:
            self.close()

    def _showMessage(self, message):
        if not self._label:
            self._label = Qt.QLabel(self)

        self._label.setText(message)
        self._label.show()

    def isRunning(self):
        if not self._proc:
            return False
        return not self._proc.state() == Qt.QProcess.NotRunning


    def getWID(self):
        time.sleep(5)
        winName = self.parent.windowTitle()  # win_name
        running = os.system("xwininfo -name \"{}\"".format(winName))
        if (not running == 0):
            return "process NotRunning"
        
        xwininfo = os.popen("xwininfo -name \"{}\"".format(winName))
        xwininfo_out = xwininfo.read()
        xwininfo.close()
        xwininfo_out = xwininfo_out.split("\n")
        xwininfo_out = xwininfo_out[1]
        winId = xwininfo_out.split(" ")[3]
        print(int(winId, 16), int(self.parent.winId()))
        return int(winId, 16)


    def getWID_width_pid(self): # FIXME: fix this function
        pid = self._proc.processId()
        ids_proc = os.popen("xwininfo -root -tree")
        
        ids = ids_proc.readlines()
        ids_proc.close()
        
        dump = []
        for i in range(len(ids)):
            if ids[i].strip().startswith("0x"):
                dump.append(ids[i].strip().split()[0])
        
        ids = dump
        del dump
        
        winIds = []
        for _id in ids:
            if os.system(f"xprop -id {_id} _NET_WM_PID") == 0:
                print("state -------------------->", self._proc.state())
                proc = os.popen(f"xprop -id {_id} _NET_WM_PID")
                winpid = proc.read()
                
                winpid = winpid.split(" ")[-1].strip("\n")
                if str(pid) == winpid:
                    winIds.append(_id)
                proc.close()
                    
        if len(winIds) > 0:
            return winIds[0] 
        else:
            return self.getWID_width_pid()

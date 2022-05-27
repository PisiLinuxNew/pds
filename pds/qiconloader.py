#!/usr/bin/python
# -*- coding: utf-8 -*-

# Pardus Desktop Services
# Copyright (C) 2010, TUBITAK/UEKAE
# 2010 - Gökmen Göksel <gokmen:pardus.org.tr>
# 2011 - Comak Developers <comak:pardus.org.tr>

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

# Pardus Desktop Services
from os import path
from os import getenv
from glob import glob

# PyQt5 Core Libraries
from PyQt5.QtCore import QFile, QFileInfo, QDir, QSize, QSettings, Qt
from PyQt5.QtGui import QPixmap, QPixmapCache, QIcon, QPainter, QImage, QImageReader # QImage, QImageReader for read svg files
from PyQt5 import QtNetwork

# Logging
import logging

# Pds
from pds import Pds

class QIconTheme:
    def __init__(self, dirList = [], parents = []):
        self.dirList = dirList
        self.parents = map(lambda x:str(x), list(parents))
        self.valid = False
        if len(dirList) > 0:
            self.valid = True

class QIconLoader:

    SizeSmall       = 16
    SizeSmallMedium = 22
    SizeMedium      = 32
    SizeLarge       = 48
    SizeHuge        = 64
    SizeEnormous    = 128

    TopLeft, TopRight, BottomLeft, BottomRight = range(4)

    def __init__(self, pds = None, debug = False, forceCache = False):

        self.iconSizes = (128, 64, 48, 32, 22, 16)

        if not pds:
            pds = Pds(debug = debug)
        self.pds = pds

        self._forceCache = forceCache

        # Get possible Data Directories
        dataDirs = QFile.decodeName(getenv('XDG_DATA_DIRS'))
        if not dataDirs.isalnum():
            dataDirs = u'/usr/local/share/:/usr/share/'

        dataDirs = QDir.homePath() + ":"+dataDirs
        #dataDirs = str(self.pds.config_path) + 'share:'+ dataDirs
        

        if self.pds.session.ExtraDirs:
            dirs = QFile.decodeName(
                    getenv(self.pds.session.ExtraDirs)).split(':')
            for dirName in dirs:
                dataDirs.append(':' + dirName + '/share')

        self.themeName = self.pds.settings(self.pds.session.IconKey, \
                                           self.pds.session.DefaultIconTheme)
        
        self.iconDirs =  filter(lambda x: path.exists(x),
                map(lambda x: path.join(unicode(x), 'icons'),
                    dataDirs.split(':')))
        self.iconDirs = list(set(self.iconDirs))

        logging.debug('Icon Dirs : %s' % ','.join(self.iconDirs))
        self.themeIndex = self.readThemeIndex(self.themeName)
        self.extraIcons = ['/usr/share/pixmaps', '/usr/share/pixmaps/icons']
        self.updateAvailableIcons()
        

    def updateAvailableIcons(self):
        self._available_icons = self.__get_icons()

    def readThemeIndex(self, themeName):

        dirList = []
        parents = []
        themeIndex = QFile()

        # Read theme index files
        for i in range(len(self.iconDirs)):
            themeIndex.setFileName(path.join(unicode(self.iconDirs[i]), 
                unicode(themeName), "index.theme"))
            if themeIndex.exists():
                indexReader = QSettings(themeIndex.fileName(), 
                        QSettings.IniFormat)
                for key in indexReader.allKeys():
                    if str(key).endswith("/Size"):
                        size = str(indexReader.value(key))
                        
                        dirList.append((size, 
                            unicode(key[:-5])))
                
                parents = indexReader.value('Icon Theme/Inherits')
                dump=parents
                parents = list()
                parents.append(dump)
                break
            
        return QIconTheme(dirList, parents)

    def __get_icons(self, themeName = ''):
        if themeName == '':
            themeName = self.themeName
        if themeName == self.themeName:
            index = self.themeIndex
        else:
            index = self.readThemeIndex(themeName)
        

        themes = [themeName]
        themes.extend(index.parents)
        logging.debug('Themes : %s ' % ','.join(themes))
        icons = []

        for iconDir in self.iconDirs:
            for theme in themes:
                if path.exists(path.join(iconDir, theme)):
                    for _path in index.dirList:
                        icons.extend(glob(path.join(iconDir, theme, 
                            _path[1],'*.png')))
                        icons.extend(glob(path.join(iconDir, theme, 
                            _path[1],'*.svg')))
                        
        
        for iconDir in self.extraIcons:
            if path.exists(iconDir):
                icons.extend(glob(path.join(iconDir, '*.png')))

        _icons = map(lambda a: a.split('/')[-1][:-4], icons)

        return list(set(_icons))

    def findIconHelper(self, size = int, themeName = str, iconName = str):
        pixmap = QPixmap()

        if iconName == '' or self.themeName == '':
            return pixmap

        if themeName == '':
            themeName = self.themeName

        if themeName == self.themeName:
            index = self.themeIndex
        else:
            index = self.readThemeIndex(themeName)

        
        subDirs = filter(lambda x:x[0] == str(size), index.dirList)
        
        for iconDir in self.iconDirs:
            if path.exists(path.join(iconDir, themeName)):
                for theme in subDirs:
                    fileName = path.join(iconDir, themeName, theme[1],
                            '%s.png' % str(iconName))
                    fileName_svg = path.join(iconDir, themeName, theme[1],
                            '%s.svg' % str(iconName))
                    logging.debug('Looking for : %s' % fileName)
                    if path.exists(fileName):
                        pixmap.load(fileName)
                        logging.debug('Icon: %s found in theme %s' % \
                                (iconName, themeName))
                        return pixmap
                    elif path.exists(fileName_svg):
                        pixmap.load(fileName_svg)
                        logging.debug('Icon: %s found in %s' % (iconName, iconDir))
                        return pixmap

        for iconDir in self.extraIcons:
            fileName = path.join(iconDir, '%s.png' % str(iconName))
            fileName_svg = path.join(iconDir, '{}.svg'.format(str(iconName)))
            if path.exists(fileName):
                pixmap.load(fileName)
                #print "pixmap ->{}".format(fileName)
                logging.debug('Icon: %s found in %s' % (iconName, iconDir))
                return pixmap
            elif path.exists(fileName_svg):
                    image=QImage(size, size, QImage.Format_RGB32)
                    reader=QImageReader(fileName)
                    reader.read(image)
                    pixmap.convertFromImage(image)
                    logging.debug('Icon: %s found in %s' % (iconName, iconDir))
                    #print "pixmap ->{}".format(fileName)
                    return pixmap

        if len(self._themes) > 0:
            self._themes.pop(0)
            if not len(self._themes) == 0 and pixmap.isNull():
                pixmap = self.findIconHelper(size, self._themes[0], iconName)
        return pixmap

    def findIcon(self, name = str, size = int):
        for _name in name:
            pixmapName = ''.join(('$qt', str(_name), str(size)))
            self.pixmap=QPixmapCache.find(pixmapName)               
            
            if (self.pixmap):
                logging.debug('Icon %s returned from cache' % _name)
                return self.pixmap
        self._themes = []
        if self.themeName:
            self._themes.append(self.themeName)
            for _name in name:
                #print self.themeName, _name
                self.pixmap = self.findIconHelper(int(size), self.themeName, _name)
                if not self.pixmap.isNull():
                    break
        if self.pixmap.isNull():
            for _name in name:
                self._themes.extend(self.themeIndex.parents)
                if len(self._themes) > 0:
                    self.pixmap = self.findIconHelper(int(size),self._themes[0] ,_name)
                    if not self.pixmap.isNull():
                        break
        if not name:
            return QPixmap()
        pixmapName = ''.join(('$qt', str(_name), str(size)))
        if not self.pixmap.isNull():
            logging.debug('Icon cached with name: %s ' % pixmapName)
            QPixmapCache.insert(pixmapName, self.pixmap)
        
        return self.pixmap

    def load(self, name, size = 128, forceCache = False):
        icon = QIcon()
        size = int(size)
        self.pixmap = QPixmap()
        if not type(name) in (list, tuple):
            name = [str(name)]
        if forceCache or self._forceCache:
            for _name in name:
                for _size in self.iconSizes:
                    self.pixmap=QPixmapCache.find('$qt'+str(_name)+str(_size))
                    
                    if (self.pixmap):
                        logging.debug('Icon %s returned from cache' % _name)
                        return self.pixmap

        logging.debug('Getting icon : %s size: %s' % (','.join(name), size))
        pix = self.findIcon(name, size)
        if pix.isNull():
            for _size in self.iconSizes:
                pix = self.findIcon(name, _size)
                if not pix.isNull():
                    if size == _size:
                        return pix
                    icon.addPixmap(pix)
            if icon.isNull():
                return self.pixmap
            return icon.pixmap(QSize(size, size))
        return pix

    def loadOverlayed(self, name, overlay = None, size = 128, overlay_size = 16, position = 2):

        if not overlay:
            return self.load(name, size)

        position = {self.TopLeft:     (0, 0),
                    self.TopRight:    (size-overlay_size, 0),
                    self.BottomLeft:  (0, size-overlay_size),
                    self.BottomRight: (size-overlay_size, size-overlay_size)}[position]

        icon = self.load(name, size).scaled(QSize(size, size), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        overlay = self.load(overlay, overlay_size)
        overlay = overlay.scaled(QSize(overlay_size, overlay_size), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        painter = QPainter(icon)
        painter.drawPixmap(position[0], position[1], overlay)

        return icon

    def icon(self, pix, size=128):
        return QIcon(self.load(pix, size))


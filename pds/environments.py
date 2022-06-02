#!/usr/bin/python
# -*- coding: utf-8 -*-

# Pardus Desktop Services
# Copyright (C) 2010, TUBITAK/UEKAE
# 2010 - Gökmen Göksel <gokmen:pardus.org.tr>
# 2010 - H. İbrahim Güngör <ibrahim:pardus.org.tr>
# 2011 - Comak Developers <comak:pardus.org.tr>

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

class DefaultDe(object):
    Name                 = 'X11'
    SessionTypes         = ()
    Version              = None
    VersionKey           = None
    ConfigPath           = '$HOME/.config'
    ConfigFile           = None
    ConfigType           = None
    ConfigBin            = None
    DefaultIconTheme     = 'hicolor'
    DefaultIconFile      = ''
    DefaultConfigPath    = None
    ExtraDirs            = None
    IconKey              = None
    i18n                 = staticmethod(lambda x: x)
# kde5 için sınıfı düzenlenecek ve kde5 için bilgiler istenecek!!!
class Kde5(DefaultDe):
    Name                 = 'kde'
    SessionTypes         = ('/usr/share/xsessions/plasma')
    Version              = '5'
    VersionKey           = 'KDE_SESSION_VERSION'
    ConfigPath           = ('$HOME/.config/', '$HOME/.config/')
    ConfigFile           = 'kdeglobals'
    ConfigType           = 'ini'
    DefaultConfigPath    = '$HOME/.config/kdeglobals'
    DefaultIconTheme     = 'breeze' # breeze simge teması svg dosyalarından oluşuyor pds png uzantılı dosyalar açıyor
    IconKey              = 'Icons/Theme'

class Xfce(DefaultDe):
    Name                 = 'xfce'
    Version              = '4'
    ConfigPath           = '$HOME/.config/xfce4/'
    ConfigFile           = 'xfconf/xfce-perchannel-xml/xsettings.xml'
    ConfigType           = 'xml'
    DefaultIconTheme     = 'Faenza'
    DefaultConfigPath    = '/etc/xdg/xfce4/%s' % ConfigFile
    IconKey              = 'IconThemeName'

class Enlightenment(DefaultDe):
    Name                 = 'enlightenment'
    Version              = '0.17'
    ConfigPath           = '$HOME/.e/e/'
    ConfigFile           = 'config/standard/e.cfg'
    ConfigType           = 'env'
    DefaultIconTheme     = 'Faenza'
    IconKey              = 'E_ICON_THEME'

class LXDE(DefaultDe):
    Name                 = 'LXDE'
    Version              = '0.5'
    ConfigPath           = '$HOME/.config'
    ConfigFile           = ''
    ConfigType           = None
    DefaultIconTheme     = 'Faenza'
    IconKey              = 'theme/name'
    DefaultIconFile      = '/usr/share/lxde/images/pisilinuxLogo.png'

class LxQt(DefaultDe):
    Name                 = 'LxQt'
    Version              = '1.1'
    ConfigPath           = '$HOME/.config/lxqt'
    ConfigFile           = ''
    ConfigType           = None
    DefaultIconTheme     = 'damadamas'
    IconKey              = 'theme/name'

class Fluxbox(DefaultDe):
    Name                 = 'fluxbox'
    Version              = '1.3.1'
    ConfigPath           = '$HOME/.config'
    ConfigFile           = ''
    ConfigType           = None
    DefaultIconTheme     = 'Faenza'

class Gnome(DefaultDe):
    Name                 = 'gnome'
    Version              = '2.32'
    ConfigPath           = '$HOME/.gnome2'
    ConfigFile           = ''
    ConfigType           = None
    DefaultIconTheme     = 'oxygen'


class Gnome3(DefaultDe):
    Name                 = 'gnome3'
    SessionTypes         = ('gnome-shell')
    Version              = '41.3'
    ConfigPath           = '$HOME/.gconf'
    ConfigFile           = ''
    ConfigType           = None
    DefaultIconTheme     = 'adwaita'

class Mate(DefaultDe):
    Name                 = 'mate'
    Version              = '1.25'
    ConfigPath           = '$HOME/.config/mate'
    ConfigFile           = ''
    ConfigType           = None
    DefaultIconTheme     = 'mate'
    
class Lumina(DefaultDe):
    Name                 = 'lumina'
    Version              = '1.6'
    ConfigPath           = '$HOME/.config/lumina'
    ConfigFile           = ''
    ConfigType           = None
    DefaultIconTheme     = 'adwaita'

class Cinnamon(DefaultDe):
    Name                 = 'cinnamon'
    Version              = '5.2'
    ConfigPath           = '$HOME/.config/cinnamon'
    ConfigFile           = ''
    ConfigType           = None
    DefaultIconTheme     = 'adwaita'

# -*- coding: utf-8 -*-
"""
/***************************************************************************
 kuw_filter
                                 A QGIS plugin
 Applies Kuwahara Filter
                              -------------------
        begin                : 2013-02-03
        copyright            : (C) 2013 by Caio Hamamura
        email                : caiohamamura@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import QFileInfo, QSettings, QObject, SIGNAL, Qt, QCoreApplication, QTranslator, qVersion
from PyQt4.QtGui import QCursor, QMessageBox, QAction, QIcon, QFileDialog, QApplication
from qgis.utils import iface
from qgis.core import QgsMapLayerRegistry, QgsMapLayer, QgsApplication
# Initialize Qt resources from file resources.py
import resources
import time
import os
# Import the code for the dialog
from kuw_filterdialog import kuw_filterDialog

class kuw_filter:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.outdir = ''
        self.ilayers = QgsMapLayerRegistry.instance()
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/python/plugins/kuw_filter"
        # initialize locale
        localePath = ""
        locale = QSettings().value("locale/userLocale").toString()[0:5]
        if QFileInfo(self.plugin_dir).exists():
            localePath = self.plugin_dir + "/i18n/kuw_filter_" + locale + ".qm"

        if QFileInfo(localePath).exists():
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = kuw_filterDialog()
    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(QIcon(":/plugins/kuw_filter/icon.png"), \
            QCoreApplication.translate("kuw_filter", "Kuwahara Filter", None, QApplication.UnicodeUTF8), self.iface.mainWindow())
        # connect the action to the run method
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&Kuwahara Filter", self.action)
    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&Kuwahara Filter", self.action)
        self.iface.removeToolBarIcon(self.action)
    # run method that performs all the real work
    def run(self):
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        # See if OK was pressed
        if True:
            # do something useful (delete the line containing pass and
            # substitute with your code)
            self.dlg.output.setText('')
            self.dlg.progressBar.setValue(0)
            self.dlg.refb.setText('1')
            self.dlg.mem.setText('100')
            self.dlg.inputbox.clear()
            for (key, layer) in self.ilayers.mapLayers().iteritems():
                if layer.type() == 1:
                    self.dlg.inputbox.addItem(str(layer.name()), key)
            pass
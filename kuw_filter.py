# -*- coding: utf-8 -*-
"""
/***************************************************************************
 kuw_filter
                                 A QGIS plugin
 Applies Kuwahara Filter
             #                 -------------------
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
from __future__ import absolute_import
from builtins import str
from builtins import object
# Import the PyQt and QGIS libraries
from qgis.PyQt.QtCore import QFileInfo, QSettings, QObject, Qt, QCoreApplication, QTranslator, qVersion
from qgis.PyQt.QtGui import QCursor, QIcon
from qgis.PyQt.QtWidgets import QMessageBox, QAction, QFileDialog, QApplication
from qgis.utils import iface
from qgis.core import QgsProject, QgsMapLayer, QgsApplication
# Initialize Qt resources from file resources.py
from . import resources
import time
import os
# Import the code for the dialog
from .kuw_filterdialog import kuw_filterDialog

class kuw_filter(object):

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.outdir = ''
        self.ilayers = QgsProject.instance()
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'KuwaharaFilter_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Kuwahara Filter')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None
        
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('KuwaharaFilter', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToRasterMenu(
                self.menu,
                action)
                
        self.actions.append(action)

        return action
    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/kuw_filter/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Kuwaraha Filter'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True
        
    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginRasterMenu(
                self.tr(u'&Kuwahara Filter'),
                action)
            self.iface.removeToolBarIcon(action)
    # run method that performs all the real work
    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = kuw_filterDialog()

        # show the dialog
        self.dlg.show()
        self.dlg.progressBar.setValue(0)
        # Run the dialog event loop
        # result = self.dlg.exec_()
        # # See if OK was pressed
        # if result:
        #     # Do something useful here - delete the line containing pass and
        #     # substitute with your code.
        #     pass

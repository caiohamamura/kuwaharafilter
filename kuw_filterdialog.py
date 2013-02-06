# -*- coding: utf-8 -*-
"""
/***************************************************************************
 kuw_filterDialog
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
from qgis.core import *
from PyQt4 import QtCore, QtGui
from form import Ui_form1
# create the dialog for zoom to point

class kuw_filterDialog(QtGui.QMainWindow, Ui_form1):
    def __init__(self, parent=None):
       super(kuw_filterDialog, self).__init__(parent)
       self.setupUi(self)

    @QtCore.pyqtSlot()
    def fsicked(self):
        self.output.setText(self.output.text())

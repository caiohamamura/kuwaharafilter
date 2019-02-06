## -*- coding: utf-8 -*-
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
from __future__ import absolute_import
from builtins import str
from qgis.PyQt.QtCore import QFileInfo, Qt
from qgis.PyQt.QtWidgets import QFileDialog, QMessageBox, QApplication, QMainWindow
from qgis.PyQt.QtGui import QCursor
from time import clock
import datetime as dt
from qgis.core import QgsProject
from qgis.PyQt import QtCore, QtGui
from .dialog import Ui_Form
from .filter import dofilter as doFilter
from qgis.utils import iface
import os
# create the dialog for zoom to point

#Use gpu if pyopencl available
try:
    import pyopencl
    from .filter_opencl import *
    doFilter = dofilter2
except:
    pass




class kuw_filterDialog(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        self.outdir = ''
        self.ilayers = QgsProject.instance()
        super(kuw_filterDialog, self).__init__(parent)
        self.layerPath = ''
        self.setupUi(self)
        self.run.clicked.connect(self.run_clicked)
        self.outputb.clicked.connect(self.outputb_clicked)
        
    @QtCore.pyqtSlot()
    def msgbox(self, texto, icon=QMessageBox.Information):
        msg = QMessageBox()
        msg.setText(str(texto))
        msg.setIcon(icon)
        msg.exec_()
    def run_clicked(self):
        self.setEnabled(False)
        input = self.inputbox.currentLayer().source()
        if str(self.output.text()) == '':
            try:
                output = os.environ['temp']+'out'+str(int(clock()*10000))+'.tif'
            except:
                if os.access('/tmp/kuw_filter', os.F_OK)==False:
                    os.mkdir('/tmp/kuw_filter')
                output = '/tmp/kuw_filter/out'+str(int(clock()*10000))+'.tif'
        else:
           output = str(self.output.text())
        self.setCursor(QCursor(Qt.WaitCursor))
        start = dt.datetime.now()
        if doFilter(self, input, output):
            elapsed = dt.datetime.now() - start
            elapsed = str(dt.timedelta(seconds=round(elapsed.total_seconds())))
            self.msgbox(QApplication.translate('kuw_filterdialog','Time elapsed:\n ')+elapsed)
            if self.addout.isChecked():
                fileName = str(output)
                fileInfo = QFileInfo(fileName)
                baseName = fileInfo.baseName()
                iface.addRasterLayer(fileName, baseName)
        self.setCursor(QCursor(Qt.ArrowCursor))
        self.setEnabled(True)
        self.close()
    def outputb_clicked(self):
        if len(self.outdir) == 0 :
            self.i=0
            self.layerPath = self.inputbox.currentLayer().source()
            while self.layerPath.find('\\', self.i) != -1:
                self.i = self.layerPath.find('\\', self.i)+1
            if self.i == 0:
                while self.layerPath.find('/', self.i) != -1:
                    self.i = self.layerPath.find('/', self.i)+1
            self.outdir = self.layerPath[0:self.i]
        else:
            self.outpath = self.outdir
            
        self.output.setText(QFileDialog.getSaveFileName(self, QApplication.translate('kuw_filterdialog','Select output file'), self.outdir, 'TIFF (*.tif);; '+QApplication.translate('kuw_filterdialog', 'All files')+' (*.*);;JPEG (*.jpg, *.jpeg)')[0])
        
        if len(str(self.output.text()))>0:
            self.i = 0
            while str(self.output.text()).find('/', self.i) != -1:
                self.i = str(self.output.text()).find('/', self.i)+1
            self.outdir = str(self.output.text())[0:self.i]   

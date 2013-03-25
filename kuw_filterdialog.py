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
from PyQt4.QtCore import QFileInfo, Qt
from PyQt4.QtGui import QFileDialog, QMessageBox, QCursor, QApplication
from time import clock
from qgis.core import QgsMapLayerRegistry
from PyQt4 import QtCore, QtGui
from form import Ui_form1
from filter import *
from qgis.utils import iface
import os
# create the dialog for zoom to point

class kuw_filterDialog(QtGui.QMainWindow, Ui_form1):
    def __init__(self, parent=None):
        self.outdir = ''
        self.ilayers = QgsMapLayerRegistry.instance()
        super(kuw_filterDialog, self).__init__(parent)
        self.layerPath = ''
        self.setupUi(self)
        self.inputbox.currentIndexChanged.connect(self.input_changed)
        self.inputb.clicked.connect(self.inputb_clicked)
        self.run.clicked.connect(self.run_clicked)
        self.outputb.clicked.connect(self.outputb_clicked)
        
    @QtCore.pyqtSlot()
    def msgbox(self, texto, icon=QMessageBox.Information):
        msg = QMessageBox()
        msg.setText(str(texto))
        msg.setIcon(icon)
        msg.exec_()
    def input_changed(self):
        self.layerID = (self.inputbox.itemData(self.inputbox.currentIndex()).toString())
        if len(self.layerID) != 0:
            self.layerPath = str(self.ilayers.mapLayer(self.layerID).source())
        else:
            self.layerPath = str(self.inputbox.currentText())
    def inputb_clicked(self):
        self.layerPath = QFileDialog.getOpenFileName(self, QApplication.translate('kuw_filterdialog', 'Select file', None, QApplication.UnicodeUTF8), '', QApplication.translate('kuw_filterdialog','TIFF (*.tif);; All files (*.*);;JPEG (*.jpg, *.jpeg)', None, QApplication.UnicodeUTF8))
        if self.inputbox != '':
            self.inputbox.addItem(self.layerPath, '')
            self.inputbox.setCurrentIndex(self.inputbox.count()-1)
    def run_clicked(self):
        start = clock()
        self.setEnabled(False)
        input = self.layerPath
        if str(self.output.text()) == '':
            try:
                output = os.environ['temp']+'out'+str(int(clock()*10000))+'.tif'
            except:
                if os.access('/tmp/kuw_filter', os.F_OK)==False:
                    os.mkdir('/tmp/kuw_filter')
                output = '/tmp/kuw_filter/out'+str(int(clock()*10000))+'.tif'
        else:
           output = str(self.output.text())
        refb = int(self.refb.text())
        memuse = int(self.mem.text())
        self.setCursor(QCursor(Qt.WaitCursor))
        if dofilter(self, input, output, refb, memuse) :
            self.msgbox(QApplication.translate('kuw_filterdialog','Time elapsed:\n ', None, QApplication.UnicodeUTF8)+str(int((clock()-start)/3600))+'h'+str(int((clock()-start)/60))+'m'+str((0.5+clock()-start)%60)[0:5]+'s')
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
            if len(self.layerPath) == 0:
                self.msgbox(QApplication.translate('kuw_filterdialog', 'Select input file first', None, QApplication.UnicodeUTF8), QMessageBox.Warning)
                return False
            self.i=0
            while self.layerPath.find('\\', self.i) != -1:
                self.i = self.layerPath.find('\\', self.i)+1
            if self.i == 0:
                while self.layerPath.find('/', self.i) != -1:
                    self.i = self.layerPath.find('/', self.i)+1
            self.outdir = self.layerPath[0:self.i]
        else:
            self.outpath = self.outdir
            
        self.output.setText(QFileDialog.getSaveFileName(self, QApplication.translate('kuw_filterdialog','Select output file', None, QApplication.UnicodeUTF8), self.outdir, 'TIFF (*.tif);; '+QApplication.translate('kuw_filterdialog', 'All files', None, QApplication.UnicodeUTF8)+' (*.*);;JPEG (*.jpg, *.jpeg)'))
        
        if len(str(self.output.text()))>0:
            self.i = 0
            while str(self.output.text()).find('/', self.i) != -1:
                self.i = str(self.output.text()).find('/', self.i)+1
            self.outdir = str(self.output.text())[0:self.i]   

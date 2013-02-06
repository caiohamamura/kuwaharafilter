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
from PyQt4.QtGui import QFileDialog, QMessageBox, QCursor
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
        self.setupUi(self)
        self.inputbox.currentIndexChanged.connect(self.input_changed)
        self.inputb.clicked.connect(self.inputb_clicked)
        self.run.clicked.connect(self.run_clicked)
        self.outputb.clicked.connect(self.outputb_clicked)
        
    @QtCore.pyqtSlot()
    def msgbox(self, texto):
        msg = QMessageBox()
        msg.setText(str(texto))
        msg.exec_()
    def input_changed(self):
        self.layerID = (self.inputbox.itemData(self.inputbox.currentIndex()).toString())
        if len(self.layerID) != 0:
            self.layerPath = str(self.ilayers.mapLayer(self.layerID).source())
        else:
            self.layerPath = str(self.inputbox.currentText())
    def inputb_clicked(self):
        self.layerPath = QFileDialog.getOpenFileName(self, 'Selecione o arquivo', '', 'TIFF (*.tif);; All files (*.*);;JPEG (*.jpg, *.jpeg)')
        if self.inputbox != '':
            self.inputbox.addItem(self.layerPath, '')
            self.inputbox.setCurrentIndex(self.inputbox.count()-1)
    def run_clicked(self):
        start = clock()
        self.setEnabled(False)
        input = self.layerPath
        if str(self.output.text()) == '':
            output = os.environ['temp']+'out'+str(int(clock()*10000))+'.tif'
        else:
           output = str(self.output.text())
        refb = int(self.refb.text())
        memuse = int(self.mem.text())
        self.setCursor(QCursor(Qt.WaitCursor))
        if dofilter(self, input, output, refb, memuse) :
            nova = QMessageBox(self)
            nova.setText('Completado com sucesso\n em '+str(int((clock()-start)/3600))+'h'+str(int((clock()-start)/60))+'m'+str((0.5+clock()-start)%60)[0:5]+'s')
            if self.addout.isChecked():
                fileName = str(output)
                fileInfo = QFileInfo(fileName)
                baseName = fileInfo.baseName()
                iface.addRasterLayer(fileName, baseName)
            nova.exec_()
        self.setCursor(QCursor(Qt.ArrowCursor))
        self.setEnabled(True)
        self.close()
    def outputb_clicked(self):
        if len(self.outdir) == 0 :
            self.i=0
            while self.layerPath.find('\\', self.i) != -1:
                self.i = self.layerPath.find('\\', self.i)+1
            self.outdir = self.layerPath[0:self.i]
        else:
            self.outpath = self.outdir
            
        self.output.setText(QFileDialog.getSaveFileName(self, 'Select output file', self.outdir, 'TIFF (*.tif);; All files (*.*);;JPEG (*.jpg, *.jpeg)'))
        
        if len(str(self.output.text()))>0:
            self.i = 0
            while str(self.output.text()).find('/', self.i) != -1:
                self.i = str(self.output.text()).find('/', self.i)+1
            self.outdir = str(self.output.text())[0:self.i]   

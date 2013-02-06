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
from PyQt4.QtCore import QFileInfo, QSettings, QObject, SIGNAL, Qt, QCoreApplication
from PyQt4.QtGui import QCursor, QMessageBox, QAction, QIcon, QFileDialog, QApplication
from qgis.utils import iface
from qgis.core import QgsMapLayerRegistry, QgsMapLayer, QgsApplication
from sys import exit
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
        locale = QSettings().value("locale/userLocale").toString()[0:2]

        if QFileInfo(self.plugin_dir).exists():
            localePath = self.plugin_dir + "/i18n/kuw_filter_" + locale + ".qm"

        if QFileInfo(localePath).exists():
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = kuw_filterDialog()
        self.dlg.input.currentIndexChanged.connect(self.muda)
        self.dlg.run.clicked.connect(self.prefilter)
        self.dlg.outputb.clicked.connect(self.savefname)
        self.dlg.inputb.clicked.connect(self.setinput)
    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(QIcon(":/plugins/kuw_filter/icon.png"), \
            "Filtro Kuwahara", self.iface.mainWindow())
        # connect the action to the run method
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&Kuwahara Filter", self.action)
    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&Kuwahara Filter", self.action)
        self.iface.removeToolBarIcon(self.action)
    def setinput(self):
        self.input = QFileDialog.getOpenFileName(self.dlg, 'Selecione o arquivo', '', 'TIFF (*.tif);; All files (*.*);;JPEG (*.jpg, *.jpeg)')
        if self.input != '':
            self.dlg.input.addItem(self.input, '')
            self.dlg.input.setCurrentIndex(self.dlg.input.count()-1)
    def muda(self):
        self.layerID = self.dlg.input.itemData(self.dlg.input.currentIndex()).toString()
        if len(self.layerID) != 0:
            self.layerPath = str(self.ilayers.mapLayer(self.layerID).source())
        else:
           self.layerPath = str(self.input)
    # run method that performs all the real work
    def msgbox(self, texto):
        msg = QMessageBox(self.dlg)
        msg.setText(str(texto))
        msg.exec_()
    def prefilter(self):
        self.dlg.setEnabled(False)
        input = self.layerPath
        if str(self.dlg.output.text()) == '':
            output = os.environ['temp']+'out'+str(int(time.clock()*10000))+'.tif'
        else:
            output = str(self.dlg.output.text())
        refb = int(self.dlg.refb.text())
        memuse = int(self.dlg.mem.text())
        self.filter(input, output, refb, memuse)
    def filter(self, input, output, refband=1, memuse=100):
        self.dlg.setCursor(QCursor(Qt.WaitCursor))
        start = time.clock()
        import gdal
        import numpy
        import sys
        gdal_datatypes={'binary':'Byte','uint8':'Byte','uint16':'UInt16','int32':'Int32'}
        try:
            from osgeo import gdal
        except ImportError:
            import gdal
        from gdalconst import GA_ReadOnly, GDT_Float32
        gdal.AllRegister()
        w = 5
        w2 = (w+1)/2
        refband=int(refband)
        memuse=int(memuse)
        tif = gdal.Open(str(input), GA_ReadOnly )
        driver = tif.GetDriver()
        xsize = tif.RasterXSize
        ysize = tif.RasterYSize
        out = driver.Create(str(output), xsize, ysize, 3, gdal.GDT_Byte)
        out.SetGeoTransform(tif.GetGeoTransform())
        out.SetProjection(tif.GetProjection())
        band = [None,None,None]
        oband = [None,None,None]
        band[0] = tif.GetRasterBand(1)
        oband[0] = out.GetRasterBand(1)
        band[1] = tif.GetRasterBand(2)
        oband[1] = out.GetRasterBand(2)
        band[2] = tif.GetRasterBand(3)
        oband[2] = out.GetRasterBand(3)
        nr=numpy.roll
        na=numpy.add
        band=nr(band,(1-refband))
        oband=nr(oband,(1-refband))
        refband2 = None
        readrows = int((((memuse-67)*48036)/xsize)/2)
        oband[0].WriteArray(numpy.repeat(0,xsize*2).reshape(2,-1),0,0)
        arr2 = band[0].ReadAsArray(0, 0, xsize, 4)
        arr3 = band[1].ReadAsArray(0, 0, xsize, 4)
        arr4 = band[2].ReadAsArray(0, 0, xsize, 4)
        for y in range(4, ysize, readrows):
            QCoreApplication.processEvents()
            if ysize-y < readrows : readrows = ysize-y
            arr1 = band[0].ReadAsArray(0, y, xsize, readrows)
            arr1 = numpy.uint32(numpy.vstack((arr2,arr1)))
            arr2 = arr1[readrows:readrows+5,]
            sum=na(na(na(na(na(arr1,nr(arr1,1,1)),nr(arr1,-1,1)),na(nr(nr(arr1,-1,1),-1,0),nr(nr(arr1,-1,1),1,0))),na(nr(nr(arr1,1,1),-1,0),nr(nr(arr1,1,1),1,0))),na(nr(arr1,-1,0),nr(arr1,1,0)))
            sum2=arr1**2
            sum2=na(na(na(na(na(sum2,nr(sum2,1,1)),nr(sum2,-1,1)),na(nr(nr(sum2,-1,1),-1,0),nr(nr(sum2,-1,1),1,0))),na(nr(nr(sum2,1,1),-1,0),nr(nr(sum2,1,1),1,0))),na(nr(sum2,-1,0),nr(sum2,1,0)))
            sum2 = numpy.uint16(numpy.round((sum2-((sum**2)/9.0))/9.0))
            sum = numpy.ubyte(numpy.round((sum/9.0)+0.5))
            sum23=nr(sum2,-2,1)
            t=numpy.vstack((sum2.flatten(),sum23.flatten(),nr(sum2,2,0).flatten(),nr(sum23,2,0).flatten()))
            t=t==numpy.min(t,0)
            sum23=nr(sum,-2,1)
            arr1=nr(nr(numpy.ubyte(numpy.reshape(numpy.max((t)*numpy.vstack((sum.flatten(),sum23.flatten(),nr(sum,2,0).flatten(),nr(sum23,2,0).flatten())),0),(readrows+4,-1))),-1,0),1,1)[2:(readrows+2),2:(xsize-2)]
            oband[0].WriteArray(arr1,2,y-2)
            arr1 = band[1].ReadAsArray(0, y, xsize, readrows)
            arr1 = numpy.uint32(numpy.vstack((arr3,arr1)))
            arr3 = arr1[readrows:readrows+5,]
            sum=numpy.ubyte((na(na(na(na(na(arr1,nr(arr1,1,1)),nr(arr1,-1,1)),na(nr(nr(arr1,-1,1),-1,0),nr(nr(arr1,-1,1),1,0))),na(nr(nr(arr1,1,1),-1,0),nr(nr(arr1,1,1),1,0))),na(nr(arr1,-1,0),nr(arr1,1,0))))/9.0+0.5)
            sum23=nr(sum,-2,1)
            arr1=nr(nr(numpy.ubyte(numpy.reshape(numpy.max((t)*numpy.vstack((sum.flatten(),sum23.flatten(),nr(sum,2,0).flatten(),nr(sum23,2,0).flatten())),0),(readrows+4,-1))),-1,0),1,1)[2:(readrows+2),2:(xsize-2)]
            oband[1].WriteArray(arr1,2,y-2)
            arr1 = band[2].ReadAsArray(0, y, xsize, readrows)
            arr1 = numpy.uint32(numpy.vstack((arr4,arr1)))
            arr4 = arr1[readrows:readrows+5,]
            sum=numpy.ubyte(numpy.round((na(na(na(na(na(arr1,nr(arr1,1,1)),nr(arr1,-1,1)),na(nr(nr(arr1,-1,1),-1,0),nr(nr(arr1,-1,1),1,0))),na(nr(nr(arr1,1,1),-1,0),nr(nr(arr1,1,1),1,0))),na(nr(arr1,-1,0),nr(arr1,1,0))))/9.0)+0.5)
            sum23=nr(sum,-2,1)
            arr1=nr(nr(numpy.ubyte(numpy.reshape(numpy.max((t)*numpy.vstack((sum.flatten(),sum23.flatten(),nr(sum,2,0).flatten(),nr(sum23,2,0).flatten())),0),(readrows+4,-1))),-1,0),1,1)[2:(readrows+2),2:(xsize-2)]
            oband[2].WriteArray(arr1,2,y-2)
            self.dlg.progressBar.setValue(int((100*(y+readrows+4))/ysize))
        out = None
        tif = None
        nova = QMessageBox(self.dlg)
        nova.setText('Completado com sucesso\n em '+str(int((time.clock()-start)/3600))+'h'+str(int((time.clock()-start)/60))+'m'+str((0.5+time.clock()-start)%60)[0:5]+'s')
        if self.dlg.addout.isChecked():
            fileName = str(output)
            fileInfo = QFileInfo(fileName)
            baseName = fileInfo.baseName()
            iface.addRasterLayer(fileName, baseName)
        nova.exec_()
        self.dlg.setCursor(QCursor(Qt.ArrowCursor))
        self.dlg.setEnabled(True)
        self.dlg.close()
    def savefname(self):
        if len(self.outdir) == 0 :
            self.i=0
            while self.layerPath.find('\\', self.i) != -1:
                self.i = self.layerPath.find('\\', self.i)+1
            self.outdir = self.layerPath[0:self.i]
        else:
            self.outpath = self.outdir
        self.dlg.output.setText(QFileDialog.getSaveFileName(self.dlg, 'Select output file', self.outdir, 'TIFF (*.tif);; All files (*.*);;JPEG (*.jpg, *.jpeg)'))
        if len(str(self.dlg.output.text()))>0:
            self.i = 0
            while str(self.dlg.output.text()).find('/', self.i) != -1:
                self.i = str(self.dlg.output.text()).find('/', self.i)+1
            self.outdir = str(self.dlg.output.text())[0:self.i]    
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
            self.dlg.input.clear()
            for (key, layer) in self.ilayers.mapLayers().iteritems():
                if layer.type() == 1:
                    self.dlg.input.addItem(str(layer.name()), key)
            pass
import gdal, numpy, sys
import gdal
import numpy
import sys
from PyQt4.QtCore import QCoreApplication

def dofilter(dlg, input, output, refband=1, memuse=100):
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
        sum = numpy.ubyte((sum/9.0)+0.5)
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
        sum=numpy.ubyte((na(na(na(na(na(arr1,nr(arr1,1,1)),nr(arr1,-1,1)),na(nr(nr(arr1,-1,1),-1,0),nr(nr(arr1,-1,1),1,0))),na(nr(nr(arr1,1,1),-1,0),nr(nr(arr1,1,1),1,0))),na(nr(arr1,-1,0),nr(arr1,1,0))))/9.0+0.5)
        sum23=nr(sum,-2,1)
        arr1=nr(nr(numpy.ubyte(numpy.reshape(numpy.max((t)*numpy.vstack((sum.flatten(),sum23.flatten(),nr(sum,2,0).flatten(),nr(sum23,2,0).flatten())),0),(readrows+4,-1))),-1,0),1,1)[2:(readrows+2),2:(xsize-2)]
        oband[2].WriteArray(arr1,2,y-2)
        dlg.progressBar.setValue(int((100*(y+readrows+4))/ysize))
    out = None
    tif = None
    return True
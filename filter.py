from builtins import str
from builtins import range
import gdal, numpy, sys
from qgis.PyQt.QtCore import QCoreApplication

NUMPY_TYPES = {
    1: numpy.ubyte,
    2: numpy.uint16,
    3: numpy.int16,
    4: numpy.uint32,
    5: numpy.int32,
    6: numpy.float32,
    7: numpy.float64
}

NUMPY_TYPES_1 = {
    1: numpy.uint16,
    2: numpy.uint32,
    3: numpy.int32,
    4: numpy.uint64,
    5: numpy.int64,
    2: numpy.float64,
    3: numpy.float64
}

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
    tif = gdal.Open(str(input), GA_ReadOnly)
    nbands = tif.RasterCount
    driver = tif.GetDriver()
    xsize = tif.RasterXSize
    ysize = tif.RasterYSize
    data_type = tif.GetRasterBand(1).DataType
    out = gdal.GetDriverByName('GTiff').Create(str(output), xsize, ysize, nbands, data_type)
    try:
        out.SetGeoTransform(tif.GetGeoTransform())
        out.SetProjection(tif.GetProjection())
    except:
        pass
    band = [None]*nbands
    oband = [None]*nbands
    for i in range(0,nbands):
        band[i] = tif.GetRasterBand(i+1)
        oband[i] = out.GetRasterBand(i+1)
    tif_numpy_type = NUMPY_TYPES[data_type]
    tif_numpy_upper_type = NUMPY_TYPES_1[data_type]
    nr=numpy.roll
    na=numpy.add
    band=nr(band,(1-refband))
    oband=nr(oband,(1-refband))
    refband2 = None
    readrows = int((((memuse-67)*48036)/xsize)/2)
    oband[0].WriteArray(numpy.repeat(0,xsize*2).reshape(2,-1),0,0)
    arr = [None]*nbands
    for i in range(0,nbands):
        arr[i]=band[i].ReadAsArray(0,0,xsize,4)
    for y in range(4, ysize, readrows):
        QCoreApplication.processEvents()
        if ysize-y < readrows : readrows = ysize-y
        arr1 = band[0].ReadAsArray(0, y, xsize, readrows)
        arr1 = tif_numpy_upper_type(numpy.vstack((arr[0],arr1)))
        arr[0] = arr1[readrows:readrows+5,]
        sum=na(na(na(na(na(arr1,nr(arr1,1,1)),nr(arr1,-1,1)),na(nr(nr(arr1,-1,1),-1,0),nr(nr(arr1,-1,1),1,0))),na(nr(nr(arr1,1,1),-1,0),nr(nr(arr1,1,1),1,0))),na(nr(arr1,-1,0),nr(arr1,1,0)))
        sum2=arr1**2
        sum2=na(na(na(na(na(sum2,nr(sum2,1,1)),nr(sum2,-1,1)),na(nr(nr(sum2,-1,1),-1,0),nr(nr(sum2,-1,1),1,0))),na(nr(nr(sum2,1,1),-1,0),nr(nr(sum2,1,1),1,0))),na(nr(sum2,-1,0),nr(sum2,1,0)))
        sum2 = tif_numpy_type(numpy.round((sum2-((sum**2)/9.0))/9.0))
        sum = tif_numpy_type((sum/9.0)+0.5)
        sum23=nr(sum2,-2,1)
        t=numpy.vstack((sum2.flatten(),sum23.flatten(),nr(sum2,2,0).flatten(),nr(sum23,2,0).flatten()))
        t=t==numpy.min(t,0)
        sum23=nr(sum,-2,1)
        band_max = band[0].GetMaximum()
        band_min = band[0].GetMinimum()
        arr1=nr(nr(tif_numpy_type(numpy.reshape(numpy.max((t)*numpy.vstack((sum.flatten(),sum23.flatten(),nr(sum,2,0).flatten(),nr(sum23,2,0).flatten())),0),(readrows+4,-1))),-1,0),1,1)[2:(readrows+2),2:(xsize-2)]
        oband[0].WriteArray(arr1,2,y-2)
        dlg.progressBar.setValue(int((100*(y+(readrows)+4))/ysize))
        for i in range(1,nbands):
            arr1 = band[i].ReadAsArray(0, y, xsize, readrows)
            arr1 = tif_numpy_upper_type(numpy.vstack((arr[i],arr1)))
            arr[i] = arr1[readrows:readrows+5,]
            sum = tif_numpy_type((na(na(na(na(na(arr1,nr(arr1,1,1)),nr(arr1,-1,1)),na(nr(nr(arr1,-1,1),-1,0),nr(nr(arr1,-1,1),1,0))),na(nr(nr(arr1,1,1),-1,0),nr(nr(arr1,1,1),1,0))),na(nr(arr1,-1,0),nr(arr1,1,0))))/9.0+0.5)
            sum23 = nr(sum,-2,1)
            band_max = band[i].GetMaximum()
            band_min = band[i].GetMinimum()
            arr1=nr(nr(tif_numpy_type(numpy.reshape(numpy.max((t)*numpy.vstack((sum.flatten(),sum23.flatten(),nr(sum,2,0).flatten(),nr(sum23,2,0).flatten())),0),(readrows+4,-1))),-1,0),1,1)[2:(readrows+2),2:(xsize-2)]
            oband[i].WriteArray(arr1,2,y-2)
            dlg.progressBar.setValue(int((100*(y+(((i+1)*readrows)/nbands)+4))/ysize))
    out = None
    tif = None
    return True

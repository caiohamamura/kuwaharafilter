from builtins import zip
from builtins import range
import numpy, sys
import numpy as np
import threading
from time import time, sleep
from datetime import timedelta
import queue
import math
import pyopencl as cl
from pyopencl import array
try:
    from .kuwahara_filter_c_opencl import cSrc
except:
    from kuwahara_filter_c_opencl import cSrc

"""
This is the algorithm for Kuwahara Filter using OpenCL devices
The algorithm works with separate threads. It contains 4 classes (+) and two buffers (-):
 - inBuffer: buffer chunks of data received from raster reading
 
 - outBuffer: buffer chunks of resulting data from filtering

 + RasterLoader: Load raster chunks and data to inBuffer (1 thread)
 
 + ProcessingUnit: Loads data from inBuffer to execute in the OpenCL kernels and capture its results to outBuffer (1 thread for each OpenCL device)
 
 + ProcessingBag: Manage ProcessingUnit(s) creating a thread for each device and handling the buffers to signal that processing has ended (in the main thread).
 
 + RasterWriter: Load resulting chunks from outBuffer and writes to output raster (1 thread) 

 Context: 
 
 The buffer mentioned here are simply main memory space allocated to store temporary data.

 Since we don't know before hand IO vs processing speed, inBuffer may store data from RasterReader to deliver as soon as a ProcessingUnit is available. Writing to raster output may also be a bottleneck, so that outBuffer can store the results to write as the RasterWriter is ready.

Though, rasters are often larger than memory, so the inBuffer and outBuffer are limited to store the same number of chunks as the number of devices providing OpenCL framework, as a suposition that if a host has many devices providing OpenCL (e.g. 4 GPUs) it may as well have larger memory. 
"""


# If opened from console qgis is not necessary
QCoreApplication = None
try:
    from qgis.PyQt.QtCore import QCoreApplication
except:
    pass

class RasterLoader (threading.Thread):
    def __init__(self, tif, xSize, ySize, readrows, numpyType, rasterLock, inBuffer):
        threading.Thread.__init__(self)
        self.tif = tif
        self.xSize = xSize
        self.ySize = ySize
        self.readrows = readrows
        self.numpyType = numpyType
        self.rasterLock = rasterLock
        self.inBuffer = inBuffer
    def run(self):
        nBands = self.tif.RasterCount
        for y in range(2, self.ySize, self.readrows):
            if (QCoreApplication != None): 
                QCoreApplication.processEvents()
            if self.ySize-y < self.readrows : self.readrows = self.ySize-y-2
            self.rasterLock.acquire()
            data = self.tif.ReadAsArray(0, y-2, self.xSize, self.readrows+4)
            self.rasterLock.release()
            self.inBuffer.put([data, y, self.numpyType])
        self.inBuffer.put(False)
        
        


class ProcessingBag:
    def __init__(self, nBands, cType, isFloat):
        # Get opencl devices and count
        devices = [j for i in cl.get_platforms() for j in i.get_devices()]
        self.nDevices = len(devices)
        self.inBuffer = queue.Queue(self.nDevices)
        self.outBuffer = queue.Queue(self.nDevices)
        
        #Create context for each device
        contexts = [cl.Context([device]) for device in devices]

        #Compile the program for each context
        cSrcCode = cSrc.format(nBands, cType, int(isFloat))
        programs = [cl.Program(context, cSrcCode) for context in contexts]
        [program.build() for program in programs]
    
        # Queues for contexts
        queues = [cl.CommandQueue(context) for context in contexts]
        
        

        #Create a processingUnit for each program/context/queue
        self.workerExec = [
            ProcessingUnit(
                programs[i], contexts[i], queues[i], self.inBuffer, self.outBuffer
                ) for i in range(self.nDevices)
                ]
        
        for i in self.workerExec:
            i.start()
    
    def readingFinished(self):
        for i in range(self.nDevices):
            self.inBuffer.put(False)

    def signalProcessingFinished(self):
        self.outBuffer.put(False)

    def waitFinishProcessing(self):
        for i in self.workerExec:
            i.join()
        self.signalProcessingFinished()

        

    
class ProcessingUnit(threading.Thread):
    def __init__(self, program, context, queue, inBuffer, outBuffer):
        threading.Thread.__init__(self)
        self.program = program
        self.context = context
        self.queue = queue
        self.inBuffer = inBuffer
        self.outBuffer = outBuffer
    def run(self):
        item = self.inBuffer.get()
        while (item != False):
            arr, y, numpyType = item

            #Create input buffers for OpenCL kernels
            mem_flags = cl.mem_flags
            matrix_buf = cl.Buffer(self.context, mem_flags.READ_ONLY | mem_flags.COPY_HOST_PTR, hostbuf=arr)
            destination_buf = cl.Buffer(self.context, mem_flags.WRITE_ONLY, arr.nbytes)

            ## Step #10. Deploy the kernel to OpenCL queue
            self.program.kuwahara_filter(self.queue, arr.shape[1:], None, np.uint32(arr.shape[2]), np.uint32(arr.shape[1]), matrix_buf, destination_buf)

            ## Move the kernels output data to host memory
            kuwahara_result = np.ones(arr.shape, dtype=numpyType)
            cl.enqueue_copy(self.queue, kuwahara_result, destination_buf)

            # Put the data into outBuffer for writing in raster
            self.outBuffer.put([kuwahara_result[:, 2:-2, 2:-2], 2, y])
            item = self.inBuffer.get()
        


class RasterWriter (threading.Thread):
    def __init__(self, outTif, outBuffer, rasterLock, isConsole, maxIterations, dlg):
        threading.Thread.__init__(self)
        self.rasterLock = rasterLock
        self.outBuffer = outBuffer
        self.nIteration = 0
        self.isConsole = isConsole
        self.maxIterations = maxIterations
        self.dlg = dlg
        self.outTif = outTif
    def run(self):
        item = self.outBuffer.get()
        nBands = self.outTif.RasterCount
        prevProgress = -1
        while (item != False):
            self.nIteration += 1
            array, xOffset, yOffset = item
            self.rasterLock.acquire()
            for i in range(nBands):
                self.outTif.GetRasterBand(i+1).WriteArray(array[i],xOffset,yOffset)
            self.rasterLock.release()
            if (self.isConsole):
                progress = int(100*self.nIteration/self.maxIterations)
                if (progress > prevProgress):
                    prevProgress = progress
                    print('\r'+str(progress),end='')
            item = self.outBuffer.get()



## Step #4. Create the accelerator program from source code.
## Step #5. Build the program.
## Step #6. Create one or more kernels from the program functions.



NUMPY_TYPES = {
    1: numpy.ubyte,
    2: numpy.uint16,
    3: numpy.int16,
    4: numpy.uint32,
    5: numpy.int32,
    6: numpy.float32,
    7: numpy.float64
}

C_TYPES = {
    1: "unsigned char",
    2: "unsigned short",
    3: "short",
    4: "unsigned int",
    5: "int",
    6: "float",
    7: "double"
}

def dofilter2(dlg, input, output, memUse=512):
    start = time()
    ###########
    # Read info on raster and create output
    ###########
    try:
        from osgeo import gdal
    except ImportError:
        import gdal
    from gdalconst import GA_ReadOnly, GDT_Float32
    gdal.AllRegister()
    memUse = int(memUse)
    tif = gdal.Open(input, GA_ReadOnly)
    nBands = tif.RasterCount
    driver = tif.GetDriver()
    xSize = tif.RasterXSize
    ySize = tif.RasterYSize
    dataType = tif.GetRasterBand(1).DataType
    no_data = tif.GetRasterBand(1).GetNoDataValue()
    out = gdal.GetDriverByName('GTiff').Create(output, xSize, ySize, nBands, dataType)
    if no_data:
        out.GetRasterBand(1).SetNoDataValue(float(no_data))
    try:
        out.SetGeoTransform(tif.GetGeoTransform())
        out.SetProjection(tif.GetProjection())
    except:
        pass
    tifNumpyType = NUMPY_TYPES[dataType]
    cType = C_TYPES[dataType]
    isFloat = dataType > 5
    
    # Calculate size of chunks and iterations needed
    ROWS_PER_CHUNK = int((((memUse-67)*48036)/xSize)/6)
    maxIterations = math.ceil((ySize-2)/ROWS_PER_CHUNK)

    # Create processing stuff
    processingBag = ProcessingBag(nBands, cType, isFloat)
    
    rasterLock = threading.Lock()
    workerWriter = RasterWriter(
        out, processingBag.outBuffer, rasterLock, dlg==None, maxIterations, dlg
        )
    workerWriter.start()
    
    rasterLoader = RasterLoader(
        tif, xSize, ySize, ROWS_PER_CHUNK, tifNumpyType, rasterLock, processingBag.inBuffer
        )
    rasterLoader.start()
    
    prevProgress = 0
    if (dlg != None):
        while (rasterLoader.isAlive()):
            if (QCoreApplication != None): QCoreApplication.processEvents()
            progress = int(100*workerWriter.nIteration/maxIterations)
            if (progress > prevProgress):
                prevProgress = progress
                dlg.progressBar.setValue(progress)
            sleep(0.016)
    
    rasterLoader.join()

    

    # Finished loading
    processingBag.readingFinished()
    processingBag.waitFinishProcessing()
    workerWriter.join()
    progress = 100
    if (dlg == None):
        print('\r'+str(progress),end='')
    else:
        dlg.progressBar.setValue(progress)

    # Close raster writing and reading
    out = None
    tif = None
    del out
    del tif
    print()
    print(timedelta(seconds=round(time()-start)))
    return True



if __name__ == "__main__":
    entrada = sys.argv[1]
    saida = sys.argv[2]
    dofilter2(None, entrada, saida)

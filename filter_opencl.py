import gdal, numpy, sys
import pyopencl as cl
from pyopencl import array
import numpy as np
import threading
from time import time
import queue
import math

nIteration = 0
isLoadingArr1 = True
## Step #1. Obtain an OpenCL platform.
devices = [j for i in cl.get_platforms() for j in i.get_devices()]
nDevices = len(devices)
buffer = queue.Queue(maxsize=nDevices)
bufferResult = queue.Queue(maxsize=nDevices)
contexts = [cl.Context([device]) for device in devices]
threadLock = threading.Lock()

class ArrayLoader (threading.Thread):
    def __init__(self, rasterBand, y, xsize, readrows, numpyType, oBand):
        threading.Thread.__init__(self)
        self.rasterBand = rasterBand
        self.y = y-2
        self.xsize = xsize
        self.readrows = readrows+4
        self.numpyType = numpyType
        self.oBand = oBand
    def run(self):
        global buffer, threadLock
        threadLock.acquire()
        data = self.rasterBand.ReadAsArray(0, self.y, self.xsize, self.readrows)
        threadLock.release()
        buffer.put([data, self.oBand, self.y, self.numpyType])
        
    
class GPUCalculator (threading.Thread):
    def __init__(self, program, context, queue):
        threading.Thread.__init__(self)
        self.program = program
        self.context = context
        self.queue = queue
    def run(self):
        global buffer, bufferResult
        item = buffer.get()
        while (item != False):
            arr, oBand, y, numpyType = item
            mem_flags = cl.mem_flags
            matrix_buf = cl.Buffer(self.context, mem_flags.READ_ONLY | mem_flags.COPY_HOST_PTR, hostbuf=arr)
            destination_buf = cl.Buffer(self.context, mem_flags.WRITE_ONLY, arr.nbytes)

            ## Step #9. Associate the arguments to the kernel with kernel object.
            ## Step #10. Deploy the kernel for device execution.
            self.program.kuwahara_filter(self.queue, arr.shape, None, np.uint32(arr.shape[1]), np.uint32(arr.shape[0]), matrix_buf, destination_buf)

            ## Step #11. Move the kernels output data to host memory.
            kuwahara_result = np.ones(arr.shape, dtype=numpyType)
            cl.enqueue_copy(self.queue, kuwahara_result, destination_buf)
            bufferResult.put([oBand, kuwahara_result[2:-2, 2:-2], 2, y])
            item = buffer.get()
        


class RasterWriter (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        global bufferResult, threadLock, nIteration, MAX_ITERATIONS
        item = bufferResult.get()
        while (item != False):
            oBand, array, xOffset, yOffset = item
            threadLock.acquire()
            oBand.WriteArray(array,xOffset,yOffset)
            nIteration += 1
            print(int(100*nIteration/MAX_ITERATIONS))
            threadLock.release()
            item = bufferResult.get()



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

def dofilter(input, output, memuse=512):
    global isLoadingArr1, arrs, N_BANDS, READROWS, Y_SIZE, bufferResult, MAX_ITERATIONS, buffer
    start_time = time()    
    try:
        from osgeo import gdal
    except ImportError:
        import gdal
    from gdalconst import GA_ReadOnly, GDT_Float32
    gdal.AllRegister()
    w = 5
    w2 = (w+1)/2
    memuse=int(memuse)
    tif = gdal.Open(input, GA_ReadOnly)
    N_BANDS = tif.RasterCount
    driver = tif.GetDriver()
    xsize = tif.RasterXSize
    Y_SIZE = tif.RasterYSize
    data_type = tif.GetRasterBand(1).DataType
    out = gdal.GetDriverByName('GTiff').Create(output, xsize, Y_SIZE, N_BANDS, data_type)
    try:
        out.SetGeoTransform(tif.GetGeoTransform())
        out.SetProjection(tif.GetProjection())
    except:
        pass
    band = [None]*N_BANDS
    oband = [None]*N_BANDS
    for i in range(0,N_BANDS):
        band[i] = tif.GetRasterBand(i+1)
        oband[i] = out.GetRasterBand(i+1)
    tif_numpy_type = NUMPY_TYPES[data_type]
    c_type = C_TYPES[data_type]
    cSrcCode = """
    #define ISFLOAT {1}

    typedef struct  {{
        unsigned char count;
        double mean;
        double m2;
    }} countMeanM2;

    typedef struct  {{
        double mean;
        double m2;
    }} meanM2;
    

    countMeanM2 update(countMeanM2 existingAggregate, {0} newValue) {{
    double val = (double)newValue;
    existingAggregate.count++;
    double delta = val - existingAggregate.mean;
    existingAggregate.mean += delta / existingAggregate.count;
    existingAggregate.m2 += (val - existingAggregate.mean) * delta;
    return existingAggregate;
    }}

    meanM2 calculateVarianceMean({0} *matrix, int x, int y) {{
    {0} *matrixPtr = &matrix[x + (y) * 5];
    meanM2 result;
    countMeanM2 aggregate = {{
        .count = 0,
        .mean = 0.0,
        .m2 = 0.0
    }};
    for (int i = 0; i < 3; i++) {{
        aggregate = update(aggregate, *matrixPtr++);
        aggregate = update(aggregate, *matrixPtr++);
        aggregate = update(aggregate, *matrixPtr);
        matrixPtr += 3;
    }}
    result.mean = aggregate.mean;
    result.m2 = aggregate.m2;
    return result;
    }}

    double calculateKuwahara({0} *matrix) {{
    meanM2 result;
    meanM2 tmpResult = {{
        .mean = 0.0,
        .m2 = -1.0,
    }};
    int subwindowPositions[6] = {{0, 2, 2, 0, 2, 2}};
    int *pointer = subwindowPositions;
    result = calculateVarianceMean(matrix, 0, 0);
    for (int i = 0; i < 3; i++) {{
        tmpResult = calculateVarianceMean(matrix, *pointer++, *pointer++);
        if(tmpResult.m2 < result.m2) {{
            result = tmpResult;
        }}
    }}
    #if (ISFLOAT == 1)
        return result.mean;
    #else
        return result.mean+0.5;
    #endif
    }}

    __kernel void kuwahara_filter(const unsigned int width, const unsigned int height, __global const {0} *matrix, __global {0} *result)
    {{
        int x = get_global_id(1);
        int y = get_global_id(0);
        if (x < 2 || x > (width - 3) || y < 2 || y > (height - 3)) {{
                result[x + y * width] = matrix[x + y * width];
            }} else {{
                {0} matrix5x5[25];
                for (int yi = 0; yi < 5; yi++) {{
                    for (int xi = 0; xi < 5; xi++) {{
                        matrix5x5[xi + yi * 5] = matrix[x - 2 + xi + (y - 2 + yi) * width];
                    }}
                }}
                result[x + y * width] = ({0})(calculateKuwahara(matrix5x5));
            }}
    }}
    """.format(c_type, int(data_type>5))
    programs = [cl.Program(context, cSrcCode) for context in contexts]
    [program.build() for program in programs]

    ## Step #7. Create a command queue for the target device.
    queues = [cl.CommandQueue(context) for context in contexts]
    GPUCalculatorInputs = zip(programs, contexts, queues)
    workerExec = [GPUCalculator(program, context, queue) for (program, context, queue) in GPUCalculatorInputs]
    [i.start() for i in workerExec]
    workerWriter = RasterWriter()
    workerWriter.start()
    nr=numpy.roll
    READROWS = int((((memuse-67)*48036)/xsize)/2)
    readrows = READROWS
    #oband[0].WriteArray(numpy.repeat(0,xsize*2).reshape(2,-1),0,0)
    arr = [None]*N_BANDS
    MAX_ITERATIONS = N_BANDS*math.ceil((Y_SIZE-2)/READROWS)
    n = 0
    for y in range(2, Y_SIZE, READROWS):
        for i in range(0, N_BANDS):
            if Y_SIZE-y < READROWS : readrows = Y_SIZE-y-2
            thread0 = ArrayLoader(band[i], y, xsize, readrows, tif_numpy_type, oband[i])
            thread0.start()
            thread0.join()
    [buffer.put(False) for i in range(nDevices)]
    [i.join() for i in workerExec]
    bufferResult.put(False)
    workerWriter.join()
    out = None
    tif = None
    del out
    del tif
    elapsed_time = time() - start_time
    print(elapsed_time)
    return True



if __name__ == "__main__":
    entrada = sys.argv[1]
    saida = sys.argv[2]
    dofilter(entrada, saida)

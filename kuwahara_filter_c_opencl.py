cSrc="""
#define IN_DATA_TYPE {0}
#define ISFLOAT {1}
#if (ISFLOAT == 1)
    #define ROUNDOFFSET 
#else
    #define ROUNDOFFSET +0.5
#endif

#define SMALLERVAR(X) tmp=subwindowStatistics[X];if (tmp.var < resultStats.var) resultStats = tmp

typedef struct  {{
    unsigned char count;
    double mean;
    double var;
}} countVarMeanStruct;

// Welford's Online algorithm
void update(countVarMeanStruct *existingAggregate, IN_DATA_TYPE newValue) {{
    double val = (double)newValue;
    existingAggregate->count++;
    double delta = val - existingAggregate->mean;
    existingAggregate->mean += delta / existingAggregate->count;
    existingAggregate->var += (val - existingAggregate->mean) * delta;
    return;
}}

__kernel void kuwahara_filter(const unsigned int width, const unsigned int height, __global const IN_DATA_TYPE *matrix, __global IN_DATA_TYPE *result)
{{
    int x = get_global_id(1);
    int y = get_global_id(0);

    //If in matrix borders skip and retain original value
    if (x < 2 || x > (width - 3) || y < 2 || y > (height - 3)) {{
            result[x + y * width] = matrix[x + y * width];
        }} else {{
            const __global IN_DATA_TYPE *matrixPointer;
            countVarMeanStruct subwindowStatistics[4];
            matrixPointer = &matrix[x - 2 + (y - 2) * width];
            const int nextRowOffset = width-4;

            subwindowStatistics[0].count = 0;
            subwindowStatistics[0].var = 0;
            subwindowStatistics[0].mean = 0;
            subwindowStatistics[1].count = 0;
            subwindowStatistics[1].var = 0;
            subwindowStatistics[1].mean = 0;
            subwindowStatistics[2].count = 0;
            subwindowStatistics[2].var = 0;
            subwindowStatistics[2].mean = 0;
            subwindowStatistics[3].count = 0;
            subwindowStatistics[3].var = 0;
            subwindowStatistics[3].mean = 0;

            // First row
            update(&subwindowStatistics[0], *matrixPointer++);
            update(&subwindowStatistics[0], *matrixPointer++);
            update(&subwindowStatistics[0], *matrixPointer);
            update(&subwindowStatistics[1], *matrixPointer++);
            update(&subwindowStatistics[1], *matrixPointer++);
            update(&subwindowStatistics[1], *matrixPointer);

            // Second row
            matrixPointer += nextRowOffset;
            update(&subwindowStatistics[0], *matrixPointer++);
            update(&subwindowStatistics[0], *matrixPointer++);
            update(&subwindowStatistics[0], *matrixPointer);
            update(&subwindowStatistics[1], *matrixPointer++);
            update(&subwindowStatistics[1], *matrixPointer++);
            update(&subwindowStatistics[1], *matrixPointer);

            // Third row
            matrixPointer += nextRowOffset;
            update(&subwindowStatistics[0], *matrixPointer);
            update(&subwindowStatistics[2], *matrixPointer++);
            update(&subwindowStatistics[0], *matrixPointer);
            update(&subwindowStatistics[2], *matrixPointer++);
            update(&subwindowStatistics[0], *matrixPointer);
            update(&subwindowStatistics[1], *matrixPointer);
            update(&subwindowStatistics[2], *matrixPointer);
            update(&subwindowStatistics[3], *matrixPointer++);
            update(&subwindowStatistics[1], *matrixPointer);
            update(&subwindowStatistics[3], *matrixPointer++);
            update(&subwindowStatistics[1], *matrixPointer);
            update(&subwindowStatistics[3], *matrixPointer);
            matrixPointer += nextRowOffset;

            // Fourth row
            update(&subwindowStatistics[2], *matrixPointer++);
            update(&subwindowStatistics[2], *matrixPointer++);
            update(&subwindowStatistics[2], *matrixPointer);
            update(&subwindowStatistics[3], *matrixPointer++);
            update(&subwindowStatistics[3], *matrixPointer++);
            update(&subwindowStatistics[3], *matrixPointer);

            // Last row
            matrixPointer += nextRowOffset;
            update(&subwindowStatistics[2], *matrixPointer++);
            update(&subwindowStatistics[2], *matrixPointer++);
            update(&subwindowStatistics[2], *matrixPointer);
            update(&subwindowStatistics[3], *matrixPointer++);
            update(&subwindowStatistics[3], *matrixPointer++);
            update(&subwindowStatistics[3], *matrixPointer);

            countVarMeanStruct resultStats;
            countVarMeanStruct tmp;
            resultStats = subwindowStatistics[0];
            SMALLERVAR(1);
            SMALLERVAR(2);
            SMALLERVAR(3);

            //printf("%f \\n", resultStats.mean);
            result[x + y * width] = (IN_DATA_TYPE)resultStats.mean ROUNDOFFSET;
        }}
}}"""
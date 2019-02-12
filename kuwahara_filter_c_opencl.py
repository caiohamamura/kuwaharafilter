cSrc="""
#define NBANDS {0}
#define IN_DATA_TYPE {1}
#define ISFLOAT {2}
#if (ISFLOAT == 1)
    #define ROUNDOFFSET 
#else
    #define ROUNDOFFSET +0.5
#endif


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
    const int x = get_global_id(1);
    const int y = get_global_id(0);
    const int bandOffset = height * width;
    const int index = y * width + x;

    if (x < 2 || x > (width - 3) || y < 2 || y > (height - 3)) {{
        for (int i = 0; i < NBANDS; i++) {{
            result[index + bandOffset*i] = matrix[index + bandOffset*i];
        }}
    }} else {{
        countVarMeanStruct subwindowStatistics[NBANDS][4];
        countVarMeanStruct *subwindowStatistics0;
        countVarMeanStruct *subwindowStatistics1;
        countVarMeanStruct *subwindowStatistics2;
        countVarMeanStruct *subwindowStatistics3;
        const __global IN_DATA_TYPE *matrixPointer;
        const int nextRowOffset = width-4;
        double (vars[4]) = {{0.0, 0.0, 0.0, 0.0}};
        for (int i = 0; i < NBANDS; i++) {{
            int index00 = index - 2 - 2 * width + bandOffset * i;
            matrixPointer = &matrix[index00];
            result[index] = matrix[index];
            
            subwindowStatistics[i][0].count = 0;
            subwindowStatistics[i][0].var = 0;
            subwindowStatistics[i][0].mean = 0;
            subwindowStatistics[i][1].count = 0;
            subwindowStatistics[i][1].var = 0;
            subwindowStatistics[i][1].mean = 0;
            subwindowStatistics[i][2].count = 0;
            subwindowStatistics[i][2].var = 0;
            subwindowStatistics[i][2].mean = 0;
            subwindowStatistics[i][3].count = 0;
            subwindowStatistics[i][3].var = 0;
            subwindowStatistics[i][3].mean = 0;
            subwindowStatistics0 = &subwindowStatistics[i][0];
            subwindowStatistics1 = &subwindowStatistics[i][1];
            subwindowStatistics2 = &subwindowStatistics[i][2];
            subwindowStatistics3 = &subwindowStatistics[i][3];

            // First row
            update(subwindowStatistics0, *matrixPointer++);
            update(subwindowStatistics0, *matrixPointer++);
            update(subwindowStatistics0, *matrixPointer);
            update(subwindowStatistics1, *matrixPointer++);
            update(subwindowStatistics1, *matrixPointer++);
            update(subwindowStatistics1, *matrixPointer);

            // Second row
            matrixPointer += nextRowOffset;
            update(subwindowStatistics0, *matrixPointer++);
            update(subwindowStatistics0, *matrixPointer++);
            update(subwindowStatistics0, *matrixPointer);
            update(subwindowStatistics1, *matrixPointer++);
            update(subwindowStatistics1, *matrixPointer++);
            update(subwindowStatistics1, *matrixPointer);

            // Third row
            matrixPointer += nextRowOffset;
            update(subwindowStatistics0, *matrixPointer);
            update(subwindowStatistics2, *matrixPointer++);
            update(subwindowStatistics0, *matrixPointer);
            update(subwindowStatistics2, *matrixPointer++);
            update(subwindowStatistics0, *matrixPointer);
            update(subwindowStatistics1, *matrixPointer);
            update(subwindowStatistics2, *matrixPointer);
            update(subwindowStatistics3, *matrixPointer++);
            update(subwindowStatistics1, *matrixPointer);
            update(subwindowStatistics3, *matrixPointer++);
            update(subwindowStatistics1, *matrixPointer);
            update(subwindowStatistics3, *matrixPointer);
            matrixPointer += nextRowOffset;

            // Fourth row
            update(subwindowStatistics2, *matrixPointer++);
            update(subwindowStatistics2, *matrixPointer++);
            update(subwindowStatistics2, *matrixPointer);
            update(subwindowStatistics3, *matrixPointer++);
            update(subwindowStatistics3, *matrixPointer++);
            update(subwindowStatistics3, *matrixPointer);

            // Last row
            matrixPointer += nextRowOffset;
            update(subwindowStatistics2, *matrixPointer++);
            update(subwindowStatistics2, *matrixPointer++);
            update(subwindowStatistics2, *matrixPointer);
            update(subwindowStatistics3, *matrixPointer++);
            update(subwindowStatistics3, *matrixPointer++);
            update(subwindowStatistics3, *matrixPointer);

            vars[0] += subwindowStatistics0->var / 9;                       
            vars[1] += subwindowStatistics1->var / 9;
            vars[2] += subwindowStatistics2->var / 9;
            vars[3] += subwindowStatistics3->var / 9;
        }}
        int tmpBestVar = vars[0];
        int bestVarIndex = 0;
        if (vars[1] < tmpBestVar) {{
            tmpBestVar = vars[1];
            bestVarIndex = 1;
        }}
        if (vars[2] < tmpBestVar) {{
            tmpBestVar = vars[2];
            bestVarIndex = 2;
        }}
        if (vars[3] < tmpBestVar) {{
            tmpBestVar = vars[3];
            bestVarIndex = 3;
        }}
        for (int i = 0; i < NBANDS; i++) {{
            result[index+i*bandOffset] = (IN_DATA_TYPE)subwindowStatistics[i][bestVarIndex].mean;
        }}  
    }}   
}}"""
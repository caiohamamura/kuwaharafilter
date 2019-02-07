cSrc="""
#define ISFLOAT {1}

typedef struct  {{
    unsigned char count;
    double mean;
    double var;
}} countVarMeanStruct;

typedef struct  {{
    double mean;
    double var;
}} varMeanStruct;

// Welford's Online algorithm
countVarMeanStruct update(countVarMeanStruct existingAggregate, {0} newValue) {{
    double val = (double)newValue;
    existingAggregate.count++;
    double delta = val - existingAggregate.mean;
    existingAggregate.mean += delta / existingAggregate.count;
    existingAggregate.var += (val - existingAggregate.mean) * delta;
    return existingAggregate;
}}

varMeanStruct subwindowVarianceMean({0} *matrix, int x, int y) {{
    {0} *matrixPtr = &matrix[x + (y) * 5];
    varMeanStruct result;
    countVarMeanStruct aggregate = {{
        .count = 0,
        .mean = 0.0,
        .var = 0.0
    }};

    // Calculate variance and mean with Welford's Online algorithm
    for (int i = 0; i < 3; i++) {{
        aggregate = update(aggregate, *matrixPtr++);
        aggregate = update(aggregate, *matrixPtr++);
        aggregate = update(aggregate, *matrixPtr);
        matrixPtr += 3;
    }}
    result.mean = aggregate.mean;
    result.var = aggregate.var;
    return result;
    }}

{0} meanFromLeastVariance({0} *matrix) {{
    varMeanStruct varMean;
    varMeanStruct tmpVarMean = {{
        .mean = 0.0,
        .var = -1.0,
    }};

    //Pairs of subwindow position y, x indexes
    int subwindowPositions[6] = {{0, 2, 2, 0, 2, 2}};
    int *pointer = subwindowPositions;
    varMean = subwindowVarianceMean(matrix, 0, 0);
    for (int i = 0; i < 3; i++) {{
        tmpVarMean = subwindowVarianceMean(matrix, *pointer++, *pointer++);
        
        if(tmpVarMean.var < varMean.var) {{
            varMean = tmpVarMean;
        }}
    }}

    #if (ISFLOAT == 1)
        return ({0})varMean.mean;
    #else
        return ({0})(varMean.mean+0.5);
    #endif
    }}

__kernel void kuwahara_filter(const unsigned int width, const unsigned int height, __global const {0} *matrix, __global {0} *result)
{{
    int x = get_global_id(1);
    int y = get_global_id(0);

    //If in matrix borders skip and retain original value
    if (x < 2 || x > (width - 3) || y < 2 || y > (height - 3)) {{
            result[x + y * width] = matrix[x + y * width];
        }} else {{

            // Fill 5x5 kernel to pass to meanFromLeastVariance
            {0} matrix5x5[25];
            for (int yi = 0; yi < 5; yi++) {{
                for (int xi = 0; xi < 5; xi++) {{
                    matrix5x5[xi + yi * 5] = matrix[x - 2 + xi + (y - 2 + yi) * width];
                }}
            }}

            result[x + y * width] = meanFromLeastVariance(matrix5x5);
        }}
}}"""
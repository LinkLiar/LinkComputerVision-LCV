import numpy as np
import numba
from numba import njit

BINARY_WHITE = 255
BINARY_BLACK = 0


@njit
def _GetArround(src, row, col, around):
    around[0] = src[row-1, col -
                    1] if ((row-1 >= 0) & (col-1 >= 0)) else BINARY_WHITE
    around[1] = src[row-1, col] if (row-1 >= 0) else BINARY_WHITE
    around[2] = src[row-1, col +
                    1] if ((row-1 >= 0) & (col+1 < src.shape[1])) else BINARY_WHITE
    around[3] = src[row, col+1] if (col+1 < src.shape[1]) else BINARY_WHITE
    around[4] = src[row+1, col +
                    1] if ((row+1 < src.shape[0]) & (col+1 < src.shape[1])) else BINARY_WHITE
    around[5] = src[row+1, col] if (row+1 < src.shape[0]) else BINARY_WHITE
    around[6] = src[row+1, col -
                    1] if ((row+1 < src.shape[0]) & (col-1 >= 0)) else BINARY_WHITE
    around[7] = src[row, col-1] if (col-1 >= 0) else BINARY_WHITE


@njit
def thin(frame):
    height = frame.shape[0]
    width = frame.shape[1]

    kernal = [[2, 0, 2, 0, 2, 2, 1, 1],
              [1, 2, 2, 0, 2, 0, 2, 1],
              [1, 2, 0, 0, 2, 2, 1, 1],
              [1, 2, 2, 0, 0, 2, 1, 1]]

    while(True):
        doneFlag = True
        for i in range(4):
            needEraseList = []
            for j in range(4):
                sel = [0]*8
                for m in range(8):
                    sel[m] = kernal[j][(2*i+m) % 8]

                for row in range(height):
                    for col in range(width):
                        pv = frame[row, col]
                        if (pv == BINARY_WHITE):
                            continue
                        around = [0] * 8
                        _GetArround(frame, row, col, around)
                        needErase = 1
                        for k in range(8):
                            if((sel[k] == 0) & (around[k] == BINARY_WHITE)):
                                needErase = False
                                break
                            elif ((sel[k] == 1) & (around[k] != BINARY_WHITE)):
                                needErase = False
                                break
                        if(needErase & ((row, col) not in needEraseList)):
                            needEraseList.append((row, col))

            if(len(needEraseList)):
                for cl in range(len(needEraseList)):
                    frame[needEraseList[cl][0],
                          needEraseList[cl][1]] = BINARY_WHITE
                doneFlag = False
                needEraseList.clear()
            else:
                break

        if(doneFlag):
            break

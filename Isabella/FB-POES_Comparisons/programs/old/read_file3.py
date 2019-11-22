import numpy as np

filename3 = 'FU3-col.txt'
def read_file3(filename3):
    colList = []
    try:
        file = open(filename3, 'r')
    except:
        print('The file may not exist or the program may have not have been able to open it.')
        return([])
    else:
        file = open(filename3, 'r')
        for line in file:
            line = line.strip().split(',')
            print(line[0])
            colList.append(line[0])
    file.close()
    colArray = np.array(colList, dtype=float)
    print('colArray')
    print(colArray)
    return colArray

def midpoints(colArray):
    midpointArray = np.zeros((98), dtype=float)
    n = 0
    print(colArray.shape)
    print(type(midpointArray))

    print(colArray[0] + colArray[1])
    print(colArray[1] + colArray[2])
    while n < 98:
        midpointArray[n] = (np.divide((colArray[n] + colArray[n+1]), 2.))
        n += 1
    print(midpointArray)
    
def main():
    col_array = read_file3(filename3)
    midpoints(col_array)

main()    
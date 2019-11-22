import numpy as np
'''
testList = [6.0, 8.0, 9.0, 6.0, 7.0, 0.0, 0.0, 2.0, 3.0]
print('this is testList')
print(testList)
completeList = []

testArray = np.array(testList)
print('this is testArray')
print(testArray)

average = np.mean(testArray)
print(average)

averageB = sum(testArray)/len(testArray)
print(averageB)

testArray[testArray==0] = np.nan
print('this is nan testArray')
print(testArray)

average = np.nanmean(testArray)
print(average)

averageB = sum(testArray)/len(testArray)
print(averageB)

a = [0., 0., 0., 0., 0.]
all_zeros = not np.any(a)
print(all_zeros)

if all_zeros == True:
    print('only zeros')
else:
    print('nope')
    
if all([v == 0 for v in a]):
    print('indeed they are') 
'''

xList = [0., 0., 0., 0., 0., 0.]
yList = [1., 2., 3., 4., 5., 6.]
zList = [1., 0., 3., 0., 5., 0.]

xArray = np.array(xList)
yArray = np.array(yList)
zArray = np.array(zList)

print(xArray)
print(yArray)
print(zArray)

all_zerosX = not np.any(xArray)
if all_zerosX == True:
    print('all zeros')
    xArray = np.mean(xArray)
    print(xArray)
else:
    print('this is xAverage')
    xArray[xArray==0] = np.nan
    xAverage = np.nanmean(xArray)
    print('this is xAverage')
    print(xAverage)

all_zerosY = not np.any(yArray)    
if all_zerosY == True:
    print('all zeros')
    print(yArray)
else:
    print('this is yAverage')
    yArray[yArray==0] = np.nan
    yAverage = np.nanmean(yArray)
    print(yAverage)

all_zerosZ = not np.any(zArray)    
if all_zerosZ == True:
    print('all zeros')
    print(zArray)
else:
    print('this is zAverage')
    zArray[zArray==0] = np.nan
    zAverage = np.nanmean(zArray)
    ('this is zAverage')
    print(zAverage)

'''
xArray[xArray==0] = np.nan
yArray[yArray==0] = np.nan
zArray[zArray==0] = np.nan
'''

print(xArray)
print(yArray)
print(zArray)

all_nan = not np.any(xArray)
if all_nan == True:
    print('yes')



















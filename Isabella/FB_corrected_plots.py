'''
Filename: 
    FB_corrected_plots.py
    
Author: 
    Isabella M. Householder
    
Synopsis:
    Create corrected FIREBIRD plots (energetic electron counts vs time)
    
Date:
    21 May 2019
    
Description:
    Read in FIREBIRD files as comma separated plain text (.txt) saved from Autoplot
    ............
    Plot for comparison with counts on y-axis and time on x-axis
    
-------------------------------------------------------------------------------
'''

import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

filename = 'test.txt'

#------------------ reads in file and creates dict from data ------------------
def read_initial_data(filename):
    data = {}
    try:
        file = open(filename, 'r')
    except:
        print('The file may not exist or the program may have not have been able to open it.')
        return({})
    else:
        file = open(filename, 'r')
        xList = []
        yList = []
        yValues = []
        nline = 0
        for line in file:
            nline += 1
            line = line.strip().split(',')
            if len(line) == 7:
                data[line[0]] = {'col_counts_0':float(line[1]),
                    'col_counts_1':float(line[2]),
                    'col_counts_2':float(line[3]),
                    'col_counts_3':float(line[4]),
                    'col_counts_4':float(line[5]),
                    'col_counts_5':float(line[6])}
                
                
            datetime_str = line[0]
            y = data[line[0]]
            yList.append(y) 
            xList.append(dt.datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%fZ'))
        file.close()
        
        file = open(filename, 'r')
        yArray = np.zeros([nline, 6])
        nline = 0
        for col_vals in file: 
            col_vals = col_vals.strip().split(',')
            yArray[nline,0] = float(col_vals[1])
            yArray[nline,1] = float(col_vals[2])
            yArray[nline,2] = float(col_vals[3])
            yArray[nline,3] = float(col_vals[4])
            yArray[nline,4] = float(col_vals[5])
            yArray[nline,5] = float(col_vals[6])
            nline += 1
        
        xArray = np.array(xList)
        
        print('this is xarray')
        print(xArray)
        print('\n')
        print('yarray')
        print(yArray)
        print('\n')
        print('yvalues')
        print(yValues)
        
        file.close()
        return data, xArray, yArray


#------------------------ plots FB counts vs time -----------------------------
def plot_data(data, xArray, yArray):
    
    plt.figure()
    
    plt.suptitle('FIREBIRD Energetic Electron Counts vs. Time (corrected)', fontsize=12)
    plt.xlabel('September 18, 2018', fontsize=10)
    plt.ylabel('Electron Counts per Timestep (cadence = 0.05 sec)', fontsize=10)
    
    lines = plt.plot(xArray, yArray[:,0], xArray, yArray[:,1], xArray, yArray[:,2], xArray, yArray[:,3], xArray, yArray[:,4], xArray, yArray[:,5], '-' )
    plt.setp(lines[0], linewidth=0.5, color='#A51D00')
    plt.setp(lines[1], linewidth=0.5, color='y')
    plt.setp(lines[2], linewidth=0.5, color='#008C0D')
    plt.setp(lines[3], linewidth=0.5, color='#00C7BE')
    plt.setp(lines[4], linewidth=0.5, color='#0500A0')
    plt.setp(lines[5], linewidth=0.5, color='#9B0091')
    
    plt.legend(('251.5 keV', '333.5 keV', '452.0 keV', '620.5 keV', '852.8 keV', '>984 keV'), loc='upper right')
    
    plt.show()

def main():
    d, x, y = read_initial_data(filename)
    plot_data(d, x, y)
    
main()

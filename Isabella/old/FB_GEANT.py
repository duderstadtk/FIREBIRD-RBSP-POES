'''
Filename: 
    GEANT.py
    
Author: 
    Isabella M. Householder
    
Synopsis:
    text here
    
Date:
    21 June 2019
    
Description:
    text here
    
-------------------------------------------------------------------------------
'''

import numpy as np
import matplotlib.pyplot as plt

filename = 'FU3-col.txt'

#------------------ reads in file and creates dict from data ------------------
def read_geant_data(filename):
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
        nline = 0
        for line in file:
            nline += 1
            line = line.strip().split(',')
            if len(line) == 8:
                data[line[0]] = {'nInBin':int(line[1]),
                    'nChan0':int(line[2]),
                    'nChan1':int(line[3]),
                    'nChan2':int(line[4]),
                    'nChan3':int(line[5]),
                    'nChan4':int(line[6]),
                    'nChan5':int(line[7])}
                
            IncEnergyBinStartMeV = float(line[0])
            y = data[line[0]]
            yList.append(y)
            xList.append(IncEnergyBinStartMeV)  
        file.close()
        
        NList = []
        file = open(filename, 'r')
        #NArray = np.zeros([nline])
        nline = 0
        for N_vals in file:
            N_vals = N_vals.strip().split(',')
            #NArray[nline] = int(N_vals[1])
            NList.append(float(N_vals[1]))
            nline += 1
        NArray = np.array(NList)
        file.close()
        
        file = open(filename, 'r')
        xArray = np.zeros([nline, 1])
        nArray = np.zeros([nline, 6])
        nline = 0
        for x_col_vals in file:
            x_col_vals = x_col_vals.strip().split(',')
            xArray[nline,0] = float(x_col_vals[0])
            nline += 1
        xArray = np.array(xList)  
        nline = 0
        file.close()
        
        
        file = open(filename, 'r')
        for n_vals in file:
            n_vals = n_vals.strip().split(',')
            nArray[nline,0] = float(n_vals[2])
            nArray[nline,1] = float(n_vals[3])
            nArray[nline,2] = float(n_vals[4])
            nArray[nline,3] = float(n_vals[5])
            nArray[nline,4] = float(n_vals[6])
            nArray[nline,5] = float(n_vals[7])
            nline += 1
        file.close()
        
        return data, xArray, nArray, NArray, nline
    
#-------------------------- calculates geometric factor -----------------------

def calculate_G(nArray, NArray, nline, xArray):
    r = 25          ##cm (radius arbitrarily chosen)        
    
    #Gfactor = np.zeros([nline, 6])
    n0 = nArray[:,0]
    n1 = nArray[:,1]
    n2 = nArray[:,2]
    n3 = nArray[:,3]
    n4 = nArray[:,4]
    n5 = nArray[:,5]
    
    Gfactor0 = np.array((n0 / NArray) * 4 * (np.pi ** 2 ) * (r ** 2))
    print(Gfactor0)
    Gfactor1 = np.array((n1 / NArray) * 4 * (np.pi ** 2 ) * (r ** 2))
    Gfactor2 = np.array((n2 / NArray) * 4 * (np.pi ** 2 ) * (r ** 2))
    Gfactor3 = np.array((n3 / NArray) * 4 * (np.pi ** 2 ) * (r ** 2))
    Gfactor4 = np.array((n4 / NArray) * 4 * (np.pi ** 2 ) * (r ** 2))
    Gfactor5 = np.array((n5 / NArray) * 4 * (np.pi ** 2 ) * (r ** 2))    

    return Gfactor0, Gfactor1, Gfactor2, Gfactor3, Gfactor4, Gfactor5
    
#------------------------ plots geometric factor vs keV -----------------------
def plot_data(xArray, Gfactor0, Gfactor1, Gfactor2, Gfactor3, Gfactor4, Gfactor5):

    xArray = xArray * 1000
    
    plt.figure()
    
    plt.suptitle('Geometric Factor for FU3 Collimated Detector', fontsize=11)
    plt.xlabel('Energy (keV)', fontsize=9)
    plt.ylabel('Geometric Factor (cm^2 sr)', fontsize=9)
    
    lines = plt.plot(xArray, Gfactor0, xArray, Gfactor1, xArray, Gfactor2, xArray, Gfactor3, xArray, Gfactor4, xArray, Gfactor5, '-' )
    plt.setp(lines[0], linewidth=0.5, color='r')
    plt.setp(lines[1], linewidth=0.5, color='y')
    plt.setp(lines[2], linewidth=0.5, color='b')
    plt.setp(lines[3], linewidth=0.5, color='g')
    plt.setp(lines[4], linewidth=0.5, color='#6F4600')
    plt.setp(lines[5], linewidth=0.5, color='k')
    
    plt.show()
    
def main():
    d, x, n, N, line = read_geant_data(filename)
    g0, g1, g2, g3, g4, g5 = calculate_G(n, N, line, x)
    plot_data(x, g0, g1, g2, g3, g4, g5)
    
    #data = calculate_G(n, N, line, x)
    #np.savetxt('FU3_Gfactors.txt', np.column_stack(calculate_G(data)), fmt='%s', delimiter=', ')    
    
main()
            
            
            

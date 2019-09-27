'''
Filename: 
    FB_flux_estimate.py
    
Author: 
    Isabella M. Householder
    
Synopsis:
    text here
    
Date:
    05 September 2019
    
Description:
    text here
    
-------------------------------------------------------------------------------
'''

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
#import datetime

filename1 = 'FU3_Gfactors.txt'
filename2 = 'IMH_example_averages.txt'
filename3 = 'FU3-col.txt'

def read_file1(filename1):
    GfactorList = []
    try:
        file = open(filename1, 'r')
    except:
        print('The file may not exist or the program may have not have been able to open it.')
        return([])
    else:
        file = open(filename1, 'r')
        for line in file:
            line = line.strip().split(',')
            GfactorList.append(line)
    file.close()
    return GfactorList

def read_file2(filename2):
    countList = []
    try:
        file = open(filename2, 'r')
    except:
        print('The file may not exist or the program may have not have been able to open it.')
        return([])
    else:
        file = open(filename2, 'r')
        for line in file:
            line = line.strip().split(',')
            countList.append(line)
    file.close()
    return countList

def calculate_flux(GfactorList, countList):
    cadence = 0.05
    G = 6.0
    timestepList = []
    counts0 = []
    counts1 = []
    counts2 = []
    counts3 = []
    counts4 = []
    #counts5 = []
    
    #---- FU3 ----
    '''
    channel_width = np.array([68.7, 107.9, 147.2, 215.9, 284.5])
    '''

    #---- FU4 ----
    channel_width = np.array([63.7, 100.2, 136.7, 200.4, 264.25])  
    
    for row in countList:
        print(row)
        timestepList.append(row[0])
        counts0.append(row[1])
        counts1.append(row[2])
        counts2.append(row[3])
        counts3.append(row[4])
        counts4.append(row[5])
    
    counts0 = np.array(counts0, dtype=float)
    counts1 = np.array(counts1, dtype=float)
    counts2 = np.array(counts2, dtype=float)
    counts3 = np.array(counts3, dtype=float)
    counts4 = np.array(counts4, dtype=float)
    
    '''
    print('counts0')
    print(counts0)
    print('counts1')
    print(counts1)
    print('counts2')
    print(counts2)
    print('counts3')
    print(counts3)
    print('counts4')
    print(counts4)
    '''
    
    flux0 = counts0 / (cadence * G * channel_width[0])
    flux1 = counts1 / (cadence * G * channel_width[1])
    flux2 = counts2 / (cadence * G * channel_width[2])
    flux3 = counts3 / (cadence * G * channel_width[3])
    flux4 = counts4 / (cadence * G * channel_width[4])
    
    ntimesteps = np.size(flux0)
    print('timesteps')
    print(ntimesteps)
    
    fluxArray = np.zeros((ntimesteps, 5), dtype=float)
    fluxArray[:,0] = flux0
    fluxArray[:,1] = flux1
    fluxArray[:,2] = flux2
    fluxArray[:,3] = flux3
    fluxArray[:,4] = flux4
    
    '''
    print('flux0')
    print(flux0)
    print('flux1')
    print(flux1)
    print('flux2')
    print(flux2)
    print('flux3')
    print(flux3)
    print('flux4')
    print(flux4)
    '''


    return flux0, flux1, flux2, flux3, flux4, fluxArray
    #flux=counts/(cadence*G*channel_width_keV) --> flux calculation formula
'''
def testfunc(E, J0, E0):
    return
'''

def func(E, J0, E0):
    return J0 * np.exp(-E/E0)

def midpoints(filename3):
    pass
    
def main():
    
    #---- FU3 ----
    '''
    channel_width = np.array([68.7, 107.9, 147.2, 215.9, 284.5])
    channel_middles = np.array([265.4, 353.7, 481.2, 662.7, 913.0])
    '''
    #---- FU4 ----
    #channel_width = np.array([63.7, 100.2, 136.7, 200.4, 264.25])   
    channel_middles = np.array([251.5, 333.5, 452.0, 620.5, 852.8], dtype=float)  
    #channel_middles = np.array([100, 120, 150, 155, 200], dtype=float)
    channel_middles = np.divide(channel_middles, 1000.)
    
    Gfactor_var = read_file1(filename1)
    counts_var = read_file2(filename2)
    flux_0, flux_1, flux_2, flux_3, flux_4, flux_array = calculate_flux(Gfactor_var, counts_var)
    
    plt.figure()
    
    plt.suptitle('Energy (keV) vs. Energetic Electron Flux', fontsize=11)
    plt.xlabel('Energy (keV)')
    plt.ylabel('Energetic Electron Flux')
    plt.xticks((channel_middles))
    #plt.xlim(0, 310)
    
    ### find a more general way to do this? ###
    plt.plot(channel_middles[0], flux_0[1], 'rx')
    plt.plot(channel_middles[1], flux_1[1], 'rx')
    plt.plot(channel_middles[2], flux_2[1], 'rx')
    plt.plot(channel_middles[3], flux_3[1], 'rx')
    plt.plot(channel_middles[4], flux_4[1], 'rx')
    
    #---- curve fit ----#
    
    '''
    optimizedParameters, pcov = opt.curve_fit(func, channel_middles, flux_array[1,:])
    print('params')
    print(*optimizedParameters)
    
    plt.plot(channel_middles, func(channel_middles, *optimizedParameters), label='fit')
    '''
    
    print('flux_array[1,:]')
    print(flux_array[1,:])
    print(type(flux_array[1,:]))
    
    print('channel_middles')
    print(channel_middles)
    print(type(channel_middles))
    
    popt, pcov = curve_fit(func, channel_middles, flux_array[1,:])
    print('params')
    print(*popt)
    plt.plot(channel_middles, func(channel_middles, *popt), label='fit')
    
    plt.legend()
    plt.show()
    
main()
        
        






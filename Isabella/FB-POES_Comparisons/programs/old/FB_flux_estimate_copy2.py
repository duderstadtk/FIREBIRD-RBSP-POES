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

def calculate_flux(GfactorList, countList):
    cadence = 0.05
    G = 6.0
    timestepList = []
    counts0 = []
    counts1 = []
    counts2 = []
    counts3 = []
    counts4 = []
    
    #---- FU3 ----
    '''
    channel_width = np.array([68.7, 107.9, 147.2, 215.9, 284.5])
    '''

    #---- FU4 ----
    channel_width = np.array([63.7, 100.2, 136.7, 200.4, 264.25])  
    
    for row in countList:
        #print(row)
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
    
    ## --- measured counts array ---
    
    dim_counts = len(counts0)
    measuredcountsArray = np.zeros((dim_counts, 5), dtype=float)
    measuredcountsArray[:,0] = counts0[:]
    measuredcountsArray[:,1] = counts1[:]  
    measuredcountsArray[:,2] = counts2[:]
    measuredcountsArray[:,3] = counts3[:]
    measuredcountsArray[:,4] = counts4[:]      
    
    ## -------
    
    flux0 = counts0 / (cadence * G * channel_width[0])
    flux1 = counts1 / (cadence * G * channel_width[1])
    flux2 = counts2 / (cadence * G * channel_width[2])
    flux3 = counts3 / (cadence * G * channel_width[3])
    flux4 = counts4 / (cadence * G * channel_width[4])
    
    ntimesteps = np.size(flux0)
    ## there are 3406 timesteps in this file
    
    fluxArray = np.zeros((ntimesteps, 5), dtype=float)
    fluxArray[:,0] = flux0
    fluxArray[:,1] = flux1
    fluxArray[:,2] = flux2
    fluxArray[:,3] = flux3
    fluxArray[:,4] = flux4

    return flux0, flux1, flux2, flux3, flux4, fluxArray, measuredcountsArray
    #flux=counts/(cadence*G*channel_width_keV) --> flux calculation formula

def func(E, J0, E0):
    return J0 * np.exp(-E/E0)

def midpoints(colArray):
    midpointArray = np.zeros((98), dtype=float)
    colwidthArray = np.zeros((98), dtype=float)
    
    n = 0
    while n < 98:
        midpointArray[n] = (np.divide((colArray[n] + colArray[n+1]), 2.))
        colwidthArray[n] = (colArray[n+1] - colArray[n])
        n += 1
    return midpointArray, colwidthArray

def calculate_counts(colwidthArray, GfactorList, J_flux):
    newcountArray = np.zeros((97,5), dtype=float)
    newcountArraySum = np.zeros((5), dtype=float)
    cadence = 0.05
    GfactorArray = np.array(GfactorList, dtype=float)
    
    n = 0
    while n < 97:
        newcountArray[n,0] = J_flux[n] * cadence * GfactorArray[n, 0] * (colwidthArray[n] * 1000.)
        newcountArray[n,1] = J_flux[n] * cadence * GfactorArray[n, 1] * (colwidthArray[n] * 1000.)
        newcountArray[n,2] = J_flux[n] * cadence * GfactorArray[n, 2] * (colwidthArray[n] * 1000.)
        newcountArray[n,3] = J_flux[n] * cadence * GfactorArray[n, 3] * (colwidthArray[n] * 1000.)
        newcountArray[n,4] = J_flux[n] * cadence * GfactorArray[n, 4] * (colwidthArray[n] * 1000.)

        newcountArraySum[0] = newcountArraySum[0] + newcountArray[n,0]
        newcountArraySum[1] = newcountArraySum[1] + newcountArray[n,1]
        newcountArraySum[2] = newcountArraySum[2] + newcountArray[n,2]
        newcountArraySum[3] = newcountArraySum[3] + newcountArray[n,3]
        newcountArraySum[4] = newcountArraySum[4] + newcountArray[n,4]
        n += 1     
        
    return newcountArraySum
    #counts = flux * cadence * Gfactor * colwidth
    
def chi_sqr(measuredcountsArray, newcountArraySum):
    print('this is chi sqr')
    chi_sqr = np.sum((measuredcountsArray[0,:] - newcountArraySum) ** 2)
    return chi_sqr   
    
    
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
    col_var = read_file3(filename3)
    
    flux_0, flux_1, flux_2, flux_3, flux_4, flux_array, measuredcounts_array = calculate_flux(Gfactor_var, counts_var)
    
    midpoint_array, colwidth_array = midpoints(col_var)
    
    
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
    print('flux array')
    print(flux_array)
    print('flux_array[1,:]')
    print(flux_array[1,:])
    print('flux array[2,:]')
    print(flux_array[2,:])
    
    print('channel_middles')
    print(channel_middles)
    
    ## curve fit
    popt, pcov = curve_fit(func, channel_middles, flux_array[0,:])
    
    print('params')
    print(*popt)
    '''
    print('pcov')
    print(pcov)
    #popt, pcov = curve_fit(func, channel_middles, flux_array[2,:])
    print('params 2')
    print(*popt)
    print('pcov2')
    print(pcov)
    '''
    
    #plt.plot(channel_middles, func(channel_middles, *popt), label='fit')
    #plt.plot(midpoint_array, func(midpoint_array, *popt), label='fit')
    
    J_flux = func(midpoint_array, *popt)

    
    plt.plot(midpoint_array, J_flux, label='fit')
  

    
    plt.legend()
    plt.show()
    
    '''
    print('J flux')
    print(J_flux)
    print('J fluxB')
    print(J_fluxB)    
    print('J fluxC')
    print(J_fluxC)
    print('J fluxD')
    print(J_fluxD)
    print('J fluxE')
    print(J_fluxE)   
    '''
    
    newcountarray_sum = calculate_counts(colwidth_array, Gfactor_var, J_flux)

    '''
    print('newcount array sum')
    print(newcountarray_sum)
    print('newcount array sum B')
    print(newcountarray_sumB)
    print('newcount array sum C')
    print(newcountarray_sumC)
    print('newcount array sum D')
    print(newcountarray_sumD)
    print('newcount array sum E')
    print(newcountarray_sumE)
    '''
    
    chi = chi_sqr(measuredcounts_array, newcountarray_sum)
    print(chi)
    
    
## trying to create 2D array for newcountarray_sum
## we still need to interate through each timestep 
    
main()   

## QUESTIONS:
# why are we starting with flux_array[1,:] and not flux_array[0,:]?
# do we need to assign new variables for the popt and pcov tuple? 

        






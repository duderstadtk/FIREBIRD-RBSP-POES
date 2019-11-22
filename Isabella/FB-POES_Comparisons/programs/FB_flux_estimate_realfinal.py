'''
Filename: 
    FB_flux_estimate.py
    
Author: 
    Isabella M. Householder
    
Date:
    05 September 2019
    
Description:
    This program calculates the minimum parameters from the best curve fit of
    FIREBIRD high-resolution data.
    
-------------------------------------------------------------------------------
'''

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from math import log10

filename1 = 'FU3_Gfactors.txt'
filename2 = 'sec-avg_FU3-2018-09-19_0756-0800.txt'
filename3 = 'FU3-col.txt'
outfile = 'flux-params_FU3_2018-09-19_0756-0800.txt'

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
            colList.append(line[0])
    file.close()
    colArray = np.array(colList, dtype=float)
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

    channel_width = np.array([68.7, 107.9, 147.2, 215.9, 284.5])

    '''
    #---- FU4 ----
    channel_width = np.array([63.7, 100.2, 136.7, 200.4, 264.25])  
    '''
    
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
    print('this is ntimesteps')
    print(ntimesteps)
    
    fluxArray = np.zeros((ntimesteps, 5), dtype=float)
    fluxArray[:,0] = flux0
    fluxArray[:,1] = flux1
    fluxArray[:,2] = flux2
    fluxArray[:,3] = flux3
    fluxArray[:,4] = flux4

    return flux0, flux1, flux2, flux3, flux4, fluxArray, measuredcountsArray, timestepList, ntimesteps
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

def calculate_counts(colwidthArray, GfactorList, midpointArray, *popt):
    
    Jflux = func(midpointArray, *popt)
    
    newcountArray = np.zeros((97,5), dtype=float)
    estimatedcountsArray = np.zeros((5), dtype=float)
    cadence = 0.05
    GfactorArray = np.array(GfactorList, dtype=float)
    
    n = 0
    while n < 97:
        newcountArray[n,0] = Jflux[n] * cadence * GfactorArray[n, 0] * (colwidthArray[n] * 1000.)
        newcountArray[n,1] = Jflux[n] * cadence * GfactorArray[n, 1] * (colwidthArray[n] * 1000.)
        newcountArray[n,2] = Jflux[n] * cadence * GfactorArray[n, 2] * (colwidthArray[n] * 1000.)
        newcountArray[n,3] = Jflux[n] * cadence * GfactorArray[n, 3] * (colwidthArray[n] * 1000.)
        newcountArray[n,4] = Jflux[n] * cadence * GfactorArray[n, 4] * (colwidthArray[n] * 1000.)

        estimatedcountsArray[0] = estimatedcountsArray[0] + newcountArray[n,0]
        estimatedcountsArray[1] = estimatedcountsArray[1] + newcountArray[n,1]
        estimatedcountsArray[2] = estimatedcountsArray[2] + newcountArray[n,2]
        estimatedcountsArray[3] = estimatedcountsArray[3] + newcountArray[n,3]
        estimatedcountsArray[4] = estimatedcountsArray[4] + newcountArray[n,4]
        n += 1     
        
    return estimatedcountsArray
    #### counts = flux * cadence * Gfactor * colwidth

def wrapper(coeff, measuredcountsArray, colwidthArray, GfactorList, midpointArray, timestep):
    coeff = list(coeff)
    sigfigs = 2
    order = [int(log10(i)) for i in coeff]
    for s in range(sigfigs):
        for i in [0, 1]:
            coeff[i] = round(coeff[i], sigfigs - 1 - order[i])
            if sigfigs - 1 - order[i] <= 0:
                coeff[i] = int(coeff[i])
        iter_range = [10 ** (x - s) for x in order]
        iter_step = [x / 10 for x in iter_range]
    
        e0_range = iter_range[0]
        j0_range = iter_range[1]
        e0_step = iter_step[0]
        j0_step = iter_step[1]
    
        min_params, chi_sqr = iterate_spectrum(coeff, measuredcountsArray, colwidthArray, GfactorList, midpointArray, e0_range, j0_range, e0_step, j0_step, timestep)
        
        coeff = min_params
        
    return coeff, chi_sqr

def calculate_steps(coeff, e0_range, j0_range, e0_step, j0_step):
    steps = [[], []]
    e0i = coeff[0]
    j0i = coeff[1]
    if e0i > e0_range:
        steps[0] = np.arange(e0i - e0_range, e0i + e0_range, e0_step)
    else:
        steps[0] = np.arange(e0_step, e0i + e0_range, e0_step)
    if j0i > j0_range:
         steps[1] = np.arange(j0i - j0_range, j0i + j0_range, j0_step)
    else:
        steps[1] = np.arange(j0_step, j0i + j0_range, j0_step)

    return steps
       

def iterate_spectrum(coeff, measuredcountsArray, colwidthArray, GfactorList, midpointArray, e0_range, j0_range, e0_step, j0_step, timestep):
    max_iterations = 50
    done = False
    loops = 0
    while not done:  ##while done == True
        if loops >= max_iterations:
            print('Maximum iterations reached')
            #flag = 1
            break
        steps = calculate_steps(coeff, e0_range, j0_range, e0_step, j0_step)
        chi_sqr = find_chi_sqr(steps, measuredcountsArray, colwidthArray, GfactorList, midpointArray, timestep)  # Calculate chi squared for each point
        idx = np.unravel_index(np.argmin(chi_sqr), chi_sqr.shape)
        min_params = np.array([steps[0][idx[0]], steps[1][idx[1]]]) 
        print('Current minimum parameters, rounded:')
        print(min_params)
        print('Current iteration: E0: ',coeff[0],'J0: ',coeff[1])
        loops += 1
        if [round(x, 5) for x in min_params] == [round(x, 5) for x in coeff]:
            done = True
            #iteration_flag = 0
        else:
            # set coefficeints to the minimum point for the next loop
            coeff = min_params
            loops += 1
            
    return min_params, chi_sqr
            
    
def find_chi_sqr(steps, measuredcountsArray, colwidthArray, GfactorList, midpointArray, timestep):
    dimension = (len(steps[0]), len(steps[1])) 
    chi_sqr = np.zeros(dimension) 
    for i, p1 in enumerate(steps[0]): 
        for j, p2 in enumerate(steps[1]): 
            estimatedcountsArray = calculate_counts(colwidthArray, GfactorList, midpointArray, p1, p2)
            chi_sqr[i, j] = np.sum((measuredcountsArray[timestep,:] - estimatedcountsArray) ** 2) 
    return chi_sqr 
    
       
def main():
    
    #- arbitrary timestep to plot -#
    t = 10
    
    #---- FU3 ----
    #channel_width = np.array([68.7, 107.9, 147.2, 215.9, 284.5])
    channel_middles = np.array([265.4, 353.7, 481.2, 662.7, 913.0], dtype=float)
    channel_middles = np.divide(channel_middles, 1000.)
    
    #---- FU4 ----
    '''
    #channel_width = np.array([63.7, 100.2, 136.7, 200.4, 264.25])   
    channel_middles = np.array([251.5, 333.5, 452.0, 620.5, 852.8], dtype=float)  
    #channel_middles = np.array([100, 120, 150, 155, 200], dtype=float)
    channel_middles = np.divide(channel_middles, 1000.)
    '''
    
    Gfactor_var = read_file1(filename1)
    counts_var = read_file2(filename2)
    col_var = read_file3(filename3)
    
    flux_0, flux_1, flux_2, flux_3, flux_4, flux_array, measuredcounts_array, timestep_list, n_timesteps = calculate_flux(Gfactor_var, counts_var)
    
    midpoint_array, colwidth_array = midpoints(col_var)
    
    plt.figure()
    
    plt.suptitle('Energy (keV) vs. Energetic Electron Flux', fontsize=11)
    plt.xlabel('Energy (keV)')
    plt.ylabel('Energetic Electron Flux')
    plt.xticks((channel_middles))
    #plt.xlim(0, 310)
    
    data = np.zeros((n_timesteps, 2), dtype=float)
    for timestep in range(n_timesteps):
    ### find a more general way to do this? ###
        if timestep == t:
            plt.plot(channel_middles[0], flux_0[timestep], 'rx')
            plt.plot(channel_middles[1], flux_1[timestep], 'rx')
            plt.plot(channel_middles[2], flux_2[timestep], 'rx')
            plt.plot(channel_middles[3], flux_3[timestep], 'rx')
            plt.plot(channel_middles[4], flux_4[timestep], 'rx')
        
    #---- curve fit ----#  
    ## curve fit
    
        popt, pcov = curve_fit(func, channel_middles, flux_array[timestep,:], bounds=(0, np.inf))
    
        coefficients = (popt[0], popt[1])
        print('Initial parameters:')
        print(coefficients)
        
        J_flux = func(midpoint_array, *popt)
        if timestep == t:
            plt.plot(midpoint_array, J_flux, label='Initial fit')
            plt.legend()
            plt.show()
        
        #newcountarray_sum = calculate_counts(colwidth_array, Gfactor_var, midpoint_array, *popt)
        min_params, chi_sqr = wrapper(coefficients, measuredcounts_array, colwidth_array, Gfactor_var, midpoint_array, timestep)
        
        print('Minimum parameters:')
        print(timestep, min_params)
        
        data[timestep,0] = min_params[0]
        data[timestep,1] = min_params[1]
        
    full_data = (timestep_list, data)
    np.savetxt(outfile, np.column_stack(full_data), fmt='%s', delimiter=', ')
    print('Complete.')
    
    
    
    #calc_steps = calculate_steps(popt[0], popt[1])
    
    #chi = chi_sqr(measuredcounts_array, newcountarray_sum)
    #print(chi)
    
    
## trying to create 2D array for newcountarray_sum
## we still need to iterate through each timestep 
    
main()   


        






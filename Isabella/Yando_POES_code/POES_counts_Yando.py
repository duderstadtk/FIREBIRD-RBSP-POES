'''
Filename: 
    POES_counts_Yando.py
    
Author: 
    Isabella M. Householder
    Katharine A. Duderstadt
    
Synopsis:
    Use electron flux calculated from FIREBIRD counts to calculate counts the POES instruments
    should measure using Yando GEANT tables
    
Date:
    20 Nov 2019
    
Description:
    Read in Yando POES electron GEANT table - Table B4
          lowest energy in bin, channel width (keV), E1 Gfactor, E2 Gfactor, E3 Gfactor
          values have been divided be 100 to arrive at correct units  cm^2*sr
    Read in FIREBIRD environmental flux values
          in electrons keV-1 cm-2 s-1 sr-1
    Read in POES observed counts
    Calculated POES counts 
         Interpolate exponential fit to flux to yando energies
         counts_bin(E1, E2, E3) = (flux in bin)*G(E1, E2, E3)
         counts_channel(E1, E2, E3) - Integrate all energy bins for each channel
    Plot calculated vs observed POES counts for a selected time step
    
CHECK ISABELLA'S CODE TO SEE IF FLUX IS IN MEV OR KEV
-------------------------------------------------------------------------------
'''

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import datetime as dt
import Ngl
import Nio

filename_POES_Gfactors = 'Yando_TableB4.csv'
#filename_FB_flux = 'FB_flux_estimates.txt'
filename_FB_flux = 'flux-params_FU3_2018-09-22_1945-1948.txt'
filename_POES_obs = 'poes_m01_20180922_raw.nc'

# -----------------------------------------------------------------------------

def read_POES_Gfactors(filename_G):
    poes_GEANT = np.genfromtxt(filename_G, delimiter=',')
    return poes_GEANT

def read_FB_flux(filename_FB):
    timestamp_list = []
    J0_value = []
    E0_value = []
    file = open(filename_FB, 'r')
    nline = 0
    for line in file:
        line = line.strip().split(',')
        datetime_str = line[0]
        timestamp_list.append(dt.datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%fZ'))
        J0_value.append(float(line[1]))
        E0_value.append(float(line[2]))
        nline = nline+1
    J0_value = np.array(J0_value)
    E0_value = np.array(E0_value)
    file.close()
    return timestamp_list, J0_value, E0_value, nline

def read_POES_counts(filename_nc):
    nc_fid = Nio.open_file(filename_nc,'r')
    timestamp = nc_fid.variables['time']
    e1_cps = nc_fid.variables['mep_ele_tel0_cps_e1']
    e2_cps = nc_fid.variables['mep_ele_tel0_cps_e2']
    e3_cps = nc_fid.variables['mep_ele_tel0_cps_e3']
    timeclock = []
    print('timeclock type')
    print(type(timeclock))
    timeindex = 1
    timeindex = len(timestamp)
    time = np.zeros((timeindex),'f')
    time[:] = timestamp[:]
    for ntime in range(timeindex):
        timeclock.append(dt.datetime.utcfromtimestamp(float(timestamp[ntime])/1000.))
    e1_counts = np.zeros((timeindex),'f')
    e2_counts = np.zeros((timeindex),'f')
    e3_counts = np.zeros((timeindex),'f')
    e1_counts[:] = e1_cps[:]
    e2_counts[:] = e2_cps[:]
    e3_counts[:] = e3_cps[:]
    POES_obs = np.zeros((timeindex,3),'f')
    POES_obs[:,0] = e1_counts
    POES_obs[:,1] = e2_counts
    POES_obs[:,2] = e3_counts
    #print("number of timesteps = ",timeindex)
    #print('time')
    #print(time)
    #print('timeclock')
    #print(timeclock[0:20])
    #print('e1')
    #print(e1_counts)
    #print('e2')
    #print(e2_counts)
    #print('e3')
    #print(e3_counts)
    return timeclock, POES_obs


def main():
    Gfactors = read_POES_Gfactors(filename_POES_Gfactors)
    timestamp, J0, E0, nlines = read_FB_flux(filename_FB_flux)
    FB_POES_counts = np.zeros((nlines,3),dtype=float)
    POES_time, POES_obs_counts = read_POES_counts(filename_POES_obs)
    # calculate counts in each Yando energy bin
    # for ntime in timestamp_list:
    for ntime in range(nlines):
        flux_en_lev = np.zeros((23), dtype = float)
        flux_en_bin = np.zeros((22), dtype = float)
        counts_en_bin = np.zeros((22,3), dtype = float)
        sum_E1 = 0.
        sum_E2 = 0.
        sum_E3 = 0.
        for en in range(22):
            flux_en_lev[en] = J0[ntime]*np.exp(-Gfactors[en,0]/1000./E0[ntime])
        flux_en_lev[22] = J0[22]*np.exp(-5./E0[22])
        #print('flux interpolated to energy levels')
        #print(flux_en_lev)
        for en in range(22):
            flux_en_bin[en] = ((flux_en_lev[en]+flux_en_lev[en+1])/2.)*(Gfactors[en+1,0]-Gfactors[en,0])
            counts_en_bin[en,0] = flux_en_bin[en]*Gfactors[en,2]
            counts_en_bin[en,1] = flux_en_bin[en]*Gfactors[en,3]
            counts_en_bin[en,2] = flux_en_bin[en]*Gfactors[en,4]
            sum_E1 = sum_E1+counts_en_bin[en,0]
            sum_E2 = sum_E2+counts_en_bin[en,1]
            sum_E3 = sum_E3+counts_en_bin[en,2]
        #print('counts in energy bins for E1')
        #print(counts_en_bin[:,0])
        #print('counts in energy bins for E2')
        #print(counts_en_bin[:,1])
        #print('counts in energy bins for E3')
        #print(counts_en_bin[:,2])
        #print('sum_E1')
        #print(sum_E1)
        #print('sum_E2')
        #print(sum_E2)
        #print('sum_E3')
        #print(sum_E3)
        FB_POES_counts[ntime,0] = sum_E1
        FB_POES_counts[ntime,1] = sum_E2
        FB_POES_counts[ntime,2] = sum_E3
    ### plot ###
    fig, axs = plt.subplots(2)
    axs[0].plot(timestamp,FB_POES_counts)
    #axs[0].set_xlim([dt.datetime(2018,9, 22,19,45,00), dt.datetime(2018, 9, 22,19,47,30)])
    axs[0].set_xlim([dt.datetime(2018,9, 22,19,43,00), dt.datetime(2018, 9, 22,19,55,30)])
    axs[0].set_ylim([0.1,1.e4])
    axs[0].set_yscale('log')
    axs[1].plot(POES_time, POES_obs_counts)
    #axs[1].set_xlim([dt.datetime(2018,9, 22,19,45,00), dt.datetime(2018, 9, 22,19,47,30)])
    axs[1].set_xlim([dt.datetime(2018,9, 22,19,43,00), dt.datetime(2018, 9, 22,19,55,30)])
    axs[1].set_yscale('log')
    axs[1].set_ylim([0.1,1.e4])
    fig.autofmt_xdate()
    plt.show()

main()








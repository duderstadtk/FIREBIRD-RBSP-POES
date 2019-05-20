#
#  File:
#    FB_HiRes_to_integral.py
#
#  Synopsis:
#    Create FIREBIRD plots of integral flux   
#
#    Files: 
#        201809022_FU3_col_flux.nc
#        201809022_FU3_McIlwain.nc
#
#  Author:
#    Katharine Duderstadt 
#  
#  Date:
#    10 Oct 2018
#
#  Description:
#    Read in FIREBIRD files as netcdf (.nc) saved from Autoplot
#    Fit FIREBIRD differential flux with power law
#       (Note...currently set to "piecewise fit") 
#    Integrate to POES channels
#    Plot for comparison -- with time and L-shell on x-axis 
# -----------------------------------------------------------------

import numpy, os
import Ngl
import Nio
import time
import datetime
from scipy import interpolate
from scipy.interpolate import interp1d
from math import exp

# --------------------- Variables to modify ---------------------------

#datetime = 2400          #timestep for diff_flux_FB.eps plot
datetime = 800          #timestep for diff_flux_FB.eps plot

energyindex = 6           # number of FB energy channels
diffen = 5                # nubmer of FB differential energy channels 
#energy_fire = [251.5, 333.5, 452., 620.5, 852.8] #FU4
#FU_int_channel = 984         #FU4
energy_fire = [265.4, 353.7, 481.2, 662.7, 913.]    #FU3
FU_int_channel = 1055       #FU3 
poes1 = 130 
poes2 = 287 
poes3 = 612 
poesindex = 3
POES_energies = ("> 130 keV","> 287 keV","> 612 keV")  #NOAA-15/Metop1b 

filedir = '/Users/katharineduderstadt/FIREBIRD/PYTHON/Campaign_18_plots/'
nc_filename = Nio.open_file(filedir+'20180927_01h_FU4_col_flux.nc', 'r')
nc_filename2 = Nio.open_file(filedir+'20180927_01h_FU4_Lshell.nc', 'r')

plotname_diff_flux = "20180927_01h_FU4_diff_flux"
plotname_int_flux = "20180927_01h_FU4_int_flux"
plotname_l_shell = "20180927_01h_FU4_int_flux_L-shell"

yaxis_max_plot = 1.e6
yaxis_min_plot = 1.e-1

# --------------------- Read FIREBIRD file ---------------------------
# read .nc file saved from Autoplot  
#
# FU4 energy channels = [251.5keV, 333.5keV, 452.keV,620.5keV, 852.8keV, > 984 keV]
# counts cm-2 sr-1 keV-1 s-1 for lowest five channels
# counts cm-2 sr-1 s-1 for integral channel 
#
# Example header:  ncdump -h filename.nc > head
# netcdf FB_test {
#dimensions:
#        Time = 4800 ;
#        dim1 = 6 ;
#variables:
#        double Time(Time) ;
#                Time:_FillValue = -1.e+31 ;
#                Time:units = "microseconds since 2000-01-01T00:00Z" ;
#        double Col_flux(Time, dim1) ;
#                Col_flux:_FillValue = -1.e+31 ;
#
#netcdf FB_test_Lshell {
#dimensions:
#        Time = 4800 ;
#variables:
#        double Time(Time) ;
#                Time:_FillValue = -1.e+31 ;
#                Time:units = "microseconds since 2000-01-01T00:00Z" ;
#        double McIlwainL(Time) ;
#                McIlwainL:_FillValue = -1.e+31 ;
# -----------------------------------------------------------------
# ---------------- Read netCDF files --------------------------
print(nc_filename)
Timenc = nc_filename.variables["Time"]    # time 
Col_fluxnc= nc_filename.variables["Col_flux"]    # McIlwain L 
McIlwainLnc = nc_filename2.variables["McIlwainL"]    # McIlwain L 

timeindex = 1 
timeindex = len(Timenc)
print("number of timesteps = ",timeindex)

data = numpy.zeros((timeindex,energyindex),'f')
time = numpy.zeros((timeindex),'f') 
McIlwainL = numpy.zeros((timeindex),'f') 
Col_flux = numpy.zeros((timeindex,energyindex),'f') 
FB_int_flux = numpy.zeros((timeindex),'f') 
int_flux = numpy.zeros((timeindex,poesindex),'f')

time[:] = Timenc[:] 
Col_flux[:,:] = Col_fluxnc[:,:]
McIlwainL[:] = McIlwainLnc[:]
FB_int_flux[:] = Col_flux[:,diffen]

# -------------------- Interpolate between energies ------------
# First create new energy levels logarithmically spaced between 0.1-5000keV
# imax=120 refers to the number of energy levels
# -------------------------------------------------------

imax = 120 
imax1 = 119 

energy_min = 0.1
energy_max = 5000.

energy_lev = numpy.zeros((imax),'f')
energy_lev[0]=energy_min
energy_lev[imax1]=energy_max

flag1 = 0
flag2 = 0
flag3 = 0
flag4 = 0
flag5 = 0
for nlev in range (0,imax1):
   ALO=numpy.log10(energy_lev[0])
   AHI=numpy.log10(energy_lev[imax1])
   SP=(AHI-ALO)/imax
   energy_lev[nlev]=10.**(ALO+SP*nlev)
   if flag1 == 0 and energy_lev[nlev] >= poes1:
     indexpoes1 = nlev
     flag1 = 1 
   if flag2 == 0 and energy_lev[nlev] >= poes2:
     indexpoes2 = nlev
     flag2 = 1 
   if flag3 == 0 and energy_lev[nlev] >= poes3:
     indexpoes3 = nlev
     flag3 = 1 
   if flag4 == 0 and energy_lev[nlev] >= FU_int_channel:
     indexFU4int = nlev
     flag4 = 1 
   if flag5 == 0 and energy_lev[nlev] >= energy_fire[0]:
     indexFU5int = nlev
     flag5 = 1
   nlev=nlev+1

print("indexpoes 1 = ",indexpoes1," energy_lev = ",energy_lev[indexpoes1])
print("indexpoes 2 = ",indexpoes2," energy_lev = ",energy_lev[indexpoes2])
print("indexpoes 3 = ",indexpoes3," energy_lev = ",energy_lev[indexpoes3])
print("FU_int_channel index = ",indexFU4int," energy_lev = ",FU_int_channel)
print("FU_low_channel index = ",indexFU5int," energy_lev = ",energy_fire[0])

print("Energy Levels", energy_lev[:])

Col_flux_enlev = numpy.zeros((timeindex,imax),'f') 

diff_flux = numpy.zeros((timeindex,imax),'f')
diff_flux_exp = numpy.zeros((timeindex,imax),'f')

ntime = 0
for ntime in range (0,timeindex):
   flux_fb = numpy.zeros((diffen),'f')
   flux_fb_log = numpy.zeros((diffen),'f')
   flux = numpy.zeros((imax),'f')
   flux_new = numpy.zeros((imax),'f')
   flux_log = numpy.zeros((imax),'f')

   flux_fb[:] = Col_flux[ntime,:diffen] 
   for nendiff in range (0,diffen):
      if flux_fb[nendiff] <= 0.:
         flux_fb[nendiff] = 1.e-8
   flux_fb_log[:] = numpy.log(flux_fb[:])
   energy_array = numpy.zeros((diffen,2),'f')
   energy_array[:,1] = numpy.array([1.,1.,1.,1.,1.]) 
   energy_array[:,0] = energy_fire[:]

   m, yint = numpy.linalg.lstsq(energy_array,flux_fb_log,rcond=-1)[0]
#   m, yint = numpy.linalg.lstsq(energy_array,flux_fb_log)[0]
#   print("ts, slope, int")
#   print(ntime,m,yint)
  
   a = exp(m)
   C = exp(yint) 
   flux_new[:] = C*(a**energy_lev[:])
   diff_flux_exp[ntime,:] = flux_new[:] 

# Create tail continuing exp fit to last two data points. 
  
   diff = flux_fb_log[diffen-2]-flux_fb_log[diffen-1]
   if diff > 0.: 
      slope = (flux_fb_log[diffen-2]-flux_fb_log[diffen-1])/(energy_fire[diffen-2]-energy_fire[diffen-1])
      energy_fb_fin = energy_max 
      flux_fb_log_fin = flux_fb_log[diffen-2]+slope*(energy_fb_fin-energy_fire[diffen-2])
   else: 
      energy_fb_fin = energy_max 
      flux_fb_log_fin =-1.e6 

   energy_fb_start = energy_min
   flux_fb_log_start = flux_fb_log[0]

   energy_fb_ext = numpy.zeros((diffen+2),'f')
   energy_fb_ext[0] = energy_fb_start
   energy_fb_ext[1:diffen+1] = energy_fire[:]
   energy_fb_ext[diffen+1] = energy_fb_fin

   flux_fb_log_ext = numpy.zeros((diffen+2),'f')
   flux_fb_log_ext[0] = flux_fb_log_start
   flux_fb_log_ext[1:diffen+1] = flux_fb_log[:]
   flux_fb_log_ext[diffen+1] = flux_fb_log_fin

   en_interp = interp1d(energy_fb_ext, flux_fb_log_ext,kind='linear',bounds_error=False,fill_value=-6.)

   flux_log[:] = en_interp(energy_lev[:])   

   for n_en in range (0,imax):
      if flux_log[n_en] > -6.:
         flux[n_en] = numpy.exp(flux_log[n_en])
      else:
         flux[n_en] = 0.   

   diff_flux[ntime,:] = flux[:]

   for n_en in range (0,indexFU5int):
      if diff_flux_exp[ntime,n_en] > 0.:
         diff_flux[ntime,n_en] = diff_flux_exp[ntime,n_en] 
      else:
         diff_flux[ntime,n_en] = flux_fb_log_start 
 

# ------------- plot interpolated differential flux -------------

wks_type = "eps"
wks = Ngl.open_wks("eps", plotname_diff_flux)  # Open a workstation.

resources1 = Ngl.Resources()
resources1a = Ngl.Resources()

resources1.tiYAxisString = "Differential Flux (cm-2 s-1 sr-1 keV-1)"
resources1.tiXAxisString = "Energy (keV)"
resources1.trXAxisType = "LogAxis"
resources1.trYAxisType = "LogAxis"
resources1.trYMaxF = 1.e3 
resources1.trYMinF = 1.e-3 
resources1.trXMaxF = 1.e4 
resources1.trXMinF = 50. 
resources1.nglMaximize = False
resources1.vpHeightF   = 0.75
resources1.vpWidthF    = 0.65
resources1.vpXF        = 0.20
resources1.vpYF        = 0.90
resources1.xyLineThicknessF = 3.0
resources1.xyMarkLineModes = "Lines"
resources1.xyMarkerColor     = "red"

resources1a.trXAxisType = "LogAxis"
resources1a.trYAxisType = "LogAxis"
resources1a.trYMaxF = 1.e3 
resources1a.trYMinF = 1.e-3 
resources1a.trXMaxF = 1.e4 
resources1a.trXMinF = 50. 
resources1a.nglMaximize = False
resources1a.xyMarkLineModes = "Markers"
resources1a.xyMarkerColor     = "black"
resources1a.xyMarkers = 3 
resources1a.vpHeightF   = 0.75
resources1a.vpWidthF    = 0.65
resources1a.vpXF        = 0.20
resources1a.vpYF        = 0.90

diff_flux_plot = numpy.zeros((imax),'f')
diff_flux_plot[:] = diff_flux[datetime,:]

for en in range (0,imax):
   if diff_flux_plot[en] <= 0.:
      diff_flux_plot[en] = 1.e-8

firebird_flux = numpy.zeros((diffen),'f')
firebird_flux[:] = Col_flux[datetime,:diffen] 

diff_flux_exp_plot = numpy.zeros((imax),'f')
diff_flux_exp_plot[:] = diff_flux_exp[datetime,:] 

for en in range (0,diffen):
   if firebird_flux[en] <= 0.:
      firebird_flux[en] = 1.e-8

resources1.nglDraw  = False
resources1.nglFrame  = False
resources1a.nglDraw  = False
resources1a.nglFrame  = False

plot1 = Ngl.xy(wks,energy_lev[21:],diff_flux_plot[21:],resources1)   # Draw an XY plot.
plot1a = Ngl.xy(wks,energy_fire,firebird_flux,resources1a)   # Draw an XY plot.
#plot1b = Ngl.xy(wks,energy_lev[21:],diff_flux_exp_plot[21:],resources1)   # Draw an XY plot.

Ngl.draw(plot1)
Ngl.draw(plot1a)
#Ngl.draw(plot1b)
Ngl.frame(wks)

# --------------------------------------------------------------------
# Calculate integral flux from differential flux
# Loop through timesteps
# Loop through energy levels beginning with poesindex
# Integrate (sum) the energy interval * flux (use midpoint of flux)  
# diff_flux = numpy.zeros((timeindex,imax),'f')
# -------------------------------------------------------------------
 
ntime = 0
for ntime in range (0,timeindex):
   for npoes in range (0,poesindex):
      flux_int_poes1 = 0.
      flux_int_poes2 = 0.
      flux_int_poes3 = 0.
      flux_in_channel = 0.
      energy_range = 0.
      avg_flux = 0.
      interval_flux = 0.
      for nen in range (indexpoes1,imax1):
         energy_range = energy_lev[nen+1]-energy_lev[nen] 
         avg_flux = (diff_flux[ntime,nen]+diff_flux[ntime,nen+1])/2.
         interval_flux = energy_range * avg_flux
         flux_int_poes1 = flux_int_poes1 + interval_flux 
      int_flux[ntime,0] = flux_int_poes1+FB_int_flux[ntime]
      for nen in range (indexpoes2,imax1):
         energy_range = energy_lev[nen+1]-energy_lev[nen] 
         avg_flux = (diff_flux[ntime,nen]+diff_flux[ntime,nen+1])/2.
         interval_flux = energy_range * avg_flux
         flux_int_poes2 = flux_int_poes2 + interval_flux 
      int_flux[ntime,1] = flux_int_poes2+FB_int_flux[ntime]
      for nen in range (indexpoes3,imax1):
         energy_range = energy_lev[nen+1]-energy_lev[nen] 
         avg_flux = (diff_flux[ntime,nen]+diff_flux[ntime,nen+1])/2.
         interval_flux = energy_range * avg_flux
         flux_int_poes3 = flux_int_poes3 + interval_flux 
      int_flux[ntime,2] = flux_int_poes3+FB_int_flux[ntime]

# --------------------- Create Plot ------------------------
# Plot integral flux vs. time for the three POES channels
# int_flux[timeindex,poesindex]
# ----------------------------------------------------------

wks_type = "eps"
wks2 = Ngl.open_wks(wks_type, plotname_int_flux)  # Open a workstation.

resources2 = Ngl.Resources()
resources2a = Ngl.Resources()
resources2b = Ngl.Resources()

resources2.tiMainString = "FIREBIRD Integral Flux at POES channels"
resources2.tiYAxisString = "Integral Flux (cm-2 s-1 sr-1)"
resources2.tiXAxisString = "Time"
resources2.trYAxisType = "LogAxis"
resources2.trYMaxF = yaxis_max_plot 
resources2.trYMinF = yaxis_min_plot 
resources2.nglMaximize = False
resources2.vpHeightF   = 0.75
resources2.vpWidthF    = 0.65
resources2.vpXF        = 0.20
resources2.vpYF        = 0.90
resources2.xyLineThicknessF = 3.0
resources2.xyLineColors     = ["black"]

resources2a.trYAxisType = "LogAxis"
resources2a.trYMaxF = yaxis_max_plot 
resources2a.trYMinF = yaxis_min_plot 
resources2a.nglMaximize = False
resources2a.vpHeightF   = 0.75
resources2a.vpWidthF    = 0.65
resources2a.vpXF        = 0.20
resources2a.vpYF        = 0.90
resources2a.xyLineThicknessF = 3.0
resources2a.xyLineColors     = ["red"]

resources2b.trYAxisType = "LogAxis"
resources2b.trYMaxF = yaxis_max_plot 
resources2b.trYMinF = yaxis_min_plot 
resources2b.nglMaximize = False
resources2b.vpHeightF   = 0.75
resources2b.vpWidthF    = 0.65
resources2b.vpXF        = 0.20
resources2b.vpYF        = 0.90
resources2b.xyLineThicknessF = 3.0
resources2b.xyLineColors     = ["green"]

#print(int_flux)

# --------------------------------------------------
# Calculate averages  (e.g. 1 s)  
# plotting routine doesn't want to print more than 250 points
# -------------------------------------------------

cadence = 20.    #20 timesteps is 1 second
#cadence = 100.
secindex = timeindex/cadence
secindexint = int(secindex)+1 
timesec = numpy.arange(1.,secindex+1,1.)

int_flux_sec = numpy.zeros((secindexint,poesindex),'f')
McIlwainL_sec = numpy.zeros((secindexint),'f')

int_flux_sum = numpy.zeros((poesindex),'f')  
McIlwainL_sum = 0.  

nstep = 0
nsec = 0
ndiv = 1. 
for ntime in range (0,timeindex):
   if nstep < cadence+1.:
      for npoes in range (0,poesindex):
        if int_flux[ntime,npoes] > 0.:
           int_flux_sum[npoes] = int_flux_sum[npoes] + int_flux[ntime,npoes] 
           ndiv = ndiv+1.
      nstep = nstep +1 
   if nstep >= cadence+1.:
      nstep = 0
      nsec = nsec + 1 
      int_flux_sec[nsec,:] = int_flux_sum[:]/ndiv
      int_flux_sum[:] = 0.
      ndiv = 1

for ntime in range (0,secindexint):
   for npoes in range (0,poesindex):
      if int_flux_sec[ntime,npoes] <= 0.:
         int_flux_sec[ntime,npoes] = 1.e-8

nstep = 0
nsec = 0
ndiv = 1. 
for ntime in range (0,timeindex):
   if nstep < cadence+1.:
     if McIlwainL[ntime] > 0.:
        McIlwainL_sum = McIlwainL_sum + McIlwainL[ntime] 
        ndiv = ndiv+1.
     nstep = nstep +1 
   if nstep >= cadence+1.:
      nstep = 0
      nsec = nsec + 1 
      McIlwainL_sec[nsec] = McIlwainL_sum/ndiv
      McIlwainL_sum = 0.
      ndiv = 1

resources2.nglDraw  = False
resources2.nglFrame  = False
resources2a.nglDraw  = False
resources2a.nglFrame  = False
resources2b.nglDraw  = False
resources2b.nglFrame  = False

plot2 = Ngl.xy(wks2,timesec[1:secindexint-1],int_flux_sec[1:secindexint-1,0],resources2)
plot2a = Ngl.xy(wks2,timesec[1:secindexint-1],int_flux_sec[1:secindexint-1,1],resources2a)
plot2b = Ngl.xy(wks2,timesec[1:secindexint-1],int_flux_sec[1:secindexint-1,2],resources2b)

Ngl.draw(plot2)
Ngl.draw(plot2a)
Ngl.draw(plot2b)
#Ngl.draw(plot2)
Ngl.frame(wks2)


# --------------------- Create plot as a function of L-shell -------------

wks_type = "eps"
wks3 = Ngl.open_wks(wks_type, plotname_l_shell)

resources3 = Ngl.Resources()
resources3a = Ngl.Resources()
resources3b = Ngl.Resources()

resources3.tiMainString = "FIREBIRD Integral Flux at POES channels"
resources3.tiYAxisString = "Integral Flux (cm-2 s-1 sr-1)"
resources3.tiXAxisString = "L-shell"
resources3.trYAxisType = "LogAxis"
resources3.trYMaxF = yaxis_max_plot 
resources3.trYMinF = yaxis_min_plot 
resources3.nglMaximize = False
resources3.vpHeightF   = 0.75
resources3.vpWidthF    = 0.65
resources3.vpXF        = 0.20
resources3.vpYF        = 0.90
resources3.xyLineThicknessF = 3.0
resources3.xyLineColors     = ["black"]

resources3a.trYAxisType = "LogAxis"
resources3a.trYMaxF = yaxis_max_plot 
resources3a.trYMinF = yaxis_min_plot 
resources3a.nglMaximize = False
resources3a.vpHeightF   = 0.75
resources3a.vpWidthF    = 0.65
resources3a.vpXF        = 0.20
resources3a.vpYF        = 0.90
resources3a.xyLineThicknessF = 3.0
resources3a.xyLineColors     = ["red"]

resources3b.trYAxisType = "LogAxis"
resources3b.trYMaxF = yaxis_max_plot 
resources3b.trYMinF = yaxis_min_plot 
resources3b.nglMaximize = False
resources3b.vpHeightF   = 0.75
resources3b.vpWidthF    = 0.65
resources3b.vpXF        = 0.20
resources3b.vpYF        = 0.90
resources3b.xyLineThicknessF = 3.0
resources3b.xyLineColors     = ["green"]

resources3.nglDraw  = False
resources3.nglFrame  = False
resources3a.nglDraw  = False
resources3a.nglFrame  = False
resources3b.nglDraw  = False
resources3b.nglFrame  = False

plot3 = Ngl.xy(wks3,McIlwainL_sec[1:secindexint-1],int_flux_sec[1:secindexint-1,0],resources3)
plot3a = Ngl.xy(wks3,McIlwainL_sec[1:secindexint-1],int_flux_sec[1:secindexint-1,1],resources3a)
plot3b = Ngl.xy(wks3,McIlwainL_sec[1:secindexint-1],int_flux_sec[1:secindexint-1,2],resources3b)

Ngl.draw(plot3)
Ngl.draw(plot3a)
Ngl.draw(plot3b)
Ngl.frame(wks3)

Ngl.end


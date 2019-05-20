#
#  File:
#    RBSP_read.py
#
#  Synopsis:
#        Read in .cdf files for RBSP data
#    Files: 
#        rbspa_rel03_ect-mageis-L3_20161224_v7.3.0.cdf
#
#  Author:
#    Katharine Duderstadt 
#  
#  Date:
#    1 Nov 2017
#
#  Description:
#    Goal is to read in RBSP files to look at data in conjunction 
#    with FIREBIRD
#    Ultimate goal is to create netCDF files for WACCM 
#    As well as be able to plot using pyncl 
# 
#  Output:
#     GCR_Cosmo_prod_table.nc 
# --------------- import modules and packages ----------- 

import os
os.environ["CDF_LIB"] = "/Applications/cdf/cdf/lib/"
from spacepy import pycdf
import datetime
import numpy as np
import Ngl
import Nio

dir = "~/FIREBIRD/CONTEXT/"
cdf = pycdf.CDF(dir+'rbspa_rel03_ect-mageis-L3_20130304_v7.3.0.cdf')
print(cdf)

FEDU_Alpha = cdf['FEDU_Alpha'][...]
print(FEDU_Alpha[:]) 
FEDU = cdf['FEDU'][...]
Epoch = cdf['Epoch'][...]

#FEDU: CDF_DOUBLE [8020, 11, 25]

FEDU_alpha_en = np.zeros((11,25), 'f')
#FEDU_pitch = np.zeros((7964,25), 'f')
FEDU_pitch = np.zeros((7970,25), 'f')


FPDU_ENERGY_LABL = cdf['FPDU_ENERGY_LABL'][...] 
print(FPDU_ENERGY_LABL)

index = 2000
pitch = 0   # 8 degrees 
FEDU_alpha_en[:,:] = FEDU[index,:,:]
FEDU_pitch[:,:] = FEDU[:,0,:]

energy_lev = [58.44, 69.29, 82.85, 99.12, 118.11, 139.81, 164.22, 194.06, 229.32, 267.29, 307.98, 356.8, 413.76, 478.86, 554.8, 636.18, 728.4, 839.61, 967.09, 1110.85, 1270.88]

#FPDU_ENERGY_LABL: CDF_CHAR*30 [1, 31]

FEDU_plot = np.transpose(FEDU_alpha_en) 
FEDU_plot2 = np.transpose(FEDU_pitch) 
print(FEDU_plot[10,:])

# ------------------------------------------
#  Open a workstation and draw the contour plot with color fill.
# ------------------------------------------

wks_type = "ps"
wks = Ngl.open_wks(wks_type,"RBSP_pitch_energy")

res = Ngl.Resources()
res.cnFillOn           = True    # turn on color fill
res.cnLineLabelsOn     = False   # turn off contour line labels
res.lbLabelFontHeightF = 0.018   # make labelbar labels smaller
res.sfXArray = FEDU_Alpha 
res.sfYArray = energy_lev 
res.cnExplicitLabelBarLabelsOn = True
res.lbLabelStrings = ("1","10","100","1e3","1e4","1e5")
res.cnLevelSelectionMode = 'ExplicitLevels'
#res.cnMinLevelValF = 0. 
#res.cnMaxLevelValF = 1.e8
res.cnLevels = (1., 10., 100., 1000., 10000., 100000.)
#res.cnLevels = ( 1, 1e2, 1e3, 1e4, 1e5, 1e6)
#res.cnLevels = np.logspace(1, 6, num=12)
res.cnFillMode = 'CellFill'
res.tmXBMode = 'Explicit'
res.tmXBValues = (8, 25, 41, 57, 74, 90, 106, 123, 139, 155, 172)
res.tmXBLabels = ("8", "25", "41", "57", "74", "90", "106", "123", "139", "155", "172")

Ngl.contour(wks,FEDU_plot[0:20,:],res)


# ------------------------------------------
# Plot RBSP for 8 degree pitch 
# ------------------------------------------ 

wks_type = "ps"
wks2 = Ngl.open_wks(wks_type,"RBSP_8degree")

res2 = Ngl.Resources()
res2.cnFillOn           = True    # turn on color fill
res2.cnLineLabelsOn     = False   # turn off contour line labels
res2.lbLabelFontHeightF = 0.018   # make labelbar labels smaller
#res2.sfXArray = Epoch 
res2.sfYArray = energy_lev 
res2.cnExplicitLabelBarLabelsOn = True
res2.lbLabelStrings = ("1","10","100","1e3","1e4","1e5")
res2.cnLevelSelectionMode = 'ExplicitLevels'
#res.cnMinLevelValF = 0. 
#res.cnMaxLevelValF = 1.e8
res2.cnLevels = (1., 10., 100., 1000., 10000., 100000.)
#res.cnLevels = ( 1, 1e2, 1e3, 1e4, 1e5, 1e6)
#res.cnLevels = np.logspace(1, 6, num=12)
res2.cnFillMode = 'CellFill'
#res.tmXBMode = 'Explicit'
#res.tmXBValues = (8, 25, 41, 57, 74, 90, 106, 123, 139, 155, 172)
#res.tmXBLabels = ("8", "25", "41", "57", "74", "90", "106", "123", "139", "155", "172")

Ngl.contour(wks2,FEDU_plot2[0:20,:],res2)

Ngl.end()

cdf.close()




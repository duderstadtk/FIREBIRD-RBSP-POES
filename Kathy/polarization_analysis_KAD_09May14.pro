;
; 
; Input: mag field tplot var.
;
; Written by: Robert C. Allen (rcc53@wildcats.unh.edu)
; 
; Modified by K. Duderstadt on 1 Sep 2019
; 
; Subroutines fft_spec.pro, tdigital_filter.pro, thm_fac_matrix_make.pro, trotate_to_fac.pro, 
; tvector_rotate.pro, twavpol.pro
; (and perhaps others from SPEDAS package) 
;
; Notes: FUNCTIONS must be before the main program in IDL
;    Can't figure out how to size ps files (test.ps) 
;              ...for now plot three stacked plots
;    Can't figure out how to get a white background to plot 
;
; Run Commands 
;    IDL
;    .rnew polarization_analysis_KADfinal.pro
;    POLARIZATION_ANALYSIS
;   (at STOPS, type '.c' to get code to continue) 
;

FUNCTION gyrof, btot, ionmass, charge, gyrofreqhz
; Note - calculate gyrofrequency and then divide by 2pi to get Hz
   qe     = 1.602e-19
   amu    = 1.661e-27
   pi = 3.1416
   gyrofreqhz = (charge*qe*btot*1.e-9)/(2.*pi*ionmass*amu)
   RETURN, gyrofreqhz
END

PRO polarization_analysis

date='2014-05-09'
;date='2018-09-22'
w_date=date+'/'+['00:00:01','23:59:59']
;w_date=date+'/'+['20:00:00','23:00:00']
;w_date=date+'/'+['20:00:00','21:00:00']
timespan, date, 1

rbsp_load_emfisis, level='l3', cadence='hires', coord='gse', probe='b' 

tname = 'rbspb_emfisis_l3_hires_gse_Mag'


; TIME CLIP 
time_clip,'rbspb_emfisis_l3_hires_gse_Mag',w_date[0],w_date[1], $
         newname = 'rbspb_emfisis_l3_hires_gse_Mag_tclip'

bfield = 'rbspb_emfisis_l3_hires_gse_Mag_tclip' 

vnm = 'rbspb_emfisis_l3_hires_gse_Mag_tclip' 

;vnm = bfield

;==========================================
;Set sizes for plotting
;==========================================
tplot_options,'charsize', 1.0   ;1.2
!P.thick = 2                  ;1.2
!P.charsize = 2.
!P.charthick = 2
!X.thick = 2
!Y.thick = 2
!X.ticklen = -0.04  
!Y.ticklen = -0.01

;==========================================
;Set constants and parameters
;==========================================

nopfft_input     = 4096				;NOPFFT_INPUT

nopfft_str = STRING(nopfft_input,'(I4.4)')

steplength_input =nopfft_input/8.
;TESTING
;steplength_input=ROUND(64*2.5/0.35)



f_low  = 0.1
f_high = 5.0
;f_low=.1
;f_high=1.5

f_low_arr = string(f_low, '(F3.1)')
f_high_arr = string(f_high,'(F3.1)')

Aripple = 50.
Nterms = 800. ;600. ;400.				;NTERMS

f_low_arr = string(f_low, '(F3.1)')
f_high_arr = string(f_high,'(F3.1)')

other_dim = 'Xgse'
    width = 10. ; time smooth width to get the ambient B field
 
     nopfft = nopfft_input ;1024. ;32 ;256
 steplength = steplength_input ;nopfft/8.
   
;==========================================
;Get wave fields via a band=pass filter
;==========================================
tdigital_filter, bfield, $
  f_low,f_high,Aripple=Aripple,Nterms=Nterms


;==========================================
;Convert to the field-aligned coordinates
;==========================================
get_data,vnm,data=dat,dlim=lim
v_data_att = {Struct, coord_sys:'gse'}
store_data,vnm,data={x:dat.x,y:dat.y},dlim={data_att:v_data_att} ;lim



trotate_to_fac,bfield+'_filtered', $
               bfield, $
               other_dim=other_dim, $
               width=width

;get_data,vnm,data=dat,dlim=lim
;v_data_att = {Struct, coord_sys:'gse'}         
;store_data,vnm,data={x:dat.x,y:dat.y},dlim={data_att:v_data_att} ;lim        

                                ; data gap troubles if using FGM 
time_av =11.
avg_data,     vnm,time_av,newname=vnm+'_av'
tinterpol_mxn,vnm+'_av',vnm

options,vnm+'_av_interp','labels',[' ',' ',' ']

thm_fac_matrix_make, vnm+'_av_interp', /degap ;,dt=3

; ### tvector_rotate ### 
; pro tvector_rotate,mat_var_in,vec_var_in,newname = newname,error=error
; mat_var_in: 3 B components in the field-aligned coordinates?
; vec_var_in: 3 B components of a wave packet?
tvector_rotate, vnm+'_av_interp_fac_mat',vnm 

vnm=vnm+'_filtered'

;==========================================
;Polarization Analysis
;==========================================
twavpol,vnm+'_rot', error=error, freqline = freqline, timeline = timeline, $
  nopfft=nopfft_input,steplength=steplength_input

;==========================================
;Set titles
;==========================================
options,vnm+'_rot_degpol', 'ztitle','Deg. Of Pol'
options,vnm+'_rot_powspec' , 'ztitle','Power (nT!E2!N/Hz)'
options,vnm+'_rot_waveangle' , 'ztitle','Normal Angle (deg.)'
options,vnm+'_rot_elliptict' , 'ztitle','Ellipticity'
options,vnm+'_rot_v1v2','ztitle','V1/V2'

options,vnm+'_rot_degpol', 'ytitle','f (Hz)'
options,vnm+'_rot_powspec' , 'ytitle','f (Hz)'
options,vnm+'_rot_waveangle' , 'ytitle','f (Hz)'
options,vnm+'_rot_elliptict' , 'ytitle','f (Hz)'
options,vnm+'_rot_deltamin' , 'ytitle','f (Hz)'
options,vnm+'_rot_v1v2' , 'ytitle','f (Hz)'
options,vnm+'_rot','ytitle','dB (nT)'

ylim,vnm+'_rot_degpol',.2,10.,1
ylim,vnm+'_rot_powspec',.2,10.,1
ylim,vnm+'_rot_waveangle',.2,10.,1
ylim,vnm+'_rot_elliptict',.2,10.,1
ylim,vnm+'_rot_deltamin',.2,10.,1
ylim,vnm+'_rot_v1v2',.2,10.,1

zlim,vnm+'_rot_degpol', 0., 1., 0
zlim,vnm+'_rot_powspec',0.01,10,1
zlim,vnm+'_rot_waveangle',0.,90.,0
zlim,vnm+'_rot_elliptict',-0.4,0.4,0
zlim,vnm+'_rot_deltamin',0,40
zlim,vnm+'_rot_v1v2',0,1.0
time_stamp,/off

;==========================================
;Wavenormal Angle rad. --> deg.
;========================================== 
get_data,vnm+'_rot_waveangle',data=dat,alim=lim
get_data,vnm+'_rot_deltamin',data=mindat,alim=lim
;mindat.y=mindat.y *180./!PI
dat.y = dat.y * 180./!PI        ; rad. --> deg. 
store_data,vnm+'_rot_waveangle',data=dat,dlim=lim
store_data,vnm+'_rot_deltamin',data=mindat,dlim=lim
options,vnm+'_rot_waveangle','ztitle','Normal Angle!C!C(deg.)!N!N'
options,vnm+'_rot_deltamin','ztitle','Uncertainty Angle!C!C(deg.)!N!N'

;==========================================
; Local Gyrofrequencies
;========================================== 
get_data, bfield+'_smooth', data=dat, alim=lim
   btot = sqrt(dat.y[*,0]^2+ $
               dat.y[*,1]^2+ $
               dat.y[*,2]^2)
   
   store_data,bfield+'_B', $
     data={x:dat.x,y:btot};, $
 ;    dlim={data_att:v_data_att}
  
;   tavg = 10.
;   average_tplot_variable,bfield+'_B',tavg
;   gyrof,bfield+'_B'

   gyrofreqhz=gyrof(btot,1,1)
      store_data, 'gyrofreq_h', data={x:dat.x,y:gyrofreqhz}, $
                                  dlim={colors:'white'}

   gyrofreqhz=gyrof(btot,4,1)
      store_data, 'gyrofreq_he', data={x:dat.x,y:gyrofreqhz}, $
                                  dlim={colors:'yellow'}

   gyrofreqhz=gyrof(btot,16,1)
      store_data, 'gyrofreq_o', data={x:dat.x,y:gyrofreqhz}, $
                                  dlim={colors:'green'}

;   options,'gyrof*','color',0;256 ; white
;   options,'gyrof*','thick',3
;   options,'gyrof*','style',2


tvar_spc_gyro = ['rbspb_emfisis_l3_hires_gse_Mag_tclip_filtered_rot_powspec',$ 
                 'gyrofreq_h','gyrofreq_he','gyrofreq_o'] 
store_data, tvar_spc_gyro[0]+'_gyro', data=tvar_spc_gyro, $ 
            dlim={yrange:[0.1,10],ylog:1,ystyle:1} 
;            dlim={yrange:[0.5,3],ylog:1,ystyle:1} 

tvar_plot = tvar_spc_gyro[0]+'_gyro' 

; Create plots

tplot_options, 'xmargin', [10,10]
tplot_options, 'ymargin', [4,2]
tplot_options, 'position', [ .2, .2, .8, .8]

options,'tvar_plot',ylog=1,yrange=[0.1,10.]
;options,'tvar_plot',ylog=1,yrange=[0.5,3.]
options,'tvar_plot',zlog=1,zrange=[0.1,10.]

tplot, [tvar_plot,tvar_plot,tvar_plot]
;tlimit, '2018-09-22/00:00:01','2018-09-22/23:59:59'
tlimit, '2014-05-09/00:00:01','2014-05-09/23:59:59'
;tlimit, '2014-05-09/20:00:00','2014-05-09/23:00:00'
;tlimit, '2014-05-09/20:00:00','2014-05-09/21:00:00'
;tlimit, '2018-08-16/20:00:00','2018-08-16/21:00:00'

popen,'./test_plot'
tplot
pclose

tplot, [tvar_plot]

tplot_names
;stop

;==========================================
; NaN noise, i.e., Deg. of Pol. >= a threshold, typically 0.6
;==========================================
var =     [vnm+'_rot_powspec',    $ 
           vnm+'_rot_degpol',   $
           vnm+'_rot_waveangle', $
           vnm+'_rot_elliptict']

;  for some reason, _rot_deltamin doesn't work and _rot_v1v2 isn't tplot_name
;           vnm+'_rot_waveangle',vnm+'_rot_deltamin',vnm+'_rot_v1v2', $



;nan_value = pwr_threshold
nan_value = 3.e-9 
;IF sat EQ 4 THEN nan_value = 5E-9
;IF sat EQ 2 THEN nan_value = 3E-9
;IF sat EQ 3 THEN nan_value = 4E-9
get_data,var[0],data=dat,alim=lim
inan = WHERE(dat.y LE nan_value, cnts);

nvar = N_ELEMENTS(var)
FOR i = 0,nvar-1 DO BEGIN
    print, var[i]
    get_data,var[i],data=dat,alim=lim
    IF (cnts GT 0) THEN dat.y[inan] = !VALUES.F_NAN 
    store_data,var[i],data=dat,dlim=lim
ENDFOR

; ===================================================
; Save variables
; ===================================================

; Save tplot variables. 
; To restore -- tplot_restore,filename='current.tplot'

cwd,'.'
tplot_save, filename='RBSP_tplot_variables_2014-05-09'

; Export to ASCII file

;tplot_ascii,'rbspb_emfisis_l3_hires_gse_lambda',filename='Lshell',trange=timerange(/current), dir='.',ext='_20180816'
;tplot_ascii,'rbspb_emfisis_l3_hires_gse_Mag_tclip_filtered_rot_powspec',filename='rbsp_powspec',trange=timerange(/current), dir='.',ext='_20180816'

;popen, 'rbsp_polarization_analysis_20121102_14001600.ps'

;tplot, [bfield, vnm+'_rot',var]

;pclose

;popen, './rbspa_polarization_analysis.ps'

;tplot

;pclose

END

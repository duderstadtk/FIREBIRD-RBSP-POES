;
; 
; Input: mag field tplot var.
;
; Written by: Robert C. Allen (rcc53@wildcats.unh.edu)
;

PRO polarization_analysis, bfield=bfield, f_low=f_low, f_high=f_high,pwr_threshold=pwr_threshold, sat=sat

vnm = bfield

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



;f_low  = 0.1
;f_high = 5.0
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
get_data, bfield, data=dat,alim=lim
   btot = sqrt(dat.y[*,0]^2+ $
               dat.y[*,1]^2+ $
               dat.y[*,2]^2)
   
   store_data,bfield+'_B', $
     data={x:dat.x,y:btot};, $
 ;    dlim={data_att:v_data_att}
   
   tavg = 10.
   average_tplot_variable,bfield+'_B',tavg
   gyrof,bfield+'_B'
   options,'gyrof*','color',0;256 ; white
   options,'gyrof*','thick',3
   options,'gyrof*','style',2

;==========================================
; NaN noise, i.e., Deg. of Pol. >= a threshold, typically 0.6
;==========================================
var =     [vnm+'_rot_powspec',    $ 
           vnm+'_rot_degpol',   $
           vnm+'_rot_waveangle',vnm+'_rot_deltamin',vnm+'_rot_v1v2', $
           vnm+'_rot_elliptict']

nan_value = pwr_threshold
;IF sat EQ 4 THEN nan_value = 5E-9
;IF sat EQ 2 THEN nan_value = 3E-9
;IF sat EQ 3 THEN nan_value = 4E-9
get_data,var[0],data=dat,alim=lim
inan = WHERE(dat.y LE nan_value, cnts);

nvar = N_ELEMENTS(var)
FOR i = 0,nvar-1 DO BEGIN
    get_data,var[i],data=dat,alim=lim
    IF (cnts GT 0) THEN dat.y[inan] = !VALUES.F_NAN 
    store_data,var[i],data=dat,dlim=lim
ENDFOR


;popen, 'rbsp_polarization_analysis_20121102_14001600.ps'

;tplot, [bfield, vnm+'_rot',var]

;pclose

;popen, './rbspa_polarization_analysis.ps'

;tplot

;pclose

END

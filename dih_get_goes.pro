;
;Name: dih_get_goes
;
;Purpose: gets goes data and saves it into a text file
;
;Inputs: start and end time strings in format 'day-month(abbreviation)-year hours:minutes:seconds.microseconds', save_name -> name for txt file for goes data
;
;Outputs: text file with two columns of time,flux data for goes along with a header containing the first time
;
;Example: dih_get_goes, '01-May-2012 00:00:00.00','02-May-2012 00:00:00.00','goes_curve.txt'
;
;Written: 7/30/14 Dan Herman daniel.herman@cfa.harvard.edu
;
;
pro dih_get_goes, start_time, end_time, save_name
catch, Error_status
IF Error_status NE 0 THEN BEGIN
      PRINT, 'Error index: ', Error_status
      PRINT, 'Error message: ', !ERROR_STATE.MSG
      CATCH, /CANCEL
      return
   END
rd_goes_sdac, stime= start_time ,etime=end_time, tarray=goes_time, yarray=goes_flux, base_ascii=base_ascii
time_str =  atime(goes_time+anytim(base_ascii))
new_time = goes_time - goes_time[0]
real_start = atime(goes_time[0]+anytim(base_ascii))
openw, unit, save_name, /get_lun
printf, unit, real_start
for i=0,n_elements(goes_time)-1 do printf, unit, new_time[i], goes_flux[i,0]
close, unit, /all
end
;ubs = dih_data_131_goes_routine('/data/george/hwinter/data/Flare_Detective_Data/Event_Stacks/Working','aia_data3_block','goes131pairtest5',['sunnymoney_goes131comtest2','aia_data_block_goes131pairtest','aia_data2_block_goes131pairtest78'],'quattro_test5_131goesbatch')
;aia_mkmovie, '2014-07-10 19:00','2014-07-10 19:35',[171,131],cutout = [ 1281,  1409,  2177,  2305], /multi_panel
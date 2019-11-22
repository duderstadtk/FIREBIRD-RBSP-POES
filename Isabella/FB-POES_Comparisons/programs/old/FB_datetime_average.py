'''
Filename:
    FB_datetime_average.py   ---> this is a temporary name

Authors:
    Isabella M. Householder & Katharine A. Duderstadt
    
Synposis:
    Calculate average of FIREBIRD energetic electron counts of each energy channel
    
Date:
    20 August 2019
    
Description:
    Read in FIREBIRD files as comma separated plain text (.txt) saved from Autoplot
    ............

-------------------------------------------------------------------------------
'''
import datetime
import numpy as np

filename = 'FU3_2018-09-22_1945-1948.txt'

#------------------- reads in file and creates list of data -------------------
def read_data(filename):
    dataList = []
    try:
        file = open(filename, 'r')
    except:
        print('The file may not exist or the program may have not have been able to open it.')
        return([])
    else:
        file = open(filename, 'r')
        for line in file:
            line = line.strip().split(',')
            dataList.append(line)
    file.close()
    return dataList

#---------- calculates average of FB counts for each energy channel -----------
def calc_average(dataList):
    last_time = None
    timestamp_list = []
    av1_list = []
    av2_list = []
    av3_list = []
    av4_list = []
    av5_list = []
    av6_list = []
    col1_list = []
    col2_list = []
    col3_list = []
    col4_list = []
    col5_list = []
    col6_list = []
    count = 0
    oldcount = 0
    count_second = 0
    oldcount_second = 0
    
    for row in dataList:
        print('count = ', count)
        col1_list.append(float(row[1]))
        col2_list.append(float(row[2]))
        col3_list.append(float(row[3]))
        col4_list.append(float(row[4]))
        col5_list.append(float(row[5]))
        col6_list.append(float(row[6])) 
        if count == 0:
            last_time = datetime.datetime.strptime(row[0], '%Y-%m-%dT%H:%M:%S.%fZ')
            curr_time = last_time
            oldcount_second = curr_time.second
            count_second = curr_time.second
            count += 1
        else:
            curr_time = datetime.datetime.strptime(row[0], '%Y-%m-%dT%H:%M:%S.%fZ')
            count_second = curr_time.second
            if (count_second == oldcount_second + 1) or (oldcount_second == 59 and count_second == 0):
               last_time_str = last_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
               timestamp_list.append(last_time_str)
               last_time = curr_time
               
               col1_array = np.array(col1_list[oldcount:count])
               print('oldcount_second = ', oldcount_second)

               all_zeros1 = not np.any(col1_array)
               if all_zeros1 == True:
                   average1 = np.mean(col1_array)
                   av1_list.append(average1)
               else:
                   col1_array[col1_array==0] = np.nan
                   average1 = np.nanmean(col1_array)
                   average1 = round(average1, 2)
                   av1_list.append(average1)
               print('col1_array =', col1_array, ' average =', average1)
                
               col2_array = np.array(col2_list[oldcount:count])
               all_zeros2 = not np.any(col2_array)
               if all_zeros2 == True:
                   average2 = np.mean(col2_array)
                   av2_list.append(average2)
               else:
                   col2_array[col2_array==0] = np.nan
                   average2 = np.nanmean(col2_array)
                   average2 = round(average2, 2)
                   av2_list.append(average2)
               print('col2_array =', col2_array, ' average =', average2)

               col3_array = np.array(col3_list[oldcount:count])
               all_zeros3 = not np.any(col3_array)
               if all_zeros3 == True:
                   average3 = np.mean(col3_array)
                   av3_list.append(average3)
               else:
                   col3_array[col3_array==0] = np.nan
                   average3 = np.nanmean(col3_array)
                   average3 = round(average3, 2)
                   av3_list.append(average3)
               
               col4_array = np.array(col4_list[oldcount:count])
               all_zeros4 = not np.any(col4_array)
               if all_zeros4 == True:
                   average4 = np.mean(col4_array)
                   av4_list.append(average4)
               else:
                   col4_array[col4_array==0] = np.nan
                   average4 = np.nanmean(col4_array)
                   average4 = round(average4, 2)
                   av4_list.append(average4)
                
               col5_array = np.array(col5_list[oldcount:count])
               all_zeros5 = not np.any(col5_array)
               if all_zeros5 == True:
                   average5 = np.mean(col5_array)
                   av5_list.append(average5)
               else:
                   col5_array[col5_array==0] = np.nan
                   average5 = np.nanmean(col5_array)
                   average5 = round(average5, 2)
                   av5_list.append(average5)  
                   
               col6_array = np.array(col6_list[oldcount:count])
               all_zeros6 = not np.any(col6_array)
               if all_zeros6 == True:
                   average6 = np.mean(col6_array)
                   av6_list.append(average6)
               else:
                   col6_array[col6_array==0] = np.nan
                   average6 = np.nanmean(col6_array)
                   average6 = round(average6, 2)
                   av6_list.append(average6)
                
               oldcount = count
               oldcount_second = count_second

            count += 1
    
    return timestamp_list, av1_list, av2_list, av3_list, av4_list, av5_list, av6_list 

#---------- prints timestamps and average calculations to .txt file -----------
def main():
    data = read_data(filename)
    
    np.savetxt('sec-avg_FU3_2018-09-22_1945-1948.txt', np.column_stack(calc_average(data)), fmt='%s', delimiter=', ')
    print('Complete.')
    
main()



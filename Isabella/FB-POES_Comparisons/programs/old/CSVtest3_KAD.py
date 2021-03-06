'''
Filename:
    CSVtest3_KAD.py   ---> this is a temporary name

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

import csv
import datetime

f_reader = csv.reader('''
2018-09-18T01:34:55.762Z,6.0,2.0,0.0,0.0,1.0,0.0
2018-09-18T01:34:55.812Z,8.0,0.0,1.0,0.0,0.0,1.0
2018-09-18T01:34:55.862Z,9.0,2.0,0.0,0.0,1.0,1.0
2018-09-18T01:34:55.912Z,6.0,1.0,0.0,0.0,0.0,1.0
2018-09-18T01:34:55.962Z,4.0,2.0,0.0,0.0,0.0,0.0
2018-09-18T01:34:56.012Z,9.0,1.0,0.0,0.0,0.0,0.0
2018-09-18T01:34:56.062Z,8.0,3.0,0.0,0.0,0.0,0.0
2018-09-18T01:34:56.112Z,8.0,2.0,2.0,0.0,0.0,0.0
2018-09-18T01:34:56.162Z,12.0,1.0,0.0,0.0,0.0,1.0
2018-09-18T01:34:56.212Z,13.0,0.0,0.0,0.0,0.0,0.0
2018-09-18T01:34:56.262Z,15.0,0.0,0.0,1.0,0.0,0.0
2018-09-18T01:34:56.312Z,9.0,0.0,0.0,0.0,1.0,0.0
2018-09-18T01:34:56.362Z,11.0,1.0,0.0,0.0,1.0,1.0
2018-09-18T01:34:56.412Z,10.0,0.0,0.0,0.0,0.0,0.0
2018-09-18T01:34:56.462Z,10.0,0.0,0.0,0.0,0.0,0.0
2018-09-18T01:34:56.512Z,6.0,2.0,0.0,0.0,0.0,1.0
2018-09-18T01:34:56.562Z,7.0,0.0,0.0,0.0,0.0,1.0
2018-09-18T01:34:56.612Z,6.0,2.0,0.0,0.0,0.0,2.0
2018-09-18T01:34:56.662Z,8.0,1.0,1.0,0.0,0.0,3.0
2018-09-18T01:34:56.712Z,7.0,2.0,0.0,2.0,0.0,0.0
2018-09-18T01:34:56.762Z,9.0,1.0,0.0,1.0,0.0,0.0
2018-09-18T01:34:56.812Z,11.0,1.0,0.0,0.0,0.0,0.0
2018-09-18T01:34:56.862Z,11.0,0.0,0.0,0.0,0.0,0.0
2018-09-18T01:34:56.912Z,6.0,2.0,0.0,1.0,0.0,0.0
2018-09-18T01:34:56.962Z,13.0,1.0,0.0,1.0,0.0,2.0
2018-09-18T01:34:57.012Z,8.0,2.0,0.0,0.0,1.0,0.0
2018-09-18T01:34:57.062Z,13.0,0.0,0.0,0.0,1.0,2.0
2018-09-18T01:34:57.112Z,13.0,0.0,0.0,0.0,0.0,1.0
2018-09-18T01:34:57.162Z,6.0,1.0,0.0,1.0,0.0,0.0
2018-09-18T01:34:57.212Z,12.0,1.0,0.0,1.0,0.0,0.0
2018-09-18T01:34:57.262Z,9.0,0.0,0.0,1.0,0.0,0.0
2018-09-18T01:34:57.312Z,12.0,0.0,0.0,0.0,0.0,0.0
2018-09-18T01:34:57.362Z,13.0,0.0,0.0,0.0,0.0,0.0
2018-09-18T01:34:57.412Z,11.0,2.0,0.0,0.0,0.0,0.0
2018-09-18T01:34:57.462Z,7.0,2.0,0.0,1.0,0.0,1.0
2018-09-18T01:34:57.512Z,12.0,1.0,0.0,0.0,0.0,1.0
2018-09-18T01:34:57.562Z,6.0,0.0,0.0,0.0,1.0,0.0
2018-09-18T01:34:57.612Z,6.0,2.0,0.0,0.0,0.0,0.0
2018-09-18T01:34:57.662Z,6.0,0.0,0.0,0.0,1.0,0.0
2018-09-18T01:34:57.712Z,11.0,0.0,0.0,0.0,1.0,0.0
2018-09-18T01:34:57.762Z,8.0,1.0,0.0,0.0,0.0,0.0
2018-09-18T01:34:57.812Z,7.0,0.0,0.0,0.0,0.0,1.0
2018-09-18T01:34:57.862Z,12.0,0.0,0.0,0.0,0.0,0.0
2018-09-18T01:34:57.912Z,7.0,1.0,1.0,0.0,0.0,0.0
2018-09-18T01:34:57.962Z,8.0,2.0,0.0,0.0,0.0,1.0
2018-09-18T01:34:58.012Z,10.0,1.0,0.0,0.0,0.0,1.0
2018-09-18T01:34:58.062Z,7.0,1.0,2.0,0.0,0.0,0.0
2018-09-18T01:34:58.112Z,11.0,2.0,0.0,0.0,0.0,0.0
2018-09-18T01:34:58.162Z,16.0,1.0,0.0,0.0,0.0,0.0
2018-09-18T01:34:58.212Z,10.0,0.0,0.0,0.0,0.0,2.0
2018-09-18T01:34:58.262Z,8.0,0.0,0.0,1.0,0.0,1.0
2018-09-18T01:34:58.312Z,11.0,2.0,0.0,0.0,0.0,2.0
2018-09-18T01:34:58.362Z,12.0,1.0,0.0,1.0,1.0,1.0
2018-09-18T01:34:58.412Z,11.0,2.0,0.0,1.0,1.0,1.0
2018-09-18T01:34:58.462Z,8.0,0.0,0.0,0.0,1.0,1.0
2018-09-18T01:34:58.512Z,11.0,1.0,0.0,0.0,0.0,0.0
2018-09-18T01:34:58.562Z,10.0,1.0,0.0,0.0,1.0,0.0
2018-09-18T01:34:58.612Z,10.0,1.0,0.0,0.0,0.0,0.0
    '''.strip().splitlines(), delimiter=',')

last_time = None
col1 = []
col2 = []
col3 = []
col4 = []
col5 = []
col6 = []
count = 0
oldcount_second = 0

for row in f_reader:
    if count == 0:
        last_time = datetime.datetime.strptime(row[0], '%Y-%m-%dT%H:%M:%S.%fZ')
        curr_time = last_time
        new_time = last_time
        oldcount_second = curr_time.second
        count_second = curr_time.second
        count = count+1
        col1.append(float(row[1]))
        col2.append(float(row[2]))
        col3.append(float(row[3]))
        col4.append(float(row[4]))
        col5.append(float(row[5]))
        col6.append(float(row[6]))  
        print('test 2')
    else:
        col1.append(float(row[1]))
        col2.append(float(row[2]))
        col3.append(float(row[3]))
        col4.append(float(row[4]))
        col5.append(float(row[5]))
        col6.append(float(row[6]))  
        print('test 3')
        if count_second == oldcount_second + 1:
           print('test 4')
           print('this is count second')
           print(count_second)
           print('this is oldcount_second')
           print(oldcount_second)
           print('''
           averages from '{last}' to '{new}'
           av1:   {av1:06.1f}
           av2:   {av2:06.1f}
           av3:   {av3:06.1f}
           av4:   {av4:06.1f}
           av5:   {av5:06.1f}
           av6:   {av6:06.1f}
           '''.format(
              last=last_time, new=new_time,
              av1=sum(col1) / len(col1), 
              av2=sum(col2) / len(col2),
              av3=sum(col3) / len(col3),
              av4=sum(col4) / len(col4),
              av5=sum(col5) / len(col5),
              av6=sum(col6) / len(col6),
              ).lstrip())
           last_time = curr_time
           print('test 5')

        oldcount_second = count_second
        new_time = curr_time 
        curr_time = datetime.datetime.strptime(row[0], '%Y-%m-%dT%H:%M:%S.%fZ')
        count_second = curr_time.second
        print(new_time)
        print('test 6')
        '''
        print('this is count second')
        print(count_second)
        print('this is oldcount second')
        print(oldcount_second)
        '''
        count += 1
        print('test 7')
        
        print('this is oldcount_second')
        print(oldcount_second)
        print('this is count_second')
        print(count_second)
        
print('this is count at end of all iterations')
print(count)

print('\n')
print('these are columns')
print(col1)
print('\n')
print(col2)
print('\n')
print(col3)
print('\n')
print(col4)
print('\n')
print(col5)
print('\n')
print(col6)






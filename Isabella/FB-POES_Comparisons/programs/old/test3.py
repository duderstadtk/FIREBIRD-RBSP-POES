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
    '''.strip().splitlines(), delimiter=',')

last_time = None
count = 0
oldcount_second = 0

for row in f_reader:
    current_time = datetime.datetime.strptime(row[0], '%Y-%m-%dT%H:%M:%S.%fZ')
    print(current_time)
    count += 1
    
    if count == 1:
        oldcount_second = current_time.second
        print('this is count second')
        print(oldcount_second)
        
    count_second = current_time.second
    
    if count_second == oldcount_second + 1:
        print('yes')
        oldcount_second = count_second
        
'''    
    if count == count + 1:
        count_second = current_time.second
        print('this is still count second')
        print(count_second)
        
        
        if count != 1:
            count_second = current_time.secomd
            print('this is still count second')
            print(count_second)
'''
 
        








        
        
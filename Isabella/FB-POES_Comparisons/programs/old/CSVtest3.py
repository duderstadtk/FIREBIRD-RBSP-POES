#import csv
import datetime

'''
with open('test.csv', 'r') as csvfile:
    f_reader = csv.reader(csvfile, delimiter',')
    for row in f_reader:
        print(row)
'''

last_time = None
col1 = []
col2 = []
col3 = []
col4 = []
col5 = []
col6 = []

for row in f_reader:
    current_time = datetime.datetime.strptime(row[0], '%Y-%m-%dT%H:%M:%S.%fZ')
    #print('this is current time')
    print(current_time)
    
    if last_time is None:
        last_time = current_time
        #print('this is last time')
        #print(last_time)
    
        
    col1.append(float(row[1]))
    col2.append(float(row[2]))
    col3.append(float(row[3]))
    col4.append(float(row[4]))
    col5.append(float(row[5]))
    col6.append(float(row[6]))  
    
    if (current_time - last_time) > datetime.timedelta(seconds=1):
        print('''
averages from '{last}' to '{curr}'
    av1:   {av1:06.1f}
    av2:   {av2:06.1f}
    av3:   {av3:06.1f}
    av4:   {av4:06.1f}
    av5:   {av5:06.1f}
    av6:   {av6:06.1f}
    '''.format(
        last=last_time, curr=current_time,
        av1=sum(col1) / len(col1),
        av2=sum(col2) / len(col2),
        av3=sum(col3) / len(col3),
        av4=sum(col4) / len(col4),
        av5=sum(col5) / len(col5),
        av6=sum(col6) / len(col6),
    ).lstrip())

        last_time = current_time
        print('this is last time')
        print(last_time)
    
        col1 = []
        col2 = []
        col3 = []       
        col4 = []
        col5 = []
        col6 = []

'''
print('\n')
print('current time - last time')
print(current_time - last_time)
print('\n')
print('this is timedelta')
print(datetime.timedelta(seconds=1))

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
'''       

### intervals of time always start from 2018-09-18 01:34:55.762000 ###

# floor function to round ms to 0
        
        
        
        
        
        
        
        
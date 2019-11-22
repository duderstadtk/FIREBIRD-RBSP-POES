import pandas as pd
import matplotlib.pyplot as plt

data = {'drawing': [{'subject': 'tiger', 'points': [{'dates': '2016-12-31', 'values': 36.0}, {'dates': '2017-01-01', 'values': 34.0}, {'dates': '2017-01-02', 'values': 50.0}, {'dates': '2017-01-03', 'values': 20.0}, {'dates': '2017-01-04', 'values': 27.0}, {'dates': '2017-01-05', 'values': 55.0}, {'dates': '2017-01-06', 'values': 34.0}, {'dates': '2017-01-07', 'values': 23.0}, {'dates': '2017-01-08', 'values': 25.0}, {'dates': '2017-01-09', 'values': 74.0}, {'dates': '2017-01-10', 'values': 43.0}, {'dates': '2017-01-11', 'values': 31.0}, {'dates': '2017-01-12', 'values': 19.0}, {'dates': '2017-01-13', 'values': 34.0}, {'dates': '2017-01-14', 'values': 55.0}, {'dates': '2017-01-15', 'values': 19.0}, {'dates': '2017-01-16', 'values': 19.0}, {'dates': '2017-01-17', 'values': 32.0}, {'dates': '2017-01-18', 'values': 26.0}, {'dates': '2017-01-19', 'values': 40.0}, {'dates': '2017-01-20', 'values': 24.0}, {'dates': '2017-01-21', 'values': 52.0}, {'dates': '2017-01-22', 'values': 25.0}, {'dates': '2017-01-23', 'values': 56.0}, {'dates': '2017-01-24', 'values': 66.0}, {'dates': '2017-01-25', 'values': 19.0}, {'dates': '2017-01-26', 'values': 50.0}, {'dates': '2017-01-27', 'values': 23.0}, {'dates': '2017-01-28', 'values': 50.0}, {'dates': '2017-01-29', 'values': 30.0}, {'dates': '2017-01-30', 'values': 43.0}, {'dates': '2017-01-31', 'values': 37.0}, {'dates': '2017-02-01', 'values': 58.0}, {'dates': '2017-02-02', 'values': 30.0}, {'dates': '2017-02-03', 'values': 23.0}, {'dates': '2017-02-04', 'values': 100.0}, {'dates': '2017-02-05', 'values': 25.0}, {'dates': '2017-02-06', 'values': 37.0}, {'dates': '2017-02-07', 'values': 57.0}, {'dates': '2017-02-08', 'values': 31.0}, {'dates': '2017-02-09', 'values': 19.0}, {'dates': '2017-02-10', 'values': 38.0}, {'dates': '2017-02-11', 'values': 34.0}, {'dates': '2017-02-12', 'values': 19.0}, {'dates': '2017-02-13', 'values': 38.0}, {'dates': '2017-02-14', 'values': 29.0}, {'dates': '2017-02-15', 'values': 26.0}, {'dates': '2017-02-16', 'values': 27.0}, {'dates': '2017-02-17', 'values': 37.0}, {'dates': '2017-02-18', 'values': 34.0}, {'dates': '2017-02-19', 'values': 47.0}, {'dates': '2017-02-20', 'values': 39.0}, {'dates': '2017-02-21', 'values': 25.0}, {'dates': '2017-02-22', 'values': 38.0}, {'dates': '2017-02-23', 'values': 32.0}, {'dates': '2017-02-24', 'values': 25.0}, {'dates': '2017-02-25', 'values': 63.0}, {'dates': '2017-02-26', 'values': 39.0}, {'dates': '2017-02-27', 'values': 27.0}]}, {'term': 'elephant', 'points': [{'dates': '2016-12-31', 'values': 24.0}, {'dates': '2017-01-01', 'values': 20.0}, {'dates': '2017-01-02', 'values': 20.0}, {'dates': '2017-01-03', 'values': 20.0}, {'dates': '2017-01-04', 'values': 0.0}, {'dates': '2017-01-05', 'values': 0.0}, {'dates': '2017-01-06', 'values': 23.0}, {'dates': '2017-01-07', 'values': 22.0}, {'dates': '2017-01-08', 'values': 46.0}, {'dates': '2017-01-09', 'values': 19.0}, {'dates': '2017-01-10', 'values': 19.0}, {'dates': '2017-01-11', 'values': 0.0}, {'dates': '2017-01-12', 'values': 19.0}, {'dates': '2017-01-13', 'values': 23.0}, {'dates': '2017-01-14', 'values': 22.0}, {'dates': '2017-01-15', 'values': 19.0}, {'dates': '2017-01-16', 'values': 0.0}, {'dates': '2017-01-17', 'values': 19.0}, {'dates': '2017-01-18', 'values': 29.0}, {'dates': '2017-01-19', 'values': 0.0}, {'dates': '2017-01-20', 'values': 0.0}, {'dates': '2017-01-21', 'values': 0.0}, {'dates': '2017-01-22', 'values': 36.0}, {'dates': '2017-01-23', 'values': 19.0}, {'dates': '2017-01-24', 'values': 19.0}, {'dates': '2017-01-25', 'values': 19.0}, {'dates': '2017-01-26', 'values': 0.0}, {'dates': '2017-01-27', 'values': 0.0}, {'dates': '2017-01-28', 'values': 22.0}, {'dates': '2017-01-29', 'values': 18.0}, {'dates': '2017-01-30', 'values': 19.0}, {'dates': '2017-01-31', 'values': 37.0}, {'dates': '2017-02-01', 'values': 29.0}, {'dates': '2017-02-02', 'values': 20.0}, {'dates': '2017-02-03', 'values': 47.0}, {'dates': '2017-02-04', 'values': 0.0}, {'dates': '2017-02-05', 'values': 28.0}, {'dates': '2017-02-06', 'values': 18.0}, {'dates': '2017-02-07', 'values': 38.0}, {'dates': '2017-02-08', 'values': 28.0}, {'dates': '2017-02-09', 'values': 39.0}, {'dates': '2017-02-10', 'values': 0.0}, {'dates': '2017-02-11', 'values': 23.0}, {'dates': '2017-02-12', 'values': 37.0}, {'dates': '2017-02-13', 'values': 19.0}, {'dates': '2017-02-14', 'values': 39.0}, {'dates': '2017-02-15', 'values': 0.0}, {'dates': '2017-02-16', 'values': 20.0}, {'dates': '2017-02-17', 'values': 24.0}, {'dates': '2017-02-18', 'values': 23.0}, {'dates': '2017-02-19', 'values': 38.0}, {'dates': '2017-02-20', 'values': 0.0}, {'dates': '2017-02-21', 'values': 19.0}, {'dates': '2017-02-22', 'values': 19.0}, {'dates': '2017-02-23', 'values': 64.0}, {'dates': '2017-02-24', 'values': 37.0}, {'dates': '2017-02-25', 'values': 24.0}, {'dates': '2017-02-26', 'values': 29.0}, {'dates': '2017-02-27', 'values': 40.0}]}]}

df1 = pd.DataFrame(data['drawing'][0]['points'])
df2 = pd.DataFrame(data['drawing'][1]['points'])

# Put the two together.
# Simple concat in your specific case since the data
# is already sorted and balanced
df = pd.concat([df1, df2['values']], axis=1)

# column names
df.columns = ['date',
              data['drawing'][0]['subject'],
              data['drawing'][1]['term']] # you use both 'subject' and 'term'

# Need datetime format for ease of plotting
df['date'] = pd.to_datetime(df['date'])


# Then the matplotlib stuff ...
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

ax.plot(df['date'], df[df.columns[1]])
ax.plot(df['date'], df[df.columns[2]])

plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
plt.tight_layout()
plt.legend()

fig.savefig('output.png', dpi=200)
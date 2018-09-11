import pandas as pd
import datetime
import matplotlib

matplotlib.use('agg')
import matplotlib.pyplot as plt
#import matplotlib.dates as md


data_type = {'BM': bool}
df = pd.read_csv('data.csv', dtype=data_type,
        index_col=0, parse_dates=[0],
        skipinitialspace=True, keep_default_na=False)
df.rename(columns={'Volume (oz)': 'Vol'}, inplace=True)

dates = df.index.date
times = df.index.time
vol = df.Vol.values ** 2
day = datetime.timedelta(days=1)

plt.scatter(dates, times, s=vol)
#plt.gca().set_ylabel('Volumes (oz)')
plt.ylabel('Volume (oz)')
plt.gcf().autofmt_xdate()
ax = plt.gca()
ax.set_xlim([min(dates)-day, max(dates)+day])
hours = [datetime.datetime.combine(datetime.date.today(), datetime.time(i)) for i in range(24)]
hours = [datetime.time(i) for i in range(0,24,2)]
plt.yticks(hours)
ax.grid(True, axis='y', linestyle='--')
ax.invert_yaxis()
plt.savefig('image.png')

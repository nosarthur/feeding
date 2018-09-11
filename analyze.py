import pandas as pd
import datetime
import matplotlib

matplotlib.use('agg')
import matplotlib.pyplot as plt
#import matplotlib.dates as md

# load data
data_type = {'BM': bool}
df = pd.read_csv(
    'data.csv',
    dtype=data_type,
    index_col=0,
    parse_dates=[0],
    skipinitialspace=True,
    keep_default_na=False)
df.rename(columns={'Volume (oz)': 'Vol'}, inplace=True)

# plot
bm = df.loc[df.BM]
formula = df.loc[df.BM == False]
for d, color, text in zip([bm, formula], ['g', 'r'],
                          ['breast milk', 'formula']):
    dates = d.index.date
    times = d.index.time
    vol = df.Vol.values**2
    day = datetime.timedelta(days=1)
    plt.scatter(dates, times, s=vol, c=color, label=text)

#plt.gca().set_ylabel('Hour')
plt.ylabel('Hour')
plt.gcf().autofmt_xdate()
ax = plt.gca()
ax.set_xlim([min(dates) - day * 2, max(dates) + day])
hours = [datetime.time(i) for i in range(0, 24, 2)]
ax.set_ylim([hours[0], datetime.time(23, 59, 59)])
plt.yticks(hours)
ax.grid(True, axis='y', linestyle='--')
ax.invert_yaxis()
plt.legend(loc='upper left')
plt.savefig('image.png')

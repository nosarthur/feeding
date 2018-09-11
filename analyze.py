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

# plot daily feeding quantity
ax1 = plt.subplot(211)
dates = df.index.date
by_date = df.groupby(dates).sum()
# bar plot doesn't work out of box because the x-axis is date and it is measured
# with respect to 1970
by_date.Vol.plot(style='bo--')
plt.ylabel('feed (oz)')

# plot daily feeding pattern
ax2 = plt.subplot(212, sharex=ax1)
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
ax2.set_xlim([min(dates) - day * 2, max(dates) + day])
hours = [datetime.time(i) for i in range(0, 24, 2)]
ax2.set_ylim([hours[0], datetime.time(23, 59, 59)])
plt.yticks(hours)
ax2.grid(True, axis='y', linestyle='--')
ax2.invert_yaxis()
plt.legend(loc='upper left')
plt.savefig('image.png')

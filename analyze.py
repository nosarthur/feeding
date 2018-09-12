import pandas as pd
import numpy as np
import datetime
import matplotlib

matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
#import matplotlib.dates as md

# load data
data_type = {'BM': bool}
df = pd.read_csv(
    'feed.csv',
    dtype=data_type,
    index_col=0,
    parse_dates=[0],
    skipinitialspace=True,
    keep_default_na=False)
df.rename(columns={'Volume (oz)': 'Vol'}, inplace=True)

stool = pd.read_csv('stool.csv',
    parse_dates=[0],
    index_col=0,
    )

fig = plt.figure(figsize=(8, 6))

# plot daily stool count
ax1 = plt.subplot(411)
#ax1 = plt.subplot2grid((6, 1), (0, 0))
ax1.grid(True, axis='y', linestyle='--')
plt.plot(stool.index.date, stool.Count.values, 'o--')
plt.ylabel('Stools')
loc = plticker.MultipleLocator(base=3.0) # this locator puts ticks at regular intervals
ax1.yaxis.set_major_locator(loc)
plt.ylim([0, max(stool.Count.values)+1])

# plot daily feeding quantity
ax2 = plt.subplot(412, sharex=ax1)
#ax2 = plt.subplot2grid((6, 1), (1, 0), rowspan=2, sharex=ax1)
dates = df.index.date
by_date = pd.pivot_table(
    df,
    values='Vol',
    index=dates,
    columns=['BM'],
    aggfunc=np.sum,
    fill_value=0)
# Pandas bar plot doesn't work out of box, see link below
# https://stackoverflow.com/questions/49269927/missing-bars-in-matplotlib-bar-chart
plt.bar(
    by_date.index,
    by_date[True].values,
    bottom=by_date[False].values,
    label='breast milk',
    color='g')
plt.bar(by_date.index, by_date[False].values, label='formula', color='r')
plt.ylabel('Feed (oz)')
plt.legend(loc='upper left')
loc = plticker.MultipleLocator(base=5.0) # this locator puts ticks at regular intervals
ax2.yaxis.set_major_locator(loc)

# plot daily feeding pattern
#ax3 = plt.subplot2grid((6, 1), (3, 0), rowspan=3, sharex=ax1)
ax3 = plt.subplot(212, sharex=ax1)
bm = df.loc[df.BM]
formula = df.loc[df.BM == False]
for d, color, text in zip([bm, formula], ['g', 'r'],
                          ['breast milk', 'formula']):
    dates = d.index.date
    times = d.index.time
    vol = d.Vol.values**2
    day = datetime.timedelta(days=1)
    plt.scatter(dates, times, s=vol, c=color, label=text)

plt.ylabel('Hour')
ax3.set_xlim([min(dates) - day * 2, max(dates) + day])
hours = [datetime.time(i) for i in range(0, 24, 2)]
ax3.set_ylim([hours[0], datetime.time(23, 59, 59)])
plt.yticks(hours)
ax3.grid(True, axis='y', linestyle='--')
ax3.invert_yaxis()
plt.legend(loc='upper left')
plt.gcf().autofmt_xdate()
plt.tight_layout(pad=0, w_pad=0, h_pad=0)
plt.savefig('image.png')

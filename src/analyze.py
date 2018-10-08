"""
Plot Luke's feeding pattern
"""

import pandas as pd
import numpy as np
import datetime
import matplotlib
matplotlib.use('agg')  # for ChromeOS

import matplotlib.pyplot as plt
from matplotlib import gridspec
#import matplotlib.dates as md

import utils

# ------------- load data ---------------------------------
df1 = utils.load_feedings()

df2 = pd.read_csv(
    utils.fullpath('weight_stool.csv'),
    parse_dates=[0],
    index_col=0,
)
df2.rename(
    columns={
        'Stool (count)': 'Stool',
        'Weight (kg)': 'Weight'
    }, inplace=True)

weight_guide = pd.read_csv(
    utils.fullpath('WHO_weight_guideline_boy_13weeks.txt'),
    index_col=0,
    delim_whitespace=True,
)

# ----------- figure setup --------------------------------
fig = plt.figure(figsize=(8, 7))
gs = gridspec.GridSpec(nrows=4, ncols=1, height_ratios=[2, 1, 2, 3])
dates = df2.index.date
one_day = datetime.timedelta(days=1)

# ----------- plot daily stool count -----------------------
ax2 = fig.add_subplot(gs[1])
ax2.grid(True, axis='y', linestyle='--')
plt.plot(dates, df2.Stool.values, 'o--', clip_on=False)
plt.ylabel('Stools')
utils.set_y_major(3)
#ax2.set_xticks(df2.index.date, minor=True)
plt.ylim([0, max(df2.Stool.values) + 1])

# ----------- plot weight change -----------------------
ax1 = fig.add_subplot(gs[0], sharex=ax2)
weight = df2.Weight.dropna()
plt.plot(weight.index.date, weight.values, 'o', clip_on=False, label='Luke')
plt.ylabel('Weight (kg)')
utils.set_y_major(0.5)
ax1.grid(True, axis='y', linestyle='--')
plt.ylim([3.25, max(weight.values) + 1])

# plot percentile guide
guide_date = [
    weight.index.date[0] + 7 * one_day * i for i in weight_guide.index
]
plt.plot(
    guide_date,
    weight_guide.P75.values,
    'go:',
    fillstyle='none',
    label='75 percentile')
plt.plot(
    guide_date,
    weight_guide.P50.values,
    'bo:',
    fillstyle='none',
    label='50 percentile')
plt.plot(
    guide_date,
    weight_guide.P25.values,
    'ro:',
    fillstyle='none',
    label='25 percentile')
plt.legend(loc='upper left')

# ----------- plot daily feeding quantity --------------------
ax3 = fig.add_subplot(gs[2], sharex=ax2)
by_date = pd.pivot_table(
    df1,
    values='Vol',
    index=df1.index.date,
    columns=['BM'],
    aggfunc=np.sum,
    fill_value=0)
# Pandas bar plot doesn't work out of box, see link below
# https://stackoverflow.com/questions/49269927/missing-bars-in-matplotlib-bar-chart
rects_bm = plt.bar(
    by_date.index,
    by_date[True].values,
    bottom=by_date[False].values,
    #    width=0.3,
    label='breast milk',
    color='g')
rects_f = plt.bar(
    by_date.index, by_date[False].values, label='formula', color='r')
utils.autolabel(rects_bm, rects_f)

plt.ylabel('Feed (oz)')
plt.legend(loc='upper left')
utils.set_y_major(10)

# ------------ plot daily feeding pattern -----------------
#ax4 = plt.subplot2grid((6, 1), (3, 0), rowspan=3, sharex=ax2)
#ax4 = plt.subplot(212, sharex=ax2)
ax4 = fig.add_subplot(gs[3], sharex=ax2)
bm = df1.loc[df1.BM]
formula = df1.loc[df1.BM == False]
for d, color, text in zip([bm, formula], ['g', 'r'],
                          ['breast milk', 'formula']):
    date = d.index.date
    times = d.index.time
    vol = d.Vol.values**2
    plt.scatter(date, times, s=vol, c=color, label=text)

plt.ylabel('Hour')
hours = [datetime.time(i) for i in range(0, 24, 2)]
plt.yticks(hours)
ax4.set_ylim([hours[0], datetime.time(23, 59, 59)])
ax4.grid(True, axis='y', linestyle='--')
ax4.invert_yaxis()
plt.legend(loc='upper left')

# ------------ overall plot control ----------------
plt.tight_layout(
    pad=0.5,
    w_pad=0,
    h_pad=0,
)
plt.xlim([dates[0], dates[-1] + one_day])
fig.autofmt_xdate()
plt.savefig('image.png')

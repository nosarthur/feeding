import pandas as pd
from pathlib import Path
import matplotlib
matplotlib.use('agg')  # for ChromeOS
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker


def autolabel(rects1, rects2):
    """
    Attach a text label above each bar displaying its height
    """
    ca = plt.gca()
    for r1, r2 in zip(rects1, rects2):
        height = r1.get_height() + r2.get_height()
        ca.text(r1.get_x() + r1.get_width()/2., 1.05*height,
                '%d' % int(round(height)),
                ha='center', va='bottom')

    # give room for the label
    ymin, ymax = ca.get_ylim()
    plt.ylim([ymin, ymax + 8])


def set_y_major(base):
    loc = plticker.MultipleLocator(
        base=base)  # this locator puts ticks at regular intervals
    plt.gca().yaxis.set_major_locator(loc)


def fullpath(fname):
    """
    return full path of the data file
    """
    return Path(__file__).parent.parent / 'data' / fname


def load_feedings():
    data_type = {'BM': bool}
    df = pd.read_csv(
        fullpath('feed.csv'),
        dtype=data_type,
        index_col=0,
        parse_dates=[0],
        skipinitialspace=True,
        keep_default_na=False)
    df.rename(columns={'Volume (oz)': 'Vol'}, inplace=True)
    return df



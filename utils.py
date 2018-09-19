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
                '%d' % int(height),
                ha='center', va='bottom')

    # give room for the label
    ymin, ymax = ca.get_ylim()
    plt.ylim([ymin, ymax + 6])


def set_y_major(base):
    loc = plticker.MultipleLocator(
        base=base)  # this locator puts ticks at regular intervals
    plt.gca().yaxis.set_major_locator(loc)



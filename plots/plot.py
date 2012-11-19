# -*- coding: utf-8 -*-
from matplotlib import cm
from matplotlib.mlab import griddata
import numpy as np
from matplotlib import pyplot as plt, rcParams, rc
rc('font', **{'family': 'serif', 'serif': ['Times'], 'size': 11})
rcParams['text.usetex'] = True
rcParams['text.latex.unicode'] = True
colors = ['b', 'r', 'g', 'k', 'm', 'c', 'y']
symbols = ['-', '--', '-.']
nc = len(colors)
ns = len(symbols)


def top_10_labels():
    top_10 = [('rock', 1186), ('metal', 880), ('electronic', 622), ('indie', 441), ('pop', 436), ('alternative', 355), ('punk', 330), ('hip-hop', 291), ('progressive', 284), ('hardcore', 281)]
    x, y = map(list, zip(*top_10))

    y = map(float, y)
    ind = range(len(y))
    fig = plt.figure(figsize=(9, 3.5))
    ax = fig.add_subplot(111)
    rects1 = ax.bar(ind, y, align='center', hatch='///', color='w')

    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                     round(height, 2), ha='center', va='bottom')
    autolabel(rects1)
    ax.set_xticks(ind)
    ax.set_xticklabels(x)
    fig.autofmt_xdate(rotation=55)
    ax.set_ylabel(u'Frequência')
    ax.set_ylim(0, 1400)
    ax.set_xlim(ind[0] - 0.5, ind[-1] + 0.5)
    ax.autoscale_view()
    ax.grid(True)
    plt.savefig('top_10_labels.pdf', bbox_inches='tight')


if __name__ == '__main__':
    top_10_labels()

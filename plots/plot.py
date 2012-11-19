# -*- coding: utf-8 -*-
from matplotlib import cm
from matplotlib.mlab import griddata
import numpy as np
from matplotlib import pyplot as plt, rcParams, rc
rc('font', **{'family': 'serif', 'serif': ['Times'], 'size': 15})
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


def k_value():
    K = range(2, 17)
    kIdx = 5
    avgWithinSS = [5326.032135, 3461.266885, 2563.416351, 2043.744647, 1698.784754, 1435.778412, 1247.495494, 1109.112444, 997.1862228, 892.6802995, 822.6883758, 757.8165924, 695.4745584, 656.0969991, 608.9624053]
    fig = plt.figure(figsize=(9, 3.5))
    # fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(K, avgWithinSS, 'k*-')
    ax.plot(K[kIdx], avgWithinSS[kIdx], marker='o', markersize=12,
        markeredgewidth=2, markeredgecolor='r', markerfacecolor='None')
    ax.set_xlim(1, 17)
    plt.grid(True)
    plt.xlabel(u'Número de Agrupamentos ($K$)')
    plt.ylabel(u'Soma média dos quadrados intra-agrupamentos')
    # plt.title(u'"Elbow" para o agrupamento $k$-means')
    plt.savefig('k_values.pdf', bbox_inches='tight')


if __name__ == '__main__':
    top_10_labels()
    k_value()

# -*- coding: utf-8 -*-
from matplotlib import cm
from matplotlib.mlab import griddata
import numpy as np
from matplotlib import pyplot as plt, rcParams, rc, ticker
rc('font', **{'family': 'serif', 'serif': ['Times'], 'size': 14})
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
                     int(height), ha='center', va='bottom')
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


def evolution():
    fig = plt.figure(figsize=(9, 3.5))
    host = fig.add_subplot(111)
    par1 = host.twinx()
    host.set_xlabel(ur'Iteração')
    host.set_ylabel(u'Distância Quadrada Total (x1000)')
    par1.set_ylabel(u'Índice de Jagota')
    X = range(1, 19)
    l1 = [27397, 20307.7107, 18745.54441, 18274.72999, 18025.45127, 17883.57673, 17860.04659, 17848.17587, 17842.58076, 17839.35274, 17833.91395, 17820.90025, 17817.67185, 17814.71098, 17810.2366,  17796.6955,  17792.89033, 17790.58114]
    l2 = [80.17167476, 78.68247563, 75.82723948, 75.38264222, 74.56758905, 73.85740491, 73.76241159, 73.75632523, 73.7292673,  73.73034556, 73.73573901, 73.72206973, 73.70413752, 73.67309554, 73.59772897, 73.55236714, 73.52939901, 73.49800218]
    host.set_xlim(X[0] - 0.5, X[-1] + 0.5)
    host.set_xticks(X)
    host.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, pos: ('%d') % (y * 1e-3)))
    host.set_ylim(min(l1) * 0.97, max(l1) * 1.03)
    par1.set_ylim(min(l2) * 0.99, max(l2) * 1.01)
    p1, = host.plot(X, l1, 'k*-', label=u'Dist. Quad. Total', linewidth=2)
    p2, = par1.plot(X, l2, 'r*-', label=u'Índice de Jagota', linewidth=2)
    host.autoscale_view()
    par1.autoscale_view()
    host.grid(True)

    box = host.get_position()
    host.set_position([box.x0, box.y0 + box.height * 0.2,
                     box.width, box.height * 0.8])
    box = par1.get_position()
    par1.set_position([box.x0, box.y0 + box.height * 0.2,
                     box.width, box.height * 0.8])
    lines = [p1, p2]
    fig.legend(lines, [l.get_label() for l in lines], loc='upper center',
               ncol=3, bbox_to_anchor=(0.5, 0.15), prop={'size': 13})

    plt.savefig('evolution.pdf')
    # plt.savefig('test.png', bbox_inches='tight')


def time():
    X = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
    Y = [2.158, 6.73, 8.876, 13.594, 26.02, 30.624, 21.584, 37.434, 42.508, 52.958]
    E = [1.675655096, 4.133448923, 2.984213464, 5.475575769, 6.87320522, 12.01690601, 5.587300779, 6.186123988, 11.30090129, 17.13246246]
    fig = plt.figure(figsize=(9, 3.5))
    ax = fig.add_subplot(111)
    ax.errorbar(X, Y, yerr=E, fmt='r*', ecolor='r', elinewidth=1.5)
    ax.plot(X, Y, 'k-', linewidth=2)
    ax.set_xticks(X)
    ax.set_xlim(0, 5500)
    plt.grid(True)
    plt.xlabel(u'Tamanho da entrada')
    plt.ylabel(u'Tempo de execução (s)')
    plt.savefig('time.pdf', bbox_inches='tight')


def num_labels():
    X = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
    Y = [806, 1317, 1676, 2022, 2345, 2651, 3007, 3297, 3618, 3869]
    fig = plt.figure(figsize=(9, 3.5))
    ax = fig.add_subplot(111)
    ax.plot(X, Y, 'k*-', linewidth=2)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, pos: ('%d') % (y * 1e-2)))
    ax.set_xticks(X)
    ax.set_xlim(0, 5500)
    plt.grid(True)
    plt.xlabel(u'Tamanho da entrada')
    plt.ylabel(u'Número de rótulos distintos (x100)')
    plt.savefig('num_labels.pdf', bbox_inches='tight')


if __name__ == '__main__':
    top_10_labels()
    k_value()
    evolution()
    time()
    num_labels()

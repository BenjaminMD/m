#!/usr/bin/python3
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import pandas as pd
import numpy as np

from ezplot import scatter_w_outline
from ezpdf import ParseResDir
def get_data(data_dir, par_path, wAl2O3) -> pd.DataFrame:
    if wAl2O3:
        res = ParseResDir(data_dir, par_path)
    else:
        res = ParseResDir(data_dir, par_path, filter="Al2O3")
    return res.df


def label_top(ax, label):
    ax_t = ax.twiny()
    ax_t.set_xticks([])
    ax_t.set_xlabel(label, fontsize=15)


def plot_mv(ax, y: pd.Series, label=None, wAl2O3=True, color='#f6a800'):
    y = y.dropna()
    x = y.index.values
    scatter_w_outline(ax, x * 29 / 3600, y, label=label, color=color)

    y_mean = y.mean()
    y_std = y.std()
    ax.set_ylim(y_mean - 3 * y_std, y_mean + 3 * y_std)
    ax.set_ylim(y_mean - 4 * y_std, y_mean + 4 * y_std)
    ax.set_xlim(0, 6)
    return ax

gs = GridSpec(7, 3,
              height_ratios=[1, 0.5, 1, 1, 1, 1, 1],
              width_ratios=[1, 0.1, 1])

axes = np.array([[plt.subplot(gs[i, j])
         for j in [0, 2]]
         for i in range(2,7)])

for i in [0, 1]:
    axes[0, i].sharex(axes[1, i])
    axes[1, i].sharex(axes[2, i])
    axes[2, i].sharex(axes[3, i])
    axes[3, i].sharex(axes[4, i])

axes[1, 0].sharey(axes[1, 1])
axes[2, 0].sharey(axes[2, 1])
axes[3, 0].sharey(axes[3, 1])
axes[4, 0].sharey(axes[4, 1])



[label_top(a, l) for a, l in zip([axes[0, i] for i in  [0, 1]] , [r'$\gamma$-Al$_2$O$_3$', *['NiO | Ni'] *2])]


df_w = get_data("/home/ben/m/0d/res/*res", par_path="./parameters.wAl2O3.txt", wAl2O3=True)
df_wo = get_data("/home/ben/MT/0_dat/INSITU_SBa200_U_15/res_threshold_NiO_Ni/*results", par_path="./parameters.woAl2O3.txt", wAl2O3=False)
keys = ['_scale', '_a', '_psize', 'Ni0_Biso', '_delta2']
cols = list(df_w.columns)
datw = [[i for i, c in enumerate(cols) if c.endswith(k) and not c.startswith('Al2O3_')] for k in keys] 
print(datw, cols)
axs = [(axes[0, 0], axes[0, 0]), (axes[1, 0], axes[1, 0]), (axes[2, 0], axes[2, 0]), (axes[3, 0], axes[3, 0]), (axes[4, 0], axes[4, 0])] 
for d, a in zip(datw, axs):
    a1, a2 = a
    d1, d2 = d[:2]
    print(a1, d1)
    a1 = plot_mv(a1, df_w[cols[d1]], wAl2O3=False, color='green')
    a2 = plot_mv(a2, df_w[cols[d2]], wAl2O3=False, color='#f6a800')

cols = list(df_wo.columns)
datwo = [[i for i, c in enumerate(cols) if c.endswith(k) and not c.startswith('Al2O3_')] for k in keys] 
print(datwo)
axs = [(axes[0, 1], axes[0, 1]), (axes[1, 1], axes[1, 1]), (axes[2, 1], axes[2, 1]), (axes[3, 1], axes[3, 1]), (axes[4, 1], axes[4, 1])] 
for d, a in zip(datwo, axs):
    a1, a2 = a
    d1, d2 = d[:2]
    print(a1, cols[d1])
    print(a2, cols[d2])
    a1 = plot_mv(a1, df_wo[cols[d1]], wAl2O3=False, color='green')
    a2 = plot_mv(a2, df_wo[cols[d2]], wAl2O3=False, color='#f6a800')
def plot(df, colfs, colno, colors):
    ...
    return
    for j,  value_str in enumerate(['_scale', '_a', '_psize', '_Biso', '_delta2']):
        value = [c for c in cols if c.endswith(value_str) and not c.startswith('Al2O3_')]
        for top, val, color in zip([axes[j, i] for i in  colno], value, colors): 
            print(value_str, j, i)
            plot_mv(top, df[val], wAl2O3=True, color=color, label=value_str.replace('_', ' ')) 
            top.legend()
        

df_w = get_data("/home/ben/m/0d/res/*res", par_path="./parameters.wAl2O3.txt", wAl2O3=True)
df_wo = get_data("/home/ben/MT/0_dat/INSITU_SBa200_U_15/res_threshold_NiO_Ni/*results", par_path="./parameters.woAl2O3.txt", wAl2O3=False)
cols = df_w.columns
plot(df_w, cols, [0, 0, 1], ['green', '#f6a800'])
cols = list(df_wo.columns)
cols = cols[::-1]
cols[1], cols[0] = cols[0], cols[1]
plot(df_wo, cols, [1, 1], ['green', '#f6a800'])
axes[4, 0].set_ylabel(r'$\delta^2\,$/$\,$nm$^2$')
axes[3, 0].set_ylabel(r'Biso$\,$/$\,$nm$^2$')
axes[2, 0].set_ylabel(r'size$\,$/$\,$nm')
axes[1, 0].set_ylabel(r'Lat$\,$/$\,\mathrm{\AA}$')
axes[0, 0].set_ylabel(r'scale$\,$/$\,$-')

axes[4, 0].set_xlabel(r'time$\,$/$\,$h')
axes[4, 1].set_xlabel(r'time$\,$/$\,$h')

#[label.set_visible(False) for label in axes[3, 0].get_xticklabels()]
axes[4, 0].set_xticks([0, 1, 2, 3, 4, 5, 6])

for ax in plt.gcf().axes:
    try:
        ax.label_outer()
    except:
        pass

ax_rw_l = plt.subplot(gs[0, 0])
ax_rw_r = plt.subplot(gs[0, 2])
ax_rw_r.sharey(ax_rw_l)
ax_rw_r.sharex(ax_rw_l)
df = df_w
scatter_w_outline(ax_rw_l, df.index.values * 29 / 3600, df["rw"], label=None)
rw_mean = df["rw"].mean()
rw_std = df["rw"].std()
ax_rw_l.set_ylim(rw_mean -  2 * rw_std, rw_mean + 2 * rw_std)
ax_rw_l.set_ylabel(r'$R_{w}$', fontsize=15)
ax_rw_l.set_title(r'$Tetragonal-\gamma$-Al$_2$O$_3$', fontsize=15)
df = df_wo
scatter_w_outline(ax_rw_r, df.index.values * 29 / 3600, df["rw"], label=None)
ax_rw_r.set_xlim(0, 6)
rw_mean = df["rw"].mean()
rw_std = df["rw"].std()
ax_rw_l.set_ylim(rw_mean -  2 * rw_std, rw_mean + 2 * rw_std)
ax_rw_r.set_title(r'$d$-PDF', fontsize=15)

axes[0, 0].set_ylim(0.1, 0.2)
axes[0, 1].set_ylim(0, 1.5)
axes[1, 0].set_ylim(3.45, 4.18)
axes[2, 0].set_ylim(20, 65)
axes[3, 0].set_ylim(0.0, 3)
axes[4, 0].set_ylim(0, 5)
plt.show()

#!/usr/bin/python3
from ezpdf import ParseResDir
from ezplot import scatter_w_outline

import numpy.typing as npt
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import pandas as pd
import numpy as np

from functools import lru_cache

# nicer labels
prop_labels = {
        'scale': 'Scale / a.u.',
        'psize': '$R$ / nm',
        'a': 'Lat $a$ / nm',
        'b': 'Lat $b$ / nm',
        'c': 'Lat $c$ / nm',
        'delta2' : r'$\Delta^2$',
        'Biso': r'$B_{iso}$ / nm$^2$', 
        }


def get_data(data_dir, par_path) -> pd.DataFrame:
    if wAl2O3:
        res = ParseResDir(data_dir, par_path)
    else:
        res = ParseResDir(data_dir, par_path, filter="Al2O3")
    return res.df

def plot_mv(ax, y: pd.Series, label=None):
    y = y.dropna()
    x = y.index.values
    x = x * 29 / 3600
    scatter_w_outline(ax, x, y, label=label)
    # based on mean and std
    y_mean = y.mean()
    y_std = y.std()
    if wAl2O3:
        ax.set_ylim(y_mean - 1 * y_std, y_mean + 1 * y_std)
    else:
        ax.set_ylim(y_mean - 2 * y_std, y_mean + 2 * y_std)

def dash_board(df: pd.DataFrame):
    cols = df.columns
    cols = cols[2:]
    phases = set(col.split("_")[0] for col in cols)
    props = set(col.split("_")[-1] for col in cols)
    
    phases = sorted(phases)
    props = sorted(props)[::-1]
    if wAl2O3:
        props[2], props[4] = props[4], props[2]
    else:
        props[2], props[3] = props[3], props[2]
        phases = phases[::-1]
    gs = GridSpec(len(props) + 2, len(phases), height_ratios=[1] + [0.2] + [1] * len(props))
    
    axes = np.empty((len(props), len(phases)), dtype=object)
    for i in range(len(phases)):
        for j in range(len(props)):
            axes[j][i] = plt.subplot(gs[j+2, i])
#            if j > 0:
#                axes[j][i].sharex(axes[0][i])

    for i, phase in enumerate(phases):
        for j, prop in enumerate(props):
            ax = axes[j, i]
            if i == 0:
                ax.set_ylabel(prop_labels[prop], fontsize=20)
            if i == len(phases) - 1:
                ax.yaxis.set_label_position("right")
                ax.yaxis.tick_right()
            if j == len(props) - 1:
                ax.set_xlabel('time / h', fontsize=20)
                ax.xaxis.set_tick_params(labelsize=15)
            if j == 0:
                ax_t = ax.twiny()
                ax_t.set_xticks([])
                ax_t.set_xlabel(phase_labels[phase], fontsize=20)
            if j != len(props) - 1:
#                ax.plot([], [], "k-", label="mean")
                ax.set_xticks([])
            col = [c for c in cols
                   if c.startswith(f'{phase}_') 
                   and c.endswith(f'_{prop}')
                   ] 
            if col:
                plot_mv(ax, df[col[0]])
    ax = plt.subplot(gs[0, :])
    scatter_w_outline(ax, df.index.values * 29 / 3600, df["rw"], label=None)
    rw_mean = df["rw"].mean()
    rw_std = df["rw"].std()
    ax.set_ylim(rw_mean - rw_std, rw_mean + rw_std)
    ax.set_ylabel(r'$R_{w}$', fontsize=20)
    for ax in plt.gcf().axes:
        try:
            ax.label_outer
            ax.yaxis.set_tick_params(labelsize=15)
        except:
            pass
    plt.tight_layout()
        
wAl2O3 = False
if wAl2O3:
    phase_labels = {
        'Ni': 'Ni',
        'NiO': 'NiO',
        'Al2O3': r'$\gamma$-Al$_2$O$_3$',
        }
else:
    phase_labels = {
        'Al2O3': r'$\gamma$-Al$_2$O$_3$',
        'NiΓ': 'Ni',
        'NiOΓ': 'NiO'
        }
def main():
    if wAl2O3:
        df = get_data("/home/ben/m/0d/res/*res", par_path="./parameters.wAl2O3.txt")
    else:
        df = get_data("/home/ben/MT/0_dat/INSITU_SBa200_U_15/res_threshold_NiO_Ni/*results",
                      par_path="./parameters.woAl2O3.txt")
    dash_board(df)

#    plt.subplot(2, 2, 1)
#    plot_mv(df["Ni_scale"])
#    plot_mv(df["NiO_scale"])
#    plot_mv(df["Al2O3_scale"])
#    plt.subplot(2, 2, 2)
#    plot_mv(df["Ni_psize"])
#    plot_mv(df["NiO_psize"])
#    plot_mv(df["Al2O3_psize"])
    plt.show()
if __name__ == "__main__":
    df = main()

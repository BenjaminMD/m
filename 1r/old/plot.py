#!/usr/bin/python3
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import pandas as pd
import numpy as np

from ezplot import scatter_w_outline
from ezpdf import ParseResDir

def plot_mv(ax, y: pd.Series, label=None, wAl2O3=True, color='#f6a800'):
    y = y.dropna()
    x = y.index.values
    x = x * 29 / 3600
    scatter_w_outline(ax, x, y, label=label, color=color)

# rolling average
    y = y.rolling(20, center=True).mean()
    ax.plot(x, y, 'k', alpha=0.5)
    # based on mean and std
    y_mean = y.mean()
    y_std = y.std()
    if wAl2O3:
        ax.set_ylim(y_mean - 3 * y_std, y_mean + 3 * y_std)
    else:
        ax.set_ylim(y_mean - 4 * y_std, y_mean + 4 * y_std)
    ax.set_xlim(0, 6)
    return ax

def get_data(data_dir, par_path, wAl2O3) -> pd.DataFrame:
    if wAl2O3:
        res = ParseResDir(data_dir, par_path)
    else:
        res = ParseResDir(data_dir, par_path, filter="Al2O3")
    return res.df

prop_labels = {
        'scale': 'Scale / a.u.',
        'psize': '$R$ / nm',
        'a': 'Lat $a$ / nm',
        'b': 'Lat $b$ / nm',
        'c': 'Lat $c$ / nm',
        'delta2': r'$\Delta^2$',
        'Biso': r'$B_{iso}$ / nm$^2$' 
        }

phase_labels = {
        'NiΓ': 'Ni',
        'NiOΓ': 'NiO',
        'Ni': 'Ni',
        'NiO': 'NiO',
        'Al2O3': r'$\gamma$-Al$_2$O$_3$',
    }

df_w = get_data("/home/ben/m/0d/res/*res",
              par_path="./parameters.wAl2O3.txt",
              wAl2O3=True)
df_wo = get_data("/home/ben/MT/0_dat/INSITU_SBa200_U_15/res_threshold_NiO_Ni/*results",
              par_path="./parameters.woAl2O3.txt",
              wAl2O3=False)
cols = np.concatenate([df_w.columns[2:], df_wo.columns[2:]])
cols = cols
#cols = [c.replace('Γ', '') for c in cols]
phases = set(col.split("_")[0] for col in cols)
props = set(col.split("_")[-1] for col in cols)
num_phases = len(phases)
num_props = len(props)

print(len(phases))
print(len(props))

gs = GridSpec(num_props + 2,
              num_phases + 1,
              width_ratios= [1, 1, 1, 0.1, 1, 1],
              height_ratios=[1, 0.5] + [1] * num_props,
              )

axes = np.array([[plt.subplot(gs[i, j]) 
         for j in [0, 1, 2, 4, 5]]
         for i in range(2, num_props + 2)])

# Plot with tetra -------------------------------------------------------------
df = df_w
cols = df.columns
cols = cols[2:]
phases = set(col.split("_")[0] for col in cols)
props = set(col.split("_")[-1] for col in cols)

phases = sorted(phases)
phases[1], phases[2] = phases[2], phases[1]
props = sorted(props)[::-1]
props[2], props[4] = props[4], props[2]

for i, phase in enumerate(phases):
    i = i - 1 if (phase.startswith('Ni') )and (not
        phase.startswith('NiO')) else i
    for j, prop in enumerate(props):
        print(phase)
        print(j, i)
        ax = axes[j, i]
        if i == 0:
            ax.set_ylabel(prop_labels[prop], fontsize=15)
        if j == len(props) - 1:
            ax.set_xlabel('time / h', fontsize=15)
            ax.xaxis.set_tick_params(labelsize=15)
        if j == 0:
            ax_t = ax.twiny()
            ax_t.set_xticks([])
            ax_t.set_xlabel(phase_labels[phase], fontsize=15)
        if j != len(props) - 1:
            ax.set_xticks([])
        col = [c for c in cols
               if c.startswith(f'{phase}_') 
               and c.endswith(f'_{prop}')
               ] 
        if col:
            color = 'green' if phase.startswith('NiO') else '#f6a800'
            ax = plot_mv(ax, df[col[0]], color=color)
ax = plt.subplot(gs[0, :])
for ax in plt.gcf().axes:
    try:
        ax.label_outer
        ax.yaxis.set_tick_params(labelsize=15)
    except:
        pass

axes[3, 1].axis('off')
axes[3, 2].axis('off')

for i in range(5):
    axes[0, i].sharex(axes[1, i])
    axes[1, i].sharex(axes[2, i])
    axes[2, i].sharex(axes[3, i])
    axes[3, i].sharex(axes[4, i])
    axes[4, i].sharex(axes[5, i])
# Plot without tetra ----------------------------------------------------------
df = df_wo
cols = df.columns
cols = cols[2:]
phases = set(col.split("_")[0] for col in cols)
props = set(col.split("_")[-1] for col in cols)

phases = sorted(phases)
props = sorted(props)[::-1]
props[2], props[3] = props[3], props[2]
for i, phase in enumerate(phases):
    for j, prop in enumerate(props):
        color = 'green' if phase.startswith('NiO_') else '#f6a800'
        i = i - 1 if phase.startswith("Ni_") else i
        j = j + 1 if j > 2 else j
        ax = axes[j, i+3]
        if j == len(props):
            ax.set_xlabel('time / h', fontsize=15)
            ax.xaxis.set_tick_params(labelsize=15)
        if j == 0:
            ax_t = ax.twiny()
            ax_t.set_xticks([])
        if j != len(props):
            ax.set_xticks([])
        col = [c for c in cols
               if c.startswith(f'{phase}_') 
               and c.endswith(f'_{prop}')
               ] 
        if col:
            plot_mv(ax, df[col[0]], wAl2O3=False, color=color)
ax = plt.subplot(gs[0, :])
for ax in plt.gcf().axes:
    try:
        ax.label_outer
        ax.yaxis.set_tick_params(labelsize=15)
    except:
        pass

axes[3, 4].axis('off')
axes[3, 3].axis('off')
# Plot rw ---------------------------------------------------------------------
ax_rw_l = plt.subplot(gs[0, 0:3])
ax_rw_l.set_title(r"With tetra $\gamma$-Al$_2$O$_3$")
ax_rw_r = plt.subplot(gs[0, 4:6])
ax_rw_r.sharey(ax_rw_l)
ax_rw_r.sharex(ax_rw_l)
ax_rw_r.set_title(r"Only Ni and NiO")
df = df_w
scatter_w_outline(ax_rw_l, df.index.values * 29 / 3600, df["rw"], label=None)
rw_mean = df["rw"].mean()
rw_std = df["rw"].std()
ax_rw_l.set_ylim(rw_mean - rw_std, rw_mean + rw_std)
ax_rw_l.set_ylabel(r'$R_{w}$', fontsize=15)
df = df_wo
scatter_w_outline(ax_rw_r, df.index.values * 29 / 3600, df["rw"], label=None)
ax_rw_r.set_xlim(0, 6)
rw_mean = df["rw"].mean()
rw_std = df["rw"].std()
ax_rw_l.set_ylim(rw_mean - rw_std, rw_mean + rw_std)
# for later axes[1, 1].axis('off')
plt.show()

from ezplot.ezplot import gather_legend
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from ezplot import plot_defaults, scatter_w_outline

# CONSTANTS
BROWN = '#8b4513'
GREEN = '#008000'
RED = '#ff0000'
ORANGE = '#f6a800'

MATH_LABELS = {
    "t": (r"t", r"h"),
    "rw": (r"R_\mathrm{w}", r"a.u."),
    "T": (r"T", r"°C"),
    "lat": (r"Lat", r"\AA"),
    "p": (r"p", r"bar"),
    "r": (r"r", r"\AA"),
}

make_label = lambda key: r"${}\,/\,\mathrm{{{}}}$".format(*MATH_LABELS[key])


def plot_tetrAl2O3(): 
    fig, gs = plot_defaults(2, 1)
    ax_top_left = fig.add_subplot(gs[0, 0])
    ax_low_left = fig.add_subplot(gs[1, 0], sharex=ax_top_left)
    ax_top_right = ax_top_left.twinx()
    ax_low_right = ax_low_left.twinx()
    plt.setp(ax_top_left.get_xticklabels(), visible=False)
    ax_top_left.grid(True, which='both', axis='both', alpha=0.3)
    ax_low_left.grid(True, which='both', axis='both', alpha=0.3)
    return fig, [[ax_top_left, ax_top_right], [ax_low_left, ax_low_right]]

ax_top_left.set_ylabel(r'$R_\mathrm{w}\,/\,$a.u.', color="#f6a800", fontweight='bold')
ax_top_right.set_ylabel(r'$T\,/\,^\circ$C', color='red', fontweight='bold')
ax_low_left.set_ylabel('Lat a$\,/\,\mathrm{\AA}$')
ax_low_right.set_ylabel(r'$p^\prime\,/\,10^{-8}\cdot$torr')

ax_low_left.set_xlabel(r'$t\,/\,$h')
ax_top_left.set_xlim(0.0, 7.2)
ax_top_left.set_ylim(0.30, 0.38)
ax_top_right.set_ylim(10, 460)
ax_low_left.set_ylim(3.55, 3.556)
ax_low_right.set_ylim(0, 100)

ax_top_left.set_yticks(np.arange(0.30, 0.39, 0.02))
ax_top_right.set_yticks(np.arange(50, 451, 100))
ax_low_left.set_yticks(np.arange(3.55, 3.556, 0.002))
ax_low_right.set_yticks(np.arange(0, 101, 20))

ax_top_left.tick_params(axis='y', colors="#f6a800")
ax_top_right.tick_params(axis='y', colors='red')
ax_low_left.tick_params(axis='y', colors='green')
ax_low_right.tick_params(axis='y', colors=brown)

ax_low_right.spines['right'].set_color(brown)
ax_low_right.spines['left'].set_color('green')
ax_low_right.yaxis.label.set_color(brown)
ax_low_right.tick_params(axis='y', colors=brown)

ax_top_left.spines['left'].set_color("#f6a800")
ax_top_left.spines['right'].set_color('red')
ax_top_left.yaxis.label.set_color("#f6a800")
ax_top_left.tick_params(axis='y', colors="#f6a800")


df = pd.read_csv('FelixStinkt.csv')
df = df[[f.startswith('azint_UC1_Al2O3_2') for f in df.file_name]]
df.reset_index(inplace=True)

switch = df["file_name"].values 

switch = [f.split('Al2O3_2_')[-1] for f in switch]
switch = [f.split('_scan')[0] for f in switch]
switch = [int(f) for f in switch]

# get id when scan number changes
switch = np.where(np.diff(switch) != 0)[0] + 1

def fill_list_with_blocks(indices, length):
    result = []
    current_value = 1  # Start with 1
    for i in range(length):
        if i in indices:
            result.append(current_value)
        else:
            result.append(1 - current_value)  # Alternate between 0 and 1
        if i + 1 in indices:
            current_value = 1 - current_value  # Flip the value for the next block
    return result


df.dt = pd.to_datetime(df.dt)
t = df.dt - df.dt[0]
t = t.dt.total_seconds() / 3600
t = t.values
df.loc[df.rw > 1, 'rw'] = np.nan

switch = fill_list_with_blocks(switch[1:], len(df))

df['scan'] = switch


plt.plot(switch)


fig, axs = plot_tetrAl2O3()

scatter_w_outline(axs[0][1], t, df['T_avg / °C'], label='T', color='red')
axs[0][1].set_ylabel(r'$T\,/\,^\circ$C', color='red', fontweight='bold')
axs[0][1].set_yticks(np.arange(50, 451, 100))
axs[0][1].set_ylim(10, 460)

scatter_w_outline(axs[0][0], t, df['rw'], label='Rw')
axs[0][0].set_ylabel(r'$R_\mathrm{w}\,/\,$a.u.', color="#f6a800", fontweight='bold')
axs[0][0].set_ylim(0.30, 0.38)


axs[0][1].fill_between(t, 0, 500, where=df['scan'] == 1, facecolor='grey', alpha=0.3)
axs[1][0].fill_between(t, 0, 1, where=df['scan'] == 1, facecolor='grey', alpha=0.8, label='Methanation')
axs[1][0].fill_between(t, 0, 100, where=df['scan'] == 1, facecolor='grey', alpha=0.3)

brown = '#8b4513'
scatter_w_outline(axs[1][0], t, df['Ni_a'], label=r'Ni lat a', color='green')
axs[1][0].set_ylabel('Lat a$\,/\,\mathrm{\AA}$')
axs[1][0].set_ylim(3.55, 3.556)
axs[1][0].set_xlabel(r'$t\,/\,$h')


scatter_w_outline(axs[1][1], t, df['H']*1e5, label=r'$\frac{1}{3}$H$_2$ pressure', color='purple')
scatter_w_outline(axs[1][1], t, df['CO2']*5e5, label=r'CO$_2$ pressure', color="black")
axs[1][1].plot(t, df['H']*1e5, color='blue', alpha=0.3)
axs[1][1].plot(t, df['CO2']*5e5, color="black", alpha=0.3)

axs[1][1].set_ylabel(r'$p^\prime\,/\,10^{-8}\cdot$torr')

h, l = gather_legend([axs[1][0], axs[1][1]])



axs[0][0].set_xlim(0.0, 7.2)
fig.legend(h, l,
           ncol=4,
           loc='upper center',
           bbox_to_anchor=(0.5, 1.00),
           frameon=False,
           fontsize=10)

axs[0][0].set_zorder(1)
axs[0][0].patch.set_visible(False)
plt.savefig('./insitutetrAl2O3_UC1.pdf', bbox_inches='tight')

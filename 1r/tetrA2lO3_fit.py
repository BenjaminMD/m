from ezplot.ezplot import gather_legend
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from ezplot import plot_defaults, scatter_w_outline

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


df = pd.read_csv('FelixStinkt.csv')
# drop rows containing azint_UC1_Al2O3_0001 
print(df.shape)
df = df[[f.startswith('azint_UC1_Al2O3_2') for f in df.file_name]]
print(df.shape)
df.reset_index(inplace=True)

switch = df["file_name"].values # azint_UC1_Al2O3_0001_scan0007_pilatus_rm_Ni

# get rid of the scan number
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

# create a list of 0 and 1, where 1 indicates a new scan
# this is used to color the background of the plot


df.dt = pd.to_datetime(df.dt)
t = df.dt - df.dt[0]
t = t.dt.total_seconds() / 3600
t = t.values
df.loc[df.rw > 1, 'rw'] = np.nan

switch = fill_list_with_blocks(switch[1:], len(df))

df['scan'] = switch


plt.plot(switch)
plt.show()


fig, axs = plot_tetrAl2O3()

scatter_w_outline(axs[0][1], t, df['T_avg / °C'], label='T', color='red')
axs[0][1].set_ylabel(r'$T\,/\,^\circ$C', color='red', fontweight='bold')
# make tiks more frequent
axs[0][1].set_yticks(np.arange(50, 451, 100))
axs[0][1].set_ylim(10, 460)

scatter_w_outline(axs[0][0], t, df['rw'], label='Rw')
axs[0][0].set_ylabel(r'$R_\mathrm{w}\,/\,$a.u.', color="#f6a800", fontweight='bold')
axs[0][0].set_ylim(0.25, 0.35)


axs[0][1].fill_between(t, 0, 500, where=df['scan'] == 1, facecolor='grey', alpha=0.3)

axs[1][0].fill_between(t, 0, 1, where=df['scan'] == 1, facecolor='grey', alpha=0.8, label='Methanation')
axs[1][0].fill_between(t, 0, 100, where=df['scan'] == 1, facecolor='grey', alpha=0.3)

brown = '#8b4513'
scatter_w_outline(axs[1][0], t, df['Ni_psize'], label='Ni size', color='green')
scatter_w_outline(axs[1][0], t, df['NiO_psize'], label='NiO size', color=brown)
scatter_w_outline(axs[1][0], t, df['delta4_Al2O3_psize'], label=r'$\gamma$-Al$_2$O$_3$ size', color='blue')
axs[1][0].set_ylabel('Particle size$\,/\,$nm')
axs[1][0].set_ylim(20, 65)
axs[1][0].set_xlabel(r'$t\,/\,$h')




scatter_w_outline(axs[1][1], t, df['H']*1e5, label='H$_2$ pressure', color='purple')
scatter_w_outline(axs[1][1], t, df['CO2']*5e5, label=r'$\frac{1}{3}$CO$_2$ pressure', color="black")
axs[1][1].plot(t, df['H']*1e5, color='blue', alpha=0.3)
axs[1][1].plot(t, df['CO2']*5e5, color="black", alpha=0.3)

axs[1][1].set_ylabel(r'$p^\prime\,/\,10^{-8}\cdot$torr')

h, l = gather_legend([axs[1][0], axs[1][1]])



axs[0][0].set_xlim(0.0, 7.2)
fig.legend(h, l,
           ncol=3,
           loc='upper center',
           bbox_to_anchor=(0.5, 1.00),
           frameon=False,
           fontsize=10)

axs[0][0].set_zorder(1)
axs[0][0].patch.set_visible(False)
plt.savefig('./insitutetrAl2O3_UC1.pdf', bbox_inches='tight')

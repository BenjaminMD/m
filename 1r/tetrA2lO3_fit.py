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
    return [[ax_top_left, ax_top_right], [ax_low_left, ax_low_right]]


df = pd.read_csv('tetrAl2O3_UC1.csv')

df.dt = pd.to_datetime(df.dt)
print(df.columns)
df.loc[df.rw > 1, 'rw'] = np.nan


axs = plot_tetrAl2O3()


scatter_w_outline(axs[0][0], df.dt, df['rw'], label='Rw')
axs[0][0].set_ylabel('Rw')

scatter_w_outline(axs[0][1], df.dt, df['T_avg / °C'], label='T_avg', color='red')
axs[0][1].set_ylabel('Temperature (K)')


scatter_w_outline(axs[1][0], df.dt, df['Ni_psize'], label='Ni_psize', color='green')
scatter_w_outline(axs[1][0], df.dt, df['NiO_psize'], label='NiO_psize', color='black')
scatter_w_outline(axs[1][0], df.dt, df['Al2O3_psize'], label='Al2O3_psize', color='blue')
axs[1][0].set_ylabel('Particle size (nm)')
axs[1][0].set_ylim(20, 65)
axs[1][0].set_xlabel('Time')


scatter_w_outline(axs[1][1], df.dt, df['CH4'], label='CH4')
scatter_w_outline(axs[1][1], df.dt, df['H'], label='H2', color='purple')
axs[1][1].plot(df.dt, df['H'], label='H2', color='blue', alpha=0.3)
axs[1][1].set_ylabel(r'$p^\prime$Mass spectrometer$\,/\,$mtorr')





plt.show()

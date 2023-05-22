from matplotlib import pyplot as plt
from ezplot import create_basic_plot
from glob import glob
import numpy as np

files = glob('*.diff')
max = 0
min = 0
fig, ax = create_basic_plot(xlabel=r'$r\,/\,\mathrm{\AA}$', ylabel='Difference')
num = [242, 264, 274, 313, 298, 321, 668, 692, 710, 726, 747, 758]
# add 30 to each num
num = [i + 30 for i in num]
c = ['r', 'r', 'r', 'b', 'b', 'b', 'g', 'g', 'g', 'k', 'k', 'k']
for i, (f, c) in enumerate(zip(np.array(files)[num], c)):
    r, d = np.loadtxt(f).T
    ax.plot(r, d + i * 0.5, c=c)
ax.plot([-1, -2], [0, 0], c='r', label='First Methanation')
ax.plot([-1, -2], [0, 0], c='b', label='First Dropout')
ax.plot([-1, -2], [0, 0], c='g', label='last Methanation')
ax.plot([-1, -2], [0, 0], c='k', label='last Dropout')
ax.legend()
ax.set_xlim(1.5, 30)
ax.set_ylim(-0.5, 6.4)
# add titel\
ax.set_title('$\Delta(r) = G(r)-G(r)_\mathrm{calc}$ always 1/3, 2/3 and 3/3 of Dropout/Methanation')
plt.savefig('/home/ben/mt/img/diff.pdf')

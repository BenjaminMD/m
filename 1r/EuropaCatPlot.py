#!/usr/bin/env python3
from numpy import zeros
from EuropaCatLayout import axs, initialize_plot, COLORS
from ezplot import scatter_w_outline
from EuropaCatData import df, t
import matplotlib.pyplot as plt


def main():
    initialize_plot()
    scatter_w_outline(axs.tl, t, df.rw, color=axs.ynames[0][2])
    axs.tl.plot(t, df.rw, axs.ynames[0][2], zorder=0) # its a class lets define a get 
    scatter_w_outline(axs.tr, t, df["T"], color=axs.ynames[1][2])
    axs.tr.plot(t, df["T"], axs.ynames[1][2], zorder=0)

    scatter_w_outline(axs.ll, t, df.Ni_a, color=axs.ynames[2][2])
    axs.ll.plot(t, df.Ni_a, axs.ynames[2][2], zorder=0)

    scatter_w_outline(axs.lr, t, df.H*1e5, color=axs.ynames[3][2])
    axs.lr.plot(t, df.H*1e5, axs.ynames[3][2], zorder=0)
    
    c = next(COLORS)
    c = next(COLORS)
    scatter_w_outline(axs.lr, t, df.CO2*5e5, color=c)
    axs.lr.plot(t, df.CO2*5e5, c, zorder=0)

#    scatter_w_outline(axs.br, t, df.Ni_Ni0_Biso, color=axs.ynames[5][2])
#    axs.br.plot(t, df.Ni_Ni0_Biso, axs.ynames[5][2], zorder=0)

    scatter_w_outline(axs.br, t, df.Ni_scale, color=axs.ynames[5][2])
    axs.br.plot(t, df.Ni_scale, axs.ynames[5][2], zorder=0)

    c = next(COLORS)
    c = next(COLORS)
    c = next(COLORS)
    scatter_w_outline(axs.br, t, df.NiO_scale, color=c)
    axs.br.plot(t, df.NiO_scale , c, zorder=0)


    scatter_w_outline(axs.bl, t, df.Ni_psize/10, color=axs.ynames[4][2])
    axs.bl.plot(t, df.Ni_psize/10, axs.ynames[4][2], zorder=0)


    c = next(COLORS)
    c = next(COLORS)
    c = next(COLORS)
    axs.tl.fill_between(t[:260], 0, 100, where=df["scan"][:260] == 0, color=c, alpha=0.1)
    axs.ll.fill_between(t[:260], 0, 100, where=df["scan"][:260] == 0, color=c, alpha=0.1)
    axs.bl.fill_between(t[:260], 0, 100, where=df["scan"][:260] == 0, color=c, alpha=0.1)
    axs.tl.fill_between(t, 0, 100, where=df["scan"] == 1, color="k", alpha=0.1)
    axs.ll.fill_between(t, 0, 100, where=df["scan"] == 1, color="k", alpha=0.1)
    axs.bl.fill_between(t, 0, 100, where=df["scan"] == 1, color="k", alpha=0.1)



    plt.savefig("Test.pdf")
    plt.show()

main()

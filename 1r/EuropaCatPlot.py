#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ezplot import scatter_w_outline, plot_defaults
from dataclasses import dataclass
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import numpy as np

#matplotlib.rc('text', usetex=True)
#matplotlib.rcParams['text.latex.preamble'] = r"\usepackage{amsmath}"

# CONSTANTS
# =========
COLORS = [
    "#8EBAE6",
    "#F58E78",
    "#9764F5",
    "#81F5CB",
    "#F5ED53",
]

MATH_LABELS = {
    "t": (r"t", r"h"),
    "rw": (r"R_\mathrm{w}", r"a.u."),
    "T": (r"T", r"°C"),
    "lat": (r"Lat", r"\AA"),
    "p": (r"p", r"bar"),
    "r": (r"r", r"\AA"),
}
# =========

@dataclass
class axs:
    fig, gs = plot_defaults(2, 1)

    tl = fig.add_subplot(gs[0, 0])
    ll = fig.add_subplot(gs[1, 0], sharex=tl)

    tr = tl.twinx()
    lr = ll.twinx()

    ynames = [("rw", tl), ("T", tr), ("lat", ll), ("p", lr)]
    xnames = [("t", ll)]


def color_labels(names, x_or_y):
    for (name, ax), c in zip(names, COLORS):
        label = r"${}\,/\,\mathrm{{{}}}$".format(*MATH_LABELS[name])
        getattr(ax, f"set_{x_or_y}label")(label, color=c, fontweight="bold")

color_labels(axs.ynames, "y")
color_labels(axs.xnames, "x")
    

plt.setp(axs.tl.get_xticklabels(), visible=False)

axs.tl.grid(True, which="both", axis="both", alpha=0.3)
axs.ll.grid(True, which="both", axis="both", alpha=0.3)




plt.show()

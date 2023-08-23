from itertools import cycle

from dataclasses import dataclass
from ezplot import plot_defaults
import matplotlib.pyplot as plt


# CONSTANTS
# =========

COLORS = cycle(["#7160A7", "#A0D3C2", "#F18C78", "#8BB2DB"])

col = {
    "purple": "#7160A7",
    "green": "#A0D3C2",
    "orange": "#F18C78",
    "blue": "#8BB2DB",
}

MATH_LABELS = {
    "t": (r"time", r"h"),
    "rw": (r"R_\mathrm{w}", r"a.u."),
    "T": (r"\mathrm{Temperature}", r"°C"),
    "lat": (r"\mathrm{Lattice parameter}", r"\AA"),
    "p": (r"\mathrm{Pressure}", r"\mu bar"),
    "R": (r"\mathrm{Particle size}", r"nm"),
    "adp": (r"\mathrm{Biso}", r"\AA^2"),
    "scale": (r"\mathrm{Scale}", r"a.u."),
}

YLIMITS = {
    "rw": (0.3, 0.36),
    "T": (300, 480),
    "lat": (3.55, 3.556),
    "p": (0, 1),
    "R": (3.0, 5.5),
    "adp": (1.18, 1.28),
    "scale": (0.1, 0.19),
}
XLIMITS = {"t": (0.5, 6)}

YTICKS = {
    "rw": (0.31, 0.33, 0.35), 
    "T": (330, 390, 450),
    "lat": (3.551, 3.553, 3.555),
    "p": (0.2, 0.5, 0.8),
    "R": (3.2, 4.2, 5.2),
    "adp": (1.2, 1.23, 1.26),
    "scale": (0.12, 0.14, 0.16),
}
# =========


def color_labels(names, x_or_y):
    for name, ax, c in names:
        label = r"${}\,/\,\mathrm{{{}}}$".format(*MATH_LABELS[name])
        getattr(ax, f"set_{x_or_y}label")(label, color=c, fontweight="bold")


@dataclass
class axs:
    fig, gs = plot_defaults(3, 1, ratio=4/3)

    # layout 
    tl = fig.add_subplot(gs[0, 0])
    ll = fig.add_subplot(gs[1, 0], sharex=tl)

    tr = tl.twinx()
    lr = ll.twinx()

    bl = fig.add_subplot(gs[2, 0], sharex=tl)
    br = bl.twinx()
    
    axs = [tl, tr, ll, lr]

    # labels
    ynames = [("rw", tl), ("T", tr), ("lat", ll), ("p", lr), ("R", bl),
              ("scale", br)]
    ynames = [
        ("rw", tl, col["orange"]),
        ("T", tr, col["purple"]),
        ("lat", ll, col["orange"]),
        ("p", lr, col["purple"]),
        ("R", bl, col["orange"]),
        ("scale", br, col["purple"]),
    ]

    xnames = [("t", bl, col["blue"])]


    # limits # TODO: make this more general
    [ax.set_ylim(*YLIMITS[name]) for name, ax, _ in ynames]
    [ax.set_xlim(*XLIMITS[name]) for name, ax, _ in xnames]

    # ticks
    [ax.set_yticks(YTICKS[name]) for name, ax, _ in ynames]


def initialize_plot():
    color_labels(axs.ynames, "y")
    color_labels(axs.xnames, "x")


    [ax.tick_params(axis="y", colors=c, which="both") for _, ax, c in axs.ynames]

    plt.setp(axs.tl.get_xticklabels(), visible=False)
    plt.setp(axs.ll.get_xticklabels(), visible=False)
    #[ax.grid(True, alpha=0.3) for ax in (axs.tl, axs.ll)]


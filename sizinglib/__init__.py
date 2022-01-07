from . import utilities
import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter
from collections import deque
import numpy as np

COLORS = plt.rcParams["axes.prop_cycle"].by_key()["color"]
plt.rcParams.update(
    {
        "text.usetex": False,
        "axes.labelsize": 16,
        "axes.titlesize": 16,
    }
)


def build_nmos(target_vstar, target_gm, target_vds, target_length=1e-6):
    RESULTS_SIZING = utilities.get_width(
        starting_width=1000e-6,
        length=target_length,
        target_vstar=target_vstar,
        target_gm=target_gm,
    )
    RESULTS_BIASING = utilities.get_vg(
        idd=RESULTS_SIZING["RESULT_SWEEP_XY"]["TARGET_ID"],
        width=RESULTS_SIZING["RESULT_SIZE"]["WIDTH"],
        length=RESULTS_SIZING["RESULT_SIZE"]["LENGTH"],
        target_vd=target_vds,
    )
    RESULTS_CHAR = utilities.get_char(
        width=RESULTS_SIZING["RESULT_SIZE"]["WIDTH"],
        length=RESULTS_SIZING["RESULT_SIZE"]["LENGTH"],
        vg=RESULTS_BIASING["RESULT_SWEEP_XY"]["TARGET_VG"],
        target_vd=target_vds,
        target_gm=target_gm,
    )

    return {
        "RESULTS_SIZING": RESULTS_SIZING,
        "RESULTS_BIASING": RESULTS_BIASING,
        "RESULTS_CHAR": RESULTS_CHAR,
    }


def build_figure():
    fig = plt.figure(figsize=(12, 16))

    # SIZING
    ax = fig.add_subplot(4, 2, 1)
    ax.set_xlabel(r"$\frac{I_D}{W/L}$ [A]")
    ax.set_ylabel(r"$\frac{g_m}{I_D}$ [1 / V]")
    ax.set_xscale("log")
    ax.xaxis.set_major_formatter(EngFormatter())

    ax = fig.add_subplot(4, 2, 2)
    ax.set_xlabel(r"$V^*$ [V]")
    ax.set_ylabel(r"$I_D$ [A]")
    ax.yaxis.set_major_formatter(EngFormatter())

    # BIASING
    ax = fig.add_subplot(4, 2, 3)
    ax.set_xlabel(r"$V_{DS}$ [V]")
    ax.set_ylabel(r"$V_{GS}$ [V]")

    # CHAR
    ax = fig.add_subplot(4, 2, 4)
    ax.set_xlabel(r"$V_{DS}$ [V]")
    ax.set_ylabel(r"$V_{TH}$ [V]")
    ax.yaxis.set_major_formatter(EngFormatter(places=1))

    ax = fig.add_subplot(4, 2, 5)
    ax.set_xlabel(r"$V_{DS}$ [V]")
    ax.set_ylabel(r"$I_D$ [A]")
    ax.yaxis.set_major_formatter(EngFormatter())

    ax = fig.add_subplot(4, 2, 6)
    ax.set_xlabel(r"$V_{DS}$ [V]")
    ax.set_ylabel(r"$C_{GG}$ [F]")
    ax.yaxis.set_major_formatter(EngFormatter())

    ax = fig.add_subplot(4, 2, 7)
    ax.set_xlabel(r"$V_{DS}$ [V]")
    ax.set_ylabel(r"$g_m$ [S]")
    ax.yaxis.set_major_formatter(EngFormatter())

    ax = fig.add_subplot(4, 2, 8)
    ax.set_xlabel(r"$V_{DS}$ [V]")
    ax.set_ylabel(r"$r_o$ [S]")
    ax.yaxis.set_major_formatter(EngFormatter())

    axes = fig.get_axes()
    deque(map(lambda x: x.grid(), axes))

    fig.subplots_adjust(
        top=0.9,
        bottom=0.1,
        left=0.1,
        right=0.9,
        wspace=0.25,
        hspace=0.4,
    )

    return axes


def plotter(num, dataset, axes):
    # sizing
    df = dataset["RESULTS_SIZING"]["RESULT_SWEEP"]
    xy = dataset["RESULTS_SIZING"]["RESULT_SWEEP_XY"]

    ax = axes[0]
    ax.plot(
        df["id_unit"],
        df["gmoverid"],
        color=COLORS[num],
    )
    ax.plot(
        xy["TARGET_ID_UNIT"],
        xy["TARGET_GMOVERID"],
        marker="o",
        markerfacecolor=COLORS[num],
    )

    ax = axes[1]
    ax.plot(
        df["vstar"],
        df["id"],
        color=COLORS[num],
    )
    ax.plot(
        xy["TARGET_VSTAR"],
        xy["TARGET_ID"],
        marker="o",
        markerfacecolor=COLORS[num],
    )
    ax.set_xlim(df["vstar"].min(), 1.2 * xy["TARGET_VSTAR"])
    ax.set_ylim(0.0, 2.0 * xy["TARGET_ID"])

    # BIASING
    df = dataset["RESULTS_BIASING"]["RESULT_SWEEP"]
    xy = dataset["RESULTS_BIASING"]["RESULT_SWEEP_XY"]

    ax = axes[2]
    ax.plot(
        df["vd"],
        df["vg"],
        color=COLORS[num],
    )
    ax.plot(
        xy["TARGET_VD"],
        xy["TARGET_VG"],
        marker="o",
        markerfacecolor=COLORS[num],
    )
    ax.set_ylim(0.95 * xy["TARGET_VG"], 1.05 * xy["TARGET_VG"])

    # CHAR
    df = dataset["RESULTS_CHAR"]["RESULT_SWEEP"]
    xy = dataset["RESULTS_CHAR"]["RESULT_SWEEP_XY"]
    # labels
    xylabel = dataset["RESULTS_SIZING"]["RESULT_SWEEP_XY"]
    xysize = dataset["RESULTS_SIZING"]["RESULT_SIZE"]

    ax = axes[3]
    ax.plot(
        df["vd"],
        df["vth"],
        color=COLORS[num],
    )
    ax = axes[2]
    ax.axhline(
        xy["TARGET_VTH"],
        linewidth=0.5,
        linestyle=(0, (5, 5)),
        color='k',
        # marker="o",
        # markerfacecolor=COLORS[num],
        # label=f'V*={xylabel["TARGET_VSTAR"]:0.3f}V',
    )

    ax = axes[4]
    ax.plot(
        df["vd"],
        df["id"],
        color=COLORS[num],
    )
    ax.plot(
        xy["TARGET_VD"],
        xy["TARGET_ID"],
        marker="o",
        markerfacecolor=COLORS[num],
        label=f'V*={xylabel["TARGET_VSTAR"]:0.3f}V',
    )
    ax.set_ylim(0, 1.2 * xy["TARGET_ID"])
    ax.legend(loc="lower right")

    ax = axes[5]
    ax.plot(
        df["vd"],
        df["cgg"],
        color=COLORS[num],
        label=f'{xysize["WIDTH"]*1e6:0.1f}u/{xysize["LENGTH"]*1e6:0.1f}u',
    )
    ax.legend(loc="right")

    ax = axes[6]
    ax.plot(
        df["vd"],
        df["gm"],
        color=COLORS[num],
    )
    ax.plot(
        xy["TARGET_VD"],
        xy["TARGET_GM"],
        marker="o",
        markerfacecolor=COLORS[num],
    )
    ax.set_ylim(0, 1.2 * xy["TARGET_GM"])

    ax = axes[7]
    ax.plot(
        df["vd"],
        df["ro"],
        color=COLORS[num],
    )
    ax.plot(
        xy["TARGET_VD"],
        xy["TARGET_RO"],
        marker="o",
        markerfacecolor=COLORS[num],
    )
    ax.set_ylim(0, 1.2 * xy["TARGET_RO"])

    xlims = list(map(lambda x: x.get_xlim(), axes))
    ylims = list(map(lambda x: x.get_ylim(), axes))

    return {
        "xlims": xlims,
        "ylims": ylims,
    }


def set_limits(axes, plotlimits):
    xlims = [pl["xlims"] for pl in plotlimits]
    ylims = [pl["ylims"] for pl in plotlimits]

    xlims_lo = np.min(
        np.array(
            [[xpair[0] for xpair in xset] for xset in xlims],
        ),
        axis=0,
    )
    xlims_hi = np.max(
        np.array(
            [[xpair[1] for xpair in xset] for xset in xlims],
        ),
        axis=0,
    )
    ylims_lo = np.min(
        np.array(
            [[ypair[0] for ypair in yset] for yset in ylims],
        ),
        axis=0,
    )
    ylims_hi = np.max(
        np.array(
            [[ypair[1] for ypair in yset] for yset in ylims],
        ),
        axis=0,
    )

    xlims = np.vstack([xlims_lo, xlims_hi]).T
    ylims = np.vstack([ylims_lo, ylims_hi]).T

    deque(map(lambda ax, x: ax.set_xlim(*x), axes, xlims))
    deque(map(lambda ax, y: ax.set_ylim(*y), axes, ylims))

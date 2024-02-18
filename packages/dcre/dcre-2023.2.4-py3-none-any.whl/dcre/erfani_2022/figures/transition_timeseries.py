import matplotlib.pyplot as plt
import numpy as np

import dcre.erfani_2022.helpers as h  # noqa: E402


def calc_strong_tseries(var, var2, perc):
    """Calculate the timeseries of var2 when averaged over the 5-10% of the
    domain with the largest var."""
    outx = var[:, 0, 0].copy()
    outx[:] = np.nan
    for i in range(var.shape[0]):
        var_x = np.percentile(var[i, :, :], perc)
        ix = np.where(var[i, :, :] >= var_x)
        outx[i] = np.nanmean(var2[i, :, :][ix])
    return outx


def smooth_ends(var, box):
    out = var.copy()
    out = h.smooth(var, box)
    out[:box] = np.nan
    out[-box:] = np.nan
    # out = np.concatenate([var[:box], smooth(var, box)[box:]])#-box, var[-box:]])
    return out


def transition_timeseries(fn3d, cases, box, styles):
    PANELS = ["a)", "b)", "c)", "d)"]
    lb = styles["labels"]
    ls = styles["linestyles"]
    lw = styles["linewidths"]
    clr = styles["label_group_colors"]

    fig1, axis = plt.subplots(4, 1, figsize=(14, 18))

    i = 0
    axis[i].set_ylabel("LCC (%)", fontsize=22)
    axis[i].set_ylim([0, 105])
    axis[i].set_xlim([-1, 1])
    axis[i].axes.get_xaxis().set_ticklabels([])
    axis[i].tick_params(axis="both", which="major", labelsize=18)
    axis[i].grid(linestyle=":", linewidth=1)
    axis[i].text(
        0.04,
        1.1,
        PANELS[i],
        transform=axis[i].transAxes,
        fontsize=22,
        fontweight="bold",
        va="top",
        fontfamily="serif",
        ha="right",
    )

    i = 1
    axis[i].set_ylabel("LWP ($g$ $m^{-2}$)", fontsize=22)
    axis[i].set_ylim([0, 170])
    axis[i].set_xlim([-1, 1])
    axis[i].axes.get_xaxis().set_ticklabels([])
    axis[i].tick_params(axis="both", which="major", labelsize=18)
    axis[i].grid(linestyle=":", linewidth=1)
    axis[i].text(
        0.04,
        1.1,
        PANELS[i],
        transform=axis[i].transAxes,
        fontsize=22,
        fontweight="bold",
        va="top",
        fontfamily="serif",
        ha="right",
    )

    i = 2
    axis[i].set_ylabel("95$^{th}$ pctl LWP $<N_c>^{-1}$", fontsize=22)
    axis[i].set_ylim([0, 25])
    axis[i].set_xlim([-1, 1])
    axis[i].axes.get_xaxis().set_ticklabels([])
    axis[i].tick_params(axis="both", which="major", labelsize=18)
    axis[i].grid(linestyle=":", linewidth=1)
    axis[i].text(
        0.04,
        1.1,
        PANELS[i],
        transform=axis[i].transAxes,
        fontsize=22,
        fontweight="bold",
        va="top",
        fontfamily="serif",
        ha="right",
    )

    i = 3
    axis[i].set_xlabel("Time (SCT as 0)", fontsize=22)
    axis[i].set_ylabel("95$^{th}$ pctl Prec. ($mm$ $d^{-1}$)", fontsize=22)
    axis[i].set_xlim([-1, 1])
    axis[i].tick_params(axis="both", which="major", labelsize=18)
    axis[i].grid(linestyle=":", linewidth=1)
    axis[i].text(
        0.04,
        1.1,
        PANELS[i],
        transform=axis[i].transAxes,
        fontsize=22,
        fontweight="bold",
        va="top",
        fontfamily="serif",
        ha="right",
    )

    ####
    for jj in cases:
        T3D = fn3d[jj].variables["time"][:]  # time: day
        t3d = T3D - int(T3D[0])
        #    x        = fn3d[jj].variables['x'][:] / 1000   # $km$
        #    y        = fn3d[jj].variables['y'][:] / 1000   # $km$
        CLD2d = fn3d[jj].variables["CLD"][:]
        Prec = fn3d[jj].variables["Prec"][:]  # * 1000    # Surface Precip. Rate: g/m
        QCPATH = fn3d[jj].variables["QCPATH"][
            :
        ]  # * 1000    # Column cloud liquid mass (vertically integrated), before conversion to unit: g/m2
        NCQCPATH = fn3d[jj].variables["NCQCPATH"][
            :
        ]  # Column integral of QC*NC (useful for computing mass-weighted NC): kg/kg/m2
        CDNC = NCQCPATH / QCPATH  # #/mg
        CDNC = CDNC * 1e-6  # #/mg
        #    x_mg, y_mg = np.meshgrid(x, y) # making meshgrid

        CWP3d = QCPATH * 1000  # + QP
        CWP_Nc = CWP3d / CDNC
        #   looking at the timeseries of CWP/Nd when averaged over the 5-10% of the domain with the largest CWP.
        CWP_Nc95 = calc_strong_tseries(CWP3d, CWP_Nc, 95)
        Prec95 = calc_strong_tseries(Prec, Prec, 95)
        #    Prec95 = calc_strong_tseries(Prec, Prec, 95)
        #    CWP3d95 = calc_strong_tseries(CWP3d, CWP3d, 95)

        CLD2d_m = np.nanmean(np.nanmean(CLD2d, 2), 1)
        i_50 = np.where((CLD2d_m > 48) & ((CLD2d_m < 52)))[0]
        if len(i_50) == 0:
            i_50 = np.where((CLD2d_m > 45) & ((CLD2d_m < 55)))[0]
        if lb[jj] == "110-60" or lb[jj] == "250-60-LD":
            i_sct = -1
        else:
            i_sct = 0
        t_sct = t3d[i_50[i_sct]]

        t_new = t3d - t_sct

        i = 0
        axis[i].plot(
            t_new,
            smooth_ends(CLD2d_m, box),
            ls[jj],
            linewidth=lw[jj],
            color=clr[jj],
            label=lb[jj],
        )
        i = 1
        axis[i].plot(
            t_new,
            smooth_ends(np.nanmean(np.nanmean(CWP3d, 2), 1), box),
            ls[jj],
            linewidth=lw[jj],
            color=clr[jj],
            label=lb[jj],
        )
        i = 2
        axis[i].plot(
            t_new,
            smooth_ends(CWP_Nc95, box),
            ls[jj],
            linewidth=lw[jj],
            color=clr[jj],
            label=lb[jj],
        )
        i = 3
        axis[i].plot(
            t_new,
            smooth_ends(Prec95, box),
            ls[jj],
            linewidth=lw[jj],
            color=clr[jj],
            label=lb[jj],
        )
        axis[i].legend(fontsize=17.5, loc="upper left", ncol=2)
    plt.tight_layout()  # w_pad=1
    plt.savefig("all_SCT.pdf", format="pdf", dpi=500)
    return fig1

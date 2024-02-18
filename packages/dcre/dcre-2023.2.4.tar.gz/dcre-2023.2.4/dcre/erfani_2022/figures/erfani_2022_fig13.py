import matplotlib.pyplot as plt

from .. import erfani_decomp_func as ed  # noqa: E402

PANELS1 = ["a)", "b)", "c)", "d)", "e)", "f)", "g)", "h)"]
marker10 = ["o", "s", "d", "^", "+", "x", "*", "p"]
color2 = ["k", "b", "tab:red", "tab:green", "k", "b", "tab:red", "tab:green"]


def fig13(res, lb):
    r_positive = res.loc[
        (slice(None), slice(None), slice(None), slice(None), slice(None), 1)
    ]
    r_negative = res.loc[
        (slice(None), slice(None), slice(None), slice(None), slice(None), -1)
    ]
    assert len(r_positive) == len(r_negative), "Datasets must have same length."

    fig, axis = plt.subplots(2, 2, figsize=(12, 10))

    metadata = {
        (0, 0): {"ylabel": "$ΔA_c$", "title": "L06"},
        (0, 1): {"ylabel": None, "title": "L10"},
        (1, 0): {"ylabel": "$-ΔR$ ($W$ $m^{-2}$)", "title": None},
        (1, 1): {"ylabel": None, "title": None},
    }

    for i, j in [(0, 0), (0, 1), (1, 0), (1, 1)]:
        axis[i, j].set_ylabel(metadata[(i, j)]["ylabel"], fontsize="18")
        axis[i, j].set_title(metadata[(i, j)]["title"], fontsize="23")
        axis[i, j].set_xlim([0.5, 10])
        if i == 0:
            axis[i, j].set_ylim([-0.025, 0.1])
        else:
            axis[i, j].set_ylim([-35, 120])
        axis[i, j].tick_params(axis="both", which="major", labelsize=14)
        axis[i, j].grid(linestyle=":", linewidth=1)  # axis='y',
        axis[i, j].text(
            0.1,
            1.08,
            PANELS1[i * 2 + j],
            transform=axis[i, j].transAxes,
            fontsize=18,
            fontweight="bold",
            va="top",
            fontfamily="serif",
            ha="right",
        )

    #####
    for ii in range(len(r_positive)):
        rp = r_positive.iloc[ii]
        rn = r_negative.iloc[ii]

        (
            rN_nan_fd,
            rL_nan_fd,
            rC_nan_fd,
            CRE_M_fd,
            CRE_T_fd,
            CRE_L_fd,
            CRE_CF_fd,
            CRE_rs_fd,
            A_M_fd,
            A_T_fd,
            A_L_fd,
            A_CF_fd,
            A_rs_fd,
            CRE_M_fd1,
            CRE_T_fd1,
            CRE_L_fd1,
            CRE_CF_fd1,
            CRE_rs_fd1,
            A_M_fd1,
            A_T_fd1,
            A_L_fd1,
            A_CF_fd1,
            A_rs_fd1,
            CRE_M_fd2,
            CRE_T_fd2,
            CRE_L_fd2,
            CRE_CF_fd2,
            CRE_rs_fd2,
            A_M_fd2,
            A_T_fd2,
            A_L_fd2,
            A_CF_fd2,
            A_rs_fd2,
            CF1_nan_fd,
            CF2_nan_fd,
            CF_nan_fd,
        ) = ed.quant_CRE_avg(rp, rn, output="extended")

        ####
        i = 0
        if ii < len(r_positive) // 2:
            j = 0
        else:
            j = 1
        axis[i, j].errorbar(
            rN_nan_fd,
            A_T_fd,
            yerr=abs(A_T_fd2 - A_T_fd1) / 2,
            markersize=10,
            fmt=marker10[1],
            color=color2[ii],
            mfc="white",
        )
        axis[i, j].errorbar(
            rN_nan_fd,
            A_L_fd,
            yerr=abs(A_L_fd2 - A_L_fd1) / 2,
            markersize=10,
            fmt=marker10[2],
            color=color2[ii],
            mfc="white",
        )
        axis[i, j].errorbar(
            rN_nan_fd,
            A_rs_fd,
            yerr=abs(A_rs_fd2 - A_rs_fd1) / 2,
            markersize=10,
            fmt=marker10[4],
            color=color2[ii],
            mfc="white",
        )
        axis[i, j].errorbar(
            rN_nan_fd,
            A_CF_fd,
            yerr=abs(A_CF_fd2 - A_CF_fd1) / 2,
            markersize=10,
            fmt=marker10[3],
            color=color2[ii],
            mfc="white",
        )

        axis[i, j].scatter(
            rN_nan_fd,
            A_M_fd,
            s=160,
            marker=marker10[0],
            color=color2[ii],
            edgecolors="y",
            label="-[(" + lb[rp.name[1]] + ")" + " - " + "(" + lb[rp.name[0]] + ")]",
        )
        if j == 0:
            axis[i, j].legend(fontsize="14", loc="lower right")
        elif j == 1:
            axis[i, j].legend(fontsize="14", loc="upper right")

        ####
        i = 1
        if ii < len(r_positive) // 2:
            j = 0
        else:
            j = 1

        if ii == 4:  # ii == 0 or
            pp1 = axis[i, j].scatter(
                rN_nan_fd,
                -CRE_M_fd,
                s=140,
                marker=marker10[0],
                facecolors="none",
                edgecolors=color2[ii],
            )
            pp2 = axis[i, j].errorbar(
                rN_nan_fd,
                -CRE_T_fd,
                yerr=abs(CRE_T_fd2 - CRE_T_fd1) / 2,
                markersize=10,
                fmt=marker10[1],
                color=color2[ii],
                mfc="white",
            )
            pp3 = axis[i, j].errorbar(
                rN_nan_fd,
                -CRE_L_fd,
                yerr=abs(CRE_L_fd2 - CRE_L_fd1) / 2,
                markersize=10,
                fmt=marker10[2],
                color=color2[ii],
                mfc="white",
            )
            pp4 = axis[i, j].errorbar(
                rN_nan_fd,
                -CRE_CF_fd,
                yerr=abs(CRE_CF_fd2 - CRE_CF_fd1) / 2,
                markersize=10,
                fmt=marker10[3],
                color=color2[ii],
                mfc="white",
            )
            pp5 = axis[i, j].errorbar(
                rN_nan_fd,
                -CRE_rs_fd,
                yerr=abs(CRE_rs_fd2 - CRE_rs_fd1) / 2,
                markersize=10,
                fmt=marker10[4],
                color=color2[ii],
                mfc="white",
            )
        axis[i, j].errorbar(
            rN_nan_fd,
            -CRE_T_fd,
            yerr=abs(CRE_T_fd2 - CRE_T_fd1) / 2,
            markersize=10,
            fmt=marker10[1],
            color=color2[ii],
            mfc="white",
        )
        axis[i, j].errorbar(
            rN_nan_fd,
            -CRE_L_fd,
            yerr=abs(CRE_L_fd2 - CRE_L_fd1) / 2,
            markersize=10,
            fmt=marker10[2],
            color=color2[ii],
            mfc="white",
        )
        axis[i, j].errorbar(
            rN_nan_fd,
            -CRE_CF_fd,
            yerr=abs(CRE_CF_fd2 - CRE_CF_fd1) / 2,
            markersize=10,
            fmt=marker10[3],
            color=color2[ii],
            mfc="white",
        )
        axis[i, j].errorbar(
            rN_nan_fd,
            -CRE_rs_fd,
            yerr=abs(CRE_rs_fd2 - CRE_rs_fd1) / 2,
            markersize=10,
            fmt=marker10[4],
            color=color2[ii],
            mfc="white",
        )

        axis[i, j].scatter(
            rN_nan_fd,
            -CRE_M_fd,
            s=160,
            marker=marker10[0],
            color=color2[ii],
            edgecolors="y",
            label="-[(" + lb[rp.name[1]] + ")" + " - " + "(" + lb[rp.name[0]] + ")]",
        )

    leg2 = axis[1, 1].legend(
        [pp1, pp2, pp3, pp4, pp5],
        ["Total", "$N_c$", "LWP", "CF", "Residual"],
        fontsize="14",
        loc="upper left",
    )

    plt.tight_layout()  # w_pad=1
    return fig

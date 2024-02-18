import matplotlib.pyplot as plt

from .. import erfani_decomp_func as ed  # noqa: E402

PANELS1 = ["a)", "b)", "c)", "d)", "e)", "f)", "g)", "h)"]
color2 = ["k", "b", "tab:red", "tab:green", "k", "b", "tab:red", "tab:green"]
marker = ["o", "x", "s", "*", "^", "+", "d", "p"]


def fig14(res, lb):
    r_positive = res.loc[
        (slice(None), slice(None), slice(None), slice(None), slice(None), 1)
    ]
    r_negative = res.loc[
        (slice(None), slice(None), slice(None), slice(None), slice(None), -1)
    ]
    assert len(r_positive) == len(r_negative), "Datasets must have same length."

    fig, axis = plt.subplots(2, 2, figsize=(11, 10))

    i = 0
    j = 0
    axis[i, j].set_ylabel("$r_C$", fontsize="18")
    axis[i, j].set_xlabel("$r_N$", fontsize="18")
    axis[i, j].set_title("L06", fontsize="23")
    axis[i, j].set_xlim([0.5, 10])
    axis[i, j].set_ylim([0.75, 3.5])
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

    ####
    i = 0
    j = 1
    axis[i, j].set_xlabel("$r_N$", fontsize="18")
    axis[i, j].set_title("L10", fontsize="23")
    axis[i, j].set_xlim([0.5, 10])
    axis[i, j].set_ylim([0.75, 3.5])
    axis[i, j].tick_params(axis="both", which="major", labelsize=14)
    axis[i, j].grid(linestyle=":", linewidth=1)
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

    ####
    i = 1
    j = 0
    axis[i, j].set_ylabel("$r_N$", fontsize="18")
    axis[i, j].set_xlabel("$r_L$", fontsize="18")
    axis[i, j].set_xlim([0.8, 1.75])
    axis[i, j].set_ylim([0.5, 10])
    axis[i, j].tick_params(axis="both", which="major", labelsize=14)
    axis[i, j].grid(linestyle=":", linewidth=1)
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

    ####
    i = 1
    j = 1
    axis[i, j].set_xlabel("$r_L$", fontsize="18")
    axis[i, j].set_xlim([0.8, 1.75])
    axis[i, j].set_ylim([0.5, 10])
    axis[i, j].tick_params(axis="both", which="major", labelsize=14)
    axis[i, j].grid(linestyle=":", linewidth=1)
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
            CF1_nan_fd,
            CF2_nan_fd,
            CF_nan_fd,
        ) = ed.quant_CRE_avg(rp, rn, output="normal")

        ####
        if ii < len(r_positive) // 2:
            i = 0
            j = 0
        else:
            i = 0
            j = 1
        axis[i, j].scatter(
            rN_nan_fd,
            rC_nan_fd,
            s=160,
            marker=marker[0],
            color=color2[ii],
            label="(" + lb[rp.name[1]] + ")" + " / " + "(" + lb[rp.name[0]] + ")",
        )
        axis[i, j].legend(fontsize="14")

        ####
        if ii < len(r_positive) // 2:
            i = 1
            j = 0
        else:
            i = 1
            j = 1
        axis[i, j].scatter(
            rL_nan_fd,
            rN_nan_fd,
            s=160,
            marker=marker[0],
            color=color2[ii],
            label="(" + lb[rp.name[1]] + ")" + " / " + "(" + lb[rp.name[0]] + ")",
        )

    plt.tight_layout()
    return fig

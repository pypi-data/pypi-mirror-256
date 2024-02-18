import matplotlib.pyplot as plt


def cre_timeseries(res, time, lb, upbound, init_time_all, lngh=5):
    xlim = time[-1]

    fig, axis = plt.subplots(2, 4, figsize=(25, 11))
    i = 0
    j = 0

    r_positive = res.loc[
        (slice(None), slice(None), slice(None), slice(None), slice(None), 1)
    ]
    r_negative = res.loc[
        (slice(None), slice(None), slice(None), slice(None), slice(None), -1)
    ]

    assert len(r_positive) == len(r_negative), "Datasets must have same length."

    for ii in range(len(r_positive)):
        rp = r_positive.iloc[ii]
        rn = r_negative.iloc[ii]
        j = ii % 4 if ii <= 6 else 3
        i = 0 if ii <= 3 else 1

        if j == 0 and i == 0:
            axis[i, j].set_ylabel("L06\n$ΔR$ ($W$ $m^{-2}$)", fontsize="20")
        elif j == 0 and i == 1:
            axis[i, j].set_ylabel("L10\n$ΔR$ ($W$ $m^{-2}$)", fontsize="20")

        (
            rN,
            rL,
            rC_nan_fd,
            CRE_M,
            CRE_T,
            CRE_L,
            CRE_CF,
            CRE_rs,
            A_M,
            A_T,
            A_L,
            A_CF,
            A_rs,
            CRE1,
            CRE2,
            CF1,
        ) = rp

        axis[i, j].fill_between(time, -upbound, upbound, color="k", alpha=0.075)
        axis[i, j].set_xlabel(
            "Time (days since " + init_time_all[ii] + ")", fontsize="20"
        )
        axis[i, j].set_xlim([0, xlim + xlim / lngh])
        axis[i, j].tick_params(axis="both", which="major", labelsize=16)
        axis[i, j].grid(linestyle=":", axis="y", linewidth=1)

        if i == 0:
            axis[i, j].set_ylim([-360, 70])
        else:
            axis[i, j].set_ylim([-205, 100])

        (
            rN,
            rL,
            rC_nan_fd,
            CRE_M2,
            CRE_T2,
            CRE_L2,
            CRE_CF2,
            CRE_rs2,
            A_M,
            A_T,
            A_L,
            A_CF,
            A_rs,
            CRE1_2,
            CRE2_2,
            CF2,
        ) = rn

        #####
        if i == 0 and j == 0:
            axis[i, j].set_xlim([0, xlim + xlim / lngh])
            axis[i, j].plot(
                time, (CRE_T + CRE_T2) / 2, linewidth=1, color="tab:red", label="CDNC"
            )
            axis[i, j].plot(
                time, (CRE_L + CRE_L2) / 2, linewidth=1, color="tab:green", label="LWP"
            )
            axis[i, j].plot(
                time, (CRE_CF + CRE_CF2) / 2, linewidth=1, color="k", label="CF"
            )
            axis[i, j].plot(
                time,
                (CRE_rs + CRE_rs2) / 2,
                linewidth=1,
                color="deepskyblue",
                label="residual",
            )
        else:
            axis[i, j].set_xlim([0, xlim + xlim / lngh])
            axis[i, j].plot(time, (CRE_T + CRE_T2) / 2, linewidth=1, color="tab:red")
            axis[i, j].plot(time, (CRE_L + CRE_L2) / 2, linewidth=1, color="tab:green")
            axis[i, j].plot(time, (CRE_CF + CRE_CF2) / 2, linewidth=1, color="k")
            axis[i, j].plot(
                time, (CRE_rs + CRE_rs2) / 2, linewidth=1, color="deepskyblue"
            )
        axis[i, j].plot(
            time,
            (CRE_M + CRE_M2) / 2,
            "-",
            linewidth=1,
            color="b",
            label="(" + lb[rp.name[1]] + ")" + " - " + "(" + lb[rp.name[0]] + ")",
        )
        axis[i, j].legend(fontsize="15", loc="lower right")

    plt.tight_layout(w_pad=1)
    return fig

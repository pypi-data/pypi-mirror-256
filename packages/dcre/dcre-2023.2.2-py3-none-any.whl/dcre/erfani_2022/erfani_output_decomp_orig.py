import numpy as np  # linear algebra

import dcre.erfani_2022.helpers as h  # noqa: E402


def quant_CRE_alltime_old(fn1, fn2, a_ft, box, factor=1, cre_scaling=False):
    (
        time,
        z,
        dz,
        RHO,
        CWP,
        RWP,
        ISCCPTOT,
        ZINV,
        entr,
        LWNTOA,
        SWNS,
        P,
        TABS,
        inv_idx,
        W2_Zinv_200,
        acc_prec,
        THETA,
        QT,
        integ_NA_BL,
        integ_NC_BL,
        COD,
        SAM_re,
        height_NARC,
        height_ENTRNMT,
        height_NASURF,
        height_NPRA,
        height_NASED,
        height_NASCAV,
        sfc_wnd,
        albedo,
        NA,
        NC,
        PREC,
        RH,
        albd_clear,
        SOLIN2,
        SW_CRE,
        SWNTOAC,
        PRECIP,
        CLD,
        W2,
        WOBS,
        QV,
    ) = h.read_model_vars(fn1)

    # CF1  = smooth(ISCCPTOT, 10)
    CF1 = ISCCPTOT
    #     T_ft1= SWNTOAC / SOLIN2  # old method: transmissivity of the free troposphere
    RADSWDN = fn1.variables["RADSWDN"][:]  # Downward shortwave radiative flux: W/m2
    RADSWDN_Zinv = SOLIN2.copy()
    RADSWDN_Zinv[:] = np.nan
    for ij in range(len(RADSWDN_Zinv)):
        RADSWDN_Zinv[ij] = RADSWDN[ij, inv_idx[ij] + 5]
    T_ft1 = RADSWDN_Zinv / SOLIN2  # new method: transmissivity of the free troposphere

    A1 = (albedo - (1 - CF1) * albd_clear) / CF1  # Chen B2
    # A1   = albedo
    a1 = (a_ft - A1) / (a_ft**2 - A1 * a_ft - T_ft1**2)
    # a1   = albedo #/ CF1
    N1 = np.concatenate([integ_NC_BL[:3], h.smooth(integ_NC_BL, box)[3:]])

    # L1   = h.smooth((CWP + RWP)/CF1, 10)
    L1 = h.smooth(CWP + RWP, 10)
    CRE1 = -a1 * SOLIN2 * CF1

    if cre_scaling is True:
        fact = SW_CRE / CRE1
        CRE1 = CRE1 * fact
    else:
        fact = 1
    # CRE1 = SW_CRE
    A1clr = albd_clear

    #####
    (
        _,
        _,
        _,
        _,
        CWP,
        RWP,
        ISCCPTOT,
        _,
        _,
        _,
        _,
        _,
        _,
        inv_idx,
        _,
        _,
        _,
        _,
        _,
        integ_NC_BL,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        albedo,
        _,
        _,
        _,
        _,
        albd_clear,
        SOLIN2,
        SW_CRE,
        _,
        _,
        _,
        _,
        _,
        _,
    ) = h.read_model_vars(fn2)

    CF2 = ISCCPTOT
    RADSWDN = fn2.variables["RADSWDN"][:]  # Downward shortwave radiative flux: W/m2
    RADSWDN_Zinv = SOLIN2.copy()
    RADSWDN_Zinv[:] = np.nan
    for ij in range(len(RADSWDN_Zinv)):
        RADSWDN_Zinv[ij] = RADSWDN[ij, inv_idx[ij] + 5]
    T_ft2 = RADSWDN_Zinv / SOLIN2  # new method: transmissivity of the free troposphere

    A2 = (albedo - (1 - CF2) * albd_clear) / CF2  # Chen B2 --> A2 = cloud albedo
    # A2   = albedo
    a2 = (a_ft - A2) / (a_ft**2 - A2 * a_ft - T_ft2**2)  # Chen B7 multiplied by -1
    N2 = np.concatenate([integ_NC_BL[:3], h.smooth(integ_NC_BL, box)[3:]])
    # L2   = h.smooth((CWP + RWP)/CF2, 10)
    L2 = h.smooth(CWP + RWP, 10)
    CRE2 = -a2 * SOLIN2 * CF2
    CRE2 = CRE2 * fact  # SW_CRE / CRE1 # Erfani et al. (2022)
    A2clr = albd_clear

    ###
    # CRE_M = - (A2 - A1) * SOLIN2 * fact * CF1
    CRE_M = factor * (CRE2 - CRE1)
    A_M = A2 - A1

    ### Twomey Effect:
    rN = N2 / N1
    a_T = a1 + factor * a1 * (1 - a1) * (
        rN ** (1 / 3) - 1
    ) / (  # complicated form of B6a derived from Wood (2021) Eq. 2
        1 + a1 * (rN ** (1 / 3) - 1)
    )
    A_T = a_ft + a_T * T_ft1**2 / (1 - a_ft * a_T)  # Chen B8 for Nc
    CRE_T = (
        -(A_T - A1) * SOLIN2 * CF1
    ) * fact  # Chen eq after B8, part for Nc; why fact(SW_CRE / CRE1)?

    ### LWP adjustment Effect:
    rL = L2 / L1
    a_L = a1 + factor * a1 * (1 - a1) * (rL ** (5 / 6) - 1) / (
        1 + a1 * (rL ** (5 / 6) - 1)
    )
    A_L = a_ft + a_L * T_ft1**2 / (1 - a_ft * a_L)  # Chen B8 for LWP
    CRE_L = (
        -(A_L - A1) * SOLIN2 * CF1
    ) * fact  # Chen eq after B8, part for Nc; why fact(SW_CRE / CRE1)?

    ### CF adjustment Effect:
    #    A_CF   = (CF2 - CF1) * (A2 - A2clr)
    #    A_CF   = A1 + (CF2 - CF1) * (A2 - A2clr)

    A_CF = A_T.copy()

    for i in range(len(CF1)):
        if (
            CF2[i] > CF1[i]
        ):  # what is the reasoning behind this? depending on the run with the higher cloud fraction, the albedo change to its reference is used. Works if clear-sky fluxes are available in cloudy columns.
            A_CF[i] = A1[i] + (CF2[i] - CF1[i]) * (A2[i] - A2clr[i])
        else:
            A_CF[i] = A1[i] + (CF2[i] - CF1[i]) * (A1[i] - A1clr[i])  # A1 gets added

    CRE_CF = -1 * factor * (A_CF - A1) * SOLIN2 * fact  # A1 gets subtracted again

    ### residual:
    A_rs = A_T + A_L + A_CF - A_M
    CRE_rs = CRE_T + CRE_L + CRE_CF - CRE_M

    rC = CF2 / CF1

    return (
        rN,
        rL,
        rC,
        CRE_M,
        CRE_T,
        CRE_L,
        CRE_CF,
        CRE_rs,
        A1,
        A_T,
        A_L,
        A_CF,
        A_rs,
        CRE1,
        CRE2,
        CF1,
    )

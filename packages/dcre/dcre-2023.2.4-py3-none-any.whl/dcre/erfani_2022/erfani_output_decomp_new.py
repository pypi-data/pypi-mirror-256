import numpy as np  # linear algebra

import dcre.cre_decomposition as decomp  # noqa: E402
import dcre.erfani_2022.helpers as h  # noqa: E402


def quant_CRE_alltime_new(fn1, fn2, a_ft, box, factor=1, cre_scaling=False):
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
    # CF1 = ISCCPTOT
    #     T_ft1= SWNTOAC / SOLIN2  # old method: transmissivity of the free troposphere
    RADSWDN = fn1.variables["RADSWDN"][:]  # Downward shortwave radiative flux: W/m2
    RADSWDN_Zinv = SOLIN2.copy()
    RADSWDN_Zinv[:] = np.nan
    for ij in range(len(RADSWDN_Zinv)):
        RADSWDN_Zinv[ij] = RADSWDN[ij, inv_idx[ij] + 5]
    T_ft1 = RADSWDN_Zinv / SOLIN2  # new method: transmissivity of the free troposphere

    N1 = np.concatenate([integ_NC_BL[:3], h.smooth(integ_NC_BL, box)[3:]])
    L1 = h.smooth(CWP + RWP, 10)
    simulation1 = decomp.Simulation(
        CWP=L1,
        CF=ISCCPTOT,
        inv_idx=inv_idx,
        NCCN=N1,
        albedo=albedo,
        albd_clear=albd_clear,
        SOLIN=SOLIN2,
        sw_dwn_profile=RADSWDN_Zinv,
    )

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

    RADSWDN = fn2.variables["RADSWDN"][:]  # Downward shortwave radiative flux: W/m2
    RADSWDN_Zinv = SOLIN2.copy()
    RADSWDN_Zinv[:] = np.nan
    for ij in range(len(RADSWDN_Zinv)):
        RADSWDN_Zinv[ij] = RADSWDN[ij, inv_idx[ij] + 5]
    T_ft2 = RADSWDN_Zinv / SOLIN2  # new method: transmissivity of the free troposphere

    N = np.concatenate([integ_NC_BL[:3], h.smooth(integ_NC_BL, box)[3:]])
    L = h.smooth(CWP + RWP, 10)
    simulation2 = decomp.Simulation(
        CWP=L,
        CF=ISCCPTOT,
        inv_idx=inv_idx,
        NCCN=N,
        albedo=albedo,
        albd_clear=albd_clear,
        SOLIN=SOLIN2,
        sw_dwn_profile=RADSWDN_Zinv,
    )

    CRE_Decomposer = decomp.CRE_Decompositer(simulation1, simulation2)
    CRE_Decomposer.decompose(factor=factor, cre_scaling=cre_scaling)

    return CRE_Decomposer.return_erfani_2022()

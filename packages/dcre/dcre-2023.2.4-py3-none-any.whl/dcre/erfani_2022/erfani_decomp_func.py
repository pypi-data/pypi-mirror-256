import numpy as np  # linear algebra

from . import erfani_output_decomp_new as dn
from . import erfani_output_decomp_orig as do


def quant_CRE_alltime(
    fn1, fn2, a_ft, box, factor=1, cre_scaling=False, mode="erfani_2022"
):
    if mode == "erfani_2022":
        return do.quant_CRE_alltime_old(
            fn1, fn2, a_ft, box, factor=factor, cre_scaling=cre_scaling
        )
    elif mode == "decomposer":
        return dn.quant_CRE_alltime_new(
            fn1, fn2, a_ft, box, factor=factor, cre_scaling=cre_scaling
        )


def quant_CRE_avg(j1j2, j2j1, output="normal"):
    (
        rN1,
        rL1,
        rC1,
        CRE_M1,
        CRE_T1,
        CRE_L1,
        CRE_CF1,
        CRE_rs1,
        A1,
        A_T1,
        A_L1,
        A_CF1,
        A_rs1,
        CRE1,
        CRE2,
        CF1,
    ) = j1j2
    (
        rN2,
        rL2,
        rC2,
        CRE_M2,
        CRE_T2,
        CRE_L2,
        CRE_CF2,
        CRE_rs2,
        A1_2,
        A_T2,
        A_L2,
        A_CF2,
        A_rs2,
        CRE1_2,
        CRE2_2,
        CF2,
    ) = j2j1

    rN = (rN1 + 1 / rN2) / 2
    rL = (rL1 + 1 / rL2) / 2
    rC = (rC1 + 1 / rC2) / 2

    CRE_T = (CRE_T1 + CRE_T2) / 2
    CRE_L = (CRE_L1 + CRE_L2) / 2
    CRE_CF = (CRE_CF1 + CRE_CF2) / 2
    CRE_rs = (CRE_rs1 + CRE_rs2) / 2
    CRE_M = (CRE_M1 + CRE_M2) / 2

    A_T = (A_T1 - A1 + A_T2 - A1_2) / 2
    A_L = (A_L1 - A1 + A_L2 - A1_2) / 2
    A_CF = (A_CF1 - A1 + A_CF2 - A1_2) / 2
    A_rs = (A_rs1 - A1 + A_rs2 - A1_2) / 2
    A_M = A1_2 - A1

    CF = (CF1 + CF2) / 2

    CF1_nan = CF.copy()  # CF1.copy()?
    CF2_nan = CF.copy()  # CF2.copy()?
    CF_nan = CF.copy()
    # CF1_nan[np.isnan(SOLIN2) == 1] = np.nan
    # CF2_nan[np.isnan(SOLIN2) == 1] = np.nan
    # CF_nan[np.isnan(SOLIN2) == 1] = np.nan

    CF1_nan_fd = np.nanmean(CF1_nan[10:-10])
    CF2_nan_fd = np.nanmean(CF2_nan[10:-10])
    CF_nan_fd = np.nanmean(CF_nan[10:-10])

    rN_nan = rN.copy()
    rL_nan = rL.copy()
    rC_nan = rC.copy()
    # rN_nan[np.isnan(SOLIN2) == 1] = np.nan
    # rL_nan[np.isnan(SOLIN2) == 1] = np.nan
    # rC_nan[np.isnan(SOLIN2) == 1] = np.nan

    rN_nan_fd = np.nanmean(rN_nan[10:-10])
    rL_nan_fd = np.nanmean(rL_nan[10:-10])
    rC_nan_fd = np.nanmean(rC_nan[10:-10])

    CRE_M_fd = np.nanmean(CRE_M[10:-10])
    CRE_T_fd = np.nanmean(CRE_T[10:-10])
    CRE_L_fd = np.nanmean(CRE_L[10:-10])
    CRE_CF_fd = np.nanmean(CRE_CF[10:-10])
    CRE_rs_fd = np.nanmean(CRE_rs[10:-10])

    A_M_fd = np.nanmean(A_M[10:-10])
    A_T_fd = np.nanmean(A_T[10:-10])
    A_L_fd = np.nanmean(A_L[10:-10])
    A_CF_fd = np.nanmean(A_CF[10:-10])
    A_rs_fd = np.nanmean(A_rs[10:-10])

    if output == "extended":
        CRE_M_fd1 = np.nanmean(CRE_M1[10:-10])
        CRE_T_fd1 = np.nanmean(CRE_T1[10:-10])
        CRE_L_fd1 = np.nanmean(CRE_L1[10:-10])
        CRE_CF_fd1 = np.nanmean(CRE_CF1[10:-10])
        CRE_rs_fd1 = np.nanmean(CRE_rs1[10:-10])

        CRE_M_fd2 = np.nanmean(CRE_M2[10:-10])
        CRE_T_fd2 = np.nanmean(CRE_T2[10:-10])
        CRE_L_fd2 = np.nanmean(CRE_L2[10:-10])
        CRE_CF_fd2 = np.nanmean(CRE_CF2[10:-10])
        CRE_rs_fd2 = np.nanmean(CRE_rs2[10:-10])

        A_M_fd1 = np.nanmean(A1[10:-10])
        A_T_fd1 = np.nanmean((A_T1 - A1)[10:-10])
        A_L_fd1 = np.nanmean((A_L1 - A1)[10:-10])
        A_CF_fd1 = np.nanmean((A_CF1 - A1)[10:-10])
        A_rs_fd1 = np.nanmean((A_rs1 - A1)[10:-10])

        A_M_fd2 = np.nanmean(A1_2[10:-10])
        A_T_fd2 = np.nanmean((A_T2 - A1_2)[10:-10])
        A_L_fd2 = np.nanmean((A_L2 - A1_2)[10:-10])
        A_CF_fd2 = np.nanmean((A_CF2 - A1_2)[10:-10])
        A_rs_fd2 = np.nanmean((A_rs2 - A1_2)[10:-10])

    if output == "normal":
        return (
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
        )
    elif output == "extended":
        return (
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
        )


def quant_CRE(
    fn1, fn2, a_ft, box, cre_scaling=False, mode="erfani_2022", output="normal"
):
    j1j2 = quant_CRE_alltime(
        fn1, fn2, a_ft, box, factor=1, cre_scaling=cre_scaling, mode=mode
    )
    j2j1 = quant_CRE_alltime(
        fn2, fn1, a_ft, box, factor=-1, cre_scaling=cre_scaling, mode=mode
    )
    return quant_CRE_avg(j1j2, j2j1)

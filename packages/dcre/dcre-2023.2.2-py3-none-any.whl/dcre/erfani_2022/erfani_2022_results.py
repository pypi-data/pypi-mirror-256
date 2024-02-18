#!/usr/bin/env python
# coding: utf-8

import hashlib

import pandas as pd
from netCDF4 import Dataset

from . import erfani_decomp_func as ed  # noqa: E402

##### read various files and variables
## model runs

datasets = {
    "fn2": [
        "./data/OUT_STAT/CSET_RF06_Tr2p3_256sqx432_100m_M2005PA_RRTM4PBL_UM5_ProgAer_40_40.nc",
        "./data/OUT_STAT/CSET_RF06_Tr2p3_96sqx432_100m_M2005PA_RRTM4PBL_UM5_ProgAer_va_1_4.nc",
        "./data/OUT_STAT/CSET_RF06_Tr2p3_96sqx432_100m_M2005PA_RRTM4PBL_UM5_ProgAer_BL40_FT40_150.nc",
        "./data/OUT_STAT/CSET_RF06_Tr2p3_96sqx432_100m_M2005PA_RRTM4PBL_UM5_ProgAer_vc_BL_150.nc",
        "./data/OUT_STAT/CSET_RF06_Tr2p3_96sqx432_100m_M2005PA_RRTM4PBL_UM5_ProgAer_vb_FTNA_150.nc",
        "./data/OUT_STAT/CSET_RF06_Tr2p3_256sqx432_100m_M2005PA_RRTM4PBL_UM5_ProgAer_MERRA2.nc",
        "./data/OUT_STAT/CSET_RF06_Tr2p3_96sqx432_100m_M2005PA_RRTM4PBL_UM5_ProgAer_MERRA2loglogMBL.nc",
        "./data/OUT_STAT/CSET_RF06_Tr2p3_96sqx432_100m_M2005PA_RRTM4PBL_UM5_ProgAer_MERRA2loglogMBL_3t.nc",
        "./data/OUT_STAT/CSET_RF10_Tr6p0_256sqx432_100m_RF10_M2005PA_RRTM4PBL_UM5_ProgAer_250_60.nc",
        "./data/OUT_STAT/CSET_RF10_Tr6p0_96x96x432_100m_M2005_RRTM4PBL_UM5_RF10_Tr6p0_va.nc",
        "./data/OUT_STAT/CSET_RF10_Tr6p0_256sqx432_100m_RF10_M2005PA_RRTM4PBL_UM5_ProgAer_70_60.nc",
        "./data/OUT_STAT/CSET_RF10_Tr6p0_96sqx432_100m_RF10_M2005PA_RRTM4PBL_UM5_ProgAer_70_60_NEW.nc",
        "./data/OUT_STAT/CSET_RF10_Tr6p0_96x96x432_100m_M2005_RRTM4PBL_UM5_RF10_Tr6p0_vc_BL_70.nc",
        "./data/OUT_STAT/CSET_RF10_Tr6p0_96x96x432_100m_M2005_RRTM4PBL_UM5_RF10_Tr6p0_vb_FTNA_200.nc",
        "./data/OUT_STAT/CSET_RF10_Tr6p0_96sqx432_100m_RF10_Tr6p0_M2005PA_RRTM4PBL_UM5_ProgAer_MERRA2loglogMBL.nc",
        "./data/OUT_STAT/CSET_RF10_Tr6p0_96sqx432_100m_Tr6p0_M2005PA_RRTM4PBL_UM5_MERRAlogBL_3t.nc",
    ],
    "fn3d": [
        "./data/OUT_2D/CSET_RF06_Tr2p3_256sqx432_100m_M2005PA_RRTM4PBL_UM5_ProgAer_40_40_128.2Dbin_1.nc",
        "./data/OUT_2D/CSET_RF06_Tr2p3_96sqx432_100m_M2005PA_RRTM4PBL_UM5_ProgAer_va_48.2Dbin_1.nc",
        "./data/OUT_2D/CSET_RF06_Tr2p3_96sqx432_100m_M2005PA_RRTM4PBL_UM5_ProgAer_BL40_FT40_150_96.2Dbin_1.nc",
        "./data/OUT_2D/CSET_RF06_Tr2p3_96sqx432_100m_M2005PA_RRTM4PBL_UM5_ProgAer_vc_BL_150_96.2Dbin_1.nc",
        "./data/OUT_2D/CSET_RF06_Tr2p3_96sqx432_100m_M2005PA_RRTM4PBL_UM5_ProgAer_vb_FTNA_150_96.2Dbin_1.nc",
        "./data/OUT_2D/CSET_RF06_Tr2p3_256sqx432_100m_M2005PA_RRTM4PBL_UM5_ProgAer_MERRA2_128.2Dbin_1.nc",
        "./data/OUT_2D/CSET_RF06_Tr2p3_96sqx432_100m_M2005PA_RRTM4PBL_UM5_ProgAer_MERRA2loglogMBL_96.2Dbin_1.nc",
        "./data/OUT_2D/CSET_RF06_Tr2p3_96sqx432_100m_M2005PA_RRTM4PBL_UM5_ProgAer_MERRA2loglogMBL_3t_96.2Dbin_1.nc",
        "./data/OUT_2D/CSET_RF10_Tr6p0_256sqx432_100m_RF10_M2005PA_RRTM4PBL_UM5_ProgAer_250_60_128.2Dbin_1.nc",
        "./data/OUT_2D/CSET_RF10_Tr6p0_96x96x432_100m_M2005_RRTM4PBL_UM5_RF10_Tr6p0_va_96.2Dbin_1.nc",
        "./data/OUT_2D/CSET_RF10_Tr6p0_256sqx432_100m_RF10_M2005PA_RRTM4PBL_UM5_ProgAer_70_60_128.2Dbin_1.nc",
        "./data/OUT_2D/CSET_RF10_Tr6p0_96sqx432_100m_RF10_M2005PA_RRTM4PBL_UM5_ProgAer_70_60_NEW_96.2Dbin_1.nc",
        "./data/OUT_2D/CSET_RF10_Tr6p0_96x96x432_100m_M2005_RRTM4PBL_UM5_RF10_Tr6p0_vc_BL_70_96.2Dbin_1.nc",
        "./data/OUT_2D/CSET_RF10_Tr6p0_96x96x432_100m_M2005_RRTM4PBL_UM5_RF10_Tr6p0_vb_FTNA_200_96.2Dbin_1.nc",
        "./data/OUT_2D/CSET_RF10_Tr6p0_96sqx432_100m_RF10_Tr6p0_M2005PA_RRTM4PBL_UM5_ProgAer_MERRA2loglogMBL_96.2Dbin_1.nc",
        "./data/OUT_2D/CSET_RF10_Tr6p0_96sqx432_100m_Tr6p0_M2005PA_RRTM4PBL_UM5_MERRAlogBL_3t_96.2Dbin_1.nc",
    ],
    "fn2d": [
        "./data/OUT_2D/CSET_RF06_Tr2p3_256sqx432_100m_M2005PA_RRTM4PBL_UM5_ProgAer_40_40_128.2Dbin_1.nc",
        "./data/OUT_2D/CSET_RF06_Tr2p3_96sqx432_100m_M2005PA_RRTM4PBL_UM5_ProgAer_va_48.2Dbin_1.nc",
        "./data/OUT_2D/CSET_RF06_Tr2p3_96sqx432_100m_M2005PA_RRTM4PBL_UM5_ProgAer_BL40_FT40_150_96.2Dbin_1.nc",
        "./data/OUT_2D/CSET_RF06_Tr2p3_96sqx432_100m_M2005PA_RRTM4PBL_UM5_ProgAer_vc_BL_150_96.2Dbin_1.nc",
        "./data/OUT_2D/CSET_RF06_Tr2p3_96sqx432_100m_M2005PA_RRTM4PBL_UM5_ProgAer_vb_FTNA_150_96.2Dbin_1.nc",
        "./data/OUT_2D/CSET_RF06_Tr2p3_256sqx432_100m_M2005PA_RRTM4PBL_UM5_ProgAer_MERRA2_128.2Dbin_1.nc",
        "./data/OUT_2D/CSET_RF06_Tr2p3_96sqx432_100m_M2005PA_RRTM4PBL_UM5_ProgAer_MERRA2loglogMBL_96.2Dbin_1.nc",
        "./data/OUT_2D/CSET_RF06_Tr2p3_96sqx432_100m_M2005PA_RRTM4PBL_UM5_ProgAer_MERRA2loglogMBL_3t_96.2Dbin_1.nc",
        "./data/OUT_2D/CSET_RF10_Tr6p0_256sqx432_100m_RF10_M2005PA_RRTM4PBL_UM5_ProgAer_250_60_128.2Dbin_1.nc",
        "./data/OUT_2D/CSET_RF10_Tr6p0_96x96x432_100m_M2005_RRTM4PBL_UM5_RF10_Tr6p0_va_96.2Dbin_1.nc",
        "./data/OUT_2D/CSET_RF10_Tr6p0_256sqx432_100m_RF10_M2005PA_RRTM4PBL_UM5_ProgAer_70_60_128.2Dbin_1.nc",
        "./data/OUT_2D/CSET_RF10_Tr6p0_96sqx432_100m_RF10_M2005PA_RRTM4PBL_UM5_ProgAer_70_60_NEW_96.2Dbin_1.nc",
        "./data/OUT_2D/CSET_RF10_Tr6p0_96x96x432_100m_M2005_RRTM4PBL_UM5_RF10_Tr6p0_vc_BL_70_96.2Dbin_1.nc",
        "./data/OUT_2D/CSET_RF10_Tr6p0_96x96x432_100m_M2005_RRTM4PBL_UM5_RF10_Tr6p0_vb_FTNA_200_96.2Dbin_1.nc",
        "./data/OUT_2D/CSET_RF10_Tr6p0_96sqx432_100m_RF10_Tr6p0_M2005PA_RRTM4PBL_UM5_ProgAer_MERRA2loglogMBL_96.2Dbin_1.nc",
        "./data/OUT_2D/CSET_RF10_Tr6p0_96sqx432_100m_Tr6p0_M2005PA_RRTM4PBL_UM5_MERRAlogBL_3t_96.2Dbin_1.nc",
    ],
}


def open_dataset(filelist):
    f = [Dataset(fn) for fn in filelist]
    return f


def add_combinations(
    filenames,
    j1,
    j2,
    a_ft,
    box,
    cre_scaling=False,
    factor=None,
    mode="erfani_2022",
    combinations=None,
):
    if combinations is None:
        combinations = {}

    def hash(obj):
        return hashlib.sha256(str(obj.__dict__).encode()).hexdigest()

    for i in range(len(j1)):
        fn1 = filenames[j1[i]]
        fn2 = filenames[j2[i]]
        res = get_dCRE(
            fn1, fn2, a_ft, box, cre_scaling=cre_scaling, factor=factor, mode=mode
        )
        combinations[j1[i], j2[i], a_ft, box, cre_scaling, factor, mode] = res
    return combinations


def get_dCRE(fn1, fn2, a_ft, box, cre_scaling=False, factor=1, mode="erfani_2022"):
    components = ed.quant_CRE_alltime(
        fn1, fn2, a_ft, box, cre_scaling=cre_scaling, factor=factor, mode=mode
    )
    return components


def calc_results(a_ft, box, scaling=False, mode="erfani_2022"):
    fn2 = open_dataset(datasets["fn2"])

    j1 = [0, 0, 0, 0, 8, 8, 8, 8]
    j2 = [5, 3, 4, 7, 9, 13, 14, 15]

    combinations = add_combinations(
        fn2, j1, j2, a_ft, box, cre_scaling=scaling, factor=1, mode=mode
    )
    combinations = add_combinations(
        fn2,
        j2,
        j1,
        a_ft,
        box,
        cre_scaling=scaling,
        factor=-1,
        mode=mode,
        combinations=combinations,
    )

    j1 = [6, 1, 1, 1, 14, 12, 12, 9]
    j2 = [7, 3, 4, 7, 15, 9, 15, 15]
    combinations = add_combinations(
        fn2,
        j1,
        j2,
        a_ft,
        box,
        cre_scaling=scaling,
        factor=1,
        mode=mode,
        combinations=combinations,
    )
    combinations = add_combinations(
        fn2,
        j2,
        j1,
        a_ft,
        box,
        cre_scaling=scaling,
        factor=-1,
        mode=mode,
        combinations=combinations,
    )

    df = pd.DataFrame.from_dict(combinations, orient="index")
    df.set_index(pd.MultiIndex.from_tuples(df.index), inplace=True)
    return df


def get_result(df, j1, j2, a_ft, box, cre_scaling, factor, mode):
    idx = (j1, j2, a_ft, box, cre_scaling, factor, mode)
    return tuple(df.loc[idx])


def select_res_subset(res, j1, j2, a_ft=None, box=None, cre_scaling=None):
    r_positive = res.loc[
        (slice(None), slice(None), slice(None), slice(None), slice(None), [1])
    ]
    r_negative = res.loc[
        (slice(None), slice(None), slice(None), slice(None), slice(None), [-1])
    ]
    r_negative = r_negative.swaplevel(0, 1)
    res_ = pd.concat([r_positive, r_negative])
    return res_.loc[
        res_.index.get_level_values(0).isin(j1) & res_.index.get_level_values(1).isin(j2)
    ]

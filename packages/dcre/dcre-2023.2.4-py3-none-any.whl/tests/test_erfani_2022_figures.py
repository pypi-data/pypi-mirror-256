#!/usr/bin/env python
# coding: utf-8
import argparse

import numpy as np  # linear algebra
import pandas as pd
from netCDF4 import Dataset

import dcre.erfani_2022.erfani_2022_results as er  # noqa: E402
import dcre.erfani_2022.figures as ef  # noqa: E402
import dcre.erfani_2022.helpers as h  # noqa: E402

lb = [
    "40-40-LD",
    "40-40",
    "40-40to150",
    "150-40",
    "40-150",
    "MERRA-LD",
    "MERRA",
    "MERRAX3",
    "250-60-LD",
    "250-60",
    "70-60-LD",
    "70-60",
    "110-60",
    "250-200",
    "MERRA",
    "MERRAX3",
]

ylim = 4000
box = 5

# Read sample file for time/mask information
sample_file = "./data/OUT_STAT/CSET_RF06_Tr2p3_256sqx432_100m_M2005PA_RRTM4PBL_UM5_ProgAer_40_40.nc"
(
    time,
    _,
    _,
    _,
    _,
    _,
    _,
    _,
    _,
    _,
    SWNS,
    P,
    _,
    _,
    _,
    _,
    _,
    _,
    _,
    _,
    _,
    _,
    _,
    _,
    _,
    _,
    _,
    _,
    _,
    _,
    _,
    _,
    _,
    _,
    _,
    _,
    _,
    _,
    _,
    _,
    _,
    _,
    _,
) = h.read_model_vars(Dataset(sample_file))

upbound = time.copy()
upbound[:] = ylim
upbound[SWNS > 0] = np.nan


def plot_figures(fn):
    """Wrapper function for plotting CRE decomposition figures following Erfani
    et al. (2022)

    Inputs
    ------
    fn : str
        filename of pickle file containing CRE decomposition
    """
    res = pd.read_pickle(fn)

    # Fig 13
    j1 = [0, 0, 0, 0, 8, 8, 8, 8]
    j2 = [5, 3, 4, 7, 9, 13, 14, 15]
    it = "2015-07-17 00Z"
    it2 = "2015-07-27 00Z"
    init_time_all = [it, it, it, it, it2, it2, it2, it2]

    res_sub = er.select_res_subset(res, j1, j2)

    fig13 = ef.fig13(res_sub, lb)
    fig13.savefig("tests/decomp_CRE_fig13.pdf", format="pdf", dpi=500)

    # Fig 14
    fig14 = ef.fig14(res_sub, lb)
    fig14.savefig("tests/decomp_ratio_fig14.pdf", format="pdf", dpi=500)

    # Fig timeseries

    j1 = [6, 1, 1, 1, 14, 12, 12, 9]
    j2 = [7, 3, 4, 7, 15, 9, 15, 15]

    res_sub = er.select_res_subset(res, j1, j2)
    fig = ef.cre_timeseries(res_sub, time, lb, upbound, init_time_all)
    fig.savefig("tests/decomp_CRE_timeseries.pdf", format="pdf", dpi=500)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Plot CRE decomposition figures following Erfani et al. (2022)."
    )
    parser.add_argument(
        "-i",
        "--input",
        metavar="i",
        type=str,
        help="input pickle file containing CRE components",
    )
    args = parser.parse_args()
    plot_figures(args.input)

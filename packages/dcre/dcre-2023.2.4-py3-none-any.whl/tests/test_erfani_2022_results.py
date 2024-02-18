#!/usr/bin/env python
# coding: utf-8
import os
import warnings

import numpy as np  # linear algebra
import pandas as pd
import pytest

import dcre.erfani_2022.erfani_2022_results as er  # noqa: E402

warnings.filterwarnings("ignore")

cre_scaling = False
fn_res_orig = f"cre_components_erfani_scaling{cre_scaling}.pkl"
fn_res_new = f"cre_components_decomposer_scaling{cre_scaling}.pkl"
abs_rel_error_tol = 0.2  # [%]


# Calculate and decompose CRE values
def get_decomposition(
    mode, cre_scaling=False, a_ft=0.05, box=5, reuse=False, cache=None
):
    if reuse:
        assert cache is not None, "Cache must be given when reuse=True"
        if os.path.exists(cache):
            res = pd.read_pickle(cache)
        else:
            print("Data could not be found in cache. Recomputing.")
            res = er.calc_results(a_ft=a_ft, box=box, scaling=cre_scaling, mode=mode)
            res.to_pickle(cache)
    else:
        res = er.calc_results(a_ft=a_ft, box=box, scaling=cre_scaling, mode=mode)
        if cache:
            res.to_pickle(cache)
    return res


@pytest.mark.parametrize("scaling", [False, True])
def test_decomposition_against_erfani_2022(scaling, **kwargs):
    res = {}
    for mode in ["erfani_2022", "decomposer"]:
        c = f"tests/cre_components_{mode}_scaling{scaling}.pkl"
        res[mode] = get_decomposition(mode, cre_scaling=scaling, cache=c, **kwargs)

    for g, grp in pd.concat([res["erfani_2022"], res["decomposer"]]).groupby(
        level=[0, 1, 2, 3, 4, 5]
    ):
        assert (
            len(grp) == 2
        ), f"For the index {g} only one of the datasets seem to have an entry."
        rel_diff = (grp.iloc[0] - grp.iloc[1]) / grp.iloc[0] * 100
        abs_rel_diff = np.abs(rel_diff)
        max_rel_diff = abs_rel_diff.apply(np.max)
        print(max_rel_diff)
        assert np.all(
            max_rel_diff < abs_rel_error_tol
        ), "Maximum relative error exceeds threshold."

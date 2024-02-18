"""Helper functions to create idealized test datasets for model testing."""

import numpy as np
import pytest
import xarray as xr
from numpy.testing import assert_almost_equal, assert_array_equal

import pycre.cre_decomposition as decomp

np.random.seed(0)


def set_simulation(ds):
    """Helper function to create a Simulation object."""
    sim = decomp.Simulation(
        ds.CWP.where(ds.cloud == 1).mean(dim=["lat", "lon"]),
        ds.cloud.mean(dim=["lat", "lon"]),
        ds.NCCN.where(ds.cloud == 1).mean(dim=["lat", "lon"]),
        ds.albedo.mean(dim=["lat", "lon"]),
        ds.albedo.where(ds.cloud == 0).mean(dim=["lat", "lon"]),
        ds.solin.mean(dim=["lat", "lon"]),
    )
    return sim


def decompose(ds1, ds2):
    """Helper function to decompose two datasets."""
    src1 = set_simulation(ds1)
    src2 = set_simulation(ds2)
    decompositer = decomp.CRE_Decompositer(src1, src2)
    decompositer.decompose(cre_scaling=False)
    return decompositer.to_dataset()


# @pytest.fixture
def create_no_change_dataset():
    """Create dataset with no change between control and perturbed run."""
    arr1 = np.random.choice([0, 1], (1, 100, 100))
    arr2 = np.ones((1, 100, 100))
    arr3 = arr2 * 0.4
    arr3[arr1 == 1] = 0.6

    ds = xr.Dataset(
        {
            "cloud": (["time", "lat", "lon"], arr1),
            "solin": (["time", "lat", "lon"], arr2.copy() * 500),
            "NCCN": (["time", "lat", "lon"], arr1.copy() * 100),
            "CWP": (["time", "lat", "lon"], arr1.copy() * 200),
            "albedo": (["time", "lat", "lon"], arr3),
        }
    )
    return ds, ds


def create_CF_increase_dataset():
    """Create dataset with increasing CF between control and perturbed run."""
    arr0 = np.random.choice([0, 1], (1, 100, 100), p=[0.99, 0.01])
    arr1 = np.random.choice([0, 1], (1, 100, 100), p=[0.01, 0.99])
    arr2 = np.ones((1, 100, 100))
    arr3 = arr2 * 0.0
    arr3[arr1 == 1] = 1
    arr4 = arr2 * 0.0
    arr4[arr0 == 1] = 1

    ds_ref = xr.Dataset(
        {
            "cloud": (["time", "lat", "lon"], arr0),
            "solin": (["time", "lat", "lon"], arr2.copy() * 500),
            "NCCN": (["time", "lat", "lon"], arr0.copy() * 100),
            "CWP": (["time", "lat", "lon"], arr0.copy() * 200),
            "albedo": (["time", "lat", "lon"], arr4),
        }
    )

    ds_pert = xr.Dataset(
        {
            "cloud": (["time", "lat", "lon"], arr1),
            "solin": (["time", "lat", "lon"], arr2.copy() * 500),
            "NCCN": (["time", "lat", "lon"], arr1.copy() * 100),
            "CWP": (["time", "lat", "lon"], arr1.copy() * 200),
            "albedo": (["time", "lat", "lon"], arr3),
        }
    )

    return ds_ref, ds_pert


def create_CF_decrease_dataset():
    """Create dataset with decreasing CF between control and perturbed run."""
    arr0 = np.random.choice([0, 1], (1, 100, 100), p=[0.99, 0.01])
    arr1 = np.random.choice([0, 1], (1, 100, 100), p=[0.01, 0.99])
    arr2 = np.ones((1, 100, 100))
    arr3 = arr2 * 0.0
    arr3[arr1 == 1] = 1
    arr4 = arr2 * 0.0
    arr4[arr0 == 1] = 1

    ds_ref = xr.Dataset(
        {
            "cloud": (["time", "lat", "lon"], arr0),
            "solin": (["time", "lat", "lon"], arr2.copy() * 500),
            "NCCN": (["time", "lat", "lon"], arr0.copy() * 100),
            "CWP": (["time", "lat", "lon"], arr0.copy() * 200),
            "albedo": (["time", "lat", "lon"], arr4),
        }
    )

    ds_pert = xr.Dataset(
        {
            "cloud": (["time", "lat", "lon"], arr1),
            "solin": (["time", "lat", "lon"], arr2.copy() * 500),
            "NCCN": (["time", "lat", "lon"], arr1.copy() * 100),
            "CWP": (["time", "lat", "lon"], arr1.copy() * 200),
            "albedo": (["time", "lat", "lon"], arr3),
        }
    )

    return ds_ref, ds_pert


def create_CWP_increase_dataset():
    """Create dataset with increasing CWP between control and perturbed run."""
    arr1 = np.random.choice([0, 1], (1, 100, 100), p=[0.1, 0.9])
    arr2 = np.ones((1, 100, 100))
    arr3 = arr2 * 0.4
    arr3[arr1 == 1] = 0.6
    arr4 = arr2 * 0.4
    arr4[arr1 == 1] = 0.6304
    # albedo needs to be adjusted to reflect the change in CWP

    ds_ref = xr.Dataset(
        {
            "cloud": (["time", "lat", "lon"], arr1),
            "solin": (["time", "lat", "lon"], arr2.copy() * 500),
            "NCCN": (["time", "lat", "lon"], arr1.copy() * 100),
            "CWP": (["time", "lat", "lon"], arr1.copy() * 200),
            "albedo": (["time", "lat", "lon"], arr3),
        }
    )

    ds_pert = xr.Dataset(
        {
            "cloud": (["time", "lat", "lon"], arr1),
            "solin": (["time", "lat", "lon"], arr2.copy() * 500),
            "NCCN": (["time", "lat", "lon"], arr1.copy() * 100),
            "CWP": (["time", "lat", "lon"], arr1.copy() * 300),
            "albedo": (["time", "lat", "lon"], arr4),
        }
    )

    return ds_ref, ds_pert


@pytest.mark.parametrize("dss", [create_no_change_dataset()])
def test_no_change(dss):
    """Test decomposition in case reference and pertrubed runs are the same."""
    ds = decompose(*dss)
    for var in [
        "dCRE_total",
        "dCRE_clear",
        "dCRE_clear_anom",
        "dCRE_cloud_anom",
        "dCRE_CF",
        "dCRE_cloud",
        "dCRE_CDNC",
        "dCRE_LWP",
        "dCRE_rs",
    ]:
        assert_array_equal(ds[var].values, 0)
    for var in [
        "dA_total",
        "dA_cloud",
        "dA_clear",
        "dA_CF",
        "dA_CDNC",
        "dA_LWP",
        "dA_rs",
    ]:
        assert_array_equal(ds[var].values, 0)
    assert_almost_equal(ds["A_cloud_sim1"].values, 0.6)
    assert_almost_equal(ds["A_cloud_sim2"].values, 0.6)

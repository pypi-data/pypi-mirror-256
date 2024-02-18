# dCRE
Computation and decomposition of Cloud Radiative Effects (CRE)

![ci.yaml](https://github.com/observingClouds/dCRE/actions/workflows/ci.yaml/badge.svg)

> [!WARNING]
> This package is still under development. Things will break.

## Installation
```
pip install dcre
```

## Usage
```python
import dcre

# Add reference and perturbed sources
src1 = dcre.cre_decomposition.Simulation(CWP, CF, NCCN, albedo, albd_clear,SOLIN)
src2 = dcre.cre_decomposition.Simulation(CWP, CF, NCCN, albedo, albd_clear,SOLIN)

# Configure decomposition
decompositer = dcre.cre_decomposition.CRE_Decompositer(src1, src2)

# Decompose
decompositer.decompose(cre_scaling=False)

# Write results to disk
ds = decompositer.to_dataset()
ds.to_netcdf("decomposition.nc")
```

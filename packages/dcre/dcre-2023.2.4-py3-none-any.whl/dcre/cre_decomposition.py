import xarray as xr


class Simulation:
    def __init__(
        self, CWP, CF, NCCN, albedo, albd_clear, SOLIN, sw_dwn_profile=None, inv_idx=None
    ):
        self.quantities = self.Quantities(
            CWP, CF, NCCN, albedo, albd_clear, SOLIN, sw_dwn_profile, inv_idx
        )
        self.calc = self.Calculations(self.quantities)

    class Calculations:
        def __init__(self, quantities):
            self.q = quantities

        def toa_cloud_albedo(self):
            """Cloud albedo calculation.

            Calculate cloud albedo as defined at the top of the atmosphere.

            References
            ----------
            Chun et al. (2023) (Eq. B2)
            """
            self.q.toa_cloud_albedo = (
                self.q.albedo - (1 - self.q.CF) * self.q.albd_clear
            ) / self.q.CF

        def free_trop_transmissivity(self, T=None):
            """Set free-tropospheric transmissivity.

            If self.quantities.inv_idx is set, the free-tropospheric transmissivity
            is calculated based on the net radiative flux above the inversion
            layer given by `inv_idx`. Otherwise, the free-tropospheric transmissivity
            is set to 0.8 or the value given by `T`.

            Inputs
            ------
            T : float (optional)
                free-tropospheric transmissivity
            """
            if self.q.inv_idx is not None and T is None:
                self.q.ft_transmissivity = self.q.sw_dwn_profile / self.q.SOLIN
            elif T is not None:
                self.q.ft_transmissivity = T
            else:
                self.q.ft_transmissivity = 0.8

        def scene_albedo(self, a_ft=0.05):
            """Cloud top albedo (without free troposphere contrib.).

            Formula follows Eq. B7 in Chun et al. (2023) which originates
            from Qu and Hall (2005) and Donohoe and Battisti (2011).

            Inputs
            ------
            a_ft : float
                albedo of free troposphere
            """
            if self.q.ft_transmissivity is None:
                self.free_trop_transmissivity()
            T_ft = self.q.ft_transmissivity
            self.q.scene_albedo = (self.q.toa_cloud_albedo - a_ft) / (
                T_ft**2 + self.q.toa_cloud_albedo * a_ft - a_ft**2
            )

        def cre(self, level="cloud_layer", a_ft=0.05):
            """Calculation of cloud radiative effect (CRE)

            Inputs
            ------
            level : str
                cloud_layer: remove free-tropospheric effect with simple approx.
                toa: cloud radiative effect measured at top-of-atmosphere
            a_ft : float
                albedo of free troposphere
            """
            if level == "cloud_layer":
                if self.q.scene_albedo is None:
                    self.scene_albedo(a_ft=a_ft)
                cre = -self.q.scene_albedo * self.q.SOLIN * self.q.CF
            elif level == "toa":
                cre = (
                    -1
                    * (self.q.toa_cloud_albedo - self.q.albd_clear)
                    * self.q.SOLIN
                    * (self.q.CF)
                )
            return cre

    class Quantities:
        def __init__(
            self, CWP, CF, NCCN, albedo, albd_clear, SOLIN, sw_dwn_profile, inv_idx
        ):
            self.CWP = CWP
            self.CF = CF
            self.albedo = albedo
            self.albd_clear = albd_clear
            self.NCCN = NCCN
            self.SOLIN = SOLIN
            self.sw_dwn_profile = sw_dwn_profile
            self.inv_idx = inv_idx
            self.toa_cloud_albedo = None
            self.ft_transmissivity = None
            self.scene_albedo = None
            self.cre = None


class CRE_Decompositer:
    def __init__(self, simulation1, simulation2):
        self.simulation1 = simulation1
        self.simulation2 = simulation2
        self.cre_scalar = 1
        self.cloud_cre_change = None
        self.CRE_change_at_TOA = None

    def cre_change(self, factor, cre_scaling=False):
        """Change in cloud-radiative effect between two datasets.

        Inputs
        ------
        factor : int
            Factor
        cre_scaling : bool
            Switch to scale cloud-radiative effect by TOA CRE of reference
            dataset.
        """
        if self.simulation1.quantities.cre is None:
            self.simulation1.quantities.cre = self.simulation1.calc.cre()
        if self.simulation2.quantities.cre is None:
            self.simulation2.quantities.cre = self.simulation2.calc.cre()
        if cre_scaling:
            cre_direct = self.simulation1.calc.cre(level="toa")
            scale = cre_direct / self.simulation1.quantities.cre
            self.cre_scalar = scale
            self.simulation1.quantities.cre *= scale
            self.simulation2.quantities.cre *= scale
        self.CRE_change = factor * (
            self.simulation2.quantities.cre - self.simulation1.quantities.cre
        )

    def cld_albedo_change(self):
        self.cld_alb_change = (
            self.simulation2.quantities.toa_cloud_albedo
            - self.simulation1.quantities.toa_cloud_albedo
        )

    def clearsky_albedo_change(self):
        self.clrsky_alb_change = (
            self.simulation2.quantities.albd_clear
            - self.simulation1.quantities.albd_clear
        )

    def cre_cloud_change(self, factor=-1):
        """CRE change due to changes in cloud properties.

        This is a more direct way to calculate the CRE change due to
        changes in cloud properties and should match the sum of CRE
        changes due to LWP adjustment and twomey effect under the
        assumption that the free-tropospheric albedo and transmissivity
        is the same.
        """
        s1 = self.simulation1.quantities
        s2 = self.simulation2.quantities
        if self.cloud_cre_change is None:
            self.cld_albedo_change()
        self.cloud_cre_change = (
            factor * self.cld_alb_change * s2.SOLIN * s1.CF * self.cre_scalar
        )

    def cre_clearsky_change(self, factor=-1):
        """CRE change due to changes in the clear-sky albedo."""
        s1 = self.simulation1.quantities
        s2 = self.simulation2.quantities

        dA_clr = self.clrsky_alb_change
        dA_cld = self.cld_alb_change
        dfc = s2.CF - s1.CF

        dCRE_clear_sky = (
            factor * self.clrsky_alb_change * s2.SOLIN * (1 - s1.CF) * self.cre_scalar
        )

        dCRE_clear_sky_anom = -1 * factor * dA_clr * dfc * s2.SOLIN * self.cre_scalar
        dCRE_cloudy_anom = factor * dA_cld * dfc * s2.SOLIN * self.cre_scalar

        self.clrsky_cre_change = dCRE_clear_sky
        self.clrsky_anom_cre_change = dCRE_clear_sky_anom
        self.cloud_anom_cre_change = dCRE_cloudy_anom

    def _integral(self, factor, albedo, r, sign=-1):
        r"""Integral of cloud albedo change with LWP/NCCN to retrieve albedo
        perturbation.

        .. math::
            a = \alpha \pm \alpa \cdot (1 - \alpha) * (r^{factor} -1) / (1 + \alpha * r^{factor}-1)

        Inputs
        ------
        factor : float
            factor in equation, LWP: 5/6; Twomey: 1/3
        albedo : float
            all-sky scene albedo
        r : float
            ratio of perturbed and control quantity, like LWP
        sign : int
            factor

        Returns
        -------
        albedo : float
            cloud albedo perturbed by quantity change (defined at cloud top)
        """
        a = albedo + sign * albedo * (1 - albedo) * (r ** (factor) - 1) / (
            1 + albedo * (r**factor - 1)
        )
        return a

    def _single_layer_model(self, Acld, alb, T):
        """Single layer atmosphere radiation model.

        Calculate top-of-atmosphere albedo (sometimes called overvast albedo)
        by using cloud albedo and include the effect of the free troposphere.

        This is a rearranged version of the function `scene_albedo`.

        Inputs
        ------
        Acld : float
            cloud albedo (defined at cloud top)
        alb : float
            free-tropospheric albedo
        T : float
            free-tropospheric transmissivity

        Returns
        -------
        toa_albedo : float
            top-of-atmosphere cloud albedo

        References
        ----------
        Chun et al. (2023) (Eq. B8)
        Diamond et al. (2019) (Eq. 4)
        """
        toa_albedo = alb + (Acld * T**2) / (1 - alb * Acld)
        return toa_albedo

    def twomey_effect(self, factor=-1, a_ft=0.05):
        """Twomey-effect on cloud albedo, scene albedo and CRE.

        Wrapper function to calculate cloud albedo, TOA cloud albedo
        and cloud radiative effect change due to the Twomey effect.

        Inputs
        ------
        factor : int
            factor
        a_ft : float
            albedo of free troposphere
        """
        s1 = self.simulation1.quantities
        s2 = self.simulation2.quantities
        rN = s2.NCCN / s1.NCCN  # .max(dim='height') / s1.NCCN.max(dim='height')
        self.twomey_rN = rN

        self.twomey_cld_albedo_change = self._integral(
            factor=1 / 3, albedo=s1.scene_albedo, r=rN, sign=factor
        )
        self.twomey_scene_albedo_change = (
            self._single_layer_model(
                alb=a_ft, Acld=self.twomey_cld_albedo_change, T=s1.ft_transmissivity
            )
            - s1.toa_cloud_albedo
        )
        self.twomey_cre_change = (
            -self.twomey_scene_albedo_change * s2.SOLIN * s1.CF * self.cre_scalar
        )

    def LWP_adjustment(self, factor=-1, a_ft=0.05):
        """LWP adjustment effect on cloud albedo, scene albedo and CRE.

        Wrapper function to calculate cloud albedo, TOA cloud albedo
        and cloud radiative effect change due to the liquid water path adjustment.

        Inputs
        ------
        factor : int
            factor
        a_ft : float
            albedo of free troposphere
        """
        s1 = self.simulation1.quantities
        s2 = self.simulation2.quantities
        rL = s2.CWP / s1.CWP
        self.LWP_rL = rL
        self.LWP_cld_albedo_change = self._integral(
            factor=5 / 6, albedo=s1.scene_albedo, r=rL, sign=factor
        )
        self.LWP_scene_albedo_change = (
            self._single_layer_model(
                alb=a_ft, Acld=self.LWP_cld_albedo_change, T=s1.ft_transmissivity
            )
            - s1.toa_cloud_albedo
        )
        self.LWP_cre_change = (
            -self.LWP_scene_albedo_change * s2.SOLIN * s1.CF * self.cre_scalar
        )

    def CF_adjustment(self, factor=-1):
        """Cloud fraction adjustment effect on cloud albedo, scene albedo and
        CRE."""
        s1 = self.simulation1.quantities
        s2 = self.simulation2.quantities
        A_CF = self.twomey_scene_albedo_change.copy()
        for i in range(len(s1.CF)):
            if (
                s2.CF[i] > s1.CF[i]
            ):  # adding clouds with properties of simulation with higher CF (simulation 2)
                A_CF[i] = (s2.CF[i] - s1.CF[i]) * (
                    s2.toa_cloud_albedo[i] - s2.albd_clear[i]
                )
            else:
                # removing clouds with properties of simulations with higher CF (simulation 1)
                A_CF[i] = (s2.CF[i] - s1.CF[i]) * (
                    s1.toa_cloud_albedo[i] - s1.albd_clear[i]
                )

        self.CF_albedo_change = A_CF.copy()
        self.CF_cre_change = factor * A_CF * s2.SOLIN * -1 * self.cre_scalar

    def decompose(self, factor=-1, a_ft=0.05, cre_scaling=False):
        self.simulation1.calc.toa_cloud_albedo()
        self.simulation2.calc.toa_cloud_albedo()
        self.simulation1.calc.scene_albedo()
        self.simulation2.calc.scene_albedo()
        self.simulation1.quantities.cre = self.simulation1.calc.cre()
        self.simulation2.quantities.cre = self.simulation2.calc.cre()
        self.cre_change(factor=factor, cre_scaling=cre_scaling)
        self.cld_albedo_change()
        self.cre_cloud_change(factor=factor)
        self.twomey_effect(factor=factor, a_ft=a_ft)
        self.LWP_adjustment(factor=factor, a_ft=a_ft)
        self.CF_adjustment(factor=factor)
        self.clearsky_albedo_change()
        self.alb_change = (
            self.simulation2.quantities.albedo - self.simulation1.quantities.albedo
        )
        self.cre_clearsky_change(factor=factor)

        self.CRE_change_at_TOA = self.simulation1.calc.cre(
            level="toa"
        ) - self.simulation2.calc.cre(level="toa")

        self.A_rs = (
            self.twomey_scene_albedo_change
            + self.LWP_scene_albedo_change
            + self.CF_albedo_change
            - self.cld_alb_change
        )
        self.CRE_rs = (
            self.twomey_cre_change
            + self.LWP_cre_change
            + self.CF_cre_change
            - self.CRE_change_at_TOA
        )

        self.rC = self.simulation2.quantities.CF / self.simulation1.quantities.CF

    def to_dataset(self):
        """Return decomposition as dataset."""
        ds_cre = xr.Dataset(
            {
                "dCRE_total": self.CRE_change_at_TOA,
                "dCRE_total_cloudlayer": self.CRE_change,
                "dCRE_clear": self.clrsky_cre_change,
                "dCRE_clear_anom": self.clrsky_anom_cre_change,
                "dCRE_cloud_anom": self.cloud_anom_cre_change,
                "dCRE_CF": self.CF_cre_change,
                "dCRE_cloud": self.cloud_cre_change,
                "dCRE_CDNC": self.twomey_cre_change,
                "dCRE_LWP": self.LWP_cre_change,
                "dCRE_rs": self.CRE_rs,
            }
        )
        ds_alb = xr.Dataset(
            {
                "dA_total": self.alb_change,
                "dA_cloud": self.cld_alb_change,
                "dA_clear": self.clrsky_alb_change,
                "dA_CF": self.CF_albedo_change,
                "dA_CDNC": self.twomey_scene_albedo_change,
                "dA_LWP": self.LWP_scene_albedo_change,
                "dA_rs": self.A_rs,
            }
        )
        ds_props = xr.Dataset(
            {
                "NCCN": xr.DataArray(
                    [self.simulation1.quantities.NCCN, self.simulation2.quantities.NCCN],
                    dims=["simulation", "time"],
                    coords={"time": self.simulation1.quantities.NCCN.time},
                ),
                "CWP": xr.DataArray(
                    [self.simulation1.quantities.CWP, self.simulation2.quantities.CWP],
                    dims=["simulation", "time"],
                    coords={"time": self.simulation1.quantities.CWP.time},
                ),
                "CF": xr.DataArray(
                    [self.simulation1.quantities.CF, self.simulation2.quantities.CF],
                    dims=["simulation", "time"],
                    coords={"time": self.simulation1.quantities.CF.time},
                ),
                "albedo": xr.DataArray(
                    [
                        self.simulation1.quantities.albedo,
                        self.simulation2.quantities.albedo,
                    ],
                    dims=["simulation", "time"],
                    coords={"time": self.simulation1.quantities.albedo.time},
                ),
                "albd_clear": xr.DataArray(
                    [
                        self.simulation1.quantities.albd_clear,
                        self.simulation2.quantities.albd_clear,
                    ],
                    dims=["simulation", "time"],
                    coords={"time": self.simulation1.quantities.albd_clear.time},
                ),
                "SOLIN": xr.DataArray(
                    [
                        self.simulation1.quantities.SOLIN,
                        self.simulation2.quantities.SOLIN,
                    ],
                    dims=["simulation", "time"],
                    coords={"time": self.simulation1.quantities.SOLIN.time},
                ),
            }
        )
        ds_sim1 = xr.Dataset(
            {"A_cloud_sim1": self.simulation1.quantities.toa_cloud_albedo}
        )
        ds_sim2 = xr.Dataset(
            {"A_cloud_sim2": self.simulation2.quantities.toa_cloud_albedo}
        )
        ds = xr.merge([ds_cre, ds_alb, ds_sim1, ds_sim2, ds_props])
        return ds

    def return_erfani_2022(self, otype="tuple"):
        """Return Erfani et al. (2022) compatible output.

        Function to return CRE decomposition results in the format that is
        compatible with the scripts used in Erfani et al. (2022). The functions'
        return matches that of `quant_CRE_alltime`.

        Inputs
        ------
        otype : str
            Return type of function (tuple, dict). Default is tuple.

        Returns
        -------
        Tuple or dictionary containing a variety of CRE decomposition factors:
            - fraction of CCN change
            - fraction of cloud water path change
            - fraction of cloud fraction change
            - total cloud-radiative effect change
            - Twomey-effect contribution to CRE change
            - Liquid-water-path adjustment contribution to CRE change
            - CRE change residual that cannot be explained by the Twomey-effect
              and the LWP adjustment
            - Cloud albedo of simulation 1
            - All-sky albedo change caused by Twomey-effect
            - All-sky albedo change caused by LWP adjustment
            - All-sly albedo change caused by CF change
            - All-sky albedo change residual that cannot be explained by the
              combination of the Twomey-effect, the LWP adjustment and the change
              in CF
            - CRE of simulation 1
            - CRE of simulation 2
            - CF of simulation 1
        """
        if otype == "tuple":
            return (
                self.twomey_rN,
                self.LWP_rL,
                self.rC,
                self.CRE_change,
                self.twomey_cre_change,
                self.LWP_cre_change,
                self.CF_cre_change,
                self.CRE_rs,
                self.simulation1.quantities.toa_cloud_albedo,
                self.twomey_scene_albedo_change,
                self.LWP_scene_albedo_change,
                self.CF_albedo_change,
                self.A_rs,
                self.simulation1.quantities.cre,
                self.simulation2.quantities.cre,
                self.simulation1.quantities.CF,
            )
        elif otype == "dict":
            return {
                "rN": self.twomey_rN,
                "rL": self.LWP_rL,
                "rC": self.rC,
                "CRE_M": self.CRE_change,
                "CRE_T": self.twomey_cre_change,
                "CRE_L": self.LWP_cre_change,
                "CRE_CF": self.CF_cre_change,
                "CRE_rs": self.CRE_rs,
                "A1": self.simulation1.quantities.toa_cloud_albedo,
                "A_T": self.twomey_scene_albedo_change,
                "A_L": self.LWP_scene_albedo_change,
                "A_CF": self.CF_albedo_change,
                "A_rs": self.A_rs,
                "CRE1": self.simulation1.quantities.cre,
                "CRE2": self.simulation2.quantities.cre,
                "CF1": self.simulation1.quantities.CF,
            }

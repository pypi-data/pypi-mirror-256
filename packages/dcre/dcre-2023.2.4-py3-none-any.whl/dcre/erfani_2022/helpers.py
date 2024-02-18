import numpy as np


def read_model_vars(file):  # noqa: C901
    def height_Ave(var):
        integ_var = np.arange(var[:, 0].size).astype(float)
        integ_var[:] = np.nan
        for i in range(var[:, 0].size):
            integ_var[i] = np.nansum(
                dz[: inv_idx[i] + 5]
                * RHO[i, : inv_idx[i] + 5]
                * var[i, : inv_idx[i] + 5]
            ) / np.nansum(dz[: inv_idx[i] + 5] * RHO[i, : inv_idx[i] + 5])
        return integ_var

    ## model variables:
    TIME = file.variables["time"][:]
    # lat_mg, lon_mg = np.meshgrid(lat, lon) # making meshgrid
    # 1-D variables
    z = file.variables["z"][:]
    SST = (
        file.variables["SST"][:] - 273.15
    )  # sea surface temperature converted from kelvin to celcius unit
    SSTOBS = file.variables["SSTOBS"][:] - 273.15
    PREC = file.variables["PREC"][:]  # Surface Precipitation"  "mm/day"
    LHF = file.variables["LHF"][:]
    LHFOBS = file.variables["LHFOBS"][:]
    SHF = file.variables["SHF"][:]
    SHFOBS = file.variables["SHFOBS"][:]
    Ps = file.variables["Ps"][:]
    LWNS = file.variables["LWNS"][:]
    SWNS = file.variables["SWNS"][:]
    RWP = file.variables["RWP"][:]  # Rain Water Path: g/m2
    CWP = file.variables["CWP"][:]  # Cloud Water Path
    LWP = file.variables["LWP"][:]  # GCSS Liquid Water Path
    MODISLWP = file.variables["MODISLWP"][:]
    CLDLOW = file.variables["CLDLOW"][:]
    # SAM's CLDLOW variable uses a threshold for cloud fraction that is based on LWP (20 g/m2, when CEM=.true., as in these runs)
    # which may not be consistent with an optical-depth-based threshold, as would be used in a satellite product.
    CLDMID = file.variables["CLDMID"][:]
    CLDHI = file.variables["CLDHI"][:]
    MODISREL = file.variables["MODISREL"][:]  # MODIS Effective Radius (Liquid): mkm
    ISCCPLOW = file.variables["ISCCPLOW"][:]
    # The ISCCP simulator approximates the cloud fraction that would be observed by a satellite using an optical depth threshold
    # of 0.3. The model domain includes only the lower troposphere, so that the relevant ISCCPTOT and ISCCPLOW should be identical.
    ISCCPTOT = file.variables["ISCCPTOT"][:]  #
    ZINV_org = file.variables["ZINV"][:]  # inversion height (km)
    WMAX = file.variables["WMAX"][:]  # max updraft vel. (m/s)
    LWNTOA = file.variables["LWNTOA"][:]  # Net LW flux at TOA (w/m2)
    SWNTOA = file.variables["SWNTOA"][:]  # Net SW flux at TOA (w/m2)
    SOLIN = file.variables["SOLIN"][:]  # Incoming SW flux at TOA (w/m2)
    ISCCPALB = file.variables["ISCCPALB"][:]  # ISCCP Cloud Albedo
    SWNTOAC = file.variables["SWNTOAC"][:]  # Net SW flux at TOA (Clear Sky)
    LWNTOAC = file.variables["LWNTOAC"][:]  # Net LW flux at TOA (Clear Sky)
    MODISTAU = file.variables["MODISTAU"][:]  # MODIS Cloud Optical Path
    ISCCPTAU = file.variables["ISCCPTAU"][:]  # ISCCP Optical Path
    TAUQCacc = file.variables["TAUQC"][:]  # Approx optical depth of cloud liquid water
    TAUQRacc = file.variables["TAUQR"][:]  # Approx optical depth of RAIN
    QCOEFFR = file.variables["QCOEFFR"][
        :
    ]  # Mixing ratio of QC over effective radius, EFFR = QC/QCOEFFR: g/kg/micro

    time = TIME - int(TIME[0])
    SOLIN2 = SOLIN.copy()
    SOLIN2[SOLIN2 <= 100] = np.nan
    albedo = (SOLIN2 - SWNTOA) / SOLIN2
    albd_clear = (SOLIN2 - SWNTOAC) / SOLIN2
    SW_CRE = SWNTOA - SWNTOAC

    # 2-D variables:
    NAd = file.variables["NAd"][:]  # dry aerosol number concentration (#/mg)
    NC = file.variables["NCCLD"][:]  # cloud number concentration in cloud
    NCORIG = file.variables["NC"][:]  # cloud number concentration
    NR = file.variables["NRCLD"][:]  # RAIN NUMBER CONCENTRATION in cloud
    NRORIG = file.variables["NR"][:]  # RAIN NUMBER CONCENTRATION
    RHO = file.variables["RHO"][:]  # kg/m3
    CLD = file.variables["CLD"][:]  # cloud Fraction
    #    CLDCUMDN=file.variables['CLDCUMD1'][:] # Cumulative Shaded Cloud Fraction, Computed Downwards
    RWC = file.variables["QPCLD"][:]  # rain water and snow content: g/kg
    CWC = file.variables["QNCLD"][:]  # cloud water and cloud ice content in cloud: g/kg
    QCCLD = file.variables["QCCLD"][:]  # Cloud liquid water mixing ratio in cloud
    QCOND = file.variables["QCOND"][:]  # Total Condensate: g/kg
    WOBS = file.variables["WOBS"][:]  # large scale W: m/s
    TABS = file.variables["TABS"][:]  # Absolute temperature: K
    QT = file.variables["QT"][:]  # Total water (no rain/snow included): g/kg
    QV = file.variables["QV"][:]  # Water vapor: g/kg
    RH = file.variables["RELH"][:]  # RH: %
    THETA = file.variables["THETA"][:]  # THETA: K
    U = file.variables["U"][:]  # x wind component: m/s
    V = file.variables["V"][:]  # y wind component: m/s
    P = file.variables["p"][:]  # pressure
    PRECIP = file.variables["PRECIP"][:]  # precipitation flux: mm/day
    W2 = file.variables["W2"][:]  # Variance of the z wind component: m2/s2
    THETAL = file.variables["THETAL"][:]  # Liquid water potential temperature: K

    QAd = file.variables["QAd"][:]  # DRY AEROSOL MASS: g/kg
    QAw = file.variables["QAw"][:]  # WET AEROSOL MASS
    QCORIG = file.variables["QC"][:]  # Cloud liquid water mass mixing ratio: g/kg
    QRORIG = file.variables["QR"][:]  # RAIN
    QAr = file.variables["QAr"][:]  # RAIN AEROSOL MASS

    # Aerosol budget terms:
    # NAd:
    # NC:
    NCSTRG = file.variables["NCSTRG"][
        :
    ]  # Storage of Cloud Water NUMBER CONCENTRATION: #/mg/day
    NCADV = file.variables["NCADV"][
        :
    ]  # Tendency of Cloud Water NUMBER CONCENTRATION due to resolved vertical advection: #/mg/day
    NCDIFF = file.variables["NCDIFF"][
        :
    ]  # Tendency of Cloud Water NUMBER CONCENTRATION due to vertical SGS transport: #/mg/day
    NCLSADV = file.variables["NCLSADV"][
        :
    ]  # Tendency of Cloud Water NUMBER CONCENTRATION due to large-scale vertical advecti: #/mg/day
    NCSED = file.variables["NCSED"][
        :
    ]  # Tendency of Cloud Water NUMBER CONCENTRATION due to sedimentation: #/mg/day
    NCMPHY = file.variables["NCMPHY"][
        :
    ]  # Tendency of CLOUD WATER NUMBER CONCENTRATION due to microphysical processes: #/mg/day
    NCFLXS = file.variables["NCFLXS"][
        :
    ]  # Subgrid flux of CLOUD WATER NUMBER CONCENTRATION: #/mg/day
    # NAd:
    try:
        NAdSTRG = (
            file.variables["NAcSTRG"][:] - NCSTRG
        )  # Storage of DRY AEROSOL NUMBER CONCENTRATION: #/mg/day
        NAdADV = (
            file.variables["NAcADV"][:] - NCADV
        )  # Tendency of DRY AEROSOL NUMBER CONCENTRATION due to resolved vertical advection: #/mg/day
        NAdDIFF = (
            file.variables["NAcDIFF"][:] - NCDIFF
        )  # Tendency of DRY AEROSOL NUMBER CONCENTRATION due to vertical SGS transport: #/mg/day
        NAdLSADV = (
            file.variables["NAcLSADV"][:] - NCLSADV
        )  # Tendency of DRY AEROSOL NUMBER CONCENTRATION due to large-scale vertical advecti: #/mg/day
        NAdSED = (
            file.variables["NAcSED"][:] - NCSED
        )  # Tendency of DRY AEROSOL NUMBER CONCENTRATION due to sedimentation: #/mg/day
        NAdMPHY = (
            file.variables["NAcMPHY"][:] - NCMPHY
        )  # Tendency of DRY AEROSOL NUMBER CONCENTRATION due to microphysical processes: #/mg/day
        NAdFLXS = (
            file.variables["NAcFLXS"][:] - NCFLXS
        )  # Subgrid flux of DRY AEROSOL NUMBER CONCENTRATION: #/m2/s
    except BaseException:
        NAdSTRG = file.variables["NAdSTRG"][
            :
        ]  # Storage of DRY AEROSOL NUMBER CONCENTRATION: #/mg/day
        NAdADV = file.variables["NAdADV"][
            :
        ]  # Tendency of DRY AEROSOL NUMBER CONCENTRATION due to resolved vertical advection: #/mg/day
        NAdDIFF = file.variables["NAdDIFF"][
            :
        ]  # Tendency of DRY AEROSOL NUMBER CONCENTRATION due to vertical SGS transport: #/mg/day
        NAdLSADV = file.variables["NAdLSADV"][
            :
        ]  # Tendency of DRY AEROSOL NUMBER CONCENTRATION due to large-scale vertical advecti: #/mg/day
        NAdSED = file.variables["NAdSED"][
            :
        ]  # Tendency of DRY AEROSOL NUMBER CONCENTRATION due to sedimentation: #/mg/day
        NAdMPHY = file.variables["NAdMPHY"][
            :
        ]  # Tendency of DRY AEROSOL NUMBER CONCENTRATION due to microphysical processes: #/mg/day
        NAdFLXS = file.variables["NAdFLXS"][
            :
        ]  # Subgrid flux of DRY AEROSOL NUMBER CONCENTRATION: #/m2/s
    SCVTNADC = file.variables["SCVTNADC"][
        :
    ]  # Tendency of NAD due to interstitial scavenging by cloud: #/mg/day
    SCVTNADR = file.variables["SCVTNADR"][
        :
    ]  # Tendency of NAD due to interstitial scavenging by rain: #/mg/day
    # NR:
    NRSTRG = file.variables["NRSTRG"][
        :
    ]  # Storage of Rain NUMBER CONCENTRATION: #/mg/day
    NRADV = file.variables["NRADV"][
        :
    ]  # Tendency of Rain NUMBER CONCENTRATION due to resolved vertical advection: #/mg/day
    NRDIFF = file.variables["NRDIFF"][
        :
    ]  # Tendency of Rain NUMBER CONCENTRATION due to vertical SGS transport: #/mg/day
    NRLSADV = file.variables["NRLSADV"][
        :
    ]  # Tendency of Rain NUMBER CONCENTRATION due to large-scale vertical advecti: #/mg/day
    NRSED = file.variables["NRSED"][
        :
    ]  # Tendency of Rain NUMBER CONCENTRATION due to sedimentation: #/mg/day
    NRMPHY = file.variables["NRMPHY"][
        :
    ]  # Tendency of Rain NUMBER CONCENTRATION due to microphysical processes: #/mg/day
    NCSTEN = file.variables["NCSTEN"][
        :
    ]  # CHANGE IN CLOUD DROPLET NUMBER DUE TO SEDIMENTATION: #/mg/day
    NRSTEN = file.variables["NRSTEN"][
        :
    ]  # CHANGE IN RAIN NUMBER DUE TO SEDIMENTATION: #/mg/day
    NPRA_pos = file.variables["NPRA"][
        :
    ]  # CHANGE IN RAIN NUMBER DUE TO ACCRETION OF CLOUD DROPLETS: #/mg/day
    NPRC = file.variables["NPRC"][:]  # CHANGE NC AUTOCONVERSION DROPLETS: #/mg/day
    NPRC1 = file.variables["NPRC1"][:]  # CHANGE NR AUTOCONVERSION DROPLETS: #/mg/day
    NCPOSLIM = file.variables["NCPOSLIM"][
        :
    ]  # CHANGE IN CLOUD DROPLET NUMBER DUE TO POSITIVE LIMITING: #/mg/day
    NCNEGLIM = file.variables["NCNEGLIM"][
        :
    ]  # CHANGE IN CLOUD DROPLET NUMBER DUE TO NEGATIVE LIMITING: #/mg/day
    NRPOSLIM = file.variables["NRPOSLIM"][
        :
    ]  # CHANGE IN RAIN DROPLET NUMBER DUE TO POSITIVE LIMITING: #/mg/day
    NRNEGLIM = file.variables["NRNEGLIM"][
        :
    ]  # CHANGE IN RAIN DROPLET NUMBER DUE TO NEGATIVE LIMITING: #/mg/day

    time_mg, z_mg = np.meshgrid(time, z)  # making meshgrid

    cld = CLDLOW.copy()
    cld[:] = np.nan
    for i in range(len(CLDLOW)):
        cld[i] = np.max(CLDLOW[i] + CLDMID[i] + CLDHI[i])

    # calculate accumulated precipitation
    acc_prec = PREC.copy()
    acc_prec[:] = np.nan
    for i in range(len(acc_prec)):
        acc_prec[i] = np.nansum(PREC[: i + 1]) / (time[-1] * 24)

    # calculate surface wind magnitude
    sfc_wnd = (U[:, 0] ** 2 + V[:, 0] ** 2) ** 0.5

    # SAM outputs only give the heights of cell centers.
    # To compute a vertical integral, you need the cell interface heights (i.e., the w levels):
    nz = len(z)
    zi = np.arange(nz + 1).astype(float)
    zi[:] = np.nan
    zi[0] = 0
    zi[1:nz] = 0.5 * (z[: nz - 1] + z[1:nz])
    zi[nz] = 1.5 * z[nz - 1] - 0.5 * z[nz - 2]
    dz = zi[1:] - zi[:-1]  # Compute the cell thicknesses

    ## Calc. inversion height
    # ZINV = inv_h(THETAL, RH, dz, z)
    dz3 = z.copy()
    dz3[:] = np.nan
    dz3[1:] = z[1:] - z[:-1]
    ZINV = inv_h(THETAL, RH, dz3, z)
    d_THETA = THETA[:, 1:] - THETA[:, :-1]

    #################################
    ### calculate modeled CTH
    # correct method
    #    SAM_CTH = CWP.copy()
    #    SAM_CTH[:] = np.nan
    #    for i in range(len(CWP)):
    #        if np.nanmax(CLDCUMDN[i,:]) > 0:
    #            tmp = CLDCUMDN[i,:] / np.nanmax(CLDCUMDN[i,:]) # normalize cumulative cloud fraction by its maxmimum value
    #            idx = np.nanmax(np.where(tmp > 0.5)[0]) # median CTH: height where normalized cumulative cloud fraction crosses 0.5
    #            SAM_CTH[i] = z[idx]

    # Calculate the index of BL:
    # method1: find index where z is equal to ZINV
    inv_idx = np.arange(len(ZINV))
    inv_idx[:] = int(0)
    for i in range(len(ZINV)):
        diff = abs(z - ZINV[i])
        inv_idx[i] = np.where(diff == np.min(diff))[0][0]
    # method2: find infrc where RH goes below 75%
    inv_idx2 = np.arange(len(ZINV))
    inv_idx2[:] = int(0)
    for i in range(len(ZINV)):
        j = 0
        while RH[i, j] > 75:
            j += 1
        inv_idx2[i] = j
    # Not very helpful method!

    # Calc. entrainment:
    entrainment = []  # np.arange(len(ZINV)) #entrainment[:] = int(0)
    for i in range(len(ZINV)):
        entrainment.append(-WOBS[i, inv_idx[i]])
    entrainment = np.array(entrainment) * 1000  # convert to mm/s

    # Marshall-Palmer and other R-Z relations
    #    Z = 10 ** (rad_refl_all[:,0] / 10)
    #    R_MP = (Z / 200) ** (1/1.6) * 24
    #    acc_R_MP = calc_acc_R(R_MP)

    #    R_C2004 = (Z / 57) ** (1/1.1) * 24
    #    acc_R_C2004 = calc_acc_R(R_C2004)

    #### MBL integral of number concentrations
    NA = NAd + NCORIG + NRORIG
    # NA  = NAd + NC + NR

    integ_NA_BL = mbl_ave_N(NA, RHO, dz, inv_idx)
    integ_NC_BL = mbl_ave_N(NC, RHO, dz, inv_idx)
    # integ_NR_BL  = mbl_ave_N(NR,  RHO, dz, inv_idx)
    # You have z(1:nz) which are the heights of the cell centers.
    # Compute the interface heights between cells: zi(1) = 0; zi(2:nz) = 0.5*(z(1:nz-1)+z(2:nz)); zi(nz+1) = 1.5*z(nz) - 0.5*z(nz-1)
    # Compute the cell thicknesses: dz(1:nz) = zi(2:nz+1) - zi(1:nz)

    ####

    ### Entrainment and W_lg
    w_ls_inv = -entrainment
    winw = 2
    entr = ZINV.copy()
    entr[:] = np.nan
    for i in range(len(time)):
        t_entr = 1 / 3
        tind = np.where(abs(time - time[i]) < t_entr / 2)[0]
        # print(tind)
        p = np.polyfit(time[tind], ZINV[tind], 1)
        entr[i] = 1e3 * p[0] / 86400 - w_ls_inv[i]
    entr = smooth(entr, winw)
    mean_entr = "{:.2f}".format(np.nanmean(entr))

    #### Calculate turbulence w'2
    W2_Zinv_200 = W2[:, 0].copy()
    W2_Zinv_200[:] = np.nan
    for i in range(W2[:, 0].size):
        ix_w2 = np.where(abs(ZINV[i] - 200 - z) == np.nanmin(abs(ZINV[i] - 200 - z)))[0]
        W2_Zinv_200[i] = W2[i, ix_w2]

    ### Calculate COD and Re
    def calc_OD(var):
        OD = var[:, 0].copy()
        OD[:] = np.nan
        for i in range(len(OD)):
            idx = np.where(QCCLD[i, :] > 0.01)[0]
            try:
                OD[i] = TAUQCacc[i, np.nanmax(idx)] - TAUQCacc[i, np.nanmin(idx)]
            except BaseException:
                pass
        return OD

    rho_idx = 65
    COD = calc_OD(TAUQCacc)
    SAM_re = (3.0 / 2.0) * (CWP / ISCCPTOT) / (COD * RHO[:, rho_idx] / ISCCPTOT)

    #### Calculate budget terms for aerosol number concentration
    NASTOR = NAdSTRG + NCSTRG + NRSTRG
    NAEDDY = NAdADV + NCADV + NRADV + NAdDIFF + NCDIFF + NRDIFF
    NALSADV = NAdLSADV + NCLSADV + NRLSADV
    NASED = NCSTEN + NRSTEN  # NAdSED + NCSED + NRSED
    NAMPHY = NAdMPHY + NCMPHY + NRMPHY - NASED
    NASCAV = -SCVTNADC - SCVTNADR

    NARC = -NPRC - NPRC1
    NPRA = -NPRA_pos
    # d NA = Srf Ad - (ScvCld Ad + ScvRn Ad) - Accr C +  SlfC R - Fallout R + (NMT Ad + NMT C + NMT R)
    NASTOR[NASTOR > 1000] = np.nan
    NASTOR[NASTOR < -1000] = np.nan
    NARESID = NASTOR - NAEDDY - NALSADV - NASED - NAMPHY - NASCAV
    NARESID[NARESID > 1000] = np.nan
    NARESID[NARESID < -1000] = np.nan

    ####
    mass_1500 = np.arange(NAd[:, 0].size).astype(float)
    mass_1500[:] = np.nan
    for i in range(NAd[:, 0].size):
        mass_1500[i] = np.nansum(RHO[i, :115] * dz[:115])

    NASURF_test = (
        86400 * NAdFLXS[:, 0] / (mass_1500 * 1e6)
    )  # convert from #/m2/s to #/mg/day

    #########
    height_NAEDDY = height_Ave(NAEDDY)
    height_NALSADV = height_Ave(NALSADV)
    height_NASED = height_Ave(NASED)
    height_NASCAV = height_Ave(NASCAV)
    height_NARC = height_Ave(NARC)
    height_NPRA = height_Ave(NPRA)

    MBL_mass = np.arange(NAd[:, 0].size).astype(float)
    MBL_mass[:] = np.nan
    for i in range(NAd[:, 0].size):
        MBL_mass[i] = np.nansum(RHO[i, : inv_idx[i] + 5] * dz[: inv_idx[i] + 5])

    height_NASURF = (
        86400 * NAdFLXS[:, 0] / (MBL_mass * 1e6)
    )  # convert from #/m2/s to #/mg/day
    height_ENTRNMT = height_NALSADV + height_NAEDDY - height_NASURF

    # globals().update(locals())
    return (
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
    )


def delta(THETA):
    nz = THETA.shape[1]
    THETAi = (
        np.arange(THETA.shape[0] * (nz + 1))
        .reshape(THETA.shape[0], nz + 1)
        .astype(float)
    )
    THETAi[:] = np.nan
    THETAi[:, 0] = 0
    THETAi[:, 1:nz] = 0.5 * (THETA[:, : nz - 1] + THETA[:, 1:nz])
    THETAi[:, nz] = 1.5 * THETA[:, nz - 1] - 0.5 * THETA[:, nz - 2]
    d_THETA = THETAi[:, 1:] - THETAi[:, :-1]
    return d_THETA


def inv_h(THETA, RH, dzz, zz):
    #    d_THETA = delta(THETA)
    #    d_RH = delta(RH)
    d_THETA = THETA[:, 1:] - THETA[:, :-1]
    d_RH = RH[:, 1:] - RH[:, :-1]

    ZINV = d_THETA[:, 0].copy()
    ZINV[:] = np.nan
    for i in range(d_THETA.shape[0]):
        z = zz[i, :] if len(zz.shape) > 1 else zz
        dz = dzz[i, :] if len(zz.shape) > 1 else dzz
        dTHETA_dz = d_THETA[i, :] / dz[1:]
        dRH_dz = d_RH[i, :] / dz[1:]
        dTHETA_dz[dTHETA_dz < 0] = 0
        dRH_dz[dRH_dz > 0] = 0
        func = dTHETA_dz * dRH_dz
        if len(zz.shape) > 1:
            indx = np.max(np.where(func == np.nanmin(func))[0])
        else:
            indx = np.min(np.where(func == np.nanmin(func))[0])
        # approximate func as a parabola around the minimum and find the height where that parabola is minimized.
        # This will allow the inversion height to vary continuously as the input profiles change.
        # inversion_test is defined at midpoints of grid
        zavg = 0.5 * (z[:-1] + z[1:])
        rnge = range(indx - 1, indx + 2)
        # we define the parabola, converting from m to km.
        pp = np.polyfit(1e-3 * zavg[rnge], func[rnge], 2)
        # take the derivative of the parabola in coeffient space.
        pp_prime = np.array([2 * pp[0], pp[1]])  # this is its derivative
        # find the zero-crossing of the derivative. This is the inversion height in meters
        z_inv = -1e3 * pp_prime[1] / pp_prime[0]
        ZINV[i] = z_inv
    return ZINV


# Calc. LTS
def calc_LTS(THETA, P):
    indx = np.where((P <= 701) & (P >= 699))[0]

    theta_700 = np.nanmean(THETA[:, indx], 1)
    theta_sfc = THETA[:, 0]
    LTS = theta_700 - theta_sfc
    return LTS


def mbl_ave_N(NA, RHO, dz, inv_idx):
    #    integ_NA_BL = np.arange(NAd[:,0].size)
    integ_NA_BL = NA[:, 0].copy()
    integ_NA_BL[:] = np.nan
    for i in range(NA[:, 0].size):
        dz2 = dz.copy()
        mmm = np.where(np.isnan(NA[i, :]) == 1)[0]
        if len(mmm) > 0:
            dz2[mmm] = np.nan
        mmm2 = np.where(NA[i, :] <= 1)[0]
        if len(mmm2) > 0 and len(mmm2) != len(NA):
            dz2[mmm2] = np.nan
        integ_NA_BL[i] = np.nansum(
            RHO[i, : inv_idx[i]] * dz2[: inv_idx[i]] * NA[i, : inv_idx[i]]
        ) / np.nansum(RHO[i, : inv_idx[i]] * dz2[: inv_idx[i]])
    return integ_NA_BL


def mbl_ave_flight(RFin_alt, RFin_N, RFin_RHO, iii, ZINV):
    if iii >= len(ZINV):
        jjj = np.where(abs(RFin_alt - ZINV[-1]) == np.nanmin(abs(RFin_alt - ZINV[-1])))[
            0
        ][0]
    else:
        jjj = np.where(
            abs(RFin_alt - ZINV[iii]) == np.nanmin(abs(RFin_alt - ZINV[iii]))
        )[0][0]
    RFin_alt_diff = RFin_alt[:-1] - RFin_alt[1:]
    RFin_alt_diff2 = RFin_alt_diff.copy()
    mmm = np.where(np.isnan(RFin_N[1:]) == 1)[0]
    RFin_alt_diff2[mmm] = np.nan
    mmm2 = np.where(RFin_N[1:] <= 0.5)[0]
    RFin_alt_diff2[mmm2] = np.nan
    RFin_N_mean = np.nansum(
        RFin_RHO[jjj:] * RFin_N[jjj:] * RFin_alt_diff2[jjj - 1 :]
    ) / np.nansum(RFin_alt_diff2[jjj - 1 :] * RFin_RHO[jjj:])
    return RFin_N_mean


def mbl_ave_MERRA(MERRA_Na, ZINV, MERRA_H, iii_MERRA, MERRA_RHO):
    MERRA_Na_mean2 = MERRA_Na[:, 0].copy()
    MERRA_Na_mean2[:] = np.nan
    for i in range(MERRA_Na_mean2.size):
        MERRA_Na_mean2[i] = mbl_ave_flight(
            MERRA_H[i, :], MERRA_Na[i, :], MERRA_RHO[i, :], iii_MERRA[i], ZINV
        )
    return MERRA_Na_mean2


def mbl_ave_Forcing(z_forc, MERRA_Na, Forcing_RHO, iii_Forcing, ZINV):
    MERRA_Na_mean2 = MERRA_Na[:, 0].copy()
    MERRA_Na_mean2[:] = np.nan
    for i in range(MERRA_Na_mean2.size):
        MERRA_Na_mean2[i] = mbl_ave_flight(
            z_forc[i, :, 0, 0], MERRA_Na[i, :], Forcing_RHO[i, :], iii_Forcing[i], ZINV
        )
    return MERRA_Na_mean2


def smooth(y, box_pts):
    box = np.ones(box_pts) / box_pts
    y_smooth = np.convolve(y, box, mode="same")
    return y_smooth

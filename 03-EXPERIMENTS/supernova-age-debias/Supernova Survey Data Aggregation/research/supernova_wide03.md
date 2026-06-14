## Facet: Space-based & Multi-wavelength Supernova Surveys

**Last Updated**: 2025  
**Searches Performed**: 15+ independent web searches across NASA archives, survey websites, arXiv, peer-reviewed journals, and data portals  
**Sources Consulted**: MAST, HEASARC, WISeREP, TNS, Gaia Alerts, ASAS-SN, arXiv, ApJ, A&A, PASP

---

### Key Findings

Space-based supernova observations span the electromagnetic spectrum from gamma-rays (INTEGRAL, Fermi) through X-rays (Chandra, XMM-Newton, NuSTAR, NICER, Swift/XRT), UV (Swift/UVOT, GALEX), optical (Kepler/K2, TESS, Gaia, HST), to infrared (Spitzer, JWST, WISE). Each mission provides unique, complementary data products critical for understanding SN physics.

**Key discoveries from this research**:

1. **SOUSA (Swift Optical/Ultraviolet Supernova Archive)** is the largest unified UV/optical SN dataset from space, with 253 SNe observed in 6 UVOT filters [^12^].
2. **TESS** has observed 307 SNe Ia light curves with continuous 30-min monitoring, providing unique early-time constraints on companion interaction [^129^].
3. **GALEX** provides UV light curves for 1,080 SNe Ia, the largest UV sample of thermonuclear SNe [^131^].
4. **Gaia Science Alerts** is the second-largest contributor of transients to the IAU Transient Name Server, publishing ~12 alerts/day [^13^].
5. **JWST** is revolutionizing SN infrared studies with first CCSN spectra (SN 2022acko) and dust detection (SN 2004et) at sensitivities impossible from the ground [^43^][^146^].
6. **Open Supernova Catalog** aggregates 36,000+ SNe with light curves and spectra spanning X-ray to radio, available in machine-readable JSON [^86^].

---

### Mission/Survey Catalog (detailed)

---

#### 1. Hubble Space Telescope (HST) - SN Surveys

**Mission Overview**: HST has been used extensively for high-redshift SN cosmology and detailed studies of individual nearby SNe.

**Major SN Programs**:
- **CANDELS** (Cosmic Assembly Near-infrared Deep Extragalactic Legacy Survey): Multi-cycle treasury program with WFC3/IR imaging; discovered SNe Ia to z ~ 2
- **CLASH** (Cluster Lensing And Supernova survey with Hubble): 25 massive galaxy clusters, 524 orbits, 16 wavelengths from near-UV to near-IR [^133^]
- **SH0ES** (Supernovae, H0, for the Equation of State of dark energy): Riess et al. Cepheid-calibrated SN Ia distances
- **Supernova Cosmology Project**: Perlmutter et al. high-z SNe Ia for dark energy discovery

**Data Archive**: 
- Primary: MAST (Mikulski Archive for Space Telescopes) - https://archive.stsci.edu
- CLASH data at MAST + IRSA: https://archive.stsci.edu/prepds/clash/ [^133^]
- HST data products: FLT, DRZ, DRC images; 1D and 2D spectra

**Data Volume**: 
- CLASH: 25 galaxy clusters with ACS/WFC3 imaging at ~30 and 65 mas pixel scales [^133^]
- Spitzer/IRAC data for all CLASH clusters at 3.6, 4.5, 5.8, 8.0 micron [^134^]

**Wavelength Coverage**: UV (ACS/WFC), optical (ACS, WFC3/UVIS), NIR (WFC3/IR)

**Key Publications**: 
- Riess et al. (2022) - SH0ES H0 measurement
- Postman et al. (2012) - CLASH overview [^133^]

**ML-Ready Datasets**: HST SN images are available through MAST; CLASH provides public catalogs and lens models suitable for ML training.

---

#### 2. Swift/UVOT - SOUSA (Swift Optical/Ultraviolet Supernova Archive)

**Mission Overview**: Swift's UV/Optical Telescope (UVOT) observes SNe in 6 filters (uvw2, uvm2, uvw1, u, b, v) providing critical UV data unavailable from the ground.

**Data Products**: 
- **SOUSA**: Reprocessed all Swift SN data using Breeveld et al. (2012) zeropoints with time-dependent sensitivity corrections [^12^]
- 253 supernovae in the archive, each with multiple UVOT filters
- Image data: hosted at MAST
- Light curves: available at external team page

**Archive Portal**: 
- MAST HLSP: https://archive.stsci.edu/prepds/sousa/ [^12^]
- HEASARC Swift archive (primary): https://heasarc.gsfc.nasa.gov/docs/swift/

**Data Format**: 
- FITS files with naming convention: `hlsp_sousa_swift_uvot_<targname>[-tempsum]_<filter>_<ver>_img.fits.gz`
- Filters: {bb, m2, uu, vv, w1, w2} corresponding to {b, uvm2, u, v, uvw1, uvw2}
- Template-subtracted images available

**Wavelength Coverage**: 1600-5500 Angstroms (UV through optical)

**Key Publications**:
- Brown et al. (2014) - SOUSA description [^12^]
- Fausnaugh et al. (2023) - Four years of TESS + Swift multiwavelength SN Ia [^129^]
- Milkoreit et al. (2022) - SLSN catalog using Swift data [^11^]

**Unique Data Products**: 
- UV light curves critical for bolometric luminosity estimates
- Early-time UV emission traces shock breakout physics
- 44Ti decay detection in young remnants

**ML-Ready**: SOUSA FITS images can be used for CNN-based classification; light curves available in standard formats.

---

#### 3. Kepler/K2 - KEGS (K2 ExtraGalactic Survey)

**Mission Overview**: Kepler/K2 provided unprecedented 30-minute cadence photometry of extragalactic fields, discovering SNe with exquisite time sampling.

**Survey Stats**:
- K2 campaigns monitored galaxies at 30-min cadence
- KEGS (K2 ExtraGalactic Survey): Monitored 11 K2 campaigns (C1, 3, 4, 5, 6, 8, 10, 12, 14, 16, 17) [^154^]
- 23 SNe discovered in KEGS fields to date
- ~6,694 targets in Campaign 16 alone (GO16079) [^163^]
- KSN 2011a, KSN 2011d, KSN 2011b, KSN 2011c, KSN 2012a published [^147^]

**Data Archive**: 
- MAST (Mikulski Archive for Space Telescopes): https://archive.stsci.edu/missions-and-data/k2 [^85^]
- Kepler/K2 HLSPs: https://archive.stsci.edu/hlsp
- Data products: target pixel files, light curves (LC), full-frame images (FFI)

**Data Format**: FITS (long cadence 30-min, short cadence 1-min)

**Key Publications**:
- Olling et al. (2015) - First K2 SNe [^147^]
- Rest et al. (2018) - SN 2018oh K2 light curve [^82^]
- Tucker et al. (2016) - KSN 2011a/d shock breakout

**Unique Data Products**: 
- 30-min cadence photometry covering explosion epoch
- Direct shock breakout detection capability
- Power-law rise time measurements from hours post-explosion

**Cross-matches**: Ground-based follow-up from Pan-STARRS1, DECam, SkyMapper [^154^]

**ML-Ready**: K2 light curves are standard FITS format; KADENZA pipeline produces reduced light curves.

---

#### 4. TESS (Transiting Exoplanet Survey Satellite)

**Mission Overview**: TESS's 30-min cadence FFIs continuously monitor SNe in its 24x96 degree sectors, providing pre-discovery light curves.

**Survey Stats**:
- **307 SNe Ia** light curves from first 4 years (Fausnaugh et al. 2023) [^129^]
- **4,000+ transients** observed in first 4 years [^130^]
- Limiting magnitude: 20th-21st in 8-30 hours
- 30-min FFI cadence (extended mission: 10-min cadence since Sector 27)

**Data Products**:
- **TessTransients**: MIT database of TESS transient light curves
  - Website: https://tess.mit.edu/public/tesstransients/ [^132^]
  - 10,584 total transients, 1,299 supernovae
  - API for downloading: `wget https://tess.mit.edu/public/tesstransients/light_curves/lc_2022sfe_cleaned`
  - Bulk downloads available via GitHub

**Data Archive**:
- Primary: MAST - https://archive.stsci.edu/tess [^138^]
- TICA (TESS Image CAlibration) HLSPs on MAST
- MIT transient server: https://tess.mit.edu/public/tesstransients/ [^132^]

**Data Format**: FITS light curves, CSV transient light curves from MIT pipeline

**Key Publications**:
- Fausnaugh et al. (2021) - Early-time SNe Ia with TESS [^136^]
- Fausnaugh et al. (2023) - 307 SNe Ia light curves [^129^]
- Gordon et al. (Wellesley thesis) - Early time light curves of four TESS SNe [^84^]

**Unique Data Products**:
- Pre-discovery light curves ("precovery") measuring first light
- Continuous monitoring through peak and decline
- Early-time power-law rise indices
- Companion interaction constraints

**Cross-matches**: Coordinated with MAXI, Swift BAT, NICER for multiwavelength monitoring [^130^]

**ML-Ready**: Light curves available as CSV files; bulk download scripts provided.

---

#### 5. Gaia Science Alerts (GSA)

**Mission Overview**: Gaia's all-sky scanning provides homogeneous, high-precision astrometric and photometric alerts for transients, including SNe.

**Survey Stats**:
- 10,765 alerts published up to 31 December 2019 [^13^]
- ~12 alerts/day current rate
- Second-largest contributor of transients to IAU Transient Name Server
- External completeness for SNe: CE = 0.46 [^13^]
- Internal completeness (2+ scans): CI = 0.79 at >3 arcsec from galaxy centers
- Per-transit photometry precise to 1% at G=13, 3% at G=19
- Astrometry accurate to 55 mas vs. Gaia DR2

**Data Archive**:
- Primary alerts page: http://gsaweb.ast.cam.ac.uk/alerts [^15^]
- Data formats: CSV, HTML, RSS, VOEvents
- IAU Transient Name Server (TNS): https://www.wis-tns.org/
- 4 Pi Sky VOEvents broker: https://4pisky.org/voevents/

**Data Products**:
- Per-transit light curves (G-band, BP/RP spectra)
- Astrometric measurements per transit
- Low-resolution BP/RP spectra for each epoch
- Finding charts via Aladin Lite

**Key Publications**:
- Hodgkin et al. (2021) - Gaia EDR3 science alerts [^13^]
- Wyrzykowski et al. (2012) - First Gaia alerts paper

**Unique Data Products**:
- All-sky coverage including Galactic plane (unique among high-resolution surveys)
- Space-based, weather-independent photometry
- BP/RP spectra at every epoch for spectral classification
- Sub-arcsecond spatial resolution
- Discovered superluminous SNe: Gaia16apd, Gaia17biu, pair-instability candidate Gaia16bvd

**ML-Ready**: Alert stream accessible as CSV/JSON; BP/RP spectra enable automated classification.

---

#### 6. GALEX - UV Supernova Observations

**Mission Overview**: The Galaxy Evolution Explorer surveyed the entire sky in UV (2003-2013), providing archival UV light curves for SNe.

**Survey Stats**:
- **1,080 SNe Ia** with GALEX UV light curves (Dubay et al. 2022) [^131^]
- FUV band: 1340-1800 Angstroms
- NUV band: 1700-3000 Angstroms
- Time resolution: 5 ms (photon lists)
- Angular resolution: 4-6 arcsec

**Data Archive**:
- MAST: https://archive.stsci.edu/missions-and-data/galex
- Photon lists stored at MAST
- gPhoton/gPhoton2 pipeline for custom light curve extraction [^137^]

**Data Format**: Photon lists (raw6 files) at MAST; gPhoton generates custom light curves

**Key Publications**:
- Dubay et al. (2022) - 1,080 SNe Ia GALEX light curves [^131^]
- Ofek et al. (2010) - PTF 09uj UV flash with GALEX [^161^]

**Unique Data Products**:
- UV light curves for circumstellar material interaction studies
- Serendipitous UV flash detections (shock breakout candidates)

**ML-Ready**: gPhoton2 pipeline enables bulk light curve generation; VizieR catalog available [^131^][^139^].

---

#### 7. Spitzer Space Telescope - Infrared SN Observations

**Mission Overview**: Spitzer provided mid-infrared imaging and spectroscopy of SNe, critical for dust formation studies.

**Instruments**: IRAC (3.6, 4.5, 5.8, 8.0 micron), IRS (5.2-37 micron spectroscopy), MIPS (24, 70, 160 micron)

**Key Programs**:
- **SEEDS** (Spitzer Extended Extragalactic Distance Survey)
- **SAFIRES** (Spitzer Archival Far-Infrared Extragalactic Survey) [^44^]
- Individual SN programs: SN 2004et, SN 2002hh, SN 2017eaw, SN 2004dj

**Notable Observations**:
- SN 2004et: Spitzer imaging 64-1406 days post-explosion; first spectroscopic evidence for silicate dust in SN ejecta [^144^][^145^]
- SN 2004dj: MIPS 24 micron detection at days 89-129; CO formation inferred [^43^]

**Data Archive**:
- IRSA (NASA/IPAC Infrared Science Archive): https://irsa.ipac.caltech.edu
- MAST for some HLSPs
- Spitzer Heritage Archive

**Data Format**: FITS images and spectra; IRAC and MIPS photometry in catalog form

**Key Publications**:
- Kotak et al. (2009) - SN 2004et dust study [^145^]
- Meikle et al. (2006) - SN 2002hh IR study [^121^]
- Tinyanont et al. (2019) - Spitzer SN II-P light curves

**Unique Data Products**:
- Direct detection of newly formed dust in SN ejecta
- IR echo measurements for CSM studies
- SiO and silicate dust mass estimates

---

#### 8. JWST (James Webb Space Telescope) - SN Observations

**Mission Overview**: JWST provides unprecedented infrared sensitivity and spectroscopic capabilities for SN studies.

**Instruments**: NIRCam (imaging 0.6-5.0 micron), NIRSpec (spectroscopy 0.6-5.3 micron), MIRI (imaging+spectroscopy 5-28 micron)

**Notable Observations**:
- **SN 2022acko** (Type IIP): First JWST CCSN spectrum - NIRSpec + MIRI at ~50 days [^43^]
  - ~30 H I features identified
  - Full SED: 0.4-25 micron combining ground + JWST
  - CO formation mass limit: <10^-8 solar masses
- **SN 2004et** and **SN 2017eaw**: JWST GO-2666 dust reservoir study [^146^]
  - JWST detected dust masses significantly exceeding previous estimates
  - Forward shock dust heating model proposed

**Data Archive**:
- MAST (Mikulski Archive for Space Telescopes): https://archive.stsci.edu
- Raw and calibrated data: level 2 and level 3 products
- Custom pipeline for MIRI MRS point source extraction available

**Key Publications**:
- Shahbandeh et al. (2023) - JWST SN 2022acko [^43^]
- Fox et al. (JWST GO-2666) - Dust reservoirs in SNe IIP [^146^]

**Unique Data Products**:
- First mid-IR CCSN spectra at R~2700 (MIRI MRS)
- Direct dust mass measurements in ejecta
- Molecular line detections (CO, SiO)
- s-process element identifications (Sc II, Ba II)

---

#### 9. Chandra X-ray Observatory - SN Data

**Mission Overview**: Chandra provides high-resolution X-ray imaging and spectroscopy of SN remnants and young SNe.

**Instruments**: ACIS (0.5-10 keV imaging spectroscopy), HRC (high-resolution imaging)

**Key Datasets**:
- **Chandra Supernova Remnants Catalog**: https://snrcat.cfa.harvard.edu/ [^115^]
  - X-ray morphology and spectra of Galactic and Magellanic Cloud SNRs
  - Images in selected energy bands, smoothed images, three-color images
  - Pulse height spectra, count rates, fluxes, luminosities
  - Event files and images downloadable in multiple formats
  - Exposures: 10-100 ks (deep 1 Ms observations excluded)
  - ACIS FOV: 8'x8' or 16'x16'

**Data Archive**:
- Chandra Data Archive (CDA): https://cxc.harvard.edu/cda/
- HEASARC: https://heasarc.gsfc.nasa.gov/
- Chandra Supernova Remnants Catalog: https://snrcat.cfa.harvard.edu/ [^115^]

**Key Publications**:
- Soderberg et al. (2008) - SN 2008D X-ray shock breakout detection
- Long et al. - Chandra ACIS Survey of M83: 458 X-ray sources

**Unique Data Products**:
- X-ray shock breakout detections (SN 2008D)
- SNR morphology and spectral evolution
- Non-thermal emission studies

---

#### 10. XMM-Newton - SN Observations

**Mission Overview**: XMM-Newton provides sensitive X-ray imaging and spectroscopy with large effective area.

**Instruments**: EPIC (pn, MOS1, MOS2 detectors; 0.2-12 keV), RGS (high-resolution spectroscopy), OM (optical/UV monitor)

**Key Datasets**:
- **M 33 XMM-Newton SNR Catalog**: 105 SNRs detected at 3-sigma [^45^]
  - 54 newly detected in X-rays
  - 3 newly discovered SNRs
  - 8-field mosaic covering D25 contours
  - Combined with Chandra data for 15 deep spectral fits
  - X-ray luminosity function constructed

**Data Archive**:
- XMM-Newton Science Archive (XSA): https://xmm.esac.esa.int/xsa/
- HEASARC: https://heasarc.gsfc.nasa.gov/

**Data Format**: ODF (Observation Data Files), PPS (Pipeline Products), EPIC event files

**Key Publications**:
- M 33 XMM-Newton SNR study (MNRAS 472, 308) [^45^]
- Williams et al. (2015) - M 33 point source catalog (ApJS 218, 9)
- Ducci et al. - XMM-Newton study of M83: 189 X-ray sources

**Unique Data Products**:
- Deep X-ray SNR population studies
- Spectral fitting (temperatures, ionization time-scales, abundances)
- X-ray luminosity functions

---

#### 11. NuSTAR - Hard X-ray SN Studies

**Mission Overview**: NuSTAR is the first focusing high-energy X-ray observatory, opening the hard X-ray sky (3-79 keV).

**Instruments**: Two co-aligned telescopes with FPMA and FPMB detectors

**Key Capabilities**:
- Energy range: 3-79 keV
- Angular resolution: 18" FWHM
- Spectral resolution: 400 eV FWHM at 10 keV
- Astrometric accuracy: 8" at 90% confidence

**Data Archive**:
- HEASARC: https://heasarc.gsfc.nasa.gov/docs/nustar/ [^111^]
- NuSTAR Caltech: https://www.nustar.caltech.edu/
- SSDC mirror: https://nustar.ssdc.asi.it/ [^122^]

**Key Publications**:
- Harrison et al. (2013) - NuSTAR reference paper
- NuSTAR detection of hard X-ray source in IC 443 SNR [^123^]
- Hard X-ray survey of Galactic Center [^112^]

**Unique Data Products**:
- 44Ti decay line detection in young SNRs
- Non-thermal continuum studies
- Hard X-ray SNR shock studies (e.g., Puppis A) [^118^]

---

#### 12. INTEGRAL - Gamma-ray SN Observations

**Mission Overview**: INTEGRAL provides hard X-ray and gamma-ray imaging with IBIS/ISGRI.

**Instruments**: IBIS/ISGRI (15 keV - 10 MeV imaging), SPI (20 keV - 8 MeV spectroscopy), JEM-X (3-35 keV), OMC (optical 500-600 nm)

**Key Datasets**:
- IBIS/ISGRI soft gamma-ray catalog: 209 sources in second catalog (20-100 keV) [^135^]
- GRB archival search: 7 new GRBs + 886 off-field GRBs [^128^]

**Data Archive**:
- INTEGRAL Science Legacy Archive (ISLA): https://www.cosmos.esa.int/web/integral [^141^]
- ISDC Data Centre for Astrophysics: https://www.isdc.unige.ch/
- HEASARC: https://heasarc.gsfc.nasa.gov/

**Key Publications**:
- Bird et al. (2004, 2006) - IBIS/ISGRI catalogs [^135^]
- Soderberg et al. (2008) - SN 2008D/Swift comparison

---

#### 13. NICER - X-ray Timing of Compact Objects

**Mission Overview**: NICER on the ISS provides fast X-ray timing and spectroscopy (0.2-12 keV).

**Applications for SNe**:
- Central compact object (CCO) studies in SNRs
- Neutron star cooling post-SN
- Pulsar timing for SNR age constraints

**Data Archive**: HEASARC: https://heasarc.gsfc.nasa.gov/docs/nicer/ [^191^]

---

### Multiwavelength Compilation Datasets

---

#### 14. Open Supernova Catalog (OSC)

**Description**: Online collection of observations and metadata for 36,000+ SNe and candidates [^86^]

**Archive**: https://github.com/astrocatalogs/supernovae [^89^]

**Data Products**:
- Individual JSON files for each SN containing all metadata, light curves, spectra
- Rebuilt daily from dozens of sources
- X-ray to radio frequency coverage
- Hierarchical, human- and machine-readable JSON

**ML Applications**:
- SNAD anomaly detection project: 45,162 objects downloaded [^81^]
- Isolation Forest algorithm for finding rare events [^160^]
- Gaussian process interpolation for light curves

**Key Publications**:
- Guillochon et al. (2016, 2017) - OSC description [^86^]
- Pruzhinskaya et al. (2019) - Anomaly detection in OSC [^81^]

---

#### 15. WISeREP (Weizmann Interactive Supernova Data Repository)

**Description**: Archive of SN spectra and photometry with interactive tools [^116^]

**Archive**: https://www.wiserep.org/ [^117^]

**Current Statistics** (as of 2024):
- 72,503 total spectra
- 29,468 objects
- 28,037 objects with spectra
- 59,793 public spectra

**Data Products**:
- Spectra search and download (CSV/TSV/JSON metadata + ASCII files)
- Light curves and photometry
- Interactive spectral analysis (iFigure tool)
- NGSF spectral classification tool
- Bulk API for automated downloads

**Key Publications**:
- Yaron & Gal-Yam (2012) - WISeREP description [^143^]

---

#### 16. Transient Name Server (TNS)

**Description**: Official IAU hub for reporting and classifying extragalactic transients.

**Archive**: https://www.wis-tns.org/

**Features**:
- Discovery reports and classifications
- Photometry points and classification spectra
- Bot API for automated submissions
- Cross-matches with major surveys

---

#### 17. HEASARC Supernova Databases

**Datasets Available**:
- **Asiago Supernova Catalog (Dynamic Version)**: All SNe since 1885 with parent galaxy data [^142^]
- **Sternberg Astronomical Institute Catalog of Supernovae**: Russian SN catalog
- **M 33 XMM-Newton SNR Catalog**: 105 X-ray SNRs in M33 [^45^]
- **SAFIRES MIPS 70 micron Catalog**: Spitzer far-IR catalog [^44^]

**Archive**: https://heasarc.gsfc.nasa.gov/W3Browse/ [^117^]

---

#### 18. Carnegie Supernova Project (CSP)

**Description**: Ground-based but included for multiwavelength completeness; optical+NIR well-calibrated SN photometry.

**Data Products**:
- CSP-I (2004-2009): 74 SNe II
- CSP-II (2011-2015): 20 SNe II
- Total: **94 SNe II** with uBgVri + YJH photometry [^190^]
- 9,817 optical + 1,872 NIR photometric data points
- Spectroscopy: Gutierez et al. (2017) for CSP-I; Davis et al. (2019) for CSP-II

**Archive**: https://csp.obs.carnegiescience.edu/data [^190^]
- CDS: http://cdsarc.u-strasbg.fr/viz-bin/cat/J/A+A/692/A95

**Key Publications**:
- Anderson et al. (2024) - CSP SN II data release [^190^]

---

#### 19. SDSS-II Supernova Survey

**Description**: 300 deg2 repeat ugriz imaging of Stripe 82 (2005-2007)

**Data Products**:
- 10,258 variable/transient sources
- 4,607 SN candidates (largest sample ever compiled)
- 889 spectroscopically observed
- SALT2 distance moduli for 1,364 SNe Ia
- Host galaxy properties from SDSS photometry

**Archive**: https://data.sdss.org/sas/dr18/ [^192^][^193^]

**Key Publications**:
- Sako et al. (2018) - SDSS-II SN Survey data release [^192^]

---

### Trends & Signals

1. **UV is Critical for Bolometric Corrections**: Swift/UVOT and GALEX provide the only large UV SN samples, essential for accurate bolometric luminosity estimates and shock breakout studies. ~20-50% of bolometric flux can be missed without UV data [^14^].

2. **Continuous Monitoring from Space**: Kepler/K2 and TESS provide unique pre-discovery light curves with power-law rise measurements starting hours after explosion, constraining progenitor radii and companion interaction [^129^][^136^].

3. **JWST is Revolutionizing SN Infrared Studies**: First CCSN spectra, direct dust mass measurements, and molecular detections are transforming our understanding of dust production in SNe [^43^][^146^].

4. **Multiwavelength Synergies**: Combining space-based UV (Swift, GALEX) + optical (TESS, Gaia) + IR (Spitzer, JWST) + X-ray (Chandra, XMM, NuSTAR) provides the most complete picture of SN physics. Cross-matched datasets are essential for ML applications.

5. **Anomaly Detection with ML**: Projects like SNAD using the Open Supernova Catalog demonstrate the power of ML (isolation forests, active anomaly detection) to find rare events in large photometric datasets [^158^][^160^].

6. **Real-time Alert Streams**: Gaia, TESS, and Swift provide near-real-time transient detection (2-3 days for Gaia, weekly TESS TICA releases, 4-6 hours for Swift), enabling rapid follow-up campaigns.

---

### Recommended Deep-Dive Areas

1. **Swift/UVOT + TESS Joint Analysis**: Cross-match SOUSA UV data with TESS optical light curves for multiwavelength early-time SN Ia physics. ~100 overlapping SNe expected.

2. **JWST SN Spectral Database**: As JWST data accumulate, create a standardized database of MIRI/NIRSpec SN spectra for ML-based spectral classification and parameter estimation.

3. **Gaia BP/RP Spectra for SN Classification**: Gaia's low-resolution spectra (R~100) for thousands of SNe present an opportunity for training spectroscopic classifiers on the largest homogeneous SN dataset.

4. **Kepler/K2 Background Pixel Survey**: Ridden-Harper et al. (2020) showed that analyzing K2 background pixels can reveal additional transients missed by target pixel analysis [^157^].

5. **Spitzer+JWST Dust Mass Comparison**: Combine archival Spitzer IR observations with new JWST MIRI data to build a comprehensive dust production catalog for core-collapse SNe.

6. **TESS Precovery Pipeline**: Systematic search for TESS precovery of all SNe reported to TNS. Fausnaugh maintains a database of 4,000+ TESS transients with light curves available on request [^130^].

7. **X-ray to Optical Correlations**: Cross-match Swift XRT data with UVOT and ground-based optical for joint X-ray/UV/optical SN studies.

8. **SNAD Anomaly Detection Integration**: Integrate the SNAD pipeline with live survey data streams (ZTF, ATLAS) for real-time detection of unusual SNe.

---

### Citation Index

[^10^] - Realtime Fitting and Classification of Supernova Light Curves (Superphot+, ZTF)
[^11^] - Light Curve Properties, Models, and Catalog Description (SLSN sample with Swift)
[^12^] - Swift's Optical/Ultraviolet Supernova Archive (SOUSA) at MAST
[^13^] - Gaia Early Data Release 3 - Gaia photometric science alerts (Hodgkin et al. 2021)
[^14^] - Supernovae Analysis Application (SNAP) paper
[^15^] - Gaia Science Alerts project page
[^43^] - JWST NIRSpec+MIRI Observations of SN 2022acko (Shahbandeh et al. 2024)
[^44^] - Spitzer SAFIRES MIPS 70 micron Catalog at Data.gov
[^45^] - M 33 XMM-Newton Supernova Remnants Catalog
[^81^] - SNAD anomaly detection in OSC (VizieR catalog)
[^82^] - SN 2018oh K2 light curve (Dong et al. 2018)
[^84^] - TESS Early Time Light Curves (Wellesley thesis)
[^85^] - K2 mission page at MAST
[^86^] - Open Supernova Catalog (Guillochon et al. 2016)
[^89^] - OSC GitHub repository
[^111^] - NuSTAR at HEASARC
[^112^] - NuSTAR Galactic Center Survey at Data.gov
[^115^] - Chandra Supernova Remnants Catalog
[^116^] - WISeREP Getting Started guide
[^117^] - WISeREP home page
[^118^] - NuSTAR Cycle 12 accepted programs (Puppis A)
[^121^] - Spitzer study of SN 2002hh (Meikle et al. 2006)
[^122^] - NuSTAR SSDC mirror archive
[^123^] - NuSTAR detection in IC 443 SNR
[^128^] - INTEGRAL IBIS archival GRB search
[^129^] - Fausnaugh et al. (2023) - 307 TESS SNe Ia
[^130^] - MIT Time Domain Astronomy (TESS transients database)
[^131^] - Dubay et al. (2022) - GALEX UV light curves of 1080 SNe Ia
[^132^] - TessTransients MIT database
[^133^] - CLASH at MAST
[^134^] - CLASH at IRSA (Spitzer data)
[^135^] - INTEGRAL/IBIS soft gamma-ray survey thesis
[^136^] - Fausnaugh et al. (2021) - Early TESS SNe Ia
[^137^] - gPhoton2 pipeline for GALEX
[^138^] - TESS at MAST
[^139^] - GALEX SNe Ia at VizieR/CDS
[^141^] - INTEGRAL at ESA
[^142^] - Asiago Supernova Catalog at HEASARC
[^143^] - WISeREP description paper (Yaron & Gal-Yam 2012)
[^144^] - Spitzer SN 2004et dust study (UT Austin repository)
[^145^] - Kotak et al. (2009) - SN 2004et dust (ApJ)
[^146^] - JWST dust reservoirs in SNe IIP (Fox et al.)
[^147^] - Kepler SNe II-P shock breakout (Tucker et al. 2016)
[^154^] - SkyMapper transient survey including KEGS fields
[^157^] - Search for undiscovered transients in K2 (Ridden-Harper et al. 2020)
[^158^] - SNAD anomaly detection paper
[^160^] - SNAD website and publications
[^161^] - SN shock breakout presentation (Suzuki 2014)
[^163^] - K2 approved programs at Campaign 16
[^189^] - NICER timing of neutron star
[^190^] - CSP SN II data release (Anderson et al. 2024)
[^191^] - NICER at HEASARC
[^192^] - SDSS-II SN Survey data release (Sako et al. 2018)
[^193^] - SDSS-II SN Survey arXiv preprint

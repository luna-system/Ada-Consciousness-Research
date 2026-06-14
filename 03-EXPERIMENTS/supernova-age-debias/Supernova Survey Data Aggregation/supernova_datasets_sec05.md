## 5. Space-based & Multi-wavelength Datasets

Ground-based surveys deliver the vast majority of supernova alerts, but several critical wavelengths and cadences are accessible only from above the atmosphere. Ultraviolet (UV) photometry below 3,000 Angstroms is fully blocked by the ozone layer; near-infrared (near-IR) windows at 1–2.5 μm suffer from strong telluric absorption; and continuous high-cadence monitoring without weather interruption is impossible from any single ground site. Space-based missions therefore fill indispensable niches in the ML training ecosystem: they provide UV spectral energy distributions (SEDs) that constrain dust extinction, high-cadence pre-explosion baselines that enable shock-breakout detection, and all-sky scanning that removes weather bias. This chapter surveys seven operational or recently completed space missions that have produced publicly available supernova datasets suitable for machine learning, concluding with an analysis of the remaining near-IR data gap that future facilities will address.

### 5.1 TESS

The Transiting Exoplanet Survey Satellite (TESS) was designed to detect transiting exoplanets around nearby stars, yet its 30-minute cadence full-frame images (FFIs) covering roughly 85% of the sky have proven to be a powerful resource for time-domain astrophysics [^1^][^2^]. TESS operates in a single broad red-optical bandpass (600–1000 nm) with a field of view of 24 x 96 degrees per sector. During the primary mission (Sectors 1–26), FFIs were recorded every 30 minutes; the extended mission from Sector 27 onward shortened this to 10 minutes, offering even finer temporal resolution for early-rise studies. The instrument reaches approximately 20th magnitude at 3-sigma significance when binned to 8-hour intervals and achieves ~1% photometric precision at TESS magnitude 14.

#### 5.1.1 MIT TessTransients Database

The primary curated access point for TESS supernova light curves is the MIT TessTransients database, maintained by the TESS team [^3^][^4^]. As of 2025, the database catalogs 10,584 total astrophysical transients of all types, of which 1,299 are confirmed supernovae with extracted light curves. The database is updated weekly using TICA High Level Science Product (HLSP) data from the Mikulski Archive for Space Telescopes (MAST).

The flagship supernova dataset is Fausnaugh et al. (2023), which reports 307 Type Ia SNe observed during TESS Years 1–4 [^3^]. This sample is complemented by Vallely et al. (2021), who present high-cadence observations of 22 core-collapse SNe, enabling rise-time measurements that are inaccessible from ground-based cadences [^2^]. Each light curve file is distributed as ASCII text containing Barycentric Julian Date (BJD), background-subtracted relative flux, flux error, quality flags, and calibrated TESS magnitude where available [^4^]. The published sample is binned to 8-hour intervals; raw FFI extraction at native cadence can be performed with tools such as `lygos`, `eleanor`, `TGLC`, or `TESSCut`.

#### 5.1.2 Unique Value for ML

TESS's principal ML contribution lies in early-time light curve morphology. The 30-minute (and now 10-minute) cadence captures the first hours to days of a supernova explosion with temporal resolution that no ground survey can match. Fausnaugh et al. (2023) measured a mean rise time of 15.7 +/- 3.5 days for their 307 SNe Ia sample and tested the fireball model prediction of a power-law rise index beta=2.0, finding significant diversity that encodes information about progenitor radius and companion interaction [^3^]. The detection of flux excess above a simple power-law rise, as seen in SNe such as 2018oh and 2017cbv, provides a discriminant between single-degenerate and double-degenerate progenitor channels. For ML classifiers, TESS-derived features—including the power-law index beta, rise curvature, and flux excess amplitude—can be concatenated with ground-based multi-color photometry to improve early-time classification accuracy.

#### 5.1.3 Data Access

Individual light curves are accessible via a simple URL pattern: `https://tess.mit.edu/public/tesstransients/light_curves/lc_2022sfe_cleaned`, where "2022sfe" is replaced with the IAU designation. Bulk downloads are available through a dedicated page or a version-controlled GitHub repository (`mmfausnaugh/lc_bulk`). The `tess-point` Python tool identifies which TESS sector covered a given coordinate, enabling programmatic cross-matching with ground-based alert streams.

### 5.2 Kepler/K2

The Kepler Space Telescope delivered continuous 30-minute cadence photometry with a stability of 10–100 parts per million, producing what remain the highest-quality extragalactic supernova light curves ever obtained [^5^][^6^]. The Kepler bandpass spans 430–890 nm, similar to the Johnson-Cousins V+R composite. Unlike TESS, Kepler provided uninterrupted month-long baselines with no day-night gaps, enabling detection of sub-hour transient phenomena.

#### 5.2.1 Kepler Extragalactic Survey (KEGS)

The Kepler Extragalactic Survey (KEGS), led by Peter Garnavich and Robert Olling, monitored approximately 500 galaxies during the prime Kepler mission [^5^]. The sample is modest—23 SNe in total across Kepler and K2 combined—but the data quality is extraordinary. Olling et al. (2015) published three SNe Ia with pre-explosion baseline coverage, while Garnavich et al. (2016) reported the first visible-light detection of shock breakout in Type II-P supernovae (KSN 2011a and KSN 2011d), measuring progenitor radii of 280 and 490 solar radii respectively [^5^]. These observations provide the only direct empirical constraints on the radii of red supergiant SN progenitors.

The K2 extension, particularly Campaign 16 (December 2017–February 2018), targeted approximately 50 times more galaxies than KEGS through the K2 Supernova Cosmology Experiment [^6^]. The most extensively studied K2 supernova is SN 2018oh (ASASSN-18bt), a Type Ia at 52.7 Mpc that exhibited a two-component early rise interpreted as evidence of companion interaction [^6^].

#### 5.2.2 Data Access

All Kepler/K2 data are archived at MAST and accessible through the `lightkurve` Python package. For supernova work, Target Pixel Files (TPFs) are the preferred product because they allow custom aperture photometry and difference imaging. The K2 mission suffered from pointing drift of ~4 arcseconds due to its two-wheel control mode, making image subtraction a necessary step in most analyses. The `lightkurve` workflow—search, download TPF, apply custom aperture, and extract light curves—enables reproduction of published K2 SN photometry in a few lines of Python.

#### 5.2.3 Unique Science for ML

Kepler/K2 data are unique in providing pre-explosion baselines and continuous shock-breakout coverage. For ML models, the pre-explosion flux constraint eliminates one of the largest systematic uncertainties in rise-time fitting: the unknown explosion epoch. K2's shock-breakout light curves also serve as training templates for identifying similar events in lower-cadence data. However, the small sample size (~23 SNe total) limits the statistical power of purely Kepler-based classifiers; these data are best used as augmentation features rather than primary training sets.

### 5.3 Swift/SOUSA

The Neil Gehrels Swift Observatory's UltraViolet/Optical Telescope (UVOT) provides the largest homogeneous sample of UV supernova light curves from any single instrument [^7^][^8^]. The 30-cm modified Ritchey-Chretien telescope carries a photon-counting detector with six broadband filters spanning 1,928 to 5,468 Angstroms: UVW2, UVM2, UVW1, U, B, and V. Swift's rapid Target of Opportunity response (typically within hours) enables early-time UV observations that ground-based surveys cannot replicate.

#### 5.3.1 MAST HLSP Archive

The Swift Optical/Ultraviolet Supernova Archive (SOUSA), led by Peter Brown at Texas A&M, contains processed UVOT photometry for 253 supernovae of all major types [^8^][^9^]. All data have been reprocessed with Breeveld et al. (2011) zeropoints and time-dependent sensitivity corrections, ensuring internal consistency across the 2005–2024 temporal baseline. Each supernova typically has photometry in 3–6 filters, creating multi-color SEDs at epochs ranging from days to weeks after explosion.

SOUSA data products are distributed at two levels [^8^]: image products hosted on MAST in FITS format (summed images with and without the supernova), and light curve products available as ASCII/CSV files from the SOUSA website. The full tarball of 270+ SNe can be downloaded directly. For researchers requiring photometry from custom apertures, the HEASoft `uvotsource` tool performs aperture photometry on UVOT images with user-defined source and background regions.

#### 5.3.2 UV Data for Dust Extinction and Color Evolution

The UV wavelength regime is critically important for ML classifiers because it provides strong discriminatory power between supernova types and constrains dust extinction independently of optical color measurements. Brown et al. (2009) established that SNe Ia show homogeneous UV colors while core-collapse SNe evolve rapidly in the UV, enabling type separation from color-color diagrams alone [^7^]. Devarakonda et al. (2022) extended this work to 97 SNe Ia, demonstrating correlations between UV and optical light curve parameters that can be used to cross-validate photometric classifiers [^10^]. The UVW2-V color differentiates SNe Ia from core-collapse events at early times, while UVW1-U tracks the UV decay rate and identifies UV-bright subtypes such as 91T-like and super-Chandrasekhar events [^7^][^10^]. For cosmological ML applications, UV data provide the leverage needed to separate intrinsic color variations from dust reddening, reducing the systematic uncertainty in distance estimates.

### 5.4 GALEX

The Galaxy Evolution Explorer (GALEX) mission, operational from 2003 to 2013, provided UV imaging in two bands: Far-UV (FUV: 1,344–1,786 Angstroms) and Near-UV (NUV: 1,771–2,831 Angstroms) [^11^][^12^]. Unlike Swift's pointed observations, GALEX scanned large areas of the sky repeatedly, building up time-domain coverage that includes serendipitous observations of thousands of supernovae. The gPhoton database at MAST hosts approximately 130 TB of photon-level data with time resolution of 5 milliseconds, comprising roughly 1.1 trillion sky-projected photon events [^11^].

#### 5.4.1 gPhoton2 Pipeline

The original gPhoton software enabled extraction of calibrated light curves from GALEX photon data, but processing speed limited its utility for large samples. The updated gPhoton2 pipeline, developed by Million Concepts, delivers 1–3 orders of magnitude faster processing with improved calibration and automatic light curve generation at user-defined temporal resolution [^12^]. The pipeline can be invoked from the command line or Python API and produces 30-second binned light curves, images, and photon lists from raw GALEX telemetry. Installation follows standard `git clone` and conda environment setup; execution requires only the target GALEX eclipse number and desired band.

#### 5.4.2 GALEX Supernova Catalog

Milne et al. (2010) compiled UV light curves for approximately 1,080 SNe Ia using a combination of GALEX and Swift data, creating the largest UV SN Ia sample to date [^11^]. More recently, the 1UVA catalog (2024) extended time-domain coverage to roughly seven times the original GALEX Time-Domain Survey area by mining 385 NUV fields with more than 10 visits each [^13^]. GALEX wavelengths extend below Swift's UVW2 filter (1,928 Angstroms), probing the regime where line blanketing and circumstellar interaction produce the strongest spectral signatures. For ML training, GALEX data provide historical UV baseline photometry that can be cross-matched with ground-based optical light curves to build bolometric SEDs and constrain extinction corrections from the UV through the optical.

### 5.5 Gaia Alerts

The Gaia Photometric Science Alerts (GSA) system provides an all-sky transient survey with two unique capabilities: sub-arcsecond spatial resolution and low-resolution BP/RP spectra at every observing epoch [^14^][^15^]. Gaia scans the entire sky approximately once per month with two fields of view separated by 106.5 degrees, delivering G-band photometry (330–1,050 nm) at ~1% precision for sources as faint as G=13 and ~3% precision at G=19.

#### 5.5.1 Alert Statistics and Spectroscopic Coverage

Through the end of 2024, Gaia has published 10,785 alerts (updated from the 10,765 reported through 2019 in Hodgkin et al. 2021) [^15^]. Alerts are published at a rate of approximately 12 per day. The classification rate stands at roughly 25%, biased toward supernovae because follow-up campaigns prioritize these events. Critically, every alert includes BP (330–680 nm, R~100) and RP (640–1,000 nm, R~100) spectra at every epoch, making Gaia the only space-based survey that provides spectral information for all transient detections [^15^][^17^].

#### 5.5.2 Real-Time Detection and Southern Sky Coverage

Gaia's scanning mode provides continuous all-sky coverage including the Galactic plane, which most ground-based time-domain surveys avoid. The southern sky advantage is particularly important for supernova studies because the southern celestial hemisphere contains the Large Magellanic Cloud, the nearest active star-forming environment, and deep extragalactic fields such as Chandra Deep Field-South and the Dark Energy Survey region. The GaiaX alert stream provides programmatic access to alert data in CSV format, enabling real-time integration with ML classification pipelines [^15^].

#### 5.5.3 BP/RP Spectra for Classification

The BP/RP spectra, though low in resolution (R~100), provide classification information that is orthogonal to photometric light curve shape. Blagorodnova et al. (2014) demonstrated that most major supernova types can be recognized from BP/RP-like spectra alone with low confusion down to G=19 magnitude [^17^]. Simulations show that the GS-TEC (Gaia Transient Event Classifier) can estimate redshift from spectral features and determine epoch relative to peak brightness. For ML applications, the spectral data at each epoch enable construction of time-resolved color indices that are more robust to dust extinction than single-epoch photometry. Data access is through the Gaia Science Alerts web interface (`gsaweb.ast.cam.ac.uk/alerts/`), which provides per-alert pages with downloadable CSV light curves, spectra in custom format, finding charts, and cross-matches to other transient catalogs. The Cambridge Photometric Calibration Server (CPCS) aggregates follow-up photometry from multiple ground-based telescopes in JSON format.

### 5.6 JWST and Hubble

The James Webb Space Telescope (JWST) and the Hubble Space Telescope (HST) extend supernova observations into the near-IR and mid-IR, probing high-redshift populations where rest-frame optical wavelengths are redshifted into the infrared. Together, these missions provide the only systematic samples of SNe at z>1, essential for training classifiers that will operate on Roman Space Telescope and Euclid data.

#### 5.6.1 JWST High-Redshift Transients

JWST's Near-Infrared Camera (NIRCam) and Near-Infrared Spectrograph (NIRSpec) have opened a new era in high-redshift supernova studies with sensitivity from 0.6 to 5.3 μm [^18^][^19^]. The JWST Advanced Deep Extragalactic Survey (JADES) has been the most productive program for transient science, discovering 53 transients in the GOODS-S field at redshifts from z=0.5 to z=4.4, corresponding to a transient density of approximately one per square arcminute per epoch [^18^][^19^]. Key discoveries include a spectroscopically confirmed SN Ia at z=2.9 (Pierel et al. 2024), a broad-lined Ic at z=2.83 (Siebert et al. 2024), and a UV-bright SN at z=3.6 (Coulter et al. 2025). Complementary treasury programs COSMOS-Web and PRIMER cover 133 square arcminutes—roughly five times the JADES-Deep area—at shallower depth (~28 AB mag), yielding 68 SNe with host photometric redshifts predominantly at 1<z<2 [^19^].

All JWST data are publicly available through MAST. Key program IDs for supernova research include 1180 and 3215 (JADES NIRCam imaging), 6541 (JADES transient follow-up with NIRSpec+NIRCam), 1727 (COSMOS-Web), and 1837 (PRIMER). Data products include multi-epoch multi-filter imaging in FITS format, prism spectra, template-subtracted difference images, and aperture photometry catalogs.

#### 5.6.2 HST Archive: CANDELS and CLASH

HST's CANDELS (Cosmic Assembly Near-infrared Deep Extragalactic Legacy Survey) and CLASH (Cluster Lensing And Supernova survey with Hubble) Multi-Cycle Treasury programs provided the first substantial sample of high-redshift SNe Ia with rest-frame optical-NIR photometry [^20^][^21^]. CANDELS covered five deep fields (GOODS-S/N, COSMOS, UDS, EGS) spanning ~0.25 square degrees, while CLASH observed 25 galaxy cluster fields plus 13 parallel fields. Observations were obtained with ACS (optical) and WFC3-IR (0.8–1.7 μm) at a cadence of approximately 50 days between epochs. Rodney et al. (2014) cataloged 65 SNe discovered in CANDELS out to z=2.5, while Riess et al. (2018) used the combined CANDELS+CLASH sample of 15 SNe Ia at z>1 (9 with reliable distance estimates) as a high-redshift anchor for Hubble constant measurements [^21^][^20^]. Photometry tables are published in the Riess et al. (2018) appendix and accessible through VizieR and MAST.

#### 5.6.3 Space-Based Mission Comparison

| Mission | SN Sample | Cadence | Wavelength Coverage | Unique ML Value | Data Access |
|:---|:---|:---|:---|:---|:---|
| TESS | 307 SNe Ia + 4,000+ transients [^3^] | 30 min (10 min extended) | 600–1000 nm, single band | Early-rise morphology; power-law index beta; companion interaction | MIT TessTransients API; CSV [^3^][^4^] |
| Kepler/K2 | 23+ SNe [^5^] | 30 min, continuous | 430–890 nm, single band | Pre-explosion baseline; shock breakout; progenitor radii | MAST; `lightkurve` Python package [^5^][^6^] |
| Swift/SOUSA | 253 SNe, 6 filters [^8^] | ~2 days (ToO: hours) | 1,928–5,468 Angstroms (UVW2/UVM2/UVW1/U/B/V) | UV-optical color evolution; dust extinction; SED fitting | MAST HLSP + SOUSA website; FITS + ASCII [^8^][^9^] |
| GALEX/gPhoton | 1,080 SNe Ia UV LCs [^11^] | Variable (days–weeks) | FUV (1,344–1,786 A) + NUV (1,771–2,831 A) | Photon-level time resolution; UV bolometric corrections | gPhoton2 @ MAST; Parquet/CSV [^11^][^12^] |
| Gaia Alerts | 10,785 alerts (through 2024) [^15^] | ~1 visit/month | G band (330–1,050 nm) + BP/RP spectra (R~100) | Low-res spectra at every epoch; all-sky; no weather bias | Gaia Science Alerts web; CSV + spectra [^15^][^17^] |
| JWST (JADES) | 53 transients (z=0.5–4.4) [^18^] | ~1 year between epochs | 6–9 NIRCam filters (0.6–5.0 μm) | First high-z SN NIR spectroscopy; rest-frame UV at z>2 | MAST; FITS [^18^][^19^] |
| HST (CANDELS+CLASH) | 65+ SNe (out to z=2.5) [^21^] | ~50 days | ACS optical + WFC3-IR (0.8–1.7 μm) | First large z>1 SN Ia sample; cosmological-quality photometry | MAST + VizieR; FITS + ASCII [^20^][^21^] |

The seven missions are complementary rather than overlapping. TESS and Kepler/K2 provide time-domain resolution; Swift, GALEX, and Gaia provide wavelength diversity (UV through optical) and spectral information; JWST and HST probe the high-redshift universe where rest-frame optical features shift into the near-IR. For an ML practitioner building a multi-wavelength classifier, the optimal strategy is to combine Swift UVOT colors with TESS early-rise parameters and Gaia BP/RP spectral slopes, using JWST/HST data as high-redshift validation samples.

### 5.7 The NIR Gap

Near-infrared observations are critical for supernova cosmology because NIR light curves exhibit reduced scatter in peak luminosity, are less affected by dust extinction, and provide direct access to the rest-frame optical emission of high-redshift SNe. Despite this importance, publicly available near-IR supernova datasets remain strikingly scarce compared to the wealth of optical and UV data. This gap has direct implications for ML model training: classifiers optimized on optical data alone will carry systematic biases when deployed on near-IR surveys such as Euclid and the Roman Space Telescope.

#### 5.7.1 The Scarcity of Public NIR Training Data

The primary source of real NIR photometry for SNe Ia is CSP DR3, which includes YJH-band observations for 120 of its 134 SNe (90% of the sample) [^166^]. This represents the largest homogeneous set of real NIR SN Ia light curves publicly available. However, 134 SNe is orders of magnitude smaller than the optical training sets from ZTF (hundreds of thousands of alerts) or even Swift (253 SNe with UV coverage). The next-largest real NIR dataset comes from Euclid Q1: serendipitous NISP (Near-Infrared Spectrometer and Photometer) measurements of 161 transients in the Y_E, J_E, and H_E bands (0.95–2.00 μm), obtained through single-epoch observations of the Euclid Deep Fields [^824^][^766^]. While the Q1 sample is not time-resolved, it represents the first statistically meaningful set of real NIR supernova photometry from a space-based mission and validates the detection efficiency of the NISP instrument for transient science.

#### 5.7.2 Simulated NIR Training Resources

Given the scarcity of real NIR data, simulated datasets are the primary resource for training NIR-ready classifiers. The Roman Hourglass simulation is the most comprehensive, providing 64,000+ transients across 10 types (including 21,700 SNe Ia) with simulated Y, J, H, and F band photometry at 5-day cadence, plus prism spectra for ~20% of the sample [^328^][^269^]. The Hourglass data are distributed as Parquet files on Zenodo and have already been used to train ParSNIP classifiers for Roman HLTDS science [^282^]. OpenUniverse2024 extends this with ~400 TB of matched Roman+Rubin imaging over 70 square degrees, enabling joint optical-NIR classifier development [^335^][^302^].

#### 5.7.3 Bridging the Gap: Current and Future Resources

| Source | Type | NIR Bands | SN Sample | Status | ML Limitations |
|:---|:---|:---|:---|:---|:---|
| CSP DR3 | Real | Y, J, H | 120 SNe Ia [^166^] | Publicly available | Small sample; low-z only (z<0.08) |
| Euclid Q1 | Real | Y_E, J_E, H_E | 161 transients [^824^] | Publicly available | Single-epoch; not time-resolved |
| Euclid DR1 | Real | Y_E, J_E, H_E | Projected ~5,000+ | Late 2026 | Multi-epoch; will enable proper light curves |
| Roman Hourglass | Simulated | Y, J, H, F | 21,700 SNe Ia [^328^] | Public (Zenodo) | Sim-to-real transfer required |
| OpenUniverse2024 | Simulated | Y, J, H, F | Thousands | Public (AWS S3) | Large volume (~400 TB); compute intensive |
| Roman HLTDS (2027+) | Real | Y, J, H, F | Projected 10,000s SNe Ia | Launch by May 2027 | Not yet available |
| JWST archival | Real | F090W–F444W | 53 transients [^18^] | Public (MAST) | Sparsely sampled; small area |

The near-IR data landscape presents a clear trajectory. Today, CSP DR3 and Euclid Q1 provide the only real NIR photometry suitable for ML training, but their combined sample of fewer than 300 transients is grossly inadequate for training deep learning classifiers. The Roman Hourglass simulation partially fills this gap with tens of thousands of simulated SNe Ia, yet the sim-to-real transfer problem documented in Chapter 7 means that classifiers trained purely on Hourglass data will likely experience 5–15% accuracy degradation when deployed on real Roman observations. Euclid DR1, expected in late 2026 with multi-epoch coverage over ~1,900 square degrees, will deliver the first large real NIR time-domain sample. The Roman HLTDS, launching by May 2027, is projected to discover thousands of high-z SNe Ia in the Y, J, H, and F bands with 5-day cadence, finally eliminating the NIR training gap. For ML practitioners preparing for this transition, the recommended strategy is to train classifiers jointly on Roman Hourglass (simulated NIR) and CSP DR3 (real low-z NIR), using domain adaptation techniques to bridge the simulated-to-real domain shift, and to validate on Euclid Q1/DR1 NISP photometry as the first real NIR test set at cosmological distances.


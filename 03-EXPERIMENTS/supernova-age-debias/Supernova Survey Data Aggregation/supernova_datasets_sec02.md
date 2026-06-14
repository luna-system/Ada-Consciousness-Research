## 2. Ground-based Optical & Time-Domain Surveys

Ground-based optical time-domain surveys remain the largest and most data-rich source of supernova observations for machine learning research. Operating from the Zwicky Transient Facility's (ZTF) ~47 deg² nightly footprint to the Dark Energy Survey's (DES) deep 5-year cosmological program, these facilities collectively produce millions of light curves, tens of thousands of spectroscopically classified transients, and a growing ecosystem of ML-ready data products. This chapter surveys the primary ground-based surveys, their data formats, access methods, and the specific products most relevant to ML practitioners.

### 2.1 Zwicky Transient Facility (ZTF)

#### 2.1.1 Dataset Scope and Data Releases

The Zwicky Transient Facility, operating the Palomar 48-inch telescope (P48) with a 47 deg² field of view, is the dominant open-data resource for time-domain astronomy ML. ZTF produces 5,000–10,000 extragalactic transients per year [^1^] [^2^], with 24 public data releases (DR1 through DR24) available via the NASA/IPAC Infrared Science Archive (IRSA) as of early 2026 [^3^] [^4^] [^5^]. DR14 (October 2022) contained 5.5 TB of light curves in Apache Parquet format; subsequent releases through DR24 (January 2026) have expanded this volume significantly [^3^] [^9^]. Each release includes an Objects Table (source catalog), bulk light curves, reference images, science images, and metadata [^5^]. DR20 introduced the Zubercal recalibration pipeline, addressing spatial, chromatic, and temporal photometric systematics [^44^].

The ZTF Objects Table contains positional and photometric summaries for billions of sources, partitioned in HATS (Hierarchical Adaptive Tiling Scheme) format for efficient spatial queries and available as bulk Parquet downloads [^5^]. The complete ZTF dataset encompasses more than 5 billion light curves stored in matchfile format (HDF5), though the Parquet-format DR bulk downloads are the recommended access path for ML workflows due to their native compatibility with pandas and Dask [^42^].

#### 2.1.2 Key Data Products

ZTF distributes data through multiple channels optimized for different use cases. The Avro alert stream provides real-time transient notifications at a rate of ~0.1 million alerts per night from the public stream [^1^] [^39^] [^40^]. Alert packets follow a nested Avro schema (`ztf.alert` namespace) containing the candidate detection record, 30 days of previous candidate history (`prv_candidates`), forced photometry history (`fp_hists`), and image cutouts (science, reference, and difference) [^13^] [^14^] [^15^]. The recommended Python library for reading Avro packets is `fastavro`, which is substantially faster than the standard `avro-python3` implementation [^13^].

The forced photometry service (FPS) performs fixed-position PSF photometry on all publicly available ZTF difference images, returning flux measurements critical for constructing complete light curves including non-detections [^16^] [^17^] [^18^]. The FPS accepts requests via GUI or programmatically through wget/curl with public credentials (username: `ztffps`, password: `dontgocrazy!`) [^16^]. Several Python tools automate this process: `ztffp` by Michael C. Stroh [^19^], `fpbot`/`ztffps` by Simeon Reusch [^20^] [^21^], `ForcePhotZTF` by Yuhan Yao [^22^], and `ZTF_api` by Joan Alcaide [^23^].

Zubercal provides a comprehensive recalibration of ZTF science-image PSF photometry calibrated to the PS1 photometric system, correcting spatial systematics (dust spots, CCD thickness variations, edge glints), chromatic color-dependent effects, temporal throughput variations, and atmospheric cloud extinction [^44^] [^45^] [^46^]. The DR20 Zubercal release occupies approximately 10 TB, stored as snappy-compressed Apache Parquet files in 0.5° × 0.5° spatial tiles [^44^].

**Table 1: ZTF Data Products for Machine Learning**

| Data Product | Format | Volume | Access Method | ML-Ready | Notes |
|--------------|--------|--------|---------------|----------|-------|
| DR Light Curves (bulk) | Parquet | 5–10 TB per DR | wget from IRSA; AWS S3 | Yes | Dask/pandas native; filter by `catflags` for quality [^9^] |
| Objects Table | Parquet (HATS) | ~TB scale | IRSA bulk or astroquery TAP | Yes | Spatially partitioned for efficient cone searches [^5^] |
| Zubercal (recalibrated) | Parquet | ~10 TB (DR20) | atua.caltech.edu; AWS S3 | Yes | Corrects spatial, chromatic, temporal systematics [^44^] |
| Avro Alerts | Avro | ~0.1M/night public | UW archive; 7 brokers | Yes | 30-day history + cutouts; `fastavro` for reading [^13^] [^39^] |
| Forced Photometry | ASCII | Per-object | FPS web service | Yes (after parsing) | Essential for non-detections; batch via wget/curl [^16^] |
| ZTF SN Ia DR2 | FITS/ASCII | 3,591 light curves | ztfcosmo.in2p3.fr; WISeREP | Yes | Largest spec-confirmed SN Ia sample [^24^] |
| BTS Sample | Catalog | ~11,575 objects | BTS website; TNS cross-match | Yes | 97% complete at m < 18 mag [^26^] [^27^] |
| Matchfiles | HDF5 | 5B+ light curves | Internal/IPAC access | Partial | Historical format; prefer Parquet DR downloads [^42^] |
| Reference/Science Images | FITS | Per-field/epoch | IRSA IBE API | Yes | Cutout extraction via URL parameters [^3^] [^12^] |

ZTF data is also available on the AWS Open Data Registry, where HATS Parquet catalogs enable efficient cross-match queries using the LSDB (Large Survey DataBase) library [^10^] [^11^]. The `dessndr` package and `sncosmo` library provide complementary FITS-reading capabilities for the SN Ia DR2 product. For image-based ML, the IBE API supports cutout retrieval with position and size parameters specified in the URL [^3^] [^12^].

#### 2.1.3 ZTF SN Ia DR2

ZTF SN Ia DR2 is the largest spectroscopically confirmed Type Ia supernova dataset ever assembled, containing 3,591 SNe Ia light curves in g, r, and i bands with 5,138 individual spectra (at least one per SN Ia), host galaxy data tables (global and local 2 kpc aperture properties), and SALT2.4/SALT3 light curve fit parameters [^24^] [^25^]. The sample includes a volume-limited subset of approximately 1,200 SNe Ia at z < 0.06 that is unique for population studies [^25^]. Light curves were fitted with SALT2.4 with Taylor et al. (2023) retraining to extract stretch (x₁) and color (c) parameters [^25^]. Host galaxy tables include rest-frame g−z color, stellar mass log(M*/M⊙) in both local 2 kpc and global apertures, host coordinates, and redshifts (available for 60% of the volume-limited sample) [^24^] [^25^]. Data tables are available at https://ztfcosmo.in2p3.fr and through WISeREP [^24^].

#### 2.1.4 BTS (Bright Transient Survey)

The ZTF Bright Transient Survey (BTS) is the largest spectroscopic supernova survey conducted to date, providing a magnitude-limited (m < 19 mag in g or r), nearly complete spectroscopic sample of extragalactic transients [^26^] [^27^] [^28^]. As of 2024, BTS has spectroscopically classified 11,575 transients brighter than 19 mag, of which 11,427 are supernovae and 148 are other transient types [^26^] [^27^]. Spectroscopic completeness is 97% at m < 18 mag, 93% at m < 18.5 mag, and 75% at m < 19 mag [^26^] [^27^]. Every transient brighter than 18.5 mag is followed with the Spectral Energy Distribution Machine (SEDM) on the Palomar 60-inch telescope [^26^]. BTS-I (Fremling et al. 2020) described the survey design [^28^]; BTS-II (Perley et al. 2020) presented 4,095 transients with classifications, host associations, and demographic measurements [^27^]. Classifications are announced nightly via the Transient Name Server (TNS) [^26^]. BTS has also enabled precise measurement of relative SN rates: approximately 7% of core-collapse SNe explode in very low-luminosity galaxies (Mᵢ > −16), approximately 10% in red-sequence galaxies, and approximately 1% in massive ellipticals [^28^]. These demographic measurements provide important prior distributions for ML classifiers. BTS-specific forced photometry processing code is available on GitHub for generating flux-calibrated photometry from the ZTF FPS for all BTS transients observed from 2018–2020 [^29^].

#### 2.1.5 Python Access to ZTF Data

The `ztfquery` package by Mickael Rigault and Simeon Reusch is the most comprehensive Python interface for ZTF data access, providing a wrapper around the IRSA web API for querying and downloading images, pipeline products, catalogs, light curves, observing logs, and marshal data [^30^] [^31^]. For image processing, `ztfimg` offers a dask-native, object-oriented API supporting operations at quadrant, CCD, and focal-plane levels with source extraction via `sep` [^32^] [^33^]. The `ztf-dr` package (ALeRCE) enables parallel downloading of any ZTF DR ≥ DR5 to S3-compatible storage with configurable worker processes [^34^]. The `alerce` Python client provides multi-survey access to ZTF and LSST data with ML classifications from the ALeRCE broker [^35^], while the `lasair` client interfaces with the Lasair broker for Sherlock cross-matches and TNS information [^36^].

IRSA TAP queries via `astroquery` provide a standard VO interface for catalog searches. The following pattern illustrates a typical cone search on the ZTF Objects Table:

```python
from astroquery.ipac.irsa import Irsa
from astropy.coordinates import SkyCoord
import astropy.units as u

coord = SkyCoord(ra=298.0025, dec=29.87147, unit='deg', frame='icrs')
table = Irsa.query_region(coordinates=coord, spatial='Cone',
                          catalog='ztf_objects_dr20', radius=5*u.arcsec)
```

For complex queries, TAP/ADQL supports full SQL syntax against the ZTF catalog. Bulk light curve downloads use `wget` against the IRSA Parquet directory structure organized by field (e.g., `https://irsa.ipac.caltech.edu/data/ZTF/lc/lc_dr20/`), with Dask or PyArrow for subsequent reading [^9^]. Light curve columns include `objectid`, `filterid` (1=g, 2=r, 3=i), `fieldid`, `hmjd`, `mag`, `magerr`, and `catflags`—the latter should be filtered to exclude `catflags = 32768`, which indicates cloudy or moon-affected observations [^9^].

The ZTF Alert Archive at the University of Washington (https://ztf.uw.edu/alerts/public/) hosts nightly summaries and historical Avro packets [^39^]. Seven community alert brokers (ALeRCE, Lasair, Fink, ANTARES, AMPEL, MARS, and Pitt-Google) process ZTF alerts and distribute them with real-time ML classifications [^40^]. ALeRCE provides light curve and stamp classifiers with an F1 score of 0.97 for the light curve classifier and 100% SN completeness at the operating point [^47^] [^50^]; Lasair offers Sherlock cross-matches with archival sources and TNS classifications [^36^]; Fink specializes in multi-messenger and early-phase SN detection. For many ML projects, querying broker APIs may be more efficient than downloading raw data and training from scratch, particularly for real-time applications where brokers amortize compute costs across the community.

### 2.2 Pan-STARRS1 Medium Deep Survey (PS1-MDS)

The Pan-STARRS1 Medium Deep Survey covered 10 fields (70 deg²) in 5 bands (grizy) over 4 years (2010–2014), discovering approximately 5,200 likely supernovae [^133^] [^134^]. Of these, 365 were spectroscopically confirmed SNe Ia spanning redshifts 0.03 < z < 0.68 [^133^]. The PS1 filter system (g_P1, r_P1, i_P1, z_P1, y_P1) provides excellent photometric calibration with 7–12 mmag stability [^507^], and the survey cadence of approximately 6 observations per 10 days per field approximates the observing pattern anticipated for the Rubin Observatory [^440^].

The 279 PS1 SNe Ia with the most precise distance estimates formed the backbone of the Pantheon compilation (Scolnic et al. 2018), which combined PS1, SDSS, SNLS, low-z, and HST samples into 1,048 SNe Ia for cosmology [^133^]. Jones et al. (2018) expanded this to 1,169 SNe Ia using photometric classifications, achieving a constraint of w = −0.989 ± 0.057 [^440^].

PS1 catalog data is accessed through the MAST CasJobs SQL interface (https://mastweb.stsci.edu/ps1casjobs), which provides full SQL query access to the PS1 catalog database with synchronous and asynchronous execution modes [^21^]. The MAST Portal (https://catalogs.mast.stsci.edu/) supports cone searches, catalog queries, and image cutout retrieval. ML practitioners working with PS1 data should note that Villar et al. (2020) published SuperRAENN photometric classifications for 5,243 PS1 "SN-like" light curves, achieving 87% accuracy across 5 classes (Type Ia: 62.0%, Type II: 19.8%, Type IIn: 4.8%, Type Ibc: 11.7%, SLSN-I: 1.6%) [^441^]. The PS1 calibration system achieves sub-1% relative precision across 3π steradians using the Supercal method [^134^], making PS1-MDS data particularly valuable for training classifiers where photometric consistency across fields is essential. The `sndata` Python package provides programmatic access to PS1-MDS light curves in a standardized format compatible with `sncosmo` [^409^]. For ML applications requiring high-redshift SNe Ia, PS1-MDS offers the largest spec-confirmed sample between z = 0.3 and z = 0.7 of any publicly available survey.

### 2.3 Dark Energy Survey (DES)

#### 2.3.1 DES-SN 5-Year Data Release

The Dark Energy Survey Supernova Program (DES-SN) used the Dark Energy Camera (DECam) on the Blanco 4-meter telescope at Cerro Tololo Inter-American Observatory (CTIO) to conduct a 5-year rolling search for supernovae, producing the largest single-instrument sample of cosmological SNe Ia ever assembled [^342^] [^350^]. The DES-SN5YR data release, published in 2024, contains 31,636 Difference Image (DiffImg) light curves and 19,706 Scene Modeling Photometry (SMP) light curves, of which 1,635 photometrically classified SNe Ia pass cosmology quality cuts over the redshift range 0.10 < z < 1.13 [^342^] [^350^] [^395^].

The DiffImg pipeline uses forced PSF photometry on difference images with deep template images from science verification, achieving approximately 2% photometric precision but with known limitations in tertiary star photometry and proper motion corrections [^394^] [^395^]. The SMP pipeline applies forward-modeling photometry that simultaneously fits time-varying SN flux and static host galaxy flux, using individual reference images selected for best quality, updated Y6 forward model calibration, and per-filter differential chromatic refraction (DCR) corrections. SMP achieves smaller scatter about SALT3 model fits across all bands and redshift ranges, increasing the cosmology sample from 1,499 (DiffImg) to 1,635 (SMP) [^395^] [^400^].

#### 2.3.2 Data Format and Access

DES-SN5YR data is distributed in SNANA FITS format through both GitHub (https://github.com/des-science/DES-SN5YR) and Zenodo (DOI: 10.5281/zenodo.12720777) [^344^] [^477^]. The release totals approximately 1.5 GB and includes seven top-level directories: `0_DATA/` (light curves), `1_SIMULATIONS/` (25 mock simulations), `2_LCFIT_MODEL/` (SALT3 models), `3_CLASSIFICATION/` (classification probabilities), `4_DISTANCES_COVMAT/` (Hubble diagram data), `5_COSMOLOGY/` (MCMC chains), `6_DCR_CORRECTIONS/`, and `7_PIPPIN_FILES/` (pipeline reproduction inputs) [^344^].

Light curves are stored as paired HEAD and PHOT FITS files. The HEAD file contains one row per SN with metadata including coordinates, redshifts, host galaxy properties (stellar mass log(M*/M⊙), star formation rate, ugrizY magnitudes, surface brightness at SN location), and pointers to the PHOT file. The PHOT file contains individual photometric observations with calibrated flux (FLUXCAL, where mag = 27.5 − 2.5·log₁₀(FLUXCAL)), flux uncertainties, PSF parameters, and quality flags [^439^]. Python access is straightforward via `sncosmo.read_snana_fits()` or the `dessndr` utility package, which provides convenience functions for loading photometry and classification data [^413^] [^485^].

#### 2.3.3 Mock Simulations and Systematic Testing

The DES-SN5YR release includes 25 statistically independent mock simulations, each containing SNANA FITS files with both SNe Ia and core-collapse SNe generated using the SALT3 SED model [^456^]. These simulations assume a flat ΛCDM cosmology (H₀ = 70.0 km/s/Mpc, ΩΛ = 0.685, ΩM = 0.315, w₀ = −1.0, wa = 0.0) and incorporate realistic observing conditions including detection efficiencies from Kessler et al. (2019), spectroscopic redshift efficiencies from Vincenzi et al. (2022), and host galaxy libraries from Qu et al. (2024) [^456^] [^475^]. The 25 simulations are critical for ML applications: they enable training of photometric classifiers (SuperNNova, SCONE, SNIRF), computation of BEAMS with Bias Correction (BBC) corrections, and validation of the full cosmological pipeline. The input cosmology is recovered to within 1σ for both Ωm and w when the full analysis pipeline is applied to each simulation [^396^].

The 1,635 cosmology-grade SNe Ia were classified primarily using SuperNNova (SNN), a recurrent neural network trained on >100,000 realistic DES-like simulations [^551^] [^258^]. Of the 1,635 SNe, 1,499 (91%) have SNN classification probability P(Ia) > 0.5 [^537^]. Classification probabilities from multiple algorithms (SNN, SCONE, SNIRF) are provided in the `3_CLASSIFICATION/` directory, enabling cross-classifier comparison and systematic uncertainty estimation [^413^].

### 2.4 Other Active Ground-based Surveys

#### 2.4.1 ASAS-SN

The All-Sky Automated Survey for SuperNovae (ASAS-SN) uses a network of 14-cm telescopes to image the entire visible sky nightly to g ~ 18.5 mag. ASAS-SN is not primarily a cosmological survey—its shallow depth limits it to nearby events—but it provides the most complete catalog of bright supernovae available. The ASAS-SN Bright Supernova Catalog (Neumann et al. 2022, Catalog V) contains 2,427 total SNe, complete to m_peak = 16.7 mag in g-band [^10^]. The survey is approximately 90% complete at m_peak ≤ 17.0 mag [^10^]. Public photometry for more than 100 million targets is available through the ASAS-SN Sky Patrol interface (https://asas-sn.ifa.hawaii.edu/), which supports ADQL queries and the `pyasassn` Python API [^15^]. The catalog includes classifications, host galaxy identifications with UV-to-mid-IR photometry, and redshifts, making it directly usable for ML training of bright-transient classifiers.

#### 2.4.2 SkyMapper

The SkyMapper Transient Survey (SMT) uses the 1.3-meter SkyMapper telescope at Siding Spring Observatory to survey the Southern sky in ugriz filters, with a focus on low-redshift SNe Ia [^65^] [^154^]. SkyMapper DR1 was released in 2018 and covers the Southern Survey region, which overlaps with the DES footprint. SN data from SkyMapper is accessible through a Table Access Protocol (TAP) interface and cross-matched with TNS. The survey targets approximately 400–600 galaxies per night and has published early data releases for transient science [^154^]. Scalzo et al. (2017) described the SMT survey design and its role as a low-z SN Ia hunter in the Southern hemisphere [^65^].

#### 2.4.3 OGLE

The Optical Gravitational Lensing Experiment (OGLE) is a long-running microlensing survey using the 1.3-meter Warsaw telescope at Las Campanas Observatory. While OGLE's primary science focus is gravitational microlensing in the Galactic Bulge, the survey's time-series photometry in V and I bands has yielded serendipitous supernova detections, particularly in the Magellanic Clouds and along high-extinction lines of sight [^208^] [^211^]. OGLE data is distributed through an FTP server and database query interface at https://ogle.astrouw.edu.pl [^208^]. The OGLE-IV transient detection system (http://ogle.astrouw.edu.pl/ogle4/transients/) publishes transient candidates in real time, including some extragalactic transients, though OGLE is not a primary SN survey for ML applications.

#### 2.4.4 Young Supernova Experiment (YSE)

The Young Supernova Experiment (YSE) operated from 2019–2021 using Pan-STARRS2 and ZTF to discover and classify young supernovae in their earliest phases. YSE DR1 (Aleo et al. 2023) contains 1,975 transients, of which 492 were spectroscopically classified and 1,483 photometrically classified using the ParSNIP variational autoencoder [^71^] [^402^]. ParSNIP achieves 82% accuracy across 3 classes (Ia, II, Ib/c) and >90% completeness and purity for SNe Ia on the spectroscopic test set [^282^]. The photometric sample contains 1,048 SNe Ia (~71%), 339 SNe II (~23%), and 96 SNe Ib/c (~6%) [^282^]. Data is available from Zenodo (DOI: 10.5281/zenodo.7317476) in SNANA HEAD+PHOT format, with ParSNIP classification results provided as CSV tables [^68^]. The YSE DR1 Tutorial GitHub repository demonstrates data loading, metadata extraction, and figure reproduction [^530^]. YSE's emphasis on early-phase observations makes it particularly valuable for training classifiers designed to operate on pre-peak light curves.

### 2.5 Legacy Ground-based Surveys

#### 2.5.1 SDSS-II SN Survey

The Sloan Digital Sky Survey-II Supernova Survey (2005–2007) repeatedly imaged Stripe 82 (300 deg² along the celestial equator) to discover and monitor SNe. The full data release (Sako et al. 2018) contains 10,258 variable and transient sources, including 4,607 SN candidates and 1,443 SNe Ia with spectroscopic redshifts and SALT2 distance moduli [^132^] [^135^]. An additional 677 purely photometric SNe Ia candidates with photometric redshifts are included. The survey used ugriz filters with a cadence of every other night for approximately 3 months per year over 3 years, reaching r ~ 22.5 mag and covering redshifts 0.05 < z < 0.4 (median z ~ 0.2) [^132^]. Data is available via the SDSS Science Archive Server in FITS and ASCII formats and is integrated into SNANA, `sncosmo`, and `sndata` [^53^] [^54^]. SDSS-II remains one of the most frequently used training datasets for SN classification ML due to its large, homogeneous sample with both spectroscopic and photometric classifications.

#### 2.5.2 SNLS

The SuperNova Legacy Survey (SNLS) was a 5-year program using the MegaCam imager on the Canada-France-Hawaii Telescope (CFHT) to discover and monitor approximately 500 Type Ia SNe for dark energy studies. SNLS3 (Guy et al. 2010) presented 231 SNe Ia that, combined with 123 low-z and 101 SDSS SNe, produced 495 SNe Ia for cosmology [^105^]. The final SNLS5 sample added additional SNe, bringing the total to approximately 400 SNe Ia from SNLS alone [^105^]. Spectroscopic observations from ESO/VLT (Balland et al. 2009) provided 139 spectra of 124 SNe Ia at z = 0.149–1.031 [^55^] [^57^]. SNLS data in u*g'r'i'z' filters is available through CDS/VizieR and the `sndata` Python package [^57^]. The CFHT Legacy Survey reference images and <1% precision photometric calibration (T0007 release) [^49^] make SNLS data well-suited for ML classification training, though access requires familiarity with CDS query services.

#### 2.5.3 ESSENCE

The Equation of State: SupErNovae trace Cosmic Expansion (ESSENCE) survey operated from 2002–2007 using the CTIO 4-meter Blanco telescope to discover approximately 200 Type Ia SNe at z ~ 0.5, designed to constrain the dark energy equation-of-state parameter w. The first cosmological results yielded w = −1.05 ± 0.13 [^17^] [^19^]. ESSENCE used primarily R and I filters with a cadence optimized for z ~ 0.5 SNe Ia. Spectroscopic data (FITS format) is available through the ESO Science Archive (Phase 3), and photometric light curves are accessible via VizieR [^17^]. With 102 spectroscopically confirmed SNe Ia in the first 4 years (z = 0.10–0.78) [^17^], ESSENCE is now most frequently encountered as a component of compilation datasets such as JLA and Pantheon+ rather than as a standalone ML training resource.

#### 2.5.4 PTF/iPTF

The Palomar Transient Factory (PTF) and its intermediate successor iPTF operated the same Palomar 48-inch telescope used by ZTF from 2009–2017, discovering thousands of SNe in g and R bands [^69^] [^76^]. Three data releases (DR1–DR3) are available through IPAC (https://www.ipac.caltech.edu/programs/ptf/), with an 18-month proprietary period followed by public release [^69^]. PTF/iPTF light curves were instrumental in developing early photometric classification methods: the Superphot training set used 518 spectroscopically classified PTF SNe across 5 classes [^13^], and Price-Whelan et al. (2014) published a sample of 10,000 light curves for variability studies. Spectra from PTF/iPTF are archived in WISeREP. While superseded by ZTF in both cadence and data volume, PTF/iPTF remains a valuable historical resource for training classifiers on pre-ZTF data and for studying long-term transient population evolution.

### 2.6 Comparison and Selection Guidance

#### 2.6.1 Survey Comparison Table

**Table 2: Ground-based Optical Survey Comparison for ML Applications**

| Survey | Years | SNe Ia Count | All Filters | Cadence | z Range | Primary Data Access |
|--------|-------|-------------|-------------|---------|---------|-------------------|
| ZTF | 2018–present | 3,628 spec-Ia (DR2) [^24^] | gri | ~3 days (g,r) | 0.01–0.3 | IRSA TAP; ztfcosmo.in2p3.fr; AWS S3 |
| PS1-MDS | 2010–2014 | 365 spec-Ia [^133^] | grizy | ~6 obs/10 days | 0.03–0.68 | MAST CasJobs; VizieR; sndata |
| DES-SN5YR | 2013–2018 | 1,635 photo-Ia [^342^] | griz | ~weekly rolling | 0.10–1.13 | GitHub; Zenodo; sncosmo |
| ASAS-SN | 2014–present | 2,427 total SNe [^10^] | g (later V) | nightly (all-sky) | <0.05 | Sky Patrol web; pyasassn API |
| YSE DR1 | 2019–2021 | ~1,048 photo-Ia [^282^] | griz + ZTF gr | variable | 0.01–0.5 | Zenodo; GitHub tutorials |
| SDSS-II | 2005–2007 | 1,443 spec-Ia [^132^] | ugriz | ~2 days | 0.05–0.4 | SDSS SAS; SNANA; sndata |
| SNLS | 2003–2008 | ~400 spec-Ia [^105^] | u*g'r'i'z' | ~3–4 days | 0.1–1.0 | CDS/VizieR; sndata |
| ESSENCE | 2002–2007 | ~200 spec-Ia [^17^] | R, I | optimized for z~0.5 | 0.2–0.8 | ESO archive; VizieR |
| PTF/iPTF | 2009–2017 | 518 spec-Ia (Superphot) [^13^] | g, R | ~3–5 days | 0.01–0.3 | IPAC archive; WISeREP |
| SkyMapper | 2014–present | ~30+ SNe Ia (early) [^65^] | ugriz | nightly (Southern) | <0.1 | TAP interface; TNS cross-match |

The table reveals a clear stratification by survey depth and scientific purpose. Shallow, wide-field surveys (ASAS-SN, ZTF) dominate the low-redshift discovery space with thousands of bright events, while deep, field-focused surveys (DES, PS1-MDS) provide the high-redshift cosmological samples essential for constraining dark energy evolution. For ML practitioners, the choice of survey depends critically on the target task: ZTF SN Ia DR2 offers the largest homogeneous spec-confirmed training sample; DES-SN5YR provides the richest multi-band photometric classification set with 25 accompanying simulations; ASAS-SN delivers the most complete bright-transient catalog; and YSE DR1 specializes in early-phase pre-peak observations. Legacy surveys (SDSS-II, SNLS, ESSENCE, PTF/iPTF) remain valuable for cross-survey generalization testing and for benchmarking classifier performance against established literature results.

#### 2.6.2 Data Access Methods Summary

**Table 3: Programmatic Data Access Methods for Ground-based Surveys**

| Survey | Primary Interface | Python Package | Query Language | Bulk Download | Authentication |
|--------|------------------|----------------|----------------|---------------|----------------|
| ZTF | IRSA TAP; AWS S3 | `astroquery.ipac.irsa`; `ztfquery`; `alerce` | ADQL/TAP; Python API | wget (Parquet) | Free IRSA account |
| PS1-MDS | MAST CasJobs | `sndata` (via `sncosmo`) | SQL | Web/API | Free MAST account |
| DES | GitHub; Zenodo | `dessndr`; `sncosmo` | — | git clone; wget | None |
| ASAS-SN | Sky Patrol | `pyasassn` | ADQL; Python API | Web; API | None |
| YSE | Zenodo | `sncosmo` | — | wget (tar.gz) | None |
| SDSS-II | SAS; SNANA | `sndata`; `sncosmo` | SQL (CasJobs) | wget; rsync | Free for DR |
| SNLS | CDS/VizieR | `sndata` | SQL (VizieR) | Web download | None |
| PTF/iPTF | IPAC | `ztfquery` (historical) | Web form | wget; web | None (public DR) |

The access landscape has converged substantially since 2020. The `sncosmo`/`sndata` ecosystem now provides a unified Python interface for SDSS-II, SNLS, CSP, and Foundation data, while `ztfquery` and broker clients (ALeRCE, Lasair, Fink) cover the ZTF alert and archive space. For surveys not yet integrated into these packages, TAP/ADQL services (IRSA, MAST, VizieR) offer standards-compliant query interfaces that work with `astroquery` or generic HTTP clients. The emergence of cloud-native distribution—ZTF on AWS S3, DES on GitHub/Zenodo—has dramatically lowered the barrier to bulk data access for ML workflows. A persistent challenge remains the "format tower of Babel": ZTF alerts use Avro, ZTF DR light curves use Parquet, DES uses SNANA FITS, SDSS-II uses FITS/ASCII, and legacy surveys use heterogeneous ASCII formats. ML practitioners should plan for a format normalization stage early in their pipeline development, as the time invested in unified data ingestion typically rivals the time spent on model architecture design.

For real-time applications, the seven ZTF alert brokers provide pre-computed ML classifications and cross-matches with TNS, enabling feature extraction without downloading raw alert packets [^40^]. For historical analysis, the bulk Parquet downloads from IRSA offer the most efficient path to large-scale ZTF light curve datasets, with Dask providing out-of-core computation for the multi-terabyte DR volumes. The DES-SN5YR GitHub repository stands as the most complete self-contained data release, bundling light curves, 25 simulations, classifications from three independent algorithms, and full cosmology reproduction pipelines in a single documented package [^344^].

When selecting a survey for a specific ML task, practitioners should consider three primary factors: sample size and class balance (ZTF leads for spec-confirmed SNe Ia; DES leads for photometrically classified high-z SNe Ia), redshift coverage (ASAS-SN and YSE for z < 0.05; DES for z > 0.5), and data completeness (forced photometry availability, non-detection upper limits, and host galaxy metadata). For training photometric classifiers intended for Rubin-era deployment, DES-SN5YR's 25 mock simulations offer the most realistic simulated training environment currently available, with input cosmology recoverable to within 1σ—providing a critical validation ground for simulation-to-reality transfer methods [^456^] [^396^].

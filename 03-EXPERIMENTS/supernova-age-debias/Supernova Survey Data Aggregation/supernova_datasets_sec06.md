## 6. Compilation & Aggregated Datasets

Individual survey releases provide the raw material for supernova machine learning, but the field has matured through a parallel ecosystem of homogenized compilations that aggregate data from dozens of sources into analysis-ready collections. These compilations serve three distinct ML purposes: cosmology regression (distance modulus prediction), classification (type labeling across all supernova species), and anomaly detection (outlier discovery in heterogeneous populations). This chapter examines the principal compilations — from the all-inclusive Open Supernova Catalog to the precision-calibrated Pantheon+ sample — and provides a practical workflow for constructing unified training sets from multi-survey data.

### 6.1 Open Supernova Catalog

#### 6.1.1 Scope and Content

The Open Supernova Catalog (OSC) is the most comprehensive open repository for supernova data, containing **50,000+ supernovae and candidates** aggregated from several dozen sources including the astronomical literature, survey data releases, and secondary catalogs [^651^] [^659^]. Unlike the cosmology-focused compilations described later in this chapter, the OSC embraces supernovae of all types — thermonuclear (Type Ia), core-collapse (Type II, Ib, Ic, and subtypes), and exotic variants — alongside non-supernova contaminants such as active galactic nuclei (AGN) and stellar variables. This diversity makes it uniquely valuable for multi-class classification and anomaly detection tasks, even as it introduces significant data-quality heterogeneity.

The catalog stores data in a hierarchical JSON format with one file per supernova [^86^]. Each file contains photometric time series (when available), spectroscopic observations, metadata (coordinates, redshift, host galaxy association), and cross-references to discovery circulars. Approximately 12,000 objects have more than 10 photometric observations, while roughly 5,000 include at least one spectrum [^81^]. The remaining entries consist primarily of metadata-only records with discovery information and classification claims.

#### 6.1.2 Bulk Download and Repository Access

The OSC data are distributed through a GitHub organization (astrocatalogs) split across year-based repositories to accommodate GitHub's repository size limits [^89^]. Individual event JSON files are organized into repositories covering: pre-1990, 1990–1999, 2000–2004, 2005–2009, 2010–2014, 2015–2019, and 2020–present. For bulk acquisition, the most efficient path is a compressed tarball (sne.tar.lzma, 379 MB) available via the SNAD project mirror at snad.space [^81^] [^661^]. This archive contains all JSON files as a single download, avoiding the overhead of cloning multiple GitHub repositories.

#### 6.1.3 Programmatic Queries

For targeted queries, the AstroCats API (api.astrocats.space) supports programmatic access to individual supernova records without requiring a local mirror. The underlying AstroCats framework can also be installed locally for full catalog reproduction, though the initial import run requires approximately one day of processing time. For ML workflows that require the full catalog, parsing the JSON files directly is straightforward:

```python
import json, glob
for json_file in glob.glob('sne-*/SN*.json'):
    with open(json_file) as f:
        sn_data = json.load(f)
    photometry = sn_data.get('photometry', [])
    spectra = sn_data.get('spectra', [])
    claimed_type = sn_data.get('claimedtype', [])
```

The SNooPy light-curve fitting package can also import OSC data directly, providing an alternative entry point for researchers already using that tool.

#### 6.1.4 Strengths and Weaknesses for ML

The OSC's principal strength for ML lies in its scale and diversity. No other compilation matches its breadth of supernova types, making it the default choice for classification tasks that must distinguish between thermonuclear and core-collapse events or identify rare subtypes. The catalog has been successfully used for automated anomaly detection: the SNAD pipeline downloaded 45,162 objects from a 2018 snapshot, selected approximately 2,000 with sufficient photometry, and applied Gaussian Process interpolation followed by t-SNE dimensionality reduction and Isolation Forest outlier detection, identifying 81 anomalies of which 27 were confirmed as peculiar supernovae, AGN, or stellar variables [^690^] [^694^].

The corresponding weakness is data heterogeneity. Photometric observations come from hundreds of different telescopes and instruments with inconsistent calibration, filter definitions, and reporting formats. Many objects have sparse time sampling with fewer than 5 photometric points, making light-curve fitting unreliable. No uniform quality flags exist, so ML practitioners must implement their own filtering criteria — typically requiring a minimum number of observations, signal-to-noise thresholds, and coverage in multiple photometric bands.

### 6.2 Pantheon+

#### 6.2.1 Sample Definition and Survey Coverage

Pantheon+ represents the definitive cosmological supernova compilation, comprising **1,701 light curves of 1,550 distinct Type Ia supernovae** drawn from **18 different surveys** spanning three decades [^451^]. The sample was assembled by the SH0ES (Supernovae and H0 for the Equation of State of dark energy) collaboration specifically for precision cosmology, combining low-redshift anchors (z < 0.1) from the Carnegie Supernova Project and CfA surveys, intermediate-redshift SNe from SDSS-II, and high-redshift events from SNLS, DES, and HST programs. The primary analysis papers are Scolnic et al. 2022 (ApJ 938:110) and Brout et al. 2022 (ApJ 938:111) [^451^] [^536^].

The repository is organized into 18 survey-specific subdirectories, each containing light-curve files in both SNANA text format and FITS binary tables [^125^] [^662^]. The text format places metadata (supernova name, coordinates, host galaxy position, Milky Way extinction, heliocentric and CMB-frame redshifts, peculiar velocity) in a header block, followed by photometric data columns (MJD, filter, calibrated flux, flux uncertainty, magnitude, magnitude uncertainty). All flux measurements share a common zero-point of 27.5 mag, enabling direct comparison across surveys.

#### 6.2.2 Cosmology Data Products and Covariance Matrices

Beyond raw photometry, Pantheon+ provides the essential data products for cosmological ML. The 4_DISTANCES_AND_COVAR directory contains the primary distance moduli and redshifts in Pantheon+SH0ES.dat, along with a full statistical-plus-systematic covariance matrix in compressed format [^664^]. Light-curve fit results from SALT2/SALT3 are available as .FITRES files, and calibration variation files enable systematic uncertainty studies. Host galaxy properties — stellar mass for the full sample, plus star formation rate and morphology for the low-redshift subset — are included as global metadata.

The covariance matrix construction is documented in a third-party analysis repository, which includes a demonstration notebook (how_to_covariance.ipynb) showing proper matrix usage in Python [^452^]. For ML practitioners, these covariance matrices enable principled treatment of correlated uncertainties in loss functions — a significant advantage over compilations that provide only point estimates.

#### 6.2.3 Calibration Evolution: SuperCal to Dovekie

Pantheon+ has undergone three generations of cross-calibration. The original SuperCal methodology (2015) tied 25 photometric systems using Pan-STARRS stellar photometry [^508^]. This was superseded by Fragilistic in the Pantheon+ analysis, which simultaneously solved for 105 filter offsets with an associated covariance matrix [^536^]. The most recent update, Dovekie (2025), provides an open-source recalibration framework using DA white dwarfs and Gaia photometry; Dovekie found systematic photometric uncertainty of 0.016 mag for a flat wCDM cosmology, improving the Pantheon+ calibration systematic by a factor of approximately 1.5 [^706^]. The Dovekie code is publicly available at github.com/bap37/Dovekie, making it possible for researchers to add new surveys to the cross-calibration framework — a critical capability as new data from ZTF, Rubin, and other facilities become available.

#### 6.2.4 ML Applications

For machine learning, Pantheon+ is best suited to cosmology regression tasks: predicting distance modulus from redshift, light-curve shape, and color; quantifying standardization residuals; and propagating systematic uncertainties through the inference pipeline. The pre-homogenized nature of the sample means it is **not** suitable for raw classification tasks — the objects have already been spectroscopically confirmed as Type Ia and quality-selected for cosmology. However, the covariance matrices and calibration documentation make it uniquely powerful for uncertainty-aware ML, where correlated errors must be propagated into model predictions.

### 6.3 Union3 and UNITY1.5

Union3 is the latest compilation from the Supernova Cosmology Project (SCP), comprising **2,087 Type Ia supernovae from 24 distinct datasets** — approximately one-third larger than Pantheon+ [^189^]. The sample is analyzed with the UNITY1.5 (Unified Nonlinear Inference for Type-Ia cosmologY) Bayesian hierarchical framework [^624^], which represents a fundamentally different statistical approach than the frequentist methodologies used in Pantheon+.

#### 6.3.1 Bayesian Framework and Data Products

UNITY1.5 implements a Bayesian hierarchical model using Hamiltonian Monte Carlo via Stan [^623^] [^626^]. The framework simultaneously models outlier contamination, selection effects (Malmquist bias), light-curve shape and color populations, standardization relations, and unexplained dispersion. A distinctive feature is that it models the underlying supernova population *before* selection effects are applied, then marginalizes over survey depth distributions — in contrast to traditional approaches that apply selection corrections post-hoc. The framework also recovers peculiar velocity fields, providing a posterior distribution for every model parameter.

#### 6.3.2 Data Availability and Access

As of early 2025, the full unbinned Union3 catalog has **not** been publicly released [^658^]. Only binned or compressed data products are available: spline-interpolated distance moduli at 22 redshift nodes, a Gaussian approximation to the posterior (location plus Hessian), and the UNITY1.5 framework code for forward-modeling. The binned release is hosted at github.com/rubind/union3_release, with an alternative access point through the Cobaya sampler's sn_data repository [^657^] [^658^].

This data availability pattern has important implications for ML. The binned format precludes per-supernova analysis — individual light curves, SALT3 fit parameters, and distance estimates are not directly accessible. Instead, cosmological constraints must be derived by implementing custom models within the UNITY framework. The full catalog release, which will include individual supernova data and SALT3 fitted parameters, is anticipated in future updates; ML practitioners should monitor the GitHub repository for releases.

### 6.4 JLA

The Joint Light-Curve Analysis (JLA) combines SDSS-II and SNLS Type Ia supernova observations with low-redshift samples, totaling **740 spectroscopically confirmed SNe Ia** with high-quality light curves [^652^]. Published by Betoule et al. 2014, JLA was the standard cosmology compilation for the decade preceding Pantheon+ and remains widely used for method validation and teaching.

Data access is available through CDS/VizieR at J/A+A/568/A22, with covariance matrices distributed as a separate compressed archive [^452^]. The SNData Python package provides programmatic access via the `Betoule14` module [^652^], which handles download, caching, and format conversion automatically. JLA uses SALT2.4 light-curve fitting (superseded by SALT3 in Pantheon+) and calibration based on the SuperCal methodology (later improved by Fragilistic and Dovekie). Both JLA and Pantheon+ employ the Tripp estimator standardization: mu = mB + alpha*x1 - beta*c - M0, though with different training samples and priors.

For ML research, JLA offers two practical advantages over its successors. First, the smaller dataset size (740 vs. 1,701 SNe) and simpler structure make it ideal for rapid prototyping and teaching — a full cosmology analysis pipeline can be executed in minutes rather than hours. Second, the well-documented covariance construction and extensive validation literature provide a reliable baseline against which new ML methods can be benchmarked. The principal caveat is that JLA's photometric calibration has been superseded; cosmology results will differ systematically from Pantheon+ by calibration offsets that must be accounted for in any cross-compilation analysis.

### 6.5 Other Compilations

Beyond the four major compilations described above, several additional catalogs serve specialized roles in the ML ecosystem.

#### 6.5.1 Asiago Catalog

The Asiago Supernova Catalog is the longest-running dedicated supernova catalog, maintaining records for all supernovae observed since 1885 along with their parent galaxies [^593^] [^596^]. The dynamic version supersedes the 1999 publication by Barbon et al. and is updated regularly. Data are available through CDS (cdsarc.cds.unistra.fr/ftp/cats/B/sn) and mirrored by HEASARC at NASA's Goddard Space Flight Center [^142^] [^596^]. The catalog contains over 11,000 supernova entries with host galaxy identifications, redshifts, classification types, and cross-references to International Astronomical Union Circulars (IAUCs). Parent galaxy properties are homogenized across multiple source catalogs (RC3, UGC, PGC, MCG, ESO). For ML applications, the Asiago Catalog is primarily useful for host galaxy correlation studies and metadata enrichment — it contains minimal photometric data but provides authoritative host identifications that can be cross-matched with survey photometry.

#### 6.5.2 Sternberg Astronomical Institute Catalog

The Sternberg Astronomical Institute (SAI) Catalog contains 2,991 extragalactic supernovae discovered from 1885 through December 2004, with host galaxy data compiled from multiple astronomical catalogs [^354^]. Available through the NASA Data Portal and CDS Table II/256, this is a static catalog that has not been updated since 2004. Its primary value lies in historical completeness for the pre-digital era; for contemporary ML work, the Asiago dynamic catalog or OSC provide superior coverage.

#### 6.5.3 DES-SN5YR and CSP

The DES-SN5YR sample from the Dark Energy Survey comprises approximately 1,820 SNe Ia used in cosmological analysis [^344^]. The recent DES-Dovekie reanalysis provides updated calibration and SALT3 model retraining (SALT3.DOVEKIE and SALT3.DOVEKIE-SYS) [^475^]. The repository at github.com/des-science/DES-SN5YR includes scene-modeling photometry, 25 mock simulations, classification probabilities for 1,635 SNe, and distance covariance matrices. For photometric classification tasks, the DES sample offers deep, well-characterized photometry alongside extensive simulation-based training data.

The Carnegie Supernova Project (CSP) provides some of the highest-precision low-redshift photometry available, with DR3 containing 134 SNe observed in natural-system optical (ugriBV) and near-infrared (YJH) bands [^166^] [^629^]. CSP data serve as the low-redshift anchor for most cosmological analyses and are accessible through the sndata Python package.

| Compilation | SNe Count | Surveys / Sources | Primary Format | Cosmology-Ready | Best ML Use Case |
|:---|:---|:---|:---|:---|:---|
| Open Supernova Catalog | 50,000+ (all types) [^651^] | 100+ literature sources | JSON per-SN [^86^] | No | Multi-type classification; anomaly detection |
| Pantheon+ | 1,701 SNe Ia [^451^] | 18 surveys | SNANA FITS + text [^125^] | Yes (SALT2/SALT3) | Cosmology regression; uncertainty-aware ML |
| Union3 / UNITY1.5 | 2,087 SNe Ia [^189^] | 24 datasets | Binned (nodes) [^657^] | Partial (binned only) | Bayesian cosmology inference |
| JLA | 740 SNe Ia [^652^] | SDSS-II, SNLS, low-z | Individual LC + covmat [^452^] | Yes (SALT2.4) | Baseline cosmology; teaching; validation |
| DES-SN5YR | ~1,820 SNe Ia [^344^] | DES 5-year | SMP photometry + FITS | Yes (SALT3.DOVEKIE) | Photometric classification; high-z analysis |
| Asiago Catalog | 11,000+ SNe [^593^] | 1885–present (all sources) | ASCII tables [^142^] | No | Host galaxy correlations; metadata enrichment |
| SAI Catalog | 2,991 SNe [^354^] | 1885–2004 | ASCII (CDS II/256) | No | Historical completeness |
| CSP DR3 | 134 SNe [^166^] | CSP (Las Campanas) | Individual tar.gz archives | Yes (natural system) | Low-z anchor; NIR studies; template building |

This comparison highlights a fundamental division in the compilation landscape. The cosmology-ready samples (Pantheon+, JLA, DES-SN5YR, CSP) provide homogeneous, well-calibrated photometry with standardized light-curve parameters but contain only Type Ia supernovae that have already passed quality cuts. The all-type catalogs (OSC, Asiago) offer breadth across supernova species but lack the calibration precision and uniform photometric processing needed for distance-scale ML. Union3 occupies a middle ground — the largest spectroscopically confirmed Ia compilation — but its binned-only release format currently limits per-supernova ML applications. Practitioners should select compilations based on task requirements: cosmology regression demands Pantheon+ or JLA, multi-type classification requires the OSC, and host-galaxy correlation studies benefit from cross-matching Asiago metadata with survey photometry.

### 6.6 Building Unified Training Sets

Compilations reduce the number of data sources, but significant work remains to produce ML-ready training sets. This section describes the practical toolchain for homogenizing multi-survey data and the challenges that must be addressed in the process.

#### 6.6.1 The SNData Python Package

The SNData package provides the most convenient unified interface for accessing multiple supernova surveys programmatically [^409^] [^635^]. It supports CSP (DR1, DR3), JLA (Betoule14), DES, SDSS, SNLS, and additional surveys on request. Data are automatically downloaded to a local cache, parsed into standardized Astropy tables, and registered with SNCosmo for filter transmission curves.

```python
from sndata.csp import DR3
from sndata.jla import Betoule14

dr3 = DR3()
dr3.download_module_data()
for sn in dr3.iter_data():
    # Each sn is a standardized Astropy table
    print(sn.meta, sn['time'], sn['magnitude'])
```

The standardized format eliminates much of the manual parsing code that would otherwise be required when working with survey-specific file formats. However, SNData does not perform photometric homogenization — it provides access to the raw data as published, leaving calibration and systematization to the user.

#### 6.6.2 SNCosmo for Simulation, Fitting, and Format Conversion

SNCosmo is the primary Python library for supernova cosmology analysis, providing model fitting, simulation, and built-in access to standard datasets [^33^] [^650^]. Its built-in models include SALT2, SALT3, MLCS2k2, Hsiao, Nugent, and SNANA-compatible templates. SALT3 is fully integrated from SNCosmo version 2.12.1 onward [^720^] [^724^]; the SALT3 model was trained on 1,083 SNe with 1,207 spectra — a sample 2.5 times larger than SALT2.JLA — covering a wavelength range of 2,000–11,000 Angstroms, which extends 1,800 Angstroms redder than SALT2 [^721^] [^723^]. The training code is publicly available at saltshaker.readthedocs.io.

For ML workflows, SNCosmo serves three critical functions. First, it converts photometric data between formats (SNANA FITS, ASCII tables, Astropy tables). Second, it fits light-curve models to produce standardized features (light-curve shape x1, color c, peak magnitude mB) that serve as input features for cosmology regression models. Third, it generates synthetic light curves from models, enabling augmentation of real training data with simulated samples:

```python
import sncosmo
model = sncosmo.Model(source='salt3')
model.set(z=0.5, t0=55000., mwebv=0.02)
# Fit to observed data:
# result, fitted_model = sncosmo.fit_lc(data, model, ['z', 't0', 'x0', 'x1', 'c'])
```

#### 6.6.3 Homogenization Challenges

Combining data from multiple surveys requires addressing seven fundamental calibration challenges [^508^] [^536^] [^667^]. Filter transmission curves differ across telescopes, with effective wavelengths varying by 10–100s of Angstroms for nominally identical bands. Photometric systems (AB, Vega, and natural) use different zero-point definitions. Spatial non-uniformity in filter throughput across focal planes can produce radial variations up to 8 mmag in Pan-STARRS. Temporal drift from mirror degradation and dust accumulation changes throughput over multi-year survey durations. Atmospheric extinction varies with airmass and weather. Fundamental flux standards (such as BD+17) exhibit luminosity variations of approximately 4% over decadal timescales. Color transformations between photometric systems introduce systematic errors that propagate nonlinearly into distance measurements.

These challenges have measurable impact on cosmological inference. Calibration uncertainty is the largest systematic contributor to SN Ia cosmology, accounting for 30–50% of the total systematic budget [^721^]. Inter-survey calibration uncertainty of 25 mmag shifts the matter density parameter Omega_M by 0.04 and the dark energy equation-of-state parameter w by −0.17 [^647^]. Filter zero-point perturbations of 0.01 mag can shift w by 0.006–0.009, and SALT model training amplifies calibration errors into distance measurements by up to a factor of 6 [^536^] [^706^].

For ML practitioners, the implications are direct. Training on heterogeneous data without calibration awareness introduces survey-dependent biases that degrade generalization. Feature normalization across surveys requires knowledge of photometric systems and zero-points. When covariance matrices are available (Pantheon+ provides them), they should be incorporated into loss functions through weighted least squares or heteroskedastic loss terms. Bias corrections in simulation-based training depend on accurate calibration in the training sample — an insight that connects to the broader sim-to-real challenges discussed in Chapter 7.

#### 6.6.4 Recommended Workflow

The following workflow synthesizes the tools discussed above into a practical pipeline for building unified training sets from compilation data:

| Stage | Tool / Package | Action | Output |
|:---|:---|:---|:---|
| 1. Data acquisition | SNData, GitHub releases | Download survey-specific subsets | Raw photometry + metadata |
| 2. Format conversion | SNCosmo | Parse SNANA FITS, JSON, ASCII into Astropy tables | Standardized data structures |
| 3. Calibration registration | SNCosmo bandpass library | Register filter curves, apply zero-point corrections | Calibrated fluxes in known systems |
| 4. Light-curve fitting | SNCosmo + SALT3 | Fit x1, c, mB (or equivalent) per supernova | Standardized feature vectors |
| 5. Quality selection | Custom cuts | Minimum N_obs, S/N, phase coverage, fit quality | Clean training sample |
| 6. Covariance propagation | numpy, scipy | Incorporate STAT+SYS covariance into ML loss | Uncertainty-aware model training |
| 7. Cross-validation | scikit-learn | Stratified by survey to test generalization | Survey-robust performance estimates |

The critical quality criteria at Stage 5 depend on the ML task. For cosmology regression, cuts typically require at least 5 photometric points per light curve, a valid SALT fit with reduced chi-squared below 5, and coverage spanning the rise and fall of the B-band peak. For classification, the requirements are less stringent — as few as 3 points in a single filter can support photometric typing with deep learning architectures — but training samples must include representative coverage across all target classes. Stage 6, covariance propagation, is unique to precision cosmology tasks; for classification and anomaly detection, where per-point uncertainties are smaller relative to class separation, simple inverse-variance weighting is often sufficient.

The survey-stratified cross-validation in Stage 7 deserves emphasis. Because each survey operates in a distinct redshift and brightness regime, random cross-validation overestimates performance by allowing training and test sets to share survey-specific systematics. Stratifying by survey ensures that the model generalizes across calibration systems, providing a more realistic estimate of real-world performance when the model is applied to data from facilities not represented in the training sample — a situation that will be common as Rubin begins operations with novel filter curves and calibration chains.

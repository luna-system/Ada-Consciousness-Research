# Dimension 06: Compilation Datasets & Cross-Survey Aggregations for Supernova ML

## Executive Summary

This document catalogs the major supernova compilation datasets and cross-survey aggregations available for machine learning research. The primary compilations include **Pantheon+** (1,701 SNe Ia from 18 surveys), **Union3** (2,087 SNe Ia from 24 datasets via UNITY1.5), **JLA** (740 SNe Ia), the **Open Supernova Catalog** (50,000+ SNe of all types), the **Asiago Supernova Catalog** (dynamic, 1885-present), **DES-SN5YR/DES-Dovekie** (~1,820 SNe), and the **Carnegie Supernova Project** (CSP) multi-release dataset. These compilations differ in their target populations, homogenization approaches, calibration precision, and ML-readiness.

---

## 1. Pantheon+ Compilation

### 1.1 Overview
Pantheon+ [^451^] is the most widely used cosmological supernova compilation, comprising **1,701 light curves of 1,550 distinct Type Ia supernovae** drawn from **18 different surveys** spanning three decades of observation. It is the successor to the original Pantheon sample and was designed for precision cosmology, particularly H0 measurement via SH0ES (Supernovae and H0 for the Equation of State of dark energy).

### 1.2 Data Access

| Attribute | Detail |
|-----------|--------|
| **Primary Repository** | https://github.com/PantheonPlusSH0ES/DataRelease [^125^] |
| **Website** | https://pantheonplussh0es.github.io/ [^595^] |
| **Primary Papers** | Scolnic et al. 2022 (ApJ 938:110) [^451^]; Brout et al. 2022 (ApJ 938:111) [^536^] |
| **Format** | SNANA-format .txt and .FITS files, .FITRES fit result files, CSV summary files |
| **Data Volume** | ~18 subdirectories, one per contributing survey; full download ~GB scale |

### 1.3 Repository Structure [^125^] [^662^]
```
Pantheon+_Data/
  - 18 survey-specific subdirectories (e.g., LOWZ/CfA, SDSS, SNLS, DES, HST)
  - Each contains: .LIST files (SN names), .txt/.FITS light curves, .README documentation
  - 4_DISTANCES_AND_COVAR/ - Contains Pantheon+SH0ES.dat (distance moduli) and covariance matrices
SH0ES_Data/
  - Cepheid and distance-ladder data
Cosmology/
  - Chain files, CosmoSIS likelihoods, cosmology inputs
```

### 1.4 Light Curve File Format [^451^]
- **Text format**: Metadata at top (SN name, R.A./Decl., host position, MW extinction, heliocentric/CMB redshifts, peculiar velocity VPEC), followed by photometric data columns
- **FITS format**: HEAD.FITS (metadata) + PHOT.FITS (light curve data)
- **Data columns**: MJD, FLT (filter), FLUXCAL, FLUXCALERR, MAG, MAGERR
- **Common zero-point**: 27.5 mag for all flux measurements
- **Filters**: All photometric bands from 18 surveys in their natural systems, with calibration offsets documented

### 1.5 Key Data Products
| Product | File/Location | Description |
|---------|--------------|-------------|
| Distance moduli + redshifts | `Pantheon+SH0ES.dat` | Primary cosmology input [^664^] |
| Statistical+Systematic covariance | `Pantheon+SH0ES_STAT+SYS.cov_compressed.gz` | Full covariance matrix |
| Light curve fit results | `.FITRES` files | SALT2/SALT3 fit parameters per SN |
| Calibration files | `calibration_files/` | FITOPT/MUOPT variations for systematic studies |
| Host galaxy properties | Global files | Mass (all), SFR and morphology (z<0.15) |

### 1.6 Covariance Matrices
The Pantheon+ covariance construction is documented in the third-party analysis repository [^452^]. The full STAT+SYS covariance matrix is provided in compressed format. A notebook `how_to_covariance.ipynb` demonstrates proper usage. The CosmoSIS module documentation describes the likelihood implementation [^660^].

### 1.7 Calibration: SuperCal / Fragilistic / Dovekie
Pantheon+ originally used the **SuperCal** cross-calibration [^508^], which tied 25 photometric systems using Pan-STARRS stellar photometry. This was updated to **Fragilistic** in the Pantheon+ analysis [^536^], solving for 105 filter offsets simultaneously with a covariance matrix. More recently, the **Dovekie** recalibration [^706^] provides improved precision with open-source code at https://github.com/bap37/Dovekie/. Dovekie found systematic photometric uncertainty of 0.016 for Flat wCDM, improving Pantheon+ calibration systematic by ~1.5x.

### 1.8 Python Access
```python
# Via SNCosmo (built-in support)
import sncosmo
# SALT3Source model integrated into sncosmo
model = sncosmo.Model(source='salt3')  # or 'salt2'

# Via CosmoSIS
# Module: likelihood/pantheon_plus/pantheon_plus_shoes.py
```

### 1.9 ML Considerations
- **Best for**: Cosmology regression (distance modulus vs. redshift), standardized brightness prediction, systematic uncertainty quantification
- **Caveat**: Only SNe Ia (cosmology-ready sample); pre-selected and homogenized, so NOT suitable for classification tasks requiring raw multi-type samples
- **Strength**: Covariance matrices enable proper treatment of correlated uncertainties in ML loss functions
- **Size**: 1,701 light curves with full photometric history and metadata

---

## 2. Union3 & UNITY1.5

### 2.1 Overview
Union3 [^189^] is the latest compilation from the Supernova Cosmology Project (SCP), comprising **2,087 SNe Ia from 24 datasets**. It is analyzed with the UNITY1.5 (Unified Nonlinear Inference for Type-Ia cosmologY) Bayesian hierarchical framework [^624^]. Union3 is ~1/3 larger than Pantheon+ and uses independent calibration paths and SALT3 light-curve fitting [^622^].

### 2.2 Data Access

| Attribute | Detail |
|-----------|--------|
| **Primary Paper** | Rubin et al. 2025 (ApJ, arXiv:2311.12098) [^189^] [^624^] |
| **Binned Data Release** | https://github.com/rubind/union3_release [^657^] |
| **Alternative Access** | https://github.com/CobayaSampler/sn_data (binned only) [^658^] |
| **Format** | Binned distance moduli + spline model; individual SN data via UNITY framework |
| **SALT3 Fits** | Included in the release |

### 2.3 Important Data Availability Note [^658^]
As of early 2025, **the full unbinned Union3 catalog has NOT been publicly released**. Only binned/compressed data products are available:
- Spline-interpolated distance moduli at 22 redshift nodes
- Gaussian approximation to the posterior (location + Hessian)
- UNITY1.5 framework code for forward-modeling

The UNITY1.5 framework forward-models observed {magnitude, light-curve shape, color} rather than providing per-SN distance moduli. To use a custom cosmology model, one must implement it within UNITY. The full catalog release is anticipated in future updates.

### 2.4 UNITY1.5 Framework Features [^623^] [^626^]
- Bayesian hierarchical model using Hamiltonian Monte Carlo with Stan
- Simultaneously models: outliers (contamination), selection effects (Malmquist bias), light-curve shape/color populations, standardization relations, unexplained dispersion
- Peculiar velocity field recovery (posterior for every parameter)
- Selection effect marginalization over survey depths
- Models populations BEFORE selection effects (unlike traditional approaches)

### 2.5 Python Access
```python
# Binned data via GitHub rubind/union3_release
# UNITY1.5 requires Stan (mc-stan.org)
# Spline model parameters: 22 node values at fixed redshifts
# Cosmological constraints via included likelihood code
```

### 2.6 ML Considerations
- **Best for**: Cosmology with fully Bayesian uncertainty propagation, comparison to Pantheon+ results
- **Caveat**: Binned-only access limits per-SN analysis; framework is designed for cosmology inference, not raw light curve ML
- **Unique feature**: Full posterior over all parameters (including peculiar velocities) enables principled uncertainty quantification
- **Size**: 2,087 SNe Ia (largest spectroscopically-confirmed Ia compilation)

---

## 3. JLA (Joint Light-Curve Analysis)

### 3.1 Overview
JLA [^652^] combines SDSS-II and SNLS SNe Ia observations with low-z samples, totaling **740 spectroscopically confirmed Type Ia supernovae with high-quality light curves**. Published by Betoule et al. 2014, it was the standard cosmology compilation before Pantheon+.

### 3.2 Data Access

| Attribute | Detail |
|-----------|--------|
| **Primary Paper** | Betoule et al. 2014, A&A 568:A22 [^652^] |
| **CDS/VizieR Catalog** | http://cdsarc.u-strasbg.fr/viz-bin/qcat?J/A+A/568/A22 [^452^] |
| **Covariance Matrices** | http://supernovae.in2p3.fr/sdss_snls_jla/covmat_v6.tgz [^452^] |
| **SNData Package** | `from sndata.jla import Betoule14` [^652^] |
| **Format** | Individual light curves + global covariance matrix |
| **Redshift Range** | z < 0.1 (low-z), 0.05 < z < 0.4 (SDSS-II), 0.2 < z < 1 (SNLS) |

### 3.3 Data Products
- **Light curves**: Full multi-band photometry for each SN
- **Covariance matrices**: Full systematic covariance (statistical + systematics) in `covmat_v6.tgz`
- **SALT2 fit parameters**: Light-curve shape (x1), color (c), peak magnitude (mB)
- **Calibration**: Based on Supercal methodology; MegaCam pre-2015 filter set documented

### 3.4 Python Access
```python
from sndata.jla import Betoule14
jla = Betoule14()
jla.download_module_data()  # Download all data
sn_list = jla.get_available_ids()  # Get SN names
data = jla.get_data_for_id('SN2005hk')  # Get light curve table
```

### 3.5 Comparison to Pantheon+
- JLA uses SALT2.4; Pantheon+ uses retrained SALT2/SALT3
- JLA photometric calibration has been superseded by SuperCal/Fragilistic/Dovekie
- Pantheon+ includes more surveys (18 vs. ~5) and more SNe (1,701 vs. 740)
- JLA covariance construction methodology differs from Pantheon+
- Both use similar Tripp estimator standardization: mu = mB + alpha*x1 - beta*c - M0

### 3.6 ML Considerations
- **Best for**: Baseline cosmology ML, smaller-scale experiments, teaching
- **Advantage**: Simpler structure than Pantheon+, full individual SN access, well-tested covariance
- **Caveat**: Superseded by Pantheon+ for precision cosmology; calibration systematics larger

---

## 4. Open Supernova Catalog (OSC)

### 4.1 Overview
The OSC [^651^] [^659^] is the most comprehensive open repository for supernova data of all types, containing **50,000+ supernovae and candidates**. It aggregates data from several dozen sources including the astronomical literature and secondary catalogs. Each SN has a single JSON file containing all its data [^86^].

### 4.2 Data Access

| Attribute | Detail |
|-----------|--------|
| **Primary Paper** | Guillochon et al. 2017, ApJ 835:64 [^651^] |
| **Website** | https://sne.space (now https://astrocrash.net) |
| **GitHub Organization** | https://github.com/astrocatalogs/ [^89^] |
| **Bulk Download (compressed)** | http://snad.space/osc/sne.tar.lzma (379 MB) [^81^] [^661^] |
| **Format** | Hierarchical JSON, one file per SN |
| **Size** | >50,000 SNe candidates; ~12,000 with >10 photometric observations; ~5,000 with spectra [^81^] |

### 4.3 GitHub Repository Structure [^89^]
Individual event JSON files are split across year-based repositories (due to GitHub 1GB/repo limit):
- `github.com/astrocatalogs/sne-pre-1990` – SNe before 1990
- `github.com/astrocatalogs/sne-1990-1999` – 1990-1999
- `github.com/astrocatalogs/sne-2000-2004` – 2000-2004
- `github.com/astrocatalogs/sne-2005-2009` – 2005-2009
- `github.com/astrocatalogs/sne-2010-2014` – 2010-2014
- `github.com/astrocatalogs/sne-2015-2019` – 2015-2019
- `github.com/astrocatalogs/sne-2020-2024` – 2020-present

### 4.4 JSON Schema Structure [^49^] [^651^]
Each SN JSON file follows a hierarchical structure:
```json
{
  "name": "SN2011fe",
  "alias": [...],
  "claimedtype": [...],
  "discoverdate": [...],
  "redshift": [...],
  "ra": [...],
  "dec": [...],
  "host": [...],
  "photometry": [
    {
      "time": "2455811.234",
      "band": "V",
      "magnitude": "11.234",
      "e_magnitude": "0.012",
      "system": "AB",
      "telescope": "LCOGT",
      ...
    }
  ],
  "spectra": [...],
  "error": [...]
}
```

### 4.5 Python Access
```python
# Via AstroCats (full catalog reproduction)
# Install: conda install matplotlib scipy; pip install -r requirements.txt
git clone https://github.com/astrocatalogs/astrocats.git
git clone https://github.com/astrocatalogs/supernovae.git
cd astrocats
python -m astrocats supernovae import  # Full rebuild (~1 day first run)

# Via SNooPy (import directly)
# SNooPy can import OSC data directly

# Parsing JSON files directly
import json, glob
for json_file in glob.glob('sne-*/SN*.json'):
    with open(json_file) as f:
        sn_data = json.load(f)
    photometry = sn_data.get('photometry', [])
    spectra = sn_data.get('spectra', [])
```

### 4.6 Anomaly Detection Use Case [^690^] [^694^]
The OSC was used for the first automated anomaly detection in supernova data (Pruzhinskaya et al. 2019, MNRAS 489:3591). The SNAD pipeline:
1. Downloaded 45,162 objects from OSC (2018 June snapshot)
2. Selected ~2,000 objects with sufficient photometry
3. Pre-processed: converted magnitudes to flux, handled upper limits, 1-day time-binning
4. Approximated light curves with Gaussian Processes (Multivariate GP)
5. Reduced dimensionality with t-SNE
6. Applied Isolation Forest for outlier detection
7. Identified 81 anomalies: 27 confirmed as peculiar SNe, AGN, stellar variables

**SNAD Code**: https://github.com/snad-space/snad [^694^]

### 4.7 ML Considerations
- **Best for**: Classification (all SN types + contaminants), anomaly detection, large-scale studies, rare event discovery
- **Advantage**: Largest and most diverse sample; includes non-SN contaminants (useful for classification training); spectra + photometry + X-ray + radio
- **Caveat**: Highly heterogeneous data quality; many objects have sparse observations; contamination from non-SNe; no uniform calibration
- **Preprocessing needed**: Significant cleaning, GP interpolation, quality cuts required
- **Size**: 50,000+ objects; ~12,000 with >10 photometric points

---

## 5. Asiago Supernova Catalog

### 5.1 Overview
The Asiago Supernova Catalog [^593^] [^596^] is the longest-running dedicated supernova catalog, containing data on **SNe observed since 1885** and their parent galaxies. The dynamic version supersedes the 1999 publication by Barbon et al. and is regularly updated.

### 5.2 Data Access

| Attribute | Detail |
|-----------|--------|
| **Original Reference** | Barbon et al. 1999, A&AS 139:531 [^593^] |
| **CDS Catalog** | https://cdsarc.cds.unistra.fr/ftp/cats/B/sn [^142^] |
| **HEASARC Mirror** | https://heasarc.gsfc.nasa.gov/W3Browse/all/asiagosn.html [^596^] |
| **NASA Data Portal** | https://catalog.data.gov/dataset/asiago-supernova-catalog-dynamic-version [^142^] |
| **Format** | ASCII tables; HEASARC provides HTML and binary (cone search) |
| **Update Frequency** | CDS updates regularly; HEASARC mirrors within ~1 week |
| **Size** | All SNe 1885 to present + parent galaxy data |

### 5.3 Data Products
- SN names, discovery dates, coordinates
- Host galaxy identifications and properties
- SN types and classification status
- Redshifts and distance moduli (where available)
- Cross-references to IAUCs and other circulars
- Parent galaxy data homogenized across multiple catalogs (RC3, UGC, PGC, MCG, ESO)

### 5.4 HEASARC Query Access
```python
# Via HEASARC web interface (cone search, table access)
# URL: https://heasarc.gsfc.nasa.gov/xamin/vo/cone?showoffsets&table=asiagosn&

# Via CDS FTP
cd cdsarc.cds.unistra.fr
# FTP path: /ftp/cats/B/sn
```

### 5.5 ML Considerations
- **Best for**: Catalog-level studies (SN rates, host galaxy correlations), metadata enrichment
- **Advantage**: Long historical baseline (1885-present), dynamic/regularly updated
- **Caveat**: Primarily metadata; light curve data limited (links to other sources for photometry)
- **Use case**: Cross-match with OSC or survey data to add host galaxy information

---

## 6. Sternberg Astronomical Institute (SAI) Catalog

### 6.1 Overview
The SAI Catalog [^354^] contains **2,991 extragalactic supernovae** discovered from 1885 through December 2004, with host galaxy data compiled from multiple astronomical catalogs.

### 6.2 Data Access
| Attribute | Detail |
|-----------|--------|
| **HEASARC** | https://data.nasa.gov/dataset/sternberg-astronomical-institute-catalog-of-supernovae [^354^] |
| **CDS Origin** | CDS Table II/256/sn.dat |
| **Size** | 2,991 SNe (static catalog, not updated) |

### 6.3 Data Products
- SN discovery dates, coordinates, types
- Host galaxy identifications (RC3, UGC, PGC, MCG, ESO, CfA)
- Galaxy morphological types, major diameters, axial ratios
- Photographic magnitudes, recession velocities, position angles

---

## 7. DES-SN5YR / DES-Dovekie

### 7.1 Overview
The Dark Energy Survey 5-Year Supernova sample (DES-SN5YR) [^344^] comprises the best-characterized high-z SN Ia sample before LSST, with ~1,820 SNe used in cosmological analysis. The recent **DES-Dovekie** reanalysis [^475^] provides updated calibration and SALT3 retraining.

### 7.2 Data Access

| Attribute | Detail |
|-----------|--------|
| **Repository** | https://github.com/des-science/DES-SN5YR [^344^] |
| **Light Curves** | Scene Modeling Photometry (SMP) pipeline; released with Sanchez et al. 2024 |
| **SALT3 Models** | SALT3.DOVEKIE and SALT3.DOVEKIE-SYS |
| **Distances** | 4_DISTANCES_COVMAT/ folder: data vector + STAT + STAT+SYS covariance matrices |
| **Simulations** | 25 DES mock simulations provided |
| **Classification** | Classification probabilities for 1,635 DES SNe |

### 7.3 Repository Structure [^344^]
```
0_DATA/          - Light curves from SMP pipeline
1_SIMULATIONS/   - 25 mock simulations
2_LCFIT_MODEL/   - SALT3.DOVEKIE models
3_CLASSIFICATION/ - Classification probabilities
4_DISTANCES_COVMAT/ - MU + zHD vectors and covariance matrices
5_COSMOLOGY/     - SN likelihood and MCMC chains
6_DCR_CORRECTIONS/ - Differential chromatic refraction corrections
7_PIPPIN_FILES/  - Input files for PIPPIN pipeline
```

### 7.4 ML Considerations
- **Best for**: Photometric classification, high-z SN Ia analysis, simulation-based training
- **Advantage**: Deep, well-characterized photometry; extensive simulations for training; CosmoSIS likelihoods
- **Size**: 1,820 SNe in cosmology sample; 1,635 with classification probabilities

---

## 8. Carnegie Supernova Project (CSP)

### 8.1 Overview
CSP provides some of the highest-quality low-z SN photometry and spectroscopy, with natural-system optical (ugriBV) and near-infrared (YJH) observations.

### 8.2 Data Access

| Attribute | Detail |
|-----------|--------|
| **Website** | https://csp.obs.carnegiescience.edu/data [^226^] |
| **DR1 Spectra** | 604 spectra of 93 SNe Ia (Folatelli et al. 2013) [^166^] |
| **DR2 Photometry** | 50 SNe Ia with NIR (Stritzinger et al. 2011) [^629^] |
| **DR3 Photometry** | 134 SNe (2004-2009): 123 SNe Ia, 5 Iax, 2 super-Ch, 2 CSM-interacting (Krisciunas et al. 2017) [^166^] |
| **Format** | Individual data files, tar.gz archives |
| **License** | Creative Commons BY |

### 8.3 Python Access
```python
from sndata.csp import DR1, DR3
# DR3: Natural-system optical (ugriBV) + NIR (YJH) photometry
# 134 SNe, z=0.0037-0.0835, median z=0.0241
# 90% have NIR photometry
```

### 8.4 ML Considerations
- **Best for**: Low-z anchor/training set, NIR SN Ia studies, template building
- **Advantage**: Exceptional photometric precision; well-understood natural photometric system
- **Size**: DR3 has 134 SNe with ugriBVYJH photometry

---

## 9. SNData Python Package (Unified Access)

### 9.1 Overview
**SNData** [^409^] [^635^] provides a standardized interface for downloading, parsing, and manipulating data from multiple supernova surveys. It is the most convenient way to access compilation data programmatically.

### 9.2 Supported Surveys [^409^]
- CSP (DR1, DR3)
- JLA (Betoule14)
- DES (various releases)
- SDSS (various releases)
- SNLS
- Other surveys added on request

### 9.3 Installation & Usage
```python
# pip install sndata
from sndata.csp import DR3
from sndata.jla import Betoule14

dr3 = DR3()
dr3.download_module_data()  # Downloads to local cache
for sn in dr3.iter_data():
    # Process each SN's light curve
    print(sn.meta, sn['time'], sn['magnitude'])
```

### 9.4 Features
- Standardized data format across all surveys (Astropy tables)
- Automatic download with local caching
- Filter transmission curve registration with SNCosmo
- VizieR table access for survey publications
- Force re-download option for data updates

---

## 10. SNCosmo (Simulation & Fitting)

### 10.1 Overview
**SNCosmo** [^33^] [^650^] is the primary Python library for supernova cosmology analysis, providing model fitting, simulation, and built-in access to standard datasets.

### 10.2 Key Features
- **Built-in models**: SALT2, SALT3, MLCS2k2, Hsiao, Nugent, PSNID, SNANA, Whalen
- **Built-in bandpasses**: Extensive filter library
- **Light curve fitting**: Fit SN model parameters to photometric data
- **Simulation**: Generate synthetic light curves from models
- **Extinction laws**: Multiple dust extinction models

### 10.3 SALT3 Integration [^720^] [^724^]
SALT3 is fully integrated into SNCosmo (v2.12.1+):
```python
import sncosmo
model = sncosmo.Model(source='salt3')  # Latest SALT3 model
model.set(z=0.5, t0=55000., mwebv=0.02)
# Fit to data: result, fitted_model = sncosmo.fit_lc(data, model, ...)
```

### 10.4 SALT3 Model Details [^721^] [^723^]
- **Training sample**: 1,083 SNe with 1,207 spectra (2.5x larger than SALT2.JLA)
- **Wavelength range**: 2,000-11,000 Angstroms (1,800A redder than SALT2)
- **Training code**: Publicly available at https://saltshaker.readthedocs.io/
- **Key advantage**: Better uncertainty estimation, improved color/stretch separation

---

## 11. Calibration & Homogenization Challenges

### 11.1 Cross-Calibration Evolution
| Generation | Method | Coverage | Reference |
|------------|--------|----------|-----------|
| **SuperCal** (2015) | PS1 stellar cross-calibration | Multiple systems | Scolnic et al. 2015 [^508^] |
| **Fragilistic** (2022) | 25 systems simultaneously solved | 105 filters | Brout et al. 2022 [^536^] |
| **Dovekie** (2025) | Open-source, DA white dwarfs + Gaia | 11 systems improved | Popovic et al. 2025 [^706^] |

### 11.2 Key Calibration Challenges [^508^] [^536^] [^667^]
1. **Filter differences**: Each telescope has unique filter transmission curves; effective wavelengths differ by 10-100s of Angstroms
2. **Photometric systems**: AB vs. Vega vs. natural systems; different zeropoint definitions
3. **Spatial non-uniformity**: Filter throughput varies across focal planes (up to 8 mmag radial variation in PS1)
4. **Temporal drift**: Mirror degradation, dust accumulation change throughput over time
5. **Atmospheric extinction**: Variable airmass, weather conditions
6. **Fundamental standards**: BD+17 luminosity varies by ~4% over decades; CALSPEC standards updated periodically
7. **Color transformations**: Converting between photometric systems introduces systematic errors

### 11.3 Impact on Cosmology
- Calibration uncertainty is the **largest systematic** in SN Ia cosmology (30-50% of total systematic) [^721^]
- 25 mmag of inter-survey calibration uncertainty shifts Omega_M by 0.04 and w by -0.17 [^647^]
- Filter zeropoint perturbations of 0.01 mag can shift w by 0.006-0.009 [^536^]
- SALT model training propagates calibration errors into distance measurements (amplified by up to 6x) [^706^]

### 11.4 Implications for ML
- **Training on heterogeneous data**: Models must account for varying photometric systems
- **Feature normalization**: Standardizing magnitudes across surveys requires calibration knowledge
- **Systematic uncertainty propagation**: Covariance matrices (when available) should be incorporated into loss functions
- **Simulation requirements**: Bias corrections depend on accurate calibration in training samples

---

## 12. Summary: Which Compilation for Which ML Task?

| ML Task | Recommended Dataset | Size | Key Advantage |
|---------|-------------------|------|---------------|
| **SN Ia cosmology regression** | Pantheon+ | 1,701 | Best calibration, covariance matrices |
| **Bayesian cosmology inference** | Union3 (binned) | 2,087 | Full Bayesian treatment, UNITY framework |
| **SN Ia/light curve fitting** | JLA, CSP DR3 | 740 / 134 | Simple, well-documented, individual access |
| **Multi-type SN classification** | OSC | 50,000+ | All types + contaminants, largest sample |
| **Anomaly detection** | OSC | 50,000+ | Proven use case (SNAD), diverse objects |
| **Photometric classification** | DES-SN5YR | 1,820 | Deep photometry, simulations, probabilities |
| **Low-z anchor/training** | CSP DR3 | 134 | Highest precision, NIR coverage |
| **Rare event discovery** | OSC + SNAD pipeline | 50,000+ | Automated anomaly detection framework |
| **Host galaxy correlation** | Asiago + Pantheon+ | Varies | Host metadata + SN distances combined |
| **Template/model building** | CSP, SALT3 training | 1,083 SNe | High-quality spectra + photometry |

---

## 13. Areas Warranting Deeper Investigation

1. **Union3 full catalog release**: The unbinned individual SN data remains unreleased as of early 2025. Monitor https://github.com/rubind/union3_release for updates.

2. **OSC quality flags**: The catalog lacks systematic quality assessments. Developing ML-ready quality scores would be valuable.

3. **Filter homogenization at scale**: No standardized tool exists to automatically homogenize photometry across all surveys in the OSC. A universal cross-calibration pipeline would benefit ML applications.

4. **SALT3 model extensions**: Ongoing work to extend into NIR for Roman Space Telescope. Monitor https://saltshaker.readthedocs.io/

5. **Foundation Supernova Survey**: Low-z sample serving as dominant anchor for most cosmological analyses [^667^]. Data may be available through ZTF or direct collaboration.

6. **Dovekie open-source calibration**: https://github.com/bap37/Dovekie/ provides an open framework for adding new surveys to the cross-calibration. Critical for integrating new data.

7. **Combining compilations**: How to properly combine Pantheon+, Union3, and OSC data for ML tasks requiring both large samples and precise calibration remains an open research question.

---

## 14. Quick Reference: Access URLs

| Dataset | Primary URL | GitHub/Data URL |
|---------|------------|-----------------|
| Pantheon+ | https://pantheonplussh0es.github.io/ | github.com/PantheonPlusSH0ES/DataRelease |
| Union3 | arXiv:2311.12098 | github.com/rubind/union3_release (binned) |
| JLA | CDS: J/A+A/568/A22 | supernovae.in2p3.fr/sdss_snls_jla/ |
| OSC | sne.space | github.com/astrocatalogs/supernovae |
| OSC Bulk | snad.space/osc/sne.tar.lzma | - |
| Asiago | HEASARC: asiagosn | cdsarc.cds.unistra.fr/ftp/cats/B/sn |
| SAI Catalog | data.nasa.gov (saisncat) | cdsarc.cds.unistra.fr/ftp/cats/II/256/ |
| DES-SN5YR | github.com/des-science/DES-SN5YR | Same (full data release) |
| CSP | csp.obs.carnegiescience.edu/data | Individual tar.gz downloads |
| SALT3 | saltshaker.readthedocs.io | Integrated in sncosmo |
| Dovekie | - | github.com/bap37/Dovekie |
| SNData | sndata.readthedocs.io | github.com/sncosmo/SNData |
| SNCosmo | sncosmo.github.io | github.com/sncosmo/sncosmo |

---

*Document compiled from 20+ independent web searches across survey official sites, arXiv, GitHub, NASA archives, and peer-reviewed publications. All citations use inline references [^N^] mapping to search results.*

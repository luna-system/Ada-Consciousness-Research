# Dimension 03: Low-Redshift Anchor Surveys for ML Training

## Executive Summary

Low-redshift (low-z) supernova surveys provide critical training data for SN classifiers and cosmological analyses. This document provides a deep-dive into the major low-z anchor surveys, their data access methods, formats, and how to combine them into unified training sets for machine learning. The six primary low-z surveys covered are: CSP DR3, CfA Archive (CfA1-4), Foundation DR1, YSE DR1, PS1-MDS, and LOSS (LOSS1/LOSS2). Together with Python packages like `sndata`, `SNooPy`, and `SNCosmo`, these surveys form the backbone of low-z training data for ML-based supernova classification and cosmology.

---

## 1. Carnegie Supernova Project (CSP) Data Release 3

### 1.1 Overview
- **Paper**: Krisciunas et al. (2017), AJ, 154, 211 [^166^]
- **Sample**: 134 SNe observed during CSP-I (2004-2009)
  - 123 Type Ia SNe
  - 5 Type Iax SNe
  - 2 super-Chandrasekhar candidates
  - 2 Type Ia-CSM
  - 2 SN 2006bt-like events
- **Redshift range**: z = 0.0037 to 0.0835 (median z = 0.0241)
- **Photometric system**: Natural-system optical (ugriBV) and near-infrared (YJH)
- **Key feature**: 90% of SNe (120/134) have near-infrared photometry

### 1.2 Data Access

#### Direct Download
- **URL**: https://csp.obs.carnegiescience.edu/data [^226^]
- **File**: `CSP_Photometry_DR3.tar.gz` - single tarball containing all photometry
- **Filter functions and zero-points**: Available at same URL
- **License**: Creative Commons BY [^532^]

#### Via SNData Python Package
- **Package**: `sndata` - https://sndata.readthedocs.io [^409^]
- **Class**: `sndata.csp.DR3`
- **Methods**:
  - `download_module_data()` - Downloads CSP DR3 data
  - `get_available_ids()` - Returns list of SN object IDs
  - `get_data_for_id(obj_id)` - Returns photometry table for given SN
  - `iter_data()` - Iterates through all SNe yielding data tables
  - `register_filters()` - Registers CSP filters with SNCosmo
  - `get_zp_for_band(band)` - Returns zero-point for a given band
- **Format**: Astropy tables with standard `sndata` format (MJD, band, flux, fluxerr, zp, zpsys)

### 1.3 Data Format
- **Photometry**: ASCII files in natural system
- **Columns**: Typically MJD, filter, magnitude, magnitude error
- **Filters**: u, g, r, i, B, V, Y, J, H (CSP natural system)
- **NIR photometry**: Available for 120 SNe
- **No redshift uncertainties included** in original release (Pantheon+ had to estimate them) [^448^]

### 1.4 SNooPy Python Package
- **Purpose**: Python package for fitting and analyzing Type Ia supernova light curves [^224^]
- **GitHub**: https://github.com/obscode/snpy [^529^]
- **Documentation**: https://csp.obs.carnegiescience.edu/data/snpy
- **Key capabilities**:
  - SNIa light-curve template generator in CSP passbands (uBVgriYJHK)
  - K-corrections based on Hsiao et al. (2007) SED templates
  - LM non-linear least-squares fitting
  - Interactive plotting
  - Built-in Lira Law for E(B-V) estimation
  - Can run MLCS2k2 and SALT2 from within SNooPy
  - Imports data directly from Open Supernova Catalog
- **Installation**: `git clone https://github.com/obscode/snpy; python setup.py install`

### 1.5 Strengths for ML
- **Best for**: Multi-band light curve fitting with NIR coverage
- **Advantages**: Precise natural-system photometry, extensive NIR data, well-calibrated templates
- **Limitations**: Relatively small sample (134 SNe), no spectroscopic data in DR3

---

## 2. CfA Supernova Archive (CfA1-4)

### 2.1 Overview
The Harvard-Smithsonian Center for Astrophysics (CfA) Supernova Group has published multiple data releases spanning two decades:

| Sample | Years | N SNe Ia | Reference | Filters |
|--------|-------|----------|-----------|---------|
| CfA1 | 1990s | ~20 | Riess et al. (1999) | UBVRI |
| CfA2 | 1998-2000 | ~25 | Jha et al. (2006) | UBVRI |
| CfA3 | 2001-2008 | 185 | Hicken et al. (2009) | UBVRI |
| CfA4 | 2006-2011 | 94 | Hicken et al. (2012) | UBVRI |
| CfA Stripped | 1994-2009 | 73 | Modjaz et al. (2014) | multi-band |
| CfA Type II | 2000-2011 | 60 | Hicken et al. (2017) | u'UBVRIr'i'JHK |

**Total**: ~324 SNe Ia + extensive core-collapse samples [^398^] [^399^] [^488^] [^493^]

### 2.2 Data Access

#### Main Archive URL
- **URL**: https://lweb.cfa.harvard.edu/supernova/SNarchive.html [^398^]
- **Bulk downloads available**:

| Content | Size | Reference |
|---------|------|-----------|
| IR SNTEMPLATES stacked FITS | 4.2 GB | - |
| Raw stacked data (part 1) | 16 GB | - |
| Raw stacked data (part 2) | 17 GB | - |
| Type II Supernova spectra (Hicken+ 2017) | 12 MB | arXiv:1706.01030 |
| Type II light curves (Natural + Standard) | varies | arXiv:1706.01030 |
| Stripped-envelope light curves (Natural) | - | Bianco et al. (2014) |
| Stripped-envelope light curves (Standard) | 25 MB | Bianco et al. (2014) |
| 645 spectra of 73 stripped SN | 271 KB | Modjaz et al. (2014) |
| 2603 spectra of 462 SN Ia (1993-2008) | 160 MB | Blondin et al. (2012) |
| CfA maximum-light SN Ia spectra | 1.4 MB | Blondin, Mandel & Kirshner |
| CfA SN Ia spectra (Matheson) | 16 MB | Matheson et al. (2008) |
| CfA SN light curves (all types, through 2000) | 26 MB | Jha et al. (2006) |

#### Spectra (FITS format)
- FAST spectrograph spectra (2008-2019) in FITS format available
- SNID results available

#### Via SNData
- Class: `sndata` supports CfA data through various modules
- Formatted for direct use with SNCosmo

### 2.3 Data Format
- **Photometry**: ASCII files in both Natural and Standard systems
- **Spectra**: FITS format with wavelength, flux, and uncertainties
- **Filter passbands**: Available as ASCII tar files
- **Key feature**: Both Natural and Standard system photometry provided

### 2.4 Strengths for ML
- **Best for**: Large spectroscopic sample for spectral classification ML
- **Advantages**: 
  - 160 MB of spectra for 462 SNe Ia (2603 individual spectra)
  - Long time baseline (1993-2011)
  - Both Type Ia and core-collapse samples
  - Standard-system photometry available
- **Limitations**: 
  - No redshift uncertainties reported (Pantheon+ estimated them) [^448^]
  - Inhomogeneous photometric calibration between CfA1-4 epochs
  - B-band calibration uncertainties are significant (~100 mmag for CfA1/2) [^508^]

---

## 3. Foundation Supernova Survey DR1

### 3.1 Overview
- **Paper**: Foley et al. (2018), MNRAS, 475, 193 [^426^]
- **Cosmology paper**: Jones et al. (2019), ApJ, 881, 19 [^427^]
- **Sample**: 225 SNe Ia observed; 180 pass cosmology cuts
  - 175 at z > 0.015 suitable for cosmology
- **Discovery surveys**: ASAS-SN (38%), PSST (20%), ATLAS, Gaia, others
- **Telescope**: Pan-STARRS1 (PS1)
- **Filters**: griz (PS1 system)
- **Redshift range**: z ~ 0.01 to 0.08 (median ~ 0.05)
- **Cadence**: Median 8 days overall, 5.5 days within 10 days of peak

### 3.2 Data Access

#### GitHub Repository
- **URL**: https://github.com/djones1040/Foundation_DR1 [^426^]
- **Maintainers**: D. O. Jones, D. Scolnic, M. Foley
- **Format**: SNANA format light curves
- **Contents**:
  - SNANA-format light curves for 180 cosmologically useful SNe Ia
  - Photometry with 1.5% error floor added in quadrature
  - Host galaxy properties (stellar mass from ZPEG SED-fitting)
  - Peculiar velocities from Carrick et al. (2015) model
  - Milky Way reddening (Schlafly & Finkbeiner 2011)
  - Flux zeropoints: standard SNANA value of 27.5

#### Filter Functions
- Pan-STARRS filter functions included in repository
- Corrected for color-dependent biases in g-band due to PSF-fitting photometry
- File: `kcor_PS1_none.fits`

#### Data Format (SNANA)
```
SURVEY: FOUNDATION
SNID: [name]
RA: [degrees]
DEC: [degrees]
MWEBV: [E(B-V)]

NOBS: [N]
NVAR: 7
VARLIST: MJD FLT FIELD FLUXCAL FLUXCALERR MAG MAGERR
OBS: [MJD] [filter] [field] [flux] [fluxerr] [mag] [magerr]
...
END_PHOTOMETRY:
```

### 3.3 Host Galaxy Properties
- **Method**: ZPEG SED-fitting with GALEX, 2MASS, SDSS, WISE photometry
- **Available for**: All SNe Ia
- **Uncertainties**: Estimated from Monte Carlo-sampled photometry
- **Used for**: Mass step correction in cosmology analyses

### 3.4 Strengths for ML
- **Best for**: Cosmological training samples with uniform photometric system
- **Advantages**:
  - Single telescope (PS1) = homogeneous photometric system
  - Untargeted, magnitude-limited sample (less galaxy-selection bias)
  - Well-calibrated PS1 photometry (few mmag systematics)
  - Host galaxy properties available
  - Similar color/stretch distributions to high-z surveys
- **Limitations**: 
  - Moderate sample size (180-225 SNe)
  - Only griz bands
  - Redshift range limited to z < 0.1

---

## 4. Young Supernova Experiment (YSE) Data Release 1

### 4.1 Overview
- **Paper**: Aleo et al. (2023), ApJS, 266, 9 [^71^] [^402^]
- **Sample**: 1,975 transients (2019-2021)
  - 492 spectroscopically classified
  - 1,483 photometrically classified
- **Filters**: Pan-STARRS1 griz + ZTF gr
- **Redshift range**: z ~ 0.01 to 0.5
- **Key feature**: Includes ParSNIP classifications for all transients

### 4.2 Data Access

#### Zenodo
- **URL**: https://zenodo.org/records/7317476 [^68^]
- **DOI**: 10.5281/zenodo.7317476
- **Files**:
  - `yse_dr1_zenodo.tar.gz` - All light curves (no S/N cut)
  - `yse_dr1_zenodo_snr_geq_4.tar.gz` - Light curves with S/N >= 4
  - `parsnip_results_for_ysedr1_table_A1_full_for_online.csv` - Full ParSNIP classifications

#### GitHub Tutorial
- **URL**: https://github.com/patrickaleo/ysedr1_data_demos [^530^]
- **Contents**: Jupyter notebook showing how to:
  - Download YSE DR1 data (full sample, spec sample, phot sample)
  - Grab metadata
  - Recreate plots from the paper

### 4.3 Data Format (SNANA)
- **Format**: SNANA HEAD+PHOT format
- **Metadata in HEAD file**: RA, Dec, redshift, host galaxy association, classification
- **Photometry in PHOT file**: MJD, filter, flux, flux error

### 4.4 ParSNIP Classifications
- **Classifier**: ParSNIP (Boone 2021) - variational autoencoder with physics layer [^282^]
- **Performance on spec test set (472 SNe)**:
  - 82% accuracy across 3 classes (Ia, II, Ib/c)
  - 90% accuracy across 2 classes (Ia vs CC)
  - >90% completeness and purity for SNe Ia
- **Photometric sample results**:
  - 1,048 (~71%) SNe Ia
  - 339 (~23%) SNe II
  - 96 (~6%) SNe Ib/c

### 4.5 Strengths for ML
- **Best for**: Multi-class photometric classification training
- **Advantages**:
  - Large, recent sample with modern photometric quality
  - Pre-computed ParSNIP classifications available
  - Multi-survey photometry (PS1 + ZTF)
  - Both spectroscopic and photometric labels
  - Includes rare classes (Iax, SLSN, TDE)
- **Limitations**:
  - Relatively short time baseline (2 years)
  - Inhomogeneous follow-up depth

---

## 5. Pan-STARRS1 Medium Deep Survey (PS1-MDS)

### 5.1 Overview
- **Paper**: Rest et al. (2014), ApJ, 795, 44 [^440^]
- **Cosmology papers**: Jones et al. (2018), Scolnic et al. (2018)
- **Sample**: ~5,200 SNe discovered; ~350 spectroscopically classified SNe Ia
  - 1,169 used for cosmology (spec + photometric classifications)
- **Area**: 70 deg^2
- **Filters**: griz (PS1)
- **Cadence**: ~6 observations per 10 days
- **Duration**: 2010-2014 (4 years)
- **Redshift range**: z ~ 0.1 to 0.7

### 5.2 Data Access

#### MAST CasJobs SQL Interface
- **URL**: https://mastweb.stsci.edu/ps1casjobs [^21^]
- **Features**:
  - Full SQL access to PS1 catalog database
  - Synchronous and asynchronous query execution
  - Results saved to private user space
  - Requires (free) MAST account

#### MAST Portal
- **Object Catalog Search**: https://catalogs.mast.stsci.edu/ [^21^]
- **Image Cutout Server**: https://ps1images.stsci.edu/cgi-bin/ps1cutouts
- **Features**: Cone search, catalog queries, image downloads

#### Programmatic Access (Python)
```python
# Example PS1 MAST API queries
# Documentation: https://ps1images.stsci.edu/ps1image.html
import requests

# Catalog query for light curves
# MAST API: https://catalogs.mast.stsci.edu/docs/panstarrs.html
```

#### SuperRAENN Classification
- **Paper**: Villar et al. (2020) [^441^]
- **Sample**: 5,243 "SN-like" light curves; 2,315 photometrically classified
- **Classes**: Type Ia (62.0%), Type II (19.8%), Type IIn (4.8%), Type Ibc (11.7%), SLSN-I (1.6%)
- **Accuracy**: 87% across 5 classes
- **Data products**: Full set of light curves and classifications published

### 5.3 Data Products Available
- Single-epoch exposure catalogs (DR2)
- Stacked image catalogs (DR1/DR2)
- Forced photometry (DR2)
- Difference image catalogs
- FITS images and cutouts

### 5.4 Strengths for ML
- **Best for**: High-z SN classification training, LSST-like survey simulation
- **Advantages**:
  - Large sample size (~5200 SNe)
  - LSST-like cadence and depth
  - Excellent photometric calibration (7-12 mmag stability) [^507^]
  - Full multi-epoch photometry for variability studies
- **Limitations**:
  - Not all SNe have spectroscopic classifications
  - Requires CasJobs knowledge for bulk access
  - Medium Deep fields are small area (70 deg^2)

---

## 6. Lick Observatory Supernova Search (LOSS)

### 6.1 Overview
The Lick Observatory Supernova Search has two major data releases:

#### LOSS1
- **Paper**: Ganeshalingam et al. (2010), ApJS, 190, 418 [^483^]
- **Sample**: 165 Type Ia SNe (105 in cosmology sample)
- **Years**: 1998-2008
- **Redshift range**: z = 0.002 to 0.095
- **Filters**: BVRI

#### LOSS2
- **Paper**: Stahl et al. (2019), MNRAS, 485, xxx [^480^] [^520^]
- **Sample**: 93 Type Ia SNe
- **Years**: 2009-2016
- **Filters**: UBVRI
- **Telescope**: Katzman Automatic Imaging Telescope (KAIT) and Nickel 1-m

### 6.2 Data Access

#### LOSS1
- **Via SNData**: `sndata.loss.Ganeshalingam13` [^482^]
- **Data tables**: VizieR tables available
- **Method**: `iter_data()` yields photometry for each SN

#### LOSS2
- Published as part of Pantheon+ sample
- Available via Pantheon+ GitHub: https://github.com/PantheonPlusSH0ES/DataRelease [^481^]

### 6.3 Strengths for ML
- **Best for**: Very nearby SNe for absolute magnitude calibration
- **Advantages**:
  - Very low redshift (some at z < 0.01)
  - Cepheid-host galaxies for H0 calibration
  - Long time baseline (1998-2016)
- **Limitations**:
  - Targeted survey (galaxy-selection bias)
  - Inhomogeneous between LOSS1 and LOSS2
  - B-band calibration relatively uncertain [^508^]

---

## 7. Python Packages for Unified Data Access

### 7.1 SNData
- **URL**: https://sndata.readthedocs.io [^409^]
- **GitHub**: https://github.com/sncosmo/SNData
- **Purpose**: Provides consistent data access across multiple supernova surveys
- **Available surveys**:

| Survey | Module | Data Types |
|--------|--------|------------|
| CSP | `sndata.csp` | DR1 (spectra), DR3 (photometry) |
| DES | `sndata.des` | Photometry |
| ESSENCE | `sndata.essence` | Photometry |
| JLA | `sndata.jla` | Compilation |
| LOSS | `sndata.loss` | Photometry |
| SDSS | `sndata.sdss` | Photometry |
| SNLS | `sndata.snls` | Photometry |
| Sweetspot | `sndata.sweetspot` | Photometry |

- **Key features**:
  - Standardized interface across all surveys
  - Automatic data download and caching
  - Direct SNCosmo integration
  - Filter registration

### 7.2 SNCosmo
- **URL**: https://sncosmo.github.io [^33^]
- **GitHub**: https://github.com/sncosmo/sncosmo
- **Purpose**: Python library for supernova cosmology
- **Features**:
  - Light curve simulation and fitting
  - Built-in models: SALT2, MLCS2k2, Hsiao, Nugent, PSNID, SNANA
  - Built-in bandpasses and magnitude systems
  - Reads/writes SNANA format files
  - Standard photometric data format: `time, band, flux, fluxerr, zp, zpsys`

### 7.3 SNooPy
- **URL**: https://csp.obs.carnegiescience.edu/data/snpy [^224^]
- **GitHub**: https://github.com/obscode/snpy [^529^]
- **Purpose**: Type Ia SN light curve fitting
- **Features**:
  - CSP-specific templates
  - K-correction computation
  - SED template matching
  - SQL database interface
  - Direct Open Supernova Catalog import

### 7.4 SNANA
- **Tutorial**: https://kicp.uchicago.edu/~kessler/SNANA_Tutorial/ [^102^]
- **Purpose**: Comprehensive SN analysis package
- **Format**: ASCII and FITS formats for photometry and spectroscopy
- **Standard fields**: `MJD, FLT, FIELD, FLUXCAL, FLUXCALERR, MAG, MAGERR`
- **Flux zeropoint**: 27.5 mag (standard)

---

## 8. Filter System Homogenization Challenges

### 8.1 The Problem
Different surveys use different filter systems, leading to systematic photometric calibration differences that are one of the largest uncertainties in SN cosmology [^508^] [^531^].

### 8.2 Survey Filter Systems Summary

| Survey | Filters | Standard | Primary Calibrator |
|--------|---------|----------|-------------------|
| PS1 | grizy | AB | 7 Calspec standards |
| SNLS | ugriz | AB | 3 Calspec standards |
| SDSS | ugriz | AB | 3 Calspec standards |
| CSP | ugriBVYJH | Natural/AB | BD+17, Smith, Landolt |
| CfA1-4 | UBVRI | Natural | Landolt |
| Foundation | griz | PS1/AB | PS1 catalog |

### 8.3 Supercal Method
- **Paper**: Scolnic et al. (2015), ApJ, 815, 117 [^508^] [^531^]
- **Approach**: Cross-calibrate all surveys to PS1 using overlapping secondary standards
- **Measured discrepancies**: Average 10 mmag, up to 35 mmag in some passbands
- **Impact on cosmology**: Changes in w by ~2.6% (half the statistical uncertainty)
- **Key findings**:
  - Largest discrepancies in B-band for low-z surveys
  - PS1, SNLS, SDSS agree better with each other than with low-z surveys
  - Low-z surveys partly tied to Vega system (BD+17), partly to AB

### 8.4 Implications for ML Training
1. **Feature space mismatch**: Same physical SN may have different magnitudes in different surveys
2. **K-correction requirements**: Need accurate SED models for cross-survey comparison
3. **Calibration-sensitive features**: Color features particularly affected by filter calibration
4. **Recommendation**: Use Supercal-corrected data when combining surveys

### 8.5 Best Practices for ML
- Use `sndata` for consistent formatting across surveys
- Register correct filter transmission functions with SNCosmo
- Apply Supercal corrections when combining multiple surveys
- Include photometric calibration uncertainty in ML uncertainty budgets
- Consider using only AB-system data for cross-survey training

---

## 9. Combining Surveys into Unified Training Sets

### 9.1 Pantheon+ Compilation
The Pantheon+ sample (Scolnic et al. 2022) represents the gold standard for combined SN Ia datasets [^451^] [^487^]:

- **1701 light curves** from 1550 unique SNe Ia
- **18 different surveys** combined
- **Redshift range**: z = 0.001 to 2.26
- **Low-z component**: LOSS, CfA1-4, CSP, Foundation, SOUSA, CNIa0.02
- **Data access**: https://github.com/PantheonPlusSH0ES/DataRelease [^481^]

### 9.2 Low-z Training Set Assembly

| Survey | N SNe Ia | z range | Key ML Feature |
|--------|----------|---------|----------------|
| CSP DR3 | 123 Ia | 0.004-0.08 | NIR photometry, precise calibration |
| CfA1-4 | ~324 Ia | 0.003-0.1 | Spectra + photometry, long baseline |
| Foundation DR1 | 180 Ia | 0.015-0.08 | Uniform PS1 system, untargeted |
| LOSS1 | 105 Ia | 0.002-0.095 | Very nearby, Cepheid hosts |
| LOSS2 | ~45 Ia | 0.003-0.08 | Continuation of LOSS |
| YSE DR1 | ~1048 Ia | 0.01-0.5 | Multi-class, pre-classified |
| PS1-MDS | ~350 Ia | 0.1-0.7 | High-z, LSST-like |

### 9.3 Recommended Approach for ML Training Sets

1. **Use `sndata`** for consistent data loading and formatting
2. **Apply Supercal** cross-calibration corrections
3. **Include metadata**: redshift, host mass, MW extinction, classification
4. **Standardize format**: SNCosmo standard (time, band, flux, fluxerr, zp, zpsys)
5. **Add quality flags**: coverage, S/N, fit quality
6. **Train/test splits**: Split by survey to test cross-survey generalization
7. **Class balance**: Consider SMOTE or weighted sampling for rare classes [^528^]

### 9.4 ML-Specific Considerations

#### For Classification
- **Temporal features** (duration, rise/fall times) most discriminative [^527^]
- **Color features** important but secondary to timing
- **Multi-band coverage** essential for reliable classification
- **Redshift information** significantly improves accuracy

#### For Cosmology
- **Uniform photometric system** most important (Foundation best)
- **Well-sampled light curves** around peak required
- **Host galaxy properties** for mass step correction
- **Accurate redshifts** and peculiar velocity corrections needed

---

## 10. Each Survey's Strengths for Different ML Tasks

### 10.1 Classification Tasks

| Task | Best Survey | Why |
|------|-------------|-----|
| Ia vs CC separation | YSE DR1, PS1-MDS | Large, multi-class samples with labels |
| Ia subtype classification | CSP DR3 | NIR photometry distinguishes subtypes |
| Photometric typing | PS1-MDS + SuperRAENN | Pre-computed classifications |
| Early-time classification | YSE DR1 | Young SNe emphasized in sample |
| Rare transient ID | YSE DR1 | Includes SLSN, TDE, Iax classes |

### 10.2 Cosmology Tasks

| Task | Best Survey | Why |
|------|-------------|-----|
| H0 calibration | LOSS1/LOSS2 | Cepheid-host SNe at z < 0.01 |
| w measurement | Foundation + PS1-MDS | Single telescope, uniform system |
| Training SALT2/3 | CSP + Foundation | Well-calibrated, multi-band |
| Bias correction | Foundation | Known selection function |

### 10.3 Physical Modeling

| Task | Best Survey | Why |
|------|-------------|-----|
| Light curve fitting | CSP DR3 (SNooPy) | NIR templates, K-corrections |
| Spectral modeling | CfA (spectra) | 2603 spectra of 462 SNe Ia |
| Bolometric light curves | CSP DR3 | ugriBVYJH coverage |
| Extinction mapping | CSP DR3 + CfA | Multi-band UV through NIR |

---

## 11. Summary Table: Complete Dataset Comparison

| Property | CSP DR3 | CfA Archive | Foundation DR1 | YSE DR1 | PS1-MDS | LOSS |
|----------|---------|-------------|----------------|---------|---------|------|
| **N SNe Ia** | 123 | ~324 | 180 | ~1048 | ~350 | ~150 |
| **z range** | 0.004-0.08 | 0.003-0.1 | 0.015-0.08 | 0.01-0.5 | 0.1-0.7 | 0.002-0.1 |
| **Filters** | ugriBVYJH | UBVRI | griz | griz+ZTF gr | griz | UBVRI |
| **Photometric System** | Natural/AB | Natural/Std | PS1/AB | PS1/AB | PS1/AB | Natural |
| **Spectra** | Separate DR | 2603 spectra | Some | No | No | Some |
| **NIR Photometry** | Yes (90%) | Some (CfA4) | No | No | No | No |
| **Classification** | Spec | Spec | Spec | Spec + ParSNIP | Spec + SuperRAENN | Spec |
| **Host Properties** | Limited | No | Yes (mass) | Yes | Yes | No |
| **ML Best For** | NIR fitting, subtypes | Spectral ML | Cosmology training | Multi-class training | High-z training | H0 anchor |
| **Download Size** | ~MB | ~200 MB | ~MB | ~GB | ~TB (catalog) | ~MB |
| **Access Method** | sndata, direct | Web, SNData | GitHub | Zenodo | CasJobs | SNData |

---

## 12. Flagged Areas for Deeper Investigation

1. **CSP DR3 tarball format**: The exact internal file structure of `CSP_Photometry_DR3.tar.gz` needs inspection
2. **CfA spectra bulk download**: Automation of downloading 160 MB of FITS spectra
3. **YSE DR1 SNANA format details**: HEAD/PHOT file structure for batch processing
4. **PS1-MDS CasJobs queries**: Specific SQL queries for extracting SN light curves
5. **LOSS2 data access**: Direct download path for the second LOSS sample
6. **Supercal correction application**: How to apply Supercal corrections to individual survey data
7. **Filter transmission functions**: Download and registration for all low-z surveys
8. **ZTF DR2 cross-matching**: Combining ZTF data with YSE for improved training samples
9. **SNANA simulation tools**: For generating training samples with known selection functions
10. **sndata extension**: Adding additional surveys to the unified interface

---

## References and Citations

- [^166^] SNData CSP Documentation: https://sndata.readthedocs.io/en/latest/module_docs/csp.html
- [^21^] Pan-STARRS1 MAST Archive: https://outerspace.stsci.edu/spaces/PANSTARRS/pages/298812201/
- [^224^] SNooPy Documentation: https://csp.obs.carnegiescience.edu/data/snpy
- [^226^] CSP Data Products: https://csp.obs.carnegiescience.edu/data
- [^33^] SNCosmo: https://sncosmo.github.io/
- [^398^] CfA Supernova Archive: https://lweb.cfa.harvard.edu/supernova/SNarchive.html
- [^399^] CfA Supernova Research: https://lweb.cfa.harvard.edu/supernova/
- [^409^] SNData Package: https://sndata.readthedocs.io/
- [^426^] Foundation DR1 GitHub: https://github.com/djones1040/Foundation_DR1
- [^427^] Foundation Cosmology (Jones+ 2019): https://iopscience.iop.org/article/10.3847/1538-4357/ab2bec
- [^441^] SuperRAENN (Villar+ 2020): https://iopscience.iop.org/article/10.3847/1538-4357/ab8dbe
- [^448^] Pantheon+ Redshifts: https://www.cambridge.org/core/journals/publications-of-the-astronomical-society-of-australia/article/pantheon-analysis-improving-the-redshifts-and-peculiar-velocities-of-type-ia-supernovae-used-in-cosmological-analyses/
- [^451^] Pantheon+ Full Dataset (Scolnic+ 2022): https://iopscience.iop.org/article/10.3847/1538-4357/ac8b7a
- [^459^] SNooPy GitHub: https://github.com/obscode/snpy
- [^470^] SNANA Tutorial: https://kicp.uchicago.edu/~kessler/SNANA_Tutorial/
- [^479^] SALTShaker Data Format: https://saltshaker.readthedocs.io/en/latest/data.html
- [^481^] Pantheon+ Data Release: https://github.com/PantheonPlusSH0ES/DataRelease
- [^482^] SNData LOSS Documentation: https://sndata.readthedocs.io/en/latest/module_docs/loss.html
- [^508^] Supercal (Scolnic+ 2015): https://iopscience.iop.org/article/10.1088/0004-637X/815/2/117
- [^530^] YSE DR1 Tutorial: https://github.com/patrickaleo/ysedr1_data_demos
- [^531^] Supercal arXiv: https://arxiv.org/abs/1508.05361
- [^532^] CSP News: https://csp.obs.carnegiescience.edu/news-items
- [^68^] YSE DR1 Zenodo: https://zenodo.org/records/7317476
- [^71^] YSE DR1 Paper (Aleo+ 2023): https://inspirehep.net/files/32e400834761c5a3597e3df73856cf1a
- [^282^] ParSNIP (Boone 2021): https://arxiv.org/abs/2106.02848
- [^527^] Compact Features for SN Classification: https://arxiv.org/abs/2603.14500
- [^528^] Superphot+: https://iopscience.iop.org/article/10.3847/1538-4357/ad6a4f
- [^440^] Jones+ 2019 PS1+Foundation Cosmology: https://iopscience.iop.org/article/10.3847/1538-4357/ab2bec
- [^520^] Stahl+ 2019 LOSS2: https://academic.oup.com/mnras/article/512/3/3195/6549938
- [^483^] Ganeshalingam+ 2010 LOSS1: https://iopscience.iop.org/article/10.1088/0067-0049/190/2/418
- [^487^] Pantheon+ Cosmology (Brout+ 2022): https://iopscience.iop.org/article/10.3847/1538-4357/ac8e04

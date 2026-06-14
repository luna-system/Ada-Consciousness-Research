# Dimension 02: Dark Energy Survey (DES) Supernova Data for ML

## Executive Summary

The Dark Energy Survey (DES) 5-Year Supernova Program (DES-SN5YR) represents one of the richest publicly available datasets for supernova cosmology and machine learning research. Released in 2024, it contains **31,636 DiffImg** and **19,706 SMP light curves**, of which **1,635 photometrically classified SNe Ia** pass cosmology quality cuts over the redshift range **0.10 < z < 1.13** -- the largest single-instrument SN sample ever assembled [^342^][^350^]. The data is available via both **GitHub (des-science/DES-SN5YR)** and **Zenodo (DOI: 10.5281/zenodo.12720777/12720778)** [^344^][^477^], with comprehensive **25 mock simulations** included for training and validation [^456^]. A dedicated **DES-SN-DR utility package** (BrunoSanchez/DES-SN-DR) provides Python tools for data access [^413^][^485^].

**Key Papers:**
- DES Key Paper: Abbott et al. 2024 (ApJL, arXiv:2401.02929) [^407^]
- Cosmology Analysis: Vincenzi et al. 2024 (ApJ, 975, 86, arXiv:2401.02945) [^409^][^410^]
- Light Curves & Data Release: Sanchez et al. 2024 (ApJ, 975, 5, arXiv:2406.05046) [^395^][^342^]
- Photometric Classification: Moller et al. 2022 (MNRAS) [^551^] and Moller et al. 2024 [^471^]

---

## 1. DES-SN5YR GitHub Repository Structure and Data Download

### 1.1 Repository Overview

The official GitHub repository is at **https://github.com/des-science/DES-SN5YR** [^344^]. The repository contains:

| Directory | Contents |
|-----------|----------|
| `0_DATA/` | Light curves in SNANA FITS format (DES, Foundation, Low-z samples) |
| `1_SIMULATIONS/` | 25 DES mock simulations (SNIa + non-Ia) |
| `2_LCFIT_MODEL/` | SALT3 light curve fitting models (SALT3.DOVEKIE and SALT3.DOVEKIE-SYS) |
| `3_CLASSIFICATION/` | Classification probabilities for 1,635 DES SNe from multiple classifiers |
| `4_DISTANCES_COVMAT/` | Hubble diagram data vectors and covariance matrices |
| `5_COSMOLOGY/` | SN likelihood and MCMC chains for cosmological fits |
| `6_DCR_CORRECTIONS/` | Wavelength-dependent atmospheric corrections |
| `7_PIPPIN_FILES/` | Pippin pipeline input files to reproduce the analysis |

### 1.2 How to Download the Data

**Method 1: Clone GitHub repository**
```bash
git clone https://github.com/des-science/DES-SN5YR.git
```

**Method 2: Download from Zenodo** [^485^][^477^]
```bash
wget https://zenodo.org/records/12720778/files/DES-SN5YR-1.2.zip?download=1
```

**Method 3: Use DES-SN-DR utility package** [^413^][^485^]
```bash
git clone https://github.com/BrunoSanchez/DES-SN-DR.git
cd DES-SN-DR
pip install -e .
downloaddessndr <destination_directory>
```

### 1.3 Zenodo Release Details

The Zenodo record (DOI: 10.5281/zenodo.12720777) contains [^477^]:
- **Total size**: ~1.5 GB (DES-SN5YR-1.2.zip)
- **Published**: July 11, 2024
- **License**: CC BY 4.0
- **Data products**:
  - `DES-SN5YR_DES_HEAD.FITS.gz` (2.9 MB) + `DES-SN5YR_DES_PHOT.FITS.gz` (66.1 MB)
  - `DES-SN5YR_Foundation_HEAD.FITS.gz` (19.3 kB) + `DES-SN5YR_Foundation_PHOT.FITS.gz` (100.6 kB)
  - `DES-SN5YR_LOWZ_HEAD.FITS.gz` (36.8 kB) + `DES-SN5YR_LOWZ_PHOT.FITS.gz` (495.1 kB)
  - 25 simulation folders (each containing HEAD.FITS.gz, PHOT.FITS.gz, DUMP files)

### 1.4 DES-SN-DR Utility Package

The `dessndr` Python package provides convenience utilities [^413^][^485^]:
```python
from dessndr import utils, data
import os

# Initialize photometry reader
phot = utils.PhotFITS(os.path.join(data.DES5YRDR_DATA, '0_DATA/DES-SN5YR_DES'))

# Get a single light curve
lc = phot.get_lc(phot.cid_recs[0])
```

Jupyter notebook tutorials are available:
- Part 1: Load DES Photometry
- Part 2: Load LCPlot file
- Part 3: Load DES SN Classification
- Part 4: Hubble Diagram from DES 5YR
- Part 5: Lambda Dependent corrections
- Part 6: Demonstrate cosmology analysis

**Note**: The GitHub page has been updated to include the DES-Dovekie reanalysis results (Popovic et al. 2026, arXiv:2511.07517) [^344^][^396^]. The original Vincenzi et al. 2024 legacy release is available at tag 1.3 [^344^].

---

## 2. Data Format Details: FITS Tables, SNANA .DAT Files, ASCII .FITRES Files

### 2.1 SNANA FITS Format (Primary Data Format)

All DES-SN5YR light curves are released in the **SNANA FITS format**, consisting of paired HEAD and PHOT files [^439^][^456^]. This is the standard format used by the SNANA (SuperNova ANAlysis) software [^554^].

**HEAD file structure:**
Each row contains summary metadata for one SN, with key columns [^439^]:

| Column | Description |
|--------|-------------|
| `SNID` | Integer or character ID |
| `FAKE` | 0=real data, 1=fake overlaid, 2=SNANA sim |
| `RA`, `DEC` | Sky coordinates (degrees) |
| `SNTYPE` | Integer type assigned by survey |
| `NOBS` | Number of observations (all bands) |
| `PTROBS_MIN` | Pointer to first light curve observation in PHOT file |
| `PTROBS_MAX` | Pointer to last light curve observation |
| `MWEBV[_ERR]` | Milky Way E(B-V) extinction |
| `REDSHIFT_HELIO[_ERR]` | Best heliocentric redshift |
| `REDSHIFT_FINAL[_ERR]` | Best CMB redshift |
| `VPEC_[ERR]` | Peculiar velocity correction |
| `PEAKMJD` | Approximate peak MJD |
| `MJD_TRIGGER` | MJD when survey trigger satisfied |
| `MJD_DETECT_FIRST/LAST` | MJD of first/last detection |
| `HOSTGAL_OBJID` | Host galaxy integer ID |
| `HOSTGAL_RA`, `HOSTGAL_DEC` | Host galaxy coordinates |
| `HOSTGAL_SNSEP` | Transient-host separation (arcsec) |
| `HOSTGAL_DDLR` | SN-host separation in distance-light-radii |
| `HOSTGAL_SPECZ[_ERR]` | Host spectroscopic redshift |
| `HOSTGAL_PHOTOZ[_ERR]` | Host photometric redshift |
| `HOSTGAL_LOGMASS[_ERR]` | Host stellar mass (log solar masses) |
| `HOSTGAL_LOGSFR[_ERR]` | Host star formation rate (log) |
| `HOSTGAL_MAG_[band]` | Host galaxy magnitudes (u,g,r,i,z,Y) |
| `HOSTGAL_MAGERR_[band]` | Uncertainties on host magnitudes |
| `HOSTGAL_SB_FLUXCAL_[band]` | Surface brightness at SN location |

**PHOT file structure:**
Contains individual photometric observations, accessed via HEAD file pointers [^439^]:

| Column | Description |
|--------|-------------|
| `MJD` | Modified Julian Date (-777 marks end of light curve) |
| `BAND` | Filter band (g, r, i, z) |
| `CCDNUM` | CCD detector number |
| `IMGNUM` | Image/exposure number |
| `FIELD` | Field name (SHALLOW, DEEP, etc.) |
| `PHOTFLAG` | Bit-mask of quality flags |
| `PHOTPROB` | RealBogus score or chi2 |
| `FLUXCAL` | Calibrated flux (mag = 27.5 - 2.5*log10(FLUXCAL)) |
| `FLUXCALERR` | Poisson uncertainty on FLUXCAL |
| `PSF_SIG1` | PSF Gaussian sigma (pixels) |
| `SKY_SIG` | Sky noise (ADU/pixel) |
| `SKY_SIG_T` | Template sky noise (DiffImg only) |
| `ZEROPT` | Image zero point |
| `GAIN` | Photoelectron/ADU conversion |
| `XPIX`, `YPIX` | CCD pixel coordinates |

**For simulated data**, additional columns include `SIM_TYPE_INDEX` (true transient type) and `SIM_[property]` (true simulated properties).

### 2.2 SNANA .DAT Format

The SNANA ASCII format uses one file per SN. It uses `VARNAMES:` header lines followed by `OBS:` lines for each observation. This is used primarily for simulations [^99^][^469^].

### 2.3 ASCII .FITRES Format

The FITRES format is SNANA's standard light curve fitting output, containing one row per SN with fit parameters [^469^]:
- Header line starting with `VARNAMES:` lists all columns
- Data lines starting with `SN:` contain per-SN values
- Key columns include: `CID`, `zHEL`, `x0`, `x1`, `c`, `mB`, `MU`, `MUMODEL`, `MUERR`, `CHI2`, `NDOF`, `FITPROB`

### 2.4 Python Data Access

**Using sncosmo (recommended):**
```python
import sncosmo

# Read SNANA FITS files
sne = sncosmo.read_snana_fits('DES-SN5YR_DES_HEAD.FITS.gz', 
                               'DES-SN5YR_DES_PHOT.FITS.gz')

# Access individual supernovae
for sn in sne:
    print(sn.meta['SNID'])  # metadata
    print(sn['MJD'])        # MJD column
    print(sn['FLUXCAL'])    # flux column
```

**Using astropy:**
```python
from astropy.io import fits

# Read HEAD file
head = fits.open('DES-SN5YR_DES_HEAD.FITS.gz')
head_data = head[1].data  # Binary table

# Read PHOT file
phot = fits.open('DES-SN5YR_DES_PHOT.FITS.gz')
phot_data = phot[1].data  # Binary table
```

**Using DES-SN-DR package:**
```python
from dessndr import utils, data
import os

phot = utils.PhotFITS(os.path.join(data.DES5YRDR_DATA, '0_DATA/DES-SN5YR_DES'))
lc = phot.get_lc(phot.cid_recs[0])
```

---

## 3. The 1,635 Cosmology-Grade SNe Ia Sample

### 3.1 Overview

The DES-SN5YR cosmology sample comprises **1,635 photometrically classified SNe Ia** with spectroscopic redshifts spanning **0.10 < z < 1.13**, making it the largest single-survey, single-instrument sample used for cosmological constraints [^409^][^407^]. Of these, **1,499 (91%)** have SuperNNova classification probability P(Ia) > 0.5 [^537^].

When combined with **194 low-redshift SNe Ia** from Foundation, CfA, and CSP, the total Hubble diagram sample contains **1,829 SNe** [^409^].

### 3.2 Selection Criteria (Iterative Cuts)

The selection follows a sequence of cuts detailed in Table 4 of Vincenzi et al. 2024 [^537^][^409^]:

| Cut | Low-z sample | DES sample | P(Ia)>0.5 fraction |
|-----|-------------|-----------|-------------------|
| Spec-z + SALT3 fit converged + z > 0.025 | 247 | 3,621 | 2,200 [60%] |
| "Normal SNIa" (\|x1\| < 3 and \|c\| < 0.3) | 238 | 2,449 | 2,052 [83%] |
| "Well constrained" (sigma_x1 < 1, sigma_tpeak < 2 days) | 238 | 1,917 | 1,639 [85%] |
| Fit probability > 0.001 | 221 | 1,835 | 1,627 [88%] |
| Detected host galaxy | 211 | 1,806 | 1,602 [88%] |
| Spec-z from host emission lines | 211 | 1,765 | 1,563 [88%] |
| Chauvenet's criterion (4-sigma outlier rejection) | 209 | 1,757 | 1,557 [88%] |
| Valid bias correction | 204 | 1,694 | 1,541 [90%] |
| Common CIDs across systematics | 194 | **1,635** | **1,499 [91%]** |

**Additional requirements** [^539^][^409^]:
- At least 2 detections with SNR > 5 in two different bands
- At least one observation before phase +5 days after B-band peak
- Host galaxy spectroscopic redshift from OzDES or other catalogs

### 3.3 Classification Method

DES-SN5YR uses **machine learning photometric classification** rather than spectroscopic typing [^409^][^551^]:

- **Primary classifier**: SuperNNova (SNN) -- recurrent neural network [^258^]
- **Alternative classifiers**: SCONE (Qu et al. 2021) and SNIRF
- **Training**: SNN is trained on large (>100,000) samples of realistic DES-like simulations including SNe Ia, peculiar SNe Ia (91bg-like, Iax), and core-collapse SNe (II, Ib, Ic) [^551^]
- Classification probabilities P(Ia) are incorporated into the cosmological analysis via the BEAMS with Bias Correction (BBC) formalism, weighting each SN by its uncertainty and probability of being Type Ia [^409^]

### 3.4 Key Properties

| Property | Value |
|----------|-------|
| Redshift range | 0.10 < z < 1.13 |
| Number of DES SNe Ia | 1,635 |
| Number with P(Ia) > 0.5 | 1,499 (91%) |
| Total Hubble diagram (DES + low-z) | 1,829 |
| RMS Hubble residual (DES+low-z) | 0.168 mag |
| Strema et al. alpha | 0.161 |
| Stretch beta | 3.12 |
| Mass step gamma | 0.038 |

### 3.5 Classification Algorithms Detail

**SuperNNova (SNN)** [^258^][^551^]:
- Open-source framework: https://github.com/supernnova/SuperNNova
- RNN architectures: LSTM, GRU, Bayesian RNNs
- Can train on SNANA FITS format or CSV
- Supports both binary (Ia vs non-Ia) and multi-class classification
- Can use redshift as optional input feature
- Branch `SNANA_DES5yr` for DES-specific analyses
- Papers: Moller & de Boissiere 2020 (MNRAS), Moller et al. 2022 (MNRAS)

**SCONE** [^475^]:
- Alternative classifier used for systematic tests
- Different training and prediction algorithm compared to SNN
- Produces consistent classification for 90% of DES SNe

### 3.6 Classification Data Products

The `3_CLASSIFICATION/` directory contains classification probabilities for the 1,635 DES SNe from multiple algorithms [^413^], enabling:
- Cross-classifier comparison
- Systematic uncertainty estimation
- Weighted cosmological fits

---

## 4. 25 DES Mock Simulations for ML Training

### 4.1 Overview

The DES-SN5YR release includes **25 statistically independent mock simulations** of the DES sample [^456^][^344^]. These are crucial for:
- Training photometric classifiers (SuperNNova, SCONE, SNIRF)
- Computing bias corrections in BBC analysis
- Validating the cosmological pipeline
- ML model development and testing

### 4.2 Simulation Specifications

**Input cosmology** [^456^]:
- H0 = 70.0 km/s/Mpc
- Omega_Lambda = 0.685
- Omega_Matter = 0.315
- w0 = -1.0, wa = 0.0 (Flat Lambda CDM)

**Simulation components** [^456^][^475^]:
- **SNIa_SIMULATIONS/**: Type Ia supernovae generated with SALT3 SED model
- **SNnonIa_SIMULATIONS/**: Core-collapse SNe (II, Ib, Ic) and peculiar SNe (91bg-like, Iax)
- SED models for CC SNe from Vincenzi et al. 2019 and 2022 templates
- DES detection efficiency from Kessler et al. 2019
- DES spectroscopic redshift efficiency from Vincenzi et al. 2022
- Host galaxy library built from DES deep coadds by Qu et al. 2024

### 4.3 File Structure

Each of the 25 simulations contains [^477^]:
```
PIP_D5YR_SIM_V2_DATADESSIM_4D_P21-XXXX/
  ├── XXXX_HEAD.FITS.gz        (~750-800 kB)
  ├── XXXX_PHOT.FITS.gz        (~7.5-8.2 MB)
  ├── XXXX.DUMP                (~1.1 MB, text summary)
  ├── XXXX.LIST                (57 bytes)
  └── XXXX.README              (4.8 kB)
```

### 4.4 Using Simulations for ML Training

**For classification training** [^551^][^475^]:
- Simulations include normal SNe Ia, peculiar SNe Ia, and core-collapse SNe
- Training samples can be class-balanced (equal numbers of Ia and non-Ia)
- Simulations incorporate realistic observing conditions (cadence, PSF, sky noise, zero-point)
- Detection efficiencies estimated from fake SNe overlaid on images
- Includes partial light curves due to season boundaries and weather gaps

**Recommended training workflow**:
1. Generate or download DES-SN5YR simulations
2. Pre-process light curves (select time window around peak, apply quality cuts)
3. Train classifier (SNN, SCONE, or custom ML model) on simulated data
4. Validate on independent simulation test set
5. Apply trained classifier to real DES data

**For bias correction**:
- 25 simulations used to compute BEAMS with Bias Correction (BBC) corrections
- Each simulation run through full analysis pipeline (fit, classify, BBC, cosmology)
- Recovered input cosmology to under 1-sigma for both Omega_m and w [^396^]

### 4.5 Reproducing Simulations

Pippin input files for generating the simulations are in `7_PIPPIN_FILES/D5yr_sim_nominal.yml` [^456^]. All auxiliary files needed are within SNANA (available on Zenodo: https://zenodo.org/records/4015340).

---

## 5. Pippin Pipeline for Reproducibility

### 5.1 Overview

**Pippin** is a Python pipeline for end-to-end supernova cosmology analysis, designed to automate the entire workflow from data preparation to cosmological constraints [^398^][^546^][^547^]. It was developed for the DES-5YR analysis and manages the complex interconnections between SNANA components.

- **Repository**: https://github.com/Samreay/Pippin
- **Documentation**: https://pippin.readthedocs.io/en/v1.0/
- **JOSS Paper**: Hinton & Brout 2020 (DOI: 10.21105/joss.02122) [^398^]
- **Zenodo**: https://zenodo.org/records/3716116

### 5.2 Pipeline Stages

Pippin executes 10 stages in sequence [^547^]:

| Stage | Task | Description |
|-------|------|-------------|
| 0 | DATAPREP | Data preparation and formatting |
| 1 | SIM | SNANA simulation generation |
| 2 | LCFIT | Light curve fitting (e.g., SALT3) |
| 3 | CLASSIFICATION | Photometric classification (SNN, SCONE) |
| 4 | AGGREGATION | Combine results from multiple classifiers |
| 5 | MERGE | Merge data and simulation outputs |
| 6 | BIASCOR | BEAMS with Bias Correction (BBC) |
| 7 | CREATE_COV | Build statistical + systematic covariance matrix |
| 8 | COSMOFIT | Cosmological parameter fitting (CosmoMC, etc.) |
| 9 | ANALYSE | Post-processing and chain analysis |

### 5.3 Configuration

Pippin uses YAML configuration files. Example from DES-SN5YR analysis [^344^]:
```yaml
# D5yr_biascor.yml - example configuration
SIM:
  IA_G10_DES5YR:
    BASE: /path/to/sim/config
    CLASSIFIER: SuperNNova
    
LCFIT:
  SALT3_DES5YR:
    BASE: /path/to/salt3/model
    
BIASCOR:
  BBC_DES5YR:
    SIMFILE_BIASCOR: $SIM_IA_G10_DES5YR
    SIMFILE_CCPRIOR: $SIM_CC_DES5YR
    
COSMO:
  wCDM:
    BASE: /path/to/cosmomc/config
```

### 5.4 Key Features for ML

- **Automated simulation generation**: Configurable SN Ia, CC SNe, and peculiar SN simulations
- **Classification integration**: Built-in support for SuperNNova, SCONE, and custom classifiers
- **Multi-core processing**: Parallel execution on clusters (Midway, Perlmutter, etc.)
- **Systematic variation handling**: ~100 systematic variations via command-line overrides
- **End-to-end reproducibility**: Single config file produces complete cosmology results

### 5.5 Integration with ML Workflows

Pippin is designed to incorporate ML at multiple stages [^538^][^552^]:
- **Classification stage**: Train/evaluate photometric classifiers (SNN, SCONE, SNIRF)
- **Simulation stage**: Generate training samples for classifier development
- **BEAMS/BBC stage**: Weight SNe by classification probability P(Ia)

---

## 6. How to Download and Work with the Zenodo Release

### 6.1 Direct Download

The Zenodo record is at **https://zenodo.org/records/12720778** [^477^]:

```bash
# Download the complete release
wget https://zenodo.org/records/12720778/files/DES-SN5YR-1.2.zip?download=1

# Unzip
unzip DES-SN5YR-1.2.zip

# Set environment variable for DES-SN-DR package
export DES5YRDR_DATA_ROOT='<path_to_unzipped>'
export DES5YRDR_DATA='<path_to_unzipped>/DES-SN5YR'
```

### 6.2 Data Product Details

**Light curve files** [^477^]:
- `DES-SN5YR_DES_HEAD.FITS.gz` (2.9 MB): HEAD file for 19,706 SMP light curves
- `DES-SN5YR_DES_PHOT.FITS.gz` (66.1 MB): PHOT file with all observations
- `DES-SN5YR_Foundation_HEAD/PHOT.FITS.gz` (19.3 kB / 100.6 kB): Foundation DR3 sample
- `DES-SN5YR_LOWZ_HEAD/PHOT.FITS.gz` (36.8 kB / 495.1 kB): Low-z sample (CfA/CSP/others)

**Classification files**:
- Classification probabilities for 1,635 SNe from SuperNNova, SCONE, SNIRF

**Distance/Covariance files**:
- Hubble diagram data vector (zHD, MU) for 1,829 SNe
- STAT-only covariance matrix
- STAT+SYST covariance matrix
- Individual systematic covariance matrices

**Simulation files**:
- 25 independent DES mock simulations
- SNIa + non-Ia simulations in SNANA FITS format

### 6.3 Python Quick Start

```python
import sncosmo
from astropy.io import fits
import matplotlib.pyplot as plt

# Read DES light curves
head_file = 'DES-SN5YR-1.2/0_DATA/DES-SN5YR_DES_HEAD.FITS.gz'
phot_file = 'DES-SN5YR-1.2/0_DATA/DES-SN5YR_DES_PHOT.FITS.gz'

# Using sncosmo (returns list of astropy Tables)
sne = sncosmo.read_snana_fits(head_file, phot_file)

# Get first supernova
sn = sne[0]
print(f"SNID: {sn.meta['SNID']}")
print(f"Redshift: {sn.meta['REDSHIFT_FINAL']}")
print(f"Host logmass: {sn.meta.get('HOSTGAL_LOGMASS', 'N/A')}")

# Plot light curve
for band in set(sn['BAND']):
    mask = sn['BAND'] == band
    plt.errorbar(sn['MJD'][mask], sn['FLUXCAL'][mask], 
                 yerr=sn['FLUXCALERR'][mask], label=band, fmt='o')
plt.xlabel('MJD')
plt.ylabel('FLUXCAL')
plt.legend()
plt.show()

# Filter for cosmology sample (SALT3-fit converged, etc.)
cosmo_sne = [sn for sn in sne 
             if sn.meta.get('SNTYPE', 0) == 1  # Type Ia
             and sn.meta.get('REDSHIFT_FINAL', -9) > 0.1]
```

---

## 7. DES Difference Imaging Photometry Methods (DiffImg vs SMP)

### 7.1 Overview

The DES-SN5YR data release provides photometry from **two independent pipelines** [^395^][^394^]:
- **DiffImg**: Real-time forced PSF photometry on difference images (used during survey operations)
- **SMP (Scene Modeling Photometry)**: Forward-modeling photometry on search images (post-survey reprocessing)

### 7.2 DiffImg Pipeline

**Characteristics** [^395^][^394^]:
- Uses Difference Image Analysis (DIA) with deep template images from science verification
- PSF fitting photometry on coadded difference images
- Real-time processing for transient discovery
- Zero-points from science verification tertiary standard star catalog
- Template images from early survey period under good conditions
- Photonometric precision: ~2%
- **Total candidates**: 31,636 light curves

**Limitations**:
- Uses MAG_AUTO for tertiary star photometry (less accurate than PSF fitting)
- No correction for stellar proper motions over 5-year survey
- Average position across all bands (ignores atmospheric chromatic effects)
- Less optimized for cosmology

### 7.3 SMP (Scene Modeling Photometry)

**Characteristics** [^395^][^400^]:
- Forward models time-varying SN flux + static host galaxy flux simultaneously
- Individual reference images selected for best quality (seeing, PSF, sky)
- Updated Y6 forward model global calibration
- Forced-position PSF fitting for tertiary stars with proper motion corrections
- Accounts for differential chromatic refraction (DCR) per filter
- Transient position fitted (not fixed)
- Photonometric precision: better than DiffImg (~reduced scatter)
- **Total light curves**: 19,706 (convergence rate ~62% of DiffImg candidates)
- **Cosmology sample**: 1,635 SNe Ia

**Key improvements over DiffImg** [^395^]:

| Feature | DiffImg | SMP |
|---------|---------|-----|
| Template | Science verification images | Best quality from full survey |
| Zero-point catalog | SV catalog | Y6 forward model calibration |
| Tertiary star photometry | MAG_AUTO | PSF fitting |
| Proper motion correction | None | Linear fit over 5 years |
| Astrometry | SV solution | Updated (Bernstein et al. 2017) |
| Transient position | Fixed average | Fitted per filter |
| Host galaxy profile | From template | Model from all epochs |
| Flux measurement | DIA + forced-PSF | Forward model |
| DCR correction | None | Per-filter, per-epoch |

### 7.4 Comparison

Sanchez et al. 2024 demonstrates that SMP photometry has [^395^]:
- Smaller scatter about SALT3 model fits across all bands and redshift ranges
- Reduced sensitivity to host-galaxy surface brightness anomaly
- Higher quality light curves, increasing cosmology sample size from 1,499 (DiffImg) to 1,635 (SMP)

### 7.5 Data Release Contents

The `0_DATA/` directory includes [^439^]:
- SMP photometry for DES, Foundation, and Low-z samples in SNANA FITS format
- `DES5YR_SALT3_LCFIT.LCPLOT.gz`: Light curve plots from SALT3 fitting
- Flux calibration: FLUXCAL with fixed standard zero-point of 27.5

---

## 8. Host Galaxy Data Available for DES SNe

### 8.1 Overview

Host galaxy information is a critical component of the DES-SN5YR analysis, providing [^395^][^409^]:
- Spectroscopic redshifts (primary redshift source)
- Host stellar masses (for mass step correction)
- Host colors and star formation rates
- Photometric properties

### 8.2 Host Galaxy Catalog Sources

**Primary catalogs**:
- **Wiseman et al. 2020**: Deep coadded DES images with photometry and stellar masses [^395^]
- **Qu et al. 2024**: Updated galaxy catalog from DES-SN field coadds, including photometric redshifts from self-organizing maps (SOM) [^416^]
- **OzDES**: Spectroscopic redshifts from the Australian Dark Energy Survey [^394^]

### 8.3 Host Properties Available

For each DES SN, the following host galaxy data is provided in the HEAD FITS files [^439^]:

| Property | Description | Source |
|----------|-------------|--------|
| `HOSTGAL_SPECZ` | Spectroscopic redshift | OzDES + external |
| `HOSTGAL_PHOTOZ` | Photometric redshift (mean of PDF) | SOM algorithm |
| `HOSTGAL_ZPHOT_Q[PPP]` | Redshift at PPP-th percentile of zPDF | SOM algorithm |
| `HOSTGAL_LOGMASS` | log10(stellar mass / solar masses) | SED fitting |
| `HOSTGAL_LOGSFR` | log10(star formation rate) | SED fitting |
| `HOSTGAL_MAG_[band]` | Host galaxy magnitudes (ugrizY) | DES deep coadds |
| `HOSTGAL_MAGERR_[band]` | Magnitude uncertainties | - |
| `HOSTGAL_SB_FLUXCAL_[band]` | Surface brightness at SN location | - |
| `HOSTGAL_SNSEP` | SN-host separation (arcsec) | - |
| `HOSTGAL_DDLR` | Distance in distance-light-radii | - |
| `HOSTGAL_OBJID` | Galaxy identifier | - |

**Photo-z quality**: sigma_68 = 0.124, outlier fraction = 0.015-0.017 for deep/shallow fields [^416^]

### 8.4 Host-SN Correlations

DES-SN5YR analysis includes several host galaxy correlations [^409^][^422^]:
- **Mass step**: SNe Ia in high-mass hosts are brighter after standardization (Sullivan et al. 2010)
- **Color step**: Host u-r color as alternative tracer (Wiseman et al. 2022)
- **Dust properties**: Host galaxy R_V and A_V correlate with SN color and Hubble residuals [^422^]
- **Selection effects**: Spectroscopic redshift requirement introduces strong mass-dependent selection effects at high redshift [^409^]

### 8.5 Host Galaxy Mismatch

Qu et al. 2024 and Palanque-Delabrouille et al. 2024 studied host galaxy association [^416^]:
- ~0.5% of 1,635 SNe have uncertain host assignments
- Host mismatch introduces negligible cosmological bias (Delta_w = 0.0013 +/- 0.0026)
- Alternative methods: DELIGHT (deep learning) and GHOST (gradient ascent) available for future analyses

---

## 9. DES Early-Type Host Galaxy SN Survey (DES-DEFT)

### 9.1 Overview

The DES Early-Type Host Galaxy SN Survey (DES-DEFT) is a dedicated spectroscopic follow-up program targeting SNe Ia in early-type (elliptical and lenticular) host galaxies. These SNe are particularly valuable because:
- Early-type galaxies have minimal dust content, providing "standard" SNe Ia
- Reduced dust systematics improve cosmological constraints
- Host stellar populations are older and more uniform

### 9.2 Key Papers and Results

**Wiseman et al. 2021** (MNRAS, 506, 330) [^543^]:
- Derived SN Ia rate from DES: 2.6 +/- 0.05 x 10^-13 yr^-1 M_sun^-1
- SN Ia rates as a function of host galaxy stellar mass
- Delay time distribution measurements

**Wiseman et al. 2022** (MNRAS, 515, 4587) [^475^]:
- Host galaxy u-r color as driver of SN Ia correlations
- Alternative "color step" to the traditional mass step

**Wiseman et al. 2023** (MNRAS, 520, 6214) [^475^]:
- SN Ia rates and delay times in DES
- Comprehensive analysis of host galaxy properties

### 9.3 Host Galaxy Selection

The DES host galaxy catalog uses [^395^][^416^]:
- DES deep coadded images for photometry
- SED fitting with BAGPIPES or similar codes for stellar masses
- Spectroscopic redshifts from OzDES
- Photometric redshifts from self-organizing maps for galaxies without spec-z

### 9.4 Data Availability

Host galaxy data is embedded in the SNANA HEAD FITS files [^439^]:
- Stellar masses, SFRs, magnitudes, and redshifts available for each SN
- Low-z host galaxy properties remeasured using hostphot package for consistency

---

## 10. SNANA Format and Reading DES Data with sncosmo

### 10.1 SNANA Software

**SNANA** (SuperNova ANAlysis) is the primary software framework for DES supernova analysis [^554^][^257^]:
- **Repository**: https://github.com/RickKessler/SNANA
- **Manual**: https://github.com/RickKessler/SNANA/blob/master/doc/snana_manual.pdf [^470^]
- **Tutorial**: https://kicp.uchicago.edu/~kessler/SNANA_Tutorial/SNANA_Tutorial_2023-05.pdf
- **SNDATA_ROOT** (public data/filters/models): https://zenodo.org/records/12655677 (~2 GB)
- **Starter Kit**: https://snana-starterkit.readthedocs.io/ [^469^]

### 10.2 SNANA FITS Format Specification

The DES-SN5YR data uses SNANA's standard FITS format with two paired files [^439^][^456^]:

**HEAD file**: One row per SN, metadata + pointers to PHOT file
**PHOT file**: One row per observation, all light curves concatenated

Pointer system:
- `PTROBS_MIN` and `PTROBS_MAX` in HEAD file point to rows in PHOT file
- `MJD = -777` marks end of each light curve in PHOT file

### 10.3 Reading DES Data with sncosmo

**sncosmo** (https://sncosmo.github.io/) is the recommended Python library [^33^]:

```python
import sncosmo
import numpy as np
import matplotlib.pyplot as plt

# Read all SN from DES-SN5YR
head_file = 'DES-SN5YR_DES_HEAD.FITS.gz'
phot_file = 'DES-SN5YR_DES_PHOT.FITS.gz'
sne = sncosmo.read_snana_fits(head_file, phot_file)

# Read specific SNe only
specific_sne = sncosmo.read_snana_fits(head_file, phot_file, 
                                        snids=['DES16C2nm', 'DES16E2bp'])

# Read first 100 SNe only (for testing)
sample = sncosmo.read_snana_fits(head_file, phot_file, n=100)

# Access a single supernova - returns astropy Table
sn = sne[0]

# Metadata (redshift, coordinates, host properties, etc.)
print(sn.meta)
# OrderedDict with keys: SNID, RA, DEC, REDSHIFT_FINAL, 
#   HOSTGAL_LOGMASS, HOSTGAL_MAG_g, etc.

# Photometry columns
print(sn.colnames)
# ['MJD', 'BAND', 'CCDNUM', 'IMGNUM', 'FIELD', 'PHOTFLAG', 
#  'PHOTPROB', 'FLUXCAL', 'FLUXCALERR', 'PSF_SIG1', 'SKY_SIG', 
#  'ZEROPT', 'GAIN', 'XPIX', 'YPIX']

# Convert to sncosmo format for model fitting
data = sncosmo.load_example_data()  # template
```

### 10.4 Using sncosmo for Light Curve Fitting

```python
import sncosmo

# Read DES data
sne = sncosmo.read_snana_fits(head_file, phot_file)
sn = sne[0]

# Convert to sncosmo photometric data table
from astropy.table import Table
import astropy.units as u

data = Table({
    'time': sn['MJD'],
    'band': sn['BAND'],
    'flux': sn['FLUXCAL'],
    'fluxerr': sn['FLUXCALERR'],
    'zp': 27.5 * np.ones(len(sn)),
    'zpsys': ['ab'] * len(sn)
})

# Create SALT3 model and fit
model = sncosmo.Model(source='salt3')
model.set(z=sn.meta['REDSHIFT_FINAL'])

result, fitted_model = sncosmo.fit_lc(
    data, model, ['t0', 'x0', 'x1', 'c'],
    bounds={'x1': (-3, 3), 'c': (-0.3, 0.3)}
)

print(f"x1 = {result.parameters[2]:.3f}")
print(f"c = {result.parameters[3]:.3f}")

# Plot fit
sncosmo.plot_lc(data, model=fitted_model, errors=result.errors)
```

### 10.5 SNANA ASCII .DAT Format

For simulations, SNANA also supports an ASCII format (one file per SN):
```
SURVEY: DES
SNID: 12345
RA: 45.1234
DECL: -23.4567
REDSHIFT_HELIO: 0.5234
MWEBV: 0.023
...

# Observations:
VARNAMES: MJD BAND FLUXCAL FLUXCALERR ZP ...
OBS: 57400.12 g 1234.5 23.4 27.5 ...
OBS: 57400.12 r 2345.6 34.5 27.5 ...
...
END:
```

Read with:
```python
import sncosmo
meta, tables = sncosmo.read_snana_ascii('SN12345.DAT')
```

### 10.6 Reading FITRES Files

The FITRES output from SNANA light curve fitting [^469^]:
```python
# Read FITRES text file
def read_fitres(filename):
    with open(filename) as f:
        lines = f.readlines()
    
    # Find VARNAMES line
    for i, line in enumerate(lines):
        if line.startswith('VARNAMES:'):
            varnames = line.split()[1:]
            break
    
    # Read SN lines
    data = []
    for line in lines[i+1:]:
        if line.startswith('SN:'):
            data.append(line.split()[1:])
    
    import pandas as pd
    df = pd.DataFrame(data, columns=varnames)
    return df

# Or use txtobj from SNANA starter kit
from util.txtobj import txtobj
fr = txtobj('PS1MD.FITRES.TEXT', fitresheader=True)
```

---

## Summary: ML-Readiness Assessment

| Dataset | Format | Size | ML-Readiness | Notes |
|---------|--------|------|--------------|-------|
| DES SMP light curves | SNANA FITS (HEAD+PHOT) | 66 MB | **High** | Use sncosmo.read_snana_fits() |
| DES DiffImg light curves | SNANA FITS | ~120 MB | **Medium** | Lower quality than SMP |
| 25 Mock simulations | SNANA FITS | ~200 MB each | **High** | Perfect for training classifiers |
| Classification probs | ASCII/FITS | ~100 KB | **High** | Multiple classifiers included |
| Hubble diagram + covmat | ASCII/FITS | ~50 MB | **High** | Ready for cosmology |
| Host galaxy properties | Embedded in HEAD FITS | Included above | **High** | Mass, SFR, color, redshift |
| SALT3 model | Proprietary | ~50 MB | **Medium** | Use via sncosmo or SNANA |
| Pippin config files | YAML | ~1 MB | **High** | Full reproducibility |

### Recommended ML Workflows

1. **Photometric Classification**:
   - Download simulations from `1_SIMULATIONS/`
   - Use sncosmo.read_snana_fits() to load training data
   - Train with SuperNNova, SCONE, or custom architecture
   - Evaluate on held-out simulations
   - Apply to real DES data in `0_DATA/`

2. **Light Curve Anomaly Detection**:
   - Use 25 independent simulations as "normal" samples
   - Train autoencoder or flow-based model
   - Detect anomalies in real data

3. **Cosmological Parameter Estimation**:
   - Use Hubble diagram data + covariance from `4_DISTANCES_COVMAT/`
   - Train neural posterior estimator (simulation-based inference)
   - Validate on 25 mock simulations from `5_COSMOLOGY/`

4. **Host Property Prediction**:
   - Extract host galaxy features from HEAD files
   - Train regression model to predict host mass from SN properties
   - Study mass step and environmental dependencies

---

## References

Key papers to cite when using DES-SN5YR data:

1. DES Collaboration 2024 (ApJL, 973, L14) - Key cosmology paper [^407^]
2. Vincenzi et al. 2024 (ApJ, 975, 86) - Cosmology analysis and systematics [^409^]
3. Sanchez et al. 2024 (ApJ, 975, 5) - Light curves and 5-year data release [^395^]
4. Moller et al. 2022 (MNRAS) - Photometric classification [^551^]
5. Hinton & Brout 2020 (JOSS) - Pippin pipeline [^398^]
6. Kessler et al. 2009 (PASP) - SNANA [^554^]

---

*Research compiled: 2025-06*
*Last updated with DES-Dovekie reanalysis information*

# Dimension 10: Software Frameworks & ML Pipelines for Supernova Research

## Executive Summary

This document provides a comprehensive survey of software frameworks and machine learning pipelines for supernova (SN) research. We cover 10+ major tools spanning light curve simulation, fitting, classification, spectral analysis, and broker deployment. The landscape has matured significantly, with Python-based tools dominating and deep learning becoming the standard for classification tasks. Integration patterns are emerging that connect simulation (sncosmo/SNANA) → classification (SuperNNova/ParSNIP/SCONE) → broker deployment (Fink/ALeRCE/AMPEL) into end-to-end automated pipelines.

---

## Table of Contents

1. [sncosmo](#1-sncosmo)
2. [SuperNNova](#2-supernnova)
3. [ParSNIP](#3-parsnip)
4. [snmachine](#4-snmachine)
5. [SNANA](#5-snana)
6. [LightCurveLynx](#6-lightcurvelynx)
7. [MOSFiT](#7-mosfit)
8. [SNID & SNID-SAGE](#8-snid--snid-sage)
9. [BTSbot](#9-btsbot)
10. [RAPID](#10-rapid)
11. [Other Notable Frameworks](#11-other-notable-frameworks)
12. [Integration Patterns](#12-integration-patterns)
13. [Broker Ecosystem](#13-broker-ecosystem)
14. [Summary Comparison Table](#14-summary-comparison-table)

---

## 1. sncosmo

**Description**: sncosmo is the foundational Python library for supernova cosmology analysis, providing tools for simulating, fitting, and typing supernova light curves. It is built on NumPy, SciPy, and AstroPy and serves as the de facto standard for SN light curve analysis in Python. [^746^]

### Key Features
- **Light curve fitting**: SALT2, SALT3, MLCS2k2, and other built-in models
- **Bandpass management**: Registry of 100+ built-in bandpasses from major surveys (SDSS, DES, HST, JWST, LSST, etc.)
- **Magnitude systems**: AB, Vega, and custom magnitude systems
- **Simulation**: `realize_lcs()` for generating synthetic light curves from models
- **Registry system**: Extensible registry for custom sources, bandpasses, and magnitude systems
- **SNANA FITS I/O**: Built-in support for reading/writing SNANA-format FITS files [^540^]

### Installation
```bash
pip install sncosmo
# or
conda install -c conda-forge sncosmo
```

### Data Formats
- Photometric data tables with required columns: `time`, `band`, `flux`, `fluxerr`, `zp`, `zpsys`
- Spectral data: phase vs. wavelength grids
- SNANA FITS format via `read_snana_fits()` / `write_snana_fits()`

### Built-in Models
- **SALT2Source**: Primary Type Ia model (Guy et al. 2007, 2010) - spectral time series with x0, x1, c parameters
- **SALT3Source**: Updated SALT model (Kenworthy et al. 2021)
- **MLCS2k2Source**: Alternative Type Ia model
- **TimeSeriesSource**: Generic spectral time series
- **StretchSource**: Time-stretched spectral model
- **Nugent models**: Built-in models for core-collapse SNe (Ibc, IIP, IIn, IIL)

### Bandpass Coverage
The built-in registry includes bandpasses from: SDSS, DES, HST (ACS, WFC3), JWST, LSST, ZTF, Pan-STARRS, CFHT, UKIRT, Spitzer, Kepler, TESS, and many more. [^542^]

### API Highlights
```python
import sncosmo
# Create a SALT2 model
model = sncosmo.Model(source='salt2')
model.set(z=0.5, t0=55000., x0=1e-5, x1=0.5, c=0.2)
# Fit light curve
result, fitted_model = sncosmo.fit_lc(data, model, ['z', 't0', 'x0', 'x1', 'c'])
# Simulate observations
sne = sncosmo.realize_lcs(observations, model, params_list)
```

### Citation & Authority
- Author: Kyle Barbary et al.
- Paper: Barbary et al. (2016) - ApJS [^35^]
- GitHub: https://github.com/sncosmo/sncosmo
- Documentation: https://sncosmo.readthedocs.io/
- **Citations: 118+ (ADS)**

### ML-Readiness
- **Essential infrastructure**: All Python ML pipelines depend on sncosmo for data I/O and model fitting
- **AstroPy integration**: Seamless integration with the Python astronomy ecosystem
- **Extensible**: Custom models and bandpasses can be registered at runtime

---

## 2. SuperNNova

**Description**: SuperNNova is an open-source photometric time-series classification framework using recurrent neural networks (RNNs). It is the standard deep learning classifier for SN cosmology and is integrated into the PIPPIN end-to-end cosmology pipeline. [^258^]

### Key Features
- **RNN architectures**: LSTM, GRU, and Bayesian RNNs for uncertainty quantification
- **Multi-class classification**: Binary (Ia vs. non-Ia) or multi-class (Ia, II, Ibc, IIn, SLSN-I)
- **Early classification**: >86% accuracy 2 days before maximum light without redshift
- **Redshift-optional**: 96.9% accuracy without redshift; 99.6% with redshift
- **Bayesian RNNs**: Provides well-calibrated uncertainty estimates via variational dropout
- **Scalable**: Handles millions of simulated light curves efficiently

### Installation
```bash
pip install supernnova
# or
git clone https://github.com/supernnova/supernnova.git
```

### Input Formats
- CSV files with photometric time series
- SNANA FITS format
- sncosmo-compatible data tables

### Training Data
- Zenodo-hosted preprocessed datasets for DES-5yr analyses
- DES simulations (Vincenzi et al. 2019, Kessler et al. 2019)
- PLAsTiCC simulations

### Architecture Details
- **LSTM/GRU**: Standard recurrent layers for temporal modeling
- **Bayesian variant**: Variational inference over network weights for uncertainty estimation
- **Features**: Raw light curves + optional redshift/host features
- **Preprocessing**: Flux normalization, time windowing, filter encoding

### Performance
| Metric | Without Redshift | With Redshift |
|--------|-----------------|-----------------|
| Ia vs. non-Ia accuracy | 96.9 +/- 0.1% | 99.6 +/- 0.1% |
| Early (2d pre-max) | >86% | >93% |

### Integration
- Part of **PIPPIN** pipeline (Hinton & Brout 2020)
- Used by **DES** collaboration for cosmology analyses
- Compatible with **Fink** broker

### Citation & Authority
- Paper: Möller & de Boissière (2020), MNRAS, 491, 4277 [^256^]
- GitHub: https://github.com/supernnova/SuperNNova
- Documentation: https://supernnova.readthedocs.io
- **Citations: 100+**

### Papers Using SuperNNova
- Möller et al. (2022) MNRAS - DES 5-year analysis
- Möller et al. (2024) MNRAS
- Vincenzi et al. (2023) MNRAS
- DES Collaboration (2024) ApJ

---

## 3. ParSNIP

**Description**: ParSNIP (Parsimonious Normalizing-flow Informed transient Prediction) is a generative model for transient light curves that uses a physics-enabled variational autoencoder (VAE) architecture. It produces a low-dimensional, redshift-invariant latent representation that can be used for classification, anomaly detection, and distance estimation. [^79^]

### Key Features
- **Generative model**: Learns to predict time-varying spectra from photometric data only
- **Redshift-invariant representation**: Classification works even with biased training sets
- **Anomaly detection**: Identifies previously-unobserved transient types
- **Distance estimation**: RMS of 0.150 +/- 0.007 mag for SNe Ia (comparable to SALT2)
- **Model uncertainties**: 0.04-0.06 mag on out-of-sample multiband light curves
- **3D intrinsic model**: Captures intrinsic diversity with low-dimensional latent space

### Installation
```bash
# Note: The 'parsnip' PyPI name may conflict with a different package
# Install from source:
git clone https://github.com/kboone/parsnip.git
cd parsnip
pip install .
```

### Architecture
- **Encoder**: Neural network maps light curve → latent parameters
- **Physics model**: Explicit model of light propagation (redshift, extinction, K-corrections)
- **Decoder**: Reconstructs time-varying spectral energy distribution
- **Latent space**: 3D intrinsic representation that is invariant to redshift

### Performance
- **PLAsTiCC**: 2.3x less contamination than state-of-the-art for SNIa classification
- **Pan-STARRS1**: 2x less contamination on real data
- **Anomaly detection**: 90% pure sample of novel transients

### Integration
- Integrated into **AMPEL** broker workflows for ELAsTiCC
- Used in **PIPPIN** pipeline
- Compatible with sncosmo for model I/O

### Citation & Authority
- Paper: Boone (2021), AJ, 162, 275 [^79^]
- GitHub: https://github.com/kboone/parsnip
- **Citations: 50+**

---

## 4. snmachine

**Description**: snmachine is a flexible Python library developed by the LSST DESC collaboration for reading photometric SN light curves, extracting features, and performing supervised machine learning classification. It was one of the first comprehensive SN ML frameworks. [^407^] [^900^]

### Key Features
- **Feature extraction**: Wavelet decomposition, parametric model fitting, SALT2 template fitting
- **Gaussian Process modeling**: 2D GP regression in time and wavelength
- **Multiple classifiers**: KNN, SVM, ANN, Boosted Decision Trees, Naive Bayes
- **Wavelet features**: Stationary Wavelet Transform with PCA dimensionality reduction
- **Survey-agnostic**: Designed for LSST but adaptable to other surveys

### Installation
```bash
pip install snmachine
# or from source:
git clone https://github.com/LSSTDESC/snmachine.git
```

### Architecture Pipeline
1. **Data ingestion**: `sndata` module reads SNANA FITS, ASCII, or custom formats
2. **Preprocessing**: GP interpolation onto regular time grid
3. **Feature extraction**: Wavelet decomposition → PCA to 40 components
4. **Classification**: GBDT/SVM/ANN on wavelet features + redshift

### Feature Extraction Details
- **Wavelet transform**: 2-level decomposition using symlet wavelets
- **PCA reduction**: 7008 wavelet coefficients → 40 principal components
- **Time grid**: ~292 points (approximately daily sampling over 295 days)
- **Additional features**: Host galaxy photometric redshift and uncertainty

### Performance
- SPCC dataset: AUC ~0.96 with representative training sample
- Performance strongly depends on training set representativeness
- SALT2 template fitting features competitive with wavelet features

### Limitations
- DESC collaboration access policy for non-DESC use
- Designed primarily for completed light curves, not real-time classification
- GBDT classifier requires careful hyperparameter tuning

### Citation & Authority
- Paper: Lochner et al. (2016), ApJS, 225, 31
- GitHub: https://github.com/LSSTDESC/snmachine
- Documentation: https://lsstdesc.org/snmachine/
- **Citations: 291+**

---

## 5. SNANA

**Description**: SNANA is the comprehensive C++/Fortran simulation and analysis package for supernova cosmology. It has been the workhorse for major SN surveys (SDSS, SNLS, DES, Pantheon, LSST) for over a decade and provides the simulation infrastructure that underlies most SN ML training. [^254^]

### Key Features
- **Simulation engine**: `snlc_sim.exe` generates realistic light curves at ~100/sec/core
- **Light curve fitting**: `snlc_fit.exe` for SALT2/MLCS2k2 parameter estimation
- **Bias correction**: BEAMS with Bias Correction (BBC) for cosmology
- **Photometric classification**: `PSNID` for typing without spectra
- **Systematic error propagation**: Built-in framework for calibration uncertainties
- **Python wrappers**: Build Your Own SED (BYOSED) model allows Python model injection

### Installation
```bash
# Clone source
git clone https://github.com/RickKessler/SNANA.git
cd SNANA
# Build with autotools
autoreconf -fi
./configure
cd src && make
```

### SNDATA_ROOT
The companion data repository (~1.7 GB) contains: [^310^]
- Public light curve datasets (SDSS, SNLS, DES, Foundation, Pantheon+)
- Filter transmission curves for 50+ instruments
- SED models (SALT2, SALT3, CC templates)
- Calibration files and zero points
- Host galaxy libraries
- Survey cadence/simlib files

Download: https://zenodo.org/records/12655677

### Simulation Capabilities
- 117 million light curves in 8 hours on 40 cores (PLAsTiCC-scale)
- Arbitrary survey configurations via `SIMLIB` files
- Realistic observing conditions (PSF, sky noise, zero points)
- Host galaxy extinction and Milky Way dust
- Selection effects and detection thresholds

### Python Integration
- **BYOSED**: Python model interface called from C++ simulation
- **PIPPIN**: Python pipeline orchestrating SNANA workflows
- **SNCosmo bridge**: sncosmo reads SNANA FITS natively

### Citation & Authority
- Paper: Kessler et al. (2009), ApJS, 185, 32
- GitHub: https://github.com/RickKessler/SNANA
- Tutorial: https://kicp.uchicago.edu/~kessler/SNANA_Tutorial/SNANA_Tutorial_2023-05.pdf
- **Citations: 1000+**

---

## 6. LightCurveLynx

**Description**: LightCurveLynx is a modern, flexible Python framework for forward modeling of time-domain light curves. Developed by the LINCC Frameworks team, it is designed to meet the needs of the Rubin/LSST era with modular architecture and support for multiple physical models. [^377^] [^752^]

### Key Features
- **Forward modeling**: End-to-end simulation from parameter distributions to observed photometry
- **Modular architecture**: DAG-based parameter models, pluggable physical models
- **Survey-aware**: Uses real ObsTables/OpSim files for realistic cadence
- **Multiple model support**: Wraps SNCosmo, PZFlow, Redback
- **Extensible**: Easy to add new model types, effects, and instruments
- **Nested Pandas**: Built on modern dataframe infrastructure

### Installation
```bash
pip install lightcurvelynx
# or for development:
git clone https://github.com/lincc-frameworks/lightcurvelynx.git
pip install -e .'[dev]'
```

### Architecture
```
Parameter Models (DAG) → Physical Model → ObsTable → Effects → Light Curves
```

### Wrapped Packages
- **SNCosmo**: SALT2/SALT3 SED models
- **PZFlow**: Data-driven parameter distributions
- **Redback**: Multi-messenger transient models

### Performance
- ZTF SN Ia DR2 simulation: KL divergence ~0.01-0.02 for parameter distributions
- Hubble diagram completeness matches data (z < 0.06)
- Excellent agreement in noise properties

### Citation & Authority
- Paper: Dai et al. (2026), arXiv:2604.07134 [^752^]
- GitHub: https://github.com/lincc-frameworks/lightcurvelynx (now tdastro)
- Documentation: https://lightcurvelynx.readthedocs.io/

---

## 7. MOSFiT

**Description**: MOSFiT (Modular Open Source Fitter for Transients) is a Python package for fitting, sharing, and estimating parameters of transients via user-contributed models. It is deeply integrated with the Open Astronomy Catalogs. [^763^]

### Key Features
- **Physical model fitting**: MCMC-based fitting with emcee sampler
- **Open Catalogs integration**: Automatic data download from OSC, OTC, ONC
- **User-contributed models**: Community-extensible model library
- **Multi-wavelength**: Supports optical, IR, UV, radio, X-ray data
- **Model sharing**: Optional upload of fits back to Open Catalogs
- **Parallel execution**: MPI support for large-scale fitting

### Installation
```bash
pip install mosfit
# or
conda install -c conda-forge mosfit
```

### Built-in Models
- `slsn`: Superluminous supernova model
- `ic`: Interacting core-collapse model
- `tde`: Tidal disruption event model
- ` magnetar `: Magnetar-powered model
- ` rprocess `: Kilonova/r-process model
- And many more user-contributed models

### Usage
```bash
# Fit a SLSN model to a transient
mosfit -m slsn -e PTF11dij
# Fit with private data
mosfit -e my_data.dat -m ic
# Upload results to Open Catalogs
mosfit -e SN2023A -m slsn -u
```

### Data Formats
- JSON (Open Catalog Schema)
- ASCII tables (auto-conversion with interactive prompts)
- CDS, LaTeX table formats

### Citation & Authority
- Paper: Guillochon et al. (2018), ApJS, 236, 6 [^901^]
- GitHub: https://github.com/guillochon/MOSFiT
- Documentation: https://mosfit.readthedocs.io/
- **Citations: 100+**

---

## 8. SNID & SNID-SAGE

### 8.1 Original SNID

**Description**: SNID (SuperNova IDentification) is the classic spectral classification tool for SNe. It uses cross-correlation techniques (Tonry & Davis 1979) to determine redshift, type, and age from observed spectra. [^755^]

**Key Features**:
- Cross-correlation with template library of 5000+ spectra
- Redshift, type, and age determination
- Interactive plotting with PGPLOT
- Extensive template sets (BSNIP, Modjaz et al., Gutierrez et al., Super-SNID)

**Installation**: Download and compile from source
- Download: https://people.lam.fr/blondin.stephane/software/snid/
- Version 5.0, templates-2.0

**Citation**: Blondin & Tonry (2007), ApJ, 666, 1024

### 8.2 SNID-SAGE (Modern Python Replacement)

**Description**: SNID-SAGE is a Python-based modern framework for supernova spectral classification that builds on the SNID cross-correlation methodology with practical and methodological refinements for survey-scale use. [^753^] [^754^]

**Key Features**:
- **698 templates**: Ia, Ib, Ic, II, SLSN, TDE, KN, and more
- **Python/PySide6 GUI**: Interactive interface with real-time plotting
- **CLI**: Single-spectrum and batch processing
- **New match-quality metric**: Optimized cross-correlation engine
- **Redshift-space clustering**: Consolidates template matches into stable classifications
- **AI assistant**: Optional LLM-powered analysis via OpenRouter
- **Validation**: ~46,000 WISeREP spectra classified

**Installation**:
```bash
pip install snid-sage
```

**Citation**: Strocchi et al. (2025), A&A [^753^]
- GitHub: https://github.com/FiorenSt/SNID-SAGE
- Documentation: https://fiorenst.github.io/SNID-SAGE/

---

## 9. BTSbot

**Description**: BTSbot is a multi-modal convolutional neural network that automates the entire bright transient discovery, identification, and follow-up pipeline for the Zwicky Transient Facility Bright Transient Survey. It achieved the first fully automated discovery-to-classification of a supernova. [^888^] [^898^]

### Key Features
- **Multi-modal CNN**: Processes image cutouts + 25 extracted metadata features
- **Real-time operation**: Integrated into Fritz/Kowalski (ZTF broker)
- **Autonomous follow-up**: Automatically requests SEDM spectroscopy
- **High purity**: 93-96% of selected sources are real extragalactic transients
- **Speed**: ~1 hour faster than human scanners
- **Completeness**: 99% (vs. 95% for human scanners)

### Architecture
- **Image encoder**: ConvNeXt or MaxViT backbone
- **Metadata encoder**: 25 features (position, magnitude, shape, etc.)
- **Fusion layer**: Combines image and metadata representations
- **Output**: Bright transient score (binary classification)

### Installation
```bash
pip install btsbot
```

### Model Availability
- Pre-trained models on HuggingFace Hub
- Auto-download on first use
- Galaxy Zoo pre-training for transfer learning

### Performance
- Selected 609 sources (Dec 2023 - May 2024), 96% real extragalactic transients
- Contributed to first fully automated SN discovery-to-classification
- Discovered SN 2024jlf with follow-up at +0.7 days after first light

### Citation & Authority
- Paper: Rehemtulla et al. (2024), ApJ, 972, 7 [^888^]
- GitHub: https://github.com/nabeelre/BTSbot
- HuggingFace: Available via `btsbot.load_HF_model()`
- **Citations: 40+**

---

## 10. RAPID

**Description**: RAPID (Real-time Automated Photometric IDentification) is a deep recurrent neural network for early classification of explosive transients. It was the first method specifically designed to provide classifications within a day of initial alert, making it ideal for broker deployment. [^802^]

### Key Features
- **Early classification**: Classifies 12 transient classes from day 1 of detection
- **GRU architecture**: Gated Recurrent Units for time-series processing
- **Time-varying predictions**: Classification probability evolves as more data arrives
- **No feature engineering**: End-to-end learning from raw photometry
- **Real-time deployment**: Classifies 5000+ extragalactic transients/night on ZTF
- **12 classes**: SNIa, SNIbc, SNII, SLSN-I, TDE, AGN, and more

### Installation
```bash
pip install astrorapid
```

### Architecture
- **Input**: Multi-band time-series photometry (MJD, flux, fluxerr, passband)
- **Encoder**: GRU layers process temporal sequence
- **Output**: 12-class probability vector at each time step
- **Context**: Optional host galaxy metadata

### Performance
- AUC = 0.95 at early epochs, 0.98 at late epochs
- Deployed on ZTF data stream
- Processes thousands of light curves in seconds

### Integration
- Deployed to ALeRCE and ANTARES brokers
- Compatible with LSST alert format
- Python API for batch or streaming classification

### Citation & Authority
- Paper: Muthukrishna et al. (2019), PASP, 131, 118 [^802^]
- GitHub: https://github.com/daniel-muthukrishna/astrorapid
- Documentation: https://astrorapid.readthedocs.io/
- **Citations: 100+**

---

## 11. Other Notable Frameworks

### 11.1 SCONE (Supernova Classification with CNN)

**Description**: SCONE uses 2D Gaussian process regression to create "flux heatmaps" that are processed by a convolutional neural network, achieving filter-independence. [^785^]

**Key Features**:
- 2D GP interpolation → CNN classification
- No redshift required: 99.7% Ia accuracy
- 6-way classification: 98.2% accuracy
- Filter-set independent (GP smoothing handles irregular sampling)

**GitHub**: https://github.com/helenqu/scone
**Paper**: Qu et al. (2021), arXiv:2106.04370

### 11.2 SuperRAENN

**Description**: Semi-supervised recurrent autoencoder neural network for SN photometric classification, trained on Pan-STARRS1 Medium Deep Survey data. [^830^]

**Key Features**:
- RAENN learns unsupervised latent representation
- Random Forest classifier on encoded features
- 87% accuracy across 5 SN classes
- Trained on 5243 PS1-MDS light curves

**Installation**: `pip install superraenn`
**GitHub**: https://github.com/villrv/SuperRAENN
**Paper**: Villar et al. (2020), ApJ, 905, 94

### 11.3 Superphot+

**Description**: Real-time fitting and classification pipeline that uses parametric model fitting + gradient-boosted machine classifier. [^528^]

**Key Features**:
- Parametric piecewise model (7 parameters per band)
- Nested sampling for fitting
- LightGBM for classification
- No redshift required
- Deployed on ANTARES broker for ZTF

**Installation**: `pip install superphot-plus`
**GitHub**: https://github.com/VTDA-Group/superphot-plus
**Paper**: de Soto et al. (2024), ApJ, 974, 95

### 11.4 DASH

**Description**: Deep Automated Supernova and Host classifier for spectral classification using deep CNNs. [^831^]

**Key Features**:
- CNN-based spectral classification
- Type + subtype + age determination
- 100x faster than Superfit
- 97.5% type accuracy on validation
- GUI + Python library interfaces

**Installation**: `pip install astrodash`
**GitHub**: https://github.com/daniel-muthukrishna/DASH
**Paper**: Muthukrishna et al. (2019), ApJ, 875, 140

### 11.5 SNGuess

**Description**: SNGuess is an early-time transient classifier designed for the AMPEL broker that identifies young transients for follow-up. [^741^]

**Key Features**:
- RiseDecline features for early classification
- Designed for Rubin/LSST ELAsTiCC
- High purity for young transient selection
- Integrated into AMPEL tier-2 workflows

**Integration**: AMPEL broker workflows
**Paper**: Miranda et al. (2022)

### 11.6 PELICAN

**Description**: Deep architecture for light curve analysis using CNNs, developed for LSST simulations. [^859^]

**Key Features**:
- CNN architecture for light curve "images"
- 96.5% accuracy on simulated LSST data
- Trained on small samples (2k DDF)
- Designed for SN Ia cosmology

**Paper**: Pasquet et al. (2019), A&A, 627, 60

---

## 12. Integration Patterns

### 12.1 End-to-End Pipeline Pattern

The standard supernova ML pipeline follows this pattern:

```
Survey (ZTF/LSST) → Alert Stream → Broker → Preprocessing → ML Classifier → Follow-up
```

### 12.2 Simulation → Training → Deployment Pattern

```
SNANA/sncosmo Simulation → Dataset Generation → ML Training → Validation → Broker Deploy
```

### 12.3 Key Integration Points

| Component | Input | Output | Connects To |
|-----------|-------|--------|-------------|
| SNANA | Survey config, SED models | Simulated FITS light curves | sncosmo, SuperNNova |
| sncosmo | Photometry, models | Fitted parameters, simulations | All Python ML tools |
| SuperNNova | Raw photometry (CSV/FITS) | Classification probabilities | PIPPIN, Fink, ALeRCE |
| ParSNIP | Light curves | Latent representation, classification | AMPEL, PIPPIN |
| SCONE | Raw photometry | Classification | Standalone |
| BTSbot | Image cutouts + features | Bright transient score | Fritz, Kowalski |

### 12.4 PIPPIN: The Orchestration Layer

PIPPIN is the standard pipeline for SN cosmology that integrates: [^552^]
- **Simulation**: SNANA for data generation
- **Classification**: SuperNNova, ParSNIP, or custom classifiers
- **Light curve fitting**: SNANA snlc_fit
- **Bias correction**: BBC framework
- **Cosmology fitting**: wfit/SALT2mu

```bash
# Run full cosmology pipeline
pippin.sh my-analysis.yml
```

**Paper**: Hinton & Brout (2020), JOSS, 5, 2122
**GitHub**: https://github.com/Samreay/Pippin

---

## 13. Broker Ecosystem

The broker infrastructure connects survey alert streams to ML classifiers and follow-up facilities:

### 13.1 Fink
- **Origin**: IJCLAB (France)
- **Features**: Active learning for SN Ia, anomaly detection, multi-messenger
- **ML**: SuperNNova-compatible, custom classifiers
- **Status**: Selected Rubin community broker, processing ZTF since 2020
- **API**: Python client `pip install alerce` [^701^]
- **Paper**: Möller et al. (2021), MNRAS, 501, 3272

### 13.2 ALeRCE
- **Origin**: Chile
- **Features**: Stamp classifier + light curve classifier
- **ML**: Random Forest, CNN, custom architectures
- **Status**: Processing ZTF alerts since 2019
- **Papers**: Förster et al. (2020), arXiv:2008.03303; Sánchez-Sáez et al. (2021), AJ, 161, 141 [^800^]

### 13.3 AMPEL
- **Origin**: DESY (Germany)
- **Features**: Modular 4-tier architecture, Python-based
- **ML**: ParSNIP, SNGuess, custom units
- **Status**: ELAsTiCC participant, Rubin community broker
- **Paper**: Nordin et al. (2019), A&A, 631, A147 [^210^]

### 13.4 ANTARES
- **Origin**: NOIRLab (USA)
- **Features**: Flexible filter system, Locus-based object model
- **ML**: RAPID integration, custom science filters
- **Status**: Longest-running broker (since 2014)
- **Paper**: Matheson et al. (2021), AJ, 161, 107

### 13.5 Lasair
- **Origin**: UK
- **Features**: Full avro redistribution, Sherlock cross-matching
- **ML**: Custom classifiers, external tool integration
- **Status**: Rubin community broker

---

## 14. Summary Comparison Table

| Framework | Type | Language | Primary Use | Classification | Real-time | Install |
|-----------|------|----------|-------------|---------------|-----------|---------|
| **sncosmo** | Library | Python | LC fitting/sim | No | No | `pip install sncosmo` |
| **SuperNNova** | ML Pipeline | Python | Photometric class | Yes (RNN) | Yes | `pip install supernnova` |
| **ParSNIP** | ML Pipeline | Python | Generative + class | Yes (VAE) | Yes | Source install |
| **snmachine** | ML Pipeline | Python | Feature-based class | Yes (GBDT) | No | `pip install snmachine` |
| **SNANA** | Analysis pkg | C++/Fortran | Simulation/fitting | Yes (PSNID) | No | Source compile |
| **LightCurveLynx** | Framework | Python | Forward modeling | No | No | `pip install lightcurvelynx` |
| **MOSFiT** | Fitter | Python | Physical modeling | No | No | `pip install mosfit` |
| **SNID-SAGE** | Tool | Python | Spectral class | Yes (xcorr) | Yes | `pip install snid-sage` |
| **BTSbot** | ML Pipeline | Python | Discovery + follow-up | Yes (CNN) | Yes | `pip install btsbot` |
| **RAPID** | ML Pipeline | Python | Early classification | Yes (GRU) | Yes | `pip install astrorapid` |
| **SCONE** | ML Pipeline | Python | CNN classification | Yes (CNN) | No | Source install |
| **SuperRAENN** | ML Pipeline | Python | Semi-supervised class | Yes (AE) | No | `pip install superraenn` |
| **Superphot+** | ML Pipeline | Python | Real-time fitting+class | Yes (GBM) | Yes | `pip install superphot-plus` |
| **DASH** | Tool | Python | Spectral class | Yes (CNN) | Batch | `pip install astrodash` |
| **PIPPIN** | Pipeline | Python | Orchestration | - | - | Source install |

---

## Areas Warranting Deeper Investigation

1. **ParSNIP PyPI packaging**: The package name conflict on PyPI needs resolution for easier installation
2. **LightCurveLynx/tdastro transition**: The repository move from lightcurvelynx to tdastro should be tracked
3. **SNID-SAGE template expansion**: Continued growth of the template library for rare transients
4. **BTSbot generalization**: Adaptation beyond ZTF to LSST-scale data
5. **AMPEL LSST workflows**: Full migration to Rubin-era alert processing
6. **Foundation models**: Integration of time-series foundation models (StarEmbed) into SN classification
7. **Uncertainty quantification**: Standardization of uncertainty estimation across frameworks (Bayesian RNNs vs. ensembles)
8. **Multi-messenger integration**: Framework support for GW/neutrino-triggered SN searches

---

## References

[^35^]: Barbary et al. (2016), "SNCosmo: Python library for supernova cosmology", ApJS, cited 118+
[^256^]: Möller & de Boissière (2020), "SuperNNova: an open-source framework for Bayesian, neural network-based supernova classification", MNRAS, 491, 4277
[^258^]: SuperNNova GitHub, https://github.com/supernnova/SuperNNova
[^79^]: Boone (2021), "ParSNIP: Generative Models of Transient Light Curves with Physics-Enabled Deep Learning", AJ, 162, 275
[^407^]: Lochner et al. (2016), "Photometric Supernova Classification with Machine Learning", ApJS, 225, 31
[^254^]: RickKessler/SNANA, https://github.com/RickKessler/SNANA
[^310^]: SNDATA_ROOT Zenodo, https://zenodo.org/records/12655677
[^377^]: Dai et al. (2026), "LightCurveLynx: Forward Modeling of Time-Domain Surveys", arXiv:2604.07134
[^763^]: Guillochon et al. (2018), "MOSFiT: Modular Open Source Fitter for Transients", ApJS, 236, 6
[^753^]: Strocchi et al. (2025), "SNID-SAGE: A Modern Framework for Interactive Supernova Classification", A&A
[^755^]: Blondin & Tonry (2007), "SNID: Supernova Identification", ApJ, 666, 1024
[^888^]: Rehemtulla et al. (2024), "BTSbot: Automated Identification and Follow-up of Bright Transients", ApJ, 972, 7
[^802^]: Muthukrishna et al. (2019), "RAPID: Early Classification of Explosive Transients using Deep Learning", PASP, 131, 118
[^785^]: Qu et al. (2021), "SCONE: Supernova Classification with a Convolutional Neural Network", arXiv:2106.04370
[^830^]: Villar et al. (2020), "SuperRAENN: A Semi-supervised Supernova Photometric Classification Pipeline", ApJ, 905, 94
[^528^]: de Soto et al. (2024), "Superphot+: Real-time Fitting and Classification of Supernova Light Curves", ApJ, 974, 95
[^831^]: Muthukrishna et al. (2019), "DASH: Deep Learning for the Automated Spectral Classification of Supernovae", ApJ, 875, 140
[^552^]: Hinton & Brout (2020), "Pippin: A pipeline for supernova cosmology", JOSS, 5, 2122
[^800^]: Förster et al. (2020), "The ALeRCE Alert Broker", arXiv:2008.03303
[^210^]: Nordin et al. (2019), "Transient processing and analysis using AMPEL", A&A, 631, A147
[^701^]: ALeRCE Client, https://alerce.readthedocs.io/
[^540^]: sncosmo Documentation, https://sncosmo.readthedocs.io/
[^542^]: sncosmo Documentation (PDF), v2.10.1
[^746^]: sncosmo Homepage, https://sncosmo.readthedocs.io/
[^900^]: LSSTDESC/snmachine, https://github.com/LSSTDESC/snmachine
[^377^]: LightCurveLynx Paper (PDF), arXiv:2604.07134v1
[^752^]: Dai et al. (2026), LightCurveLynx arXiv abstract
[^893^]: MOSFiT Documentation, https://mosfit.readthedocs.io/
[^901^]: Guillochon et al. (2018), MOSFiT Paper, ApJS, 236, 6
[^898^]: BTSbot GitHub, https://github.com/nabeelre/BTSbot
[^859^]: Pasquet et al. (2019), PELICAN, arXiv:1901.01298
[^741^]: AMPEL workflows for LSST, A&A, 2025

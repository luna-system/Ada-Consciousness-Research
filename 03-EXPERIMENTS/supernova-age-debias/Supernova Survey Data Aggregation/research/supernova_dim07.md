# Dimension 7: Simulated & ML Challenge Datasets

## Executive Summary

This document catalogs the major simulated supernova datasets and ML challenge datasets available for machine learning research in time-domain astronomy. These datasets span from early benchmarks (SNPCC, 2010) through contemporary large-scale simulations (OpenUniverse2024, 400TB) and include purpose-built ML challenge datasets (PLAsTiCC, ELAsTiCC) as well as multimodal foundation model training sets (Maven). Together they represent the primary infrastructure for training and evaluating supernova classification algorithms in the era of large-scale photometric surveys.

---

## 1. PLAsTiCC (Photometric LSST Astronomical Time-Series Classification Challenge)

### Overview
PLAsTiCC was a Kaggle-hosted classification challenge that ran from September 28 to December 17, 2018, designed to prepare the astronomy community for LSST/Rubin Observatory data volumes [^122^][^607^]. It remains the most widely used benchmark for supernova photometric classification.

**Scale**: ~3.5 million objects (test set), ~7,848 training objects, ~450+ million total photometric observations [^184^][^605^]

### Data Format
- **Primary format**: CSV (gzip-compressed)
- Training data: `plasticc_training_lightcurves.csv` + `plasticc_train_metadata.csv`
- Test data: `plasticc_test_lightcurves_01.csv.gz` through `plasticc_test_lightcurves_11.csv.gz` (11 files) + `plasticc_test_metadata.csv.gz` [^639^]
- Total data volume: ~18 GB compressed (test set), ~7.5 GB for unblinded release [^255^][^638^]
- **Light curve columns**: `object_id`, `mjd` (Modified Julian Date), `passband` (0-5 for ugrizy), `flux`, `flux_err`, `detected_bool` [^605^][^607^]
- **Metadata columns**: `object_id`, `ra`, `decl`, `gal_l`, `gal_b`, `ddf` (DDF flag), `hostgal_specz`, `hostgal_photoz`, `hostgal_photoz_err`, `distmod`, `mwebv`, `target` [^607^]

### 15 Classes (14 in training + 1 unknown)

| Class ID | Class Name | Description | Training Count |
|----------|-----------|-------------|----------------|
| 6 | Microlensing (uLens) | Gravitational microlensing event | ~151 |
| 15 | TDE | Tidal Disruption Event | ~495 |
| 16 | Eclipsing Binary | Periodic eclipsing binary | ~924 |
| 42 | SN II | Core-collapse Type II supernova | ~1,193 |
| 52 | SNIax | Peculiar Type Ia supernova | ~183 |
| 53 | Mira Variable | Long-period variable star | ~30 |
| 62 | SNIbc | Core-collapse Type Ibc supernova | ~484 |
| 64 | Kilonova (KN) | Neutron star merger | ~100 |
| 65 | M-dwarf flare | Stellar flare | ~981 |
| 67 | SNIa-91bg | Cool/subluminous Type Ia | ~208 |
| 88 | AGN | Active Galactic Nucleus | ~370 |
| 90 | SNIa | Normal Type Ia supernova | ~2,313 |
| 92 | RR Lyrae | Pulsating variable star | ~239 |
| 95 | SLSN-I | Superluminous supernova | ~175 |
| 99 | Unknown/Other | Not present in training set | N/A (test only) |

**Class distribution**: Highly imbalanced. Training set ranges from ~30 (Mira) to ~2,313 (SNIa). Test set has more uniform distribution [^605^][^697^].

### Access
- **Original Kaggle data**: https://www.kaggle.com/c/PLAsTiCC-2018/data [^607^]
- **Unblinded data (with true labels)**: Zenodo DOI 10.5281/zenodo.2539456 [^255^][^623^]
- **Model parameters**: `plasticc_modelpar.tar` with physical parameters per model [^639^]
- **Simulation source code**: http://snana.uchicago.edu [^625^]

### Key References
- Allam Jr. et al. 2018, arXiv:1810.00001 (data set paper) [^676^]
- Kessler et al. 2019 (simulation details)
- Hlozek et al. 2022 (challenge results)

### ML-Readiness
- **High**. CSV format is directly readable with pandas. Multiple example notebooks exist on Kaggle. The unblinded data allows full train/test evaluation. Imbalanced class distribution makes it realistic but challenging. Training set is non-representative of test set (simulating real survey conditions where training comes from brighter, nearby spectroscopic samples) [^605^][^184^].

---

## 2. ELAsTiCC (Extended LSST Astronomical Time-series Classification Challenge)

### Overview
ELAsTiCC is the successor to PLAsTiCC, designed to test broker systems and classification algorithms with a realistic LSST alert stream. Unlike PLAsTiCC, it was delivered as a real-time alert stream to participating Rubin Observatory community brokers [^334^][^641^].

**Scale**: ~4.3 million objects, ~50 million alerts, ~139 million observations [^641^][^642^]

### Data Format
- **Alert format**: Apache AVRO (matching LSST alert schema)
- **Simulation format**: SNANA FITS files (HEAD + PHOT tables)
- **Alternative formats**: Parquet files, CSV truth tables, tarballs of AVRO alerts [^334^][^674^]
- **Schema**: `elasticc.v0_9_1.alert.avsc` for alerts, `elasticc.v0_9_1.brokerClassification.avsc` for broker responses [^334^]
- Alert content includes: diaObject (object summary), diaSource (new detection), prv_diaSources (previous detections), forced photometry (going back 30 days from first detection) [^334^]

### Full Taxonomy (Tree-Structured)

ELAsTiCC uses a hierarchical taxonomy with 30+ leaf classes [^334^][^674^]:

**Extragalactic Transients**:
- **SN-like**: SNIa, SNIb/c, SNII, SNIax, SNIa-91bg
- **Fast**: Kilonova (KN), M-dwarf Flare, Dwarf Novae, Microlensing (uLens)
- **Long**: SLSN, TDE, ILOT (Intermediate Luminosity Optical Transient), CART (Calcium-Rich Transient), PISN (Pair-Instability SN)

**Galactic Variable**:
- **Periodic**: Cepheid, RR Lyrae, Delta Scuti, Eclipsing Binary (EB), LPV/Mira
- **Non-Periodic**: AGN

**Static/Other classes**: Meta/Other, Residual, NotClassified

### Access
- **Public web portal**: https://portal.nersc.gov/cfs/lsst/DESC_TD_PUBLIC/ELASTICC/ [^334^]
- **ELAsTiCC1 Training Samples**: https://portal.nersc.gov/cfs/lsst/DESC_TD_PUBLIC/ELASTICC/TRAINING_SAMPLES/
  - Full tar file: `FULL_ELASTICC_TRAIN.tar` (7.3 GiB)
- **ELAsTiCC2 Training Sample**: https://portal.nersc.gov/cfs/lsst/DESC_TD_PUBLIC/ELASTICC/ELASTICC2_TRAINING_SAMPLE_2
  - SNANA FITS format (per model)
  - `ELASTICC2_TRAIN_02.tar.bz2` (7.4 GiB)
  - AVRO subdirectory for alert-format training data [^334^]
- **NERSC direct access**: `/global/cfs/cdirs/lsst/www/DESC_TD_PUBLIC/ELASTICC/` [^334^]
- **ELAsTiCC2 data (NERSC)**: `/global/cfs/cdirs/desc-td/ELASTICC2` [^674^]
- **GitHub**: https://github.com/LSSTDESC/elasticc [^334^]

### Campaigns
- **ELAsTiCC1**: September 2022 - January 2023 [^334^]
- **ELAsTiCC2**: November - December 2023 (3x alert rate) [^334^]

### Key References
- ADS Abstract: 2023AAS...24111701N [^641^]
- Lokken, Gagliano et al. 2023 (simulation methodology) [^640^]

### ML-Readiness
- **Moderate to High**. FITS format requires SNANA or astropy knowledge. Parquet format is more accessible. The AVRO alert format is realistic but complex. Training data is divided by model, requiring user-side train/validation splitting. The hierarchical taxonomy enables multi-level classification problems.

---

## 3. Hourglass Simulation (Roman Space Telescope)

### Overview
The Hourglass simulation is a catalog-level simulation for the Nancy Grace Roman Space Telescope's High-Latitude Time-Domain Core Community Survey (HLTD CCS). It is the most comprehensive Roman time-domain simulation to date, including both photometry and spectroscopy (prism) [^622^][^269^].

**Scale**: 64,000+ transient objects, 11 million photometric observations, 500,000 spectra [^622^][^328^]

### 10 Transient Classes

| Class | Total Detected | Median S/N at Max | Median Redshift |
|-------|---------------|-------------------|-----------------|
| SN Ia | 21,700 | 13.5 | 1.32 |
| SN Ia-91bg | 1,300 | 10.6 | 0.84 |
| SN Iax | 1,300 | 8.5 | 0.95 |
| CCSNe | 39,000 | 8.8 | 0.90 |
| SLSN-I | 70 | 32.4 | 1.82 |
| TDE | 39 | 13.5 | 0.65 |
| ILOT | 35 | 6.7 | 0.49 |
| Kilonova | 14 | 7.9 | 0.35 |
| PISN | 15 | 8.2 | 2.23 |
| AGN | 139 | 13.6 | 1.78 |

### Data Format
- **Format**: Apache Parquet (three files)
  - `hourglass_objects.parquet` - one row per object (metadata)
  - `hourglass_photometry.parquet` - one row per flux measurement
  - `hourglass_spectra.parquet` - one row per object per epoch (spectral time series) [^328^][^269^]
- **Photometry columns**: `cid`, `mjd`, `band` (R/Z/Y/J/H/F), `fluxcal`, `fluxcal_err`, `psf_nea`, `sky_sig`, `zp`, `sim_mag_obs` [^269^]
- **Spectra columns**: `cid`, `mjd`, `t_expose`, `n_bin_lam`, `lam_min`, `lam_max`, `flam`, `flam_err`, `sim_flam` [^269^]
- **Survey parameters**: 4 filters per tier, 5-day cadence, 2 years, wide tier 19 deg2, deep tier 4.2 deg2, ~20% with prism coverage [^622^]

### Access
- **Zenodo**: DOI 10.5281/zenodo.14262943 [^328^][^269^]
- **Python reading**: `pandas.read_parquet()` or `pyarrow`
- Metadata inspection: `pq.ParquetFile('hourglass_objects.parquet').metadata.metadata` [^269^]

### Key References
- Rose et al. 2025, ApJ, arXiv:2506.05161 [^622^][^269^]

### ML-Readiness
- **Very High**. Parquet format is native to pandas/PyArrow. Three well-structured files with clear join keys (CID). Includes both photometry and spectroscopy, enabling multimodal models. Objects file has redshift and classification labels built-in. Much cleaner structure than PLAsTiCC/ELAsTiCC.

---

## 4. OpenUniverse2024

### Overview
OpenUniverse2024 is a massive cross-collaboration effort producing matched simulated imaging for multiple surveys (Rubin LSST and Roman) as they would observe a common simulated sky. It includes catalog-level simulations and pixel-level synthetic imaging [^301^][^302^].

**Scale**: ~400 TB total synthetic imaging, ~70 deg2 of overlapping LSST+Roman coverage, ~1.4 million transient objects, ~117 million galaxies [^301^]

### Data Products
- **Imaging**: Simulated FITS images for both Roman and Rubin LSST
- **Input catalogs**: Parquet files with truth information
  - `snana_<hpixid>.parquet` - transient properties table
  - `snana_<hpixid>.hdf5` - transient SEDs (time-resolved spectral energy distributions)
  - `pointsource_flux_<hpixid>.parquet` - Milky Way star fluxes
- **Processed products**: Object catalogs from LSST Science Pipelines, coadds, visit-level source catalogs [^301^]

### Transient Models (10 Classes)
SNe Type Ia, Ib, Ic, II, TDE, PISN, Kilonova, and others. Uses updated Diffsky extragalactic model and improved transient models extending through Roman+Rubin wavelength range [^301^].

### Access
- **IPAC/IRSA portal**: https://irsa.ipac.caltech.edu/data/theory/openuniverse2024/overview.html [^302^]
- **AWS cloud access**: Available via Amazon S3
- **Preview dataset**: DOI 10.26131/IRSA569 (browseable at IPAC + AWS)
- **Full release**: DOI 10.26131/IRSA596 (AWS cloud only) [^302^]
- **Documentation**: https://roman.ipac.caltech.edu/page/nasa-openuniverse-images-2024 [^303^]
- **Paper**: OpenUniverse et al. 2025, arXiv:2501.05632 [^301^]

### ML-Readiness
- **Moderate**. The imaging data requires significant processing to extract light curves. The catalog/Parquet data (truth tables) is directly usable. HDF5 SED files allow spectro-temporal modeling. The scale (400TB) requires cloud or institutional access. Best suited for end-to-end pipeline development rather than direct classification benchmarking.

---

## 5. SNPCC (Supernova Photometric Classification Challenge)

### Overview
SNPCC (also called SNPhotCC) was the first major public supernova photometric classification challenge, organized by Kessler et al. in 2010. It established the template for later challenges and remains a useful benchmark for Ia vs. non-Ia classification [^239^][^244^].

**Scale**: 21,319 total light curves (5,086 SNIa + 16,231 core-collapse SNe) over 5 simulated seasons [^362^][^244^]

### Data Format
- **Simulation software**: SNANA
- **Output formats**: SNANA native ASCII and FITS formats
- **Survey**: Simulated DES griz filters
- **Two challenges**: SNPhotCC+HOSTZ (with host galaxy photo-z) and SNPhotCC-noHOSTZ (no redshift) [^244^]
- **Training subset**: Spectroscopically confirmed subset provided for algorithm tuning
- **Selection criteria**: S/N>5 in 2+ passbands, minimum 5 observations after explosion [^244^]

### 7 Classes
SNIa (50%), SNII, SNIIn, SNIIL, SNIb, SNIb/c, SNIc [^362^]

### SN Ia Models
- Equal mix of MLCS2k2 and SALT2
- Additional random color variation
- MLCS-U2 extinction correction [^362^]

### Non-Ia Models
Based on spectroscopically confirmed light curves from CSP, SNLS, SDSS-II. 41 non-Ia SNe templates: 16 Ibc, 23 II-P, 2 IIn [^244^].

### Access
- **Original website**: http://www.hep.anl.gov/SNchallenge (historical) [^239^]
- **Current access**: Included in SNANA package distribution
- **SNANA download**: http://snana.uchicago.edu/ [^102^]
- **Updated simulations**: Post-challenge improved samples with bug fixes available via SNANA [^244^]

### Key References
- Kessler et al. 2010a, arXiv:1001.5210 (challenge announcement) [^239^]
- Kessler et al. 2010b, arXiv:1008.1024 (results paper) [^242^][^244^]

### ML-Readiness
- **Moderate**. Requires SNANA software to read native formats. Historical dataset with known bugs (documented in Kessler et al. 2010b). Smaller scale makes it less relevant for deep learning but useful for algorithm development and validation. Updated post-challenge simulations fix known issues [^244^].

---

## 6. SuperNNova Simulations

### Overview
SuperNNova is an open-source framework for Bayesian neural network-based supernova photometric classification, developed by Moller & de Boissiere (2020). The associated Zenodo release includes 2 million simulated light curves for training and testing [^654^][^256^].

**Scale**: ~2 million simulated light curves (~55-56 MB per file, 18 paired data+header files) [^100^]

### Data Format
- **Format**: SNANA native format (HDF5 and ASCII)
- **Content**: Simulated light curves for SNIa vs. non-Ia classification
- **Features**: 3D arrays (time x filter x features) preprocessed for RNN input
- **Files**: Paired photometry and header files, organized by simulation batch [^100^]

### Access
- **Zenodo**: https://zenodo.org/records/3265189 [^100^]
- **GitHub**: https://github.com/supernnova/SuperNNova [^655^][^656^]
- **Paper**: Moller & de Boissiere 2020, MNRAS, 491, 4277 [^654^][^256^]
- **arXiv**: arXiv:1901.06384 [^656^]

### Key Capabilities
- SNN achieves >96.92% accuracy without redshift, >99.55% with redshift [^654^]
- Early-time classification: >86.4% accuracy 2 days before maximum light (without redshift) [^654^]
- Bayesian RNN variants: MC Dropout and Bayes by Backprop for uncertainty quantification
- No feature engineering required - operates directly on light curve data [^654^]

### ML-Readiness
- **High**. Designed specifically for ML. Preprocessed 3D arrays ready for RNN training. Includes both full and SALT2-fitted datasets. Well-documented Python pipeline. Excellent for benchmarking classification methods.

---

## 7. Maven Multimodal Dataset

### Overview
Maven is the first multimodal foundation model for supernova science, trained via contrastive learning on paired light curves and spectra. The dataset includes both simulated pre-training data and real observational fine-tuning data [^667^][^663^].

**Scale**: 
- **Pre-training**: 500,000 simulated light curve-spectrum pairs (5 classes, evenly split) [^663^][^667^]
- **Fine-tuning/Evaluation**: 4,702 observed SNe from ZTF Bright Transient Survey [^663^][^280^]
- **HuggingFace dataset size**: 8.78 GB, 5,170 rows [^699^]

### 5 SN Classes
1. SNe Ia (thermonuclear)
2. SNe Ib/c (core-collapse)
3. SNe II (core-collapse, includes IIP/IIL)
4. SLSNe-I (superluminous)
5. SNe IIn [^663^]

### Data Format
- **Simulated pre-training**: HDF5 file (`ZTF_Pretrain_5Class.hdf5`) containing 500K events
- **Real observations**: ZTFBTS photometry + SEDM spectra from TNS/WISeREP
- **HuggingFace Hub**: `thelfer/multimodal_supernovae` [^699^][^665^]
- **Content per object**: Light curves (g, r, i filters), spectra (flux vs. wavelength), host galaxy images (60x60 pixel cutouts) [^699^]

### Access
- **HuggingFace Dataset**: https://huggingface.co/datasets/thelfer/multimodal_supernovae [^699^][^280^]
- **Clone**: `git clone https://huggingface.co/datasets/thelfer/multimodal_supernovae`
- **Pre-training sims**: `wget https://huggingface.co/datasets/thelfer/multimodal_supernovae/resolve/main/sim_data/ZTF_Pretrain_5Class.hdf5` [^665^]
- **GitHub code**: https://github.com/ThomasHelfer/multimodal-supernovae [^665^]
- **Paper**: Zhang et al. 2024, Machine Learning: Science and Technology, arXiv:2408.16829 [^280^][^668^]

### Key Results
- State-of-the-art on SN classification and photometric redshift estimation
- Synthetic pre-training significantly improves over real-data-only training (Maven vs. Maven-lite)
- Contrastive learning aligns photometric and spectroscopic representations in shared latent space [^667^][^663^]

### ML-Readiness
- **Very High**. HuggingFace integration enables one-line loading. HDF5 format is standard. Multimodal structure (light curves + spectra + host images) enables rich model architectures. Clear train/validation splits. Well-documented codebase with pre-training and fine-tuning scripts.

---

## 8. DES-SN5YR Mock Simulations

### Overview
The DES-SN5YR data release includes 25 DES mock simulations used for testing and validating the DES cosmological pipeline. These are professional-grade simulations used in the DES-Dovekie cosmology analysis [^344^][^485^].

**Scale**: 25 independent mock simulations [^344^]

### Data Format
- SNANA FITS format (HEAD + PHOT tables)
- Includes both simulated Ia and non-Ia DES light curves
- Truth tables with generated parameters for each event [^344^]

### Access
- **GitHub (data release)**: https://github.com/des-science/DES-SN5YR [^344^]
- **Zenodo**: DOI 10.5281/zenodo.12720778 (`DES-SN5YR-1.2.zip`) [^485^]
- **Utility package**: `pip install -e .` from `git clone https://github.com/BrunoSanchez/DES-SN-DR.git` [^485^][^413^]
- **Download command**: `downloaddessndr <dest_dir>` [^485^]

### Key References
- Vincenzi et al. 2024 (DES cosmology paper)
- Sanchez et al. 2024 (data release paper)
- Popovic et al. 2025 (DES-Dovekie cosmology) [^550^]

### ML-Readiness
- **Moderate**. Professional cosmology-grade simulations. SNANA format requires domain knowledge. Smaller scale than PLAsTiCC/ELAsTiCC. Best suited for SNIa cosmology studies rather than general classification benchmarking.

---

## 9. SNDATA_ROOT (SNANA Simulation Infrastructure)

### Overview
SNDATA_ROOT is the standard data environment for the SNANA supernova analysis package. It contains public light curve datasets, filter transmissions, SED models, simulation libraries, and calibration files [^310^][^102^].

**Scale**: ~1.7 GB compressed (2024-07-04 release) [^310^]

### Contents
- Public light curve data sets (DES, SDSS, PS1, LOWZ, FOUNDATION, etc.)
- Filter transmission functions for all major surveys
- Primary spectral energy distributions (SEDs)
- SNIa models (SALT2, MLCS2k2, SNooPy, etc.)
- Core-collapse SN spectral templates
- Milky Way extinction maps
- SIMLIB files (observing cadence libraries)
- HOSTLIB files (host galaxy properties)
- Efficiency maps for surveys [^102^][^310^]

### Access
- **Zenodo**: https://zenodo.org/records/12655677 (SNDATA_ROOT_2024-07-04) [^310^]
- **Direct download**: `wget http://snana.uchicago.edu/downloads/SNDATA_ROOT.tar.gz` [^657^][^671^]
- **SNANA GitHub**: https://github.com/RickKessler/SNANA [^643^]
- **Documentation**: http://snana.uchicago.edu/ [^257^]
- **Tutorial**: https://snana-starterkit.readthedocs.io/ [^657^]

### Key References
- Kessler et al. 2009, PASP, 121, 1028 (SNANA overview paper) [^643^]

### ML-Readiness
- **Infrastructure-level**. SNDATA_ROOT is not a dataset per se but the foundational infrastructure from which all SNANA simulations are built. Essential for anyone generating custom supernova simulations. Enables survey-specific simulation of DES, LSST, ZTF, Roman, and other facilities.

---

## 10. Simulation Fidelity and the Sim-to-Real Gap

### Key Challenges
A critical concern for all simulated datasets is the "sim-to-real gap" - the performance degradation when models trained on simulations are applied to real data [^705^][^706^]:

1. **Domain shift**: Simulations may not perfectly capture observational noise characteristics, selection effects, and instrumental artifacts [^705^]
2. **Redshift distribution mismatch**: Training sets (spectroscopically confirmed) are typically biased toward brighter, lower-redshift objects [^605^][^184^]
3. **Class imbalance**: Rare classes (kilonovae, PISNe) may have very few examples even in large simulations [^696^]
4. **Model limitations**: SED templates for non-Ia SNe are based on limited spectroscopic samples [^244^]

### Evidence of the Gap
- Gupta et al. (2025) found that for redshift estimation, models achieve R2=0.580 on simulations but only R2=0.431 on real ZTF data [^705^][^706^]
- Fine-tuned models consistently underperform on real data compared to simulations [^706^]
- "Models trained on simulations need to be fine-tuned on real data to work well" [^706^]

### Mitigation Strategies
1. **Domain adaptation**: Adversarial or contrastive training to align simulation and observation domains [^705^]
2. **Synthetic pre-training + real fine-tuning**: Maven approach - pre-train on 500K simulated pairs, fine-tune on 4.7K real objects [^667^][^663^]
3. **Bayesian methods**: Uncertainty quantification for out-of-distribution detection (SuperNNova) [^654^]
4. **Active learning**: Selective labeling of real data to bridge the gap efficiently [^707^]
5. **Survey-agnostic representations**: Training across multiple surveys (ZTF + LSST) improves cross-survey transfer [^705^]

### Assessment by Dataset
- **PLAsTiCC**: Good fidelity for LSST forecasts. Known issues with training/test distribution mismatch (intentional). Seasonal gaps and realistic cadence [^184^]
- **ELAsTiCC**: Improved host galaxy associations and photo-z realism over PLAsTiCC. Alert format matches LSST pipeline. Some training/test cadence differences (intentional) [^334^]
- **Hourglass**: State-of-the-art Roman simulation with updated SED models. First to include non-Ia spectral time series. Prism spectroscopy included [^622^]
- **SuperNNova**: SNANA simulations with realistic survey detection. Well-calibrated for Ia vs. non-Ia. Smaller scope but high fidelity for its use case [^654^]
- **OpenUniverse2024**: Most comprehensive imaging simulation. Diffsky model improves galaxy realism. Transient models span Roman+Rubin wavelength range [^301^]

---

## Dataset Comparison Summary

| Dataset | Events | Classes | Format | Size | Access | Primary Use |
|---------|--------|---------|--------|------|--------|-------------|
| PLAsTiCC | 3.5M | 15 | CSV | ~18GB | Kaggle/Zenodo | General classification benchmark |
| ELAsTiCC | 4.3M | 30+ | FITS/AVRO/Parquet | ~15GB | NERSC | Broker testing, alert processing |
| Hourglass | 64K | 10 | Parquet | ~GB | Zenodo | Roman preparation, multimodal |
| OpenUniverse2024 | 1.4M | 10+ | FITS/Parquet/HDF5 | ~400TB | IPAC/AWS | End-to-end pipeline testing |
| SNPCC | 21K | 7 | SNANA FITS/ASCII | ~MB-GB | SNANA | Historical benchmark |
| SuperNNova | 2M | 2 | HDF5/SNANA | ~500MB | Zenodo | RNN classification, Bayesian |
| Maven | 500K sim + 4.7K real | 5 | HDF5 | ~9GB | HuggingFace | Multimodal foundation models |
| DES-SN5YR mocks | 25 sims | 2 (Ia/CC) | SNANA FITS | ~GB | GitHub/Zenodo | Cosmology validation |

---

## Flagged Areas for Deeper Investigation

1. **Maven dataset expansion**: The HuggingFace dataset shows only 5,170 rows but claims 500K+500K+4.7K samples. Need to verify actual structure and splits [^699^].

2. **ELAsTiCC parquet format**: The ELAsTiCC2 parquet files at NERSC (`/global/cfs/cdirs/desc-td/ELASTICC2_parquet`) may be the most accessible entry point for ML use, but require documentation review [^674^].

3. **Hourglass v2**: The ROTAC-recommended survey strategy should increase transient counts by 25-30%. Updated simulations may be released [^269^].

4. **OpenUniverse2024 truth tables**: The `snana_<hpixid>.parquet` files contain transient properties that may serve as an alternative to processing raw imaging. Need to verify if light curves can be directly extracted [^301^].

5. **Cross-dataset transfer**: Combining PLAsTiCC (large, multi-class) with Maven (multimodal) for richer representations remains unexplored.

6. **Sim-to-real domain adaptation**: The gap between simulation and real data remains the primary barrier. Systematic study of which simulation parameters most affect classification performance would be valuable [^705^].

---

## References

[^100^]: Zenodo SuperNNova light-curve simulations, https://zenodo.org/records/3265189
[^102^]: KICP Chicago SNANA Tutorial, https://kicp.uchicago.edu/~kessler/SNANA_Tutorial/
[^122^]: PLAsTiCC official website, https://plasticc.org/
[^184^]: Burhanudin & Maund 2022, "Pan-chromatic photometric classification of supernovae", MNRAS
[^239^]: Kessler et al. 2010, arXiv:1001.5210 (SNPCC announcement)
[^242^]: Kessler et al. 2010, arXiv:1008.1024 (SNPCC results)
[^244^]: Kessler et al. 2010, "Results from the Supernova Photometric Classification Challenge", ApJS
[^255^]: Zenodo PLAsTiCC unblinded data, https://zenodo.org/records/2539456
[^256^]: Moller & de Boissiere 2020, "SuperNNova", MNRAS, 491, 4277
[^257^]: SNANA Homepage, http://snana.uchicago.edu/
[^269^]: Rose et al. 2025, "The Hourglass Simulation", ApJ, arXiv:2506.05161
[^280^]: Zhang et al. 2024, "Maven: a multimodal foundation model for supernova science", arXiv:2408.16829
[^301^]: OpenUniverse et al. 2025, "OpenUniverse2024", arXiv:2501.05632
[^302^]: IRSA OpenUniverse2024 portal, https://irsa.ipac.caltech.edu/data/theory/openuniverse2024/
[^303^]: NASA OpenUniverse2024, https://roman.ipac.caltech.edu/page/nasa-openuniverse-images-2024
[^310^]: Zenodo SNDATA_ROOT, https://zenodo.org/records/12655677
[^328^]: Rose et al. 2025, arXiv:2506.05161 (Hourglass paper)
[^334^]: ELAsTiCC NERSC portal, https://portal.nersc.gov/cfs/lsst/DESC_TD_PUBLIC/ELASTICC/
[^344^]: DES-SN5YR GitHub, https://github.com/des-science/DES-SN5YR
[^362^]: Carreira et al. data-driven photometric redshift paper
[^605^]: Prapas 2018, Kaggle PLAsTiCC report
[^607^]: Kaggle PLAsTiCC data page, https://www.kaggle.com/c/PLAsTiCC-2018/data
[^622^]: Rose et al. 2025, arXiv:2506.05161 (Hourglass abstract)
[^623^]: Chaini et al. 2020, "Astronomical Classification of Light Curves"
[^625^]: PLAsTiCC model summary, https://plasticc.org/wp-content/uploads/2019/01/plasticc_modelreveal_2versions.pdf
[^638^]: Chaini et al. 2020, arXiv:2006.12333
[^639^]: PLAsTiCC unblinded data release note
[^640^]: ELAsTiCC AAS poster, https://portal.nersc.gov/cfs/lsst/DESC_TD_PUBLIC/ELASTICC/Elasticc_poster_AAS_Jan2023.pdf
[^641^]: ADS: 2023AAS...24111701N
[^642^]: Nordin et al. 2024, "AMPEL workflows for LSST", arXiv:2501.16511
[^643^]: Kessler et al. 2009, "SNANA: A Public Software Package for Supernova Analysis", PASP, 121, 1028
[^654^]: Moller & de Boissiere 2020, "SuperNNova", MNRAS, 491, 4277
[^655^]: Moller 2025 presentation on BNNs for SN classification
[^656^]: Moller & de Boissiere 2019, arXiv:1901.06384
[^657^]: SNANA Starter Kit, https://snana-starterkit.readthedocs.io/
[^663^]: OpenReview Maven paper, https://openreview.net/pdf?id=VltwtJEJWD
[^665^]: Maven GitHub, https://github.com/ThomasHelfer/multimodal-supernovae
[^667^]: IAIFI Research: Maven foundation model, https://research.iaifi.org/posts/maven-a-multimodal-foundation-model-for-supernova-science
[^671^]: SNANA Starter Kit documentation
[^674^]: ELAsTiCC Tutorial slides, https://lsstdesc.org/assets/pdf/docs/sprint_school_slides/elasticc.pdf
[^676^]: Allam Jr. et al. 2018, "The PLAsTiCC Data Set", arXiv:1810.00001
[^697^]: Vicedomini et al., "Statistical Characterization and Classification of Astronomical Time Series"
[^699^]: HuggingFace multimodal_supernovae dataset, https://huggingface.co/datasets/thelfer/multimodal_supernovae
[^705^]: Gupta et al. 2025, "Simulation-Based Pretraining and Domain Adaptation for Astronomical Time Series", arXiv:2510.12958
[^706^]: Gupta et al. 2025, ML4Astro ICML 2025 proceedings
[^707^]: Active Learning for Sim-to-Real transfer, DLR 2024

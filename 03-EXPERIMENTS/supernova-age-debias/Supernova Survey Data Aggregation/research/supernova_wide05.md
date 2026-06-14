# Facet: Simulated & ML Challenge Datasets for Supernova Classification

**Research Date**: 2025-07-23
**Researcher**: AI Agent
**Searches Conducted**: 14 independent search queries across arXiv, Zenodo, GitHub, ADS, survey official sites
**Sources**: Peer-reviewed papers, official challenge websites, GitHub repositories, data archives, conference proceedings

---

## Key Findings

1. **The simulated supernova dataset landscape is anchored by three major community challenges**: SNPCC (2010, ~18-21K events) [^1^], PLAsTiCC (2018, ~1.98M events) [^2^], and ELAsTiCC/ELAsTiCC2 (2022-2023, ~4M events each) [^3^]. These form the backbone of ML supernova classification research.

2. **SNANA is the dominant simulation engine** [^4^] -- nearly all major simulated datasets are produced with SNANA, which provides a unified framework for simulation, light-curve fitting, and cosmology analysis. SNDATA_ROOT provides public access to models, filters, and calibration data (~2 GB) [^5^].

3. **New-generation simulations for upcoming facilities** include the Roman Space Telescope Hourglass simulation (~64,000 transients, 11M photometric observations) [^6^] and OpenUniverse2024 (~400 TB of overlapping Roman+Rubin simulated imaging) [^7^], providing unprecedented realism for future survey preparation.

4. **Pre-trained model ecosystems** have emerged around these datasets: ParSNIP [^8^], Avocado [^9^], SuperNNova [^10^], and SCONE [^11^] all provide trained models and associated simulation data, lowering the barrier to entry for new researchers.

5. **Critical ML caveat**: Simulated datasets systematically overestimate classification performance compared to real data due to limited template diversity (especially for core-collapse SNe), idealized noise models, and incomplete representation of rare subclasses [^12^]. The PLAsTiCC training set was intentionally non-representative to simulate realistic spectroscopic follow-up biases.

---

## Dataset Catalog (Detailed Per Dataset)

### Dataset 1: SNPCC -- Supernova Photometric Classification Challenge

| Attribute | Details |
|-----------|---------|
| **Full Name** | Supernova Photometric Classification Challenge |
| **Also Known As** | SNPhotCC, SPCC |
| **URL/Download** | Original: `www.hep.anl.gov/SNchallenge` (now defunct); data distributed via SNANA software package. Updated simulations with answer keys released post-challenge. |
| **Primary References** | Kessler et al. 2010a (arXiv:1001.5210) [^1^]; Kessler et al. 2010b (arXiv:1008.1024) [^13^] |
| **Creator** | Dark Energy Survey (DES) Supernova Working Group |
| **Challenge Dates** | January 29 -- June 1, 2010 |
| **Number of Objects** | ~18,000-21,319 light curves (original challenge: ~18,321; later references cite 21,318-21,319 including all variants) |
| **Object Types** | SNe Ia (5,086), core-collapse SNe (16,231) distributed among: II, IIn, II-P, II-L, Ib, Ib/c, Ic |
| **Simulation Method** | SNANA software; SNe Ia simulated with equal mix of MLCS2k2 and SALT2 models plus random color variation; non-Ia SNe based on spectroscopically confirmed light curves donated from CSP, SNLS, SDSS-II with Nugent SED templates |
| **Survey Configuration** | DES griz filters; realistic sky noise, PSF, atmospheric transparency based on ESSENCE project CTIO data; 5 survey fields (3 deg2 each); 5 seasons |
| **Redshift Range** | 0 -- 1.1 |
| **Data Format** | SNANA FITS format (HEAD+PHOT files); ASCII light curves |
| **Training Set** | 1,256 spectroscopically confirmed SNe provided for training |
| **Includes Classifications** | Yes -- answer keys released post-challenge |
| **Includes Redshifts** | Yes -- host-galaxy photo-z (avg resolution 0.03) and true redshifts in answer keys |
| **Includes Host Properties** | Photo-z for host galaxies; no detailed host properties |
| **Noise Model** | Realistic: CCD gain, sky noise, PSF variations, atmospheric transparency from real CTIO weather histories |
| **Known Limitations** | (1) Only 2 Type IIn templates used to generate 800 LCs; only 16 Type Ibc templates for 3,200 LCs -- severe diversity underrepresentation for CCSN [^12^]; (2) Missing SLSNe entirely; (3) Several simulation bugs documented post-challenge (bright tail issues, SED normalization errors); (4) Template-fitting methods have inherent advantage due to SALT2/MLCS2 being used for simulation |
| **ML Readiness** | **High** -- widely used, well-documented, answer keys available. However, CCSN classifiers trained on this data may overestimate accuracy. Best suited for: algorithm comparison, feature engineering development, baseline classification testing. |

---

### Dataset 2: PLAsTiCC -- Photometric LSST Astronomical Time-Series Classification Challenge

| Attribute | Details |
|-----------|---------|
| **Full Name** | Photometric LSST Astronomical Time-Series Classification Challenge |
| **URL/Download** | Unblinded data on Zenodo: https://zenodo.org/records/2539456 (7.5 GB) [^14^]; Model libraries: https://doi.org/10.5281/zenodo.6672739 [^15^]; Original Kaggle: https://www.kaggle.com/c/PLAsTiCC-2018 |
| **Primary References** | Kessler et al. 2019 (PASP 131, 094501) [^2^]; Hlozek et al. 2020; Boone 2019 (Avocado) [^9^]; Boone 2021 (ParSNIP) [^8^] |
| **Creator** | LSST-DESC & LSST-TVS collaboration |
| **Challenge Dates** | September 28 -- December 17, 2018 (Kaggle) |
| **Number of Objects** | ~3.5 million total (training: ~7,000-8,000 labeled; test set: ~3.49M). After unblinding: all ~3.5M have labels. Note: 1.98M are simulated supernovae specifically. |
| **Object Types** | 18 transient and variable classes: SNe Ia, SNe Iax, SNe Ia-91bg, SNe Ibc, SNe II, SLSNe-I, TDE, AGN, RRLyr, Eclipsing Binaries, Cepheids, Microlensing (several types), Kilonova, plus variable stars |
| **Simulation Method** | SNANA; SED models from PLAsTiCC model library; LSST Operations Simulator for cadence; ugrizy filters |
| **Data Format** | CSV (time, flux, flux_err, detected_bool, MJD, passband); FITS; metadata includes RA, Dec, Galactic coordinates, host galaxy spec-z and photo-z |
| **Includes Classifications** | Yes -- full truth table released after unblinding (Jan 2019) |
| **Includes Redshifts** | Yes -- host spectroscopic and photometric redshifts |
| **Includes Host Properties** | Host galaxy photo-z, spec-z, coordinates; Milky Way extinction |
| **Noise Model** | Realistic LSST noise model: sky noise, read noise, PSF; seasonal gaps; cadence from OpSim |
| **Key ML Papers Using It** | Boone 2019 (Avocado, winning entry) [^9^]; Boone 2021 (ParSNIP) [^8^]; Möller & de Boissière 2020 (SuperNNova) [^10^]; Qu et al. 2021 (SCONE) [^11^]; Allam & McEwen 2021; Alves et al. 2022 |
| **Known Limitations** | (1) Training set intentionally non-representative (bright, low-z bias to simulate spectroscopic follow-up limitations); (2) Class imbalance (some classes have millions of objects, others hundreds); (3) Seasonal gaps in light curves; (4) Model SEDs extend only to 11,000A rest-frame; (5) Simulated photo-z may differ from real LSST photo-z performance; (6) Some rare classes (kilonovae) had rates artificially boosted for statistics |
| **ML Readiness** | **Excellent** -- largest public simulated transient dataset. Kaggle format makes it accessible. Multiple Python packages ( ParSNIP, SuperNNova) provide loaders. Ideal for: deep learning training, class imbalance studies, transfer learning experiments. |

---

### Dataset 3: ELAsTiCC -- Extended LSST Astronomical Time-series Classification Challenge

| Attribute | Details |
|-----------|---------|
| **Full Name** | Extended LSST Astronomical Time-series Classification Challenge |
| **URL/Download** | Training data: https://portal.nersc.gov/cfs/lsst/DESC_TD_PUBLIC/ELASTICC/ELASTICC2_TRAINING_SAMPLE_2 [^3^]; GitHub: https://github.com/LSSTDESC/elasticc; Data at NERSC: `/global/cfs/cdirs/desc-td/ELASTICC2` |
| **Primary References** | DESC collaboration; related to Kessler et al. 2019 PLAsTiCC framework |
| **Creator** | LSST Dark Energy Science Collaboration (DESC) |
| **Challenge Dates** | ELAsTiCC: September 2022 -- January 2023; ELAsTiCC2: November -- December 2023 |
| **Number of Objects** | ~4-5 million detected events per dataset; ~50 million alerts (ELAsTiCC2); ~400 million photometry points |
| **Object Types** | 32-model taxonomy: Milky Way variables, microlensing, AGN, multiple supernova types (Ia, Iax, 91bg, Ibc, II, SLSN-I, TDE, KN, PISN), plus Random Magnitude test sources |
| **Simulation Method** | SNANA; photometry-level simulation (not pixel-level); SNANA FITS format (HEAD+PHOT); includes forced photometry; host galaxies simulated with 0-2 possible hosts per object |
| **Survey Configuration** | LSST baseline 3.2 cadence including rolling cadence years 2-3; DDF fields included (ELAsTiCC2) |
| **Data Format** | SNANA FITS files; also AVRO alert format for broker testing |
| **Training Set** | Divided by model in subdirectories; truth tables in *.DUMP files; taxonomy mapping files provided |
| **Includes Classifications** | Yes -- full truth tables available |
| **Includes Redshifts** | Yes -- simulated photo-z quantiles available |
| **Includes Host Properties** | Yes -- mock galaxy catalog matches; Milky Way extinction; host galaxy color, stellar mass |
| **Alert Format** | Simulated LSST alert format (elasticc.v0_9_1.alert.avsc); forced photometry included from second detection onward (30 days of history) |
| **Known Limitations** | (1) Not pixel-level simulation (no image data); (2) No RA/Dec uncertainty simulation; (3) AGN and variable stars underrepresented (focus on transients); (4) Requires NERSC access or large downloads for full dataset |
| **ML Readiness** | **Excellent** -- most current LSST simulation. Designed specifically for broker development and real-time classification testing. Multi-format output (FITS + AVRO) supports end-to-end pipeline testing. |

---

### Dataset 4: Roman Hourglass Simulation

| Attribute | Details |
|-----------|---------|
| **Full Name** | Hourglass Simulation for Roman High-Latitude Time-Domain Core Community Survey |
| **URL/Download** | Zenodo: https://doi.org/10.5281/zenodo.14262943 [^6^]; GitHub input files: https://github.com/Roman-Supernova-PIT/hourglass_snana_sims |
| **Primary References** | Rose et al. 2025 (ApJ, accepted; arXiv:2506.05161) [^6^]; Kessler et al. 2025 (arXiv:2506.04402) |
| **Creator** | Roman Supernova Project Infrastructure Team (SN PIT) |
| **Release Date** | 2025 |
| **Number of Objects** | 64,000+ transient objects; 11 million photometric observations; 500,000 spectra |
| **Object Types** | 10 extragalactic classes: SNe Ia (21,700), SNIa-91bg (~1,300), SN Iax (~1,300), CCSNe (~39,000), SLSN-I (70), TDE (39), ILOT (35), Kilonova (14), PISN (15), AGN (139) |
| **Simulation Method** | SNANA + PIPPIN pipeline; SALT3-NIR for SNe Ia; PLAsTiCC-based models for most other classes; updated volumetric rates from Strolger et al. 2020 |
| **Survey Configuration** | Roman WFI; 4 filters per tier; 5-day cadence; 2 years; wide tier (19 deg2) + deep tier (4.2 deg2); ~20% prism coverage |
| **Redshift Range** | 0 -- 3 (artificially cut); median z for SNe Ia = 1.32 |
| **Data Format** | 3 Parquet files: hourglass_objects.parquet, hourglass_photometry.parquet, hourglass_spectra.parquet |
| **Includes Classifications** | Yes -- perfect truth labels |
| **Includes Redshifts** | Yes -- true redshifts for all objects |
| **Includes Host Properties** | Yes -- RA, Decl, S/N at maximum, host galaxy association; spectroscopic time series from Roman prism |
| **Noise Model** | Roman WFI realistic: zodiacal + thermal sky noise, read noise, dark current; PSF NEA per filter; detailed exposure time modeling |
| **Spectra** | **Yes** -- first public simulation of non-Ia SN spectral time series from Roman prism; 500,000 spectra included |
| **Known Limitations** | (1) Artificial rate boosts for rare events (KN x5, PISN x4, TDE x10); (2) Cutoff at z=3; (3) No variable stars; (4) Does not include latest Roman hardware knowledge from thermal-vacuum testing |
| **ML Readiness** | **Excellent** -- specifically designed for ML training. Parquet format is pandas-friendly. Includes both photometry and spectroscopy. SCONE classifier validated at ~95% Ia purity to z>2 [^11^]. |

---

### Dataset 5: OpenUniverse2024

| Attribute | Details |
|-----------|---------|
| **Full Name** | OpenUniverse2024: A shared, simulated view of the sky for next-generation cosmological surveys |
| **URL/Download** | IPAC landing page: https://irsa.ipac.caltech.edu/data/theory/openuniverse2024/overview.html [^7^]; AWS Open Data Registry: https://registry.opendata.aws/openuniverse2024/; 10TB preview: DOI 10.26131/IRSA569; Full: DOI 10.26131/IRSA596 |
| **Primary References** | OpenUniverse collaboration 2025 (arXiv:2501.05632) [^7^] |
| **Creator** | LSST DESC + Roman HLIS PIT + Roman RAPID PIT (Michael Troxel, lead) |
| **Data Volume** | ~400 TB total; 10 TB preview available |
| **Coverage** | ~70 deg2 of overlapping LSST WFD + Roman HLWAS; ELAIS-S1 DDF for both; Roman TDS overlap |
| **Transient Objects** | 1.39 million generated transient events; 312 million SEDs on MJD grid |
| **Transient Types** | 10 extragalactic classes: SLSN-I (1,128), TDE (3,784), PISN-H (113), PISN-He (112), KN (53), RanMag (27,884), plus SNe Ia, CCSNe, etc. |
| **Simulation Method** | SNANA for transients; Diffsky model for galaxies; updated SED models extending to Roman K-band (25,000A); pixel-level image simulation for Roman |
| **Data Products** | Simulated images (FITS), truth catalogs (Parquet), per-SCA truth files, coadds, observation sequence tables |
| **Includes Classifications** | Yes -- full truth catalogs |
| **Includes Redshifts** | Yes -- all cosmological effects modeled |
| **Image Format** | Roman: FITS (truth + calibrated images); LSST: matched simulated imaging |
| **Known Limitations** | (1) Diffsky galaxy model is prototype calibration (NIR colors narrower than real data); (2) Transient template library has reduced diversity compared to PLAsTiCC; (3) 400TB requires cloud or NERSC access |
| **ML Readiness** | **Good for advanced users** -- unprecedented realism with pixel-level data. Best for: image-based classification, difference-imaging pipeline testing, joint Roman+Rubin studies. Not suitable for quick table-based ML experiments. |

---

### Dataset 6: SuperNNova Light-Curve Simulations

| Attribute | Details |
|-----------|---------|
| **URL/Download** | Zenodo: https://zenodo.org/records/3265189 [^16^]; GitHub: https://github.com/supernnova/SuperNNova |
| **Primary References** | Möller & de Boissière 2020 (MNRAS 491, 4277) [^10^]; Möller et al. 2022, 2024 |
| **Creator** | Anais Möller, T. de Boissière |
| **Number of Objects** | 1,983,213 simulated light curves |
| **Object Types** | 7 SN templates: Ia, Ib, Ic, II-n, IIL1, IIL2, IIP |
| **Simulation Method** | SNANA with SALT2 fits; 7 supernova templates |
| **Data Format** | FITS (SNANA format); also CSV conversion available |
| **Data Volume** | ~1 GB total (multiple files ~48 MB each + SALT2 fit files ~4.5 MB each) |
| **Includes Classifications** | Yes -- binary (Ia vs non-Ia) and multi-class labels |
| **Includes Redshifts** | Yes -- available in SNANA format |
| **ML Readiness** | **Excellent** -- specifically created for SuperNNova RNN training. Format compatible with SuperNNova pipeline. Good for: RNN/LSTM/GRU training, Bayesian deep learning experiments, large-scale classification. |

---

### Dataset 7: SNDATA_ROOT (SNANA Public Data Release)

| Attribute | Details |
|-----------|---------|
| **URL/Download** | Zenodo: https://zenodo.org/records/12655677 (latest v13, April 2026, 2.0 GB) [^5^]; GitHub: https://github.com/rickkessler/SNANA |
| **Primary References** | Kessler et al. 2009 (ApJS 185, 32) [^4^] |
| **Creator** | Richard Kessler, University of Chicago |
| **Contents** | Public light curve datasets, filter transmissions, primary SEDs, calibration files, SNIa & CC models, cadence libraries, host-galaxy libraries for simulations |
| **Included Survey Data** | DES-SN5YR (DES + LOWZ + FOUNDATION), SDSS, SNLS, CSP, PS1, and many others |
| **Included Models** | SALT2, SALT3, MLCS2k2, SNooPy, Nugent templates, SNIbc templates, SLSN models, TDE models, KN models, many more |
| **Included Simlibs** | Cadence and observing condition libraries for major surveys (DES, LSST, ZTF, Roman) |
| **Format** | SNANA FITS; ASCII; standard calibration files |
| **ML Readiness** | **Essential infrastructure** -- required to run SNANA simulations. Includes everything needed to generate custom simulated datasets for any supported survey. Critical for researchers who need to create tailored training data. |

---

### Dataset 8: Maven Multimodal Supernova Simulation Dataset

| Attribute | Details |
|-----------|---------|
| **URL/Download** | HuggingFace: https://huggingface.co/datasets/thelfer/multimodal_supernovae [^17^]; GitHub: https://github.com/ThomasHelfer/multimodal-supernovae |
| **Primary References** | Zhang et al. 2024 (NeurIPS 2024 Workshop) [^17^] |
| **Creator** | Geirui Zhang et al., MIT/IAIFI |
| **Number of Objects** | 500,000 simulated events (evenly split: 100,000 per class x 5 classes) |
| **Object Types** | 5 classes: SNe Ia, SNe Ib/c, SLSNe-I, SNe II (IIP/IIL), SNe IIn |
| **Simulation Method** | SNANA; ZTF survey strategy; SED models from PLAsTiCC: SALT2 (Ia), SNIbc-Templates, SLSNI-MOSFIT, SNII-Templates, SNIIn-MOSFIT |
| **Redshift Distribution** | Low-z (z<0.1) favored, matching ZTF BTS selection |
| **Data Format** | Photometry (light curves) + synthetic spectra; HDF5/parquet via HuggingFace |
| **Spectra** | Synthetic spectra generated in SNANA matching ZTF SEDM spectrograph wavelength coverage; random S/N=5 |
| **Includes Classifications** | Yes -- 5-class labels |
| **Includes Redshifts** | Yes |
| **ML Readiness** | **Excellent** -- designed for multimodal (photometry+spectra+metadata) ML. HuggingFace format makes it extremely accessible. Ideal for: contrastive learning, multimodal foundation models, transfer learning to real ZTF data. |

---

### Dataset 9: DES-SN 5YR Simulated Data Products

| Attribute | Details |
|-----------|---------|
| **URL/Download** | GitHub: https://github.com/des-science/DES-SN5YR (folder 1_SIMULATIONS) [^18^]; Zenodo: doi:10.5281/zenodo.12720777 |
| **Primary References** | Vincenzi et al. 2024 (ApJ 975, 86); Sánchez et al. 2024 (ApJ 975, 5) [^18^] |
| **Creator** | Dark Energy Survey collaboration |
| **Number of Objects** | 25 DES mock simulations; includes both simulated Ia and non-Ia light curves |
| **Survey Configuration** | DES 5-year griz survey |
| **Redshift Range** | 0.1 < z < 1.13 |
| **Simulation Method** | SNANA; matched to DES observing conditions |
| **Data Format** | SNANA FITS; classification probabilities provided (folder 3_CLASSIFICATION) |
| **Classification Data** | 1,635 photometrically classified SNe with cosmology quality cuts; classification probabilities from multiple algorithms |
| **ML Readiness** | **Good** -- provides both simulations and real DES light curves with classifications. Useful for: training classifiers for DECam-like surveys, cosmology pipeline validation, testing classification+distances joint analysis. |

---

### Dataset 10: BTSbot Training Dataset

| Attribute | Details |
|-----------|---------|
| **URL/Download** | Zenodo training set: Available via GitHub https://github.com/nabeelre/BTSbot [^19^]; Models on HuggingFace Hub |
| **Primary References** | Nabeel Rehemtulla et al. (ML4Astro ICML 2023) [^19^] |
| **Creator** | Nabeel Rehemtulla, Northwestern |
| **Number of Objects** | Training set for production model available on Zenodo |
| **Object Types** | Real + simulated supernova detection triplets (science, reference, difference images) |
| **Data Format** | Image triplets (fits/png); metadata |
| **ML Model** | Multi-modal deep vision model (ConvNeXt / MaxViT); automates discovery-to-classification pipeline |
| **ML Readiness** | **Good for image-based SN detection** -- focused on real-time discovery rather than light-curve classification. Complements photometric classification datasets. |

---

### Dataset 11: RAPIDS Classifier Simulated Dataset

| Attribute | Details |
|-----------|---------|
| **Primary References** | Muthukrishna et al. 2019 (ApJS 245, 27) [^20^] |
| **Creator** | D. Muthukrishna et al. |
| **Number of Objects** | ~48,000 simulated light curves across 12 transient classes |
| **Object Types** | 8 SN types + 4 exotic transients (kilonova, TDE, etc.) |
| **Simulation Method** | PLAsTiCC simulation software repurposed for ZTF; real-time classification oriented |
| **Survey Configuration** | ZTF (g, r, i filters) |
| **ML Readiness** | **Good** -- designed for early-time classification (RAPIDS). Training/test splits available. Useful for: early alert classification, real-time broker applications. |

---

### Dataset 12: Roman-SNANA Simulations (Hourglass+Cosmology)

| Attribute | Details |
|-----------|---------|
| **URL/Download** | Zenodo: https://doi.org/10.5281/zenodo.14262943 [^6^]; GitHub: https://github.com/Roman-Supernova-PIT/hourglass_snana_sims |
| **Primary References** | Kessler et al. 2025 (arXiv:2506.04402); Rose et al. 2025 (arXiv:2506.05161) |
| **Creator** | Roman SN PIT team |
| **Number of Objects** | ~11,000 Roman SNe Ia + ~4,500 LSST SNe Ia after cosmology cuts |
| **Simulation Method** | SNANA + PIPPIN; SALT3-NIR; realistic Roman WFI characteristics |
| **Survey Configuration** | Roman HLTDS reference survey: 4 filters, 5-day cadence, wide+deep tiers |
| **Redshift Range** | 0.3 < z < 3.0 (Roman); unique large redshift range |
| **Cosmology Analysis** | Full pipeline: light curve fitting, photometric redshifts, BEAMS classification, systematic uncertainties, cosmology fitting |
| **Classification** | SCONE classifier trained on 30,000 SNIa + 15,000 non-Ia; achieves ~95% Ia purity to z>2 |
| **ML Readiness** | **Excellent for cosmology+classification joint studies** -- provides both the raw simulation and full analysis pipeline. SCONE classifier weights available. |

---

## Comparison of Simulation Methods

| Method/Package | Type | SN Models | Survey Support | ML Output Format | Key Strengths | Limitations |
|---------------|------|-----------|---------------|------------------|---------------|-------------|
| **SNANA** [^4^] | End-to-end simulation+analysis | SALT2/3, MLCS2k2, Nugent, custom SIMSED | DES, LSST, ZTF, Roman, SDSS, PS1, many others | FITS (HEAD+PHOT), ASCII | Industry standard; massive model library; validated against many surveys | C++ core; steep learning curve; catalog-level only (no images) |
| **SNCosmo** [^21^] | Python library | SALT2, SALT3, Hsiao, Nugent, MLCS2k2, BayeSN | Any (user-defined filters) | Python objects; astropy tables | Easy Python API; extensible; great for quick experiments | Less optimized than SNANA for large surveys; fewer built-in surveys |
| **ParSNIP** [^8^] | VAE generative model | Data-driven (PLAsTiCC trained) | Any (model is survey-agnostic after training) | HDF5 model files; sncosmo compatible | Redshift-invariant latent space; produces synthetic spectra; anomaly detection | Requires large training set; trained models available for PLAsTiCC+PS1 only |
| **Avocado** [^9^] | GP augmentation+classifier | Uses existing simulations | LSST (primary) | LightGBM model | Winning PLAsTiCC entry; GP augmentation handles biased training sets; redshift-independent classification | Not a simulator per se -- needs input simulations to augment |
| **SuperNNova** [^10^] | RNN classifier framework | SNANA-generated | Any SNANA output | PyTorch models; HDF5/CSV | Bayesian RNNs; excellent uncertainty calibration; early-time classification | Requires SNANA format input; primarily Ia vs non-Ia |
| **LightCurveLynx** [^22^] | Python forward-modeling | Wraps SNCosmo, PZFlow, Redback, custom | Any (user-defined ObsTable) | Python objects; pandas | Modern Python framework; modular; wrappers for existing packages | New package (2024-2025); less mature than SNANA; community still building |
| **MOSFiT** [^23^] | Physical model fitter | Semi-analytical physical models | Any (via Open Astronomy Catalogs) | JSON outputs; model posteriors | Physics-based; generates synthetic photometry from model posteriors; shares fits to public catalogs | Slower (MCMC-based); physical models may not match all transient diversity |

---

## Trends & Signals

### 1. Shift from Generic to Survey-Specific Simulations
Early datasets (SNPCC) used idealized survey configurations. Modern datasets (Hourglass, ELAsTiCC2, OpenUniverse) model specific upcoming facilities with increasing fidelity, including instrument-specific noise characteristics, detector effects, and even pixel-level simulations [^6^][^7^].

### 2. Multimodal Data Integration
The Maven dataset [^17^] represents a new trend: combining photometric light curves with synthetic spectra and metadata (redshift, host properties) for multimodal foundation models. This mimics how real surveys will have access to multiple data types.

### 3. Real-Time and Streaming Classification
ELAsTiCC [^3^] was specifically designed to test real-time broker pipelines with simulated alert streams. The alert format (AVRO), forced photometry history, and streaming architecture match the actual LSST alert distribution system. This represents a shift from static batch classification to dynamic, online classification.

### 4. Synthetic Pre-Training + Real Fine-Tuning
The Maven approach [^17^] of pre-training on large simulated datasets then fine-tuning on smaller real datasets using contrastive learning has emerged as a powerful paradigm. This addresses the fundamental problem of limited labeled real data while leveraging the volume of simulations.

### 5. Open Science Infrastructure
The trend toward hosting datasets on Zenodo [^14^][^6^], HuggingFace [^17^], and AWS Open Data Registry [^7^] with DOIs has dramatically improved accessibility. Combined with packages like LightCurveLynx [^22^] that provide Python-native simulation frameworks, the barrier to entry for new researchers has lowered significantly.

### 6. Physics-Informed Deep Learning
ParSNIP [^8^] demonstrates the value of embedding physical symmetries (redshift invariance, dust extinction models) directly into neural network architectures. This approach produces more generalizable models than pure data-driven approaches.

---

## Recommended Deep-Dive Areas

### Priority 1: PLAsTiCC + ELAsTiCC2 Combined Analysis
**Why**: These are the largest and most realistic LSST simulations available. ELAsTiCC2 uses updated cadence (baseline 3.2 with rolling) and is the current state-of-the-art for LSST preparation. Combined analysis across both datasets could quantify how much classification performance improves with updated survey simulations.

### Priority 2: Roman Hourglass for Cross-Survey Transfer Learning
**Why**: The Hourglass simulation [^6^] is the first comprehensive Roman simulation with both photometry and spectroscopy. Testing whether classifiers trained on PLAsTiCC/ELAsTiCC (optical) transfer to Roman (NIR) data is critical for joint Roman+Rubin science. The inclusion of prism spectra enables novel multimodal training approaches.

### Priority 3: Simulation Fidelity Assessment
**Why**: Multiple papers [^12^] have shown that SNPCC-trained classifiers overestimate CCSN accuracy. A systematic study comparing classification performance across SNPCC -> PLAsTiCC -> ELAsTiCC -> real ZTF/DES data would quantify the simulation-to-reality gap and inform requirements for future simulation fidelity.

### Priority 4: OpenUniverse2024 for Image-Based Classification
**Why**: The 400TB OpenUniverse dataset [^7^] provides pixel-level simulated images for both Roman and Rubin. This enables training of image-based classifiers (like BTSbot [^19^]) on simulated data before real survey operations, a capability that has not been widely explored for supernovae.

### Priority 5: LightCurveLynx for Custom Simulation Generation
**Why**: LightCurveLynx [^22^] represents the next generation of simulation tools, offering Python-native flexible simulation with wrappers for SNCosmo, PZFlow, and other packages. Evaluating its capabilities for generating tailored training datasets for specific ML projects could unlock new research directions.

### Priority 6: Active Learning with Simulated Data
**Why**: The Active Learning for SN classification approach [^24^] showed that only 12% of the SNPCC training sample was needed to achieve comparable results with intelligent sampling. Combining this with the large ELAsTiCC2 dataset could dramatically reduce the need for expensive spectroscopic follow-up in future surveys.

---

## Complete Reference List

[^1^]: Kessler, Conley, Jha, Kuhlmann et al. 2010a, "Supernova Photometric Classification Challenge," arXiv:1001.5210

[^2^]: Kessler, Narayan, Avelino et al. 2019, "Models and Simulations for PLAsTiCC," PASP 131, 094501, arXiv:1903.11756

[^3^]: DESC ELAsTiCC portal: https://portal.nersc.gov/cfs/lsst/DESC_TD_PUBLIC/ELASTICC/; ELAsTiCC2 training: https://portal.nersc.gov/cfs/lsst/DESC_TD_PUBLIC/ELASTICC/ELASTICC2_TRAINING_SAMPLE_2

[^4^]: Kessler, Bernstein, Cinabro et al. 2009, "SNANA: A Public Software Package for Supernova Analysis," ApJS 185, 32; GitHub: https://github.com/rickkessler/SNANA

[^5^]: SNDATA_ROOT Zenodo: https://zenodo.org/records/12655677 (latest: https://zenodo.org/records/19503606)

[^6^]: Rose, Vincenzi, Hounsell et al. 2025, "The Hourglass Simulation," ApJ (accepted), arXiv:2506.05161; Data: https://doi.org/10.5281/zenodo.14262943

[^7^]: OpenUniverse collaboration 2025, "OpenUniverse2024," arXiv:2501.05632; Data: https://irsa.ipac.caltech.edu/data/theory/openuniverse2024/overview.html

[^8^]: Boone 2021, "ParSNIP: Generative Models of Transient Light Curves with Physics-enabled Deep Learning," AJ 162, 275; GitHub: https://github.com/LSSTDESC/parsnip

[^9^]: Boone 2019, "Avocado: Photometric Classification of Astronomical Transients with Gaussian Process Augmentation," AJ 158, 257, arXiv:1907.04690

[^10^]: Möller & de Boissière 2020, "SuperNNova: an open-source framework for Bayesian, neural network-based supernova classification," MNRAS 491, 4277; Zenodo data: https://zenodo.org/records/3265189; GitHub: https://github.com/supernnova/SuperNNova

[^11^]: Qu et al. 2021, "SCONE: Supernova Classification with Oracle Network Estimation," ApJ 921, 14

[^12^]: Jones et al. 2017 (PS1-MDS classification paper); Villar et al. 2019; multiple subsequent papers documenting SNPCC limitations for CCSN

[^13^]: Kessler et al. 2010b, "Results from the Supernova Photometric Classification Challenge," PASP 122, 1415, arXiv:1008.1024

[^14^]: PLAsTiCC unblinded data: https://zenodo.org/records/2539456 (v1, 7.5 GB)

[^15^]: PLAsTiCC model libraries: https://doi.org/10.5281/zenodo.6672739

[^16^]: SuperNNova simulations: https://zenodo.org/records/3265189 (1,983,213 light curves, ~1 GB)

[^17^]: Zhang et al. 2024, "Maven: A Multimodal Foundation Model for Supernovae," NeurIPS 2024 Workshop; Data: https://huggingface.co/datasets/thelfer/multimodal_supernovae

[^18^]: DES-SN5YR: https://github.com/des-science/DES-SN5YR; Sánchez et al. 2024, ApJ 975, 5

[^19^]: BTSbot: https://github.com/nabeelre/BTSbot; Rehemtulla et al., ML4Astro ICML 2023

[^20^]: Muthukrishna et al. 2019, "RAPIDS: Real-time Automated Photometric Identification of Supernovae," ApJS 245, 27

[^21^]: Barbary et al. 2016, "SNCosmo: Python library for supernova cosmology," ASCL 1602.012; https://sncosmo.github.io/

[^22^]: Dai et al. 2026, "LightCurveLynx: Forward Modeling of Time-Domain Surveys," arXiv:2604.07134; https://lightcurvelynx.readthedocs.io/

[^23^]: Guillochon et al. 2018, "MOSFiT: Modular Open Source Fitter for Transients," ApJS 236, 6; https://mosfit.readthedocs.io/

[^24^]: Ishida et al. 2019, "Active Learning for Supernova Photometric Classification," MNRAS 483, 2

[^25^]: Kessler et al. 2025, "Cosmology Constraints from Type Ia Supernova Simulations of the Roman Space Telescope," arXiv:2506.04402

[^26^]: Leoni et al. 2022, "Fink: Early supernovae Ia classification using active learning," A&A 663, A13, arXiv:2111.11438

[^27^]: Nabat et al. 2024 (Roman cosmology paper with SCONE classifier training)

---

## Quick Reference: Dataset URLs

| Dataset | URL | Size | Access |
|---------|-----|------|--------|
| SNPCC data | Via SNANA package (sndata_root) | ~2 GB | Download SNANA + SNDATA_ROOT |
| PLAsTiCC unblinded | https://zenodo.org/records/2539456 | 7.5 GB | Free download |
| PLAsTiCC models | https://doi.org/10.5281/zenodo.6672739 | ~2 GB | Free download |
| ELAsTiCC2 training | https://portal.nersc.gov/cfs/lsst/DESC_TD_PUBLIC/ELASTICC/ELASTICC2_TRAINING_SAMPLE_2 | 7.4 GB | Free download |
| Hourglass (Roman) | https://doi.org/10.5281/zenodo.14262943 | ~GBs | Free download |
| OpenUniverse2024 | https://irsa.ipac.caltech.edu/data/theory/openuniverse2024/ | 400 TB | Cloud (AWS) or IPAC |
| SuperNNova sims | https://zenodo.org/records/3265189 | ~1 GB | Free download |
| SNDATA_ROOT | https://zenodo.org/records/12655677 | 2.0 GB | Free download |
| Maven dataset | https://huggingface.co/datasets/thelfer/multimodal_supernovae | ~GBs | Free download |
| DES-SN5YR sims | https://github.com/des-science/DES-SN5YR | Variable | Free download |
| BTSbot training | Via GitHub + Zenodo | Variable | Free download |

---

*End of Report*

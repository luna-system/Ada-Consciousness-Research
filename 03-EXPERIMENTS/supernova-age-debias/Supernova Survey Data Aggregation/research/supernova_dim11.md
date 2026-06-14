# Dimension 11: Multi-messenger & Emerging Data Streams for Supernova Research

## Executive Summary

This document provides a comprehensive catalog of multi-messenger and emerging data streams relevant to supernova (SN) research and machine learning (ML) applications. We cover radio transient surveys (ASKAP VAST, LOFAR LoTSS, MeerKAT ThunderKAT, VLASS), neutrino alert systems (SNEWS 2.0, IceCube, DUNE), gravitational wave (GW) counterpart search infrastructures (GCN/TAN, ZTF, Fritz), citizen science projects (SNAD, Zooniverse), and software packages for neutrino simulation (SNEWPY). Each dataset is assessed for ML-readiness, data volume, access methods, and relevance for next-generation supernova studies.

---

## 1. ASKAP VAST: Variables and Slow Transients Survey

### 1.1 Overview
The ASKAP (Australian Square Kilometre Array Pathfinder) Variables and Slow Transients (VAST) Survey is a systematic exploration of the dynamic radio sky, targeting slowly evolving synchrotron transients in the southern sky [^369^]. ASKAP operates at 888 MHz with 288 MHz bandwidth, using 36 12-meter dishes equipped with phased array feeds (PAF), providing a large ~30 deg^2 field of view [^861^].

### 1.2 Data Release 1 (DR1) Specifications
- **Observation period**: June 2023 to May 2025 [^369^]
- **Sky coverage**: ~12,300 deg^2 (276 fields) [^369^]
- **Number of images**: 2,945 images [^369^]
- **Central frequency**: 888 MHz [^369^]
- **Typical rms sensitivity**: 0.24 mJy/beam [^369^]
- **Angular resolution**: 12-20 arcseconds [^369^]
- **Cadence**: Each field revisited approximately every 2 months, yielding 10-11 epochs per field [^369^]
- **Light curve database**: 0.5 million sources with 6.4 million individual measurements [^369^]

### 1.3 Transient Detections in DR1
An untargeted variability search identified 117 astrophysical variables [^369^]:
- 27 pulsars
- 40 radio stars (10 newly detected at radio wavelengths)
- 44 active galactic nuclei (AGN)
- **2 optically identified supernovae**
- **1 supernova candidate**
- 1 brown dwarf
- 2 unidentified sources without multi-wavelength counterparts

### 1.4 Data Access
- **Primary portal**: CSIRO Data Access Portal (DAP) at https://data.csiro.au/collection/csiro:72199 [^371^]
- **Data products**: Light curve database with measurements catalogue, source catalogue, and image catalogue [^371^]
- **Format**: FITS images, CSV catalogues (Selavy source finder component catalogue format) [^371^]
- **Access**: Publicly available; no proprietary restrictions

### 1.5 Radio Supernova Applications
VAST data has been used to study late-time radio re-brightening in core-collapse supernovae (CCSNe), including SN 2016coi, SN 2003bg, and SN 2017gmr [^861^]. ASKAP's 887.5 MHz observations are sensitive to CCSNe out to z~0.15 (~700 Mpc) for the most luminous events, with typical detection limits of ~8 Mpc for average CCSNe peak luminosities [^861^].

### 1.6 ML-Readiness Assessment
| Feature | Status |
|---------|--------|
| Light curve data | ✅ Public, uniform format |
| Data volume | Moderate (0.5M sources, 6.4M measurements) |
| Cadence | Bimonthly - suitable for slow transient studies |
| Radio SNe samples | Small (3 SN-related sources in DR1) |
| Multi-epoch coverage | Good (10-11 epochs) |
| Sky coverage | Southern sky (declination < +41 deg) |
| **ML Suitability** | ⚠️ Limited by small SN sample; excellent for variable/transient population studies |

---

## 2. LOFAR LoTSS: LOFAR Two-metre Sky Survey

### 2.1 Overview
The LOFAR Two-metre Sky Survey (LoTSS) is the largest low-frequency radio survey ever conducted, operating at 120-168 MHz with the LOw-Frequency ARray (LOFAR) across Europe [^830^]. LOFAR consists of 38 stations in the Netherlands and 14 international stations, with maximum baselines of ~2,000 km [^831^].

### 2.2 Data Release 3 (DR3) Specifications
- **Observation period**: >10.5 years of data accumulation [^830^]
- **Sky coverage**: 19,035 deg^2 (88% of the northern sky) [^842^]
- **Total data volume**: 18.6 PB of raw data from 12,950 hours of observations [^830^]
- **Central frequency**: 144 MHz [^842^]
- **Angular resolution**: 6 arcsec (9 arcsec below declination +10 deg) [^830^]
- **Median sensitivity**: 92 uJy/beam [^842^]
- **Source catalogue**: 13,664,379 radio sources (16,943,656 Gaussian components) [^842^]
- **Astrometric accuracy**: ~0.24 arcsec systematic [^830^]
- **Flux density scale accuracy**: 6% random, 2% systematic [^830^]

### 2.3 Data Products and Access
All data products are publicly available [^842^]:
- **Source catalogues**: PyBDSF source and Gaussian catalogues (v1.0) at https://lofar-surveys.org/dr3.html [^840^]
- **Mosaic images**: Stokes I at 6" and 20" resolution [^842^]
- **Individual field images**: Stokes I, Q, U, V at 6" and 20" resolution [^842^]
- **UV data**: Calibrated measurement sets with direction-dependent calibration solutions [^842^]
- **Access method**: Download via LoTSS DR3 page; individual pointing products available upon request (email: lotss-dr3-infrastructure@strw.leidenuniv.nl)
- **Processing**: Direction-independent and direction-dependent calibration pipelines correcting for instrumental and ionospheric effects [^830^]

### 2.4 Supernova-Relevant Science
LoTSS-DR3 has uncovered rare objects including faint supernova remnants and flaring/interacting stars [^831^]. The combination of wide sky coverage, high sensitivity, and fine angular resolution makes rare and previously difficult-to-detect objects visible [^836^].

### 2.5 ML-Readiness Assessment
| Feature | Status |
|---------|--------|
| Source catalogue | ✅ 13.7M sources |
| Data volume | Large (18.6 PB raw, reduced products public) |
| Frequency | Low (144 MHz) - unique for CSM interaction studies |
| Transient capability | Static survey; time-domain requires epoch comparison |
| Sky coverage | Northern sky (88%) |
| **ML Suitability** | ⚠️ Primarily a static survey; valuable for radio SN host galaxy studies and SN remnant identification |

---

## 3. MeerKAT ThunderKAT: Image-Plane Radio Transients

### 3.1 Overview
ThunderKAT is the image-plane transients programme for MeerKAT, a 64-dish cm-wave telescope and SKA precursor in the southern hemisphere [^877^]. It performs targeted monitoring of Galactic synchrotron transients and extragalactic synchrotron transients including supernovae [^878^].

### 3.2 Key Components (approved 2016-2022)
- X-ray binaries
- Cataclysmic Variables
- Short Gamma-Ray Bursts
- **Supernovae Type Ia** [^878^]

### 3.3 Unique Features
- **Commensal observing**: ThunderKAT has agreements with other MeerKAT Large Survey Projects to search their data for transients, effectively increasing discovery space by factor of ~10 [^877^]
- **MeerLICHT**: Simultaneous optical imaging for each radio transient detected [^878^]
- **Citizen science**: Radio Galaxy Zoo and other Zooniverse projects for transient identification [^883^]

### 3.4 Data Access
- Data products available through SARAO (South African Radio Astronomy Observatory)
- Radio Galaxy Zoo citizen science classifications: https://www.zooniverse.org/projects/zookeeper/radio-galaxy-zoo
- Commensal transient search methodologies documented in publications [^880^]

---

## 4. SNEWS 2.0: SuperNova Early Warning System

### 4.1 Overview
SNEWS (SuperNova Early Warning System) is a worldwide network of neutrino detectors designed to provide automated early alerts for galactic core-collapse supernovae [^822^]. The original SNEWS has been operational since 1998, running in fully-automated mode since 2005 [^822^].

### 4.2 SNEWS 2.0 Specifications
SNEWS 2.0 represents a major upgrade for the multi-messenger astronomy era [^906^]:
- **Alert threshold**: Reduced threshold for generating alerts to gain sensitivity
- **Alert latency**: Reduced compared to SNEWS 1.0
- **Pointing**: Combines pointing information from individual experiments; enhances via timing triangulation
- **Pre-supernova alert**: Based on rising neutrino flux from silicon burning preceding core-collapse
- **Follow-up strategy**: Develops observing strategy for astronomical community
- **Citizen science engagement**: Interfaces with amateur astronomer and citizen science communities [^910^]

### 4.3 Participating Detectors
Current and planned participating experiments [^822^][^910^]:
- **Water Cherenkov**: Super-Kamiokande (Japan), IceCube (South Pole)
- **Liquid Scintillator**: KamLAND (Japan), Borexino (Italy), LVD (Italy), Daya Bay (China), JUNO (under construction)
- **Other**: HALO (Canada), KM3NeT, NOvA, Baksan
- **Future**: DUNE, Hyper-Kamiokande, XENON1T/dark matter detectors

### 4.4 Alert System
- **Primary server**: Brookhaven National Laboratory
- **Backup server**: University of Bologna
- **Coincidence window**: 10 seconds
- **Alert tiers**: Gold (automatic worldwide), Silver (experiments only) [^910^]
- **False alarm rate**: Less than one per century for Gold alerts
- **Website**: https://snews.bnl.gov

### 4.5 Data Sharing Tiers
1. **Alert tier**: Above-threshold activity messages
2. **Significance tier**: Signal significance, p-values, skymaps
3. **Rich data tier**: Neutrino light curves, distance estimates, full data sharing [^910^]

### 4.6 ML-Readiness Assessment
| Feature | Status |
|---------|--------|
| Neutrino light curves | Available from simulations (SNEWPY) |
| Real-time alerts | ✅ GCN/TAN integration |
| Pointing information | ~3-5 deg (Super-K), triangulation possible |
| Historical data | No galactic SN since 1987A |
| **ML Suitability** | Training on simulated data; real-time event classification systems |

---

## 5. SNEWPY: SuperNova Neutrino Early Warning Models for Python

### 5.1 Overview
SNEWPY is an open-source Python package that bridges the gap between supernova neutrino simulations and expected detector signals on Earth [^821^]. It was developed explicitly for SNEWS 2.0 but is broadly useful for modelers and experimentalists [^821^].

### 5.2 Key Features
- **Unified interface**: Simple access to hundreds of supernova simulations [^375^]
- **Flavor transformations**: Large library of flavor transformation prescriptions [^375^]
- **SNOwGLoBES integration**: Python interface to compute event rates in different neutrino detectors [^375^]
- **Complete pipeline**: From simulation data to observable detector signals [^821^]

### 5.3 Supported Supernova Models
The `snewpy.models` module interfaces with simulation datasets including [^818^][^376^]:
- Bollig 2016 (11.2 M_sun)
- Tamborra 2014 (11.2 M_sun)
- Nakazato 2013 (13 M_sun)
- And many more (hundreds of simulations from various modeling groups)

### 5.4 Pipeline Components
1. **snewpy.models**: Extract neutrino emission as function of time, energy, angle, flavor
2. **snewpy.flavor_transformation**: Convolve spectra with flavor transformation prescriptions
3. **snewpy.snowglobes**: Interface to SNOwGLoBES for event rate computation [^821^]

### 5.5 Installation and Documentation
- **Documentation**: https://snewpy.readthedocs.io [^375^]
- **Installation**: pip installable
- **Paper**: arXiv:2109.08188 [^821^]
- **Jupyter notebooks**: CCSN models, Pre-SN models, usage tutorials [^375^]

### 5.6 ML Applications
- Generate synthetic neutrino detector signals for ML training
- Model discrimination using ML classifiers on detector data [^902^]
- Parameter inference (energy spectra, flavor composition, time distributions)
- Sensitivity studies for future detectors (DUNE, Hyper-K, JUNO) [^818^]

---

## 6. IceCube and IceCube-Gen2: Neutrino Burst Detection

### 6.1 Current IceCube Sensitivity
- **Location**: South Pole (cubic-kilometer detector) [^911^]
- **Optical modules**: 5,160 DOMs
- **Supernova detection**: Searches for collective excess of detection rate above noise floor
- **11-year search**: No evidence for galactic CCSNe found (2008-2019) [^912^]
- **Sensitivity**: >99% of galactic supernovae from progenitor stars, even with minimal mass [^911^]
- **Distance reach**: Mass-independent sensitivity above 10 sigma within entire Milky Way; limited sensitivity for LMC/SMC depending on model [^909^]
- **90% C.L. upper limit**: 0.23/yr on core-collapse supernovae out to ~25 kpc [^912^]

### 6.2 IceCube-Gen2 Projected Sensitivity
- **Size**: ~8x larger optical array than current IceCube [^909^]
- **New sensors**: ~10,000 new sensors with segmented mDOM technology
- **Coincidence-based method**: Two-stage trigger using local coincidences (20 ns) + global multiplicity
- **False alarm rate**: <1 per century with coincidence-based method [^909^]
- **Distance reach**: Observable out to 270 kpc in 50% of cases [^909^]
- **Machine learning tools**: Energy reconstruction framework using ML under development [^909^]

### 6.3 Real-Time Alerts
- Gold alerts issued for high-energy neutrino candidate events
- Integration with GCN/TAN network
- Website: https://icecube.wisc.edu

---

## 7. DUNE: Deep Underground Neutrino Experiment

### 7.1 Overview
DUNE is a next-generation long-baseline neutrino experiment with four 10-kton liquid argon time projection chambers (LArTPCs) in South Dakota [^833^]. DUNE has unique sensitivity to electron neutrinos from supernovae [^888^].

### 7.2 Supernova Detection Capabilities
- **Channels**: Primarily ve + 40Ar --> e- + 40K* (charged-current); also elastic scattering and neutral current [^322^]
- **Expected events**: ~3,000 events at 10 kpc for 40 kton (model-dependent) [^888^]
- **Energy range**: 5-100 MeV [^818^]
- **Galaxy coverage**: >90% efficiency on SN burst at distances up to >=20 kpc [^322^]
- **Trigger scheme**: Real-time algorithm using TPC or photon detection system information [^833^]

### 7.3 Supernova Pointing
- **Resolution**: 3.4 deg at 68% CL for 40 kton, perfect event classification [^888^][^889^]
- **Realistic resolution**: 4.3 deg (8.7 deg for single 10 kton module) with 4% misclassification [^888^]
- **Technique**: "Brems flipping" for head-tail disambiguation + maximum likelihood method [^888^]
- **Goal**: Contribute pointing information to SNEWS 2.0 within minutes [^322^]

### 7.4 Machine Learning for DUNE Supernova Trigger
Research is actively developing ML-based triggers [^833^][^837^][^838^]:
- **Sparse CNN**: Pixel classification distinguishing tracks (protons, muons) from showers (electrons)
- **Data reduction**: ML-based extreme data reduction for prompt supernova pointing [^833^]
- **Image dimensions**: 512x512 pixel representations of LArTPC interactions
- **Performance**: High accuracy in pixel classification; potential for real-time trigger [^837^]
- **Challenges**: Low-energy regime presents unique triggering and reconstruction challenges [^322^]
- **Neural network architectures**: CNNs, Graph NNs, Sparse CNNs being benchmarked [^902^]

### 7.5 ProtoDUNE
- ProtoDUNE-SP (Single Phase) and ProtoDUNE-DP (Dual Phase) are test detectors at CERN
- Used for validating LArTPC technology and reconstruction algorithms [^897^]
- Supernova trigger development includes full detector simulation with backgrounds [^835^]

### 7.6 ML-Readiness Assessment
| Feature | Status |
|---------|--------|
| Simulated data | ✅ Extensive (LArSoft, MARLEY) |
| Real detector data | ProtoDUNE available; far detector under construction |
| Data format | LArTPC images (sparse 3D data) |
| ML pipelines | Under active development |
| **ML Suitability** | Excellent for developing SN neutrino detection and classification algorithms |

---

## 8. Gravitational Wave Counterpart Searches

### 8.1 LIGO/Virgo/KAGRA Observing Runs
- **O4**: May 2023 - present (two parts: O4a May 2023-Jan 2024, O4b April 2024-present) [^860^]
- **O4a detections**: 81 significant candidates (92 total - 11 retracted) [^863^]
- **O4b so far**: 68 significant candidates [^863^]
- **O5 goal**: 1.5x astrophysical range, 3+ times more detections [^863^]
- **BNS mergers in O4**: S230518h, S230529ay (confirmed as GW230529), S240422ed (retracted) [^860^]

### 8.2 ZTF Follow-up of GW Events
The Zwicky Transient Facility (ZTF) has been a primary electromagnetic follow-up facility for GW events [^820^]:
- **Fritz platform**: Web-based system for managing GW event information, triggering observations, candidate vetting [^820^]
- **SniperGW**: Open-source backup for programmatic ZTF scheduler access [^820^]
- **Alert stream**: Real-time alerts issued to brokers (ALeRCE, AMPEL, ANTARES, Fink, Lasair, Pitt-Google) [^820^]
- **Re-weighting strategy**: Immediate access to ZTF images and alerts from GW follow-ups [^820^]
- **O4a summary paper**: "Searching for Gravitational Wave Optical Counterparts with the Zwicky Transient Facility: Summary of O4a" [^820^]

### 8.3 Recent GW-Supernova Events
- **S250818k**: Sub-threshold sub-solar gravitational wave trigger with candidate superkilonova AT2025ulz/ZTF25abjmnps [^817^]
- **Follow-up**: Extensive observations by ZTF, GOTO, Pan-STARRS1, Gemini, Keck, Liverpool Telescope, CFHT, and others [^817^][^819^]
- **nuztf pipeline**: Selected 58 candidates with at least two detections; identified ZTF25abjmnps as only plausible counterpart [^817^]

### 8.4 GOTO: Gravitational-wave Optical Transient Observer
- **Dual-hemisphere network**: La Palma (North) and Siding Spring (Australia) [^862^]
- **O4 performance**: Median delay from GW alert to first observation ~3 hours; nearly 1 million difference-image detections processed [^862^]
- **Coverage**: Up to 95% of skymap localization probability in single night with dual sites [^862^]

### 8.5 GCN/TAN Alert Network
- **GCN Circulars**: Human-readable citable reports for follow-up observations [^885^]
- **GCN Notices**: Real-time automated alerts with event localization [^885^]
- **Integration**: Connects GW, neutrino, gamma-ray, and optical communities [^819^]
- **Website**: https://gcn.nasa.gov

### 8.6 Multi-messenger Correlation Features for ML
Key features for ML classifiers in multi-messenger SN searches:
- **Time coincidence**: GW neutrino and EM signals arrive within seconds to hours [^895^]
- **Skymap localization**: GW skymap area (tens to thousands of sq deg) [^860^]
- **Distance estimates**: GW luminosity distance + redshift from host galaxy [^820^]
- **Color evolution**: Kilonova candidates identified by rapid color evolution [^817^]
- **Rising/fading rates**: Superkilonova candidates show unique light curve evolution [^817^]
- **Contextual features**: Host galaxy photometric redshift, offset from galaxy center [^817^]

### 8.7 ML-Readiness Assessment
| Feature | Status |
|---------|--------|
| GW event alerts | ✅ Public via GraceDB/GCN |
| EM follow-up data | Available through GCN Circulars |
| Candidate light curves | ZTF, PS1, GOTO archives |
| Classification | Real-bogus scoring (ZTF), broker-based ML |
| Multi-messenger features | Time, position, distance, color evolution |
| **ML Suitability** | Good for developing automated counterpart identification |

---

## 9. Alert Brokers and Real-Time Classification

### 9.1 ALeRCE (Automatic Learning for the Rapid Classification of Events)
- **Origin**: Chilean-led broker [^907^]
- **ZTF processing**: Real-time ingestion, aggregation, cross-matching, ML classification, visualization [^907^]
- **Classifiers**: Stamp-based CNN (94% accuracy on balanced test set) + light curve-based classifier [^908^]
- **SN Hunter**: Visualization tool for SN candidate discovery [^908^]
- **Results (2019-2021)**: 1.5x10^8 alerts processed, 6,846 SN candidates reported, 971 spectroscopically confirmed [^907^]
- **Website**: https://alerce.science

### 9.2 Fink Broker
- **Features**: Active learning for optimized supernova follow-up [^726^]
- **Real-time AL**: First real-time active learning application on survey data for SN Ia classification [^689^]
- **Performance**: Reduces follow-up time by ~40% compared to traditional methods [^726^]
- **Integration**: Connected to SNAD Viewer, Astro-COLIBRI [^158^]
- **Website**: https://fink-broker.org

### 9.3 AMPEL (Alert Management, Photometry, and Evaluation of Light Curves)
- **Framework**: Modular system for time-domain data analysis [^741^]
- **LSST readiness**: One of 7 approved LSST community brokers
- **Features**: ML workflows including ParSNIP classifier, modular and reproducible [^741^]
- **ELAsTiCC**: Participated in Extended LSST Astronomical Time-series Classification Challenge

### 9.4 Other Brokers
- **ANTARES**: Arizona-NOIRLab Temporal Analysis and Response to Events System
- **Lasair**: Edinburgh-led broker
- **Babamul**: Korean broker
- **Pitt-Google**: University of Pittsburgh
- **Website references**: https://rubinobservatory.org/for-scientists/data-products/alerts-and-brokers [^44^]

---

## 10. Citizen Science Projects

### 10.1 SNAD (SuperNova Anomaly Detection)

**Overview**: SNAD is a project for detecting unusual astronomical objects by their photometric features using machine learning + human expertise [^158^][^160^].

**Key Resources**:
- **Website**: https://snad.space [^158^]
- **GitHub**: https://github.com/snad-space/snad [^694^]
- **SNAD Viewer**: https://ztf.snad.space - centralized view of ZTF objects [^158^]
- **SNAD Transient Miner**: ML-based anomaly detection tool [^158^]
- **Supernova Catalog**: 144 new SN candidates identified in ZTF data [^158^]

**Data Sources**:
- Open Supernova Catalog (OSC): 1,999 light curves in g'r'i' [^158^]
- ZTF DR3: 2.25 million objects in 3 fields analyzed [^160^]
- ZTF public data releases

**Techniques**:
- 3-stage pipeline: feature extraction, outlier search with ML algorithms, expert identification [^160^]
- Active learning algorithms: Isolation Forest, Local Outlier Factor, etc. [^160^]
- Code: https://github.com/snad-space/zwad [^160^]

**Publications**:
- Pruzhinskaya et al. 2019 (Proceedings of Science) [^160^]
- Malanchev et al. 2021, MNRAS, 502, 5147 [^160^]
- "The SNAD Viewer" PASP 135, 1044 (2023) [^160^]

### 10.2 Zooniverse Supernova Hunters
- **Project**: https://www.zooniverse.org/projects/dwright04/supernova-hunters [^321^]
- **Goal**: Classify detections as real or bogus to improve detection algorithms
- **Approach**: Volunteers inspect astronomical images to identify supernovae
- **Status**: Active Zooniverse project

### 10.3 Galaxy Zoo: Weird and Wonderful (GZ:W&W)
- **Platform**: Zooniverse [^876^]
- **Purpose**: Combined human-machine anomaly detection pipeline
- **Dataset**: ~200,000 images from Subaru Hyper-Suprime Cam survey
- **Results**: ~2,000 volunteers identified mergers, gravitational lenses, ringed galaxies, supernova candidates, asteroids, potential white dwarfs [^876^]
- **Correlation with ML**: Found no appreciable correlation between ML anomaly scores and human chosen fraction, demonstrating complementary value [^887^]
- **SN-relevant tags**: #supernova_candidates identified by volunteers [^876^]

### 10.4 ML-Readiness Assessment
| Feature | Status |
|---------|--------|
| Labeled anomaly data | ✅ From SNAD + citizen science |
| Human-verified anomalies | Expert-curated from ML pipeline |
| Multi-wavelength viewer | SNAD Viewer integrates ZTF + archives |
| **ML Suitability** | Excellent for anomaly detection training; transferrable to radio SN searches |

---

## 11. Astro-COLIBRI: Multi-Messenger Platform

### 11.1 Overview
Astro-COLIBRI is a comprehensive platform for real-time multi-messenger astrophysics that combines a public RESTful API, real-time databases, cloud-based alert system, and user-friendly interfaces [^903^].

### 11.2 Features
- **Alert ingestion**: Multiple sources including GCN, VOEvent, ATel [^885^]
- **Real-time processing**: Automated filtering and contextualization
- **Platforms**: Website, iOS and Android apps [^903^]
- **Transient coverage**: Supernovae, GRBs, FRBs, flares, high-energy neutrinos, GWs [^901^]
- **Multi-messenger context**: Cross-matches events across messengers and wavelengths
- **Workshops**: 4th Astro-COLIBRI Multi-Messenger Astrophysics Workshop (October 2025) [^901^]

### 11.3 ML-Readiness
- Provides structured multi-messenger event data
- RESTful API enables programmatic access for ML pipelines
- Real-time alert streams suitable for automated follow-up triggering

---

## 12. Radio Supernovae for Machine Learning

### 12.1 MALT: Machine Learning for Transients
MALT is a general ML pipeline for multiwavelength transient classification, first applied to radio transients [^841^][^928^]:

**Pipeline**:
1. Data augmentation using Gaussian Processes (GP regression)
2. Feature extraction using wavelet decomposition
3. Classification with random forests

**Radio Dataset**:
- 87 (or 82) publicly available radio light curves from literature
- 11 classes: AGN, Algol, Flare Star, GRB, Kilonova, Magnetar, Nova, RS CVn, **Supernova**, TDE, XRB
- Sources: Green Bank Interferometer and other radio telescopes

**Results**:
- Realistic dataset: ~78% accuracy after 8 hours of observations [^928^]
- Simulated representative training: ~97% accuracy [^928^]
- Adding optical data: improves worst-performing class by 19% [^928^]
- **SN classification**: Moderate performance due to small sample diversity; SNe confused with TDEs [^841^]

**Key Challenge**: Publicly available radio transient data is scarce; small sample sizes hinder ML training [^841^]

### 12.2 Wavelet Feature Extraction
- Superior to simple flux difference features [^841^]
- Dimensionality reduction via PCA
- Contextual features (e.g., Galactic plane location) improve accuracy [^841^]

### 12.3 Expected Data Growth
Future surveys will dramatically increase radio transient samples:
- **MeerKAT/ThunderKAT**: Factor of ~10 increase in discovery space via commensal observing [^877^]
- **ASKAP VAST**: 0.5M sources in DR1; ongoing survey will grow [^369^]
- **SKA**: Next-generation sensitivity and survey speed
- **VLASS**: VLA Sky Survey providing additional radio counterparts [^924^]

---

## 13. Multi-Messenger Correlation Features for ML Classifiers

### 13.1 Time-Domain Features
| Feature | Description | Sources |
|---------|-------------|---------|
| Neutrino burst arrival | Prompt (within seconds of core collapse) | SNEWS, IceCube, DUNE |
| GW arrival | Coincident with neutrino burst (within seconds) | LIGO/Virgo/KAGRA |
| EM delay | Optical may be delayed by hours to days due to shock breakout | ZTF, LSST, ATLAS |
| Rising time | Kilonovae: rapid rise (~hours); supernovae: slower (~days) | All optical surveys |
| Fading rate | Different decay timescales for different transients | All optical surveys |

### 13.2 Spatial Features
| Feature | Description | Sources |
|---------|-------------|---------|
| GW skymap | Probability distribution on sky (tens to thousands sq deg) | GraceDB |
| Neutrino pointing | ~3-5 deg resolution (Super-K), triangulation with network | SNEWS 2.0 |
| Host galaxy offset | Distance from galaxy center for counterpart candidates | Legacy Surveys |
| Host redshift | Photometric/spectroscopic redshift of candidate host | PS1, SDSS |

### 13.3 Multi-Wavelength Features
| Feature | Description | Sources |
|---------|-------------|---------|
| Radio flux density | Synchrotron emission from CSM interaction | VAST, VLASS, LoTSS |
| Optical color (g-r, u-g) | Temperature evolution; kilonovae are redder | ZTF, PS1 |
| UV/X-ray emission | Shock breakout, circumstellar interaction | eROSITA, Swift |
| Spectral lines | H-alpha, He I for SN typing | Follow-up spectrographs |

### 13.4 Contextual Features
| Feature | Description | Value |
|---------|-------------|-------|
| Distance | Luminosity distance from GW + redshift | Mpc scale |
| HasNS probability | GW parameter estimation: probability of neutron star component | GraceDB |
| HasRemnant probability | Probability of ejected matter (kilonova likelihood) | GraceDB |
| Galactic latitude | Higher extinction/confusion near plane | Coordinate-based |

---

## 14. Time-Domain Radio Data Formats and Access

### 14.1 Common Formats
| Format | Description | Used By |
|--------|-------------|---------|
| FITS | Standard astronomy image format | VAST, VLASS, LoTSS |
| CASA Image | Radio astronomy image format (NRAO) | VLA, VLASS |
| Measurement Set (MS) | Interferometric UV data format | LOFAR, ASKAP, VLA |
| HDF5 | Hierarchical data format for large datasets | IceCube, DUNE simulations |
| VOEvent | XML-based alert format for transient events | GCN, FRB alerts |
| Avro/ZTF alert | Binary format for ZTF alert packets | ZTF, LSST |

### 14.2 Data Archives and Portals
| Archive | URL | Content |
|---------|-----|---------|
| CSIRO DAP (VAST) | https://data.csiro.au/collection/csiro:72199 | ASKAP VAST images, light curves |
| LoTSS Surveys | https://lofar-surveys.org/dr3.html | LoTSS-DR3 catalogues, images |
| CASDA | https://data.csiro.au | CSIRO ASKAP Science Data Archive |
| GraceDB | https://gracedb.ligo.org | GW event database, skymaps |
| GCN/TAN | https://gcn.nasa.gov | Gamma-ray burst/Transient alerts |
| SNAD Viewer | https://ztf.snad.space | ZTF object exploration |

---

## 15. Summary Table: All Datasets and Their ML-Readiness

| Dataset/Source | Data Volume | Format | Access | ML-Ready | SN-Relevant |
|--------------|-------------|--------|--------|----------|-------------|
| ASKAP VAST DR1 | 0.5M sources, 6.4M measurements | FITS, CSV | Public (CSIRO DAP) | ⚠️ (small SN sample) | Radio SNe, variables |
| LoTSS DR3 | 13.7M sources | FITS, catalogues | Public | ⚠️ (static survey) | SN remnants, hosts |
| MeerKAT ThunderKAT | Growing | CASA format | SARAO | ⚠️ (limited public data) | Radio SNe, transients |
| VLASS | Millions of sources | FITS | Public (CIRADA) | ⚠️ | Radio transients |
| SNEWS 2.0 | Alert system | VOEvent, email | Public subscription | ✅ (for real-time systems) | Neutrino burst alerts |
| SNEWPY | Hundreds of models | Python package | pip install | ✅ | Neutrino simulations |
| IceCube | 11+ years of data | Custom (HDF5) | Collaboration | ✅ (for trigger ML) | SN neutrino bursts |
| DUNE | Simulations | LArSoft/ROOT | Collaboration/FNAL | ✅ | SN detection, pointing |
| ZTF GW Follow-up | ~1M alerts/run | Avro, FITS | Public brokers | ✅ | Counterpart search |
| SNAD | 2.25M ZTF objects | Web viewer, code | Public | ✅ | Anomaly detection |
| Zooniverse: SN Hunters | Labeled images | Web interface | Public | ✅ | Real/bogus classification |
| GCN/TAN | >10^5 circulars | Email, web, VOEvent | Public | ✅ | Multi-messenger alerts |
| Astro-COLIBRI | Real-time alerts | REST API, apps | Public | ✅ | Multi-messenger context |
| ALeRCE | 1.5x10^8 alerts processed | Web, API | Public | ✅ | SN classification |
| Fink | ZTF + LSST streams | Web, API | Public | ✅ | SN Ia classification |
| eROSITA | eRASS:1-8 all-sky | FITS, event files | Public releases | ⚠️ | X-ray SN counterparts |
| MALT radio transients | 87 light curves | Text, code | Publication | ⚠️ (small sample) | Radio transient classification |

---

## 16. Areas Warranting Deeper Investigation

### 16.1 High-Priority
1. **ASKAP VAST DR2**: Expected to significantly expand the light curve database; SN samples will grow
2. **SKA precursors synergy**: Combining VAST, ThunderKAT, and MeerKAT data for unified radio transient catalogs
3. **DUNE first module commissioning**: Expected ~2028-2029; will provide first real LArTPC supernova neutrino data
4. **LSST alert stream**: Starting 2025; will dramatically increase transient discovery rates
5. **SNEWS 2.0 deployment**: Integration of new detectors (DUNE, JUNO, Hyper-K)

### 16.2 Medium-Priority
1. **Radio SN population studies**: Need larger samples for robust ML classification
2. **Real-time multi-messenger pipelines**: Astro-COLIBRI, AMON, and custom broker development
3. **ProtoDUNE ML datasets**: Public release of simulated LArTPC images for SN neutrino studies
4. **IceCube-Gen2 sensitivity studies**: ML-based energy reconstruction improvements
5. **Citizen science + ML pipelines**: Scaling Galaxy Zoo: W&W approach to SN searches

### 16.3 Technical Challenges
1. **Small sample sizes**: Radio SNe and GW-EM counterparts have limited training data
2. **Class imbalance**: Supernovae are rare compared to AGN and variable stars
3. **Real-time requirements**: Low-latency classification for follow-up triggering
4. **Data heterogeneity**: Different formats, resolutions, and cadences across messengers
5. **Simulation-to-reality gap**: ML models trained on simulations need validation with real data

---

## References

[^369^] de Ruiter et al., "The ASKAP Variables and Slow Transients (VAST) Extragalactic Survey - Data Release 1," arXiv:2602.22739, 2026.

[^371^] de Ruiter et al., "The ASKAP Variables and Slow Transients (VAST) extragalactic survey Data Release 1," PASA, Cambridge Core, 2026.

[^375^] SNEWPY Documentation, https://snewpy.readthedocs.io

[^376^] SNEWPY Theory Presentation, CERN Indico, 2022.

[^818^] arXiv:2411.07716, "Sensitivity Study of Supernova Neutrinos for Mass Hierarchy," 2024.

[^821^] JOSS Paper, "A Data Pipeline from Supernova Simulations to Neutrino Signals" (SNEWPY).

[^822^] SNEWS: The SuperNova Early Warning System, ADS Abstract.

[^830^] Shimwell et al., "The LOFAR Two-metre Sky Survey: VII. Third Data Release," arXiv:2602.15949, 2026.

[^831^] Leiden University Press Release, "Largest radio survey ever maps the Universe in unprecedented detail," 2026.

[^833^] IEEE Paper, "Machine Learning-Based Extreme Data Reduction for Prompt Supernova Pointing at DUNE," 2025.

[^835^] CERN Repository, "Supernova Neutrino Trigger and Heavy Neutral Lepton Sensitivity in DUNE," 2025.

[^837^] FNAL-PUB-24-0524, "Machine Learning for DUNE Supernova Trigger," 2024.

[^840^] LoTSS Data Releases, https://lofar-surveys.org/releases.html

[^841^] Sooknunan, "Classification of Multiwavelength Transients with Machine Learning," M.Sc. Thesis, UCT, 2019.

[^842^] LoTSS DR3 Public Data Release, https://lofar-surveys.org/dr3.html

[^860^] Nicholl et al., "Electromagnetic follow-up of gravitational waves: review and lessons learned," Phil. Trans. R. Soc. A, 2025.

[^861^] Late-time supernovae radio re-brightening in the VAST survey, Macquarie University, 2024.

[^862^] GOTO Observatory, "Follow-up of gravitational-wave alerts during LIGO-Virgo-KAGRA's fourth observing run," 2026.

[^876^] "Through the Citizen Scientists' Eyes," Citizen Science: Theory and Practice, 2024.

[^877^] Fender et al., "ThunderKAT: The MeerKAT Large Survey Project for Image-Plane Radio Transients," arXiv:1711.04132, 2017.

[^878^] ThunderKAT website, University of Cape Town.

[^885^] "TransientVerse," arXiv:2501.04247, 2025.

[^888^] "Supernova Pointing Capabilities of DUNE," arXiv:2407.10339, 2024; Phys. Rev. D 111, 092006, 2025.

[^890^] "Multi-messenger astrophysics of black holes and neutron stars," Frontiers in Astronomy and Space Sciences, 2024.

[^895^] Christensen, "Multi-messenger Astronomy," Moriond presentation.

[^897^] "Evaluating Machine Learning Models for Supernova Gravitational Wave Signal Classification," arXiv:2409.14508, 2024.

[^898^] GitHub: anpugeat/supernova-neutrino-classification.

[^899^] "LIGO Core-Collapse Supernova Detection Using Convolutional Neural Networks," Sensors, 2026.

[^900^] "Evaluating machine learning models for supernova gravitational wave signal classification," MNRAS, 2025.

[^901^] 4th Astro-COLIBRI Multi-Messenger Astrophysics Workshop, 2025.

[^903^] "Astro-COLIBRI: An Innovative Platform for Real-Time Multi-Messenger Astrophysics," arXiv:2602.02058, 2026.

[^906^] Kharusi et al., "SNEWS 2.0: A Next-Generation SuperNova Early Warning System," arXiv:2011.00035, 2020.

[^907^] Forster et al., "The ALeRCE Alert Broker," 2021.

[^908^] Carrasco-Davis et al., "Alert Classification for the ALeRCE Broker System," arXiv:2008.03309, 2020.

[^909^] Beise, "Improving Supernova Neutrino Detection in IceCube-Gen2," Uppsala Dissertations, 2026.

[^910^] "SNEWS 2.0: a next-generation supernova early warning system for multi-messenger astronomy," NJP, 2021.

[^911^] IceCube Collaboration, "IceCube search for hidden galactic core-collapse supernovae," 2023.

[^912^] IceCube Collaboration, "Search for Galactic core-collapse supernovae in a decade of data," ApJ 961, 84, 2024.

[^817^] "A Candidate Superkilonova from a Sub-threshold Sub-Solar Gravitational Wave Trigger," arXiv:2510.23732, 2025.

[^820^] "Searching for Gravitational Wave Optical Counterparts with ZTF: Summary of O4a," PASP, 2024.

[^817^] ZTF Collaboration, GCN Circulars for S250818k/AT2025ulz, 2025.

[^926^] arXiv:1811.08446, "Classification of Multiwavelength Transients with Machine Learning," 2018.

[^928^] Sooknunan et al., "Classification of Multiwavelength Transients with Machine Learning," MNRAS, 2021.

[^158^] "Exploring the Universe with SNAD: Anomaly Detection in Astronomy," arXiv:2410.18875, 2024.

[^160^] SNAD website, https://snad.space

[^694^] SNAD GitHub, https://github.com/snad-space/snad

[^321^] Zooniverse Supernova Hunters, https://www.zooniverse.org/projects/dwright04/supernova-hunters

[^887^] "Galaxy Zoo: Weird & Wonderful," AAS 243, 2024.

[^44^] Rubin Observatory Alerts and Brokers, https://rubinobservatory.org/for-scientists/data-products/alerts-and-brokers

[^726^] "Enhancing early SN Ia classification with the Fink broker," PASA, 2026.

[^689^] Fink Broker blog, "First real-time active learning for optimising supernova follow-up," 2025.

[^741^] "AMPEL workflows for LSST," A&A, 2025.

[^924^] "UNIONS Optical Identifications for VLASS Radio Sources (UNVEIL)," arXiv:2507.08604, 2025.

[^922^] SDSS DR19, "Galactic eROSITA Sources," https://www.sdss.org/dr19/mwm/programs/erosita/

[^925^] Predehl et al., "The eROSITA X-ray telescope on SRG," A&A, 2021.

[^864^] Astrobites, "A Machine Learning View of Supernova GWs," 2022.

[^880^] Chastain et al., "Commensal Transient Searches with MeerKAT," ApJ, 2025.

[^883^] Andersson et al., "The first citizen science project dedicated to commensal radio transients," 2023.

[^841^] Sooknunan thesis, "Classification of Multiwavelength Transients with Machine Learning," 2019.

[^863^] Di Renzo, "Astrophysical Searches in LIGO-Virgo-KAGRA O4," AHEAD2020 presentation.

[^865^] Virgo-GW, "LIGO-Virgo-KAGRA Runs."

[^890^] "Multi-messenger astrophysics of black holes and neutron stars," Frontiers, 2024.

[^895^] Christensen, "Multi-messenger Astronomy," Moriond.

[^897^] Cuesta presentation, "Supernova neutrinos in DUNE," CERN, 2025.

[^902^] "Supernova Model Discrimination and Pointing using Machine Learning," CERN presentation, 2025.

[^904^] "Machine-Learning Classification of Gamma-Producing Neutral Current Interactions from Supernova Neutrino Burst," Syracuse University PhD thesis, 2026.

[^82^] "Supernova classification from spectral data using machine learning," UPC, 2022.

[^905^] Mitra et al., "Probing nuclear physics with supernova gravitational waves," MNRAS, 2024.

[^909^] Beise, "Improving Supernova Neutrino Detection in IceCube-Gen2," Uppsala thesis, 2026.

[^911^] IceCube, "IceCube search for hidden galactic core-collapse supernovae," 2023.

[^912^] IceCube Collaboration, "Search for Galactic core-collapse supernovae," ApJ 961, 84, 2024.

[^927^] IceCube website, https://icecube.wisc.edu

[^924^] "UNIONS Optical Identifications for VLASS Radio Sources," arXiv:2507.08604, 2025.

[^876^] "Through the Citizen Scientists' Eyes," Citizen Science: Theory and Practice, 2024.

[^322^] Cuesta, "Supernova neutrinos in the DUNE experiment," Indico, 2025.

[^318^] "Supernova neutrino detection in DUNE," Orsay presentation.

[^896^] Cohen, "Supernova neutrino signal studies in the DUNE Far Detector," PhD thesis.

[^897^] Villa, "SuperNova pointing capabilities of DUNE," 2025.

[^892^] DUNE Publications, https://dune-data.fnal.gov/dunepublicplot/

[^893^] Inspire HEP, "Supernova pointing capabilities of DUNE."

[^894^] "Supernova Neutrino Detection with DUNE," ORNL presentation.

[^869^] (Note: Not used in final compilation)

[^870^] (Note: Not used in final compilation)

[^871^] (Note: Not used in final compilation)

[^872^] (Note: Not used in final compilation)

---

*Document compiled: June 2025*
*Total searches performed: 25 across 10 independent search batches*
*Sources: arXiv preprints, peer-reviewed journals, official survey websites, conference proceedings, GitHub repositories, data archives*

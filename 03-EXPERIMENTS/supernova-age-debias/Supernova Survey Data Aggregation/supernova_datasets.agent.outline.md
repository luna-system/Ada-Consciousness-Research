# Complete Guide to Supernova Survey Datasets for Machine Learning

## Executive Summary (~1,500 words)
### Key Findings
#### Over 60 publicly available supernova datasets identified across 25+ active and legacy surveys
#### Simulated datasets (PLAsTiCC: 3.5M events, ELAsTiCC: 50M alerts) dwarf real labeled data (~3,000 spec-confirmed SNe Ia total)
#### Critical insight: the sim-to-real gap is the #1 unsolved problem in SN ML — classifiers trained on simulations show 5-15% accuracy degradation on real data
#### 7 Rubin community brokers now provide pre-trained classifications via Python APIs, enabling model-as-a-service approaches
#### A 12-month readiness window exists before Rubin proprietary restrictions limit access to real training data

## 1. Introduction (~2,500 words, 1 table)
### 1.1 Why Supernovae Matter for ML
#### 1.1.1 SNe as cosmological probes: Type Ia standard candles enabling precision dark energy measurement (Hubble constant tension, w0/wa constraints)
#### 1.1.2 The classification challenge: photometric typing without spectra (Ia vs II vs Ibc vs rare types), driving need for ML
#### 1.1.3 Scale of the opportunity: Rubin Observatory will detect 10M alerts/night, requiring automated classification at unprecedented throughput
### 1.2 The ML Practitioner's Landscape
#### 1.2.1 Overview of survey types: photometric vs spectroscopic, time-domain vs static, ground-based vs space-based, real vs simulated
#### 1.2.2 Key ML tasks: real-time classification, cosmology parameter estimation, anomaly detection, early-time typing, host galaxy association
#### 1.2.3 Table: survey landscape at a glance (name, type, wavelength, cadence, data volume, access URL)

## 2. Ground-based Optical & Time-Domain Surveys (~4,500 words, 3 tables)
### 2.1 Zwicky Transient Facility (ZTF)
#### 2.1.1 Dataset scope: DR1-DR24 via IRSA, 5,000-10,000 extragalactic transients/year, 24 public data releases
#### 2.1.2 Key products: bulk DR downloads, Avro alert streams, forced photometry service, matchfiles (5B+ light curves)
#### 2.1.3 ZTF SN Ia DR2: 3,628 spec-confirmed SNe Ia — the largest homogeneous spec-Ia sample available
#### 2.1.4 BTS (Bright Transient Survey): spectroscopically classified bright transient sample with follow-up
#### 2.1.5 Python access: IRSA TAP queries, wget/curl bulk download, ztfquery package, alert archive at UW
### 2.2 Pan-STARRS1 Medium Deep Survey (PS1-MDS)
#### 2.2.1 365 spec-confirmed SNe Ia with multi-band grizy light curves
#### 2.2.2 CasJobs SQL interface for catalog queries, catalog data access via STScI MAST
### 2.3 Dark Energy Survey (DES)
#### 2.3.1 DES-SN 5-Year Data Release: 31,636 DiffImg + 19,706 SMP light curves, 1,635 photometrically classified SNe Ia
#### 2.3.2 Data format: SNANA FITS, ASCII .FITRES; GitHub (des-science/DES-SN5YR) + Zenodo
#### 2.3.3 25 mock simulations included for systematic testing
### 2.4 Other Active Ground-based Surveys
#### 2.4.1 ASAS-SN: all-sky survey, 1,000+ SNe/year, public photometry via ASAS-SN Sky Patrol
#### 2.4.2 SkyMapper: Southern sky survey, SN data via TAP interface
#### 2.4.3 OGLE: microlensing survey with serendipitous SNe, photometry database
#### 2.4.4 Young Supernova Experiment (YSE): 1,975 SNe DR1, ParSNIP classifications, Zenodo
### 2.5 Legacy Ground-based Surveys
#### 2.5.1 SDSS-II SN Survey: ~500 SNe Ia, foundational dataset, SNANA format
#### 2.5.2 SNLS: 泽 understanding of the table shows approximately 500 SNe Ia, the SuperNova Legacy Survey
#### 2.5.3 ESSENCE: 200 SNe Ia for dark energy, now in compilation datasets
#### 2.5.4 PTF/iPTF: predecessor to ZTF, historical light curves in IPAC archive
### 2.6 Comparison Table
#### 2.6.1 Table: ground-based survey comparison (survey, years, SNe count, bands, cadence, data access URL)

## 3. Low-Redshift Anchor Surveys (~3,500 words, 2 tables)
### 3.1 Carnegie Supernova Project (CSP)
#### 3.1.1 CSP DR3: 134 SNe Ia with optical (ugriBV) + NIR (YJH) photometry — the gold standard low-z training set
#### 3.1.2 Data format: ASCII tarballs, SNooPy Python package for reading and analysis
#### 3.1.3 Critical role: low-z anchor for Hubble diagram, essential for standardization training
### 3.2 Center for Astrophysics (CfA) Archive
#### 3.2.1 CfA3 + CfA4 + stripped-envelope + Type II samples: ~278 SNe Ia total with thousands of spectra
#### 3.2.2 Bulk download in FITS format, comprehensive spectroscopic follow-up
#### 3.2.3 Role in training spectroscopic classifiers and cross-validation
### 3.3 Foundation Survey
#### 3.3.1 Foundation DR1: 225 SNe Ia in SNANA format, GitHub repository
#### 3.3.2 Host galaxy properties included, well-suited for cosmology ML
### 3.4 Other Low-z Resources
#### 3.4.1 KAIT/LOSS: historical nearby SN survey, photometry and spectra
#### 3.4.2 CfA Core-Collapse Program: Type II-P, II-L, IIn, IIb photometry and spectra
#### 3.4.3 Calán/Tololo: foundational SNe Ia sample from 1990s
### 3.5 The Low-z Training Gap
#### 3.5.1 Table: low-z survey comparison (survey, SNe Ia count, NIR coverage, format, access)
#### 3.5.2 The bottleneck: only ~3,000 spec-confirmed SNe Ia exist across ALL low-z surveys combined
#### 3.5.3 Implications: massive sim-to-real gap, need for domain adaptation and active learning

## 4. Spectroscopic Archives (~3,000 words, 2 tables)
### 4.1 WISeREP
#### 4.1.1 The world's largest SN spectroscopic archive: 72,503 spectra for 29,468 objects
#### 4.1.2 Bulk download via web interface, Python API (wiserep_api) for programmatic access
#### 4.1.3 Spectral diversity: 30+ instruments, heterogeneous resolutions, calibration methods
#### 4.1.4 ML applications: spectral classification, feature extraction (line velocities, equivalent widths), anomaly detection
### 4.2 Nearby Supernova Factory (SNfactory)
#### 4.2.1 300+ SNe Ia with integral-field unit (IFU) spectrophotometry — unique dataset
#### 4.2.2 SNIFS instrument data, spectral time series, SUGAR/SNEMO model inputs
#### 4.2.3 Data access via project website, specialized format requiring custom readers
### 4.3 SDSS-V and Spectroscopic Follow-up Programs
#### 4.3.1 SDSS-V multi-epoch spectroscopy for transient follow-up
#### 4.3.2 DEIMOS/Keck, VLT/X-shooter, Gemini public archives for SN spectra
#### 4.3.3 Table: spectroscopic archive comparison (archive, spectra count, SN count, instruments, access)
### 4.4 Spectral Classification Tools
#### 4.4.1 SNID: the classic cross-correlation tool (C++), 5,000+ spectral templates
#### 4.4.2 SNID-SAGE: modern Python replacement, 698 templates, PySide6 GUI, batch processing
#### 4.4.3 DASH: CNN-based spectral classifier, 97.5% type accuracy, 100x faster than Superfit
#### 4.4.4 Spectra-to-features pipeline: converting heterogeneous spectra to ML-ready feature vectors

## 5. Space-based & Multi-wavelength Datasets (~3,500 words, 2 tables)
### 5.1 TESS
#### 5.1.1 MIT TessTransients database: 307 SNe Ia + 4,000+ transients with 30-minute cadence
#### 5.1.2 Unique value: high-cadence light curves for early-time classification, shock breakout detection
#### 5.1.3 Bulk download via MIT database, CSV format
### 5.2 Kepler/K2
#### 5.2.1 23 SNe with 30-minute cadence photometry — the highest-quality extragalactic SN light curves ever obtained
#### 5.2.2 K2 Extragalactic Survey (KEGS) data via MAST archive
#### 5.2.3 Unique science: direct observation of shock breakout, early rise constraints
### 5.3 Swift/SOUSA
#### 5.3.1 MAST HLSP: 253 SNe with UVOT 6-filter photometry (uvw2, uvm2, uvw1, u, b, v)
#### 5.3.2 Critical UV data for dust extinction correction, early-time color evolution
### 5.4 GALEX
#### 5.4.1 gPhoton2 pipeline: 1,080 SNe Ia UV light curves from archival data
#### 5.4.2 VizieR catalog with UV photometry for SN population studies
### 5.5 Gaia Alerts
#### 5.5.1 10,785 alerts (through 2024), BP/RP low-resolution spectra for all alerts
#### 5.5.2 Real-time transient detection in scanning mode, southern sky advantage
#### 5.5.3 Gaia Science Alerts page, bulk alert history downloads
### 5.6 JWST and Hubble
#### 5.6.1 JWST first supernova spectroscopy at mid-infrared wavelengths
#### 5.6.2 HST archive: CANDELS, CLASH, Frontier Fields SN data via MAST
#### 5.6.3 Table: space-based mission comparison (mission, SNe count, cadence, wavelength, unique value, access)
### 5.7 The NIR Gap
#### 5.7.1 Despite NIR's critical role for high-z cosmology, publicly available NIR SN datasets are scarce
#### 5.7.2 CSP DR3 (YJH) and Roman Hourglass simulations are the primary NIR training resources
#### 5.7.3 Euclid Q1 NISP measurements represent the largest real NIR transient dataset currently available

## 6. Compilation & Aggregated Datasets (~3,000 words, 2 tables)
### 6.1 Open Supernova Catalog (OSC)
#### 6.1.1 50,000+ SNe with photometry, spectra, metadata; JSON per-SN files
#### 6.1.2 GitHub repository (astrocatalogs/supernovae), bulk download via sne.tar.lzma
#### 6.1.3 API access: api.astrocats.space for programmatic queries
#### 6.1.4 Strengths: comprehensive, multi-survey aggregation; weaknesses: heterogeneous quality, incomplete coverage
### 6.2 Pantheon+
#### 6.2.1 1,701 SNe Ia from 18 surveys — the definitive cosmology compilation
#### 6.2.2 GitHub DataRelease (PantheonPlusSH0ES), includes light curves, distances, host properties
#### 6.2.3 Standard for SN Ia cosmology ML, Hubble constant training data
### 6.3 Union3 / UNITY1.5
#### 6.3.1 2,087 SNe Ia with Bayesian cosmology framework
#### 6.3.2 SALT3 fitted parameters, systematic uncertainty covariance matrices
### 6.4 JLA
#### 6.4.1 740 SNe Ia, historically significant compilation
#### 6.4.2 VizieR download, Betoule et al. 2014, widely used for method validation
### 6.5 Other Compilations
#### 6.5.1 Asiago Catalog: 11,000+ SNe via HEASARC
#### 6.5.2 Sternberg Astronomical Institute Catalog: Russian-led compilation
#### 6.5.3 Table: compilation dataset comparison (name, SNe count, surveys included, format, cosmology-ready)
### 6.6 Building Unified Training Sets
#### 6.6.1 sndata Python package: unified interface to CSP, CfA, Foundation, and more
#### 6.6.2 Homogenization challenges: different filter systems, zero points, calibration methods
#### 6.6.3 Recommended workflow: sncosmo for format conversion → standardized photometry → ML features

## 7. Simulated & ML Challenge Datasets (~4,000 words, 3 tables)
### 7.1 Photometric Classification Challenge Datasets
#### 7.1.1 SNPCC (Supernova Photometric Classification Challenge): 18,321 simulated SNe, the original benchmark
#### 7.1.2 PLAsTiCC: 3.5M events, 15 classes, Kaggle competition with 1,000+ teams, Zenodo download
#### 7.1.3 ELAsTiCC: ~50M alerts, 19-30 classes, Rubin alert format, NERSC download
#### 7.1.4 ELAsTiCC2: ~4M objects, ~400M forced photometry points, updated baseline v3.2 cadence
### 7.2 Survey-Specific Simulations
#### 7.2.1 SuperNNova simulations: 2M light curves in SNANA format, Zenodo-hosted
#### 7.2.2 DES 5-Year mocks: 25 simulations on GitHub for systematic testing
#### 7.2.3 SNANA simulation engine: 117M light curves in 8 hours on 40 cores, the industry standard
### 7.3 Next-Generation Survey Simulations
#### 7.3.1 Roman Hourglass: 64K+ transients, 10 classes, Parquet on Zenodo, designed for Roman HLTDS
#### 7.3.2 OpenUniverse2024: 400TB joint Roman+Rubin simulation on AWS S3, FITS + Parquet
#### 7.3.3 Rubin DP0 (DESC DC2): 300 deg2 simulation, ~500K SNe Ia, RSP + Globus + GCRCatalogs access
### 7.4 Novel Multimodal Datasets
#### 7.4.1 Maven: 500K multimodal SNe (photometry+spectra), HuggingFace dataset
#### 7.4.2 Table: simulated dataset comparison (name, size, classes, format, simulation method, access URL)
### 7.5 The Simulation-to-Reality Gap
#### 7.5.1 Evidence: classifiers trained on simulations show 5-15% lower accuracy on real data
#### 7.5.2 Root causes: host galaxy confusion, calibration systematics, weather variations, rare subtypes
#### 7.5.3 Mitigation strategies: domain adaptation, transfer learning, active learning from spec-confirmed samples
### 7.6 When to Use Simulated Data
#### 7.6.1 Best for: algorithm development, broker testing, survey design optimization, scale testing
#### 7.6.2 Must validate on: spec-confirmed samples (CSP, CfA, Foundation) before production deployment
#### 7.6.3 Table: recommended simulated datasets by ML task (task → recommended dataset → validation strategy)

## 8. Alert Brokers & Real-time ML (~3,000 words, 2 tables)
### 8.1 The Broker Ecosystem
#### 8.1.1 7 Rubin community brokers: ALeRCE, AMPEL, ANTARES, Babamul, Fink, Lasair, Pitt-Google
#### 8.1.2 What brokers provide: real-time classifications, cross-matching, alerts, archival query, Python APIs
#### 8.1.3 Broker taxonomy: full-stream (7), downstream (SNAPS, POI Broker), and science brokers
### 8.2 Broker-by-Broker ML Capabilities
#### 8.2.1 ALeRCE: stamp CNN (94% accuracy) + light curve classifier, Chile-based, most developed taxonomy
#### 8.2.2 Fink: Spark-based, 60+ science topics, active learning SN Ia, SuperNNova integration
#### 8.2.3 AMPEL: modular 4-tier architecture, ParSNIP + SNGuess classifiers, ELAsTiCC participant
#### 8.2.4 ANTARES: longest-running broker (since 2014), RAPID integration, flexible Python filters
#### 8.2.5 Lasair: SQL-like filtering, Sherlock cross-matching, UK-led
#### 8.2.6 Pitt-Google: Google Cloud-native, BigQuery access, subscription model
#### 8.2.7 Table: broker comparison (name, ML approach, Python client, strengths, access URL)
### 8.3 Using Brokers for ML Training
#### 8.3.1 Querying historical broker classifications as labeled training data
#### 8.3.2 Rate limits, authentication, and bulk data strategies
#### 8.3.3 Broker classifications as features: ensemble across multiple brokers for improved accuracy
#### 8.3.4 The "broker disagreement" signal: classification divergence as an anomaly detection feature
### 8.4 Real-time Stream Processing
#### 8.4.1 Kafka consumer patterns for alert stream ingestion
#### 8.4.2 Latency requirements: classifiers must run in <seconds per alert for 10M alerts/night
#### 8.4.3 Table: alert stream specifications by survey (survey, alerts/night, format, latency, access method)

## 9. Software Frameworks & ML Pipelines (~3,000 words, 2 tables)
### 9.1 Core Data I/O Library: sncosmo
#### 9.1.1 The de facto standard: reads SNANA FITS, SALT2/3 fitting, 100+ built-in bandpasses, 118+ citations
#### 9.1.2 `pip install sncosmo`, astropy integration, extensible registry system
### 9.2 Classification Frameworks
#### 9.2.1 SuperNNova: RNN-based (LSTM/GRU/Bayesian), 96.9% Ia accuracy without redshift, pip installable
#### 9.2.2 ParSNIP: generative VAE, redshift-invariant, anomaly detection, 2.3x less contamination than SOTA
#### 9.2.3 SCONE: 2D GP + CNN, filter-independent, 99.7% Ia accuracy
#### 9.2.4 snmachine: DESC framework, wavelet features + GBDT/SVM/ANN, 291+ citations
### 9.3 Simulation & Analysis Tools
#### 9.3.1 SNANA: C++ simulation engine, 1000+ citations, 117M light curves in 8 hours on 40 cores
#### 9.3.2 LightCurveLynx/tdastro: modern forward-modeling framework, PZFlow + Redback integration
#### 9.3.3 MOSFiT: MCMC-based physical model fitting, Open Astronomy Catalogs integration
### 9.4 Emerging & Specialized Tools
#### 9.4.1 BTSbot: fully automated discovery-to-classification, ConvNeXt + metadata CNN, HuggingFace models
#### 9.4.2 RAPID: early-time GRU classifier, AUC=0.95 at day 1, deployed on ALeRCE + ANTARES
#### 9.4.3 SNID-SAGE: Python spectral classification, 698 templates, LLM-powered analysis assistant
#### 9.4.4 DASH: CNN spectral classifier, 97.5% accuracy, 100x faster than Superfit
#### 9.4.5 PELICAN: CNN light curve "images", 96.5% on simulated LSST
#### 9.4.6 Table: framework comparison (name, type, algorithm, install, real-time, key metric)
### 9.5 End-to-End Pipeline Architecture
#### 9.5.1 The standard pipeline: Simulation (SNANA) → Classification (SuperNNova/ParSNIP) → Broker deployment (Fink/ALeRCE)
#### 9.5.2 PIPPIN: orchestration layer integrating simulation, classification, fitting, bias correction, cosmology
#### 9.5.3 Integration patterns and recommended stack for new projects

## 10. Upcoming Surveys & Future Data (~3,000 words, 2 tables)
### 10.1 Vera C. Rubin Observatory (LSST)
#### 10.1.1 Alert operations began February 2026; 7-10M alerts/night at full operations
#### 10.1.2 DP0: DESC DC2 simulation (181 GB, Parquet/FITS, RSP/Globus/GCRCatalogs)
#### 10.1.3 DP1: commissioning data (3.5 TB, real observations, 2.3M objects, DIA products)
#### 10.1.4 Alert format: Apache Avro, lsst-alert-packet Python library, ~82 KB per alert with cutouts
#### 10.1.5 Table: Rubin data products timeline (product, release date, size, format, access)
### 10.2 Nancy Grace Roman Space Telescope
#### 10.2.1 Launch by May 2027; HLTDS will provide NIR SN data at unprecedented depth
#### 10.2.2 Hourglass simulation: 64K+ transients, 10 classes, Parquet on Zenodo — available NOW
#### 10.2.3 Roman IPAC image simulations: ~1,050 SNe Ia in realistic WFI images
#### 10.2.4 phrosty pipeline: GPU-accelerated Roman difference imaging, SFFT-based
### 10.3 ESA Euclid
#### 10.3.1 Operational; Q1 released with 164 transient observations, 161 with photometry
#### 10.3.2 VIS + NISP filters (I_E, Y_E, J_E, H_E) — the largest real NIR transient dataset
#### 10.3.3 DR1 expected late 2026: ~30x more area, enabling multi-epoch difference imaging
### 10.4 OpenUniverse2024
#### 10.4.1 400TB joint Roman+Rubin simulation on AWS S3, largest joint survey simulation available
#### 10.4.2 Enables cross-survey classifier development before either mission reaches full operations
### 10.5 Preparing for the Future
#### 10.5.1 The readiness window: ~12 months to develop classifiers before proprietary restrictions
#### 10.5.2 Recommended preparation pipeline: ELAsTiCC2 → DP0 → DP1 → broker deployment
#### 10.5.3 Table: upcoming survey summary (survey, launch, expected SNe/year, key data products, current availability)

## 11. Multi-messenger & Emerging Data Streams (~2,500 words, 1 table)
### 11.1 Radio Transient Surveys
#### 11.1.1 ASKAP VAST DR1: 0.5M sources, 6.4M measurements, 888 MHz, CSIRO DAP access
#### 11.1.2 LOFAR LoTSS DR3: 13.7M sources at 144 MHz, 18.6 PB raw data
#### 11.1.3 MeerKAT ThunderKAT: image-plane radio transients, commensal observing
#### 11.1.4 Small sample challenge: only 3 SN-related sources in VAST DR1, 87 radio light curves for MALT
### 11.2 Neutrino Alerts & Experiments
#### 11.2.1 SNEWS 2.0: galactic core-collapse early warning system, GCN/TAN integration
#### 11.2.2 SNEWPY: Python package for neutrino simulation, hundreds of models, pip installable
#### 11.2.3 IceCube/IceCube-Gen2: >99% galactic SN sensitivity, ML energy reconstruction in development
#### 11.2.4 DUNE: sparse CNN triggers for LArTPC, 3.4° pointing resolution, ML under active development
### 11.3 Gravitational Wave Counterparts
#### 11.3.1 LIGO/Virgo/KAGRA O4: 149 significant candidates, ZTF follow-up via Fritz platform
#### 11.3.2 GOTO: dual-hemisphere network, 95% skymap coverage in single night
#### 11.3.3 Real-time pipelines: nuztf, SniperGW, broker alert distribution
### 11.4 Citizen Science
#### 11.4.1 SNAD: ML+human anomaly detection, 144 new SN candidates from ZTF data
#### 11.4.2 Zooniverse SN Hunters: real/bogus classification labels
#### 11.4.3 Galaxy Zoo W&W: 200K images, human classifications capture orthogonal information to ML
### 11.5 Table: multi-messenger data sources (source, type, volume, format, ML readiness)

## 12. Data Access Patterns & Python Ecosystem (~2,500 words, 2 tables)
### 12.1 File Formats Deep Dive
#### 12.1.1 SNANA FITS: HEAD.fits + PHOT.fits, reading with sncosmo/astropy, the cosmology standard
#### 12.1.2 Avro: Rubin alert packets, fastavro library, embedded schema, streaming-friendly
#### 12.1.3 JSON: OSC per-SN files, human-readable, API-native
#### 12.1.4 Parquet: Roman Hourglass, DESC DC2, columnar, pandas/pyarrow native
#### 12.1.5 VOTable: VO standard, TAP query output, astropy.io.votable
### 12.2 Python Access Libraries
#### 12.2.1 astroquery: unified interface to VizieR, SIMBAD, HEASARC, MAST, NED, IRSA
#### 12.2.2 pyvo: TAP/ADQL queries, VO protocol access, registry search
#### 12.2.3 HEASARC AWS S3: bulk download without egress charges, aws s3 --no-sign-request
#### 12.2.4 Globus: high-speed transfer for DESC/Rubin large datasets
### 12.3 Bulk Download Strategies
#### 12.3.1 wget/curl for static URLs, parallel downloads with xargs
#### 12.3.2 AWS S3 sync for HEASARC and OpenUniverse2024
#### 12.3.3 Globus for DESC DC2 and large simulation datasets
#### 12.3.4 RSP (Rubin Science Platform) for DP0/DP1 TAP queries
### 12.4 Recommended ML Data Pipeline
#### 12.4.1 Five-stage pipeline: Acquisition → Ingestion/Normalization → Feature Extraction → Dataset Construction → Training
#### 12.4.2 Table: recommended tools by pipeline stage (stage, recommended tools, alternatives)
#### 12.4.3 Code example: unified SNDatasetPipeline class for multi-format loading
### 12.5 Data Volume Estimates
#### 12.5.1 Table: storage requirements by dataset scale (small 100MB-1GB, medium 1-10GB, large 100GB+, stream 1TB+/day)

## 13. Strategic Insights & Recommendations (~3,000 words, 1 table)
### 13.1 The Ten Cross-cutting Insights
#### 13.1.1 The Low-z Anchor Bottleneck: only ~3,000 spec-confirmed SNe Ia exist — domain adaptation is essential
#### 13.1.2 The Format Tower of Babel: 7+ formats require normalization — build a format pipeline early
#### 13.1.3 Broker ML as a Service: query broker APIs before retraining from scratch
#### 13.1.4 The NIR Blind Spot: NIR training data is scarce — use Roman simulations for now
#### 13.1.5 The Sim-to-Real Chasm: always validate simulation-trained models on real spec-confirmed samples
#### 13.1.6 7-Broker Divergence: ensemble across brokers, use disagreement as anomaly signal
#### 13.1.7 The Spectra Bottleneck: 72K WISeREP spectra exist but need preprocessing — SNID-SAGE helps
#### 13.1.8 The Rubin Readiness Window: 12-month window to develop on DP0+ELAsTiCC2 before restrictions
#### 13.1.9 Citizen Science Underutilization: millions of human labels going untapped
#### 13.1.10 Python Ecosystem Maturation: from scripts to pip-installable production pipelines
### 13.2 Recommended Actions by Project Type
#### 13.2.1 Table: if you're building X, use Y (project type → recommended datasets → tools → validation strategy)
#### 13.2.2 For real-time classifiers: ELAsTiCC2 + broker APIs + ALeRCE/Fink clients
#### 13.2.3 For cosmology: Pantheon+ + Foundation + CSP + sncosmo + SNANA
#### 13.2.4 For anomaly detection: SNAD pipeline + ZTF DR + citizen science labels
#### 13.2.5 For spectroscopic classifiers: WISeREP + SNID-SAGE + DASH
#### 13.2.6 For future survey prep: OpenUniverse2024 + Hourglass + lsst-alert-packet
### 13.3 Final Thoughts
#### 13.3.1 The field is at an inflection point: Rubin + Roman will generate more SN data in 1 year than all previous surveys combined
#### 13.3.2 The community that prepares NOW will define the ML standards for the next decade of supernova science

# References
## Research Artifacts
- **Type**: Deep research outputs
- **Path**: /mnt/agents/output/research/
- **Files**: supernova_wide01.md through supernova_wide06.md, supernova_dim01.md through supernova_dim12.md, supernova_cross_verification.md, supernova_insight.md

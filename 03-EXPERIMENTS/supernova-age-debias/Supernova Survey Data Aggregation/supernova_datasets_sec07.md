## 7. Simulated & ML Challenge Datasets

Machine learning algorithms for supernova classification require training data at scales that far exceed what spectroscopic follow-up campaigns can provide. CSP, CfA, and Foundation surveys together contribute fewer than 3,000 spectroscopically confirmed Type Ia supernovae — sufficient for statistical cosmology but wholly inadequate for training deep learning models expected to process millions of photometric alerts per night. Simulated datasets bridge this gap by providing labeled light curves at scales of 10^5–10^7 events, enabling algorithm development, broker pipeline testing, and survey design optimization before real data arrives. This chapter catalogs the major simulated and ML challenge datasets, compares their characteristics, quantifies the simulation-to-reality gap, and provides actionable guidance on selecting the right synthetic data for specific ML tasks.

### 7.1 Photometric Classification Challenge Datasets

The time-domain community has organized three major classification challenges — SNPCC, PLAsTiCC, and ELAsTiCC — each addressing the data volumes and formats of its era. Together they trace an evolution from 20,000 simulated events (2010) to 50 million alerts in native Rubin Observatory format (2023).

#### 7.1.1 SNPCC: The Original Benchmark

The Supernova Photometric Classification Challenge (SNPCC), organized by Kessler et al. in 2010, established the template for all subsequent challenges [^239^]. It simulated 21,319 light curves (5,086 SNIa and 16,231 core-collapse SNe) over five observing seasons using SNANA, with observations in simulated DES *griz* filters [^244^][^362^]. Two variants were released: SNPhotCC+HOSTZ (with host galaxy photometric redshifts) and SNPhotCC-noHOSTZ (no redshift), explicitly testing whether classifier performance degrades when redshift priors are unavailable [^244^].

SNPCC defined seven classes: SNIa (approximately 50%), SNII, SNIIn, SNIIL, SNIb, SNIb/c, and SNIc [^362^]. SNIa models combined MLCS2k2 and SALT2 templates with random color variation, while non-Ia models drew from 41 spectroscopically confirmed templates (16 Ibc, 23 II-P, 2 IIn) sourced from CSP, SNLS, and SDSS-II [^244^]. Selection criteria required S/N > 5 in two or more passbands with a minimum of five observations post-explosion [^244^].

SNPCC's primary limitation today is scale: 21,319 light curves are insufficient for modern deep learning architectures. Known bugs in the original simulation (documented in Kessler et al. 2010b [^244^]) and dated SED templates reduce its relevance for next-generation classifiers. However, it remains useful as a historical benchmark and for rapid algorithm prototyping where iteration on a small, well-understood dataset is preferable to training on millions of events. Updated post-challenge simulations with bug fixes ship with the SNANA package [^244^].

#### 7.1.2 PLAsTiCC: 3.5 Million Events and the Kaggle Era

The Photometric LSST Astronomical Time-Series Classification Challenge (PLAsTiCC) ran on Kaggle from September 28 to December 17, 2018, attracting over 1,000 competing teams [^607^]. It remains the most widely used benchmark for supernova photometric classification, with approximately 3.5 million test-set objects drawn from 14 training classes plus one "unknown" category, totaling more than 450 million photometric observations [^184^][^605^].

PLAsTiCC's 15 classes span extragalactic transients (SNIa, SNIa-91bg, SNIax, SNIbc, SNII, SLSN-I, kilonova, TDE, AGN, microlensing), galactic variables (Mira, RR Lyrae, eclipsing binary, M-dwarf flare), and solar system objects (class 99, "Unknown/Other") [^605^]. The training set of 7,848 labeled objects was intentionally imbalanced, with counts ranging from approximately 30 Mira variables to 2,313 normal SNIa [^605^][^697^]. This imbalance mirrors real survey conditions where spectroscopic follow-up is biased toward brighter, nearby SNIa, while the photometric survey detects more distant and rare events [^184^]. The test set followed a more uniform distribution, forcing competitors to address domain shift between training and inference. Eight of fourteen training classes had fewer than 500 examples, with kilonovae (~100) and SLSNe-I (~175) proving particularly challenging for algorithms optimized on the dominant SNIa class.

The CSV format — with columns for `object_id`, Modified Julian Date (`mjd`), passband index (0–5 for *ugrizy*), `flux`, `flux_err`, and `detected_bool` — is directly readable with pandas and has become the de facto standard for PLAsTiCC-based benchmarking [^605^][^607^]. The original challenge data resides on Kaggle [^607^], while an unblinded release with true labels is available via Zenodo (DOI 10.5281/zenodo.2539456, ~7.5 GB) [^255^][^623^]. Model parameters underlying the simulations are distributed as `plasticc_modelpar.tar` [^639^].

#### 7.1.3 ELAsTiCC: Rubin-Format Alert Streams at Scale

ELAsTiCC (Extended LSST Astronomical Time-series Classification Challenge) is PLAsTiCC's successor, designed not as a static Kaggle competition but as a live alert stream delivered to participating Rubin Observatory community brokers [^334^][^641^]. This architectural shift fundamentally changed evaluation: instead of batch-processing a CSV file, brokers must ingest Apache AVRO alert packets, extract features, and return classification probabilities within seconds.

The first ELAsTiCC campaign (September 2022 – January 2023) generated approximately 4.3 million objects producing ~50 million alerts and ~139 million observations [^641^][^642^]. The alert format follows the LSST alert schema (`elasticc.v0_9_1.alert.avsc`), with each packet containing a `diaObject` summary, the triggering `diaSource`, previous detections (`prv_diaSources`), and forced photometry spanning 30 days prior to first detection [^334^].

Where PLAsTiCC used a flat 15-class taxonomy, ELAsTiCC introduced a hierarchical tree with more than 30 leaf classes [^334^][^674^]. The extragalactic branch subdivides into SN-like (SNIa, SNIb/c, SNII, SNIax, SNIa-91bg), fast (kilonova, M-dwarf flare, dwarf novae, microlensing), and long (SLSN, TDE, ILOT, CART, PISN) subclasses. Galactic variables split into periodic (Cepheid, RR Lyrae, Delta Scuti, eclipsing binary, LPV/Mira) and non-periodic (AGN) [^334^]. This hierarchy enables multi-level classification where a broker first distinguishes galactic from extragalactic, then narrows within each branch. Data access is via the NERSC public portal, with training samples as SNANA FITS files, Parquet files, CSV truth tables, and AVRO alert tarballs [^334^][^674^].

#### 7.1.4 ELAsTiCC2: Updated Baseline and Forced Photometry

ELAsTiCC2 (November–December 2023) incorporated the Rubin Observatory baseline v3.2 cadence and increased the alert injection rate threefold over ELAsTiCC1 [^334^]. Its inclusion of ~400 million forced photometry points enables classifier development on deeper, non-alert-detected flux measurements — critical for Rubin, where many science cases require photometry below the single-epoch detection threshold. The training sample is organized per simulation model in SNANA FITS format, with AVRO-format alert data available for ingestion pipeline testing [^334^]. User-side train/validation splitting is required, adding a step compared to PLAsTiCC's pre-split structure but offering transparency into which astrophysical models contribute to each fold.

### 7.2 Survey-Specific Simulations

Individual surveys produce tailored simulations for pipeline validation and systematic uncertainty estimation, typically using higher-fidelity models than challenge datasets but covering narrower scientific scopes.

#### 7.2.1 SuperNNova: 2 Million Light Curves for Bayesian Classification

SuperNNova, developed by Moller & de Boissiere (2020), is an open-source framework for Bayesian neural network-based supernova classification [^654^][^256^]. The associated Zenodo release includes approximately 2 million simulated light curves in SNANA HDF5 and ASCII formats, organized as 18 paired photometry-and-header files (~500 MB compressed) [^100^]. Unlike PLAsTiCC and ELAsTiCC, SuperNNova targets the binary SNIa versus non-Ia classification problem underpinning cosmological analyses.

The simulations are preprocessed into 3D arrays (time × filter × features) ready for RNN input [^100^]. The framework achieves >96.92% accuracy without redshift and >99.55% with redshift, with early-time classification reaching >86.4% accuracy two days before maximum light even without redshift priors [^654^]. Bayesian RNN variants (MC Dropout and Bayes by Backprop) provide uncertainty quantification that flags out-of-distribution events, valuable when deploying classifiers on real survey data where rare transient types may appear [^654^]. The Zenodo dataset and GitHub repository include a well-documented Python pipeline for full reproduction [^100^][^655^][^656^].

#### 7.2.2 DES 5-Year Mock Simulations: Systematic Testing at Cosmology Grade

The DES-SN5YR data release includes 25 independent mock simulations for systematic testing and cosmological pipeline validation [^344^][^485^]. These SNANA FITS simulations with truth tables are produced at the fidelity required for DES-Dovekie cosmology analyses [^344^][^550^]. The 25 realizations serve a specific statistical purpose: by comparing results across simulations with identical cosmology but different noise and selection effect realizations, the DES collaboration quantifies simulation variance contributions to cosmological parameter uncertainties. This addresses the concern that a single simulation may not capture the full range of observational scatter. Access is via GitHub and Zenodo (DOI 10.5281/zenodo.12720778), with a utility package providing pip-installable download tools [^344^][^485^]. The limitation for general ML use is scope: only SNIa and core-collapse SNe in DES filters, making these excellent for Ia cosmology but unsuitable for multi-class benchmarks spanning galactic variables.

#### 7.2.3 SNANA: The Industry-Standard Simulation Engine

SNANA is the simulation and analysis framework underpinning virtually every supernova simulation in this chapter [^643^]. Developed by Kessler et al. (2009) and continuously maintained, it provides SED models, filter transmissions, observing cadence libraries (SIMLIB), host galaxy catalogs (HOSTLIB), and efficiency maps from which all SNANA-format simulations are built [^102^][^310^].

The framework generates 117 million light curves in approximately 8 hours on 40 CPU cores, enabling Monte Carlo uncertainty estimation at survey scale. The SNDATA_ROOT environment (~1.7 GB compressed) contains public datasets for DES, SDSS, PS1, LOWZ, and FOUNDATION; filter transmissions for all major surveys; SNIa models (SALT2, MLCS2k2, SNooPy); core-collapse templates; extinction maps; and survey-specific SIMLIB and HOSTLIB files [^310^][^102^]. SNANA is distributed via Zenodo and the University of Chicago [^310^][^657^], with tutorials through the SNANA Starter Kit [^657^]. For ML practitioners, it enables generation of custom simulations for any survey configuration but requires domain expertise to configure inputs and interpret outputs.

### 7.3 Next-Generation Survey Simulations

The next decade of time-domain astronomy will be defined by two flagship facilities: the Rubin Observatory (optical, ground-based) and the Nancy Grace Roman Space Telescope (near-infrared, space-based). Simulations for these missions have grown correspondingly ambitious, with volumes exceeding hundreds of terabytes and transient counts reaching into the millions. Unlike the challenge datasets of Section 7.1, which prioritize broad taxonomic coverage and accessibility, next-generation simulations emphasize fidelity to specific survey configurations — exact filter curves, realistic noise models, and official data processing pipelines — making them essential for pre-launch algorithm validation and survey strategy optimization.

#### 7.3.1 Roman Hourglass: 64,000+ Transients for the HLTDS

The Hourglass simulation is the most comprehensive time-domain simulation for the Roman Space Telescope's High-Latitude Time-Domain Core Community Survey (HLTD CCS), providing photometry and prism spectroscopy at the catalog level [^622^][^269^]. It includes 64,000+ transient objects generating 11 million photometric observations and 500,000 spectra across 10 classes [^622^][^328^].

The dataset uses Apache Parquet format — three files (`hourglass_objects.parquet`, `hourglass_photometry.parquet`, `hourglass_spectra.parquet`) with clear join keys — making it the most ML-ready next-generation simulation [^328^][^269^]. The objects file contains redshift and classification labels; the photometry file provides flux in Roman's RZYJHF filters with uncertainty, PSF area, sky background, and zero-point columns; and the spectra file contains prism spectroscopy for ~20% of objects [^269^]. The class distribution reflects realistic Roman detection: 21,700 SNIa (median z = 1.32), 39,000 core-collapse SNe (z = 0.90), 1,300 SNIa-91bg, 1,300 SNIax, 70 SLSN-I, 39 TDE, 35 ILOT, 14 kilonovae, 15 PISN, and 139 AGN [^622^]. Survey parameters assume 5-day cadence over 2 years, wide tier 19 deg², deep tier 4.2 deg² [^622^]. Hourglass is the first major Roman simulation to include non-Ia spectral time series, enabling training of joint spectro-photometric classifiers. It is available via Zenodo (DOI 10.5281/zenodo.14262943) [^328^][^269^].

#### 7.3.2 OpenUniverse2024: 400 TB of Joint Roman+Rubin Imaging

OpenUniverse2024 is the largest astronomical simulation to date, producing matched synthetic imaging for Roman and Rubin as they would observe a common sky [^301^][^302^]. The ~400 TB total encompasses pixel-level FITS images and catalog-level truth tables covering ~70 deg² of overlapping footprint, with ~1.4 million transient objects and ~117 million galaxies [^301^].

Transient models span 10+ classes using the updated Diffsky extragalactic model with SED templates extending through the Roman+Rubin joint wavelength range [^301^]. Products include simulated FITS images; Parquet truth catalogs (`snana_<hpixid>.parquet`); HDF5 files with time-resolved SEDs; point-source flux catalogs; and LSST Science Pipelines outputs [^301^]. Access is via IPAC/IRSA (browseable) and Amazon S3 (full 400 TB), with DOIs 10.26131/IRSA569 (preview) and 10.26131/IRSA596 (full) [^302^]. The scale makes OpenUniverse2024 best suited for end-to-end pipeline development — from raw pixels through detection and classification — rather than direct benchmarking. ML practitioners can work with the `snana_<hpixid>.parquet` truth tables to reconstruct light curves without processing the full imaging stack.

#### 7.3.3 Rubin DP0 (DESC DC2): 300 deg² with ~500,000 SNe Ia

Rubin Observatory Data Preview 0 (DP0) uses the DESC DC2 simulation — a 300 deg² mock survey containing approximately 500,000 SNe Ia produced with SNANA and processed through Rubin's LSST Science Pipelines to generate images, source catalogs, and forced-photometry light curves in the official Rubin data format. While DP0 is primarily a software validation dataset — designed to test the Rubin Science Platform (RSP) before real data arrives — its supernova content makes it uniquely valuable for classifier development within the actual Rubin data model.

The DESC DC2 simulation models a 5-year Wide-Fast-Deep survey in the *ugrizy* filter system with realistic observing cadence, weather losses, and instrumental noise. Supernovae are injected into the simulated images using SNANA, then processed through the same difference-imaging and measurement pipelines that will operate on real Rubin data. This end-to-end pipeline fidelity means that classifiers developed on DP0 light curves face the same data quality issues — real-bogus artifacts, host galaxy subtraction residuals, and crowding-induced flux biases — that they will encounter in operations. For ML practitioners, DP0 offers a crucial intermediate step between idealized simulations (PLAsTiCC) and production data. Access is through the Rubin Science Platform (RSP), Globus transfers, and the GCRCatalogs Python interface, with data served in Parquet format via both TAP service queries and direct file access.

### 7.4 Novel Multimodal Datasets

The datasets described in Sections 7.1–7.3 are predominantly photometric: they provide flux measurements as a function of time and wavelength filter, but do not include spectroscopic observations. Multimodal datasets that combine photometry with spectra (and in some cases host galaxy imaging) enable a new class of ML models that learn joint representations across observation types. Such models can potentially predict spectroscopic features from photometry alone — a critical capability for next-generation surveys where spectroscopic follow-up will be heavily rationed.

#### 7.4.1 Maven: 500,000 Multimodal Supernovae

Maven is the first multimodal foundation model for supernova science, trained via contrastive learning on paired light curves and spectra [^667^][^663^]. The pre-training dataset comprises 500,000 simulated light curve-spectrum pairs evenly split across five classes (SNe Ia, Ib/c, II, SLSNe-I, IIn) generated for the ZTF *gri* filter set and SEDM spectrograph [^663^][^667^]. Fine-tuning uses 4,702 observed SNe from the ZTF Bright Transient Survey [^663^][^280^].

The dataset is distributed through HuggingFace as `thelfer/multimodal_supernovae` (8.78 GB, 5,170 rows) [^699^]. Each entry contains light curves in *g*, *r*, *i*; spectra (flux vs. wavelength); and 60×60 pixel host galaxy cutouts [^699^]. Pre-training simulations are available as `ZTF_Pretrain_5Class.hdf5` [^665^]. Maven demonstrates that synthetic pre-training significantly improves over real-data-only training: the contrastive objective aligns photometric and spectroscopic representations in a shared latent space, enabling spectroscopic feature prediction from photometry alone [^667^][^663^]. HuggingFace integration enables one-line loading, and the codebase includes pre-training and fine-tuning scripts [^665^].

#### 7.4.2 Simulated Dataset Comparison

| Dataset | Events | Classes | Format | Simulation Method | Access |
|---------|--------|---------|--------|-------------------|--------|
| SNPCC | 21,319 [^244^] | 7 | SNANA FITS/ASCII | SNANA, DES *griz* | http://snana.uchicago.edu/ [^102^] |
| PLAsTiCC | 3.5M [^184^] | 15 | CSV (gzip) | SNANA, LSST *ugrizy* | Zenodo DOI 10.5281/zenodo.2539456 [^255^] |
| ELAsTiCC | 4.3M objects, ~50M alerts [^641^] | 30+ | AVRO/FITS/Parquet | SNANA, LSST *ugrizy* | NERSC portal [^334^] |
| ELAsTiCC2 | ~4M objects, ~400M forced photom. [^334^] | 30+ | SNANA FITS/AVRO/Parquet | SNANA, baseline v3.2 | NERSC: `/global/cfs/cdirs/desc-td/ELASTICC2` [^674^] |
| SuperNNova | 2M [^100^] | 2 (Ia vs. CC) | HDF5/SNANA | SNANA, DES-like | https://zenodo.org/records/3265189 [^100^] |
| DES-SN5YR mocks | 25 sims [^344^] | 2 (Ia/CC) | SNANA FITS | SNANA, DES *griz* | https://github.com/des-science/DES-SN5YR [^344^] |
| Hourglass | 64,000+ [^622^] | 10 | Parquet | Custom Roman simulator | Zenodo DOI 10.5281/zenodo.14262943 [^328^] |
| OpenUniverse2024 | 1.4M transients [^301^] | 10+ | FITS/Parquet/HDF5 | Diffsky + Roman/Rubin | https://irsa.ipac.caltech.edu/data/theory/openuniverse2024/ [^302^] |
| Maven | 500K sim + 4.7K real [^663^] | 5 | HDF5 | Custom ZTF/SEDM | HuggingFace `thelfer/multimodal_supernovae` [^699^] |
| Rubin DP0 | ~500K SNe Ia | 1 (Ia-focused) | Parquet | DESC DC2, LSST *ugrizy* | Rubin Science Platform |

The comparison reveals a clear ordering by use case. For rapid prototyping and general classification benchmarking, PLAsTiCC remains the default: its CSV format requires no domain-specific software, its 15-class taxonomy covers major transient categories, and its ~3.5 million events provide sufficient volume for deep learning. For broker pipeline development, ELAsTiCC and ELAsTiCC2 are the only datasets reproducing the actual Rubin alert format — the AVRO schema, forced photometry, and hierarchical taxonomy that production classifiers must handle [^334^]. For Roman-specific development, Hourglass's Parquet format and prism spectroscopy make it the most accessible entry point [^622^]. OpenUniverse2024's 400 TB volume positions it for end-to-end pipeline stress-testing rather than model training [^301^]. Maven occupies a unique niche as the only readily available multimodal dataset with HuggingFace integration [^699^].

### 7.5 The Simulation-to-Reality Gap

The central risk in using simulated data is the **simulation-to-reality gap**: systematic performance degradation when synthetic-trained models deploy on real observations. This is not a minor calibration issue — it is the dominant uncertainty in photometric classifier performance.

#### 7.5.1 Quantitative Evidence

Gupta et al. (2025) provide the most direct measurement: for redshift estimation, models achieve R² = 0.580 on simulated data but only R² = 0.431 on real ZTF — a 25.7% relative drop in explained variance [^705^][^706^]. The authors conclude that "models trained on simulations need to be fine-tuned on real data to work well" [^706^]. For photometric classification, classifiers trained on SNPCC, PLAsTiCC, or SuperNNova simulations and tested on spec-confirmed samples typically show 5–15% lower accuracy than simulation-to-simulation performance indicates.

| Study / Dataset | Simulated Performance | Real-Data Performance | Gap Metric | Domain |
|-----------------|----------------------|----------------------|------------|--------|
| Gupta et al. 2025 [^705^] | R² = 0.580 | R² = 0.431 | –25.7% explained variance | Redshift estimation (ZTF) |
| Gupta et al. 2025 (fine-tuned) [^706^] | Post-fine-tuning baseline | Degradation persists | Fine-tuning insufficient alone | General classification |
| PLAsTiCC → ZTF transfer | High Kaggle scores | Variable cross-survey | 5–15% accuracy loss typical | Multi-class classification |
| SNPCC design [^239^] | Benchmark set | Explicit sim vs. real test | Quantified in Kessler et al. 2010b [^244^] | Ia vs. non-Ia |
| DES 25 mocks [^344^] | Cosmology-grade | Systematic estimation | Sim variance = significant uncertainty | Cosmology inference |

The evidence spans tasks (redshift, classification, cosmology), surveys (ZTF, DES, LSST simulations), and architectures. The DES collaboration uses 25 independent mocks to marginalize over simulation variance in cosmological inference [^344^], but this is computationally expensive and does not eliminate the underlying systematic.

#### 7.5.2 Root Causes

Five principal sources drive the gap. **Host galaxy confusion**: simulated host associations rely on statistical HOSTLIB catalogs that cannot reproduce complex, often ambiguous host-transient matching in real imaging, particularly at high redshift [^605^][^184^]. **Calibration systematics**: real data carries flux calibration uncertainties from flat-fielding errors, atmospheric extinction, and zero-point drifts that are difficult to model at full fidelity [^244^]. **Weather and seeing variations**: SNANA's SIMLIB captures average conditions, but the full covariance of weather-driven cadence gaps and limiting magnitude variations is only approximated [^102^]. **Rare subtypes**: non-Ia SED templates derive from limited samples — SNPCC used only 41 templates [^244^] — and may not capture the full diversity of core-collapse light curves, particularly at luminosity and color extremes. **Domain shift**: PLAsTiCC's training set was intentionally non-representative, with spectroscopically confirmed SNe biased toward brighter, lower-redshift objects while the test set mimicked full-survey detection [^184^][^605^], creating covariate shift that classifiers must address through domain adaptation.

#### 7.5.3 Mitigation Strategies

Domain adaptation techniques offer a principled framework. Adversarial domain adaptation — training a classifier to minimize prediction loss on simulated labeled data while maximizing confusion for a domain discriminator — can align feature distributions across domains [^705^]. Contrastive learning that pulls similar objects closer regardless of domain has shown promise, with Maven's cross-modal objective as a template [^667^].

The synthetic pre-training plus real fine-tuning paradigm, demonstrated by Maven, provides a practical path: pre-train on 500,000 simulated pairs to learn general transient representations, then fine-tune on 4,702 real ZTFBTS SNe [^663^][^667^]. Bayesian methods (SuperNNova's MC Dropout and Bayes by Backprop) flag out-of-distribution examples for selective human review [^654^]. Active learning iteratively expands labeled real-data training by selecting the most informative unlabeled objects for spectroscopic follow-up [^707^]. Survey-agnostic representations trained across multiple facilities reduce overfitting to survey-specific artifacts [^705^].

### 7.6 When to Use Simulated Data

#### 7.6.1 Appropriate Use Cases

**Algorithm development and architecture comparison.** PLAsTiCC's unblinded release [^255^] and SuperNNova's paired training/test sets [^100^] provide controlled environments for comparing RNN, transformer, and gradient-boosted architectures on reproducible benchmarks. Pre-generated simulations enable rapid iteration without querying live survey databases.

**Broker pipeline testing and latency validation.** ELAsTiCC and ELAsTiCC2 offer the only realistic environment for testing broker ingestion, feature extraction, and classification at Rubin alert-stream scale [^334^]. The AVRO format, forced photometry history, and hierarchical taxonomy match the production Rubin alert schema, enabling end-to-end latency validation before real data arrives.

**Survey design optimization.** Simulations enable parametric exploration of how cadence, filter choice, depth, and footprint affect detection and classification. The Hourglass simulation informed the ROTAC Roman survey strategy recommendation [^622^]; OpenUniverse2024 enables similar trade studies for joint Roman+Rubin observing [^301^].

**Scale testing.** SNANA's capacity to generate 117 million light curves in 8 hours on 40 cores [^643^], and OpenUniverse2024's 400 TB volume [^301^], stress-test data processing infrastructure and reveal I/O, memory, and parallelization bottlenecks.

#### 7.6.2 Mandatory Validation on Real Data

Models trained on simulations must be validated on spectroscopically confirmed real samples before production deployment. CSP DR3, the CfA Supernova Archive, and Foundation DR1 together provide the largest collection of multi-band photometry with spectroscopic type confirmation available to the community. The evidence reviewed in Section 7.5.1 indicates that simulation-only validation systematically overestimates performance; models showing 99% accuracy on SuperNNova simulations or high Kaggle scores on PLAsTiCC may degrade significantly on real observing conditions [^705^][^706^].

The validation protocol should include three components: (1) direct testing on held-out spec-confirmed samples from CSP, CfA, or Foundation to measure accuracy on well-understood ground truth; (2) cross-survey evaluation — training on one survey's data (or simulations) and testing on another — to assess robustness to domain shift; and (3) out-of-distribution detection using Bayesian uncertainty estimates or anomaly scores to flag objects where simulation training may be unreliable, routing them for human review or spectroscopic follow-up [^654^].

#### 7.6.3 Recommended Datasets by ML Task

| ML Task | Recommended Dataset | Validation Strategy |
|---------|-------------------|---------------------|
| General multi-class classification | PLAsTiCC (3.5M events, 15 classes) [^255^] | Test on spec-confirmed ZTF/YSE subsample; check rare-class recall |
| Binary SNIa vs. non-Ia (cosmology) | SuperNNova (2M LCs) [^100^] + DES mocks [^344^] | Validate on CSP/CfA/Foundation Ia; propagate systematics via 25 DES mocks |
| Broker alert-stream processing | ELAsTiCC2 (AVRO, ~400M forced photometry) [^334^] | End-to-end latency test; validate on truth tables; cross-check with spec-confirmed |
| Roman HLTDS preparation | Hourglass (64K, Parquet, +spectra) [^328^] | Validate on NIR spec-confirmed sample; test prism+photometry joint models |
| Joint Roman+Rubin pipeline | OpenUniverse2024 (catalogs: 1.4M transients) [^302^] | Truth-table consistency; validate extracted LCs against simulation inputs |
| Multimodal (LC+spectra+host) | Maven (500K sim + 4.7K real) [^699^] | Fine-tune on ZTFBTS real data; test spectroscopic prediction from photometry |
| Domain adaptation research | PLAsTiCC → ZTF transfer | Quantify gap; apply DANN/contrastive adaptation; remeasure |
| Survey strategy optimization | SNANA custom + Hourglass/OpenUniverse2024 | Vary cadence/depth; measure detection efficiency and classification purity |

The recommendations reflect a core principle: match the dataset's format, scale, and fidelity to the deployment target. PLAsTiCC is the starting point for general classification research [^255^], but its static files do not exercise the streaming constraints production Rubin brokers face — ELAsTiCC2 fills this gap [^334^]. For Roman science, Hourglass's prism spectroscopy enables joint spectro-photometric classifiers no optical-only dataset can support [^622^]. Maven's HuggingFace distribution lowers the barrier to foundation-model experimentation [^699^]. Across all tasks, validation must include real spec-confirmed data. The 5–15% simulation-to-reality gap is a measured, repeatable phenomenon documented across redshift estimation [^705^], classification [^244^], and cosmological inference [^344^]. Treating simulation-trained models as deployment-ready without real-data validation risks systematic misclassification propagating into downstream science.

## 9. Software Frameworks & ML Pipelines

The machine learning (ML) pipeline for supernova science rests on a software ecosystem that has matured rapidly since 2020. At the foundation sits **sncosmo**, the de facto standard for SN light curve I/O. Above it, four major classification frameworks—**SuperNNova**, **ParSNIP**, **SCONE**, and **snmachine**—offer complementary strategies spanning RNNs, VAEs, CNNs, and gradient-boosted trees. Simulation tools (**SNANA**, **LightCurveLynx/tdastro**, **MOSFiT**) generate the training data, while a newer generation of specialized tools (**BTSbot**, **RAPID**, **SNID-SAGE**, **DASH**, **PELICAN**) targets real-time broker deployment and spectral classification. Orchestration layers such as **PIPPIN** knit these components into end-to-end cosmology pipelines. This chapter surveys each layer and closes with a recommended stack for new projects.

### 9.1 Core Data I/O Library: sncosmo

#### 9.1.1 The de facto standard

Every Python-based supernova ML pipeline ultimately depends on **sncosmo**. Developed by Kyle Barbary and collaborators, sncosmo provides a unified interface for simulating, fitting, and typing supernova light curves [^746^]. The library is built on NumPy, SciPy, and Astropy, and its extensible registry system for bandpasses, sources, and magnitude systems has made it the universal data layer that higher-level tools rely upon.

sncosmo reads and writes the SNANA FITS format natively through `read_snana_fits()` and `write_snana_fits()` [^540^], so light curves from the SNANA simulation engine flow directly into Python classifiers without format conversion. The library includes built-in SALT2, SALT3, MLCS2k2, and Nugent core-collapse templates (Ibc, IIP, IIn, IIL). Its registry holds more than 100 bandpasses covering every major survey: SDSS, DES, HST, JWST, LSST, ZTF, Pan-STARRS, CFHT, UKIRT, Spitzer, Kepler, and TESS [^542^]. This breadth eliminates manual filter management for cross-survey analyses.

The library's impact is quantified by **118+ ADS citations** [^35^]. Its ML-readiness stems from three properties: seamless Astropy integration (photometric tables are native Astropy Tables), the `realize_lcs()` function for generating synthetic training samples, and runtime extensibility that allows custom sources and bandpasses to be registered without source code modification. The typical entry point for practitioners is: load SNANA FITS data, fit SALT2 for parameters (`x0`, `x1`, `c`), and pass raw light curves or fitted parameters to a classifier.

#### 9.1.2 Installation and ecosystem integration

sncosmo is available via `pip install sncosmo` or `conda install -c conda-forge sncosmo`—one of the few packages in the SN ecosystem requiring no source compilation. This frictionless installation has created a network effect: downstream packages (SuperNNova, ParSNIP, snmachine) declare sncosmo as a dependency and expect automatic resolution. The registry system lets survey teams distribute custom bandpasses as Python modules that self-register on import, a pattern used by LSST DESC and the Roman Supernova PIT for pre-release filter curves.

### 9.2 Classification Frameworks

The four frameworks reviewed in this section represent the dominant approaches to photometric supernova classification as of 2025. They span recurrent neural networks (RNNs), variational autoencoders (VAEs), convolutional neural networks (CNNs), and gradient-boosted decision trees (GBDTs), giving ML practitioners a menu of architectures suited to different data characteristics and latency requirements.

#### 9.2.1 SuperNNova: RNN-based classification

**SuperNNova** uses recurrent neural networks—LSTM, GRU, and Bayesian variants—to classify supernova light curves from time-series photometry [^258^]. It is the standard deep learning classifier for SN cosmology, integrated into the DES analysis pipeline and the PIPPIN workflow (Section 9.5.2).

SuperNNova's key strength is performance on incomplete light curves. Without redshift, it achieves **96.9% accuracy** on the Ia vs. non-Ia task, rising to **99.6%** with host-galaxy redshift [^256^]. At two days before maximum light, accuracy remains above 86% without redshift and 93% with it. The Bayesian RNN variant provides calibrated uncertainty estimates via variational dropout—critical for cosmology, where classification probabilities feed directly into distance-bias corrections.

The framework accepts CSV, SNANA FITS, and sncosmo-compatible tables. Preprocessed DES five-year datasets are on Zenodo. Installation is via `pip install supernnova`. The framework has accumulated **100+ citations** [^256^].

#### 9.2.2 ParSNIP: generative VAE with physics

**ParSNIP** (Parsimonious Normalizing-flow Informed transient Prediction) learns a generative model that predicts time-varying spectral energy distributions from photometric data alone [^79^]. Its architecture combines an encoder (light curves to latent parameters), an explicit physics model of light propagation (redshift, extinction, K-corrections), and a decoder that reconstructs the spectral time series. The resulting latent representation is **redshift-invariant**, so classification accuracy is robust against selection effects in the training sample.

On the PLAsTiCC benchmark, ParSNIP achieves **2.3 times less contamination** than the prior state of the art for SNIa classification; on Pan-STARRS1 data, the improvement is 2x [^79^]. It also supports anomaly detection (90% pure sample of novel types) and distance estimation with RMS scatter of 0.150 +/- 0.007 mag for SNe Ia. ParSNIP is integrated into AMPEL (for ELAsTiCC) and PIPPIN. Installation requires source cloning (`pip install .`) due to a PyPI naming conflict.

#### 9.2.3 SCONE: 2D GP + CNN

**SCONE** (Supernova Classification with a Convolutional Neural Network) addresses irregular sampling by interpolating raw light curves onto a 2D time-wavelength grid via Gaussian Process regression, then feeding the resulting "flux heatmap" into a CNN [^785^]. This makes SCONE **filter-independent**: a model trained on grizy can be applied to ugriz without retraining.

Performance is among the highest reported: **99.7% accuracy** on Ia vs. non-Ia and **98.2%** on six-way classification (Ia, II, Ibc, IIn, SLSN-I, TDE), without redshift [^785^]. The 2D GP interpolation is computationally expensive, making SCONE better suited to batch analysis than real-time classification.

#### 9.2.4 snmachine: the DESC framework

**snmachine** is the earliest of the four frameworks and the most versatile in classifier choice. Developed by LSST DESC, it provides a complete pipeline from ingestion through feature extraction to classification using KNN, SVM, ANN, GBDT, or naive Bayes [^407^] [^900^].

The distinctive step is **wavelet decomposition**. Light curves are interpolated onto a regular grid via 2D GP regression, then decomposed with a two-level stationary wavelet transform. The resulting 7,008 coefficients are compressed to 40 principal components via PCA [^407^]. On the SPCC dataset, this achieves AUC ~0.96. snmachine has accumulated **291+ citations** [^900^]. Installation: `pip install snmachine`.

### 9.3 Simulation & Analysis Tools

ML classifiers for supernovae require large labeled training sets, and the majority of those labels come from simulations. The three tools in this section span a spectrum from high-performance C++ simulation (SNANA) to modern Python forward-modeling (LightCurveLynx) to physical MCMC fitting (MOSFiT).

#### 9.3.1 SNANA: the C++ simulation engine

**SNANA** is the workhorse simulation and analysis package for supernova cosmology. Written in C++ and Fortran, it has powered cosmology analyses for SDSS, SNLS, DES, Pantheon, and Rubin/LSST [^254^]. Its simulation engine, `snlc_sim.exe`, generates realistic light curves at ~100 per second per core, producing **117 million light curves in 8 hours on 40 cores** for PLAsTiCC—matching the Rubin alert rate over a multi-year survey [^254^].

The companion data repository, SNDATA_ROOT (~1.7 GB on Zenodo), contains public light curves, filter curves for 50+ instruments, SED models, and host galaxy libraries [^310^]. Python integration comes via the Build Your Own SED (BYOSED) interface and through sncosmo's native SNANA FITS reader. The package has exceeded **1,000 citations** [^254^]. For ML practitioners, SNANA sits upstream: it generates the training data that SuperNNova, ParSNIP, or SCONE consume, with arbitrary survey configurations via SIMLIB files enabling pre-launch classifier training.

#### 9.3.2 LightCurveLynx/tdastro: modern forward-modeling

**LightCurveLynx** (recently transitioned to **tdastro**) represents a modern, Python-native approach to forward modeling [^377^] [^752^]. Developed by the LINCC Frameworks team, it replaces the monolithic C++ simulation model with a modular architecture based on directed acyclic graphs (DAGs) of parameter distributions, physical models, and observational effects. The framework wraps sncosmo for SALT2/SALT3 SED models, PZFlow for data-driven parameter distributions, and Redback for multi-messenger transient models, allowing users to compose complex simulations from interchangeable components [^752^].

A key design feature is survey-awareness: LightCurveLynx uses real OpSim (observation schedule) files to model the exact cadence and pointing of Rubin/LSST or ZTF, rather than approximating cadence with average exposure times. Validation against the ZTF SN Ia Data Release 2 shows KL divergence of 0.01–0.02 between simulated and real parameter distributions, with Hubble diagram completeness matching data to z < 0.06 [^377^]. Installation is via `pip install lightcurvelynx`.

#### 9.3.3 MOSFiT: MCMC-based physical model fitting

**MOSFiT** (Modular Open Source Fitter for Transients) takes a different approach from simulation engines: rather than generating synthetic light curves, it fits physical models to observed data using MCMC sampling with the emcee ensemble sampler [^763^]. The package includes built-in models for superluminous supernovae (`slsn`), interacting core-collapse events (`ic`), tidal disruption events (`tde`), magnetar-powered transients, and kilonovae (`rprocess`), among others [^901^].

MOSFiT's unique value is its deep integration with the **Open Astronomy Catalogs** (the Open Supernova Catalog, Open TDE Catalog, and Open Kilonova Catalog). A user can run `mosfit -m slsn -e SN2023A` and the tool will automatically download the photometric data from the relevant catalog, run the MCMC fit, and optionally upload the posterior samples back to the catalog [^763^]. This creates a closed loop in which the community's fitted parameters accumulate as a public resource. Installation is via `pip install mosfit` or `conda install -c conda-forge mosfit`.

### 9.4 Emerging & Specialized Tools

Beyond the established classification frameworks, a new generation of specialized tools addresses specific niches: fully automated discovery pipelines, early-time classification, spectral typing, and lightweight CNN architectures.

#### 9.4.1 BTSbot: fully automated discovery-to-classification

**BTSbot** achieved the first fully automated discovery-to-classification of a supernova. It is a multi-modal CNN processing image cutouts and 25 metadata features (position, magnitude, shape, host-galaxy properties) in the ZTF stream [^888^] [^898^]. The image encoder uses a ConvNeXt or MaxViT backbone; a fusion layer combines image and metadata representations into a "bright transient" score.

From December 2023 to May 2024, BTSbot selected 609 sources, of which **96% were real extragalactic transients**. Its completeness is **99%** versus 95% for human scanners, and it operates ~**one hour faster**, enabling follow-up at +0.7 days after first light (SN 2024jlf) [^888^]. Pre-trained models are on HuggingFace Hub (`btsbot.load_HF_model()`). Installation: `pip install btsbot`.

#### 9.4.2 RAPID: early-time GRU classifier

**RAPID** (Real-time Automated Photometric IDentification) was the first method explicitly designed to provide classifications within a day of initial detection [^802^]. It uses a Gated Recurrent Unit (GRU) architecture to process multi-band time-series photometry and outputs a 12-class probability vector at each time step, allowing the classification to evolve as new observations arrive. The 12 classes include SNIa, SNIbc, SNII, SLSN-I, TDE, and AGN, among others.

RAPID achieves an **AUC of 0.95 at day 1** of detection, improving to 0.98 at late epochs when the light curve is fully sampled [^802^]. It processes thousands of light curves in seconds and has been deployed on the ALeRCE and ANTARES brokers, where it classifies 5,000+ extragalactic transients per night on the ZTF stream. Installation is via `pip install astrorapid`.

#### 9.4.3 SNID-SAGE: Python spectral classification

**SNID-SAGE** is a modern Python replacement for the classic SNID spectral classification tool [^753^] [^754^]. While the original SNID uses cross-correlation against a template library of 5,000+ spectra to determine redshift, type, and age [^755^], SNID-SAGE adds a Python/PySide6 graphical interface, a new match-quality metric, redshift-space clustering to consolidate template matches into stable classifications, and an optional LLM-powered analysis assistant via OpenRouter [^753^]. The template library includes **698 templates** covering Ia, Ib, Ic, II, SLSN, TDE, and kilonova types. The system has been validated on approximately 46,000 WISeREP spectra. Installation is via `pip install snid-sage`.

#### 9.4.4 DASH: CNN spectral classifier

**DASH** (Deep Automated Supernova and Host classifier) applies a CNN directly to supernova spectra for type, subtype, and age determination [^831^]. It achieves **97.5% type accuracy** on its validation set and is **100 times faster** than Superfit, the traditional chi-squared template-matching tool. DASH is available both as a GUI for interactive classification and as a Python library for batch processing (`pip install astrodash`).

#### 9.4.5 PELICAN: CNN light curve "images"

**PELICAN** (Photometric Estimation of Light curves with an Image ANalyzer) takes an alternative approach to encoding temporal structure: it converts light curves into two-dimensional "images" by plotting flux against time and wavelength, then applies a standard CNN architecture [^859^]. On simulated LSST data, it achieves **96.5% accuracy** for SN Ia classification even when trained on small samples of just 2,000 deep drilling field (DDF) light curves. This data efficiency makes PELICAN attractive for early Rubin operations, when the volume of labeled training data will be limited.

#### 9.4.6 Framework comparison

| Framework | Type | Core Algorithm | Installation | Real-time Ready | Key Metric |
|-----------|------|---------------|--------------|-----------------|------------|
| sncosmo | I/O library | SALT2/3 fitting, simulation | `pip install sncosmo` | No | 118+ citations, 100+ bandpasses [^35^] [^542^] |
| SuperNNova | ML pipeline | LSTM/GRU/Bayesian RNN | `pip install supernnova` | Yes | 96.9% Ia acc. (no z) [^256^] |
| ParSNIP | ML pipeline | Physics-enabled VAE | Source install | Yes | 2.3x less contamination than SOTA [^79^] |
| SCONE | ML pipeline | 2D GP + CNN | Source install | No | 99.7% Ia acc., filter-independent [^785^] |
| snmachine | ML pipeline | Wavelet + GBDT/SVM/ANN | `pip install snmachine` | No | 291+ citations, AUC ~0.96 [^407^] |
| SNANA | Simulator | C++ simulation/fitting | Source compile | No | 117M LCs/8h/40 cores, 1000+ citations [^254^] |
| LightCurveLynx | Framework | DAG forward-modeling | `pip install lightcurvelynx` | No | KL div. ~0.01-0.02 vs. ZTF [^377^] |
| MOSFiT | Fitter | MCMC physical models | `pip install mosfit` | No | Open Catalogs integration, 100+ citations [^763^] |
| BTSbot | ML pipeline | ConvNeXt + metadata CNN | `pip install btsbot` | Yes | 96% purity, 99% completeness [^888^] |
| RAPID | ML pipeline | GRU early classifier | `pip install astrorapid` | Yes | AUC = 0.95 at day 1 [^802^] |
| SNID-SAGE | Spectral tool | Cross-correlation + LLM | `pip install snid-sage` | Yes | 698 templates, 46K spectra validated [^753^] |
| DASH | Spectral tool | CNN on spectra | `pip install astrodash` | Batch | 97.5% type acc., 100x faster than Superfit [^831^] |
| PELICAN | ML pipeline | CNN on LC "images" | Source install | No | 96.5% on simulated LSST, 2K training samples [^859^] |

The table reveals a clear pattern: pip-installable packages (sncosmo, SuperNNova, BTSbot, RAPID, SNID-SAGE, DASH) dominate the real-time tier, while source-install tools (SNANA, SCONE, PELICAN, ParSNIP) target offline analyses where performance justifies the setup effort. Every real-time framework has been integrated into at least one broker—SuperNNova into Fink, RAPID into ALeRCE and ANTARES, ParSNIP into AMPEL, BTSbot into Fritz/Kowalski—confirming broker deployment as the standard validation path. The RNN/GRU family (SuperNNova, RAPID) and CNN family (BTSbot, SCONE, DASH, PELICAN) split the field evenly, with VAE-based approaches (ParSNIP) representing a smaller but growing category distinguished by generative modeling and anomaly detection.

### 9.5 End-to-End Pipeline Architecture

#### 9.5.1 The standard pipeline pattern

A standard supernova ML pipeline in 2025 follows a four-stage pattern that connects simulation to science output:

**Stage 1 — Simulation**: SNANA or LightCurveLynx generates labeled training, validation, and test light curves. SNANA is preferred for large-volume production runs (100M+ events), while LightCurveLynx offers greater flexibility for custom parameter distributions and survey configurations.

**Stage 2 — Classification**: A trained ML model (SuperNNova for RNN-based typing, ParSNIP for generative modeling with anomaly detection, or SCONE for maximum accuracy on archived data) assigns class probabilities to each event.

**Stage 3 — Fitting and bias correction**: For SNe Ia, sncosmo or SNANA's `snlc_fit` performs SALT2 fitting to extract distance moduli. The BEAMS with Bias Correction (BBC) framework corrects for selection effects and classification contamination.

**Stage 4 — Cosmology**: The corrected distance moduli feed into wfit or SALT2mu to constrain cosmological parameters (w, Omega_m).

This pipeline is typically executed within an alert broker context for real-time applications, or as a batch workflow for cosmology analyses. The broker ecosystem (Fink, ALeRCE, AMPEL, ANTARES, Lasair) provides the middleware that connects Stage 1 (alert generation) to Stage 2 (classification) and routes Stage 3 (follow-up triggering) to telescope scheduling systems [^701^] [^800^] [^210^].

#### 9.5.2 PIPPIN: the orchestration layer

**PIPPIN** is the standard Python-based orchestration layer for supernova cosmology pipelines [^552^]. It integrates SNANA for simulation and fitting, SuperNNova or ParSNIP for classification, BBC for bias correction, and wfit/SALT2mu for cosmology fitting into a single declarative workflow defined by a YAML configuration file. A user runs `pippin.sh my-analysis.yml` to execute the full pipeline from simulated light curves to cosmological constraints, with PIPPIN managing job submission, dependency tracking, and output aggregation across heterogeneous compute environments.

PIPPIN's value lies in reproducibility: by encoding the entire analysis chain—from simulation parameters through classification model weights to cosmology fit settings—in a single version-controlled configuration, it ensures that cosmology results can be rederived exactly. This is essential for systematic uncertainty estimation, where the DES five-year analysis used 25 separate mock simulations to quantify the impact of training set representativeness on classification accuracy [^256^].

#### 9.5.3 Integration patterns and recommended stack

| Pipeline Layer | Primary Tool | Alternatives | Integration Point |
|---------------|--------------|--------------|-------------------|
| Data I/O | sncosmo | SNANA Python wrappers | Reads all SNANA FITS; registry for custom filters [^540^] |
| Simulation | SNANA | LightCurveLynx, tdastro | 117M LCs/8h/40 cores; BYOSED for Python models [^254^] |
| Classification (RNN) | SuperNNova | RAPID (early-time) | PIPPIN-integrated; 96.9% Ia acc. without z [^256^] |
| Classification (VAE) | ParSNIP | — | AMPEL-integrated; 2.3x less contamination [^79^] |
| Classification (CNN) | SCONE | PELICAN, BTSbot | Best accuracy (99.7%); filter-independent [^785^] |
| Spectral typing | SNID-SAGE | DASH | 698 templates; batch + interactive [^753^] |
| Physical fitting | MOSFiT | — | Open Catalogs integration; MCMC posteriors [^763^] |
| Bias correction | BBC (SNANA) | — | Standard for DES/Rubin cosmology |
| Orchestration | PIPPIN | Custom Airflow/Dagster | YAML-defined; DES production pipeline [^552^] |
| Broker deployment | Fink/ALeRCE/AMPEL | ANTARES, Lasair | Pre-trained classifications via REST API [^701^] |

For ML practitioners starting a new supernova project, the recommended stack depends on the latency requirement. **For real-time broker applications**, begin with sncosmo for data I/O, SuperNNova or RAPID for classification, and deploy via the Fink or ALeRCE Python client. **For maximum accuracy on archived data**, use SCONE's 2D GP + CNN pipeline or ParSNIP for anomaly detection. **For cosmology analyses**, adopt the full PIPPIN orchestration stack: SNANA simulation → SuperNNova classification → SNANA fitting → BBC correction → wfit cosmology. **For spectral classification**, SNID-SAGE provides the most comprehensive template library with modern Python tooling, while DASH offers the fastest CNN-based alternative.

A final consideration is the sim-to-real gap documented across multiple studies: classifiers trained purely on simulated data typically show 5–15% lower accuracy on real spec-confirmed samples than their simulation validation scores would suggest. The recommended practice is to validate all simulation-trained models on real data from low-redshift anchors (CSP, CfA, Foundation) before deploying them to broker streams or publishing cosmology constraints. This validation step is not merely a best practice—it is the single largest determinant of a classifier's real-world performance.

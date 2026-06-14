# Complete Guide to Supernova Survey Datasets for Machine Learning

> **Date**: June 2026
> **Scope**: Publicly available supernova datasets from 25+ active and legacy surveys, 60+ datasets, 7 alert brokers, 12 simulated datasets, and 10 upcoming missions
> **Target Audience**: Machine learning practitioners and astrophysicists

---

# Executive Summary

This report presents a comprehensive survey of publicly available supernova (SN) datasets for machine learning practitioners, synthesizing findings across 12 research dimensions covering 60+ datasets, 25 active and legacy surveys, 12 simulated datasets, and 7 real-time alert brokers. The analysis identifies critical opportunities, persistent gaps, and actionable recommendations for researchers entering the rapidly evolving field of time-domain astronomical classification. The landscape is characterized by an unprecedented abundance of simulated training data — PLAsTiCC alone provides 3.5 million events, and ELAsTiCC contributes ~50 million alerts — alongside a severe shortage of real spectroscopic labels totaling only ~3,000 confirmed SNe Ia across all surveys. This asymmetry creates a domain adaptation challenge that affects every photometric classifier. Complementing this data landscape is a maturing Python software ecosystem that has transformed from custom research scripts to pip-installable production frameworks, and a narrow temporal window before the Vera C. Rubin Observatory's full alert stream of 7–10 million alerts per night transforms the field. This executive summary distills the six most consequential findings for ML practitioners.

## Key Findings

**The Dataset Landscape.** Over 60 publicly available supernova datasets exist across more than 25 active and legacy surveys, spanning from small precisely calibrated low-redshift samples to billion-object all-sky catalogs. The largest real labeled collections include ZTF SN Ia Data Release 2 (3,628 spectroscopically confirmed SNe Ia) [^1^], the Dark Energy Survey 5-Year release (1,635 cosmology-grade SNe Ia) [^342^], and compilation datasets Pantheon+ (1,701 SNe Ia from 18 surveys) [^451^] and Union3 (2,087 SNe Ia from 24 datasets) [^189^]. Space-based missions contribute unique wavelength coverage: TESS provides 307 SNe Ia with 30-minute cadence light curves [^3^], Swift/SOUSA offers 253 SNe with UVOT 6-filter photometry, and GALEX hosts 1,080 SNe Ia in the ultraviolet via the gPhoton2 pipeline. The Open Supernova Catalog aggregates over 50,000 SNe of all types in JSON format, serving as the most comprehensive cross-survey aggregation available [^6^].

**The Sim-to-Real Gap.** Simulated datasets dwarf real labeled data by orders of magnitude. PLAsTiCC contains 3.5 million simulated events across 15 astrophysical classes [^184^][^605^], ELAsTiCC provides approximately 50 million alerts in a hierarchical taxonomy of 30+ classes [^641^][^642^], the Roman Hourglass simulation generates 64,000+ transients with both photometry and spectroscopy [^622^][^328^], and the Maven multimodal dataset contributes 500,000 events on HuggingFace. OpenUniverse2024 offers 400 TB of joint Roman+Rubin synthetic imaging over ~70 deg² of overlapping coverage [^301^][^302^]. By contrast, all low-z anchor surveys combined — CSP DR3 (134 SNe Ia) [^166^], CfA (~278) [^398^], Foundation DR1 (225) [^426^], PS1-MDS (365), and YSE DR1 (1,975, mostly photometric) — total only approximately 3,000 spectroscopically confirmed SNe Ia. This roughly 1,000:1 simulated-to-real ratio creates a fundamental domain adaptation challenge that affects every photometric classifier in the field.

**Critical Insight: The Sim-to-Real Chasm.** Classifiers trained on simulated data exhibit systematic performance degradation of 5–15% on real spectroscopically confirmed observations, a gap that persists across architectures from SuperNNova RNNs (96.9% accuracy on simulations without redshift, 99.6% with redshift) [^256^] to ParSNIP variational autoencoders [^79^]. Five irreducible factors drive this: imperfect host galaxy confusion modeling, calibration systematics, weather and seeing variations, real-bogus artifact distributions, and rare subclass population dependencies. The DES collaboration addresses this by running 25 separate mock simulations for systematic uncertainty estimation [^456^], yet even this extensive approach does not fully close the gap. This sim-to-real domain shift is the single most significant unsolved problem in supernova ML. Every simulation-trained model must be validated on real spectroscopic samples before deployment.

**Broker ML as a Service.** Seven Rubin Observatory community brokers — ALeRCE, Fink, AMPEL, ANTARES, Lasair, Babamul, and Pitt-Google — now provide pre-trained classifications via Python APIs, effectively offering model-as-a-service infrastructure [^44^]. ALeRCE's stamp classifier achieves 94% balanced accuracy and has reported 6,846 SN candidates with 971 spectroscopic confirmations [^685^]. Fink pioneered real-time active learning for SN Ia classification, achieving 89% purity and identifying candidates a median of 6 days before peak brightness [^729^]. For most applications, querying broker APIs is more efficient than retraining from scratch: running SuperNNova independently on Rubin's 10 million nightly alerts would require approximately $10,000 per day in compute, whereas brokers amortize this cost across the entire community. ML practitioners should treat broker classifications as input features — analogous to pre-trained embeddings in NLP — and fine-tune only when novel classification targets or specialized performance requirements exist.

**The 12-Month Readiness Window.** A narrow temporal window extends from mid-2025 through approximately mid-2027 during which Rubin simulation data (DP0, ~181 GB via DESC DC2 [^370^]), Roman simulations (Hourglass on Zenodo [^328^], OpenUniverse2024 on AWS S3 [^302^]), and early Rubin commissioning data (DP1, released June 2025 with ~2.3 million objects [^767^]) are all publicly accessible. After this period, Rubin's data rights policy imposes a 2-year proprietary restriction on much of the real survey data [^765^]. ML researchers who develop and validate classifiers during this window using the combined simulation-plus-commissioning data will hold a decisive first-mover advantage when the full Rubin stream arrives at 7–10 million alerts per night [^793^][^929^].

**Cross-Cutting Challenges.** Five additional findings carry high confidence. First, data format fragmentation across SNANA FITS, Avro, JSON, VOTable, Parquet, HDF5, and ASCII creates a "Format Tower of Babel" where normalization costs rival model development; sncosmo reads SNANA FITS natively but lacks support for modern streaming formats [^35^]. Second, near-infrared training data remains critically scarce — only CSP DR3 provides significant real NIR photometry (YJH bands for 120 SNe) [^166^], while Euclid Q1's 161 NIR-transient measurements represent the largest real space-based NIR sample currently available [^824^]. Third, the seven brokers use different ML architectures (CNN, RNN, GRU, VAE, GBDT), producing classification disagreements for 5–10% of transients that serve as powerful anomaly detection signals. Fourth, the spectroscopic archive WISeREP hosts 72,503 spectra for 29,468 objects [^116^], but heterogeneous resolutions, wavelength ranges, and calibration methods require substantial preprocessing; SNID-SAGE (698 templates, ~46,000 WISeREP spectra classified) [^753^] and DASH (97.5% type accuracy) are emerging solutions. Fifth, citizen science projects including Galaxy Zoo: Weird and Wonderful (~2,000 volunteers assessing ~200,000 images) produced labels that correlate weakly with ML anomaly scores [^887^], suggesting they capture orthogonal information that remains largely untapped by production classifiers.

**Python Ecosystem Maturation.** The software landscape has transformed dramatically since 2020. Production packages are now pip-installable: `sncosmo` (118+ citations) [^35^], `supernnova` (100+ citations) [^256^], `fink-client` [^699^], `alerce` [^701^], `btsbot` [^888^], and `snid-sage` [^753^]. Pipeline orchestration frameworks (PIPPIN), broker integrations, and cloud-native deployments (Pitt-Google on GCP) enable non-specialists to deploy SN classifiers in approximately 10 lines of Python. The entry barrier has dropped precipitously, shifting the primary challenge from building classifiers to ensuring robust, validated performance on real observational data. These six findings — the dataset landscape, the sim-to-real chasm, broker ML services, the readiness window, cross-cutting challenges, and ecosystem maturation — frame the detailed recommendations and ten cross-cutting insights presented in the full report. Action during the current 12-month window will determine which methodologies define the standards for the next decade of supernova science.

---

---

# 1. Introduction to Supernova Datasets for Machine Learning

## 1.1 Why Supernovae Matter for ML

### 1.1.1 SNe as Cosmological Probes

Type Ia supernovae (SNe Ia) remain the most precise single tracer of cosmic expansion over the redshift range 0.01 < z < 2.3. Their utility rests on a well-established empirical property: after standardization by light-curve shape and color, SNe Ia exhibit a peak absolute magnitude dispersion of approximately 0.15 mag, making them effective "standard candles" for distance measurement [^409^]. The 2011 Nobel Prize in Physics was awarded for the discovery of cosmic acceleration using this technique, and subsequent surveys have dramatically enlarged the available sample. The Dark Energy Survey (DES) 5-Year Supernova Program alone provides 1,635 photometrically classified SNe Ia spanning 0.10 < z < 1.13, the largest single-instrument sample ever assembled [^342^] [^409^]. When combined with low-redshift anchor samples from the Carnegie Supernova Project (CSP), CfA, and Foundation surveys, the Pantheon+ compilation reaches 1,701 SNe Ia from 18 independent surveys, enabling constraints on the dark energy equation-of-state parameter *w* to within ~3% [^451^] [^487^].

The tension between the Hubble constant (*H*0) measured from the local distance ladder (Cepheids + SNe Ia) and that inferred from the cosmic microwave background (Planck) now stands at approximately 5 sigma, constituting one of the most pressing problems in cosmology [^481^]. Resolving this tension demands both larger SN samples and more precise photometric classification to eliminate systematics. The Vera C. Rubin Observatory, projected to discover millions of SNe Ia during its ten-year Legacy Survey of Space and Time (LSST), is expected to reduce the statistical uncertainty on *w* to below 1% and to decisively test whether the dark energy equation of state evolves with redshift (*w*0/*w*a parameterization) [^793^]. For machine learning practitioners, this translates into a clear scientific mandate: develop classification and parameter estimation models capable of operating at unprecedented scale while preserving the subtle photometric signatures that encode cosmological information.

### 1.1.2 The Classification Challenge

The central obstacle in SN cosmology is that the vast majority of discovered supernovae never receive spectroscopic confirmation. Spectroscopy—the traditional gold standard for typing—requires target-of-opportunity observations on 4-meter-class or larger telescopes, typically allocating 30–60 minutes per object. At current survey rates, only a few percent of detected transients can be spectroscopically classified; for the Rubin Observatory, spectroscopic follow-up of even 0.1% of detected SNe would be impossible [^793^] [^815^]. This reality makes **photometric classification**—inferring SN type from multi-band light-curve morphology alone—a critical capability.

The classification problem is nontrivial. SNe Ia, which power cosmological analyses, must be distinguished from core-collapse SNe (Type II, Type Ib/c), superluminous SNe (SLSNe), tidal disruption events (TDEs), active galactic nuclei (AGN), and variable stars, all of which populate the same discovery stream. SuperNNova, a recurrent neural network (RNN) framework, achieves 96.9% accuracy for Ia vs. non-Ia separation when redshift information is available, but this drops to approximately 83% without redshift—a regime relevant for the faintest, highest-redshift Rubin discoveries [^654^]. On five-class problems (Ia, II, Ib/c, IIn, SLSN-I), the Superphot+ classifier attains an F1-score of only 0.61 without redshift and 0.71 with redshift, illustrating the difficulty of fine-grained discrimination [^528^]. ALeRCE's stamp classifier achieves ~94% accuracy at the coarse level (transient vs. stochastic vs. periodic), but its light-curve classifier drops to an F1 of 0.62 ± 0.04 on four SN subclasses [^685^] [^528^]. These performance gaps—particularly for rare classes and early-time classification—define the frontier where ML research can have the greatest scientific impact.

### 1.1.3 Scale of the Opportunity

The Rubin Observatory will generate up to 10 million alerts per night at full LSST operations, with each alert corresponding to a 5-sigma detection in a difference image [^793^] [^815^]. Alerts are distributed as Apache Avro packets (~82 KB each) within approximately 60 seconds of shutter closure, streamed via Apache Kafka to seven community brokers [^298^]. The raw data rate of 0.2–5 Gbps dwarfs all previous time-domain surveys by orders of magnitude. For context, the Zwicky Transient Facility (ZTF)—currently the most productive open transient survey—produces roughly 0.1 million alerts per night and has discovered approximately 3,628 spectroscopically confirmed SNe Ia over its entire operational lifetime [^1^] [^24^]. Rubin will exceed this spectroscopic sample in a single week of operations, albeit without spectra.

The simulation datasets designed to prepare for this deluge are correspondingly massive. The Photometric LSST Astronomical Time-Series Classification Challenge (PLAsTiCC) released 3.5 million simulated events across 15 classes with 450+ million photometric observations [^184^] [^605^]. Its successor, the Extended LSST Astronomical Time-series Classification Challenge (ELAsTiCC), delivered approximately 50 million alerts in a streaming format matching the Rubin alert schema [^641^] [^642^]. OpenUniverse2024—a joint Roman+Rubin simulation—spans ~400 TB of synthetic imaging over 70 deg² of overlapping sky [^301^]. These volumes are not merely incremental improvements over previous datasets; they represent a qualitative shift in the scale of astronomical data processing that demands ML-first approaches. A classifier processing 10 million alerts per night has a computational budget measured in seconds per alert, ruling out expensive forward-modeling or Monte Carlo inference for real-time decisions.

## 1.2 The ML Practitioner's Landscape

### 1.2.1 Overview of Survey Types

The datasets available for SN ML research span a multidimensional landscape that can be organized along four axes: **observation mode** (photometric vs. spectroscopic), **temporal structure** (time-domain survey vs. static compilation), **platform** (ground-based vs. space-based), and **data origin** (real observations vs. simulated).

*Photometric surveys* dominate the available volume. ZTF provides g- and r-band (with limited i-band) photometry for billions of sources through 24 public data releases, with bulk light curves distributed as Apache Parquet files totaling 5–10 TB per release [^1^] [^9^]. DES offers deeper griz photometry via its Scene Modeling Photometry (SMP) pipeline, with 19,706 high-quality light curves and 25 independent mock simulations for training [^342^] [^395^]. The Young Supernova Experiment (YSE) contributes 1,975 transients observed in Pan-STARRS1 griz plus ZTF gr, with pre-computed ParSNIP classifications for all objects [^71^] [^402^].

*Spectroscopic data*, though smaller in volume, remains essential for training and validation. The Open Supernova Catalog (OSC) aggregates 50,000+ SNe with JSON-formatted per-object files [^6^]. WISeREP hosts 72,503 individual spectra for 29,468 objects from 30+ instruments, accessible via a Python API client [^4^]. The CfA archive alone provides 2,603 spectra of 462 SNe Ia spanning 1993–2008 [^398^]. These heterogeneous spectral libraries are indispensable for building template models and for validating photometric classifiers against spectroscopic ground truth.

*Space-based* missions provide unique wavelength coverage. Swift/SOUSA delivers six-filter UV/optical photometry (UVW2, UVM2, UVW1, U, B, V) for 253 SNe [^8^]. TESS monitors the sky at 30-minute cadence in a broad 600–1000 nm bandpass and has extracted light curves for 307 SNe Ia plus over 4,000 additional transients [^3^]. Gaia publishes 10,765 alerts with low-resolution BP/RP spectra at every epoch, offering the only space-based spectral time series at scale [^15^]. GALEX, via the gPhoton2 pipeline, provides UV photon-level time series for 1,080 SNe Ia [^12^].

*Simulated datasets* bridge the gap between current real data volumes and Rubin-era scales. PLAsTiCC (3.5M events, CSV format) remains the standard benchmark for multi-class photometric classification [^607^]. ELAsTiCC (~4.3M objects, Avro/FITS/Parquet) tests broker infrastructure under realistic streaming conditions [^334^]. The Roman Hourglass simulation provides 64,000+ transients across 10 classes with both photometry and prism spectroscopy in clean Parquet files, making it the most ML-ready simulation available [^622^] [^328^]. The Maven multimodal dataset offers 500,000 simulated light-curve–spectrum pairs on HuggingFace, specifically designed for foundation-model training [^699^].

The "low-z anchor bottleneck" remains a critical structural constraint: across all low-redshift surveys (CSP, CfA, Foundation, YSE, PS1-MDS combined), only approximately 3,000 spectroscopically confirmed SNe Ia exist, compared to millions of simulated events. This roughly 1,000:1 simulated-to-real ratio likely causes classifiers to overfit simulation artifacts and constitutes the dominant systematic risk in photometric SN cosmology. Empirical evidence for this gap is substantial: Gupta et al. (2025) found that redshift estimation models achieve R² = 0.580 on simulations but only R² = 0.431 on real ZTF data, a performance degradation of roughly 26% [^705^]. Domain adaptation techniques—adversarial training, contrastive alignment, and the Maven approach of synthetic pre-training followed by real-data fine-tuning—are actively being developed to close this chasm, but no general-purpose solution yet exists [^667^].

### 1.2.2 Key ML Tasks

The ML tasks relevant to SN science can be organized by latency requirement and scientific objective.

**Real-time classification** is the highest-priority task for Rubin operations. Brokers must assign a classification probability to each alert within seconds of detection to enable rapid follow-up prioritization. ALeRCE's stamp classifier processes the first-detection image cutout with a CNN, achieving ~94% accuracy and reporting 70% of SN candidates within one day of first detection [^685^]. Fink's active learning pipeline identifies SNe Ia with ~89% purity a median of 6 days before peak brightness, having spectroscopically confirmed 459 of 535 candidates (86%) through TNS [^47^] [^56^]. The Babamul broker deploys a multimodal AppleCiDEr framework that fuses photometry ([CLS]-Transformer, 87.8% accuracy), image cutouts (AstroMiNN), and spectra (SpectraNeXt-2D, 87.6%) into ensemble predictions [^718^].

**Cosmology parameter estimation** operates at longer latency. The DES-SN5YR analysis demonstrates a complete ML-integrated pipeline: SuperNNova classifiers assign P(Ia) probabilities, which are incorporated into the BEAMS with Bias Correction (BBC) formalism for the Hubble diagram, yielding constraints on Ωm and *w* from 1,829 SNe [^409^]. Neural posterior estimators trained on the 25 DES mock simulations can now recover input cosmology to within 1-sigma for both Ωm and *w* [^396^], opening the door to simulation-based inference approaches that bypass traditional likelihood-based methods.

**Anomaly detection** targets the unknown unknowns in the transient sky. The SNAD project explicitly uses broker classification disagreement as an anomaly signal, having identified 144 new SN candidates through a three-stage ML-plus-human pipeline [^11^]. Approximately 5–10% of transients show non-trivial classification divergence across the seven Rubin brokers, and this disagreement itself is a powerful novelty indicator.

**Early-time typing**—classification from the first few photometric points—enables the fastest follow-up. Studies show that random forests achieve ~82% accuracy with just 3 photometric points for Ia vs. II vs. Ib/c separation, rising to ~90% with 5 points and color information [^23^]. TESS and Kepler data, with their continuous 30-minute cadence, provide unique constraints on early rise morphology and shock breakout that ground-based surveys cannot match [^3^].

**Host galaxy association** provides critical contextual information. Lasair's Sherlock system cross-matches against Pan-STARRS1, AllWISE, 2MASS, SDSS, and the million-quasar catalog to classify transients by association type [^727^]. DES-SN5YR embeds host stellar mass, star formation rate, and photometric redshift directly in the SNANA FITS headers, enabling models that condition classification and distance estimates on host properties [^439^].

### 1.2.3 Survey Landscape at a Glance

The table below provides a compact reference to the major surveys, datasets, and simulations relevant to SN ML research. The entries are selected to cover the full wavelength, redshift, and data-volume range that a practitioner is likely to encounter when building training pipelines.

| Survey / Dataset | Type | Wavelength | Cadence | Data Volume | Access URL |
|:---|:---|:---|:---|:---|:---|
| **ZTF** (DR1–DR24) | Ground, time-domain | g, r, i | 3 days | 5B+ light curves; 5–10 TB/DR | irsa.ipac.caltech.edu/Missions/ztf.html [^1^] |
| **ZTF SN Ia DR2** | Ground, spec-confirmed | g, r, i | 3 days | 3,591 SNe Ia + 5,138 spectra | ztfcosmo.in2p3.fr [^24^] |
| **BTS** (Bright Transient Survey) | Ground, spec-complete | g, r | Daily | 11,575 spec-confirmed transients | sites.astro.caltech.edu/ztf/bts [^26^] |
| **DES-SN5YR** | Ground, time-domain | g, r, i, z | ~6 days | 19,706 SMP LCs; 1,635 SNe Ia | github.com/des-science/DES-SN5YR [^344^] |
| **CSP DR3** | Ground, low-z anchor | ugriBV, YJH | Variable | 134 SNe (90% with NIR) | csp.obs.carnegiescience.edu/data [^226^] |
| **Foundation DR1** | Ground, low-z anchor | g, r, i, z (PS1) | ~5.5 days | 225 SNe Ia | github.com/djones1040/Foundation_DR1 [^426^] |
| **YSE DR1** | Ground, young SNe | g, r, i, z + ZTF gr | 3 days | 1,975 transients (492 spec) | zenodo.org/records/7317476 [^68^] |
| **PS1-MDS** | Ground, medium-deep | g, r, i, z | ~6 days | ~5,200 SNe discovered | mastweb.stsci.edu/ps1casjobs [^21^] |
| **TESS** (TessTransients) | Space, high-cadence | 600–1000 nm | 30 min | 307 SNe Ia + 4,000+ transients | tess.mit.edu/public/tesstransients [^3^] |
| **Swift/SOUSA** | Space, UV/optical | UVW2–V (6 filters) | ~2 days | 253 SNe with UVOT photometry | archive.stsci.edu/prepds/sousa [^8^] |
| **Gaia Alerts** | Space, all-sky | G + BP/RP spectra | ~monthly | 10,765 alerts (2014–2019) | gsaweb.ast.cam.ac.uk/alerts [^15^] |
| **JWST** (JADES/COSMOS) | Space, NIR | 0.6–5.3 µm | ~1 year | 80+ high-z transients | archive.stsci.edu (JWST) [^18^] |
| **PLAsTiCC** | Simulated | ugrizy | LSST-like | 3.5M events, 15 classes | kaggle.com/c/PLAsTiCC-2018/data [^607^] |
| **ELAsTiCC / ELAsTiCC2** | Simulated (streaming) | ugrizy | LSST-like | ~4.3M objects, ~50M alerts | portal.nersc.gov/cfs/lsst/DESC_TD_PUBLIC/ELASTICC [^334^] |
| **Roman Hourglass** | Simulated | R, Z, Y, J, H, F | 5 days | 64K+ transients, 10 classes | zenodo.org/records/14262943 [^328^] |
| **OpenUniverse2024** | Simulated (joint) | Rubin + Roman | Rolling | ~400 TB, ~1.4M transients | irsa.ipac.caltech.edu/data/theory/openuniverse2024 [^301^] |
| **Maven** | Simulated + real | g, r, i + spectra | — | 500K sim pairs + 4,702 real SNe | huggingface.co/datasets/thelfer/multimodal_supernovae [^699^] |
| **Rubin DP0 (DESC DC2)** | Simulated | ugrizy | LSST ref. | ~181 GB (Object + Truth) | data.lsst.cloud [^370^] |
| **Rubin DP1** | Real commissioning | ugrizy | 48 nights | 3.5 TB, ~2.3M objects | data.lsst.cloud (RSP) [^765^] |
| **Euclid Q1** | Real, NIR | I_E, Y_E, J_E, H_E | Single-epoch | 164 transients (161 with photometry) | ESA Euclid Archive [^824^] |

The diversity of this landscape carries direct implications for ML pipeline design. A practitioner training a classifier on ZTF g+r-band data [^1^] will face a wavelength-domain shift when deploying on Rubin's six-band ugrizy system [^370^]; models trained on PLAsTiCC's simulated photometry [^607^] will encounter a "sim-to-real gap" of 5–15% accuracy degradation on spectroscopically confirmed samples [^705^]; and classifiers that ignore Swift UVW2–V color information [^8^] will forfeit a powerful discriminant between thermonuclear and core-collapse explosions. The data format heterogeneity—spanning SNANA FITS, Apache Avro, Parquet, HDF5, and ASCII—adds a further integration burden that rivals model development in effort; the sncosmo library, which reads SNANA FITS natively, has become the de facto standard despite not handling modern streaming formats like Avro or Parquet [^33^]. The Roman Hourglass simulation [^328^] currently offers the only substantial NIR training data for high-redshift SN classification, as real near-infrared SN datasets remain extremely scarce—CSP DR3 provides YJH bands for only 134 SNe [^226^], and Euclid Q1's 161 transient measurements represent single-epoch detections rather than full light curves [^824^]. These gaps define the problem frontier: the most impactful ML research in the coming years will be research that bridges wavelength regimes, closes the sim-to-real divide through domain adaptation, and scales to the 10-million-alert nights that Rubin will deliver starting in 2026 [^793^] [^796^].

---

## 2. Ground-based Optical & Time-Domain Surveys

Ground-based optical time-domain surveys remain the largest and most data-rich source of supernova observations for machine learning research. Operating from the Zwicky Transient Facility's (ZTF) ~47 deg² nightly footprint to the Dark Energy Survey's (DES) deep 5-year cosmological program, these facilities collectively produce millions of light curves, tens of thousands of spectroscopically classified transients, and a growing ecosystem of ML-ready data products. This chapter surveys the primary ground-based surveys, their data formats, access methods, and the specific products most relevant to ML practitioners.

### 2.1 Zwicky Transient Facility (ZTF)

#### 2.1.1 Dataset Scope and Data Releases

The Zwicky Transient Facility, operating the Palomar 48-inch telescope (P48) with a 47 deg² field of view, is the dominant open-data resource for time-domain astronomy ML. ZTF produces 5,000–10,000 extragalactic transients per year [^1^] [^2^], with 24 public data releases (DR1 through DR24) available via the NASA/IPAC Infrared Science Archive (IRSA) as of early 2026 [^3^] [^4^] [^5^]. DR14 (October 2022) contained 5.5 TB of light curves in Apache Parquet format; subsequent releases through DR24 (January 2026) have expanded this volume significantly [^3^] [^9^]. Each release includes an Objects Table (source catalog), bulk light curves, reference images, science images, and metadata [^5^]. DR20 introduced the Zubercal recalibration pipeline, addressing spatial, chromatic, and temporal photometric systematics [^44^].

The ZTF Objects Table contains positional and photometric summaries for billions of sources, partitioned in HATS (Hierarchical Adaptive Tiling Scheme) format for efficient spatial queries and available as bulk Parquet downloads [^5^]. The complete ZTF dataset encompasses more than 5 billion light curves stored in matchfile format (HDF5), though the Parquet-format DR bulk downloads are the recommended access path for ML workflows due to their native compatibility with pandas and Dask [^42^].

#### 2.1.2 Key Data Products

ZTF distributes data through multiple channels optimized for different use cases. The Avro alert stream provides real-time transient notifications at a rate of ~0.1 million alerts per night from the public stream [^1^] [^39^] [^40^]. Alert packets follow a nested Avro schema (`ztf.alert` namespace) containing the candidate detection record, 30 days of previous candidate history (`prv_candidates`), forced photometry history (`fp_hists`), and image cutouts (science, reference, and difference) [^13^] [^14^] [^15^]. The recommended Python library for reading Avro packets is `fastavro`, which is substantially faster than the standard `avro-python3` implementation [^13^].

The forced photometry service (FPS) performs fixed-position PSF photometry on all publicly available ZTF difference images, returning flux measurements critical for constructing complete light curves including non-detections [^16^] [^17^] [^18^]. The FPS accepts requests via GUI or programmatically through wget/curl with public credentials (username: `ztffps`, password: `dontgocrazy!`) [^16^]. Several Python tools automate this process: `ztffp` by Michael C. Stroh [^19^], `fpbot`/`ztffps` by Simeon Reusch [^20^] [^21^], `ForcePhotZTF` by Yuhan Yao [^22^], and `ZTF_api` by Joan Alcaide [^23^].

Zubercal provides a comprehensive recalibration of ZTF science-image PSF photometry calibrated to the PS1 photometric system, correcting spatial systematics (dust spots, CCD thickness variations, edge glints), chromatic color-dependent effects, temporal throughput variations, and atmospheric cloud extinction [^44^] [^45^] [^46^]. The DR20 Zubercal release occupies approximately 10 TB, stored as snappy-compressed Apache Parquet files in 0.5° × 0.5° spatial tiles [^44^].

**Table 1: ZTF Data Products for Machine Learning**

| Data Product | Format | Volume | Access Method | ML-Ready | Notes |
|--------------|--------|--------|---------------|----------|-------|
| DR Light Curves (bulk) | Parquet | 5–10 TB per DR | wget from IRSA; AWS S3 | Yes | Dask/pandas native; filter by `catflags` for quality [^9^] |
| Objects Table | Parquet (HATS) | ~TB scale | IRSA bulk or astroquery TAP | Yes | Spatially partitioned for efficient cone searches [^5^] |
| Zubercal (recalibrated) | Parquet | ~10 TB (DR20) | atua.caltech.edu; AWS S3 | Yes | Corrects spatial, chromatic, temporal systematics [^44^] |
| Avro Alerts | Avro | ~0.1M/night public | UW archive; 7 brokers | Yes | 30-day history + cutouts; `fastavro` for reading [^13^] [^39^] |
| Forced Photometry | ASCII | Per-object | FPS web service | Yes (after parsing) | Essential for non-detections; batch via wget/curl [^16^] |
| ZTF SN Ia DR2 | FITS/ASCII | 3,591 light curves | ztfcosmo.in2p3.fr; WISeREP | Yes | Largest spec-confirmed SN Ia sample [^24^] |
| BTS Sample | Catalog | ~11,575 objects | BTS website; TNS cross-match | Yes | 97% complete at m < 18 mag [^26^] [^27^] |
| Matchfiles | HDF5 | 5B+ light curves | Internal/IPAC access | Partial | Historical format; prefer Parquet DR downloads [^42^] |
| Reference/Science Images | FITS | Per-field/epoch | IRSA IBE API | Yes | Cutout extraction via URL parameters [^3^] [^12^] |

ZTF data is also available on the AWS Open Data Registry, where HATS Parquet catalogs enable efficient cross-match queries using the LSDB (Large Survey DataBase) library [^10^] [^11^]. The `dessndr` package and `sncosmo` library provide complementary FITS-reading capabilities for the SN Ia DR2 product. For image-based ML, the IBE API supports cutout retrieval with position and size parameters specified in the URL [^3^] [^12^].

#### 2.1.3 ZTF SN Ia DR2

ZTF SN Ia DR2 is the largest spectroscopically confirmed Type Ia supernova dataset ever assembled, containing 3,591 SNe Ia light curves in g, r, and i bands with 5,138 individual spectra (at least one per SN Ia), host galaxy data tables (global and local 2 kpc aperture properties), and SALT2.4/SALT3 light curve fit parameters [^24^] [^25^]. The sample includes a volume-limited subset of approximately 1,200 SNe Ia at z < 0.06 that is unique for population studies [^25^]. Light curves were fitted with SALT2.4 with Taylor et al. (2023) retraining to extract stretch (x₁) and color (c) parameters [^25^]. Host galaxy tables include rest-frame g−z color, stellar mass log(M*/M⊙) in both local 2 kpc and global apertures, host coordinates, and redshifts (available for 60% of the volume-limited sample) [^24^] [^25^]. Data tables are available at https://ztfcosmo.in2p3.fr and through WISeREP [^24^].

#### 2.1.4 BTS (Bright Transient Survey)

The ZTF Bright Transient Survey (BTS) is the largest spectroscopic supernova survey conducted to date, providing a magnitude-limited (m < 19 mag in g or r), nearly complete spectroscopic sample of extragalactic transients [^26^] [^27^] [^28^]. As of 2024, BTS has spectroscopically classified 11,575 transients brighter than 19 mag, of which 11,427 are supernovae and 148 are other transient types [^26^] [^27^]. Spectroscopic completeness is 97% at m < 18 mag, 93% at m < 18.5 mag, and 75% at m < 19 mag [^26^] [^27^]. Every transient brighter than 18.5 mag is followed with the Spectral Energy Distribution Machine (SEDM) on the Palomar 60-inch telescope [^26^]. BTS-I (Fremling et al. 2020) described the survey design [^28^]; BTS-II (Perley et al. 2020) presented 4,095 transients with classifications, host associations, and demographic measurements [^27^]. Classifications are announced nightly via the Transient Name Server (TNS) [^26^]. BTS has also enabled precise measurement of relative SN rates: approximately 7% of core-collapse SNe explode in very low-luminosity galaxies (Mᵢ > −16), approximately 10% in red-sequence galaxies, and approximately 1% in massive ellipticals [^28^]. These demographic measurements provide important prior distributions for ML classifiers. BTS-specific forced photometry processing code is available on GitHub for generating flux-calibrated photometry from the ZTF FPS for all BTS transients observed from 2018–2020 [^29^].

#### 2.1.5 Python Access to ZTF Data

The `ztfquery` package by Mickael Rigault and Simeon Reusch is the most comprehensive Python interface for ZTF data access, providing a wrapper around the IRSA web API for querying and downloading images, pipeline products, catalogs, light curves, observing logs, and marshal data [^30^] [^31^]. For image processing, `ztfimg` offers a dask-native, object-oriented API supporting operations at quadrant, CCD, and focal-plane levels with source extraction via `sep` [^32^] [^33^]. The `ztf-dr` package (ALeRCE) enables parallel downloading of any ZTF DR ≥ DR5 to S3-compatible storage with configurable worker processes [^34^]. The `alerce` Python client provides multi-survey access to ZTF and LSST data with ML classifications from the ALeRCE broker [^35^], while the `lasair` client interfaces with the Lasair broker for Sherlock cross-matches and TNS information [^36^].

IRSA TAP queries via `astroquery` provide a standard VO interface for catalog searches. The following pattern illustrates a typical cone search on the ZTF Objects Table:

```python
from astroquery.ipac.irsa import Irsa
from astropy.coordinates import SkyCoord
import astropy.units as u

coord = SkyCoord(ra=298.0025, dec=29.87147, unit='deg', frame='icrs')
table = Irsa.query_region(coordinates=coord, spatial='Cone',
                          catalog='ztf_objects_dr20', radius=5*u.arcsec)
```

For complex queries, TAP/ADQL supports full SQL syntax against the ZTF catalog. Bulk light curve downloads use `wget` against the IRSA Parquet directory structure organized by field (e.g., `https://irsa.ipac.caltech.edu/data/ZTF/lc/lc_dr20/`), with Dask or PyArrow for subsequent reading [^9^]. Light curve columns include `objectid`, `filterid` (1=g, 2=r, 3=i), `fieldid`, `hmjd`, `mag`, `magerr`, and `catflags`—the latter should be filtered to exclude `catflags = 32768`, which indicates cloudy or moon-affected observations [^9^].

The ZTF Alert Archive at the University of Washington (https://ztf.uw.edu/alerts/public/) hosts nightly summaries and historical Avro packets [^39^]. Seven community alert brokers (ALeRCE, Lasair, Fink, ANTARES, AMPEL, MARS, and Pitt-Google) process ZTF alerts and distribute them with real-time ML classifications [^40^]. ALeRCE provides light curve and stamp classifiers with an F1 score of 0.97 for the light curve classifier and 100% SN completeness at the operating point [^47^] [^50^]; Lasair offers Sherlock cross-matches with archival sources and TNS classifications [^36^]; Fink specializes in multi-messenger and early-phase SN detection. For many ML projects, querying broker APIs may be more efficient than downloading raw data and training from scratch, particularly for real-time applications where brokers amortize compute costs across the community.

### 2.2 Pan-STARRS1 Medium Deep Survey (PS1-MDS)

The Pan-STARRS1 Medium Deep Survey covered 10 fields (70 deg²) in 5 bands (grizy) over 4 years (2010–2014), discovering approximately 5,200 likely supernovae [^133^] [^134^]. Of these, 365 were spectroscopically confirmed SNe Ia spanning redshifts 0.03 < z < 0.68 [^133^]. The PS1 filter system (g_P1, r_P1, i_P1, z_P1, y_P1) provides excellent photometric calibration with 7–12 mmag stability [^507^], and the survey cadence of approximately 6 observations per 10 days per field approximates the observing pattern anticipated for the Rubin Observatory [^440^].

The 279 PS1 SNe Ia with the most precise distance estimates formed the backbone of the Pantheon compilation (Scolnic et al. 2018), which combined PS1, SDSS, SNLS, low-z, and HST samples into 1,048 SNe Ia for cosmology [^133^]. Jones et al. (2018) expanded this to 1,169 SNe Ia using photometric classifications, achieving a constraint of w = −0.989 ± 0.057 [^440^].

PS1 catalog data is accessed through the MAST CasJobs SQL interface (https://mastweb.stsci.edu/ps1casjobs), which provides full SQL query access to the PS1 catalog database with synchronous and asynchronous execution modes [^21^]. The MAST Portal (https://catalogs.mast.stsci.edu/) supports cone searches, catalog queries, and image cutout retrieval. ML practitioners working with PS1 data should note that Villar et al. (2020) published SuperRAENN photometric classifications for 5,243 PS1 "SN-like" light curves, achieving 87% accuracy across 5 classes (Type Ia: 62.0%, Type II: 19.8%, Type IIn: 4.8%, Type Ibc: 11.7%, SLSN-I: 1.6%) [^441^]. The PS1 calibration system achieves sub-1% relative precision across 3π steradians using the Supercal method [^134^], making PS1-MDS data particularly valuable for training classifiers where photometric consistency across fields is essential. The `sndata` Python package provides programmatic access to PS1-MDS light curves in a standardized format compatible with `sncosmo` [^409^]. For ML applications requiring high-redshift SNe Ia, PS1-MDS offers the largest spec-confirmed sample between z = 0.3 and z = 0.7 of any publicly available survey.

### 2.3 Dark Energy Survey (DES)

#### 2.3.1 DES-SN 5-Year Data Release

The Dark Energy Survey Supernova Program (DES-SN) used the Dark Energy Camera (DECam) on the Blanco 4-meter telescope at Cerro Tololo Inter-American Observatory (CTIO) to conduct a 5-year rolling search for supernovae, producing the largest single-instrument sample of cosmological SNe Ia ever assembled [^342^] [^350^]. The DES-SN5YR data release, published in 2024, contains 31,636 Difference Image (DiffImg) light curves and 19,706 Scene Modeling Photometry (SMP) light curves, of which 1,635 photometrically classified SNe Ia pass cosmology quality cuts over the redshift range 0.10 < z < 1.13 [^342^] [^350^] [^395^].

The DiffImg pipeline uses forced PSF photometry on difference images with deep template images from science verification, achieving approximately 2% photometric precision but with known limitations in tertiary star photometry and proper motion corrections [^394^] [^395^]. The SMP pipeline applies forward-modeling photometry that simultaneously fits time-varying SN flux and static host galaxy flux, using individual reference images selected for best quality, updated Y6 forward model calibration, and per-filter differential chromatic refraction (DCR) corrections. SMP achieves smaller scatter about SALT3 model fits across all bands and redshift ranges, increasing the cosmology sample from 1,499 (DiffImg) to 1,635 (SMP) [^395^] [^400^].

#### 2.3.2 Data Format and Access

DES-SN5YR data is distributed in SNANA FITS format through both GitHub (https://github.com/des-science/DES-SN5YR) and Zenodo (DOI: 10.5281/zenodo.12720777) [^344^] [^477^]. The release totals approximately 1.5 GB and includes seven top-level directories: `0_DATA/` (light curves), `1_SIMULATIONS/` (25 mock simulations), `2_LCFIT_MODEL/` (SALT3 models), `3_CLASSIFICATION/` (classification probabilities), `4_DISTANCES_COVMAT/` (Hubble diagram data), `5_COSMOLOGY/` (MCMC chains), `6_DCR_CORRECTIONS/`, and `7_PIPPIN_FILES/` (pipeline reproduction inputs) [^344^].

Light curves are stored as paired HEAD and PHOT FITS files. The HEAD file contains one row per SN with metadata including coordinates, redshifts, host galaxy properties (stellar mass log(M*/M⊙), star formation rate, ugrizY magnitudes, surface brightness at SN location), and pointers to the PHOT file. The PHOT file contains individual photometric observations with calibrated flux (FLUXCAL, where mag = 27.5 − 2.5·log₁₀(FLUXCAL)), flux uncertainties, PSF parameters, and quality flags [^439^]. Python access is straightforward via `sncosmo.read_snana_fits()` or the `dessndr` utility package, which provides convenience functions for loading photometry and classification data [^413^] [^485^].

#### 2.3.3 Mock Simulations and Systematic Testing

The DES-SN5YR release includes 25 statistically independent mock simulations, each containing SNANA FITS files with both SNe Ia and core-collapse SNe generated using the SALT3 SED model [^456^]. These simulations assume a flat ΛCDM cosmology (H₀ = 70.0 km/s/Mpc, ΩΛ = 0.685, ΩM = 0.315, w₀ = −1.0, wa = 0.0) and incorporate realistic observing conditions including detection efficiencies from Kessler et al. (2019), spectroscopic redshift efficiencies from Vincenzi et al. (2022), and host galaxy libraries from Qu et al. (2024) [^456^] [^475^]. The 25 simulations are critical for ML applications: they enable training of photometric classifiers (SuperNNova, SCONE, SNIRF), computation of BEAMS with Bias Correction (BBC) corrections, and validation of the full cosmological pipeline. The input cosmology is recovered to within 1σ for both Ωm and w when the full analysis pipeline is applied to each simulation [^396^].

The 1,635 cosmology-grade SNe Ia were classified primarily using SuperNNova (SNN), a recurrent neural network trained on >100,000 realistic DES-like simulations [^551^] [^258^]. Of the 1,635 SNe, 1,499 (91%) have SNN classification probability P(Ia) > 0.5 [^537^]. Classification probabilities from multiple algorithms (SNN, SCONE, SNIRF) are provided in the `3_CLASSIFICATION/` directory, enabling cross-classifier comparison and systematic uncertainty estimation [^413^].

### 2.4 Other Active Ground-based Surveys

#### 2.4.1 ASAS-SN

The All-Sky Automated Survey for SuperNovae (ASAS-SN) uses a network of 14-cm telescopes to image the entire visible sky nightly to g ~ 18.5 mag. ASAS-SN is not primarily a cosmological survey—its shallow depth limits it to nearby events—but it provides the most complete catalog of bright supernovae available. The ASAS-SN Bright Supernova Catalog (Neumann et al. 2022, Catalog V) contains 2,427 total SNe, complete to m_peak = 16.7 mag in g-band [^10^]. The survey is approximately 90% complete at m_peak ≤ 17.0 mag [^10^]. Public photometry for more than 100 million targets is available through the ASAS-SN Sky Patrol interface (https://asas-sn.ifa.hawaii.edu/), which supports ADQL queries and the `pyasassn` Python API [^15^]. The catalog includes classifications, host galaxy identifications with UV-to-mid-IR photometry, and redshifts, making it directly usable for ML training of bright-transient classifiers.

#### 2.4.2 SkyMapper

The SkyMapper Transient Survey (SMT) uses the 1.3-meter SkyMapper telescope at Siding Spring Observatory to survey the Southern sky in ugriz filters, with a focus on low-redshift SNe Ia [^65^] [^154^]. SkyMapper DR1 was released in 2018 and covers the Southern Survey region, which overlaps with the DES footprint. SN data from SkyMapper is accessible through a Table Access Protocol (TAP) interface and cross-matched with TNS. The survey targets approximately 400–600 galaxies per night and has published early data releases for transient science [^154^]. Scalzo et al. (2017) described the SMT survey design and its role as a low-z SN Ia hunter in the Southern hemisphere [^65^].

#### 2.4.3 OGLE

The Optical Gravitational Lensing Experiment (OGLE) is a long-running microlensing survey using the 1.3-meter Warsaw telescope at Las Campanas Observatory. While OGLE's primary science focus is gravitational microlensing in the Galactic Bulge, the survey's time-series photometry in V and I bands has yielded serendipitous supernova detections, particularly in the Magellanic Clouds and along high-extinction lines of sight [^208^] [^211^]. OGLE data is distributed through an FTP server and database query interface at https://ogle.astrouw.edu.pl [^208^]. The OGLE-IV transient detection system (http://ogle.astrouw.edu.pl/ogle4/transients/) publishes transient candidates in real time, including some extragalactic transients, though OGLE is not a primary SN survey for ML applications.

#### 2.4.4 Young Supernova Experiment (YSE)

The Young Supernova Experiment (YSE) operated from 2019–2021 using Pan-STARRS2 and ZTF to discover and classify young supernovae in their earliest phases. YSE DR1 (Aleo et al. 2023) contains 1,975 transients, of which 492 were spectroscopically classified and 1,483 photometrically classified using the ParSNIP variational autoencoder [^71^] [^402^]. ParSNIP achieves 82% accuracy across 3 classes (Ia, II, Ib/c) and >90% completeness and purity for SNe Ia on the spectroscopic test set [^282^]. The photometric sample contains 1,048 SNe Ia (~71%), 339 SNe II (~23%), and 96 SNe Ib/c (~6%) [^282^]. Data is available from Zenodo (DOI: 10.5281/zenodo.7317476) in SNANA HEAD+PHOT format, with ParSNIP classification results provided as CSV tables [^68^]. The YSE DR1 Tutorial GitHub repository demonstrates data loading, metadata extraction, and figure reproduction [^530^]. YSE's emphasis on early-phase observations makes it particularly valuable for training classifiers designed to operate on pre-peak light curves.

### 2.5 Legacy Ground-based Surveys

#### 2.5.1 SDSS-II SN Survey

The Sloan Digital Sky Survey-II Supernova Survey (2005–2007) repeatedly imaged Stripe 82 (300 deg² along the celestial equator) to discover and monitor SNe. The full data release (Sako et al. 2018) contains 10,258 variable and transient sources, including 4,607 SN candidates and 1,443 SNe Ia with spectroscopic redshifts and SALT2 distance moduli [^132^] [^135^]. An additional 677 purely photometric SNe Ia candidates with photometric redshifts are included. The survey used ugriz filters with a cadence of every other night for approximately 3 months per year over 3 years, reaching r ~ 22.5 mag and covering redshifts 0.05 < z < 0.4 (median z ~ 0.2) [^132^]. Data is available via the SDSS Science Archive Server in FITS and ASCII formats and is integrated into SNANA, `sncosmo`, and `sndata` [^53^] [^54^]. SDSS-II remains one of the most frequently used training datasets for SN classification ML due to its large, homogeneous sample with both spectroscopic and photometric classifications.

#### 2.5.2 SNLS

The SuperNova Legacy Survey (SNLS) was a 5-year program using the MegaCam imager on the Canada-France-Hawaii Telescope (CFHT) to discover and monitor approximately 500 Type Ia SNe for dark energy studies. SNLS3 (Guy et al. 2010) presented 231 SNe Ia that, combined with 123 low-z and 101 SDSS SNe, produced 495 SNe Ia for cosmology [^105^]. The final SNLS5 sample added additional SNe, bringing the total to approximately 400 SNe Ia from SNLS alone [^105^]. Spectroscopic observations from ESO/VLT (Balland et al. 2009) provided 139 spectra of 124 SNe Ia at z = 0.149–1.031 [^55^] [^57^]. SNLS data in u*g'r'i'z' filters is available through CDS/VizieR and the `sndata` Python package [^57^]. The CFHT Legacy Survey reference images and <1% precision photometric calibration (T0007 release) [^49^] make SNLS data well-suited for ML classification training, though access requires familiarity with CDS query services.

#### 2.5.3 ESSENCE

The Equation of State: SupErNovae trace Cosmic Expansion (ESSENCE) survey operated from 2002–2007 using the CTIO 4-meter Blanco telescope to discover approximately 200 Type Ia SNe at z ~ 0.5, designed to constrain the dark energy equation-of-state parameter w. The first cosmological results yielded w = −1.05 ± 0.13 [^17^] [^19^]. ESSENCE used primarily R and I filters with a cadence optimized for z ~ 0.5 SNe Ia. Spectroscopic data (FITS format) is available through the ESO Science Archive (Phase 3), and photometric light curves are accessible via VizieR [^17^]. With 102 spectroscopically confirmed SNe Ia in the first 4 years (z = 0.10–0.78) [^17^], ESSENCE is now most frequently encountered as a component of compilation datasets such as JLA and Pantheon+ rather than as a standalone ML training resource.

#### 2.5.4 PTF/iPTF

The Palomar Transient Factory (PTF) and its intermediate successor iPTF operated the same Palomar 48-inch telescope used by ZTF from 2009–2017, discovering thousands of SNe in g and R bands [^69^] [^76^]. Three data releases (DR1–DR3) are available through IPAC (https://www.ipac.caltech.edu/programs/ptf/), with an 18-month proprietary period followed by public release [^69^]. PTF/iPTF light curves were instrumental in developing early photometric classification methods: the Superphot training set used 518 spectroscopically classified PTF SNe across 5 classes [^13^], and Price-Whelan et al. (2014) published a sample of 10,000 light curves for variability studies. Spectra from PTF/iPTF are archived in WISeREP. While superseded by ZTF in both cadence and data volume, PTF/iPTF remains a valuable historical resource for training classifiers on pre-ZTF data and for studying long-term transient population evolution.

### 2.6 Comparison and Selection Guidance

#### 2.6.1 Survey Comparison Table

**Table 2: Ground-based Optical Survey Comparison for ML Applications**

| Survey | Years | SNe Ia Count | All Filters | Cadence | z Range | Primary Data Access |
|--------|-------|-------------|-------------|---------|---------|-------------------|
| ZTF | 2018–present | 3,628 spec-Ia (DR2) [^24^] | gri | ~3 days (g,r) | 0.01–0.3 | IRSA TAP; ztfcosmo.in2p3.fr; AWS S3 |
| PS1-MDS | 2010–2014 | 365 spec-Ia [^133^] | grizy | ~6 obs/10 days | 0.03–0.68 | MAST CasJobs; VizieR; sndata |
| DES-SN5YR | 2013–2018 | 1,635 photo-Ia [^342^] | griz | ~weekly rolling | 0.10–1.13 | GitHub; Zenodo; sncosmo |
| ASAS-SN | 2014–present | 2,427 total SNe [^10^] | g (later V) | nightly (all-sky) | <0.05 | Sky Patrol web; pyasassn API |
| YSE DR1 | 2019–2021 | ~1,048 photo-Ia [^282^] | griz + ZTF gr | variable | 0.01–0.5 | Zenodo; GitHub tutorials |
| SDSS-II | 2005–2007 | 1,443 spec-Ia [^132^] | ugriz | ~2 days | 0.05–0.4 | SDSS SAS; SNANA; sndata |
| SNLS | 2003–2008 | ~400 spec-Ia [^105^] | u*g'r'i'z' | ~3–4 days | 0.1–1.0 | CDS/VizieR; sndata |
| ESSENCE | 2002–2007 | ~200 spec-Ia [^17^] | R, I | optimized for z~0.5 | 0.2–0.8 | ESO archive; VizieR |
| PTF/iPTF | 2009–2017 | 518 spec-Ia (Superphot) [^13^] | g, R | ~3–5 days | 0.01–0.3 | IPAC archive; WISeREP |
| SkyMapper | 2014–present | ~30+ SNe Ia (early) [^65^] | ugriz | nightly (Southern) | <0.1 | TAP interface; TNS cross-match |

The table reveals a clear stratification by survey depth and scientific purpose. Shallow, wide-field surveys (ASAS-SN, ZTF) dominate the low-redshift discovery space with thousands of bright events, while deep, field-focused surveys (DES, PS1-MDS) provide the high-redshift cosmological samples essential for constraining dark energy evolution. For ML practitioners, the choice of survey depends critically on the target task: ZTF SN Ia DR2 offers the largest homogeneous spec-confirmed training sample; DES-SN5YR provides the richest multi-band photometric classification set with 25 accompanying simulations; ASAS-SN delivers the most complete bright-transient catalog; and YSE DR1 specializes in early-phase pre-peak observations. Legacy surveys (SDSS-II, SNLS, ESSENCE, PTF/iPTF) remain valuable for cross-survey generalization testing and for benchmarking classifier performance against established literature results.

#### 2.6.2 Data Access Methods Summary

**Table 3: Programmatic Data Access Methods for Ground-based Surveys**

| Survey | Primary Interface | Python Package | Query Language | Bulk Download | Authentication |
|--------|------------------|----------------|----------------|---------------|----------------|
| ZTF | IRSA TAP; AWS S3 | `astroquery.ipac.irsa`; `ztfquery`; `alerce` | ADQL/TAP; Python API | wget (Parquet) | Free IRSA account |
| PS1-MDS | MAST CasJobs | `sndata` (via `sncosmo`) | SQL | Web/API | Free MAST account |
| DES | GitHub; Zenodo | `dessndr`; `sncosmo` | — | git clone; wget | None |
| ASAS-SN | Sky Patrol | `pyasassn` | ADQL; Python API | Web; API | None |
| YSE | Zenodo | `sncosmo` | — | wget (tar.gz) | None |
| SDSS-II | SAS; SNANA | `sndata`; `sncosmo` | SQL (CasJobs) | wget; rsync | Free for DR |
| SNLS | CDS/VizieR | `sndata` | SQL (VizieR) | Web download | None |
| PTF/iPTF | IPAC | `ztfquery` (historical) | Web form | wget; web | None (public DR) |

The access landscape has converged substantially since 2020. The `sncosmo`/`sndata` ecosystem now provides a unified Python interface for SDSS-II, SNLS, CSP, and Foundation data, while `ztfquery` and broker clients (ALeRCE, Lasair, Fink) cover the ZTF alert and archive space. For surveys not yet integrated into these packages, TAP/ADQL services (IRSA, MAST, VizieR) offer standards-compliant query interfaces that work with `astroquery` or generic HTTP clients. The emergence of cloud-native distribution—ZTF on AWS S3, DES on GitHub/Zenodo—has dramatically lowered the barrier to bulk data access for ML workflows. A persistent challenge remains the "format tower of Babel": ZTF alerts use Avro, ZTF DR light curves use Parquet, DES uses SNANA FITS, SDSS-II uses FITS/ASCII, and legacy surveys use heterogeneous ASCII formats. ML practitioners should plan for a format normalization stage early in their pipeline development, as the time invested in unified data ingestion typically rivals the time spent on model architecture design.

For real-time applications, the seven ZTF alert brokers provide pre-computed ML classifications and cross-matches with TNS, enabling feature extraction without downloading raw alert packets [^40^]. For historical analysis, the bulk Parquet downloads from IRSA offer the most efficient path to large-scale ZTF light curve datasets, with Dask providing out-of-core computation for the multi-terabyte DR volumes. The DES-SN5YR GitHub repository stands as the most complete self-contained data release, bundling light curves, 25 simulations, classifications from three independent algorithms, and full cosmology reproduction pipelines in a single documented package [^344^].

When selecting a survey for a specific ML task, practitioners should consider three primary factors: sample size and class balance (ZTF leads for spec-confirmed SNe Ia; DES leads for photometrically classified high-z SNe Ia), redshift coverage (ASAS-SN and YSE for z < 0.05; DES for z > 0.5), and data completeness (forced photometry availability, non-detection upper limits, and host galaxy metadata). For training photometric classifiers intended for Rubin-era deployment, DES-SN5YR's 25 mock simulations offer the most realistic simulated training environment currently available, with input cosmology recoverable to within 1σ—providing a critical validation ground for simulation-to-reality transfer methods [^456^] [^396^].

---

# 3. Low-Redshift Anchor Surveys

The cosmological utility of Type Ia supernovae rests on a hierarchical calibration framework: high-redshift SNe Ia constrain the expansion history, but only if their luminosities can be standardized against a local sample whose absolute distances are known independently. The low-redshift (low-z) anchor — roughly $z < 0.1$, where peculiar velocities dominate the redshift uncertainty — provides this calibration. For machine learning, these same surveys furnish the only spectroscopically confirmed, multi-band light-curve templates against which photometric classifiers are trained and validated. Without them, the transition from spectroscopic to photometric typing — a requirement for next-generation surveys such as the Legacy Survey of Space and Time (LSST) — lacks a ground-truth foundation. This chapter examines the six primary low-z anchor surveys, their data formats, Python access interfaces, and the structural training bottleneck they collectively reveal.

## 3.1 Carnegie Supernova Project (CSP)

### 3.1.1 CSP DR3: The Gold Standard Low-z Training Set

The Carnegie Supernova Project (CSP) was conceived explicitly to provide the photometric calibration chain linking nearby Type Ia SNe to the Hubble flow. Data Release 3 (DR3), published by Krisciunas et al. (2017) [^166^], contains 134 SNe observed during CSP-I (2004–2009), of which 123 are spectroscopically confirmed Type Ia events. The remainder includes five Type Iax SNe, two super-Chandrasekhar candidates, two Type Ia-CSM events, and two SN 2006bt-like objects, offering a valuable but small window into spectroscopic subclasses that are frequently misclassified by photometric pipelines. The redshift range spans $z = 0.0037$ to $0.0835$ with a median of $z = 0.0241$, placing the bulk of the sample well within the peculiar-velocity regime where Cepheid-based distance measurements are available.

The photometric system is the most comprehensive of any low-z survey: optical imaging in the natural-system $ugriBV$ passbands is supplemented by near-infrared (NIR) photometry in $YJH$ for 120 of the 134 SNe (approximately 90%). This NIR coverage is not merely additive — it is cosmologically critical. NIR light curves of Type Ia SNe exhibit lower intrinsic scatter in peak luminosity (approximately 0.12 mag in $H$-band versus 0.15–0.20 mag in $B$-band) and are significantly less affected by dust extinction, making them more accurate standard candles when host-galaxy reddening is uncertain. For ML classifiers, the presence of $YJH$ photometry provides color features that help distinguish genuine SNe Ia from dust-reddened core-collapse events or AGN contaminants. No other low-z survey matches this wavelength breadth.

A practical limitation of the original DR3 release is the absence of reported redshift uncertainties. The Pantheon+ compilation team had to estimate these externally [^448^], which introduces a systematic floor of order 150 km s$^{-1}$ in the peculiar-velocity correction. ML practitioners training distance-sensitive models should adopt the Pantheon+ redshift values rather than the native DR3 values.

### 3.1.2 Data Access and the SNooPy Ecosystem

CSP DR3 data are distributed as a single ASCII tarball, `CSP_Photometry_DR3.tar.gz`, downloadable from the CSP website [^226^] under a Creative Commons BY license [^532^]. Individual SN files contain Modified Julian Date (MJD), filter name, magnitude, and magnitude uncertainty in the CSP natural system. Filter transmission functions and zero-points are provided as separate ASCII tables, which must be loaded into the analysis framework for correct synthetic photometry.

The `SNooPy` Python package [^224^], maintained by the CSP collaboration and available on GitHub [^529^], is the canonical tool for CSP data analysis. SNooPy provides: (1) a Type Ia light-curve template generator in the CSP $uBVgriYJHK$ passbands; (2) K-correction computation based on the Hsiao et al. (2007) spectral energy distribution (SED) templates; (3) Levenberg-Marquardt non-linear least-squares fitting; (4) interactive plotting utilities; (5) the Lira Law for $E(B-V)$ estimation from the $(B-V)$ color curve; and (6) wrappers for the SALT2 and MLCS2k2 fitters. SNooPy can also import data directly from the Open Supernova Catalog, simplifying cross-survey comparison studies. Installation remains source-based (`git clone` followed by `python setup.py install`), which may require manual dependency resolution on modern Python environments.

For ML pipelines that prefer a standardized interface, the `sndata` package [^409^] exposes CSP DR3 through the `sndata.csp.DR3` class. Methods include `download_module_data()`, `get_available_ids()`, `get_data_for_id(obj_id)`, and `iter_data()`, all returning Astropy tables in the SNCosmo standard format (MJD, band, flux, fluxerr, zp, zpsys). The `register_filters()` method automatically registers CSP filter passbands with SNCosmo, eliminating a common source of calibration error when combining CSP with other surveys.

### 3.1.3 Critical Role as Low-z Anchor

CSP DR3 serves two indispensable roles in the ML-cosmology pipeline. First, its NIR-enhanced light curves anchor the Hubble diagram at $z < 0.05$, providing the distance calibrators that underpin measurements of the Hubble constant $H_0$. Second, its multi-band templates — particularly the NIR color evolution — are the primary training data for classifiers that must operate in redder passbands, such as those planned for the Nancy Grace Roman Space Telescope. The sample size of 134 SNe is adequate for cosmological analysis when combined with other low-z samples, but it is a severe constraint for deep-learning models that typically require $10^4$–$10^6$ training examples. As a result, CSP data are most effectively used as a high-quality validation set or as fine-tuning data after pre-training on larger (but lower-fidelity) simulated samples.

## 3.2 Center for Astrophysics (CfA) Archive

### 3.2.1 CfA1 through CfA4: The Largest Low-z Spectroscopic Sample

The Harvard-Smithsonian Center for Astrophysics Supernova Group has published four major photometric data releases spanning two decades, together comprising approximately 324 spectroscopically confirmed Type Ia SNe [^398^] [^399^]. CfA1 (Riess et al. 1999) contributed roughly 20 SNe Ia in the 1990s; CfA2 (Jha et al. 2006) added approximately 25 SNe Ia from 1998–2000; CfA3 (Hicken et al. 2009) provided 185 SNe Ia from 2001–2008; and CfA4 (Hicken et al. 2012) delivered 94 SNe Ia from 2006–2011. All observations were conducted in the $UBVRI$ filter system. Beyond Type Ia events, the CfA archive includes 73 stripped-envelope SNe (Modjaz et al. 2014) and 60 Type II SNe (Hicken et al. 2017), the latter with multi-band photometry extending into the NIR ($u'UBVRIr'i'JHK$) [^488^] [^493^].

The spectroscopic holdings are unmatched among low-z resources: 2,603 individual spectra of 462 SNe Ia, collected between 1993 and 2008, are available as a 160 MB FITS archive (Blondin et al. 2012). Additional spectral releases include 645 spectra of 73 stripped-envelope SNe (Modjaz et al. 2014) and maximum-light SN Ia spectra from the FAST spectrograph. These spectra are the primary training data for spectroscopic classification ML models — in particular, recurrent neural network (RNN) and 1D convolutional neural network (CNN) architectures that operate directly on spectral feature vectors.

### 3.2.2 Data Format and Bulk Access

The CfA archive is hosted at `https://lweb.cfa.harvard.edu/supernova/SNarchive.html` [^398^], with bulk downloads available for all major data products. Photometry is distributed as ASCII files in both natural and standard magnitude systems; spectra are in FITS format with wavelength, flux, and uncertainty arrays. Filter passbands are provided as ASCII tar files. The total download footprint is approximately 200 MB for photometry and spectra combined, making it among the most data-dense low-z archives relative to its sample size.

The `sndata` package provides programmatic access to select CfA releases, though the interface is less uniform than for CSP because the CfA data span multiple papers with different file conventions. The SNANA format is not native to CfA; conversion is required for use with SNANA-based simulation pipelines.

A significant calibration challenge affects the CfA sample: the $B$-band zero-point uncertainties for CfA1 and CfA2 epochs are estimated at approximately 100 millimagnitudes [^508^], substantially larger than the 7–12 millimagnitude stability achieved by Pan-STARRS1 [^507^]. This inhomogeneity limits the CfA archive's utility for precision cosmology training unless Supercal corrections (Scolnic et al. 2015) [^508^] [^531^] are applied uniformly across all epochs. ML practitioners should treat survey identity as a categorical feature or apply explicit calibration offsets when combining CfA photometry with more modern datasets.

### 3.2.3 Role in Training Spectroscopic Classifiers and Cross-Validation

The CfA archive's spectroscopic depth makes it uniquely valuable for two ML tasks. First, the 2,603 SN Ia spectra provide the largest homogeneous low-z spectral training set available, supporting supervised learning of spectral typing at signal-to-noise ratios (S/N) comparable to those expected from 4-m class telescope follow-up of Rubin alerts. Second, the long time baseline (1993–2011) enables robust cross-validation: models trained on the CfA3 epoch and tested on CfA4, or vice versa, provide a stringent test of temporal generalization that mimics the challenge of deploying a classifier on future survey data. The stripped-envelope and Type II samples further enable multi-class training beyond the standard Ia-versus-core-collapse dichotomy, although the smaller sample sizes (73 and 60, respectively) require careful regularization to avoid overfitting.

## 3.3 Foundation Survey

### 3.3.1 Foundation DR1: 225 SNe Ia in SNANA Format

The Foundation Supernova Survey (Foley et al. 2018) [^426^] was designed to bridge the gap between the very nearby ($z < 0.02$) Cepheid-calibrated SNe and the intermediate-redshift ($z \sim 0.3$) samples from the Dark Energy Survey (DES) and Pan-STARRS1 Medium Deep Survey (PS1-MDS). Foundation DR1 contains 225 Type Ia SNe observed with the Pan-STARRS1 (PS1) telescope in the $griz$ filters; of these, 180 pass cosmology-quality cuts, and 175 lie at $z > 0.015$ where peculiar-velocity corrections are manageable. The cosmology analysis by Jones et al. (2019) [^427^] demonstrated that Foundation SNe Ia, combined with PS1-MDS data, constrain the dark energy equation-of-state parameter $w$ with competitive precision.

The survey design emphasizes homogeneity: all photometry comes from a single telescope (PS1) with a well-characterized photometric system, achieving calibration stability of 7–12 millimagnitudes [^507^]. The median cadence is 8 days overall, tightening to 5.5 days within 10 days of peak brightness — sufficient for ML classifiers that rely on rise-time and post-maximum decline-rate features. The redshift distribution, $z \sim 0.01$ to $0.08$ with median $z \sim 0.05$, overlaps substantially with CSP and LOSS but extends to slightly higher redshift, improving overlap with the DES sample.

Unlike the targeted surveys (CSP, LOSS), Foundation is an untargeted, magnitude-limited survey, which reduces the galaxy-selection bias that preferentially discovers SNe Ia in massive, early-type hosts. This selection function is closer to that of future wide-field surveys like LSST, making Foundation a more representative training sample for photometric classifiers that will operate in similar discovery modes.

### 3.3.2 Data Access, Format, and Host Galaxy Properties

Foundation DR1 is distributed through a GitHub repository [^426^] maintained by D. O. Jones, D. Scolnic, and M. Foley. Light curves are provided in SNANA format, with 180 cosmologically useful SNe Ia accompanied by a 1.5% photometric error floor added in quadrature to the measured flux uncertainties. Flux zero-points are set to the SNANA standard value of 27.5 mag. The repository includes PS1 filter transmission functions corrected for color-dependent biases in $g$-band due to point-spread-function (PSF)-fitting photometry.

A distinctive feature of Foundation DR1 is the inclusion of host galaxy stellar masses derived from ZPEG SED-fitting using GALEX, 2MASS, SDSS, and WISE photometry [^426^]. These masses are essential for applying the mass step correction — the empirical finding that SNe Ia in galaxies with stellar mass $\log(M_*/M_\odot) > 10$ are approximately 0.06 mag brighter after standardization than those in lower-mass hosts. For ML cosmology pipelines, host mass serves as both a covariate for distance bias correction and a feature that improves photometric classification accuracy when combined with light-curve shape and color. The repository also includes peculiar velocity corrections from the Carrick et al. (2015) model and Milky Way reddening estimates from Schlafly & Finkbeiner (2011).

Foundation's principal limitation for ML training is its restriction to the $griz$ optical bands, with no NIR coverage. This limits its utility for dust-extinction modeling and for training classifiers that must operate in the redder passbands of Roman or Euclid. The moderate sample size (180–225 SNe Ia) also falls short of the thousands of examples typically required for training deep neural networks from scratch.

## 3.4 Other Low-z Resources

### 3.4.1 KAIT/LOSS: Historical Nearby Supernova Survey

The Lick Observatory Supernova Search (LOSS), conducted with the Katzman Automatic Imaging Telescope (KAIT) and the Nickel 1-m telescope, comprises two data releases spanning 1998–2016. LOSS1 (Ganeshalingam et al. 2010) [^483^] contains 165 Type Ia SNe (105 in the cosmology-quality sample) observed in $BVRI$ from 1998–2008 at redshifts $z = 0.002$ to $0.095$. LOSS2 (Stahl et al. 2019) [^480^] [^520^] adds 93 Type Ia SNe in $UBVRI$ from 2009–2016. Together, LOSS1 and LOSS2 provide the largest sample of very nearby SNe Ia ($z < 0.01$), many of which occur in galaxies with Cepheid distance measurements and thus anchor the absolute luminosity calibration of Type Ia SNe for $H_0$ determination.

Data access is split: LOSS1 is available through the `sndata` package (`sndata.loss.Ganeshalingam13`) [^482^] and VizieR tables, while LOSS2 is distributed as part of the Pantheon+ compilation via its GitHub Data Release [^481^]. The inhomogeneity between LOSS1 ($BVRI$ only) and LOSS2 ($UBVRI$), combined with the targeted survey design that preferentially monitors known galaxies, introduces selection effects that must be modeled explicitly when using LOSS for ML training. The $B$-band calibration uncertainty (approximately 100 mmag for early epochs) [^508^] further limits precision cosmology applications unless corrected.

### 3.4.2 CfA Core-Collapse Program

The CfA Core-Collapse Program provides systematic photometric and spectroscopic coverage of non-Type Ia supernovae that are essential for training multi-class photometric classifiers. The Type II sample (Hicken et al. 2017) includes 60 events (Type II-P, II-L, IIn, and IIb) with photometry in $u'UBVRIr'i'JHK$ and 12 MB of accompanying spectra. The stripped-envelope sample (Bianco et al. 2014; Modjaz et al. 2014) contains 73 SNe with 645 spectra. These samples are smaller than the Type Ia collections but are among the largest homogeneous core-collapse datasets publicly available. For ML applications, they provide critical negative examples: the light-curve shapes, color evolution, and spectral signatures of core-collapse SNe define the decision boundaries that separate them from Type Ia events in feature space. Without such data, binary classifiers default to learning Ia-versus-not-Ia discriminators that are systematically biased by the absence of realistic core-collapse templates.

### 3.4.3 Calán/Tololo and Early-Epoch Compilations

The Calán/Tololo survey, conducted in the 1990s, established the modern paradigm of using Type Ia SNe as standardized candles and provided the first large sample of systematically observed low-z events. While superseded in sample size and photometric quality by CSP, CfA, and Foundation, the Calán/Tololo data remain embedded in historical compilations such as the Joint Light-curve Analysis (JLA) and Union2.1 samples. For ML practitioners working with these legacy compilations, the Calán/Tololo subset should be flagged for lower photometric precision and the absence of modern calibration chains. The JLA sample of 740 SNe Ia (Betoule et al. 2014), available via VizieR, includes these early data along with more modern observations, but the inhomogeneity across contributing surveys requires careful survey-indexed feature encoding or explicit calibration correction.

## 3.5 The Low-z Training Gap

### 3.5.1 Comparative Overview of Low-z Anchor Surveys

The low-z landscape can be characterized along five axes: sample size, wavelength coverage, photometric precision, data format, and ease of programmatic access. Table 1 summarizes these properties for the six primary low-z anchor surveys.

| Survey | SNe Ia (spec-confirmed) | Filter Bands | NIR Coverage | Photometric System | Data Format | Primary Access |
|:---|:---|:---|:---|:---|:---|:---|
| CSP DR3 | 123 [^166^] | $ugriBVYJH$ | Yes (90% of SNe) | Natural/AB | ASCII tarball | Direct [^226^], `sndata` [^409^], SNooPy [^224^] |
| CfA1–4 | ~324 [^398^] [^399^] | $UBVRI$ | Limited (CfA4 only) | Natural/Standard | ASCII + FITS spectra | Web [^398^], `sndata` |
| Foundation DR1 | 180 (cosmology) [^426^] | $griz$ | No | PS1/AB | SNANA ASCII | GitHub [^426^] |
| LOSS1+2 | ~150 [^483^] [^520^] | $UBVRI$ / $BVRI$ | No | Natural | ASCII, `sndata` | `sndata` [^482^], Pantheon+ [^481^] |
| YSE DR1 | ~492 spec-classified [^71^] | PS1 $griz$ + ZTF $gr$ | No | PS1/AB | SNANA HEAD+PHOT | Zenodo [^68^] |
| PS1-MDS | ~350 spec-Ia [^440^] | $griz$ | No | PS1/AB | SQL/CasJobs [^21^] | MAST Portal |

**Analytical interpretation.** Several patterns emerge from this comparison. First, there is an inverse relationship between wavelength coverage and sample size: CSP DR3 provides the broadest filter set (optical + NIR) but the smallest confirmed-Ia sample among the major surveys, while PS1-MDS and YSE DR1 offer larger samples but restrict coverage to optical $griz$ bands. This trade-off has direct implications for ML model design — classifiers trained exclusively on $griz$ data will lack the NIR color features needed to robustly separate dust-reddened SNe Ia from intrinsically red subclasses such as SN 2006bt-like events. Second, data format fragmentation remains a significant barrier: CSP uses native ASCII, CfA uses a mix of ASCII and FITS, Foundation uses SNANA, YSE uses SNANA HEAD+PHOT, and PS1-MDS requires SQL queries through the MAST CasJobs interface. The `sndata` package [^409^] mitigates this for CSP, CfA, and LOSS, but Foundation and YSE require custom loaders, and PS1-MDS demands database expertise. Any ML project combining multiple low-z surveys should budget substantial effort for format normalization — the "format tower of babel" problem identified across the broader SN data ecosystem. Third, only CSP DR3 provides significant NIR photometry; this NIR "blind spot" means that ML models destined for Roman Space Telescope $YJH$ filters or Euclid NISP bands lack real training data and must rely on simulated NIR light curves with unverified fidelity.

### 3.5.2 The Bottleneck: Quantifying the Low-z Training Deficit

The most consequential finding for ML practitioners is the sheer numerical deficit of spectroscopically confirmed low-z training examples. Table 2 itemizes the spec-confirmed and photometrically classified sample sizes across all major low-z surveys, together with their primary limitations for ML use.

| Survey | Spec-Confirmed SNe Ia | Photometric-Only SNe Ia | Total Usable for ML | Critical Limitation |
|:---|:---|:---|:---|:---|
| CSP DR3 | 123 | — | 123 | Small sample; no spectroscopic data in DR3 |
| CfA1–4 | ~324 | — | 324 | Inhomogeneous calibration between epochs [^508^] |
| Foundation DR1 | 180 | — | 180 | $griz$ only; no NIR |
| LOSS1+2 | ~150 | — | 150 | Targeted survey; galaxy-selection bias |
| YSE DR1 | ~492 | ~1,048 (ParSNIP-typed) [^282^] | ~1,540 | Only 2-year baseline; inhomogeneous follow-up |
| PS1-MDS | ~350 | ~1,169 (SuperRAENN-typed) [^441^] | ~1,519 | Requires CasJobs; not all SNe have spec classifications |
| **Combined unique total** | **~1,500–1,700** | **~2,200** | **~3,000–3,500** | Heavy overlap; spec-confirmed subset is the binding constraint |

**Analytical interpretation.** The combined spec-confirmed low-z sample across all six surveys amounts to approximately 1,500–1,700 unique Type Ia SNe, after accounting for overlaps (the same SNe frequently appear in Pantheon+, JLA, and individual survey releases). Adding photometrically classified events from YSE and PS1-MDS raises the total to roughly 3,000–3,500 SNe Ia with some form of classification label. This number — approximately 3,000 — represents the entire spectroscopically validated low-z training corpus available to the field as of 2025. By comparison, the PLAsTiCC simulation challenge alone generated 3.5 million events across 15 classes, and the ELAsTiCC Rubin simulation produced approximately 50 million alerts. The ratio of simulated-to-real training data exceeds 1,000:1, creating a sim-to-real gap that is among the most severe in observational astrophysics.

The implications are structural. Deep learning classifiers — particularly transformer-based light-curve models and variational autoencoders — typically require $O(10^4)$–$O(10^5)$ training examples to saturate performance. With only 3,000 spec-confirmed low-z SNe Ia, fully supervised training from scratch is infeasible. The field has responded with three complementary strategies, each with distinct trade-offs.

**Transfer learning and domain adaptation.** The dominant approach pre-trains models on large simulated datasets (PLAsTiCC, ELAsTiCC, SuperNNova simulations) and fine-tunes on the smaller real low-z sample. This reduces the real-data requirement but introduces a domain shift: simulations cannot perfectly reproduce host galaxy confusion noise, photometric calibration systematics, weather-induced seeing variations, and rare-population subclasses. Empirical evidence from the photometric classification literature indicates that classifiers trained purely on simulations and tested on spec-confirmed low-z samples typically exhibit 5–15% lower accuracy than those trained on matched real data. Domain adaptation techniques — adversarial training with gradient reversal layers (DANN), maximum mean discrepancy (MMD) regularization, or self-supervised pre-training on real light curves followed by supervised fine-tuning — partially mitigate this gap but remain underexplored in the SN literature.

**Active learning on streaming surveys.** The Zwicky Transient Facility (ZTF) and, prospectively, the Rubin Observatory alert stream provide an opportunity to grow the labeled low-z sample through targeted spectroscopic follow-up. Active learning frameworks iteratively select the most informative unlabeled events for follow-up observation, maximizing the information gain per telescope hour. Fink, ALeRCE, and other Rubin community brokers are implementing such pipelines, but the rate of new low-z spec confirmations is limited by 4-m class telescope availability to roughly 100–200 SNe Ia per year — a meaningful but incremental increase relative to the 3,000-event baseline.

**Semi-supervised and self-supervised learning.** Methods that leverage large unlabeled photometric datasets — through contrastive learning, masked light-curve modeling, or variational autoencoder latent-space clustering — can extract structural information from the millions of unlabeled ZTF and ATLAS light curves without requiring spectroscopic confirmation. Boone's ParSNIP architecture [^282^], applied to YSE DR1, exemplifies this approach: a variational autoencoder learns a latent representation from photometry alone, and the latent space separates SNe Ia from core-collapse events with 82% three-class accuracy even without redshift information. Extending such methods to the full ZTF archive (billions of light curves) represents a high-leverage opportunity for expanding effective training set sizes by orders of magnitude.

### 3.5.3 Implications for the ML Practitioner

The low-z training gap imposes three concrete constraints on model development. First, **any photometric classifier deployed on Rubin data must be validated on the spec-confirmed low-z sample** (CSP + CfA + Foundation) before it can be trusted for cosmological analysis. The 3,000 spec-confirmed SNe Ia are the only ground truth available; they are the binding constraint on classification purity and completeness estimates. Second, **survey calibration differences must be explicitly modeled**: the Supercal method [^508^] [^531^] measures cross-survey discrepancies averaging 10 mmag and reaching 35 mmag in some passbands, with the largest offsets in the $B$-band for legacy low-z surveys. A classifier trained on uncorrected CSP + CfA + Foundation data implicitly learns survey-dependent magnitude offsets that degrade generalization to Rubin's $ugrizy$ system. Third, **the NIR wavelength gap limits model readiness for Roman and Euclid**: with CSP DR3 providing the only significant real NIR training data, classifiers for these missions must rely on simulated NIR photometry (Hourglass, OpenUniverse2024) whose fidelity at the light-curve level remains largely unvalidated against real observations.

The low-z anchor surveys, despite their small collective size relative to simulation volumes, remain the indispensable bedrock of SN cosmology and ML classification. Every photometric classifier, every distance fitter, and every cosmological likelihood ultimately traces its calibration to these few thousand spectroscopically confirmed, multi-band light curves. The gap between their limited numbers and the massive data volumes of upcoming surveys is not a transient problem but a structural feature of the field — one that demands domain adaptation, active learning, and semi-supervised methods as core components of any production ML pipeline.

---

## 4. Spectroscopic Archives

Photometric classifiers may dominate survey-scale operations, but their training depends on spectroscopic labels. Every light-curve-based type assignment ultimately traces back to a spectrum that a human expert or template-matching algorithm has classified. This section examines the archives that preserve these spectra, the tools that extract physical parameters from them, and the pipelines that convert heterogeneous spectroscopic observations into machine-ready feature vectors.

The central reality of SN spectroscopy for ML is heterogeneity. Unlike photometric surveys that use standardized filters and calibrated pipelines, spectroscopic data arrive from dozens of instruments with resolutions spanning R ~ 100 to R ~ 22,500, wavelength coverage from the ultraviolet to the near-infrared, and flux calibration methods that vary by telescope and epoch. Building ML-ready datasets from this patchwork requires careful preprocessing, and the archives described here differ substantially in how close they bring data to that goal.

### 4.1 WISeREP

#### 4.1.1 Archive Scope and Content

The Weizmann Interactive Supernova data REPository (WISeREP) serves as the primary global archive for supernova spectroscopy, hosted at the Weizmann Institute of Science. As of early 2026, it contains 72,503 spectra for 29,468 objects, making it roughly two orders of magnitude larger than the next largest public SN spectroscopic dataset [^116^]. This collection spans more than three decades of observations, from the late 1980s through present-day follow-up programs, and encompasses not only core-collapse and thermonuclear supernovae but also tidal disruption events (TDEs), super-luminous supernovae (SLSNe), luminous blue variables, and active galactic nuclei. The archive's spectral type taxonomy recognizes more than 30 subtypes, from the common SN Ia and SN II-P to rare classifications such as SN Icn and SN Ia-CSM.

The diversity of WISeREP's holdings reflects its role as an aggregation point rather than a single-survey product. Spectra are contributed by individual observers, survey follow-up teams, and other archives, creating a collection that is comprehensive but instrumentally heterogeneous. More than 30 different spectrographs are represented, ranging from low-resolution classification spectrographs such as the Spectral Energy Distribution Machine (SEDM; R ~ 100) on the Palomar 60-inch to high-resolution echelle spectrographs. Resolutions span three orders of magnitude, and calibration quality varies from quick-look reductions suitable only for type classification to fully flux-calibrated, telluric-corrected spectra suitable for detailed line-profile analysis.

#### 4.1.2 Data Access Methods

WISeREP offers three distinct access pathways, each suited to different use cases. The web interface (https://www.wiserep.org) supports queries by object name, coordinates, redshift, spectral type, date range, instrument, and observer, with results downloadable as CSV, TSV, or JSON metadata accompanied by ASCII text or FITS spectrum files [^116^]. For programmatic access, the `wiserep_api` Python package (available via `pip install wiserep_api`) wraps the repository's URL-based query protocol, enabling bulk downloads by spectral type, automated retrieval of target spectra with instrument exclusions, and extraction of object properties including redshift, host galaxy, and coordinates [^430^]. The package supports more than 40 spectral types and can invoke SNID automatically on downloaded spectra, streamlining the classification workflow.

For researchers requiring the complete archive, the WISeWEBSpider tool provides a dedicated scraping utility that downloads all publicly available spectra while maintaining a structured directory hierarchy and guarding against duplicates [^118^]. A full initial scrape requires approximately 18.7 hours; subsequent update runs (for example, fetching only spectra from the last 30 days) complete in minutes. Individual object pages follow RESTful URL patterns (`https://wiserep.org/iauname/2013fs`), making it straightforward to construct target-specific data retrieval scripts.

#### 4.1.3 Spectral Diversity and Its Implications

The heterogeneity that makes WISeREP comprehensive also complicates its direct use for ML. Spectra arrive on different wavelength grids with varying resolutions, signal-to-noise ratios, and calibration states. ASCII files contain space-delimited wavelength, flux, and flux-error columns, while FITS files store these quantities in separate extensions [^116^]. Metadata records include object name, spectral type, redshift, observation date, observer, instrument, and telescope, but the completeness of these fields varies across submissions.

For ML practitioners, this diversity imposes a preprocessing burden. Spectra must be de-redshifted to the rest frame, interpolated to a common wavelength grid, and continuum-normalized before they can serve as inputs to classifiers or feature extractors. The archive's inclusion of both high- and low-resolution spectra means that a model trained on X-shooter data (R ~ 10,000) will encounter very different noise characteristics when applied to SEDM spectra (R ~ 100). Cross-survey consistency therefore becomes a critical concern, and pipelines that ingest WISeREP data wholesale must include robust calibration quality flags.

#### 4.1.4 ML Applications

WISeREP data power three broad categories of ML applications. First, spectral classification models use WISeREP spectra as training labels for photometric classifiers. The 72,503 spectra provide the largest set of spectroscopically confirmed types available, though the uneven distribution across types (SNe Ia dominate, followed by SNe II and SNe Ib/c, with rare types underrepresented) requires careful stratification during train-test splitting [^116^]. Second, feature extraction pipelines measure line velocities, pseudo-equivalent widths (pEWs), and continuum temperatures from WISeREP spectra, producing physical parameter vectors that serve as inputs to regression models or anomaly detectors. The `spectral_lines` Python package, for instance, measures 10 standard spectral feature zones including Ca II H&K, Si II 4000, Mg II, Fe 4800, S II W, Si II 5972, and Si II 6355, outputting velocities and pEWs suitable for random forest or neural network classifiers [^486^]. Third, anomaly detection systems use WISeREP's large collection of normal SNe to establish baselines against which unusual or previously unclassified spectra can be compared, with self-supervised approaches operating directly on the flux arrays showing particular promise for identifying rare subclasses without labeled training data.

### 4.2 Nearby Supernova Factory (SNfactory)

#### 4.2.1 Integral-Field Spectrophotometry

The Nearby Supernova Factory (SNfactory) is an international collaboration led by Lawrence Berkeley National Laboratory that has produced a dataset unique in the supernova literature: more than 300 SNe Ia observed with integral-field unit (IFU) spectrophotometry at redshifts z < 0.1 [^150^]. Unlike traditional long-slit spectroscopy, which captures only a one-dimensional cut through the target, IFU observations produce a spatially resolved data cube (two spatial dimensions plus wavelength), enabling precise host-galaxy subtraction, spatially varying extinction correction, and accurate flux calibration against simultaneously observed standard stars.

The SuperNova Integral Field Spectrograph (SNIFS), mounted on the University of Hawaii 2.2-m telescope, provides a 6" x 6" field of view sampled by 15 x 15 spaxels at 0.43" per spaxel, with wavelength coverage from 3,200 to 10,000 Angstroms split between blue (3,200-5,200 AA) and red (5,100-9,700 AA) channels [^478^][^483^]. The spectral resolution of R ~ 1,000-1,200 is modest compared to high-resolution spectrographs, but the spectrophotometric precision under photometric conditions is better than 5%, a level of accuracy that makes SNfactory data particularly valuable for training light-curve models where flux calibration directly affects distance modulus measurements [^478^].

#### 4.2.2 Data Releases and Content

The primary public dataset is the 2020 interim release, containing spectrophotometric time series for 210 SNe Ia comprising approximately 2,500 individual spectra observed between 2004 and 2013 [^150^][^464^]. These data include host-galaxy subtractions, extinction corrections, and flux-calibrated spectra spanning 3,300-8,600 AA, with phase coverage from 5 days before to 50 days after maximum light and a median of approximately 14 epochs per supernova. The data are available through the Centre de Donnees astronomiques de Strasbourg (CDS) and the project's data page at Lawrence Berkeley National Laboratory [^199^].

Beyond the SNfactory collaboration's own data releases, the SNIFS instrument continues to serve the broader community through the Spectroscopic Classification of Astronomical Transients (SCAT) survey. SCAT Data Release 1 contains 1,810 spectra of 1,330 transients observed from March 2018 to January 2023, including 838 SNe Ia spectra (722 objects), 392 SNe II (275 objects), and 125 SNe Ibc (78 objects), along with 171 nuclear transients and 229 stellar phenomena [^489^]. The SCAT data products, available through Zenodo, include FITS and ASCII spectra, multi-filter light curves with phenomenological fits, host galaxy associations, and summary plots totaling approximately 1 GB of science data.

#### 4.2.3 SUGAR and SNEMO Models

The SNfactory spectrophotometric time series have enabled two spectral template models that are themselves valuable as ML features. SUGAR (SUpernova Generator And Reconstructor) is a spectro-temporal model trained on 171 SNe Ia, using 13 spectral indicators near maximum light to extract three intrinsic factors via factor analysis [^461^][^190^]. The first factor captures coherent variation in pseudo-equivalent widths of Si and Ca lines, correlated with light-curve stretch; the second captures velocity variations; and the third shows slight correlation with stretch. SUGAR factor scores serve as compressed, physically motivated spectral features that describe most SN Ia diversity in just three dimensions, offering an alternative to raw principal component analysis that accounts for measurement errors [^461^].

SNEMO (SuperNova Eigenvectors using MOrlet wavelets) provides a complementary wavelet-based decomposition of the same spectral time series [^464^]. Both models are distributed with the SNfactory data releases and can be used to generate synthetic spectra as functions of time and wavelength, enabling data augmentation for ML training sets where observed spectra are scarce.

### 4.3 SDSS-V and Spectroscopic Follow-up Programs

#### 4.3.1 SDSS-V Multi-Epoch Spectroscopy

The Sloan Digital Sky Survey-V (SDSS-V), described in Almeida et al. (2025), is the fifth generation of the Sloan Digital Sky Survey, operating in three modes: the Milky Way Mapper, the Black Hole Mapper, and the Local Volume Mapper [^395^][^397^]. Data Release 19 (DR19), the second public data release, contains 479,081 optical BOSS spectra of stars, 390,676 near-infrared APOGEE spectra, and 318,123 galaxy and quasar spectra [^397^]. While SDSS-V is not a transient-focused survey, its BOSS optical spectra (R ~ 2,000, 3,650-10,400 AA) and APOGEE near-infrared spectra (R ~ 22,500, 1.5-1.7 um) contain serendipitous supernova observations and host galaxy redshifts that are valuable for photometric classification pipelines.

Access to SDSS-V data has been modernized for DR19. The Science Archive Server supports bulk downloads via wget, rsync, and Globus Online, while the new Zora web framework provides interactive search, target visualization, and a sky viewer [^396^]. The underlying Valis API, built in FastAPI, exposes programmatic endpoints for query, target retrieval, and maskbit inspection, with full documentation at https://api.sdss.org/valis/docs [^396^]. The legacy SDSS-II Supernova Survey, which produced multi-epoch imaging and spectroscopy of approximately 500 SNe Ia in the redshift range 0.05-0.4, is now available through the Mikulski Archive for Space Telescopes (MAST) [^397^].

#### 4.3.2 Major Telescope Archives

Beyond survey-specific releases, three major telescope archives provide access to supernova spectra obtained through PI-led programs. The Keck Observatory Archive (KOA) archives all science observations since 1994, with public data available after an 18-month proprietary period [^431^]. Supernova spectra are primarily from the Low Resolution Imaging Spectrometer (LRIS) and the Deep Extragalactic Imaging Multi-Object Spectrograph (DEIMOS), with the DEIMOS 1200G grating providing particularly high signal-to-noise data for stellar and supernova spectroscopy [^398^]. Reduced one-dimensional spectra and multi-epoch measurements are available through a web query interface and a programmatic API.

The ESO Science Archive Facility hosts data from the Very Large Telescope (VLT) X-shooter spectrograph, with more than 33,000 reduced spectra from 2009 onward, covering ultraviolet through near-infrared wavelengths (300-2,480 nm) in three arms at resolutions of R ~ 3,300-11,000 [^425^][^426^]. Programmatic access is available through the Simple Spectral Access Protocol (SSAP) as well as Table Access Protocol (TAP) services for both raw and reduced data [^463^]. The archive also supports server-side cutouts via the SODA service and DataLink for finding related calibration files.

The Gemini Observatory Archive contains all Gemini data since operations began, with a 12-month proprietary period for recent observations [^407^]. Reduced data products are classified as Quick-Look (for rapid evaluation) or Science-Quality (automated reduction with user verification recommended). Supernova spectroscopy is primarily from the Gemini Multi-Object Spectrograph (GMOS) [^409^][^415^], with data searchable by instrument, coordinates, and observation date. The archive provides a Python API for automated retrieval.

#### 4.3.3 Spectroscopic Archive Comparison

| Archive | Spectra Count | Object Count | Primary Instruments | Wavelength Coverage | Redshift Range | Access Method | Data Format | Proprietary Period |
|---|---|---|---|---|---|---|---|---|
| WISeREP | 72,503 [^116^] | 29,468 | 30+ spectrographs | Various | 0-2+ | Web, Python API | ASCII, FITS | None |
| SNfactory 2020 DR | ~2,500 [^150^] | 210 | SNIFS (UH 2.2-m) | 3,300-8,600 AA | z < 0.1 | CDS, project website | ASCII, FITS | None |
| SCAT DR1 | 1,810 [^489^] | 1,330 | SNIFS (UH 2.2-m) | 3,200-9,200 AA | z < 0.1 | Zenodo | ASCII, FITS | None |
| PESSTO SSDR4 | ~3,700 frames [^494^] | 2,323 | EFOSC2, SOFI (NTT) | 3,345-9,995 AA | All | ESO Science Portal | FITS (Phase 3) | None |
| ePESSTO+ SSDR1 | 2,138 [^465^] | 2,138 | EFOSC2, SOFI (NTT) | 3,345-9,995 AA | All | ESO Archive | FITS (Phase 3) | None |
| BSNIP (DR1+DR2) | 1,935 [^479^][^480^] | 824 | Kast (Lick 3-m) | 3,300-10,400 AA | z < 0.2 | Website, `sndata` | ASCII, FITS | None |
| ZTF BTS/SEDM | 5,138 [^151^][^514^] | 3,628 | SEDM (P60) | 3,500-9,500 AA | z < 0.5 | ZTF Archive | ASCII | None |
| SDSS-II SN Survey | ~1,000s [^397^] | ~500 | BOSS (SDSS 2.5-m) | 3,800-9,200 AA | 0.05-0.4 | SAS, MAST | FITS | None |
| VLT/X-shooter | 33,000+ [^425^] | 100s+ | X-shooter (VLT) | 300-2,480 nm | All | ESO SSAP, TAP | FITS (Phase 3) | None |
| Keck Archive | Varies [^431^] | 100s+ | LRIS, DEIMOS, HIRES | All Keck bands | All | KOA web/API | FITS | 18 months |
| Gemini Archive | Varies [^407^] | 100s+ | GMOS, GNIRS, NIFS | All Gemini bands | All | GOA web/API | FITS | 12 months |

This comparison reveals a clear ordering in ML readiness. WISeREP, BSNIP, the ZTF Bright Transient Survey (BTS), and SNfactory offer immediate programmatic access to well-documented, publicly available spectra with no proprietary restrictions. The telescope archives (Keck, VLT, Gemini) contain scientifically valuable data but require navigating proprietary periods, instrument-specific query interfaces, and heterogeneous reduction pipelines. For ML practitioners building training sets, the recommended priority is WISeREP for breadth, BSNIP for high-quality low-redshift SNe Ia with well-calibrated photometry, and SNfactory/SCAT for spectrophotometric time series. The ESO public surveys (PESSTO/ePESSTO+) provide excellent coverage of rare transient types including SLSNe and TDEs that are underrepresented in other archives.

### 4.4 Spectral Classification Tools

#### 4.4.1 SNID: The Classic Cross-Correlation Tool

SuperNova IDentification (SNID), developed by Blondin and Tonry (2007), remains the most widely used spectral classification code in time-domain astronomy [^435^]. Written in C with PGPLOT graphics, SNID determines supernova type, redshift, and age by cross-correlating an input spectrum against a library of template spectra in Fourier space. The current version 5.0 includes several template sets: the default SNID 2.0 templates, BSNIP SN Ia templates, SN Ib/c templates from Modjaz et al. (2014, 2016), Liu et al. (2016), and Williamson et al. (2019), and SN IIP templates from Gutierrez et al. (2017). The total template library encompasses approximately 5,000 spectra across all major SN types. SNID is released under the GNU General Public License and is available at https://people.lam.fr/blondin.stephane/software/snid/ [^435^].

SNID's cross-correlation approach offers several advantages for ML preprocessing. It is robust to noisy input spectra, requires no training data beyond the template library, and produces interpretable rlap (redshift-lap) significance scores that quantify the confidence of each classification. The tool achieves approximately 95% accuracy for SNe Ia with quality spectra (signal-to-noise ratio greater than 5), though performance degrades for heavily extincted or high-redshift objects where template coverage is sparse [^435^]. However, SNID's C-based implementation and dependence on PGPLOT for visualization make integration into modern Python ML pipelines cumbersome, and its batch-processing capabilities are limited compared to newer alternatives.

#### 4.4.2 SNID-SAGE: A Modern Python Replacement

SNID-SAGE addresses these limitations by reimplementing SNID's cross-correlation techniques in Python with a PySide6/Qt graphical interface, high-performance plotting via pyqtgraph, and modern features including multi-template inference, clustering, and LLM-powered analysis summaries [^433^]. The package includes 698 spectral templates and is installable via `pip install snid-sage`. Batch processing capabilities allow users to classify large collections of spectra in a single invocation, and the Python API enables direct integration with scikit-learn and PyTorch workflows. In comparative testing, SNID-SAGE achieves equivalent classification accuracy to the original SNID while offering substantially improved usability for ML practitioners [^433^].

A complementary development is the Super-SNID template library (Magill et al. 2025), which expands coverage to rare transient classes including SLSNe, TDEs, and luminous fast blue optical transients (LFBOTs) [^424^]. This addresses a significant gap in the original SNID templates, which were weighted toward common SN types. Integration of Super-SNID templates with either the original SNID or SNID-SAGE enables classification of the rare events that are increasingly discovered by wide-field surveys but lack spectroscopic templates in standard libraries.

#### 4.4.3 DASH: Deep Learning Spectral Classification

DASH (Deep Automated Supernova and Host classifier) represents a fundamentally different approach, using a deep convolutional neural network (CNN) trained directly on spectral flux arrays rather than cross-correlating against templates [^477^][^489^]. Developed by Muthukrishna et al. (2019), DASH classifies supernova type, age, redshift, and host galaxy properties in a single forward pass, processing thousands of spectra in seconds on a standard GPU. The model was trained on more than 4,000 supernova spectra from the Harvard-Smithsonian Center for Astrophysics (CfA) and BSNIP programs and tested on four years of OzDES data, demonstrating that learned features can match or exceed template-matching accuracy while operating orders of magnitude faster [^477^].

In direct comparisons, DASH achieves approximately 97.5% accuracy for SN type classification, with the speed advantage becoming particularly significant for survey-scale applications where 10,000+ spectra require classification per observing run [^477^][^489^]. Kim et al. (2024) tested SNID, NGSF (Next Generation SuperFit), and DASH on 4,646 SEDM spectra with Bright Transient Survey classifications, finding all three tools achieve high accuracy on quality spectra (signal-to-noise ratio greater than 3), with DASH providing the fastest processing and NGSF offering the most detailed fitting through its simultaneous modeling of supernova and host galaxy templates [^510^]. The combination of DASH for rapid bulk classification followed by NGSF for detailed modeling of interesting candidates achieves 99.9% purity at 70% efficiency for SNe Ia [^478^]. DASH is available via `pip install astrodash`, with pre-trained models hosted on Zenodo [^489^].

#### 4.4.4 Spectra-to-Features Pipeline

Converting heterogeneous archive spectra into ML-ready feature vectors requires a standardized preprocessing pipeline. The canonical sequence, drawn from literature practice [^410^][^411^], proceeds through four stages. First, spectra are de-redshifted to the rest frame using known redshifts (from host galaxies or line measurements), corrected for Milky Way extinction following Cardelli et al. (1989), interpolated to a common wavelength grid, and continuum-normalized using spline fits or the SNID normalization method. Second, spectral line measurements extract physical parameters: the `spectral_lines` package measures velocities and pseudo-equivalent widths for 10 standard feature zones including Ca II H&K, Si II 4000, Mg II, Fe 4800, S II W, Si II 5972, and Si II 6355, using the relativistic Doppler equation for velocity calculations [^486^]. Third, continuum parameters include blackbody temperature fits and slope measurements across wavelength regions. Fourth, global parameters such as phase (days from maximum light), redshift, and instrument metadata complete the feature vector.

| Tool | Method | Templates/Training | Speed | Type Accuracy | Best For | Installation |
|---|---|---|---|---|---|---|
| SNID 5.0 | Cross-correlation (C++) | ~5,000 templates [^435^] | Moderate | ~95% | Gold-standard classification, redshift/age | Source compile |
| SNID-SAGE | Cross-correlation (Python) | 698 templates [^433^] | Moderate | ~95% | Modern Python workflows, batch processing | `pip install snid-sage` |
| Super-SNID | Cross-correlation (add-on) | +SLSNe, TDEs, LFBOTs [^424^] | Moderate | ~95% | Rare transient classification | GitHub |
| NGSF | Chi-squared template matching | Host + SN templates [^480^] | Slow | ~95% | Detailed fitting with host galaxy modeling | GitHub |
| DASH | 1D CNN | 4,000+ CfA/BSNIP spectra [^477^] | Very fast | ~97.5% | Bulk automated classification | `pip install astrodash` |

Random forest feature importance analysis from Parrag (2023) indicates that the most informative spectral features for supernova classification are, in descending order: the standard deviation-to-mean ratio (a noise proxy, importance 0.451), blackbody temperature (0.191), Fe II 5169 velocity (0.124), H-alpha amplitude (0.112), and H-alpha velocity (0.077) [^410^][^411^]. Temperature and velocity measurements together account for nearly half of the model's predictive power, underscoring the physical basis of spectral classification. For time-series spectral data such as SNfactory's multi-epoch observations, Gaussian process interpolation to a common phase grid enables extraction of velocity evolution rates and equivalent width derivatives that capture the dynamical evolution of the ejecta [^461^].

The emerging ecosystem of spectral classification tools offers ML practitioners a choice tailored to their specific requirements. SNID remains the reference standard for single-spectrum classification with full interpretability. SNID-SAGE modernizes the interface and Python integration. DASH provides the throughput needed for survey-scale automated pipelines. NGSF delivers the most physically detailed modeling for science cases where host galaxy subtraction matters. For building large labeled training sets, the recommended workflow combines WISeREP bulk downloads via `wiserep_api` [^430^], classification with SNID-SAGE or DASH, and feature extraction with `spectral_lines` [^486^] or SupSpec [^483^], yielding standardized feature vectors ready for ingestion into photometric classification models.

---

## 5. Space-based & Multi-wavelength Datasets

Ground-based surveys deliver the vast majority of supernova alerts, but several critical wavelengths and cadences are accessible only from above the atmosphere. Ultraviolet (UV) photometry below 3,000 Angstroms is fully blocked by the ozone layer; near-infrared (near-IR) windows at 1–2.5 μm suffer from strong telluric absorption; and continuous high-cadence monitoring without weather interruption is impossible from any single ground site. Space-based missions therefore fill indispensable niches in the ML training ecosystem: they provide UV spectral energy distributions (SEDs) that constrain dust extinction, high-cadence pre-explosion baselines that enable shock-breakout detection, and all-sky scanning that removes weather bias. This chapter surveys seven operational or recently completed space missions that have produced publicly available supernova datasets suitable for machine learning, concluding with an analysis of the remaining near-IR data gap that future facilities will address.

### 5.1 TESS

The Transiting Exoplanet Survey Satellite (TESS) was designed to detect transiting exoplanets around nearby stars, yet its 30-minute cadence full-frame images (FFIs) covering roughly 85% of the sky have proven to be a powerful resource for time-domain astrophysics [^1^][^2^]. TESS operates in a single broad red-optical bandpass (600–1000 nm) with a field of view of 24 x 96 degrees per sector. During the primary mission (Sectors 1–26), FFIs were recorded every 30 minutes; the extended mission from Sector 27 onward shortened this to 10 minutes, offering even finer temporal resolution for early-rise studies. The instrument reaches approximately 20th magnitude at 3-sigma significance when binned to 8-hour intervals and achieves ~1% photometric precision at TESS magnitude 14.

#### 5.1.1 MIT TessTransients Database

The primary curated access point for TESS supernova light curves is the MIT TessTransients database, maintained by the TESS team [^3^][^4^]. As of 2025, the database catalogs 10,584 total astrophysical transients of all types, of which 1,299 are confirmed supernovae with extracted light curves. The database is updated weekly using TICA High Level Science Product (HLSP) data from the Mikulski Archive for Space Telescopes (MAST).

The flagship supernova dataset is Fausnaugh et al. (2023), which reports 307 Type Ia SNe observed during TESS Years 1–4 [^3^]. This sample is complemented by Vallely et al. (2021), who present high-cadence observations of 22 core-collapse SNe, enabling rise-time measurements that are inaccessible from ground-based cadences [^2^]. Each light curve file is distributed as ASCII text containing Barycentric Julian Date (BJD), background-subtracted relative flux, flux error, quality flags, and calibrated TESS magnitude where available [^4^]. The published sample is binned to 8-hour intervals; raw FFI extraction at native cadence can be performed with tools such as `lygos`, `eleanor`, `TGLC`, or `TESSCut`.

#### 5.1.2 Unique Value for ML

TESS's principal ML contribution lies in early-time light curve morphology. The 30-minute (and now 10-minute) cadence captures the first hours to days of a supernova explosion with temporal resolution that no ground survey can match. Fausnaugh et al. (2023) measured a mean rise time of 15.7 +/- 3.5 days for their 307 SNe Ia sample and tested the fireball model prediction of a power-law rise index beta=2.0, finding significant diversity that encodes information about progenitor radius and companion interaction [^3^]. The detection of flux excess above a simple power-law rise, as seen in SNe such as 2018oh and 2017cbv, provides a discriminant between single-degenerate and double-degenerate progenitor channels. For ML classifiers, TESS-derived features—including the power-law index beta, rise curvature, and flux excess amplitude—can be concatenated with ground-based multi-color photometry to improve early-time classification accuracy.

#### 5.1.3 Data Access

Individual light curves are accessible via a simple URL pattern: `https://tess.mit.edu/public/tesstransients/light_curves/lc_2022sfe_cleaned`, where "2022sfe" is replaced with the IAU designation. Bulk downloads are available through a dedicated page or a version-controlled GitHub repository (`mmfausnaugh/lc_bulk`). The `tess-point` Python tool identifies which TESS sector covered a given coordinate, enabling programmatic cross-matching with ground-based alert streams.

### 5.2 Kepler/K2

The Kepler Space Telescope delivered continuous 30-minute cadence photometry with a stability of 10–100 parts per million, producing what remain the highest-quality extragalactic supernova light curves ever obtained [^5^][^6^]. The Kepler bandpass spans 430–890 nm, similar to the Johnson-Cousins V+R composite. Unlike TESS, Kepler provided uninterrupted month-long baselines with no day-night gaps, enabling detection of sub-hour transient phenomena.

#### 5.2.1 Kepler Extragalactic Survey (KEGS)

The Kepler Extragalactic Survey (KEGS), led by Peter Garnavich and Robert Olling, monitored approximately 500 galaxies during the prime Kepler mission [^5^]. The sample is modest—23 SNe in total across Kepler and K2 combined—but the data quality is extraordinary. Olling et al. (2015) published three SNe Ia with pre-explosion baseline coverage, while Garnavich et al. (2016) reported the first visible-light detection of shock breakout in Type II-P supernovae (KSN 2011a and KSN 2011d), measuring progenitor radii of 280 and 490 solar radii respectively [^5^]. These observations provide the only direct empirical constraints on the radii of red supergiant SN progenitors.

The K2 extension, particularly Campaign 16 (December 2017–February 2018), targeted approximately 50 times more galaxies than KEGS through the K2 Supernova Cosmology Experiment [^6^]. The most extensively studied K2 supernova is SN 2018oh (ASASSN-18bt), a Type Ia at 52.7 Mpc that exhibited a two-component early rise interpreted as evidence of companion interaction [^6^].

#### 5.2.2 Data Access

All Kepler/K2 data are archived at MAST and accessible through the `lightkurve` Python package. For supernova work, Target Pixel Files (TPFs) are the preferred product because they allow custom aperture photometry and difference imaging. The K2 mission suffered from pointing drift of ~4 arcseconds due to its two-wheel control mode, making image subtraction a necessary step in most analyses. The `lightkurve` workflow—search, download TPF, apply custom aperture, and extract light curves—enables reproduction of published K2 SN photometry in a few lines of Python.

#### 5.2.3 Unique Science for ML

Kepler/K2 data are unique in providing pre-explosion baselines and continuous shock-breakout coverage. For ML models, the pre-explosion flux constraint eliminates one of the largest systematic uncertainties in rise-time fitting: the unknown explosion epoch. K2's shock-breakout light curves also serve as training templates for identifying similar events in lower-cadence data. However, the small sample size (~23 SNe total) limits the statistical power of purely Kepler-based classifiers; these data are best used as augmentation features rather than primary training sets.

### 5.3 Swift/SOUSA

The Neil Gehrels Swift Observatory's UltraViolet/Optical Telescope (UVOT) provides the largest homogeneous sample of UV supernova light curves from any single instrument [^7^][^8^]. The 30-cm modified Ritchey-Chretien telescope carries a photon-counting detector with six broadband filters spanning 1,928 to 5,468 Angstroms: UVW2, UVM2, UVW1, U, B, and V. Swift's rapid Target of Opportunity response (typically within hours) enables early-time UV observations that ground-based surveys cannot replicate.

#### 5.3.1 MAST HLSP Archive

The Swift Optical/Ultraviolet Supernova Archive (SOUSA), led by Peter Brown at Texas A&M, contains processed UVOT photometry for 253 supernovae of all major types [^8^][^9^]. All data have been reprocessed with Breeveld et al. (2011) zeropoints and time-dependent sensitivity corrections, ensuring internal consistency across the 2005–2024 temporal baseline. Each supernova typically has photometry in 3–6 filters, creating multi-color SEDs at epochs ranging from days to weeks after explosion.

SOUSA data products are distributed at two levels [^8^]: image products hosted on MAST in FITS format (summed images with and without the supernova), and light curve products available as ASCII/CSV files from the SOUSA website. The full tarball of 270+ SNe can be downloaded directly. For researchers requiring photometry from custom apertures, the HEASoft `uvotsource` tool performs aperture photometry on UVOT images with user-defined source and background regions.

#### 5.3.2 UV Data for Dust Extinction and Color Evolution

The UV wavelength regime is critically important for ML classifiers because it provides strong discriminatory power between supernova types and constrains dust extinction independently of optical color measurements. Brown et al. (2009) established that SNe Ia show homogeneous UV colors while core-collapse SNe evolve rapidly in the UV, enabling type separation from color-color diagrams alone [^7^]. Devarakonda et al. (2022) extended this work to 97 SNe Ia, demonstrating correlations between UV and optical light curve parameters that can be used to cross-validate photometric classifiers [^10^]. The UVW2-V color differentiates SNe Ia from core-collapse events at early times, while UVW1-U tracks the UV decay rate and identifies UV-bright subtypes such as 91T-like and super-Chandrasekhar events [^7^][^10^]. For cosmological ML applications, UV data provide the leverage needed to separate intrinsic color variations from dust reddening, reducing the systematic uncertainty in distance estimates.

### 5.4 GALEX

The Galaxy Evolution Explorer (GALEX) mission, operational from 2003 to 2013, provided UV imaging in two bands: Far-UV (FUV: 1,344–1,786 Angstroms) and Near-UV (NUV: 1,771–2,831 Angstroms) [^11^][^12^]. Unlike Swift's pointed observations, GALEX scanned large areas of the sky repeatedly, building up time-domain coverage that includes serendipitous observations of thousands of supernovae. The gPhoton database at MAST hosts approximately 130 TB of photon-level data with time resolution of 5 milliseconds, comprising roughly 1.1 trillion sky-projected photon events [^11^].

#### 5.4.1 gPhoton2 Pipeline

The original gPhoton software enabled extraction of calibrated light curves from GALEX photon data, but processing speed limited its utility for large samples. The updated gPhoton2 pipeline, developed by Million Concepts, delivers 1–3 orders of magnitude faster processing with improved calibration and automatic light curve generation at user-defined temporal resolution [^12^]. The pipeline can be invoked from the command line or Python API and produces 30-second binned light curves, images, and photon lists from raw GALEX telemetry. Installation follows standard `git clone` and conda environment setup; execution requires only the target GALEX eclipse number and desired band.

#### 5.4.2 GALEX Supernova Catalog

Milne et al. (2010) compiled UV light curves for approximately 1,080 SNe Ia using a combination of GALEX and Swift data, creating the largest UV SN Ia sample to date [^11^]. More recently, the 1UVA catalog (2024) extended time-domain coverage to roughly seven times the original GALEX Time-Domain Survey area by mining 385 NUV fields with more than 10 visits each [^13^]. GALEX wavelengths extend below Swift's UVW2 filter (1,928 Angstroms), probing the regime where line blanketing and circumstellar interaction produce the strongest spectral signatures. For ML training, GALEX data provide historical UV baseline photometry that can be cross-matched with ground-based optical light curves to build bolometric SEDs and constrain extinction corrections from the UV through the optical.

### 5.5 Gaia Alerts

The Gaia Photometric Science Alerts (GSA) system provides an all-sky transient survey with two unique capabilities: sub-arcsecond spatial resolution and low-resolution BP/RP spectra at every observing epoch [^14^][^15^]. Gaia scans the entire sky approximately once per month with two fields of view separated by 106.5 degrees, delivering G-band photometry (330–1,050 nm) at ~1% precision for sources as faint as G=13 and ~3% precision at G=19.

#### 5.5.1 Alert Statistics and Spectroscopic Coverage

Through the end of 2024, Gaia has published 10,785 alerts (updated from the 10,765 reported through 2019 in Hodgkin et al. 2021) [^15^]. Alerts are published at a rate of approximately 12 per day. The classification rate stands at roughly 25%, biased toward supernovae because follow-up campaigns prioritize these events. Critically, every alert includes BP (330–680 nm, R~100) and RP (640–1,000 nm, R~100) spectra at every epoch, making Gaia the only space-based survey that provides spectral information for all transient detections [^15^][^17^].

#### 5.5.2 Real-Time Detection and Southern Sky Coverage

Gaia's scanning mode provides continuous all-sky coverage including the Galactic plane, which most ground-based time-domain surveys avoid. The southern sky advantage is particularly important for supernova studies because the southern celestial hemisphere contains the Large Magellanic Cloud, the nearest active star-forming environment, and deep extragalactic fields such as Chandra Deep Field-South and the Dark Energy Survey region. The GaiaX alert stream provides programmatic access to alert data in CSV format, enabling real-time integration with ML classification pipelines [^15^].

#### 5.5.3 BP/RP Spectra for Classification

The BP/RP spectra, though low in resolution (R~100), provide classification information that is orthogonal to photometric light curve shape. Blagorodnova et al. (2014) demonstrated that most major supernova types can be recognized from BP/RP-like spectra alone with low confusion down to G=19 magnitude [^17^]. Simulations show that the GS-TEC (Gaia Transient Event Classifier) can estimate redshift from spectral features and determine epoch relative to peak brightness. For ML applications, the spectral data at each epoch enable construction of time-resolved color indices that are more robust to dust extinction than single-epoch photometry. Data access is through the Gaia Science Alerts web interface (`gsaweb.ast.cam.ac.uk/alerts/`), which provides per-alert pages with downloadable CSV light curves, spectra in custom format, finding charts, and cross-matches to other transient catalogs. The Cambridge Photometric Calibration Server (CPCS) aggregates follow-up photometry from multiple ground-based telescopes in JSON format.

### 5.6 JWST and Hubble

The James Webb Space Telescope (JWST) and the Hubble Space Telescope (HST) extend supernova observations into the near-IR and mid-IR, probing high-redshift populations where rest-frame optical wavelengths are redshifted into the infrared. Together, these missions provide the only systematic samples of SNe at z>1, essential for training classifiers that will operate on Roman Space Telescope and Euclid data.

#### 5.6.1 JWST High-Redshift Transients

JWST's Near-Infrared Camera (NIRCam) and Near-Infrared Spectrograph (NIRSpec) have opened a new era in high-redshift supernova studies with sensitivity from 0.6 to 5.3 μm [^18^][^19^]. The JWST Advanced Deep Extragalactic Survey (JADES) has been the most productive program for transient science, discovering 53 transients in the GOODS-S field at redshifts from z=0.5 to z=4.4, corresponding to a transient density of approximately one per square arcminute per epoch [^18^][^19^]. Key discoveries include a spectroscopically confirmed SN Ia at z=2.9 (Pierel et al. 2024), a broad-lined Ic at z=2.83 (Siebert et al. 2024), and a UV-bright SN at z=3.6 (Coulter et al. 2025). Complementary treasury programs COSMOS-Web and PRIMER cover 133 square arcminutes—roughly five times the JADES-Deep area—at shallower depth (~28 AB mag), yielding 68 SNe with host photometric redshifts predominantly at 1<z<2 [^19^].

All JWST data are publicly available through MAST. Key program IDs for supernova research include 1180 and 3215 (JADES NIRCam imaging), 6541 (JADES transient follow-up with NIRSpec+NIRCam), 1727 (COSMOS-Web), and 1837 (PRIMER). Data products include multi-epoch multi-filter imaging in FITS format, prism spectra, template-subtracted difference images, and aperture photometry catalogs.

#### 5.6.2 HST Archive: CANDELS and CLASH

HST's CANDELS (Cosmic Assembly Near-infrared Deep Extragalactic Legacy Survey) and CLASH (Cluster Lensing And Supernova survey with Hubble) Multi-Cycle Treasury programs provided the first substantial sample of high-redshift SNe Ia with rest-frame optical-NIR photometry [^20^][^21^]. CANDELS covered five deep fields (GOODS-S/N, COSMOS, UDS, EGS) spanning ~0.25 square degrees, while CLASH observed 25 galaxy cluster fields plus 13 parallel fields. Observations were obtained with ACS (optical) and WFC3-IR (0.8–1.7 μm) at a cadence of approximately 50 days between epochs. Rodney et al. (2014) cataloged 65 SNe discovered in CANDELS out to z=2.5, while Riess et al. (2018) used the combined CANDELS+CLASH sample of 15 SNe Ia at z>1 (9 with reliable distance estimates) as a high-redshift anchor for Hubble constant measurements [^21^][^20^]. Photometry tables are published in the Riess et al. (2018) appendix and accessible through VizieR and MAST.

#### 5.6.3 Space-Based Mission Comparison

| Mission | SN Sample | Cadence | Wavelength Coverage | Unique ML Value | Data Access |
|:---|:---|:---|:---|:---|:---|
| TESS | 307 SNe Ia + 4,000+ transients [^3^] | 30 min (10 min extended) | 600–1000 nm, single band | Early-rise morphology; power-law index beta; companion interaction | MIT TessTransients API; CSV [^3^][^4^] |
| Kepler/K2 | 23+ SNe [^5^] | 30 min, continuous | 430–890 nm, single band | Pre-explosion baseline; shock breakout; progenitor radii | MAST; `lightkurve` Python package [^5^][^6^] |
| Swift/SOUSA | 253 SNe, 6 filters [^8^] | ~2 days (ToO: hours) | 1,928–5,468 Angstroms (UVW2/UVM2/UVW1/U/B/V) | UV-optical color evolution; dust extinction; SED fitting | MAST HLSP + SOUSA website; FITS + ASCII [^8^][^9^] |
| GALEX/gPhoton | 1,080 SNe Ia UV LCs [^11^] | Variable (days–weeks) | FUV (1,344–1,786 A) + NUV (1,771–2,831 A) | Photon-level time resolution; UV bolometric corrections | gPhoton2 @ MAST; Parquet/CSV [^11^][^12^] |
| Gaia Alerts | 10,785 alerts (through 2024) [^15^] | ~1 visit/month | G band (330–1,050 nm) + BP/RP spectra (R~100) | Low-res spectra at every epoch; all-sky; no weather bias | Gaia Science Alerts web; CSV + spectra [^15^][^17^] |
| JWST (JADES) | 53 transients (z=0.5–4.4) [^18^] | ~1 year between epochs | 6–9 NIRCam filters (0.6–5.0 μm) | First high-z SN NIR spectroscopy; rest-frame UV at z>2 | MAST; FITS [^18^][^19^] |
| HST (CANDELS+CLASH) | 65+ SNe (out to z=2.5) [^21^] | ~50 days | ACS optical + WFC3-IR (0.8–1.7 μm) | First large z>1 SN Ia sample; cosmological-quality photometry | MAST + VizieR; FITS + ASCII [^20^][^21^] |

The seven missions are complementary rather than overlapping. TESS and Kepler/K2 provide time-domain resolution; Swift, GALEX, and Gaia provide wavelength diversity (UV through optical) and spectral information; JWST and HST probe the high-redshift universe where rest-frame optical features shift into the near-IR. For an ML practitioner building a multi-wavelength classifier, the optimal strategy is to combine Swift UVOT colors with TESS early-rise parameters and Gaia BP/RP spectral slopes, using JWST/HST data as high-redshift validation samples.

### 5.7 The NIR Gap

Near-infrared observations are critical for supernova cosmology because NIR light curves exhibit reduced scatter in peak luminosity, are less affected by dust extinction, and provide direct access to the rest-frame optical emission of high-redshift SNe. Despite this importance, publicly available near-IR supernova datasets remain strikingly scarce compared to the wealth of optical and UV data. This gap has direct implications for ML model training: classifiers optimized on optical data alone will carry systematic biases when deployed on near-IR surveys such as Euclid and the Roman Space Telescope.

#### 5.7.1 The Scarcity of Public NIR Training Data

The primary source of real NIR photometry for SNe Ia is CSP DR3, which includes YJH-band observations for 120 of its 134 SNe (90% of the sample) [^166^]. This represents the largest homogeneous set of real NIR SN Ia light curves publicly available. However, 134 SNe is orders of magnitude smaller than the optical training sets from ZTF (hundreds of thousands of alerts) or even Swift (253 SNe with UV coverage). The next-largest real NIR dataset comes from Euclid Q1: serendipitous NISP (Near-Infrared Spectrometer and Photometer) measurements of 161 transients in the Y_E, J_E, and H_E bands (0.95–2.00 μm), obtained through single-epoch observations of the Euclid Deep Fields [^824^][^766^]. While the Q1 sample is not time-resolved, it represents the first statistically meaningful set of real NIR supernova photometry from a space-based mission and validates the detection efficiency of the NISP instrument for transient science.

#### 5.7.2 Simulated NIR Training Resources

Given the scarcity of real NIR data, simulated datasets are the primary resource for training NIR-ready classifiers. The Roman Hourglass simulation is the most comprehensive, providing 64,000+ transients across 10 types (including 21,700 SNe Ia) with simulated Y, J, H, and F band photometry at 5-day cadence, plus prism spectra for ~20% of the sample [^328^][^269^]. The Hourglass data are distributed as Parquet files on Zenodo and have already been used to train ParSNIP classifiers for Roman HLTDS science [^282^]. OpenUniverse2024 extends this with ~400 TB of matched Roman+Rubin imaging over 70 square degrees, enabling joint optical-NIR classifier development [^335^][^302^].

#### 5.7.3 Bridging the Gap: Current and Future Resources

| Source | Type | NIR Bands | SN Sample | Status | ML Limitations |
|:---|:---|:---|:---|:---|:---|
| CSP DR3 | Real | Y, J, H | 120 SNe Ia [^166^] | Publicly available | Small sample; low-z only (z<0.08) |
| Euclid Q1 | Real | Y_E, J_E, H_E | 161 transients [^824^] | Publicly available | Single-epoch; not time-resolved |
| Euclid DR1 | Real | Y_E, J_E, H_E | Projected ~5,000+ | Late 2026 | Multi-epoch; will enable proper light curves |
| Roman Hourglass | Simulated | Y, J, H, F | 21,700 SNe Ia [^328^] | Public (Zenodo) | Sim-to-real transfer required |
| OpenUniverse2024 | Simulated | Y, J, H, F | Thousands | Public (AWS S3) | Large volume (~400 TB); compute intensive |
| Roman HLTDS (2027+) | Real | Y, J, H, F | Projected 10,000s SNe Ia | Launch by May 2027 | Not yet available |
| JWST archival | Real | F090W–F444W | 53 transients [^18^] | Public (MAST) | Sparsely sampled; small area |

The near-IR data landscape presents a clear trajectory. Today, CSP DR3 and Euclid Q1 provide the only real NIR photometry suitable for ML training, but their combined sample of fewer than 300 transients is grossly inadequate for training deep learning classifiers. The Roman Hourglass simulation partially fills this gap with tens of thousands of simulated SNe Ia, yet the sim-to-real transfer problem documented in Chapter 7 means that classifiers trained purely on Hourglass data will likely experience 5–15% accuracy degradation when deployed on real Roman observations. Euclid DR1, expected in late 2026 with multi-epoch coverage over ~1,900 square degrees, will deliver the first large real NIR time-domain sample. The Roman HLTDS, launching by May 2027, is projected to discover thousands of high-z SNe Ia in the Y, J, H, and F bands with 5-day cadence, finally eliminating the NIR training gap. For ML practitioners preparing for this transition, the recommended strategy is to train classifiers jointly on Roman Hourglass (simulated NIR) and CSP DR3 (real low-z NIR), using domain adaptation techniques to bridge the simulated-to-real domain shift, and to validate on Euclid Q1/DR1 NISP photometry as the first real NIR test set at cosmological distances.

---

## 6. Compilation & Aggregated Datasets

Individual survey releases provide the raw material for supernova machine learning, but the field has matured through a parallel ecosystem of homogenized compilations that aggregate data from dozens of sources into analysis-ready collections. These compilations serve three distinct ML purposes: cosmology regression (distance modulus prediction), classification (type labeling across all supernova species), and anomaly detection (outlier discovery in heterogeneous populations). This chapter examines the principal compilations — from the all-inclusive Open Supernova Catalog to the precision-calibrated Pantheon+ sample — and provides a practical workflow for constructing unified training sets from multi-survey data.

### 6.1 Open Supernova Catalog

#### 6.1.1 Scope and Content

The Open Supernova Catalog (OSC) is the most comprehensive open repository for supernova data, containing **50,000+ supernovae and candidates** aggregated from several dozen sources including the astronomical literature, survey data releases, and secondary catalogs [^651^] [^659^]. Unlike the cosmology-focused compilations described later in this chapter, the OSC embraces supernovae of all types — thermonuclear (Type Ia), core-collapse (Type II, Ib, Ic, and subtypes), and exotic variants — alongside non-supernova contaminants such as active galactic nuclei (AGN) and stellar variables. This diversity makes it uniquely valuable for multi-class classification and anomaly detection tasks, even as it introduces significant data-quality heterogeneity.

The catalog stores data in a hierarchical JSON format with one file per supernova [^86^]. Each file contains photometric time series (when available), spectroscopic observations, metadata (coordinates, redshift, host galaxy association), and cross-references to discovery circulars. Approximately 12,000 objects have more than 10 photometric observations, while roughly 5,000 include at least one spectrum [^81^]. The remaining entries consist primarily of metadata-only records with discovery information and classification claims.

#### 6.1.2 Bulk Download and Repository Access

The OSC data are distributed through a GitHub organization (astrocatalogs) split across year-based repositories to accommodate GitHub's repository size limits [^89^]. Individual event JSON files are organized into repositories covering: pre-1990, 1990–1999, 2000–2004, 2005–2009, 2010–2014, 2015–2019, and 2020–present. For bulk acquisition, the most efficient path is a compressed tarball (sne.tar.lzma, 379 MB) available via the SNAD project mirror at snad.space [^81^] [^661^]. This archive contains all JSON files as a single download, avoiding the overhead of cloning multiple GitHub repositories.

#### 6.1.3 Programmatic Queries

For targeted queries, the AstroCats API (api.astrocats.space) supports programmatic access to individual supernova records without requiring a local mirror. The underlying AstroCats framework can also be installed locally for full catalog reproduction, though the initial import run requires approximately one day of processing time. For ML workflows that require the full catalog, parsing the JSON files directly is straightforward:

```python
import json, glob
for json_file in glob.glob('sne-*/SN*.json'):
    with open(json_file) as f:
        sn_data = json.load(f)
    photometry = sn_data.get('photometry', [])
    spectra = sn_data.get('spectra', [])
    claimed_type = sn_data.get('claimedtype', [])
```

The SNooPy light-curve fitting package can also import OSC data directly, providing an alternative entry point for researchers already using that tool.

#### 6.1.4 Strengths and Weaknesses for ML

The OSC's principal strength for ML lies in its scale and diversity. No other compilation matches its breadth of supernova types, making it the default choice for classification tasks that must distinguish between thermonuclear and core-collapse events or identify rare subtypes. The catalog has been successfully used for automated anomaly detection: the SNAD pipeline downloaded 45,162 objects from a 2018 snapshot, selected approximately 2,000 with sufficient photometry, and applied Gaussian Process interpolation followed by t-SNE dimensionality reduction and Isolation Forest outlier detection, identifying 81 anomalies of which 27 were confirmed as peculiar supernovae, AGN, or stellar variables [^690^] [^694^].

The corresponding weakness is data heterogeneity. Photometric observations come from hundreds of different telescopes and instruments with inconsistent calibration, filter definitions, and reporting formats. Many objects have sparse time sampling with fewer than 5 photometric points, making light-curve fitting unreliable. No uniform quality flags exist, so ML practitioners must implement their own filtering criteria — typically requiring a minimum number of observations, signal-to-noise thresholds, and coverage in multiple photometric bands.

### 6.2 Pantheon+

#### 6.2.1 Sample Definition and Survey Coverage

Pantheon+ represents the definitive cosmological supernova compilation, comprising **1,701 light curves of 1,550 distinct Type Ia supernovae** drawn from **18 different surveys** spanning three decades [^451^]. The sample was assembled by the SH0ES (Supernovae and H0 for the Equation of State of dark energy) collaboration specifically for precision cosmology, combining low-redshift anchors (z < 0.1) from the Carnegie Supernova Project and CfA surveys, intermediate-redshift SNe from SDSS-II, and high-redshift events from SNLS, DES, and HST programs. The primary analysis papers are Scolnic et al. 2022 (ApJ 938:110) and Brout et al. 2022 (ApJ 938:111) [^451^] [^536^].

The repository is organized into 18 survey-specific subdirectories, each containing light-curve files in both SNANA text format and FITS binary tables [^125^] [^662^]. The text format places metadata (supernova name, coordinates, host galaxy position, Milky Way extinction, heliocentric and CMB-frame redshifts, peculiar velocity) in a header block, followed by photometric data columns (MJD, filter, calibrated flux, flux uncertainty, magnitude, magnitude uncertainty). All flux measurements share a common zero-point of 27.5 mag, enabling direct comparison across surveys.

#### 6.2.2 Cosmology Data Products and Covariance Matrices

Beyond raw photometry, Pantheon+ provides the essential data products for cosmological ML. The 4_DISTANCES_AND_COVAR directory contains the primary distance moduli and redshifts in Pantheon+SH0ES.dat, along with a full statistical-plus-systematic covariance matrix in compressed format [^664^]. Light-curve fit results from SALT2/SALT3 are available as .FITRES files, and calibration variation files enable systematic uncertainty studies. Host galaxy properties — stellar mass for the full sample, plus star formation rate and morphology for the low-redshift subset — are included as global metadata.

The covariance matrix construction is documented in a third-party analysis repository, which includes a demonstration notebook (how_to_covariance.ipynb) showing proper matrix usage in Python [^452^]. For ML practitioners, these covariance matrices enable principled treatment of correlated uncertainties in loss functions — a significant advantage over compilations that provide only point estimates.

#### 6.2.3 Calibration Evolution: SuperCal to Dovekie

Pantheon+ has undergone three generations of cross-calibration. The original SuperCal methodology (2015) tied 25 photometric systems using Pan-STARRS stellar photometry [^508^]. This was superseded by Fragilistic in the Pantheon+ analysis, which simultaneously solved for 105 filter offsets with an associated covariance matrix [^536^]. The most recent update, Dovekie (2025), provides an open-source recalibration framework using DA white dwarfs and Gaia photometry; Dovekie found systematic photometric uncertainty of 0.016 mag for a flat wCDM cosmology, improving the Pantheon+ calibration systematic by a factor of approximately 1.5 [^706^]. The Dovekie code is publicly available at github.com/bap37/Dovekie, making it possible for researchers to add new surveys to the cross-calibration framework — a critical capability as new data from ZTF, Rubin, and other facilities become available.

#### 6.2.4 ML Applications

For machine learning, Pantheon+ is best suited to cosmology regression tasks: predicting distance modulus from redshift, light-curve shape, and color; quantifying standardization residuals; and propagating systematic uncertainties through the inference pipeline. The pre-homogenized nature of the sample means it is **not** suitable for raw classification tasks — the objects have already been spectroscopically confirmed as Type Ia and quality-selected for cosmology. However, the covariance matrices and calibration documentation make it uniquely powerful for uncertainty-aware ML, where correlated errors must be propagated into model predictions.

### 6.3 Union3 and UNITY1.5

Union3 is the latest compilation from the Supernova Cosmology Project (SCP), comprising **2,087 Type Ia supernovae from 24 distinct datasets** — approximately one-third larger than Pantheon+ [^189^]. The sample is analyzed with the UNITY1.5 (Unified Nonlinear Inference for Type-Ia cosmologY) Bayesian hierarchical framework [^624^], which represents a fundamentally different statistical approach than the frequentist methodologies used in Pantheon+.

#### 6.3.1 Bayesian Framework and Data Products

UNITY1.5 implements a Bayesian hierarchical model using Hamiltonian Monte Carlo via Stan [^623^] [^626^]. The framework simultaneously models outlier contamination, selection effects (Malmquist bias), light-curve shape and color populations, standardization relations, and unexplained dispersion. A distinctive feature is that it models the underlying supernova population *before* selection effects are applied, then marginalizes over survey depth distributions — in contrast to traditional approaches that apply selection corrections post-hoc. The framework also recovers peculiar velocity fields, providing a posterior distribution for every model parameter.

#### 6.3.2 Data Availability and Access

As of early 2025, the full unbinned Union3 catalog has **not** been publicly released [^658^]. Only binned or compressed data products are available: spline-interpolated distance moduli at 22 redshift nodes, a Gaussian approximation to the posterior (location plus Hessian), and the UNITY1.5 framework code for forward-modeling. The binned release is hosted at github.com/rubind/union3_release, with an alternative access point through the Cobaya sampler's sn_data repository [^657^] [^658^].

This data availability pattern has important implications for ML. The binned format precludes per-supernova analysis — individual light curves, SALT3 fit parameters, and distance estimates are not directly accessible. Instead, cosmological constraints must be derived by implementing custom models within the UNITY framework. The full catalog release, which will include individual supernova data and SALT3 fitted parameters, is anticipated in future updates; ML practitioners should monitor the GitHub repository for releases.

### 6.4 JLA

The Joint Light-Curve Analysis (JLA) combines SDSS-II and SNLS Type Ia supernova observations with low-redshift samples, totaling **740 spectroscopically confirmed SNe Ia** with high-quality light curves [^652^]. Published by Betoule et al. 2014, JLA was the standard cosmology compilation for the decade preceding Pantheon+ and remains widely used for method validation and teaching.

Data access is available through CDS/VizieR at J/A+A/568/A22, with covariance matrices distributed as a separate compressed archive [^452^]. The SNData Python package provides programmatic access via the `Betoule14` module [^652^], which handles download, caching, and format conversion automatically. JLA uses SALT2.4 light-curve fitting (superseded by SALT3 in Pantheon+) and calibration based on the SuperCal methodology (later improved by Fragilistic and Dovekie). Both JLA and Pantheon+ employ the Tripp estimator standardization: mu = mB + alpha*x1 - beta*c - M0, though with different training samples and priors.

For ML research, JLA offers two practical advantages over its successors. First, the smaller dataset size (740 vs. 1,701 SNe) and simpler structure make it ideal for rapid prototyping and teaching — a full cosmology analysis pipeline can be executed in minutes rather than hours. Second, the well-documented covariance construction and extensive validation literature provide a reliable baseline against which new ML methods can be benchmarked. The principal caveat is that JLA's photometric calibration has been superseded; cosmology results will differ systematically from Pantheon+ by calibration offsets that must be accounted for in any cross-compilation analysis.

### 6.5 Other Compilations

Beyond the four major compilations described above, several additional catalogs serve specialized roles in the ML ecosystem.

#### 6.5.1 Asiago Catalog

The Asiago Supernova Catalog is the longest-running dedicated supernova catalog, maintaining records for all supernovae observed since 1885 along with their parent galaxies [^593^] [^596^]. The dynamic version supersedes the 1999 publication by Barbon et al. and is updated regularly. Data are available through CDS (cdsarc.cds.unistra.fr/ftp/cats/B/sn) and mirrored by HEASARC at NASA's Goddard Space Flight Center [^142^] [^596^]. The catalog contains over 11,000 supernova entries with host galaxy identifications, redshifts, classification types, and cross-references to International Astronomical Union Circulars (IAUCs). Parent galaxy properties are homogenized across multiple source catalogs (RC3, UGC, PGC, MCG, ESO). For ML applications, the Asiago Catalog is primarily useful for host galaxy correlation studies and metadata enrichment — it contains minimal photometric data but provides authoritative host identifications that can be cross-matched with survey photometry.

#### 6.5.2 Sternberg Astronomical Institute Catalog

The Sternberg Astronomical Institute (SAI) Catalog contains 2,991 extragalactic supernovae discovered from 1885 through December 2004, with host galaxy data compiled from multiple astronomical catalogs [^354^]. Available through the NASA Data Portal and CDS Table II/256, this is a static catalog that has not been updated since 2004. Its primary value lies in historical completeness for the pre-digital era; for contemporary ML work, the Asiago dynamic catalog or OSC provide superior coverage.

#### 6.5.3 DES-SN5YR and CSP

The DES-SN5YR sample from the Dark Energy Survey comprises approximately 1,820 SNe Ia used in cosmological analysis [^344^]. The recent DES-Dovekie reanalysis provides updated calibration and SALT3 model retraining (SALT3.DOVEKIE and SALT3.DOVEKIE-SYS) [^475^]. The repository at github.com/des-science/DES-SN5YR includes scene-modeling photometry, 25 mock simulations, classification probabilities for 1,635 SNe, and distance covariance matrices. For photometric classification tasks, the DES sample offers deep, well-characterized photometry alongside extensive simulation-based training data.

The Carnegie Supernova Project (CSP) provides some of the highest-precision low-redshift photometry available, with DR3 containing 134 SNe observed in natural-system optical (ugriBV) and near-infrared (YJH) bands [^166^] [^629^]. CSP data serve as the low-redshift anchor for most cosmological analyses and are accessible through the sndata Python package.

| Compilation | SNe Count | Surveys / Sources | Primary Format | Cosmology-Ready | Best ML Use Case |
|:---|:---|:---|:---|:---|:---|
| Open Supernova Catalog | 50,000+ (all types) [^651^] | 100+ literature sources | JSON per-SN [^86^] | No | Multi-type classification; anomaly detection |
| Pantheon+ | 1,701 SNe Ia [^451^] | 18 surveys | SNANA FITS + text [^125^] | Yes (SALT2/SALT3) | Cosmology regression; uncertainty-aware ML |
| Union3 / UNITY1.5 | 2,087 SNe Ia [^189^] | 24 datasets | Binned (nodes) [^657^] | Partial (binned only) | Bayesian cosmology inference |
| JLA | 740 SNe Ia [^652^] | SDSS-II, SNLS, low-z | Individual LC + covmat [^452^] | Yes (SALT2.4) | Baseline cosmology; teaching; validation |
| DES-SN5YR | ~1,820 SNe Ia [^344^] | DES 5-year | SMP photometry + FITS | Yes (SALT3.DOVEKIE) | Photometric classification; high-z analysis |
| Asiago Catalog | 11,000+ SNe [^593^] | 1885–present (all sources) | ASCII tables [^142^] | No | Host galaxy correlations; metadata enrichment |
| SAI Catalog | 2,991 SNe [^354^] | 1885–2004 | ASCII (CDS II/256) | No | Historical completeness |
| CSP DR3 | 134 SNe [^166^] | CSP (Las Campanas) | Individual tar.gz archives | Yes (natural system) | Low-z anchor; NIR studies; template building |

This comparison highlights a fundamental division in the compilation landscape. The cosmology-ready samples (Pantheon+, JLA, DES-SN5YR, CSP) provide homogeneous, well-calibrated photometry with standardized light-curve parameters but contain only Type Ia supernovae that have already passed quality cuts. The all-type catalogs (OSC, Asiago) offer breadth across supernova species but lack the calibration precision and uniform photometric processing needed for distance-scale ML. Union3 occupies a middle ground — the largest spectroscopically confirmed Ia compilation — but its binned-only release format currently limits per-supernova ML applications. Practitioners should select compilations based on task requirements: cosmology regression demands Pantheon+ or JLA, multi-type classification requires the OSC, and host-galaxy correlation studies benefit from cross-matching Asiago metadata with survey photometry.

### 6.6 Building Unified Training Sets

Compilations reduce the number of data sources, but significant work remains to produce ML-ready training sets. This section describes the practical toolchain for homogenizing multi-survey data and the challenges that must be addressed in the process.

#### 6.6.1 The SNData Python Package

The SNData package provides the most convenient unified interface for accessing multiple supernova surveys programmatically [^409^] [^635^]. It supports CSP (DR1, DR3), JLA (Betoule14), DES, SDSS, SNLS, and additional surveys on request. Data are automatically downloaded to a local cache, parsed into standardized Astropy tables, and registered with SNCosmo for filter transmission curves.

```python
from sndata.csp import DR3
from sndata.jla import Betoule14

dr3 = DR3()
dr3.download_module_data()
for sn in dr3.iter_data():
    # Each sn is a standardized Astropy table
    print(sn.meta, sn['time'], sn['magnitude'])
```

The standardized format eliminates much of the manual parsing code that would otherwise be required when working with survey-specific file formats. However, SNData does not perform photometric homogenization — it provides access to the raw data as published, leaving calibration and systematization to the user.

#### 6.6.2 SNCosmo for Simulation, Fitting, and Format Conversion

SNCosmo is the primary Python library for supernova cosmology analysis, providing model fitting, simulation, and built-in access to standard datasets [^33^] [^650^]. Its built-in models include SALT2, SALT3, MLCS2k2, Hsiao, Nugent, and SNANA-compatible templates. SALT3 is fully integrated from SNCosmo version 2.12.1 onward [^720^] [^724^]; the SALT3 model was trained on 1,083 SNe with 1,207 spectra — a sample 2.5 times larger than SALT2.JLA — covering a wavelength range of 2,000–11,000 Angstroms, which extends 1,800 Angstroms redder than SALT2 [^721^] [^723^]. The training code is publicly available at saltshaker.readthedocs.io.

For ML workflows, SNCosmo serves three critical functions. First, it converts photometric data between formats (SNANA FITS, ASCII tables, Astropy tables). Second, it fits light-curve models to produce standardized features (light-curve shape x1, color c, peak magnitude mB) that serve as input features for cosmology regression models. Third, it generates synthetic light curves from models, enabling augmentation of real training data with simulated samples:

```python
import sncosmo
model = sncosmo.Model(source='salt3')
model.set(z=0.5, t0=55000., mwebv=0.02)
# Fit to observed data:
# result, fitted_model = sncosmo.fit_lc(data, model, ['z', 't0', 'x0', 'x1', 'c'])
```

#### 6.6.3 Homogenization Challenges

Combining data from multiple surveys requires addressing seven fundamental calibration challenges [^508^] [^536^] [^667^]. Filter transmission curves differ across telescopes, with effective wavelengths varying by 10–100s of Angstroms for nominally identical bands. Photometric systems (AB, Vega, and natural) use different zero-point definitions. Spatial non-uniformity in filter throughput across focal planes can produce radial variations up to 8 mmag in Pan-STARRS. Temporal drift from mirror degradation and dust accumulation changes throughput over multi-year survey durations. Atmospheric extinction varies with airmass and weather. Fundamental flux standards (such as BD+17) exhibit luminosity variations of approximately 4% over decadal timescales. Color transformations between photometric systems introduce systematic errors that propagate nonlinearly into distance measurements.

These challenges have measurable impact on cosmological inference. Calibration uncertainty is the largest systematic contributor to SN Ia cosmology, accounting for 30–50% of the total systematic budget [^721^]. Inter-survey calibration uncertainty of 25 mmag shifts the matter density parameter Omega_M by 0.04 and the dark energy equation-of-state parameter w by −0.17 [^647^]. Filter zero-point perturbations of 0.01 mag can shift w by 0.006–0.009, and SALT model training amplifies calibration errors into distance measurements by up to a factor of 6 [^536^] [^706^].

For ML practitioners, the implications are direct. Training on heterogeneous data without calibration awareness introduces survey-dependent biases that degrade generalization. Feature normalization across surveys requires knowledge of photometric systems and zero-points. When covariance matrices are available (Pantheon+ provides them), they should be incorporated into loss functions through weighted least squares or heteroskedastic loss terms. Bias corrections in simulation-based training depend on accurate calibration in the training sample — an insight that connects to the broader sim-to-real challenges discussed in Chapter 7.

#### 6.6.4 Recommended Workflow

The following workflow synthesizes the tools discussed above into a practical pipeline for building unified training sets from compilation data:

| Stage | Tool / Package | Action | Output |
|:---|:---|:---|:---|
| 1. Data acquisition | SNData, GitHub releases | Download survey-specific subsets | Raw photometry + metadata |
| 2. Format conversion | SNCosmo | Parse SNANA FITS, JSON, ASCII into Astropy tables | Standardized data structures |
| 3. Calibration registration | SNCosmo bandpass library | Register filter curves, apply zero-point corrections | Calibrated fluxes in known systems |
| 4. Light-curve fitting | SNCosmo + SALT3 | Fit x1, c, mB (or equivalent) per supernova | Standardized feature vectors |
| 5. Quality selection | Custom cuts | Minimum N_obs, S/N, phase coverage, fit quality | Clean training sample |
| 6. Covariance propagation | numpy, scipy | Incorporate STAT+SYS covariance into ML loss | Uncertainty-aware model training |
| 7. Cross-validation | scikit-learn | Stratified by survey to test generalization | Survey-robust performance estimates |

The critical quality criteria at Stage 5 depend on the ML task. For cosmology regression, cuts typically require at least 5 photometric points per light curve, a valid SALT fit with reduced chi-squared below 5, and coverage spanning the rise and fall of the B-band peak. For classification, the requirements are less stringent — as few as 3 points in a single filter can support photometric typing with deep learning architectures — but training samples must include representative coverage across all target classes. Stage 6, covariance propagation, is unique to precision cosmology tasks; for classification and anomaly detection, where per-point uncertainties are smaller relative to class separation, simple inverse-variance weighting is often sufficient.

The survey-stratified cross-validation in Stage 7 deserves emphasis. Because each survey operates in a distinct redshift and brightness regime, random cross-validation overestimates performance by allowing training and test sets to share survey-specific systematics. Stratifying by survey ensures that the model generalizes across calibration systems, providing a more realistic estimate of real-world performance when the model is applied to data from facilities not represented in the training sample — a situation that will be common as Rubin begins operations with novel filter curves and calibration chains.

---

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

---

## 8. Alert Brokers & Real-time ML

### 8.1 The Broker Ecosystem

The Vera C. Rubin Observatory's Legacy Survey of Space and Time (LSST) will generate up to 10 million alerts per night at full operational capacity [^948^], with each alert packet carrying approximately 82 KB of structured data including 12 months of photometric history, 30×30 pixel postage-stamp cutouts, and cross-matched catalog associations [^210^]. On February 24, 2026, Rubin issued its first public alerts — 800,000 notifications distributed globally within approximately two minutes of image readout [^796^]. This event marked the transition from a decade of broker development on precursor surveys to live operations at an unprecedented scale.

Alert brokers are software systems that ingest, process, classify, and redistribute these streams. The Rubin project formally selected seven "full-stream" community brokers that receive the complete alert feed: ALeRCE, AMPEL, ANTARES, Babamul, Fink, Lasair, and Pitt-Google [^44^]. These brokers serve distinct scientific communities and employ heterogeneous ML architectures — from convolutional neural networks to variational autoencoders — producing classification taxonomies that are not standardized across platforms [^210^]. Two additional "downstream" brokers, SNAPS (Solar System Notification Alert Processing System) and POI Broker (Point of Interest), receive filtered subsets from full-stream partners rather than the complete feed [^44^]. SNAPS specializes in Solar System objects, ingesting alerts tagged as moving sources from its upstream partner ANTARES [^713^], while POI Broker focuses on variable star light curve analysis, receiving high-amplitude variable star candidates from ANTARES for feature extraction and classification [^947^].

What brokers provide extends well beyond raw alert forwarding. Each broker applies ML classifiers trained on historical survey data, cross-matches alerts against astronomical catalogs (Gaia, Pan-STARRS1, AllWISE, SDSS, and proprietary compilations), computes derived features (light curve statistics, host galaxy associations, variability indices), and exposes the enriched data through programmatic interfaces [^210^]. The seven full-stream brokers collectively process the ZTF alert stream of approximately 300,000 alerts per night as a precursor rehearsal [^815^], with Fink alone having processed over 180 million alerts since 2019 [^60^]. All seven demonstrated sub-hour classification latency during the Extended LSST Astronomical Time-series Classification Challenge (ELAsTiCC) in 2022–2023 [^334^], establishing operational readiness for Rubin-scale throughput.

A functional taxonomy of the broker ecosystem distinguishes three tiers. **Full-stream brokers** (7) ingest every alert and are responsible for the computationally intensive work of real-time classification and cross-matching. **Downstream brokers** (2) subscribe to filtered subsets matched to specific science domains. **Science brokers** — a category that includes marshal systems like SkyPortal and the TOM Toolkit — sit at the end of the pipeline, ingesting broker-classified alerts to coordinate follow-up observations [^733^]. For ML practitioners, this layered architecture means that classification features, probability scores, and contextual annotations from multiple brokers can be queried as pre-computed features, amortizing the computational cost of running deep learning models across the entire alert stream.

### 8.2 Broker-by-Broker ML Capabilities

**ALeRCE.** The Automatic Learning for the Rapid Classification of Events (ALeRCE) broker, led by a Chilean consortium, operates the most developed hierarchical taxonomy among the seven brokers [^684^] [^728^]. Its classification pipeline combines a stamp classifier and a light curve classifier into a two-level decision system. The stamp classifier applies a Convolutional Neural Network (CNN) to the first-detection image cutouts (science, reference, and difference images) together with alert metadata, achieving approximately 94% accuracy on a balanced test set across five top-level classes: AGN, SNe, Variable Stars, Asteroids, and Bogus [^685^]. Between June 2019 and February 2021, this classifier identified 6,846 supernova candidates, of which 971 were spectroscopically confirmed, with 70% of reported SNe occurring within one day of first detection [^685^].

The light curve classifier uses a Balanced Random Forest (BRF) with 152 features extracted from ZTF *g*- and *r*-band light curves, organized into a hierarchical taxonomy with three top-level classes (Transient, Stochastic, Periodic) and five transient subclasses (SN Ia, SN Ib/c, SN II, SLSN, TDE) [^698^] [^528^]. The top-level F1-score reaches 0.97, with 100% SN completeness [^698^]. ALeRCE's transient taxonomy was expanded in 2025 to include Tidal Disruption Events (TDEs) [^698^]. The broker provides a unified Python client (`alerce`) supporting multi-survey queries for both ZTF and LSST data, with capabilities for light curve retrieval, probability queries, stamp access, and cone searches [^701^].

**Fink.** Fink is a community-driven broker built on Apache Spark and centered at the French National Centre for Scientific Research [^48^]. Its distinguishing ML contributions are two-fold: the deployment of the SuperNNova deep learning framework for supernova classification, and the pioneering application of active learning to early SN Ia identification [^729^] [^47^]. SuperNNova, implemented as an RNN-based photometric classifier, runs in two modes within Fink: SN1 (binary SN Ia vs. non-Ia) and SN2 (general supernova classification). The SN1 model achieves greater than 98% accuracy on simulated training data and produces classifications a median of 6 days before observed peak brightness [^729^].

Fink's active learning pipeline for early SN Ia discovery uses feature extraction followed by Random Forest classification with uncertainty sampling [^47^] [^56^]. Averaged over 100 realizations, the system achieves approximately 89% purity and 54% efficiency, with an accuracy of 0.97 for the best-performing model [^47^]. During live deployment from November 2020 to October 2021, 535 candidates were reported to the Transient Name Server (TNS), of which 459 (86%) received spectroscopic confirmation as SNe Ia [^56^]. An active learning loop operated during 2023–2024 identified 177 follow-up candidates, with the uncertainty-sampling strategy outperforming random selection after approximately 60 new objects and saving an estimated 1.5 nights of observation compared to 5.3 nights under alternative approaches [^726^] [^689^]. Fink organizes its science output into more than 60 science topics, accessible through a REST API, a Python Kafka client (`fink-client`), and a Data Transfer service designed for bulk historical downloads [^686^] [^716^].

**AMPEL.** AMPEL (Alert Management, Photometry and Evaluation of Light curves) follows a modular four-tier architecture developed at DESY and Humboldt University [^740^] [^741^]. Tier 0 handles alert ingestion; Tier 1 combines related photometric datapoints into object states; Tier 2 executes user-defined analysis units; and Tier 3 produces summaries and visualization outputs. This structure enables users to develop analysis schemas locally — distributed as reproducible YAML configurations — and deploy them to a live instance for real-time processing [^741^].

AMPEL's supernova classification workflow employs a cascade of two ML models. **SNGuess**, based on XGBoost gradient boosting, performs initial separation of non-recurring supernovae from recurring sources (AGN, variables) [^741^]. Transients passing this filter proceed to **ParSNIP**, a hybrid generative model combining explicit physical variables (redshift) with intrinsic latent variables learned through a variational autoencoder architecture [^741^]. ParSNIP infers at discrete redshift samples, averaging predictions weighted by model fit χ² values, which partially mitigates catastrophic photometric redshift errors. A third stage, **FinalBet**, incorporates classification priors. On the ELAsTiCC evaluation, the FinalBet classifier achieved Area Under Curve (AUC) scores above 0.9 for most non-recurrent transient classes, with true classification fractions between 50% and 70% under blind evaluation [^741^]. AMPEL participated in both ELAsTiCC campaigns (2022 and 2023), demonstrating full provenance tracking with trace IDs for every classification step [^334^] [^741^].

**ANTARES.** The Arizona-NOIRLab Temporal Analysis and Response to Events System is the longest-running Rubin broker, conceived in 2014 and processing ZTF alerts since 2018 [^210^] [^682^]. Its defining abstraction is the **Locus** — a time-series data object that aggregates all alerts within a 1 arcsecond positional tolerance, providing the full historical light curve together with multiwavelength crossmatch information and accumulated tags [^682^] [^713^]. This design enables classifiers to access significantly more photometric history than the 12-month window carried in individual alert packets.

ANTARES offers a flexible Python filter development kit in which users write `Filter` subclasses with access to the complete Locus data, including light curves, properties, tags, and LIGO/Virgo event information [^682^]. For supernova classification, ANTARES integrates **Superphot+**, a parametric light curve fitting and classification system that distinguishes five SN classes (SN Ia, SN II, SN Ib/c, SN IIn, SLSN-I) with class-averaged F1-scores of 0.61 ± 0.02 without redshift and 0.71 ± 0.02 with redshift information [^528^] [^696^]. The fit parameters are saved as Locus properties for downstream tasks. ANTARES also hosts **RAPID** (Real-time Automated Photometric Identification), a deep learning algorithm for exotic transient identification [^680^]. The broker provides open API access (no authentication required) and Kafka streams (credentials provided on request), and serves as the upstream provider for the SNAPS downstream broker [^682^].

**Lasair.** Lasair is the UK community broker, developed by the LSST:UK consortium, distinguished by its SQL-based filtering interface and the Sherlock host galaxy association system [^43^]. Users construct filters using standard SQL syntax against a rich database of alert data, pre-computed light curve features, cross-matches, and Sherlock contextual classifications. Sherlock categorizes each transient into one of seven types — Variable Star (VS), Cataclysmic Variable (CV), Bright Star (BS), AGN (AGR), Nuclear Transient (NT), Supernova (SR), or Orphan (no match) — by cross-matching against catalogs including Pan-STARRS1, AllWISE, 2MASS, SDSS, the Million Quasars Catalog, and a 100 Mpc volume-limited galaxy catalog (LASe-GPS) [^727^] [^732^]. Lasair also ingests classification annotations from ALeRCE and Fink, making their ML scores available through the same SQL query interface [^43^]. The `lasair` Python client supports database queries, Sherlock lookups, annotation creation, and Kafka stream consumption, with authentication via API token [^43^] [^733^].

**Pitt-Google.** The Pitt-Google Broker is the only cloud-native broker among the seven, built on Google Cloud Platform (GCP) and offering three primary access patterns: Pub/Sub streams for real-time subscription, BigQuery for historical SQL queries, and Cloud Storage for full Avro archives including cutouts [^687^] [^738^]. This architecture eliminates the need for users to maintain local Kafka infrastructure. The broker provides pre-filtered topic streams (e.g., `ztf-SuperNNova` for SN Ia vs. non-Ia classifications, `ztf-tagged` for basic phenomenological categories) and petabyte-scale BigQuery tables for SQL-based exploration [^372^]. The `pittgoogle-client` Python library abstracts authentication, schema handling, and data type conversions [^734^]. For supernova science, the BigQuery warehouse enables queries across the full ZTF alert archive with up to 1 TB of free querying per month under GCP's free tier [^738^].

**Babamul.** Babamul is the newest full-stream broker, jointly developed by Caltech and the University of Minnesota, with an underlying processing framework called BOOM (Bursts and Outbursts Observation Monitor) written in Rust for maximum throughput at LSST scale [^702^] [^719^]. BOOM's architecture uses a tier-like worker system with independent horizontal scaling, Valkey for in-memory queuing, and MongoDB with native spatial querying. Its unique capability is continuous cross-matching of ZTF and Rubin alert streams, enabling filters to use combined light curves from both surveys at decision time [^719^].

Babamul's ML framework, **AppleCiDEr**, is a multimodal system processing photometry, image cutouts, metadata, and (eventually) spectra [^718^] [^725^]. The photometry branch uses a [CLS]-Transformer achieving 87.8% accuracy; the image-plus-metadata branch employs AstroMiNN (competitive with BTSbot); and the spectra branch uses SpectraNeXt-2D at 87.6% accuracy [^718^]. An ensemble averages predictions across all available modalities. Python-trained models are converted to ONNX format for execution within the Rust pipeline, and users access filtered streams through Kafka topics, with each phenomenological filter producing a disjoint output stream [^718^].

| Broker | ML Approach | Primary Classifiers | SN Taxonomy | Python Client | Strengths | Access URL |
|:---|:---|:---|:---|:---|:---|:---|
| ALeRCE | CNN + Balanced RF | Stamp CNN, Light Curve BRF | Ia, Ib/c, II, SLSN, TDE | `alerce` | Most developed taxonomy; 94% stamp accuracy [^685^]; 0.97 top-level F1 [^698^] | alerce.science |
| Fink | RNN + Active Learning | SuperNNova, RF (active learning) | Ia vs. non-Ia + subclasses | `fink-client` | 6-day early classification [^729^]; 60+ science topics; 180M+ alerts processed [^60^] | fink-broker.org |
| AMPEL | XGBoost + VAE | SNGuess (XGB), ParSNIP (VAE) | User-defined (channel-based) | AMPEL framework | Reproducible YAML schemas; full provenance tracking [^741^] | ampelproject.github.io |
| ANTARES | Parametric fit + DL | Superphot+, RAPID | User-defined (tags) | `antares-client` | Full light curve history via Locus [^682^]; flexible Python filters | antares.noirlab.edu |
| Lasair | SQL + Associations | Sherlock host matching | SN, NT, AGR, VS, CV, ORPHAN | `lasair` | SQL filtering; pre-computed features; ALeRCE/Fink annotations [^43^] | lasair.lsst.ac.uk |
| Pitt-Google | RNN (deployed) | SuperNNova, UPSILoN | Ia vs. non-Ia, variables | `pittgoogle-client` | Cloud-native; BigQuery archive; no local Kafka needed [^738^] | pitt-broker.readthedocs.io |
| Babamul | Multimodal Transformer | AppleCiDEr (photometry + images) | Phenomenological filters | Kafka clients | Rust-based throughput; multi-survey crossmatch [^719^] | babamul.caltech.edu |

The diversity of ML approaches across brokers represents both a challenge and an opportunity. The stamp-based CNN in ALeRCE excels at early-time classification when few photometric points exist, while Fink's SuperNNova RNN requires more data but achieves higher discrimination power once a partial light curve has accumulated. AMPEL's modular architecture supports classifier cascades of arbitrary complexity, and Babamul's multimodal framework represents the most ambitious attempt to fuse photometric, imaging, and spectral information in real time. As the table indicates, every broker provides a programmatic Python interface, though access models range from open APIs (ALeRCE, ANTARES) to authenticated services (Lasair, Fink Kafka) to cloud-project-based access (Pitt-Google). For practitioners building training datasets, these interfaces allow broker classifications to be retrieved as pre-computed features rather than recomputed from raw photometry.

### 8.3 Using Brokers for ML Training

The most immediate ML application of broker data is to treat historical classifications as labeled training data. Every broker maintains an archive of classified alerts that can be queried programmatically, offering an alternative to training purely on simulated light curves. Fink's Data Transfer service, for instance, enables selection of specific observing nights, filtering by classification class, and application of custom conditions on alert content (e.g., `candidate.magpsf > 19.5` and `rf_snia_vs_nonia > 0.5`), with output streamed to a Kafka topic for consumption at the user's pace [^716^]. Pitt-Google's BigQuery warehouse supports SQL queries across the full ZTF archive, with up to 1 TB/month free under GCP's free tier [^738^]. ALeRCE's Python client permits batch retrieval of objects by classifier and class name with probability thresholds, returning light curves, stamps, and classification probabilities in a single workflow [^701^].

Authentication and rate limits vary across brokers and must be accounted for in bulk data strategies. Fink's REST API requires no authentication, but its Kafka stream and Data Transfer service require registration. Lasair requires an API token for all programmatic access. AMPEL requires pre-authorization for its live query API, though its batch mode can run entirely locally. Pitt-Google requires a GCP project but no billing setup for tutorial-scale usage [^738^]. ANTARES offers open HTTP API access with no authentication, though Kafka credentials are provided on request [^682^]. Most brokers do not publish explicit rate limits, operating on reasonable-use policies; users planning large-scale queries should contact broker teams directly.

A more sophisticated approach treats broker classifications as ensemble features. Because each broker uses different architectures, training data, and taxonomies, their classifications carry partially independent information. Cross-broker agreement studies show that Superphot+ (ANTARES) and the ALeRCE light curve classifier achieve 82 ± 2% agreement on light curves with spectroscopic labels, but only 72% agreement on unlabeled light curves [^528^]. Superphot+ tends to classify uncertain objects as common types (SN Ia or SN II), while ALeRCE-SN favors SLSN labels for the same ambiguous events [^528^]. This systematic difference in classifier bias means that an ensemble combining both predictions — or, more broadly, combining scores from ALeRCE, Fink, and ANTARES — can achieve higher accuracy than any individual broker. Lasair explicitly implements this by ingesting ALeRCE and Fink classification streams as annotations available through its SQL interface [^43^].

The **broker disagreement signal** — the divergence in classification probabilities across brokers for the same object — functions as a powerful anomaly detection feature. When two or more brokers disagree strongly on a transient's class, the object is either genuinely unusual (warranting follow-up) or sits in a region of feature space where training data is sparse. The SNAD project has demonstrated that broker disagreement can be used as an anomaly detection signal, identifying objects that deserve human scrutiny [^528^]. For ML practitioners, computing the Jensen-Shannon divergence or Kullback-Leibler divergence between broker probability distributions provides a continuous anomaly score that requires no additional model training. This approach is particularly valuable for Rubin-scale operations, where even a 1% anomaly rate corresponds to 100,000 events per night.

### 8.4 Real-time Stream Processing

Alert streams from Rubin and ZTF are distributed via Apache Kafka, a distributed event streaming platform that maintains ordered, durable message logs. Each broker consumes the survey's Kafka feed, processes alerts, and may republish enriched alerts to its own Kafka topics. Users subscribe to these topics through broker-specific clients. The latency budget is demanding: Rubin requires that 98% of alerts from any given visit be distributed within 60 seconds of image readout, with no more than 1% of visits exceeding this threshold [^948^]. At 10,000 alerts per visit and approximately 1,000 visits per night, this requirement permits up to 200,000 alerts per night to experience minor delays while still meeting specifications [^948^].

Kafka consumer patterns for astronomical alert ingestion follow a standard structure. The consumer establishes a connection to the broker's Kafka cluster, subscribes to one or more topics (e.g., `ztf-alerts` for the full stream, `ztf-SuperNNova` for pre-classified SN candidates at Pitt-Google [^372^]), and processes messages in a poll loop. Key configuration parameters include `group.id` (which controls consumer group membership for load balancing), `auto.offset.reset` (whether to begin at the earliest available message or only new ones), and `enable.auto.commit` (whether the consumer automatically acknowledges processed messages). For ML classifiers, the critical constraint is processing latency: each alert must be classified in under a second to avoid falling behind at Rubin's peak rate of 10 million alerts per night. This translates to approximately 115 alerts per second sustained throughput, though peaks during crowded Galactic fields or deep drilling fields may briefly exceed this rate.

The computational requirement is substantial. Running a deep learning classifier (e.g., a SuperNNova RNN inference, taking roughly 10–50 ms per alert on a CPU) on 10 million alerts requires on the order of 100,000 CPU-seconds per night, or approximately 28 CPU-hours. GPU acceleration reduces this by a factor of 10–50 but introduces deployment complexity. This is precisely why broker-classified streams are economically efficient: the broker amortizes this compute cost across all users. For a research group subscribing to Fink's pre-classified SN Ia stream, the marginal computational cost of ingestion is negligible compared to the cost of independently running classifiers on the full stream.

| Survey | Alerts/Night | Packet Format | Latency Requirement | Stream Technology | Access Method |
|:---|:---|:---|:---|:---|:---|
| ZTF (public) | ~300,000 | Avro (80 KB) | Minutes | Apache Kafka | `fink-client`, `alerce`, `antares-client` [^699^] [^701^] [^678^] |
| Rubin/LSST (full) | Up to 10,000,000 [^948^] | Avro (~82 KB) with 12-month history | <60 sec from readout [^948^] | Apache Kafka | 7 full-stream brokers [^44^] |
| Rubin/LSST (lite) | Subset of full | Avro (reduced, no cutouts) | <60 sec from readout | Apache Kafka | Broker-dependent |
| Rubin (Feb 2026 first light) | 800,000 [^796^] | Avro | ~2 minutes | Apache Kafka | ALeRCE, Lasair annotations [^796^] |
| ELAsTiCC (simulated) | ~3× Rubin rate [^334^] | LSST-like schema | <24 hours (broker challenge) | Kafka via DESC TOM | NERSC archive [^334^] |
| DECam auxiliary | Variable | Avro | Minutes | Kafka | Babamul multi-survey [^719^] |

The table above captures the dramatic scale increase from ZTF to Rubin. ZTF's 300,000 alerts per night, distributed since 2019, have served as the development platform for all seven brokers [^815^]. Rubin's first alert release on February 24, 2026 delivered 800,000 alerts, with full operations projected to reach 7 million per night initially and up to 10 million at peak [^796^] [^948^]. The alert packet size of approximately 82 KB includes 12 months of photometric history and postage-stamp cutouts [^210^]; a "lite" packet format without these attachments reduces bandwidth at the cost of eliminating the contextual information that stamp classifiers depend on. For ML practitioners, the transition from ZTF to Rubin means that training data volumes will increase by a factor of 20–30, and real-time classifiers must operate at correspondingly higher throughput.

Several strategies enable scalable real-time ML on broker streams. **Pre-filtering** — subscribing to broker-classified topics rather than the full stream — reduces data volume by 1–2 orders of magnitude. Fink's `rf_snia_vs_nonia > 0.5` topic, for example, delivers only the small fraction of alerts classified as likely SNe Ia. **Batch windowing** — accumulating alerts over short time windows (e.g., 30 seconds) and processing them as a batch — amortizes inference overhead and enables GPU utilization. **Model distillation** — training lightweight student models (e.g., gradient boosted trees) from the predictions of heavy teacher models (e.g., ParSNIP or SuperNNova) — reduces per-alert inference time to sub-millisecond levels while preserving most of the accuracy. Babamul's use of ONNX Runtime to execute Python-trained models within its Rust pipeline exemplifies this approach [^719^]. As Rubin approaches full operations, the combination of broker-provided classifications, efficient stream filtering, and distilled lightweight models will be essential for ML systems that operate in true real time.

---

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

---

## 10. Upcoming Surveys & Future Data

The next five years will bring data volumes that dwarf all previous supernova surveys combined. The Vera C. Rubin Observatory's Legacy Survey of Space and Time (LSST) entered alert operations in February 2026 and is projected to issue up to 10 million alerts per night at full operations [^793^][^815^]. The Nancy Grace Roman Space Telescope is scheduled for launch by May 2027 and will deliver near-infrared (NIR) time-domain data at depths unreachable from the ground [^269^]. ESA's Euclid mission, already operational, has released its first transient observations [^824^]. Crucially, simulation and commissioning datasets are available *now* for each of these missions — enabling machine learning (ML) practitioners to develop and validate classifiers before the full data torrent begins. This chapter catalogs these preparatory datasets, describes their formats and access methods, and outlines a development pipeline for researchers aiming to have analysis-ready code when proprietary restrictions tighten.

### 10.1 Vera C. Rubin Observatory (LSST)

#### 10.1.1 Alert Operations and Scale

The Rubin Observatory began distributing alert packets to community brokers in February 2026, marking the transition from commissioning to science-grade transient detection [^796^]. At full operations, the system is designed to produce up to 10 million alerts per night — 5σ detections in difference images across the 9.6 deg² LSST camera field of view — serialized in Apache Avro and delivered via Apache Kafka with ~60 second latency from shutter close to broker receipt [^793^][^815^][^298^]. The raw alert bandwidth spans 0.2–5 Gbps [^210^]. Seven full-stream community brokers (ALeRCE, AMPEL, ANTARES, Babamul, Fink, Lasair, Pitt-Google) receive the complete stream, each applying distinct ML architectures [^44^][^332^]. Any classifier deployed at a broker must execute inference in seconds per alert, making pre-operations benchmarking essential.

#### 10.1.2 DP0: DESC DC2 Simulation

Data Preview 0 (DP0) is the foundational simulated dataset for Rubin science preparation, built from the LSST Dark Energy Science Collaboration (DESC) Data Challenge 2 (DC2). DC2 covers a 300 deg² simulated sky region in the six LSST bands (*ugrizy*) over five years of Wide-Fast-Deep (WFD) observing at a reference cadence [^370^][^745^]. The simulation incorporates realistic atmospheric effects, instrument signatures, and source populations, making it the highest-fidelity Rubin precursor dataset publicly available.

The primary data products span approximately 181 GB in Apache Parquet format and include: an Object Table with 114 million extended and 33 million point sources (~118 GB); a Truth-match Table with 759 million galaxy, 5 million star, and 500,000 supernova entries (~63 GB); and unmerged truth variability tables containing per-observation light curves for all transient and variable sources [^370^][^746^]. The SN truth catalogs include full light curves, host galaxy assignments, redshifts, and classification labels, providing the ground-truth annotations necessary for supervised classifier training.

Three access pathways are available: the Rubin Science Platform (RSP) at `data.lsst.cloud`, which provides TAP catalog queries, Jupyter notebooks with the LSST Science Pipelines, and Butler-based image access [^374^]; the DESC Data Portal (`data.lsstdesc.org`) for bulk Globus transfer from the "LSSTDESC Public" collection [^749^][^750^]; and the `GCRCatalogs` Python package, which enables programmatic access via `GCRCatalogs.load_catalog('desc_dc2_run2.2i_dr6_object')` with lazy loading suitable for ML pipelines [^745^].

#### 10.1.3 DP1: ComCam Commissioning Data

Data Preview 1 (DP1), released on June 30, 2025, is the first data product from actual Rubin on-sky observations, obtained with the LSST Commissioning Camera (LSSTComCam) during a 48-night campaign from October 24 to December 11, 2024 [^770^][^765^][^767^]. The release comprises approximately 3.5 TB, including 1,792 science-grade exposures, 2,644 coadded images, and pre-generated difference images across seven non-contiguous fields totaling ~15 deg² [^765^]. The catalog contains ~2.3 million distinct objects, including 1.6 million extended sources [^765^]. Critically for transient science, DP1 includes full Difference Image Analysis (DIA) products — DiaSource and DiaObject detection catalogs, and DiaForcedSource light curves — produced with the LSST Science Pipelines. The ECDFS field, with 21 observing epochs and a mean of 40.7 visits per night, offers the best time-domain coverage [^765^].

DP1 access is exclusively through the RSP [^795^]. Data rights are restricted to US/Chilean scientists and international in-kind team members; after a two-year proprietary period from ~June 2027, data becomes public but RSP compute remains reserved for data rights holders [^765^]. For ML practitioners, DP1 is the only currently available real Rubin dataset with DIA products, enabling sim-to-real validation of transient detection algorithms with realistic noise, PSF variation, and calibration artifacts.

#### 10.1.4 Alert Format and Tools

Each Rubin alert packet occupies approximately 82 KB and contains a DiaSource record with photometry, astrometry, and shape parameters; an associated DiaObject or SSObject record; 12 months of prior DiaSource and DiaForcedSource history; and three FITS-format postage stamp cutouts (science, difference, and template images) [^290^][^298^]. This rich contextual payload enables both light-curve-based and image-based classification strategies from a single packet.

The `lsst-alert-packet` Python library provides the official toolkit for alert manipulation [^811^]. Installable via `pip install lsst-alert-packet`, it offers schema management, parsing, simulation, and validation built on `fastavro` [^809^]. Key functions: `lap.Schema.from_file()` for the latest schema, `lap.retrieve_alerts()` for iterating Avro files, and `lap.simulate_alert()` for synthetic test data. Sample alerts with a companion SQLite Prompt Products Database (PPDB) are available from `lsst-dm/sample_alert_info` [^810^]. Schema versions follow `MAJOR.MINOR` numbering with forward-transitive compatibility within major versions [^811^].

#### 10.1.5 Rubin Data Products Timeline

Table 10.1 summarizes the Rubin data products relevant to supernova and transient ML, ordered by release date and maturity.

**Table 10.1 — Rubin Data Products Timeline**

| Product | Release Date | Size | Format | Access Method | Key Content |
|---------|-------------|------|--------|---------------|-------------|
| DP0 (DESC DC2) | 2021 (ongoing) | ~181 GB | Parquet, FITS | RSP, Globus, GCRCatalogs [^374^][^749^] | 500K simulated SNe, full truth labels [^370^] |
| DP1 (ComCam) | June 2025 | ~3.5 TB | FITS, catalogs (RSP) | RSP only (data rights) [^795^] | 2.3M objects, DIA products, real transients [^765^] |
| ELAsTiCC2 alerts | Nov–Dec 2023 | ~50 GB | SNANA FITS, Avro | NERSC, DESC TOM [^334^] | ~4M objects, 19 classes, Rubin-format alerts [^334^] |
| DP2 (LSSTCam) | Projected 2027 | TBD | RSP native | RSP (data rights) | Full camera, 10× DP1 area, 30-night baseline |
| Full alert stream | Feb 2026 (ramping) | ~82 KB/alert | Apache Avro | 7 community brokers [^793^] | Up to 10M alerts/night [^815^] |
| Alert archive | Projected 2027 | TBD | Avro, PPDB | RSP archive [^825^] | Historical alerts for training set construction |

The progression from DP0 through DP1 to the live alert stream represents a staged increase in realism: DC2 provides volume and perfect labels for initial training; DP1 introduces real instrumental effects for sim-to-real validation; ELAsTiCC2 exposes classifiers to the alert packet format and cadence; and the live stream adds the latency and throughput constraints of production operations. ML practitioners should treat this sequence as a development ladder, testing classifiers on each rung before advancing to the next.

### 10.2 Nancy Grace Roman Space Telescope

#### 10.2.1 Mission Overview and HLTDS

The Nancy Grace Roman Space Telescope is scheduled for launch by May 2027 and will carry out the High-Latitude Time-Domain Survey (HLTDS), a NIR survey targeting Type Ia supernovae to *z* ≈ 2 [^269^]. The HLTDS operates in two tiers: a Wide tier (19 deg², *RZYJ* filters, 100s exposures, 5-day cadence) and a Deep tier (4.2 deg², *YJHF* filters, 300s exposures) [^329^]. Approximately 20% of the area receives prism spectroscopy at *R* ≤ 100 across 7500–18000 Å [^329^]. NIR coverage reduces dust extinction and probes higher-redshift SNe Ia where optical emission is redshifted into the infrared. Roman is projected to detect ~100,000 SNe Ia over its mission, but real data will not arrive until late 2027 at the earliest. The following datasets enable pre-launch classifier development.

#### 10.2.2 Hourglass Simulation

The Hourglass simulation is the most comprehensive synthetic dataset for Roman transient science currently available, produced by the Roman Supernova Physics Investigation Team (PIT) [^328^][^269^]. Published in *ApJ* (2025), it simulates 10 extragalactic transient types across both HLTDS tiers with realistic Roman observational characteristics including noise models, PSF profiles, and detection thresholds [^269^].

The transient population includes 21,700 SNe Ia, 39,000 core-collapse SNe, 1,300 SN Ia-91bg-like events, 1,300 SN Iax, 70 superluminous SNe (SLSNe-I), 39 tidal disruption events (TDEs), 14 kilonovae, 15 pair-instability SNe (PISNe), and 139 AGN flares — totaling over 64,000 detected transients spanning *z* = 0.35–2.23 [^269^]. The wide redshift range and inclusion of rare events make this dataset valuable for training classifiers that must generalize across diverse populations.

The Zenodo release (DOI: 10.5281/zenodo.14262943) comprises three Apache Parquet files: `hourglass_objects.parquet` (one row per object: RA, Declination, redshift, S/N, classification); `hourglass_photometry.parquet` (one row per flux measurement); and `hourglass_spectra.parquet` (spectral time series for the prism subset) [^328^][^269^]. A common CID (candidate ID) links records across tables. The Parquet format enables direct ingestion via `pandas.read_parquet()` or `pyarrow`. The simulation framework is documented at the `Roman-Supernova-PIT/hourglass_snana_sims` GitHub repository [^269^]. The Hourglass data has been used to train the ParSNIP and SCONE classifiers [^282^], and the availability of both light curves and spectra enables multi-modal classifier architectures combining photometric and spectroscopic features.

#### 10.2.3 Roman IPAC Image Simulations

Complementing the Hourglass catalog, Wang et al. (2023) produced the first simulations of realistic Roman WFI images with artificial Type Ia supernovae injected as point sources [^266^][^267^]. The dataset covers a 1 deg² subarea of a planned 5 deg² deep field over a two-year time series, with ~1,050 SNe Ia injected at realistic rates and brightness distributions [^266^]. Unlike Hourglass, the IPAC simulations deliver pixel-level FITS images, enabling training of CNN and vision transformer models on cutouts rather than pre-extracted features.

The release includes time-series images, input catalogs with known positions and fluxes, coadded images, and difference image subtraction demonstrations [^828^]. The known injection parameters provide exact ground truth for detection efficiency studies — enabling quantitative measurement of ML recovery rates as a function of host galaxy surface brightness and S/N [^267^]. Access: `roman.ipac.caltech.edu/page/sn-survey-image-sim-html` [^828^].

#### 10.2.4 phrosty: GPU-Accelerated Difference Imaging

Processing Roman images at survey scale requires handling ~241 Level-2 images per day (~0.4 TB/day). The `phrosty` pipeline ("PHotometry for ROman with SFFT for tYpe Ia supernovae") uses a GPU-accelerated Saccadic Fast Fourier Transform (SFFT) algorithm for image subtraction [^764^][^775^]. Developed by Aldoroty et al. (2025), phrosty achieves orders-of-magnitude speedup over CPU-based alternatives: a HOTPANTS-style subtraction requires ~10 minutes per detector image (~80 hours/day), whereas phrosty's mixed GPU/CPU architecture processes the full Roman daily throughput in a fraction of that time [^775^]. The pipeline uses `galsim` + `roman_imsim` for spatially varying PSF modeling and operates on OpenUniverse2024 FITS images, producing difference images and forced-photometry light curves [^775^].

The open-source codebase (GitHub: `Roman-Supernova-PIT/phrosty`) includes deployment configurations for NERSC Perlmutter via Docker/Podman, with scripts for interactive and Slurm batch modes [^775^]. For ML practitioners, phrosty provides a data reduction layer that transforms raw images into the difference-image and light-curve products used as classifier input features. Configuration requires three environment variables (`SIMS_DIR`, `SN_INFO_DIR`, `DIA_OUT_DIR`) pointing to the OpenUniverse data, survey YAML, and output paths [^775^].

### 10.3 ESA Euclid

#### 10.3.1 Q1 Quick Data Release

Euclid's Quick Data Release 1 (Q1), published in March 2025, provided the first public look at Euclid's imaging capabilities, including serendipitous observations of transients in the Euclid Deep Fields [^824^][^766^]. The transient analysis by Duffy et al. (2025) cross-matched Euclid single-epoch observations against the Transient Name Server (TNS), identifying 164 previously reported transients, of which 161 have photometric measurements [^824^]. Photometry was extracted using the `ecsnoopy` PSF-fitting package. The detection efficiency analysis shows ~70% of known transients reported within six months before Euclid observation, with discovery magnitudes brighter than 24, were recovered in the *I_E* (VIS) images [^824^] — a benchmark for ML-based detection algorithms.

Notable transients include SN 2024pvw, one of the earliest NIR detections of a Type Ia SN captured 15 days prior to peak brightness, and SN 2023aew, observed at 435.9 days post peak — a rare late-phase core-collapse detection [^824^][^766^]. Q1 data is accessible through the ESA Euclid archive.

#### 10.3.2 NIR Filter Coverage

The defining characteristic of Euclid's transient dataset is its four-filter coverage spanning optical to NIR: *I_E* (VIS, 550–900 nm), *Y_E* (NISP, 0.95–1.19 μm), *J_E* (NISP, 1.19–1.55 μm), and *H_E* (NISP, 1.55–2.00 μm). With 161 measured transients, Q1 constitutes the largest real NIR transient photometric dataset currently available for ML training — a critical resource given the scarcity of public NIR supernova data [^824^]. This enables two immediate ML applications: training dust-robust classifiers that exploit lower NIR extinction, and validating sim-to-real transfer by testing classifiers trained on simulated Roman NIR data (Hourglass, OpenUniverse2024) against real Euclid photometry to quantify domain-shift effects before Roman launch.

#### 10.3.3 DR1 Outlook

Euclid Data Release 1 (DR1) is expected in late 2026 and will cover ~30× the Q1 area (~1,900 deg²), with ~1.5 orders of magnitude more objects [^766^]. Critically, DR1 will include multi-epoch observations, enabling proper transient detection via difference imaging rather than the single-epoch cross-matching that defines Q1. This will allow Euclid to function as an independent time-domain survey, complementing Rubin's optical alerts with NIR detections of the same transients. For ML practitioners, DR1 marks the transition of Euclid from a validation dataset to a primary discovery survey for NIR transients.

### 10.4 OpenUniverse2024

#### 10.4.1 Dataset Overview and Scale

OpenUniverse2024 is the largest joint survey simulation ever produced for time-domain astronomy, generating ~400 TB of matched pixel-level imaging for Roman and Rubin over a common ~70 deg² sky region [^335^][^302^]. Published in *MNRAS* (2025), it uses the updated Diffsky extragalactic model with improved transient templates to produce self-consistent multi-survey observations of the same underlying sources [^335^]. The survey geometry includes five overlapping components — the LSST ELAIS-S1 Deep Drilling Field, the Roman Time-Domain Survey shifted to overlap ELAIS, the LSST Wide-Fast-Deep survey with rolling cadence, the Roman Wide-Area Survey, and a Roman deep-field calibration region — meaning many transients are "observed" by both facilities with different filters, cadences, and depths [^335^].

Two release tiers are available: a smaller Data Preview (DOI: 10.26131/IRSA569) hosted at IPAC and on AWS, and the full 400 TB release (DOI: 10.26131/IRSA596) on AWS cloud storage [^302^]. Listed on the AWS Open Data Registry (`registry.opendata.aws/openuniverse2024/`), it provides direct S3 access without egress charges [^305^]. Products include Roman and Rubin simulated images (FITS) plus companion catalogs (Parquet).

#### 10.4.2 Cross-Survey Classifier Development

The unique value of OpenUniverse2024 is its enablement of cross-survey classifier development before either mission reaches full operations. A classifier trained on the Rubin-only portion of a transient's light curve can be validated against the Roman-only portion, enabling quantification of how accuracy degrades when one survey's data is missing or delayed — a practical concern given the different observing schedules, weather constraints, and processing latencies of the two facilities. OpenUniverse2024 provides the only current source of realistic training data for fusion models combining optical and NIR photometry from different instruments into a single classification decision.

The simulation has been adopted by the `phrosty` pipeline for Roman difference imaging and by the Roman SN PIT and DESC collaborations for cosmology testing [^775^]. FITS images support CNN/ViT training on cutouts, while Parquet catalogs enable tabular-feature classifiers. AWS cloud hosting allows processing without local storage — analysis can run on EC2 or SageMaker with direct S3 reads.

### 10.5 Preparing for the Future

#### 10.5.1 The Readiness Window

There is a ~12-month window during which simulation data (DP0, Hourglass, OpenUniverse2024), commissioning data (DP1), and alert-format test data (ELAsTiCC2) are simultaneously accessible with minimal proprietary restrictions. After Rubin reaches full operations and the two-year proprietary period on DP1-era data takes effect (~mid-2027), much of the high-fidelity labeled training material will be restricted to data-rights holders [^765^]. ML researchers who develop models during this window gain a first-mover advantage: classifiers can be deployed to brokers and tuned as the stream ramps up, while late starters face data-access barriers and pressure to produce results from an already-mature alert stream.

Two areas demand particular urgency. First, sim-to-real validation must be completed before proprietary restrictions tighten. DP1 is the only available real Rubin data with DIA products; comparing DC2-trained classifier performance against DP1 real transients quantifies the domain-shift penalty that will apply on the live stream. Second, broker integration testing should occur during the ramp-up phase (thousands to millions of alerts per night) rather than deploying untested code at full capacity.

#### 10.5.2 Recommended Preparation Pipeline

A concrete four-stage pipeline is recommended for ML practitioners preparing for the Rubin-Roman era:

**Stage 1 — ELAsTiCC2 for format familiarity.** ELAsTiCC2 provides ~4 million objects across 19 transient types in Rubin-compatible alert format, with ~50 million detections and ~400 million forced-photometry points [^334^]. The training set (ELASTICC2_TRAIN_02.tar.bz2, 7.4 GiB) is available at NERSC and via the DESC TOM portal [^334^][^829^]. Working with ELAsTiCC2 first ensures classifiers handle the correct feature schema, class taxonomy, and cadence.

**Stage 2 — DP0 for volume training.** The DESC DC2 truth catalogs contain ~500,000 simulated SNe Ia with perfect labels, light curves, and host associations [^370^]. Training on DP0 enables large-model development requiring hundreds of thousands of labeled examples, with Parquet format enabling efficient batched loading into PyTorch or TensorFlow.

**Stage 3 — DP1 for sim-to-real calibration.** Deploy the DP0-trained classifier on DP1 DIA products and measure performance degradation. Key metrics: detection completeness versus magnitude, false positive rate on difference images, and classification accuracy for transients with spectroscopic cross-matches. The DP1 ECDFS field, with 21 epochs, provides sufficient time-sampling for meaningful tests [^765^].

**Stage 4 — Broker deployment.** Integrate the validated classifier with one or more Rubin community brokers. Each offers a distinct deployment model: Fink provides Spark-based stream processing [^815^]; AMPEL offers modular user-defined classifiers; ALeRCE exposes a Python client with a rich taxonomy. The Rubin Alerts & AI Hackathon (April 1–3, 2026, SkAI Institute, Chicago) signals strong community momentum around this deployment step [^794^].

#### 10.5.3 Upcoming Survey Summary

Table 10.2 consolidates the key parameters of the four missions discussed in this chapter, along with their current data availability status for ML preparation.

**Table 10.2 — Upcoming Survey Summary**

| Survey | Launch/Operations | Expected SNe/Transients per Year | Key Data Products for ML | Current Availability |
|--------|-------------------|----------------------------------|--------------------------|---------------------|
| Vera C. Rubin Observatory (LSST) | Alert ops: Feb 2026 | Up to 10M alerts/night [^793^] | DP0 (181 GB sim), DP1 (3.5 TB real), ELAsTiCC2 (4M objects), live Avro stream | DP0, DP1, ELAsTiCC2 available now; stream live |
| Nancy Grace Roman Space Telescope | By May 2027 | ~100K SNe Ia (full mission) [^269^] | Hourglass (64K transients, 10 classes), IPAC images (1,050 SNe Ia), OpenUniverse2024 (400 TB joint) | All simulations available now |
| ESA Euclid | Operational (2023) | TBD (DR1 will enable discovery) | Q1 (164 transients, 161 with photometry), DR1 projected late 2026 | Q1 available; DR1 in ~18 months |
| OpenUniverse2024 (Joint) | N/A (simulation) | 64K+ transients across types [^269^] | 400 TB FITS images + Parquet catalogs on AWS S3 [^302^] | Full dataset available via AWS |

The timeline is compressing. Rubin is already distributing alerts; Roman will launch within ~12 months; Euclid DR1 arrives in late 2026. For each mission, the simulation and commissioning products cataloged here provide a pre-launch runway that did not exist for previous surveys. The recommended progression — ELAsTiCC2 → DP0 → DP1 → broker deployment — offers a concrete path from concept to production, with each stage adding realism that the next depends upon. Researchers who complete this pipeline before mid-2027 will be positioned not merely to consume the upcoming data deluge, but to direct it toward defined science objectives from the first night of full operations.

---

## 11. Multi-messenger & Emerging Data Streams

The preceding chapters have focused primarily on optical and near-infrared data streams that constitute the bulk of contemporary supernova (SN) machine learning (ML) training sets. However, a growing fraction of SN science now depends on data that arrives through entirely different physical channels—radio synchrotron emission, neutrino bursts, gravitational waves, and human classifications from citizen science platforms. These non-traditional streams are not merely supplementary. For core-collapse supernovae (CCSNe), radio emission traces circumstellar interaction on timescales of months to years; neutrino bursts carry information from the innermost seconds of stellar collapse; gravitational waves (GWs) probe the asymmetry of the explosion mechanism; and citizen science labels capture pattern-recognition capabilities that complement algorithmic classifiers. This chapter catalogs the datasets, access methods, and ML-readiness of each stream, with particular attention to the practical challenges that arise when training models on small samples, heterogeneous formats, and simulation-derived labels.

### 11.1 Radio Transient Surveys

Radio observations of supernovae probe the interaction between the SN blast wave and the circumstellar medium (CSM), revealing mass-loss history and progenitor properties that are often invisible at optical wavelengths. Three Southern-Hemisphere-pathfinder telescopes now deliver wide-field radio transient data at an unprecedented scale, though the number of SN-specific detections remains a limiting factor for ML training.

#### 11.1.1 ASKAP VAST Data Release 1

The Australian Square Kilometre Array Pathfinder (ASKAP) Variables and Slow Transients (VAST) Survey operates at 888 MHz with 288 MHz bandwidth, using 36 12-meter dishes equipped with phased-array feeds (PAF) that deliver a ~30 deg$^2$ field of view [^861^]. Data Release 1 (DR1), spanning observations from June 2023 to May 2025, covers ~12,300 deg$^2$ across 276 fields and comprises 2,945 images [^369^]. The survey achieves a typical root-mean-square (RMS) sensitivity of 0.24 mJy/beam with angular resolution of 12–20 arcseconds, and revisits each field approximately every two months, yielding 10–11 epochs per field [^369^]. The resulting light curve database contains 0.5 million sources with 6.4 million individual measurements [^369^].

For supernova science, however, the yield is modest. An untargeted variability search across DR1 identified 117 astrophysical variables, of which only 2 were optically identified supernovae and 1 was a supernova candidate—the remaining population comprising 27 pulsars, 40 radio stars, 44 active galactic nuclei (AGN), and a handful of other classes [^369^]. The scarcity of SN detections reflects both the genuinely low surface density of radio-bright supernovae and the fact that ASKAP's 888 MHz observations are sensitive to typical CCSNe only out to ~8 Mpc, though the most luminous events remain detectable to z ~ 0.15 (~700 Mpc) [^861^]. VAST data products are publicly available through the CSIRO Data Access Portal (DAP) in FITS image and CSV catalogue formats [^371^].

#### 11.1.2 LOFAR LoTSS DR3

The LOFAR Two-metre Sky Survey (LoTSS), conducted with the LOw-Frequency ARray across Europe at 120–168 MHz, represents the largest low-frequency radio survey ever undertaken [^830^]. Data Release 3 (DR3) covers 19,035 deg$^2$ (88% of the northern sky) and catalogs 13,664,379 radio sources derived from 16,943,656 Gaussian components, accumulated over more than 10.5 years of observations consuming 18.6 PB of raw data from 12,950 hours of telescope time [^830^][^842^]. At a median sensitivity of 92 μJy/beam and 6 arcsecond angular resolution, LoTSS-DR3 has uncovered rare objects including faint supernova remnants and flaring stars [^831^][^836^]. The source catalogues, mosaic images, and calibrated measurement sets are publicly available via the LoTSS DR3 website [^840^][^842^].

LoTSS is fundamentally a static survey; transient identification requires epoch-by-epoch comparison rather than built-in time-domain cadence. Its primary SN-relevant contribution lies in host-galaxy studies and supernova remnant identification rather than real-time transient discovery.

#### 11.1.3 MeerKAT ThunderKAT

ThunderKAT is the image-plane transients programme for MeerKAT, a 64-dish cm-wave telescope and Square Kilometre Array (SKA) precursor in the southern hemisphere [^877^]. The programme targets extragalactic synchrotron transients including Type Ia supernovae, alongside Galactic sources such as X-ray binaries and cataclysmic variables [^878^]. A distinctive feature of ThunderKAT is its commensal observing strategy: agreements with other MeerKAT Large Survey Projects allow transients to be searched in data collected for other science goals, effectively increasing the discovery space by a factor of approximately 10 [^877^]. The project also operates MeerLICHT, an optical telescope that performs simultaneous imaging for each radio transient detected [^878^]. Data products are available through the South African Radio Astronomy Observatory (SARAO).

#### 11.1.4 The Small-Sample Challenge in Radio SN ML

The central obstacle to ML applications in radio supernova astronomy is sample size. VAST DR1 contains only 3 SN-related sources among 117 variables [^369^]. The Machine Learning for Transients (MALT) pipeline—the most systematic ML effort for radio transient classification to date—was trained on just 87 publicly available radio light curves drawn from the literature, spanning 11 classes including supernovae, AGN, gamma-ray bursts, and tidal disruption events [^841^][^928^]. Using a pipeline of Gaussian-process data augmentation, wavelet feature extraction, and random-forest classification, MALT achieves ~78% accuracy on realistic datasets after 8 hours of observation, rising to ~97% with simulated representative training [^928^]. However, supernovae are among the most frequently misclassified classes, commonly confused with tidal disruption events, and adding optical data improves the worst-performing class accuracy by 19% [^928^]. The message for practitioners is clear: radio SN classification with current samples requires multi-wavelength augmentation or transfer learning from optical counterparts. Future commensal observing with MeerKAT and continued VAST operations are projected to grow sample sizes substantially, but for the present, publicly available radio SN light curves remain a scarce training resource [^841^].

### 11.2 Neutrino Alerts and Experiments

Neutrinos provide the only direct observational window into the core-collapse mechanism itself. Unlike electromagnetic emission, which emerges hours to days after collapse, neutrino bursts escape within seconds and carry kinematic information about the proto-neutron star.

#### 11.2.1 SNEWS 2.0

The SuperNova Early Warning System (SNEWS) is a worldwide network of neutrino detectors that has operated in fully automated mode since 2005 [^822^]. SNEWS 2.0 represents a major upgrade designed for the multi-messenger astronomy era, featuring reduced alert thresholds and latency, pointing information derived from timing triangulation across the detector network, and integration with the Gamma-ray Coordinates Network/Transient Astronomy Network (GCN/TAN) alert infrastructure [^906^][^910^]. Participating experiments include Super-Kamiokande, IceCube, KamLAND, Borexino, LVD, Daya Bay, and the under-construction JUNO and DUNE detectors [^822^][^910^]. The system issues two alert tiers: Gold alerts, which are distributed automatically worldwide with a false-alarm rate of less than one per century, and Silver alerts, shared among experiments only [^910^]. A three-tier data-sharing framework provides progressively richer information: alert-tier activity messages, significance-tier skymaps and p-values, and rich-data-tier neutrino light curves with distance estimates [^910^]. SNEWS 2.0 also engages citizen science and amateur astronomer communities for follow-up coordination [^910^].

#### 11.2.2 SNEWPY

SNEWPY is an open-source Python package that bridges the gap between supernova neutrino simulations and expected detector signals, developed explicitly for SNEWS 2.0 but broadly applicable to modelers and experimentalists [^821^]. The package provides a unified interface to hundreds of supernova simulations from multiple modeling groups, a large library of flavor transformation prescriptions, and a complete Python interface to SNOwGLoBES for computing event rates in different detector configurations [^375^]. The pipeline proceeds from simulation extraction (time, energy, angle, and flavor-dependent neutrino emission) through flavor transformation convolution to observable detector signals [^821^]. SNEWPY is pip-installable and documented at snewpy.readthedocs.io [^375^]. For ML practitioners, SNEWPY enables generation of synthetic neutrino detector signals for training classifiers, model discrimination studies, and sensitivity projections for future detectors [^818^][^902^].

#### 11.2.3 IceCube and IceCube-Gen2

The IceCube Neutrino Observatory at the South Pole, instrumenting a cubic kilometer of Antarctic ice with 5,160 digital optical modules (DOMs), detects supernovae through a collective excess of low-energy events above the noise floor [^911^]. An 11-year search from 2008–2019 found no evidence for galactic CCSNe, placing a 90% confidence-level upper limit of 0.23 events per year out to ~25 kpc [^912^]. IceCube's sensitivity exceeds 99% for galactic supernovae from progenitor stars of any mass within the Milky Way, though its reach to the Large and Small Magellanic Clouds depends on the neutrino emission model [^909^][^911^]. The planned IceCube-Gen2 upgrade will expand the optical array by roughly a factor of 8, deploying ~10,000 new sensors with segmented multi-PMT DOM (mDOM) technology [^909^]. A two-stage coincidence-based trigger—local coincidences within 20 nanoseconds combined with a global multiplicity requirement—will maintain a false-alarm rate below one per century while extending the observable distance to 270 kpc in 50% of cases [^909^]. ML-based energy reconstruction frameworks are under active development for IceCube-Gen2 [^909^].

#### 11.2.4 DUNE

The Deep Underground Neutrino Experiment (DUNE) will deploy four 10-kiloton liquid argon time projection chambers (LArTPCs) in South Dakota, offering unique sensitivity to electron neutrinos from supernovae via the charged-current channel $\nu_e + {}^{40}\text{Ar} \rightarrow e^- + {}^{40}\text{K}^*$ [^833^][^322^]. At a fiducial distance of 10 kpc, the 40-kiloton array expects ~3,000 neutrino events (model-dependent), with detection efficiency exceeding 90% for bursts at distances up to 20 kpc [^888^][^322^]. DUNE's supernova pointing capability is projected to achieve 3.4° resolution at 68% confidence for the full 40-kiloton array under perfect event classification, or 4.3° under realistic 4% misclassification conditions [^888^][^889^]. The pointing algorithm employs "brems flipping" for head-tail disambiguation combined with a maximum likelihood method [^888^], with a design goal of contributing pointing information to SNEWS 2.0 within minutes of a burst [^322^].

Machine learning for DUNE's supernova trigger is an active research frontier. Sparse convolutional neural networks (CNNs) perform pixel classification to distinguish track-like particles (protons, muons) from shower-like signatures (electrons), operating on 512×512 pixel representations of LArTPC interactions [^833^][^837^]. Multiple architectures—standard CNNs, Graph Neural Networks, and Sparse CNNs—are under benchmark comparison [^902^]. The low-energy regime below 5 MeV presents unique triggering and reconstruction challenges that require specialized ML approaches [^322^]. Simulated training data is available through LArSoft and MARLEY frameworks, with ProtoDUNE test-detector data at CERN providing validation datasets [^835^][^897^].

### 11.3 Gravitational Wave Counterparts

Core-collapse supernovae and neutron star mergers emit gravitational waves that can trigger rapid electromagnetic follow-up campaigns. While the SN GW signature from core collapse is weaker and more uncertain than binary neutron star (BNS) mergers, the infrastructure developed for GW follow-up has become a critical component of the multi-messenger ecosystem.

#### 11.3.1 LIGO/Virgo/KAGRA O4 and ZTF Follow-up

The fourth observing run (O4) of the LIGO/Virgo/KAGRA detector network began in May 2023 and was conducted in two segments: O4a (May 2023–January 2024) yielded 81 significant candidates out of 92 total events, while O4b (April 2024–present) contributed an additional 68 significant candidates as of early 2026 [^863^]. The Zwicky Transient Facility (ZTF) has served as a primary electromagnetic follow-up facility, managing GW event information through the Fritz web-based platform for candidate vetting and observation triggering [^820^]. An open-source backup scheduler, SniperGW, provides programmatic ZTF access [^820^]. Real-time alerts from GW follow-up observations are distributed through seven approved community brokers—ALeRCE, AMPEL, ANTARES, Fink, Lasair, and Pitt-Google—enabling automated classification pipelines to process counterpart candidates within minutes of detection [^820^].

Recent GW-supernova events demonstrate the maturity of this infrastructure. The sub-threshold sub-solar gravitational-wave trigger S250818k was associated with the candidate superkilonova AT2025ulz/ZTF25abjmnps, identified from 58 candidates with at least two detections by the nuztf pipeline [^817^]. Extensive follow-up by ZTF, GOTO, Pan-STARRS1, Gemini, Keck, and other facilities confirmed the multi-messenger nature of the event [^817^][^819^].

#### 11.3.2 GOTO

The Gravitational-wave Optical Transient Observer (GOTO) operates a dual-hemisphere network with telescopes at La Palma (North) and Siding Spring (Australia), designed specifically for rapid GW follow-up [^862^]. During O4, GOTO achieved a median delay from GW alert to first observation of approximately 3 hours and processed nearly 1 million difference-image detections [^862^]. With both sites operational, GOTO can cover up to 95% of a GW skymap localization probability in a single night, a coverage fraction that is critical when localization areas span hundreds to thousands of square degrees [^862^].

#### 11.3.3 Real-Time Multi-messenger Pipelines

Several software pipelines now automate the correlation of GW alerts with optical and neutrino data. The nuztf pipeline cross-matches ZTF detections with GW localizations and applies photometric and contextual filters to rank counterpart candidates [^817^]. The GCN/TAN network distributes both human-readable GCN Circulars for citable follow-up reports and automated GCN Notices with event localization [^885^]. Astro-COLIBRI provides a unified platform with a public RESTful API that ingests alerts from GCN, VOEvent, and ATel streams, offering programmatic access for ML pipelines that need structured multi-messenger event data [^903^][^901^]. Key features for ML classifiers in multi-messenger SN searches include time coincidence (GW and neutrino signals arrive within seconds), skymap localization area (tens to thousands of square degrees), distance estimates from GW luminosity distance combined with host-galaxy redshift, and color evolution patterns (kilonova candidates exhibit rapid reddening) [^895^][^817^][^860^].

### 11.4 Citizen Science

Citizen science projects have emerged as a source of human classifications that capture pattern-recognition capabilities complementary to algorithmic approaches. For supernova ML, the value lies not in replacing automated classifiers but in providing orthogonal labels for uncertain objects and anomaly detection signals that pure algorithms may miss.

#### 11.4.1 SNAD

The SuperNova Anomaly Detection (SNAD) project combines machine learning with human expertise to identify unusual astronomical objects by their photometric features [^158^][^160^]. Operating on the Open Supernova Catalog (1,999 light curves in g'r'i') and ZTF Data Release 3 (2.25 million objects across 3 fields), SNAD employs a three-stage pipeline: feature extraction, outlier search with algorithms such as Isolation Forest and Local Outlier Factor, and expert identification [^160^]. The project maintains the SNAD Viewer (ztf.snad.space), a centralized web interface for exploring ZTF objects, and the SNAD Transient Miner for ML-based anomaly detection [^158^]. To date, SNAD has identified 144 new supernova candidates from ZTF data [^158^]. The underlying code is publicly available on GitHub, and the anomaly detection methodology is well-documented [^694^][^160^].

#### 11.4.2 Zooniverse Supernova Hunters

The Zooniverse Supernova Hunters project (zooniverse.org/projects/dwright04/supernova-hunters) engages volunteers to classify astronomical detections as real or bogus, providing human labels that improve detection algorithms [^321^]. The project operates in the real/bogus classification domain—the same task addressed by ML algorithms such as the ZTF Random Forest real/bogus scorer—allowing direct comparison between human and machine performance on identical images.

#### 11.4.3 Galaxy Zoo: Weird and Wonderful

Galaxy Zoo: Weird and Wonderful (GZ:W&W) represents perhaps the most instructive case study for ML practitioners. The project presented ~200,000 images from the Subaru Hyper-Suprime Cam survey to approximately 2,000 volunteers, who identified mergers, gravitational lenses, ringed galaxies, supernova candidates, and other rare phenomena [^876^]. A critical finding emerged when volunteer anomaly scores were compared against ML anomaly scores: no appreciable correlation was detected between the two [^887^]. This lack of correlation is not a failure of either system; rather, it demonstrates that human visual inspection and algorithmic feature extraction capture fundamentally different and orthogonal information about astronomical images. For ML practitioners, the implication is that citizen science labels—particularly for ambiguous or anomalous transients—can provide a valuable complementary signal when combined with algorithmic classifications in ensemble frameworks.

### 11.5 Multi-messenger Data Sources: A Comparative Overview

Table 11.1 summarizes the key multi-messenger and emerging data sources discussed in this chapter, organized by messenger type, data volume, format, access method, and readiness for ML applications. The diversity of formats, access restrictions, and sample sizes presents a practical challenge: no single data access pattern serves all channels, and ML pipelines must accommodate everything from pip-installable Python packages (SNEWPY) to 18.6 PB raw interferometric datasets (LoTSS) to real-time alert streams (GCN/TAN).

| Source | Messenger Type | Data Volume | Primary Format | Access Method | ML Readiness |
|---|---|---|---|---|---|
| ASKAP VAST DR1 | Radio (888 MHz) | 0.5M sources, 6.4M measurements [^369^] | FITS images, CSV catalogues | Public (CSIRO DAP) [^371^] | Limited by small SN sample |
| LOFAR LoTSS DR3 | Radio (144 MHz) | 13.7M sources; 18.6 PB raw [^842^] | FITS images, source catalogues | Public (LoTSS website) [^840^] | Static survey; host/remnant studies |
| MeerKAT ThunderKAT | Radio (cm-wave) | Growing via commensal observing [^877^] | CASA image format | SARAO | Limited public data availability |
| SNEWS 2.0 | Neutrino alerts | Real-time alert stream | VOEvent, email, GCN/TAN | Public subscription [^910^] | Ready for real-time trigger systems |
| SNEWPY | Neutrino simulation | Hundreds of models [^821^] | Python package | `pip install snewpy` [^375^] | Ready for synthetic training data |
| IceCube/IceCube-Gen2 | Neutrino bursts | 11+ years; >99% Galactic SN sensitivity [^911^] | Custom HDF5 | Collaboration [^912^] | ML energy reconstruction in dev. [^909^] |
| DUNE | Neutrino (LArTPC) | Extensive simulations [^833^] | LArSoft/ROOT | FNAL collaboration | Sparse CNN triggers active [^837^] |
| LIGO/Virgo/KAGRA O4 | Gravitational wave | 149 significant candidates [^863^] | GraceDB, GCN/TAN | Public (GraceDB) [^860^] | Ready for counterpart search ML |
| GOTO | Optical follow-up | ~1M detections processed (O4) [^862^] | Difference-image catalogs | Public alerts | Ready for rapid-response pipelines |
| SNAD | Multi-wavelength anomaly | 2.25M ZTF objects analyzed [^160^] | Web viewer, Python code | Public [^158^] | Ready for anomaly detection models |
| Zooniverse SN Hunters | Human labels | Active classification stream | Web interface | Public [^321^] | Ready for real/bogus training data |
| Galaxy Zoo W&W | Human labels | ~200,000 images classified [^876^] | Image classifications | Public | Orthogonal labels to ML scores [^887^] |

**Analytical interpretation.** Several patterns emerge from this comparison. First, the data sources cluster into three distinct readiness tiers. Tier 1—comprising SNEWPY, SNEWS 2.0, SNAD, and GOTO—offers programmatic or pip-installable access with immediate ML applicability. Tier 2—including IceCube, DUNE, and ThunderKAT—contains scientifically rich data but requires collaboration membership or specialized domain knowledge to access and process. Tier 3—exemplified by LoTSS DR3's 18.6 PB archive—offers public access at a scale that demands significant computational infrastructure before ML can be applied.

Second, the small-sample problem is pervasive across messengers. Radio supernovae face the most acute constraint (3 SN-related sources in VAST DR1, 87 light curves for MALT), but GW-electromagnetic counterparts are comparably scarce, with only a handful of confirmed multi-messenger events to date. Neutrino astrophysics sidesteps this limitation through simulation: SNEWPY provides hundreds of models and DUNE's LArSoft framework generates effectively unlimited simulated detector images, though the simulation-to-reality gap remains a systematic concern for models deployed on real detector data.

Third, the emergence of broker-based alert distribution—connecting GW detectors, neutrino observatories, and optical follow-up facilities through standardized alert packets—creates an architectural foundation for real-time multi-messenger ML. The seven Rubin community brokers (ALeRCE, AMPEL, ANTARES, Fink, Lasair, and Pitt-Google [^44^]) already process and classify alerts from ZTF, and their extension to multi-messenger streams is underway. For ML practitioners, the most actionable strategy is to design pipelines that consume broker-classified alerts as input features, supplementing traditional photometric and contextual features with messenger-specific signals such as GW skymap probability, neutrino burst significance, and citizen science anomaly scores. This multi-stream fusion approach, while technically demanding due to heterogeneous formats and cadences, represents the frontier where the next generation of supernova discovery algorithms will operate.

---

## 12. Data Access Patterns & Python Ecosystem

Supernova data is distributed across a complex ecosystem of formats, protocols, and access tools. No single format dominates: cosmology analyses rely on SNANA FITS, real-time brokers stream Avro packets, columnar analytics favor Parquet, and web APIs return JSON. An ML practitioner building a training set from multiple surveys must therefore ingest and normalize data across all of these formats. This chapter provides a practical guide to each format's structure, the Python libraries that read them, bulk download strategies for large datasets, and a recommended five-stage pipeline that unifies multi-format ingestion into a single workflow.

### 12.1 File Formats Deep Dive

#### 12.1.1 SNANA FITS: The Cosmology Standard

The SNANA software package uses a dual-file FITS format that has become the de facto standard for large-scale supernova simulations and cosmology analyses [^848^][^102^]. Each dataset comprises two paired binary-table files. The HEAD.fits file contains one row per supernova with metadata including SNID, right ascension, declination, redshift (heliocentric and CMB-corrected), peak MJD, SALT2 fit parameters (mB, x1, c), and classification flags. The PHOT.fits file contains one row per photometric epoch with MJD, filter, calibrated flux, flux error, zero point, and PSF parameters. A pointer column (SNID) connects each photometry row back to its parent entry in the HEAD file [^99^][^98^].

This split design is efficient for analyses that iterate over object metadata without loading photometry, or that vectorize operations across light curves. The `sncosmo` library provides native support: `sncosmo.read_snana_fits('HEAD.fits', 'PHOT.fits')` returns an iterator over supernova objects, each exposing both metadata (via `sn.meta`) and photometry columns (via `sn['MJD']`, `sn['FLUXCAL']`). For lower-level access, `astropy.table.Table.read()` loads either file directly [^848^][^870^]. Major releases in this format include SDSS-II DR7, DES 5-Year, Pantheon, Pantheon+, and Foundation DR1.

#### 12.1.2 Avro: Rubin Alert Packets

Apache Avro is a compact binary serialization format that embeds its schema within each file, enabling both schema evolution and compact transmission. It is the native format of the Rubin Observatory alert stream [^810^][^811^]. Each alert packet contains a diaSource record (the triggering 5-sigma detection), an associated diaObject record (aggregated history), up to 12 months of previous detections in prvDiaSources, forced photometry in prvDiaForcedSources, and three 30x30 pixel FITS cutouts (science, template, difference) [^290^][^914^][^915^].

The `fastavro` library is the recommended Python reader. It exposes both the embedded schema and packet contents through a streaming interface that does not require the entire file to be loaded into memory:

```python
import fastavro

with open('alerts.avro', 'rb') as f:
    reader = fastavro.reader(f)
    schema = reader.schema  # Extract embedded schema
    for packet in reader:
        dia_source = packet['diaSource']
        prv_sources = packet.get('prvDiaSources', [])
        cutout = packet.get('cutoutScience', {}).get('stampData')
```

This streaming-friendly design is critical at Rubin scale: the observatory produces 7–10 million alerts per night, each approximately 82 KB in size with history and cutouts, yielding a nightly alert volume of roughly 1 TB [^929^][^50^][^210^]. The ZTF collaboration uses a similar Avro schema documented at the ztf-avro-alert repository [^108^].

#### 12.1.3 JSON: Open Supernova Catalog

The Open Supernova Catalog (OSC) stores one JSON file per supernova, making it human-readable and web-native but comparatively inefficient for bulk analysis [^651^][^866^]. Each file follows the astroschema specification and contains nested structures for aliases, photometry arrays, spectral data, redshift measurements, and host-galaxy associations. Photometry entries include time, band, magnitude, error, upper-limit flags, and provenance (telescope/instrument).

The per-file granularity means that loading 10,000 supernovae requires 10,000 individual file operations. For small-scale projects or web API access, this is acceptable; for ML training sets exceeding hundreds of thousands of objects, converting to Parquet or HDF5 after ingestion is strongly recommended. The OSC API (`api.astrocats.space`) enables direct programmatic queries that return JSON responses without requiring a local clone of the repository.

#### 12.1.4 Parquet: Columnar Storage for Modern Surveys

Apache Parquet is a columnar storage format with efficient compression and predicate pushdown, making it well suited for ML workflows that select subsets of columns across large datasets. It has been adopted by the Roman Space Telescope Hourglass simulation and the LSST DESC DC2 data release [^328^][^269^][^750^].

The Roman Hourglass release on Zenodo provides three Parquet files: `hourglass_objects.parquet` (~65,000 rows, one per object), `hourglass_photometry.parquet` (millions of rows, one per flux measurement), and `hourglass_spectra.parquet` (one per object per epoch) [^328^][^269^]. Reading with `pandas.read_parquet()` or `pyarrow.parquet` supports column selection at parse time, so loading only `[cid, ra, dec, z_cmb, class]` avoids reading the full file into memory. The DESC DC2 Object Catalog (~180 GB) and cosmoDC2 (>5 TB) are accessible through `GCRCatalogs` or via the DESC Data Portal [^750^].

#### 12.1.5 VOTable: The Virtual Observatory Standard

VOTable is the IVOA-standard XML format for astronomical tabular data, returned by Virtual Observatory services including VizieR, SIMBAD, and TAP/ADQL queries [^861^]. Three encoding variants exist: TABLEDATA (XML string storage, human-readable but verbose), BINARY (Base64-encoded, compact), and BINARY2 (binary with null-value masking, recommended for new data) [^861^]. Astropy's `astropy.io.votable` module provides parsing via `parse_single_table('catalog.xml').to_table()`, which converts a VOTable directly into an `astropy.table.Table`. For large catalogs downloaded from VO services, converting the resulting table to Parquet after ingestion typically reduces file size by 50–70% and improves subsequent read performance.

**Table 1** compares the six formats most commonly encountered in supernova ML workflows. The ratings for read/write speed and file size are relative to the full set; the "Best For" column reflects the primary design target of each format.

| Format | Structure | Best For | Python Tool | Read Speed | Write Speed | File Size |
|---|---|---|---|---|---|---|
| SNANA FITS | HEAD+PHOT paired tables | Large simulations, cosmology | sncosmo, astropy.io.fits | Fast | Fast | Medium |
| Avro | Binary packets with embedded schema | Streaming alerts, brokers | fastavro | Very Fast | Very Fast | Small |
| JSON (OSC) | Per-SN files | Human-readable, web APIs | json, pandas | Slow | Slow | Large |
| Parquet | Columnar, compressed | Analysis, ML training | pandas, pyarrow | Very Fast | Very Fast | Small |
| VOTable | XML tables | VO queries, interoperability | astropy.io.votable | Medium | Slow | Large |
| HDF5 | Hierarchical datasets | Large simulations | h5py, pandas | Fast | Fast | Medium |

*Table 1. Format comparison for supernova data access. Read/write speed and file size ratings are relative comparisons across the full set of formats. HDF5 is included as it remains common for DESC DC2 and cosmoDC2 despite Parquet adoption in newer releases.*

The most consequential implication of this comparison is that **no single format is optimal across all pipeline stages**. Avro excels for streaming ingestion but lacks columnar query efficiency. Parquet is ideal for training-data storage but cannot represent schema-evolving alert streams. SNANA FITS remains the cosmology standard but requires `sncosmo` or astropy and does not natively support modern features like embedded schema or predicate pushdown. ML practitioners should plan for format conversion at ingestion time rather than attempting to work in native formats throughout.

### 12.2 Python Access Libraries

#### 12.2.1 astroquery: Unified Archive Interface

`astroquery` provides a unified Python interface to dozens of astronomical archives, abstracting over protocol differences across services [^845^][^854^]. For supernova research, the most relevant modules query VizieR (published catalogs), SIMBAD (object identifications and bibliography), HEASARC (X-ray and high-energy data), MAST (Hubble, TESS, Pan-STARRS), NED (extragalactic redshifts and classifications), and IRSA (infrared photometry). Each module follows a consistent pattern: instantiate a query object, optionally set row limits and column selections, then call `query_region()` or `query_object()` with an astropy `SkyCoord`.

#### 12.2.2 pyvo: TAP/ADQL and Registry Search

`pyvo` implements Virtual Observatory protocols at a lower level than astroquery, providing direct access to Table Access Protocol (TAP) services through ADQL queries [^941^][^857^]. TAP services support complex queries with geometric constraints (CONTAINS, CIRCLE, POLYGON) that are not always available through simpler HTTP interfaces. For Rubin data, TAP queries via pyvo are the primary mechanism for accessing DP0/DP1 catalogs from outside the Rubin Science Platform. Registry search (`vo.registry.search`) enables discovery of services by data model or keyword, which is valuable when tracking down auxiliary data (e.g., finding all cone-search services that index supernova catalogs) [^941^].

#### 12.2.3 HEASARC AWS S3: Bulk Download Without Egress Charges

HEASARC has made its entire mission archive (>50 TB) available as an AWS Open Dataset at `s3://nasa-heasarc/` [^37^][^864^]. Data can be downloaded with the AWS CLI using `--no-sign-request`, which incurs no egress charges and requires no AWS account. The astroquery HEASARC module also supports cloud-hosted downloads via `heasarc.download_data(links, host='aws')` [^860^]. For bulk transfers, `aws s3 sync --no-sign-request` provides incremental synchronization that skips unchanged files, making it suitable for maintaining local mirrors that update nightly.

#### 12.2.4 Globus: High-Speed Transfer for DESC and Rubin Datasets

The DESC Data Portal uses Globus for transfers of large datasets including DC2 Object+Truth Match (~180 GB) and cosmoDC2 (>5 TB) [^750^]. Globus handles authentication, endpoint management, and parallel TCP streams automatically, achieving transfer rates that saturate institutional network connections. It is the recommended channel for any dataset exceeding ~10 GB where AWS S3 is not available.

### 12.3 Bulk Download Strategies

Four strategies cover the bulk-download needs of most supernova ML projects. For static URL lists (e.g., published data-release files), `wget -i urls.txt` with `xargs -P 8` for parallelization provides the simplest approach. For HEASARC and OpenUniverse2024 data, `aws s3 sync --no-sign-request` enables incremental synchronization without authentication or egress costs [^864^][^37^]. For DESC DC2 and cosmoDC2, Globus provides reliable high-throughput transfer with automatic retry and checksum verification [^750^]. For Rubin DP0/DP1 catalog data, TAP queries through the Rubin Science Platform (RSP) or via pyvo from external hosts allow precise subset extraction using ADQL constraints, avoiding the need to download full catalog dumps [^787^].

### 12.4 Recommended ML Data Pipeline

#### 12.4.1 Five-Stage Architecture

A robust ML data pipeline for supernova research can be decomposed into five stages. **Stage 1 (Acquisition)** selects the appropriate download strategy based on dataset size and location: S3 sync for HEASARC, Globus for DESC, TAP queries for Rubin catalogs, wget for static releases, and Kafka subscription for real-time alert streams. **Stage 2 (Ingestion and Normalization)** detects the input format, validates against expected schemas, standardizes column names (e.g., mapping `FLT` → `band`, `FLUXCAL` → `flux`), converts to a common magnitude system, and applies quality cuts on signal-to-noise ratio, real-bogus score, and bad-pixel flags. **Stage 3 (Feature Extraction)** interpolates light curves to a common time grid, computes photometric features (rise time, decline rate, color indices), extracts image features from cutouts where available, and augments with contextual data (host galaxy, redshift, Milky Way extinction). **Stage 4 (Dataset Construction)** performs train/validation/test splits (temporal splits are preferred over random splits for time-domain data), balances class representation, scales features, pads sequences for recurrent or transformer models, and converts to the target ML framework format (TFRecord, HDF5, or Arrow). **Stage 5 (Training and Iteration)** uses incremental data loaders for large datasets, active learning to prioritize uncertain objects for labeling, and experiment tracking for reproducibility.

**Table 2** maps each pipeline stage to recommended tools and viable alternatives.

| Stage | Recommended Tools | Alternatives |
|---|---|---|
| Acquisition (S3) | `aws s3 sync --no-sign-request` | astroquery HEASARC module |
| Acquisition (Globus) | Globus Connect Personal + Portal | rsync (for smaller sets) |
| Acquisition (TAP/ADQL) | pyvo TAP queries | astroquery region queries |
| Acquisition (alerts) | fastavro + KafkaConsumer | Broker Python clients (ALeRCE, Fink) |
| Ingestion (FITS) | sncosmo.read_snana_fits() | astropy.io.fits.Table.read() |
| Ingestion (Avro) | fastavro.reader() | lsst-alert-packet |
| Ingestion (Parquet) | pandas.read_parquet() | pyarrow.parquet.ParquetFile |
| Ingestion (JSON) | json + pandas | requests (for API access) |
| Ingestion (VOTable) | astropy.io.votable.parse_single_table() | pyvo TAP output |
| Normalization | pandas DataFrame operations | astropy.table operations |
| Feature Extraction | sncosmo, custom numpy/scipy | SuperNNova feature module |
| Dataset Construction | pandas/pyarrow + sklearn | Dask (for out-of-core) |
| Training | PyTorch DataLoader, TensorFlow TFRecord | Dask-ML, Ray Train |

*Table 2. Recommended tools by pipeline stage, with alternatives. The primary recommendation is the tool that provides the best balance of reliability, performance, and ecosystem integration for supernova data workflows.*

The key design principle emerging from this table is **layered abstraction**: use low-level libraries (fastavro, astropy.io.fits, pyarrow) for ingestion where format-specific handling is required, then convert to pandas DataFrames or astropy Tables for normalization and feature extraction, and finally export to framework-native formats (TFRecord, PyTorch Dataset) for training. This avoids coupling the model-training code to any specific astronomical data format.

#### 12.4.2 Unified SNDatasetPipeline Class

The following `SNDatasetPipeline` class demonstrates the multi-format loading pattern. It encapsulates format-specific readers behind a common interface, converts all inputs to standardized pandas DataFrames with consistent column names (`mjd`, `band`, `flux`, `fluxerr`, `snid`, `redshift`), applies quality cuts, and provides a conversion back to sncosmo Tables for downstream analysis:

```python
import pandas as pd
import numpy as np
from astropy.table import Table, vstack
import sncosmo
import pyarrow.parquet as pq
from pathlib import Path

class SNDatasetPipeline:
    """ML-ready supernova data pipeline supporting multi-format ingestion."""

    def __init__(self, cache_dir='./cache'):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def load_snana_fits(self, head_file, phot_file):
        """Load SNANA FITS data into standardized DataFrame format."""
        sne = sncosmo.read_snana_fits(head_file, phot_file)
        standardized = []
        for sn in sne:
            df = pd.DataFrame({
                'mjd': sn['MJD'],
                'band': sn['FLT'],
                'flux': sn['FLUXCAL'],
                'fluxerr': sn['FLUXCALERR'],
                'zp': sn.get('ZPFLUX', 25.0),
                'snid': sn.meta.get('SNID', 'unknown')
            })
            df['redshift'] = sn.meta.get('ZHEL', np.nan)
            standardized.append(df)
        return pd.concat(standardized, ignore_index=True)

    def load_parquet(self, filepath, columns=None):
        """Load Parquet data with optional column selection for efficiency."""
        return pd.read_parquet(filepath, columns=columns)

    def load_avro_alerts(self, filepath):
        """Load Avro alert packets and extract source measurements."""
        import fastavro
        alerts = []
        with open(filepath, 'rb') as f:
            for packet in fastavro.reader(f):
                dia = packet['diaSource']
                alerts.append({
                    'diaSourceId': dia['diaSourceId'],
                    'ra': dia['ra'],
                    'dec': dia['decl'],
                    'mjd': dia['midPointTai'],
                    'mag': dia.get('mag', np.nan),
                    'band': dia.get('filterName', '')
                })
        return pd.DataFrame(alerts)

    def apply_quality_cuts(self, df):
        """Apply standard quality cuts for SN data."""
        if 'rb' in df.columns:  # ZTF real-bogus score
            df = df[df['rb'] >= 0.65]
        if 'nbad' in df.columns:
            df = df[df['nbad'] == 0]
        if 'fluxerr' in df.columns:
            df = df[df['fluxerr'] > 0]
        return df.reset_index(drop=True)

    def to_sncosmo_format(self, df, snid_col='snid'):
        """Convert standardized DataFrame to list of sncosmo Tables."""
        tables = []
        for snid, group in df.groupby(snid_col):
            t = Table.from_pandas(group)
            t.meta['SNID'] = snid
            tables.append(t)
        return tables
```

This class addresses the "Format Tower of Babel" problem identified in cross-dimensional analysis: each survey chose a format optimized for its own operational constraints, but ML pipelines must ingest from multiple sources. By standardizing immediately after format-specific reading, downstream feature extraction and model training code becomes format-agnostic. A production deployment would extend this skeleton with schema validation (using `jsonschema` for JSON, `lsst-alert-packet` for Avro), unit conversion to a common zero-point system, and integration with a caching layer (e.g., `pickle` or `diskcache`) to avoid re-ingesting unchanged files.

### 12.5 Data Volume Estimates

Understanding data volumes is essential for selecting appropriate storage and processing infrastructure. The Rubin Observatory generates the largest data products in the field: ~20 TB of raw imaging per night, producing 7–10 million alert packets that sum to approximately 1 TB nightly [^929^][^931^]. The 10-year catalog volume is projected at 15 PB with 37 billion objects [^940^]. At the other end of the scale, compiled cosmology samples such as Pantheon+ (~1,500 SNe Ia) occupy roughly 500 MB in SNANA FITS format, and the full Open Supernova Catalog is approximately 2 GB of JSON [^651^][^102^].

| Scale | Size Range | Typical Datasets | Format Recommendation | Processing Strategy |
|---|---|---|---|---|
| Small | 100 MB – 1 GB | Pantheon+, Foundation DR1, CSP DR3 | Parquet or HDF5 | Load entirely into memory |
| Medium | 1 – 10 GB | Roman Hourglass, OSC full catalog | Parquet + lazy loading | pandas/pyarrow selective columns |
| Large | 100+ GB | DESC DC2, ZTF alerts (cumulative) | Parquet/Arrow + Dask | Out-of-core, partitioned processing |
| Stream | 1+ TB/day | Rubin alert stream | Avro + Kafka | Real-time filtering, cloud-native |

*Table 3. Storage requirements and processing strategies by dataset scale. The format recommendation reflects the need for efficient columnar access at medium-to-large scales and streaming efficiency at the largest scale.*

For ML projects working at small scale (100 MB–1 GB), loading the entire dataset into memory as pandas DataFrames or astropy Tables is practical and simplifies exploration. At medium scale (1–10 GB), Parquet's columnar access becomes important: selecting only the subset of columns needed for a given model can reduce memory usage by an order of magnitude. At large scale (100+ GB), Dask or Ray Data provides out-of-core DataFrame operations that maintain a pandas-compatible API while partitioning work across cluster nodes. For the Rubin alert stream, real-time processing requires a fundamentally different architecture: alerts must be filtered, classified, and either persisted or discarded within seconds of arrival, using streaming frameworks (Kafka, Apache Spark) rather than batch processing [^719^][^59^].

The practical implication for most ML practitioners is that the **medium scale** (1–10 GB) is the relevant target for current training sets. Datasets at this scale—Roman Hourglass, full OSC, ELAsTiCC subsets—fit comfortably on a single workstation with Parquet-based selective loading, while providing enough diversity (tens of thousands to hundreds of thousands of objects) to train deep-learning classifiers effectively. As Rubin data volumes grow through DP2 and beyond, pipelines that already use Parquet and lazy-loading patterns will scale naturally to the large-scale regime without requiring architectural redesign.

---

## 13. Strategic Insights & Recommendations

### 13.1 The Ten Cross-cutting Insights

The preceding chapters surveyed the full landscape of supernova datasets, software frameworks, alert brokers, and emerging data streams. This section distills that analysis into ten insights that cross-cut multiple dimensions, each representing a strategic consideration for any supernova ML project.

#### 13.1.1 The Low-z Anchor Bottleneck: Only ~3,000 Spec-Confirmed SNe Ia Exist — Domain Adaptation Is Essential

The most fundamental constraint on supernova ML is not computational capacity or algorithmic sophistication — it is the scarcity of spectroscopically confirmed training labels at low redshift. Across all publicly available low-z anchor surveys, the total inventory amounts to approximately 3,000 spec-confirmed SNe Ia: CSP DR3 (134 SNe with optical and NIR photometry) [^166^], the CfA archive (~278 SNe spanning two decades) [^398^][^399^], Foundation DR1 (225 SNe observed with Pan-STARRS1) [^426^], PS1-MDS (365 spec-Ia), and YSE DR1 (1,975 SNe, though the majority are photometrically classified). This entire empirical foundation supports classifiers trained on millions of simulated events. The ratio of simulated-to-real training data is approximately 1,000:1, creating severe overfitting risk to simulation artifacts.

The practical implication is that domain adaptation techniques are essential, not optional. Adversarial domain adaptation aligns simulated and real feature distributions by training a discriminator against domain-invariant representations. Transfer learning pre-trains on simulations and fine-tunes on the small real labeled set. Active learning uses broker-classified alerts to iteratively expand labeled pools — Fink's system demonstrated 86% spectroscopic confirmation purity on 535 candidates [^729^]. Foundation's homogeneous PS1 photometry makes it particularly valuable as a validation set for these experiments [^426^].

#### 13.1.2 The Format Tower of Babel: 7+ Formats Require Normalization — Build a Format Pipeline Early

Supernova data exists in at least seven major formats, each chosen for operational reasons rather than interoperability. SNANA FITS (paired HEAD+PHOT binary tables) dominates historical releases [^848^] and is the native format of DES, Pantheon+, and Foundation. Apache Avro serves the Rubin alert stream, embedding schema for streaming efficiency [^810^][^811^]. Apache Parquet is used by Roman Hourglass [^328^], DESC DC2 [^370^], and ZTF bulk light curves [^9^]. JSON underpins the Open Supernova Catalog. VOTable supports Virtual Observatory queries. HDF5 stores OpenUniverse2024 SED time series. ASCII persists in CSP DR3 photometry and TESS light curves.

No single tool reads all formats. sncosmo reads SNANA FITS natively [^35^] but cannot handle Avro or Parquet. lsst-alert-packet handles Avro only [^809^]. The sndata package provides a partial abstraction layer. Any ML project ingesting multiple surveys must invest in format normalization before model development — a hidden cost that frequently exceeds training effort. The recommended strategy is to build a format-agnostic ingestion pipeline as the first project step, converting all inputs into a standardized DataFrame. Budget 20–30% of total development time for this normalization.

#### 13.1.3 Broker ML as a Service: Query Broker APIs Before Retraining from Scratch

Alert brokers have evolved from data distributors to ML platforms that amortize classification costs across the community. ALeRCE uses a CNN stamp classifier (94% balanced accuracy) plus a Balanced Random Forest on light curve features [^685^][^698^]. Fink deploys SuperNNova RNNs and a pioneering active learning system [^729^]. ANTARES integrates the RAPID GRU-based classifier [^802^]. AMPEL runs ParSNIP VAEs within a modular tiered architecture [^740^]. Lasair provides SQL-based filtering with Sherlock host associations [^727^]. Pitt-Google operates cloud-native classifiers on GCP.

For most applications, querying broker APIs is more efficient than training custom classifiers. Fink has processed over 180 million alerts [^60^]; ALeRCE reported 6,846 SN candidates with 971 spectroscopic confirmations between 2019 and 2021 [^685^]. The recommended pattern is to treat broker classifications as input features and fine-tune only for novel targets. All seven brokers offer Python clients (`alerce` [^701^], `fink-client` [^699^], `lasair` [^43^]) enabling programmatic access with ~10 lines of code. The TOM Toolkit provides unified follow-up coordination across 13+ broker integrations [^820^].

#### 13.1.4 The NIR Blind Spot: NIR Training Data Is Scarce — Use Roman Simulations for Now

Near-infrared photometry is critical for high-redshift supernova cosmology because NIR wavelengths are less affected by dust extinction and provide better standard candle properties. Yet publicly available NIR training data is extremely scarce. CSP DR3 provides YJH photometry for 120 SNe — the largest real NIR sample — but covers only 134 total objects [^166^]. Euclid Q1 offers NISP measurements for 161 transients, the first significant space-based NIR sample [^824^]. JWST provides exquisite individual spectra but no systematic survey dataset.

The Roman Space Telescope's High-Latitude Time-Domain Survey (launch by May 2027) will transform this landscape. Until then, the Roman Hourglass simulation (64,000+ transients with NIR photometry and 500,000 spectra across 10 classes) [^622^][^328^] is the most realistic NIR training data available. OpenUniverse2024 adds joint Roman+Rubin coverage across 70 deg² with ~1.4 million transient objects [^301^]. ML practitioners developing dust-robust or high-z classifiers should prioritize Hourglass + OpenUniverse2024 NIR data for training, with validation on the limited real NIR samples from CSP DR3 and Euclid Q1.

#### 13.1.5 The Sim-to-Real Chasm: Always Validate Simulation-Trained Models on Real Spec-Confirmed Samples

Multiple converging lines of evidence demonstrate that simulation-trained classifiers degrade on real data. SNPCC explicitly benchmarked this effect [^239^]. PLAsTiCC winners showed varying performance on real ZTF data. The SuperNNova framework notes that "performance strongly depends on training set representativeness" [^256^]. DES mitigates with 25 separate mock simulations [^456^]. Five root causes persist: host galaxy confusion, calibration systematics, weather/seeing variations, real-bogus artifacts, and rare subclass distributions. The accuracy degradation ranges from 5% (well-tuned simulations) to 15% (idealized simulations).

The mitigation strategy is threefold. Always validate on real spec-confirmed samples (CSP, CfA, Foundation). Use domain adaptation (DANN, adversarial training) when real labels are scarce. Incorporate active learning loops where broker-classified alerts are spectroscopically confirmed and fed back into training — Fink demonstrated this successfully, with its active learning strategy outperforming random selection after ~60 new labeled objects while saving ~1.5 nights of follow-up versus ~5.3 nights [^726^][^689^].

#### 13.1.6 7-Broker Divergence: Ensemble Across Brokers, Use Disagreement as Anomaly Signal

The seven Rubin community brokers use different architectures, training data, and optimization objectives, leading to non-trivial disagreements for ~5–10% of transients. ALeRCE optimizes for hierarchical taxonomy depth; Fink for early SN Ia purity; AMPEL for modular flexibility; ANTARES for speed. This divergence is both a risk (science results may depend on broker choice) and an opportunity. The SNAD project explicitly uses multi-algorithm outlier scores as anomaly indicators, identifying 144 new SN candidates in ZTF data through a 3-stage pipeline of feature extraction, outlier search, and expert verification [^158^][^160^].

The recommended strategy is to query multiple brokers per object and treat disagreement as a signal for deeper investigation. Simple ensemble averaging typically outperforms any individual broker. Broker disagreement itself is a high-value anomaly detection feature — objects where ALeRCE classifies as SN, Fink as AGN, and AMPEL as uncertain warrant immediate attention. The ELAsTiCC taxonomy [^334^] provides partial standardization, but full interoperability remains an active development area.

#### 13.1.7 The Spectra Bottleneck: 72K WISeREP Spectra Exist but Need Preprocessing — SNID-SAGE Helps

WISeREP hosts 72,503 spectra for 29,468 objects from over 30 instruments [^116^], making it the largest SN spectroscopic archive by an order of magnitude. However, varying resolutions (R ~ 100–10,000), wavelength ranges, signal-to-noise ratios, and calibration methods create a substantial gap between "spectra available" and "ML-ready features." Unlike photometry — where SNANA FITS standardizes format — spectroscopic data lacks a unified ML representation.

Classification tools are emerging to bridge this gap. SNID-SAGE is a modern Python replacement for classic SNID, providing 698 templates across all major SN types and having classified ~46,000 WISeREP spectra [^753^][^754^]. DASH uses a CNN to classify spectra directly, achieving 97.5% type accuracy within specific windows. The recommended workflow: query WISeREP via `wiserep_api` (`pip install wiserep_api`) [^430^]; classify with SNID-SAGE; resample onto a common wavelength grid; normalize and mask telluric regions; extract line equivalent widths as supplemental features. Self-supervised pre-training on the full spectral corpus remains a largely unexplored high-value opportunity.

#### 13.1.8 The Rubin Readiness Window: 12-Month Window to Develop on DP0+ELAsTiCC2 Before Restrictions

From mid-2025 through approximately mid-2027, an unprecedented convergence of publicly accessible datasets enables pre-development of Rubin-era classifiers. Rubin DP0 (DESC DC2 simulation, ~181 GB) is available via the Rubin Science Platform and Globus [^370^][^749^]. DP1 (real commissioning data, 48 nights, ~3.5 TB with 2.3 million objects) was released in June 2025 [^767^]. ELAsTiCC2 (~4 million objects, ~50 million detections in SNANA FITS and Avro) is at NERSC [^334^][^674^]. Roman Hourglass (64,000+ transients with photometry and spectra in Parquet) is on Zenodo [^328^]. OpenUniverse2024 (400 TB of joint Roman+Rubin synthetic imaging) is on AWS S3 [^302^].

After this window, Rubin's data rights policy imposes a 2-year proprietary period [^765^]. Immediate priorities: download ELAsTiCC2 and develop baseline classifiers; use DP0 for pipeline testing and DP1 for sim-to-real validation; train joint Roman+Rubin models on OpenUniverse2024; publish benchmark results before the full Rubin stream at 7–10 million alerts per night dominates the literature [^793^][^929^].

#### 13.1.9 Citizen Science Underutilization: Millions of Human Labels Going Untapped

Citizen science projects have produced millions of human classifications rarely used in production ML training. Zooniverse Supernova Hunters engages volunteers in real-vs-bogus classification [^321^]. Galaxy Zoo: Weird and Wonderful involved ~2,000 volunteers examining ~200,000 Subaru images [^876^]. Critically, GZ:W&W found no appreciable correlation between ML anomaly scores and human anomaly fractions [^887^], demonstrating that citizen scientists detect patterns orthogonal to algorithmic classifiers. The SNAD project leveraged this complementarity, identifying 144 new SN candidates through its ML+human pipeline [^158^].

The underutilization stems from production pipelines prioritizing speed and reproducibility over integrating heterogeneous human labels. Semi-supervised approaches that apply human labels to low-confidence ML predictions offer a pragmatic path forward. Active learning loops — where ML systems select candidates for human verification and verified labels feed back into training — have demonstrated clear success. Fink's active learning saved ~1.5 nights of follow-up observation compared to ~5.3 nights with random selection after accumulating ~60 labeled objects [^726^][^689^].

#### 13.1.10 Python Ecosystem Maturation: From Scripts to pip-Installable Production Pipelines

The supernova ML software ecosystem has undergone rapid maturation since 2020. The foundational layer is sncosmo (118+ citations, `pip install sncosmo`), providing SALT2/SALT3 fitting, 100+ bandpasses, and SNANA FITS I/O [^35^]. Deep learning frameworks include SuperNNova (`pip install supernnova`, 100+ citations, 96.9% Ia accuracy without redshift) [^256^]; ParSNIP (redshift-invariant VAE, 50+ citations) [^79^]; and BTSbot (`pip install btsbot`, 93–96% purity, pre-trained models on HuggingFace) [^888^]. Broker access is streamlined: `pip install fink-client` [^699^], `pip install alerce` [^701^], `pip install lasair` [^43^]. Emerging tools include SNID-SAGE (`pip install snid-sage`) [^753^], LightCurveLynx/ tdastro for forward modeling [^752^], and PIPPIN for end-to-end cosmology orchestration.

This maturation creates a flywheel effect: easier installation drives more users, more users generate feedback that improves code, and better code attracts more citations and investment. The entry barrier has dropped from months of custom development to days of package installation. The ecosystem is converging on sncosmo as the universal data layer, broker APIs as the universal classification layer, and pip-installable packages as the universal distribution mechanism. Reproducibility is improving but still requires attention — version pinning, containerization, and deterministic seeds remain best practices rather than defaults.

### 13.2 Recommended Actions by Project Type

#### 13.2.1 Table: Project Type → Datasets → Tools → Validation Strategy

The insights above apply differentially depending on project type. Table 13.1 maps five common archetypes to recommended resources.

| Project Type | Primary Datasets | Software Tools | Validation Strategy |
|:---|:---|:---|:---|
| **Real-time classification** | ELAsTiCC2 (~4M objects, ~50M detections) [^334^]; ZTF DR20+ Parquet LCs [^9^]; Rubin DP0 truth catalogs (~500K sim SNe) [^370^] | `alerce` / `fink-client` APIs [^701^][^699^]; SuperNNova (`pip install supernnova`) [^256^]; `lsst-alert-packet` [^809^] | Validate on ZTF SN Ia DR2 (3,628 spec-confirmed) [^1^]; test accuracy at <3 days post-detection; measure purity/completeness with broker ensemble |
| **Cosmology & distance estimation** | Pantheon+ (1,701 SNe Ia, 18 surveys) [^451^]; Foundation DR1 (225) [^426^]; CSP DR3 (134 + NIR) [^166^]; DES-SN5YR (1,635 + 25 mocks) [^342^]; Union3 (2,087) [^189^] | `sncosmo` [^35^]; SNANA + PIPPIN [^254^]; SALT2/SALT3 fitting; CosmoSIS | Train on DES mocks [^456^]; validate on spec-confirmed low-z anchors; test Hubble residual scatter; propagate covariance [^660^] |
| **Anomaly detection** | SNAD ZTF DR3 (2.25M objects) [^160^]; ZTF alerts via brokers; OSC (50,000+ SNe) [^6^]; GZ:W&W labels (~200K images) [^876^] | SNAD pipeline (`zwad`) [^694^]; ParSNIP outlier scoring [^79^]; scikit-learn isolation forest/LOF; broker disagreement features | Cross-validate on known unusual objects (SLSN-I, TDE); test broker ensemble disagreement; measure contamination at fixed recall; spectroscopic follow-up |
| **Spectroscopic classification** | WISeREP (72,503 spectra) [^116^]; CfA (2,603 spectra of 462 SNe Ia) [^398^]; BSNIP (1,298 spectra); SNfactory (300+) [^150^] | SNID-SAGE (`pip install snid-sage`) [^753^]; DASH CNN (97.5% accuracy); `wiserep_api` [^430^] | 20% WISeREP holdout stratified by instrument; validate redshift against host spec-z; test on instruments not in training; cross-match with photometric types |
| **Future survey prep** | OpenUniverse2024 (~400 TB, joint Roman+Rubin) [^301^]; Hourglass (64K+, Parquet) [^328^]; Rubin DP0/DP1 [^370^][^767^]; ELAsTiCC2 Avro [^334^] | `phrosty` GPU DIA [^764^]; `GCRCatalogs` [^745^]; `lsst-alert-packet` [^809^]; SuperNNova/ParSNIP baselines | Validate on DP1 real data; test throughput at >1M alerts/night; cross-validate Hourglass on OpenUniverse overlap; publish pre-Rubin benchmarks |

**Table 13.1.** Recommended datasets, tools, and validation strategies by project type. All resources are publicly available as of mid-2025.

#### 13.2.2 For Real-Time Classifiers: ELAsTiCC2 + Broker APIs + ALeRCE/Fink Clients

Real-time classifiers face latency budgets of seconds, incomplete light curves at detection, and purity requirements to avoid wasting limited spectroscopic follow-up. Begin with ELAsTiCC2 training data (~4 million objects in SNANA FITS, downloadable from NERSC [^334^]), which provides the most realistic Rubin alert stream simulation available. The training set (`ELASTICC2_TRAIN_02.tar.bz2`, 7.4 GiB) includes updated rolling cadence and Deep Drilling Field coverage.

Use SuperNNova as the baseline RNN architecture (`pip install supernnova` [^256^]) or ALeRCE's open-source classifier implementations [^701^]. Critical validation: test on ZTF SN Ia DR2 (3,628 spec-confirmed SNe Ia) [^1^] to measure the sim-to-real gap. Early classification accuracy at <3 days post-detection is the key metric — Fink's deployment classifies a median 6 days before peak brightness [^729^]. Integrate broker APIs from the start: `alerce` provides probabilities, light curves, and stamps [^701^]; `fink-client` provides 60+ science topics [^699^]. Ensemble across brokers; use disagreement as an anomaly signal for uncertain objects.

#### 13.2.3 For Cosmology: Pantheon+ + Foundation + CSP + sncosmo + SNANA

Cosmological analyses require precise photometry with robust systematic uncertainty propagation. Pantheon+ (1,701 SNe Ia from 18 surveys with full STAT+SYS covariance matrices) [^451^] is the gold standard, available via GitHub with CosmoSIS likelihood modules. Foundation DR1 (225 SNe Ia with homogeneous PS1 photometry) [^426^] and CSP DR3 (134 SNe Ia, the only significant real NIR coverage) [^166^] provide the highest-quality low-z anchors. DES-SN5YR (1,635 cosmology-grade SNe Ia) [^342^] offers the largest single-instrument sample with 25 included mock simulations.

The software stack centers on sncosmo for light curve fitting with SALT2/SALT3 models [^35^], SNANA for simulation and cosmology fitting [^254^], and PIPPIN for pipeline orchestration. Union3 (2,087 SNe Ia) [^189^] provides cross-checks via the UNITY1.5 Bayesian framework, though the full unbinned catalog release is pending. Validation must emphasize systematics: use 25 DES mocks [^456^] for robust training, test Hubble diagram residual scatter on spec-confirmed anchors, and incorporate covariance matrices into ML loss functions [^660^].

#### 13.2.4 For Anomaly Detection: SNAD Pipeline + ZTF DR + Citizen Science Labels

Anomaly detection identifies rare transients — SLSNe, TDEs, kilonovae, pair-instability SNe — that classifiers may miss due to training set underrepresentation. The SNAD project provides the most mature open-source pipeline, combining feature extraction, outlier search (isolation forest, local outlier factor), and expert verification through the SNAD Viewer [^158^][^160^]. On ZTF DR3, SNAD analyzed 2.25 million objects and identified 144 new SN candidates [^158^].

Training data: ZTF alerts via broker APIs, the Open Supernova Catalog (50,000+ SNe for population context) [^6^], and GZ:W&W citizen science labels (~200,000 images with human anomaly flags) [^876^]. ParSNIP outlier scoring (90% purity on novel transients) provides a strong baseline [^79^]. Broker disagreement (5–10% of objects) adds signal. Validate on known unusual objects; the key metric is contamination rate at fixed recall. Coordinate spectroscopic follow-up via the TOM Toolkit.

#### 13.2.5 For Spectroscopic Classifiers: WISeREP + SNID-SAGE + DASH

Spectroscopic classifiers operate on higher-dimensional data but face greater preprocessing challenges. WISeREP (72,503 spectra for 29,468 objects) [^116^] is the primary corpus, accessible via `wiserep_api` (`pip install wiserep_api` [^430^]). CfA adds 2,603 spectra of 462 SNe Ia [^398^]; SNfactory contributes 300+ SNe Ia with time-series spectrophotometry [^150^].

SNID-SAGE (698 templates, ~46,000 spectra classified) is the recommended modern tool [^753^][^754^]; DASH's CNN achieves 97.5% accuracy on preprocessed windows. The recommended pipeline: download via `wiserep_api`; classify with SNID-SAGE for type and redshift; resample to a common wavelength grid; normalize continuum and mask telluric regions; extract line equivalent widths as supplemental features. Self-supervised pre-training on the full spectral corpus remains a high-value unexplored opportunity. Validate with 20% instrument-stratified WISeREP holdout; cross-check redshifts against host galaxy values.

#### 13.2.6 For Future Survey Preparation: OpenUniverse2024 + Hourglass + lsst-alert-packet

Preparing for Rubin and Roman requires joint-survey training data. OpenUniverse2024 (400 TB over 70 deg² of overlapping Roman+Rubin coverage, ~1.4 million transients in Parquet) [^301^][^302^] is the definitive resource, accessible via AWS S3. The phrosty pipeline provides GPU-accelerated Roman difference imaging, producing light curves at rates orders of magnitude faster than CPU-based approaches [^764^][^775^].

For rapid prototyping, Roman Hourglass (64,000+ transients in three well-structured Parquet files with photometry and spectra) [^328^] is more immediately usable. Its 10 transient classes span SNe Ia at median z=1.32 to kilonovae at z~0.35. `GCRCatalogs` provides high-level DESC data access [^745^]. For alert-format preparation, ELAsTiCC2 Avro + `lsst-alert-packet` (`pip install lsst-alert-packet`) [^809^] enables end-to-end pipeline testing. Validate classifiers on Rubin DP1 real commissioning data [^767^] to measure sim-to-real gap before the full stream arrives. Publish benchmarks now — before Rubin dominates the literature — to establish community standards for the decade ahead.

### 13.3 Final Thoughts

The field of supernova machine learning stands at an inflection point without precedent in time-domain astronomy. The Vera C. Rubin Observatory, now in alert operations, will generate more supernova alerts in its first year of full operations — up to 10 million per night, translating to billions annually [^793^][^929^] — than all previous surveys combined across the entire history of the discipline. The Nancy Grace Roman Space Telescope, launching by May 2027, will add systematic near-infrared time-domain coverage that transforms high-redshift supernova cosmology. Euclid is already operational, with Data Release 1 anticipated in late 2026 to deliver an order-of-magnitude expansion over its current catalog [^766^].

The scale of incoming data is matched by the maturity of available tools. Where the PLAsTiCC challenge in 2018 represented a community just beginning to grapple with large-scale photometric classification, the 2026 ecosystem offers pip-installable deep learning frameworks, seven competing broker platforms with pre-trained models, 400 TB of joint survey simulations, and Python APIs that reduce classifier deployment from months to days. The remaining challenge is not building classifiers — it is ensuring that those classifiers perform reliably on real data, across wavelengths, and at scale.

The ten insights in this chapter converge on a single strategic message: preparation during the current 12-month readiness window will determine which research groups and methodologies define the ML standards for the next decade of supernova science. The community that invests now in domain-adapted classifiers validated on real spectroscopic samples, ensemble broker architectures that leverage disagreement as signal, and format-agnostic pipelines capable of ingesting Rubin Avro, Roman Parquet, and Euclid FITS alike will be positioned to extract maximum scientific value from the coming data torrent. The community that waits risks finding itself with powerful simulation-trained models that degrade unpredictably when confronted with the full complexity of the real night sky.

The datasets exist. The software exists. The window is open. The decisive factor now is action.

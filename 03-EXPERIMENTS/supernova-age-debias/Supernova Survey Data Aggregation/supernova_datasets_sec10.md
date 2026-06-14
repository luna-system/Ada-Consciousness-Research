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

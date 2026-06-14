# Dimension 09: Rubin/Roman/Euclid Future Survey Data Preparation

## Executive Summary

This document catalogs all available and upcoming datasets for supernova and transient science from three next-generation surveys: the Vera C. Rubin Observatory (operational, alert stream live), the Nancy Grace Roman Space Telescope (launch by May 2027), and ESA's Euclid mission (operational, Q1 released). Key datasets include the DESC DC2 300 deg² simulation (DP0, ~181 GB via RSP/Globus), Rubin DP1 commissioning data (3.5 TB, 2.3M objects via RSP), the Roman Hourglass simulation (10 transient types, Parquet on Zenodo), OpenUniverse2024 (~400 TB joint Roman+Rubin on AWS), and Euclid Q1 transient observations (164 transients, 161 with photometry). Multiple alert-format datasets (ELAsTiCC/ELAsTiCC2, lsst-alert-packet library) enable ML classifier preparation for Rubin's 7-10M alerts/night.

---

## 1. Rubin DP0: DESC DC2 Simulation

### 1.1 Overview
The DESC Data Challenge 2 (DC2) is a 300 deg² simulated optical/infrared sky survey in six LSST bands (ugrizy) covering 5 years of Wide-Fast-Deep (WFD) observations following a reference LSST cadence [^370^][^745^]. It serves as the foundation for Rubin Data Preview 0 (DP0), the first simulated data release used to prepare the community for LSST operations.

**Key Publication**: "The LSST DESC DC2 Simulated Sky Survey" (arXiv:2101.04855) [^370^]

### 1.2 Data Products

| Product | Description | Size | Format |
|---------|-------------|------|--------|
| Object Table | 114M extended + 33M point sources | ~118 GB | Parquet (166 tract files) |
| Truth-match Table | 759M galaxy, 5M star, 0.5M SN entries | ~63 GB | Parquet (166 tract files) |
| Unmerged Truth - SN Summary | Per-SN static info | Included | Parquet + SQLite |
| Unmerged Truth - SN Variability | Per-observation SN light curves | Included | Parquet + SQLite |
| Unmerged Truth - Star Summary | Per-star static info | Included | Parquet + SQLite |
| Unmerged Truth - Star Variability | Variable star light curves | Included | Parquet + SQLite |
| Unmerged Truth - Galaxy | Galaxy properties | Included | Parquet (healpix) |
| Intermediate Products | Calibrated exposures, source catalogs | Large | FITS |
| Coadded Images | Two tracts available | - | FITS |

The truth catalogs include SN Ia light curves and host galaxy assignments, making this the premier dataset for developing SN classification and cosmology pipelines before real data arrives [^370^][^746^].

### 1.3 Data Access Methods

**Method 1: Rubin Science Platform (RSP) — Recommended**
- Portal: https://data.lsst.cloud
- TAP service for catalog queries (ADQL)
- Notebook aspect with Jupyter + full LSST Science Pipelines
- Butler for image access
- Access catalogs: `object`, `truth_match`, `position`, `reference`, `forced_photometry` [^374^]

**Method 2: DESC Data Portal via Globus**
- URL: https://data.lsstdesc.org [^750^]
- Collection: "LSSTDESC Public"
- Path: `/lsstdesc-public/dc2/run2.2i-dr6-v4/` [^749^]
- Supports high-speed parallel transfer
- Total dataset: ~181 GB (Object + Truth Match tables)

**Method 3: GCRCatalogs Python Interface**
```python
import GCRCatalogs
obj = GCRCatalogs.load_catalog('desc_dc2_run2.2i_dr6_object')
truth = GCRCatalogs.load_catalog('desc_dc2_run2.2i_dr6_truth')
```
- High-level Python API for catalog access
- Install: `pip install GCRCatalogs`
- Citation: Mao et al. 2018, ApJS, 234, 36 [^745^]

### 1.4 ML Readiness
- **Format**: Apache Parquet — natively supported by pandas, pyarrow, polars, Spark
- **Truth labels**: Full SN classification, redshift, host association
- **Light curves**: Available via truth variability tables
- **Recommended for**: SN classification training, cosmology pipeline development, deblending studies, photo-z testing

---

## 2. Rubin DP1: ComCam Commissioning Data

### 2.1 Overview
Data Preview 1 (DP1) is the first Rubin data release from actual on-sky observations, obtained with the LSST Commissioning Camera (LSSTComCam) during a 48-night campaign from 2024-10-24 to 2024-12-11 [^765^][^767^].

**Release Date**: June 30, 2025 [^770^]
**Citation**: NSF-DOE Vera C. Rubin Observatory (2025); DOI: 10.71929/rubin/2570308 [^767^]

### 2.2 Dataset Scale
- **Size**: ~3.5 TB
- **Exposures**: 1,792 science-grade raw exposures
- **Nights**: 48 distinct nights
- **Area**: ~15 deg² across 7 non-contiguous fields
- **Objects**: ~2.3 million distinct astronomical objects
  - 1.6 million extended in at least one band
  - 431 solar system objects (93 new asteroid discoveries)
- **Coadded images**: 2,644

### 2.3 Fields
| Field | Epochs (nights) | Mean Visits/Night | Notes |
|-------|----------------|-------------------|-------|
| ECDFS | 21 | 40.7 | Best for time-domain |
| Low Galactic Latitude | 10 | 29.2 | Good for time-domain |
| EDFS (Euclid Deep Field S) | 9 | 30.2 | Overlaps Euclid |
| 47 Tuc | 4 | 16.5 | Globular cluster |
| Low Ecliptic Latitude | 5 | 31.8 | Solar system |
| Fornax dSph | 2 | 21.0 | Dwarf galaxy |
| Seagull Nebula | 4 | 25.0 | Star-forming |

### 2.4 Data Products
- Raw images
- Calibrated single-epoch processed visit images (PVIs)
- Coadded images (deepCoadd)
- **Difference images** (pre-generated) [^765^]
- DIA detection catalogs (DiaSource, DiaObject)
- DIA ForcedSource catalogs (light curves)
- Object catalogs with forced photometry
- SSP (Solar System Processing) catalogs
- Calibration products (bias, dark, flat, PTC, BF kernel, CTI)
- Standard bandpass transmission curves

### 2.5 Data Access
**Exclusive access via Rubin Science Platform (RSP)**:
- URL: https://data.lsst.cloud [^795^]
- Three aspects: Portal (GUI), Notebook (Jupyter), API (VO standards)
- TAP service for catalog queries [^788^]
- Butler for image and complex catalog access [^788^]
- SIA for image discovery
- **Data rights required**: US/Chile scientists + international in-kind team members
- After 2-year proprietary period (from ~June 2027), data becomes public but RSP access remains for data rights holders [^765^]

### 2.6 ML Readiness
- **Real data** with realistic noise, PSF, calibration artifacts
- DIA products enable transient detection algorithm training
- Difference images included (rare pre-generated product)
- ForcedSource tables provide light curves for variable/transient sources
- Overlap with Euclid Deep Field South enables multi-survey studies

---

## 3. Rubin Alert Format

### 3.1 Overview
Rubin alerts are serialized in Apache Avro format and distributed via Apache Kafka to community brokers within ~60 seconds of image acquisition [^793^][^298^]. Each alert corresponds to a single 5σ detection in a difference image.

### 3.2 Alert Packet Contents
Each alert packet (~82 KB) contains [^290^][^298^]:
- **diaSourceId**: Unique identifier for the triggering detection
- **Scheduler metadata**: Visit information
- **DiaSource record**: The triggering detection (photometry, astrometry, shape)
- **DiaObject or SSObject record**: Associated object
- **mpc_orbits**: If solar system object identified
- **12-month history**: Prior DiaSource and DiaForcedSource records
- **Postage stamp cutouts** (FITS format):
  - Science visit image
  - Difference image
  - Template coadd image

### 3.3 Alert Schema and Python Tools

**Primary Package: lsst-alert-packet**
- GitHub: https://github.com/lsst/alert_packet [^811^]
- PyPI: `lsst-alert-packet`
- Documentation: https://pipelines.lsst.io/modules/lsst.alert.packet/index.html [^809^]
- Uses `fastavro` library
- Provides: schema management, alert parsing, simulation, validation

**Installation**:
```bash
pip install lsst-alert-packet
```

**Key functions** [^809^]:
```python
import lsst.alert.packet as lap

# Get latest schema
schema = lap.Schema.from_file()

# Read alerts from Avro file
for alert in lap.retrieve_alerts(open('alerts.avro', 'rb')):
    print(alert['diaSource']['diaSourceId'])

# Simulate random alerts
lap.simulate_alert(schema)
```

**Schema versions**: Follow `MAJOR.MINOR` versioning with forward-transitive compatibility within major versions [^811^]. Latest schema always at `schema/latest.txt`.

### 3.4 Alert Stream Scale
- **Full LSST operations**: Up to 10 million alerts/night [^793^][^815^]
- **Current alert operations** (Feb 2026 start): Building up from lower rates
- **Bandwidth**: 0.2–5 Gbps [^210^]
- **Latency**: ~2 minutes from shutter close to broker delivery [^796^]
- **Serialization**: Apache Avro (compact binary)
- **Distribution**: Apache Kafka

### 3.5 Sample Alerts
- Sample alert data available: https://github.com/lsst-dm/sample_alert_info [^810^]
- Includes PPDB as SQLite database for exploration
- Sample files: single-CCD and single-visit subsets for testing

### 3.6 ML Readiness
- **Apache Avro** format has libraries in Python, C, Java, Scala, Go
- **Schema is well-documented** at sdm-schemas.lsst.io
- **Postage stamps included** — enables image-based classifiers
- **12-month history** — enables light-curve-based classifiers
- **lsst-alert-packet** provides full Python parsing/simulation toolkit
- All major broker frameworks (ALeRCE, Fink, AMPEL, ANTARES) already prototype on ZTF and process Rubin-format alerts

---

## 4. Roman Hourglass Simulation

### 4.1 Overview
The Hourglass simulation is a comprehensive synthetic dataset for the Roman High-Latitude Time-Domain Core Community Survey (HLTDS), simulating 10 extragalactic transient types with realistic Roman observational characteristics [^328^][^269^].

**Publication**: "The Hourglass Simulation: A Catalog for the Roman High-Latitude Time-Domain Core Community Survey" (ApJ, 2025) [^269^]

### 4.2 Transient Types (10 classes)

| Type | Total Detected | Median S/N | Median z |
|------|---------------|------------|----------|
| SN Ia | 21,700 | 13.5 | 1.32 |
| SNIa-91bg | 1,300 | 10.6 | 0.84 |
| SN Iax | 1,300 | 8.5 | 0.95 |
| CCSNe | 39,000 | 8.8 | 0.90 |
| SLSN-I | 70 | 32.4 | 1.82 |
| TDE | 39 | 13.5 | 0.65 |
| ILOT | 35 | 6.7 | 0.49 |
| Kilonova | 14 | 7.9 | 0.35 |
| PISN | 15 | 8.2 | 2.23 |
| AGN | 139 | 13.6 | 1.78 |

### 4.3 Survey Configuration Simulated
- **Wide tier**: 19 deg², 4 filters (R, Z, Y, J), 100s exposures, 5-day cadence
- **Deep tier**: 4.2 deg², 4 filters (Y, J, H, F), 300s exposures, 5-day cadence
- **Prism**: ~20% of area covered with spectroscopy (R≤100, 7500–18000 Å) [^329^]

### 4.4 Data Release
- **DOI**: 10.5281/zenodo.14262943 [^328^][^269^]
- **Format**: Three Parquet files
  - `hourglass_objects.parquet` — one row per object (RA, Dec, redshift, S/N, etc.)
  - `hourglass_photometry.parquet` — one row per flux measurement (flux, band, PSF, sky noise)
  - `hourglass_spectra.parquet` — one row per object per epoch (spectral time series)
- **Access**: Direct download from Zenodo via DOI
- **Python read**: `pandas.read_parquet()` or `pyarrow.parquet.read_table()`

### 4.5 Simulation Code
- SNANA simulation framework with PIPPIN pipeline manager
- Input files: https://github.com/Roman-Supernova-PIT/hourglass_snana_sims [^269^]

### 4.6 ML Readiness
- **Parquet format** — direct pandas/pyarrow ingestion
- **CID column** for joining objects → photometry → spectra
- **Light curves + spectra** for multi-modal classifiers
- **Truth labels** (exact transient type + redshift) for supervised learning
- **Used for**: ParSNIP training, SCONE photometric classifier development [^282^]
- **Well-suited for**: Photometric classifier development for Roman, cadence optimization studies

---

## 5. Roman Synthetic Images (IPAC)

### 5.1 Overview
Wang et al. (2023) created the first simulations of realistic Roman images with artificial Type Ia supernovae injected as point sources, covering a time series over 2 years of a nominal HLTDS deep field [^266^][^267^].

**Publication**: Wang et al., MNRAS, 523, 3874 (2023) [^266^]
**Access URL**: https://roman.ipac.caltech.edu/page/sn-survey-image-sim-html [^828^]

### 5.2 Dataset Characteristics
- **Size**: 1 deg² subarea of a planned 5 deg² deep survey
- **Duration**: 2-year time series
- **SNe Ia**: ~1,050 injected as point sources
- **Content**: Realistic Roman WFI images with injected SNe + input source catalogs
- **Secondary products**: Coadded images, difference image subtraction demonstrations

### 5.3 Public Products
- Simulated time-series images (FITS format)
- Input catalogs of all injected sources
- Coadded images
- Demonstrations of difference image subtraction
- Light curve data

### 5.4 ML Readiness
- **FITS format** — standard for astronomy (astropy, fitsio)
- **Image-level simulation** — enables CNN/Transformer training on cutouts
- **Point-source injection** — ground-truth positions and fluxes for detection algorithms
- **Used for**: Galaxy detection efficiency, point-source detection efficiency, host-galaxy association bias studies [^267^]

---

## 6. Euclid Q1: Quick Data Release

### 6.1 Overview
Euclid's Quick Data Release 1 (Q1) provides an early look at Euclid data, including single-epoch observations of the Euclid Deep Fields (EDFs). Q1 contains serendipitous observations of 164 previously known transients reported to the Transient Name Server (TNS) [^824^][^826^].

**Transient Paper**: Duffy et al. (2025), arXiv:2503.15334 [^824^]
**Main Q1 Paper**: Euclid Collaboration: Aussel et al., arXiv:2503.15302 [^766^]

### 6.2 Transient Data
- **Total transients identified**: 164 (cross-matched with TNS)
- **With photometric measurements**: 161
- **Photometric method**: PSF-fitting using `ecsnoopy` package
- **Detection rate**: ~70% of known transients reported within 6 months before Euclid observation, with discovery magnitude <24, detected in I_E images [^824^]

### 6.3 Filters and Measurements
Photometric measurements/upper limits in four Euclid bands:
- **I_E** (VIS-like, 550–900 nm)
- **Y_E** (NISP, 0.95–1.19 μm)
- **J_E** (NISP, 1.19–1.55 μm)
- **H_E** (NISP, 1.55–2.00 μm)

### 6.4 Notable Transients
- **SN 2024pvw**: One of the earliest NIR detections of a Type Ia SN, 15 days prior to peak brightness [^824^][^766^]
- **SN 2023aew**: Late-phase observation (435.9 days post peak) of enigmatic core-collapse SN [^824^]
- Host galaxies of several "hostless" transients detected

### 6.5 Data Access
- Euclid Q1 data released via ESA Euclid archive
- DESC TOM also provides some Euclid transient data integration
- Data products in standard Euclid processing pipeline format

### 6.6 Future Data Releases
- **DR1**: Expected late 2026, ~30× Q1 area (~1900 deg²), ~1.5 orders of magnitude more objects [^766^]
- **DR2**: First 3 years of data
- **DR3**: Full mission (~6 years)

### 6.7 ML Readiness
- Single-epoch data limits time-domain analysis in Q1
- **Foundational for**: Training data for transient detection in Euclid images, PSF-fitting validation, NIR transient characterization
- **DR1** (late 2026) will enable proper multi-epoch transient detection via difference imaging

---

## 7. OpenUniverse2024: Joint Roman+Rubin Simulation

### 7.1 Overview
OpenUniverse2024 is a massive cross-collaboration effort producing ~400 TB of matched simulated imaging for Roman and Rubin surveys over a common ~70 deg² sky region [^335^][^302^]. It uses the updated Diffsky extragalactic model and improved transient models.

**Publication**: OpenUniverse et al. (2025), MNRAS, 544, 3799 [^335^]
**Data Access**: https://irsa.ipac.caltech.edu/data/theory/openuniverse2024/ [^302^]

### 7.2 Survey Components
1. LSST ELAIS-S1 Deep Drilling Field (DDF)
2. Roman Time-Domain Survey (TDS) shifted to overlap ELAIS region
3. Overlapping LSST Wide-Fast-Deep (WFD) with rolling cadence
4. Overlapping Roman Wide-Area Survey (WAS)
5. Roman deep-field calibration region

### 7.3 Data Products

| Product | Format | Size | Access |
|---------|--------|------|--------|
| Roman simulated images | FITS | ~400 TB total | AWS S3 |
| Rubin simulated images | FITS | Included | AWS S3 |
| Roman simulated tables | Parquet | Included | AWS S3 |
| Rubin simulated tables | Parquet | Included | AWS S3 |

Two releases:
- **Data Preview**: Smaller preview, DOI 10.26131/IRSA569 (on-premise at IPAC + AWS)
- **Full Release**: Complete 400 TB, DOI 10.26131/IRSA596 (AWS cloud only) [^302^]

### 7.4 AWS Access
- Listed on AWS Open Data Registry: https://registry.opendata.aws/openuniverse2024/ [^305^]
- Direct S3 access for cloud-based analysis
- Browseable directories for exploration
- Download scripts provided
- Tutorials available from IPAC-IRSA [^305^]

### 7.5 ML Readiness
- **400 TB** of pixel-level simulation — the largest joint survey simulation available
- **FITS images** for CNN/Transformer training
- **Parquet tables** for catalog-based ML
- **Multi-survey overlap** — enables cross-survey classifier development
- **Transient models** included in simulation
- **Used by**: phrosty pipeline, Roman SN PIT, DESC analysis

---

## 8. DESC Data Portals and Globus Access

### 8.1 DESC Data Portal
- **URL**: https://data.lsstdesc.org [^750^]
- **Primary access**: Globus-based high-speed transfer
- **Collection**: "LSSTDESC Public" (in Globus File Manager) [^749^]
- **Path**: `/lsstdesc-public/dc2/run2.2i-dr6-v4/` [^749^]

### 8.2 Globus Access Instructions
1. Create Globus account (organizational login, GitHub, Google, ORCID)
2. Install Globus Connect Personal for bulk download
3. In Globus File Manager, search for "LSSTDESC Public"
4. Navigate to desired data path
5. Select files/folders and initiate transfer [^748^][^749^]

### 8.3 NERSC Access (DESC Members)
- Data also available on NERSC at `/global/cfs/cdirs/lsst/` paths
- DESC TOM database access via NERSC credentials
- ELAsTiCC/ELAsTiCC2 data at `/global/cfs/cdirs/desc-td/` [^334^]

### 8.4 GCRCatalogs
- High-level Python interface to DESC datasets
- Install: `pip install GCRCatalogs`
- Supports lazy loading, column selection, tract filtering
- Tutorial notebooks available at https://github.com/LSSTDESC/gcr-catalogs

---

## 9. phrosty: Roman Difference Imaging Pipeline

### 9.1 Overview
phrosty (PHotometry for ROman with SFFT for tYpe Ia supernovae) is a Python difference imaging and forced photometry pipeline designed specifically for Roman HLTDS data [^764^][^775^].

**Publication**: Aldoroty et al. (2025), arXiv:2509.18544 [^764^]
**GitHub**: https://github.com/Roman-Supernova-PIT/phrosty [^775^]
**Documentation**: https://roman-supernova-pit.github.io/phrosty/

### 9.2 Technical Features
- **Algorithm**: GPU-accelerated Saccadic Fast Fourier Transform (SFFT) for image subtraction
- **PSF**: Uses galsim + roman_imsim for spatially-varying PSF
- **Architecture**: Mixed GPU/CPU computation for speed
- **Input**: Currently handles OpenUniverse simulation FITS images
- **Output**: Difference images + forced photometry light curves as CSV

### 9.3 Performance
- Addresses the challenge of ~241 Level-2 images/day from Roman (~0.4 TB/day)
- Compared to DES HOTPANTS pipeline (10 min/single detector image → 80 hours/day), phrosty achieves orders of magnitude speedup via GPU SFFT [^775^]
- Among the fastest astronomical DIA pipelines available

### 9.4 Environment Requirements
Three environment variables:
- `SIMS_DIR`: OpenUniverse Roman data path
- `SN_INFO_DIR`: Directory with `tds.yaml` config
- `DIA_OUT_DIR`: Output directory for difference images

### 9.5 NERSC Deployment
- Designed to run on NERSC/Perlmutter with Docker/Podman containers
- Example scripts for interactive and Slurm batch modes [^775^]

### 9.6 ML Relevance
- Enables generation of **training data** from Roman simulations
- Produces light curves from difference imaging for SN Ia cosmology
- Open-source Python code extensible to other transient types

---

## 10. Preparing Classifiers for Rubin Alert Volume

### 10.1 The Scale Challenge
- **Volume**: Up to 10 million alerts/night at full LSST operations [^793^][^815^]
- **Rate**: 0.2–5 Gbps continuous stream [^210^]
- **Latency**: ~60 seconds from shutter close to broker delivery [^298^]
- **Current**: Rubin alert operations started February 2026, building from lower rates
- **Format**: Apache Avro packets, each ~82 KB with cutouts [^210^]

### 10.2 Training Datasets for ML Classifiers

#### 10.2.1 ELAsTiCC (Extended LSST Astronomical Time-Series Classification Challenge)
- **Purpose**: Real-time test of broker infrastructure and ML classifiers [^812^][^334^]
- **ELAsTiCC v1**: Streamed Sep 2022–Jan 2023
  - ~4.3M objects, ~139M observations
  - 30 models, 19 classes
  - Alert format matching Rubin
- **ELAsTiCC2**: Nov–Dec 2023
  - ~4M objects, ~50M detections, ~400M forced photometry points
  - Updated cadence (baseline v3.2), rolling cadence, DDF fields
  - SNANA FITS format (HEAD + PHOT files)
  - Available at NERSC: `/global/cfs/cdirs/desc-td/ELASTICC2` [^334^]
- **Training sets**: Downloadable from NERSC portal [^334^]
  - ELASTICC2_TRAIN_02.tar.bz2 (7.4 GiB)
- **Access**: DESC TOM at https://desc-tom.lbl.gov [^829^]

#### 10.2.2 PLAsTiCC (Photometric LSST Astronomical Time-Series Classification Challenge)
- Predecessor to ELAsTiCC
- Static light curve dataset (non-streaming)
- Kaggle competition with 1000+ participating teams
- Available via Kaggle archives

#### 10.2.3 DC2 Truth Catalogs
- ~500,000 simulated SNe with full light curves and truth labels [^370^]
- Available via RSP or Globus download

#### 10.2.4 Roman Hourglass
- 10 transient types with Roman-specific characteristics
- Zenodo: 10.5281/zenodo.14262943

### 10.3 Alert Broker Ecosystem
Seven full-stream brokers receive the complete Rubin alert stream [^44^][^332^]:

| Broker | ML Approach | Strengths | Access |
|--------|------------|-----------|--------|
| **ALeRCE** | Rich ML classifiers (VAE, XGBoost, CNN) | Most developed ML taxonomy, web portal, Python client | science.alerce.online |
| **AMPEL** | Modular, user-provided classifiers | Most flexible architecture, workflow extensibility | ampel.zeuthen.desy.de |
| **ANTARES** | Gradient boosting + ParSNIP | Rich web portal, watchlists, Python filters | antares.noirlab.edu |
| **Babamul** | Lightweight, deployable | Channels by event type, minimal hardware | babamul.caltech.edu |
| **Fink** | Spark-based, 60+ science topics | Proven stream processor, high scalability | fink-broker.org |
| **Lasair** | SQL + light curve features | Rich web portal, Zooniverse integration | lasair-lsst.lsst.ac.uk |
| **Pitt-Google** | Google Cloud-based | Cloud-native, subscription model | pittgoogle.lsst.cloud |

Two downstream brokers: SNAPS, POI Broker [^332^]

### 10.4 Fink Benchmarks (on ELAsTiCC)
- Fink tested on 17.2M training alerts + 34.9M test alerts [^812^]
- Current rate: 300K alerts/night (ZTF), tested up to 50M/night
- Science database: 7 TB, 200M events
- Uses Spark computing, HBase database, Kafka streaming, Ceph/HDFS storage [^815^]

### 10.5 Rubin Alerts & AI Hackathon 2026
- **Dates**: April 1–3, 2026
- **Location**: SkAI Institute, Chicago
- **Focus**: AI tools for real-time Rubin alert processing
- **Tracks**: Alert classification, filtering/prioritization, multi-modal fusion, anomaly detection, scalable pipelines, community tools [^794^]
- Signals strong community emphasis on ML readiness

### 10.6 ML Preparation Recommendations
1. **Start with ELAsTiCC2** data (SNANA FITS) for classifier training
2. **Use lsst-alert-packet** to understand Avro format and simulate alerts
3. **Test on ZTF streams** via broker partners (300K/night current rate)
4. **Use DC2 truth catalogs** for large-scale labeled training data
5. **Process OpenUniverse2024** for joint Roman+Rubin classifier development
6. **Consider latency requirements**: Classifiers must run in <seconds per alert
7. **Key features to engineer**: Light curve history, cutout images, host galaxy context, cross-survey multi-wavelength data

---

## 11. Summary of All Datasets

| Dataset | Survey | Size | Format | Access | SN/Transient Content | ML Ready |
|---------|--------|------|--------|--------|---------------------|----------|
| DESC DC2 | Rubin (sim) | ~181 GB+ | Parquet, FITS | RSP, Globus, GCRCatalogs | 500K SNe Ia + hosts | ★★★★★ |
| Rubin DP1 | Rubin (real) | 3.5 TB | Various (RSP) | RSP only | DIA sources, real transients | ★★★★☆ |
| lsst-alert-packet | Rubin | N/A | Avro (lib) | pip install | Alert simulation | ★★★★★ |
| Roman Hourglass | Roman (sim) | ~GBs | Parquet | Zenodo DOI | 10 types, 64K+ transients | ★★★★★ |
| Roman IPAC Images | Roman (sim) | TB-scale | FITS | IPAC website | ~1,050 SNe Ia in images | ★★★★☆ |
| Euclid Q1 | Euclid (real) | Survey-scale | Euclid pipeline | ESA archive | 161 transients photometry | ★★☆☆☆ |
| OpenUniverse2024 | Roman+Rubin (sim) | ~400 TB | FITS, Parquet | AWS S3 | Multiple transient types | ★★★★★ |
| ELAsTiCC/ELAsTiCC2 | Rubin (sim alerts) | ~50 GB | Avro, FITS | NERSC, DESC TOM | 19-30 types, 4M+ objects | ★★★★★ |
| phrosty | Roman (pipeline) | N/A | Python | GitHub | DIA + forced photometry | ★★★★☆ |

---

## 12. Areas Warranting Deeper Investigation

1. **Rubin alert archive**: Archive interface not yet available; when live, will provide historical alert data via RSP for training set construction [^825^]
2. **Euclid DR1** (late 2026): Will provide multi-epoch data enabling proper transient detection via difference imaging — much more valuable for ML than Q1
3. **phrosty scalability**: GPU-accelerated DIA for Roman — performance benchmarks on full OpenUniverse2024 would be valuable
4. **Roman alert system**: Roman will have its own alert stream; RAPID PIT developing alert distribution — schema and tools still under development
5. **Cross-survey classifiers**: Joint training on OpenUniverse2024 (Roman+Rubin overlap) for maximal classification performance
6. **Real-bogus classification**: Rubin's DIA false positive rate and training data for real/bogus classifiers at LSST scale
7. **PLAsTiCC legacy data**: Still valuable as a large labeled static light curve dataset

---

## References

[^266^]: Wang et al. 2023, "A Synthetic Roman Space Telescope High-Latitude Time-Domain Survey: Supernovae in the Deep Field", MNRAS, 523, 3874, arXiv:2204.13553
[^267^]: Wang et al. 2023, MNRAS, 523, 3874, https://scholars.duke.edu/publication/1583891
[^269^]: Rose et al. 2025, "The Hourglass Simulation: A Catalog for the Roman High-Latitude Time-Domain Core Community Survey", ApJ, arXiv:2506.05161
[^282^]: "Picture Perfect: Photometric Transient Classification Using ParSNIP with Roman Hourglass Simulations", arXiv:2412.03604
[^290^]: Rubin Prompt Products: Alert packets, https://prompt-products.lsst.io/products/alerts/index.html
[^298^]: "Design of the LSST Alert Distribution System" (DMTN-093), https://dmtn-093.lsst.io/
[^302^]: OpenUniverse 2024, IRSA/IPAC, https://irsa.ipac.caltech.edu/data/theory/openuniverse2024/overview.html
[^305^]: OpenUniverse 2024 on AWS Open Data Registry, https://registry.opendata.aws/openuniverse2024/
[^328^]: "A Catalog for the Roman High-Latitude Time-Domain Core Community Survey", arXiv:2506.05161
[^329^]: UC Santa Cruz/Rose et al., Hourglass paper eprint
[^332^]: NOIRLab press release on Rubin alert brokers, https://noirlab.edu/public/news/noirlab2605/
[^334^]: DESC ELAsTiCC Challenge, https://portal.nersc.gov/cfs/lsst/DESC_TD_PUBLIC/ELASTICC/
[^335^]: OpenUniverse2024 paper, MNRAS, 544, 3799, arXiv:2501.05632
[^370^]: DESC DC2 Data Release Note, arXiv:2101.04855
[^374^]: DP0.2 Data Products, https://dp0-2.lsst.io/v/roll-back/data-products-dp0-2/index.html
[^745^]: DC2 Simulated Sky Survey, https://data.lsstdesc.org/doc/dc2_sim_sky_survey
[^746^]: "Data Preview 0: The Simulated Data Set from the DESC's DC2", LSST Community, 2021
[^748^]: Globus download tutorial
[^749^]: DESC Data Portal GitHub discussion on Globus access
[^750^]: LSST DESC Data Portal, https://data.lsstdesc.org
[^764^]: "phrosty: A difference imaging pipeline for Roman", arXiv:2509.18544
[^765^]: "The Vera C. Rubin Observatory Data Preview 1", arXiv:2603.23786
[^766^]: "Euclid Quick Data Release (Q1)", arXiv:2503.15302
[^767^]: DP1 Documentation, https://dp1.lsst.io
[^770^]: "Rubin DP1 will be released on June 30, 2025", LSST Community
[^775^]: phrosty GitHub, https://github.com/Roman-Supernova-PIT/phrosty
[^788^]: DP1 Data Access, https://dp1.lsst.io/access/index.html
[^792^]: Rubin Data Access, https://rubinobservatory.org/for-scientists/data-products/data-access
[^793^]: "Machine learning for time-domain astronomy at scale" (Fink/Rubin presentation)
[^794^]: Rubin Alerts & AI Hackathon 2026, https://rubinalerts26.github.io/
[^796^]: Rubin Observatory First Alerts press release, 2026-02-25
[^809^]: lsst.alert.packet documentation, https://pipelines.lsst.io/modules/lsst.alert.packet/index.html
[^810^]: Sample alert info, https://github.com/lsst-dm/sample_alert_info
[^811^]: lsst/alert_packet GitHub, https://github.com/lsst/alert_packet
[^812^]: "Transient classifiers for Fink - Benchmarks for LSST", A&A, 2024
[^815^]: "Vera Rubin Observatory Plans for the low latency alert system" (Fink/J. Peloton)
[^824^]: Duffy et al. 2025, "Euclid Q1 -- Photometric studies of known transients", arXiv:2503.15334
[^825^]: Prompt Products Data Access, https://prompt-products.lsst.io/access/index.html
[^828^]: Roman SN Survey Image Simulations, https://roman.ipac.caltech.edu/page/sn-survey-image-sim-html
[^829^]: DESC TOM GitHub, https://github.com/LSSTDESC/tom_desc

# Facet: Upcoming/Future Surveys & Emerging Data Streams

## Summary

This report catalogs upcoming and future supernova surveys, emerging data streams, and simulated data available now for ML preparation. The landscape is dominated by the imminent Vera C. Rubin Observatory (LSST) which began alert operations in February 2026 and will discover millions of new supernovae annually. Other major upcoming missions include the Nancy Grace Roman Space Telescope (launch no later than May 2027), ESA's Euclid (already operational), SKA pathfinders (ASKAP/VAST producing data now), CTA/CTAO (under construction), DUNE (under construction), and next-generation alert brokers processing the LSST alert stream. Critically, large volumes of simulated pre-operation data are available NOW for algorithm development.

---

## Key Findings

1. **Rubin Observatory is NOW in early operations** with real-time alerts having begun February 2026 [^44^]. Data Preview 1 (DP1) was released June 2025, DP2 is expected mid-2026 [^291^]. The LSST will discover an estimated 1-10 million supernovae over 10 years.

2. **Seven full-stream alert brokers** (ALeRCE, AMPEL, ANTARES, Babamul, Fink, Lasair, Pitt-Google) are operational and receiving/processing LSST alerts [^44^][^210^]. The alert format is Apache Avro with ~82KB packets and a stream rate of 0.2-5 Gbps [^210^].

3. **Roman Space Telescope** (launch by May 2027) will conduct a High-Latitude Time-Domain Survey covering 19 deg2 wide + 4.2 deg2 deep tier, detecting ~21,000 SNe Ia and ~40,000 core-collapse SNe [^269^]. The Hourglass simulation and OpenUniverse2024 (~400 TB of joint Roman+Rubin synthetic imaging) are available NOW [^335^][^336^].

4. **Large-scale simulated datasets available NOW** for ML training: DESC DC2 (300 deg2, 5 years), PLAsTiCC (3.5M+ events), ELAsTiCC (~5M events, ~50M alerts), OpenUniverse2024 (~400 TB), Hourglass (64,000+ transients, 11M photometric observations), SNANA-generated light curves [^97^][^335^][^269^].

5. **Neutrino supernova alerts** are operational NOW via IceCube (part of SNEWS 2.0 since 2016), providing real-time early warning of galactic core-collapse supernovae hours before optical emission [^292^][^295^].

6. **Radio supernova surveys** are producing data NOW: ASKAP VAST (0.5M sources, 6.4M measurements in DR1), LOFAR LoTSS-DR3 (13.6M radio sources), with SKA construction ongoing [^369^][^384^].

---

## Upcoming Survey Catalog

### 1. Vera C. Rubin Observatory (LSST)

| Attribute | Details |
|-----------|---------|
| **Status** | Early operations; alerts began Feb 2026; survey start ~2026 [^289^][^291^] |
| **Location** | Cerro Pachon, Chile (2,682m) |
| **Aperture** | 8.4m effective |
| **FOV** | 9.6 deg2 (LSSTCam) |
| **Filters** | ugrizy (320-1050 nm) |
| **Expected SNe** | 1-10 million SNe over 10 years (10^6+ SNe Ia) |
| **Cadence** | Every 3-4 nights per field (Wide-Fast-Deep) |

#### Data Products & Access
- **DP0**: Simulated data based on DESC DC2, available NOW via Rubin Science Platform (RSP). 300 deg2, 5 years of simulated WFD observations including Type Ia supernovae [^374^]. DP0.2 processed with LSST Science Pipelines v23 includes DIA (Difference Image Analysis) data products [^273^].
- **DP1**: Released June 30, 2025. Real ComCam data: ~15 sq.deg over 7 fields, ~2.3M distinct objects, 3.5 TB. Includes DIA source catalogs for transient detection [^270^].
- **DP2**: Expected mid-2026. LSSTCam commissioning data with full suite of data products [^291^][^289^].
- **DR1**: First year LSST data, expected late 2026-early 2027 [^291^].
- **Access**: Rubin Science Platform (RSP) on Google Cloud Platform; data rights required for DP1/DP2 [^278^].
- **Alerts**: Apache Avro format, world-public, no proprietary period. Each packet contains diaSource, diaObject, 12-month history, FITS cutouts [^290^].
- **Alert Rate**: ~10 million alerts/night expected during operations [^372^].

#### Key Publications
- "The Vera C. Rubin Observatory Data Preview 1" [^270^]
- "Recovered supernova Ia rate from simulated LSST images" (A&A, 2024) [^273^]
- "Commissioning of the Vera C. Rubin Observatory" [^289^]
- RTN-095, RTN-010 (Rubin technical notes)

#### ML-Readiness
- **Simulated data available NOW**: DP0 (DC2-based) with supernova truth catalogs, DIA products. DESC data portal with Globus access [^370^].
- **Alert format**: Apache Avro with well-defined schema (sdm-schemas.lsst.io) [^290^][^298^].
- **Broker ecosystem**: Seven brokers providing classified, filtered alert streams with ML classification [^44^].
- **Python access**: lsst-alert-packet repository, RSP with Jupyter notebooks [^298^].

---

### 2. Nancy Grace Roman Space Telescope

| Attribute | Details |
|-----------|---------|
| **Launch** | No later than May 2027 (NASA commitment) [^269^] |
| **Orbit** | Earth-Sun L2 |
| **Primary Instrument** | Wide Field Instrument (WFI): 0.48-2.3 um, 0.281 deg2 FOV |
| **Mirror** | 2.4m primary |
| **Core Community Surveys** | High-Latitude Wide-Area, High-Latitude Time-Domain, Galactic Bulge Time-Domain [^271^] |

#### Data Products
- **Data Levels**: Level 0 (raw) through Level 5 (user-contributed) [^272^]
- **Level 1**: `_uncal.asdf` uncalibrated detector data
- **Level 2**: `_cal.asdf` calibrated rate images
- **Level 3**: `_coadd.asdf` coadded mosaics
- **Level 4**: `_cat.parquet` source catalogs, `_segm.asdf` segmentation maps
- **Format**: ASDF (Advanced Scientific Data Format), Parquet for catalogs [^272^]

#### Expected Supernova Yields
- **HLTDS Wide Tier**: 19 deg2, ~21,000 SNe Ia, ~40,000 core-collapse SNe, ~70 SLSNe, ~35 TDEs, 3 kilonovae [^269^]
- **HLTDS Deep Tier**: 4.2 deg2, 5-day cadence over 2 years
- **Total Hourglass catalog**: 64,000+ transients, 11,000,000 photometric observations, 500,000 spectra [^269^]

#### Simulated Data Available NOW
- **Hourglass Simulation**: Full simulation of Roman HLTDS with 10 transient types, designed for ML classification training. Zenodo DOI: 10.5281/zenodo.14262943. GitHub: github.com/Roman-Supernova-PIT/hourglass_snana_sims [^269^]
- **Synthetic Roman Images**: Simulated 2-year time series with ~1,050 SNe Ia in 1 deg2, publicly available at roman.ipac.caltech.edu/sims/SN_Survey_Image_sim.html [^266^][^268^]
- **OpenUniverse2024**: ~400 TB of joint Roman+Rubin synthetic imaging covering 70 deg2, publicly available. Includes updated Diffsky extragalactic models and transient models [^335^][^336^]
- **phrosty**: Roman difference-imaging pipeline, open-source, GPU-optimized, ~2 seconds per image [^263^]

#### Key Publications
- Wang et al. 2022: "A Synthetic Roman Space Telescope High-Latitude Time-Domain Survey" [^266^]
- Rose et al. 2025: "The Hourglass Simulation" [^269^][^263^]
- Troxel et al. 2022/2025: OpenUniverse joint Roman-Rubin simulations [^338^][^335^]

---

### 3. ESA Euclid

| Attribute | Details |
|-----------|---------|
| **Status** | Operational (launched July 2023, science operations ongoing) |
| **Orbit** | Sun-Earth L2 |
| **Instruments** | VIS (optical), NISP (near-IR imaging + slitless spectroscopy) |
| **Deep Fields** | 3 fields (~10-20 deg2 each) with repeat observations |

#### Supernova Data Products
- **Euclid Deep Fields**: Repeated observations over 2-week span, 6-month gap, enabling transient detection [^276^]
- **Coordinated Release Q1**: 164 known transients with Euclid photometry (VIS + NISP Y/J/H filters) [^274^]
- **Expected SNe**: >3,700 SNe (0.0 < z < 1.5) with >=5 detections at S/N > 3 around peak [^276^]
- **Synergy with LSST**: Combining Euclid NIR + LSST optical reduces distance uncertainties by 20-30% (z < 0.8) and 40-50% (z > 0.8) [^276^]
- **Access**: Euclid data archives (Q1 Quick Data Release publicly available), via ESA science data center [^274^]

#### Key Publications
- Duffy et al.: "Quick Data Release (Q1) - Photometric studies of known transients" [^274^]
- Hounsell et al.: "Type Ia Supernova cosmology combining Euclid and LSST" [^276^]
- Goobar et al.: Euclid SN Ia rate estimates [^277^]

---

### 4. SKA (Square Kilometre Array) and Pathfinders

#### ASKAP VAST (Variables and Slow Transients)
| Attribute | Details |
|-----------|---------|
| **Status** | Operational; Data Release 1 available (Feb 2026) [^369^] |
| **Telescope** | Australian SKA Pathfinder (ASKAP) |
| **Frequency** | 888 MHz |
| **Coverage** | ~12,300 deg2 (southern sky) |
| **Cadence** | Every ~2 months per field |
| **Sensitivity** | 0.24 mJy/beam rms |

- **Data Release 1**: 2,945 images of 276 fields, 0.5 million sources, 6.4 million individual light curve measurements. Publicly available through CSIRO Data Access Portal [^369^]
- **Supernovae detected**: 2 optically identified supernovae (SN 2024abfo, SN 2023mut), 1 supernova candidate [^369^]
- **Other transients**: 117 astrophysical variables including 27 pulsars, 40 radio stars, 44 AGN [^369^]

#### LOFAR
| Attribute | Details |
|-----------|---------|
| **Status** | Operational; LoTSS-DR3 released (March 2026) [^384^] |
| **Frequency** | 120-168 MHz |
| **Coverage** | 88% of northern sky |
| **DR3 Sources** | 13,667,877 radio sources [^384^] |

- **LoTSS-DR3**: 18.6 PB of processed data, 13,575 hours of observations. Includes calibrated uv data, images, catalogs [^384^]
- **Supernova studies**: Subarcsecond imaging of SNe, radio remnants, low-frequency absorption studies [^388^]
- **Access**: LOFAR Long Term Archive (LTA) at SURF Amsterdam, FZ Juelich, PCSS Poznan [^386^]
- **Future**: LOFAR2.0 upgrade will double survey speed [^385^]

#### Full SKA
| Attribute | Details |
|-----------|---------|
| **Status** | Construction ongoing (Phase 1) |
| **Expected Sensitivity** | Orders of magnitude beyond current instruments |
| **Supernova Science** | Radio emission from SN remnants, CSM interaction, synchrotron transients |

---

### 5. CTA/CTAO (Cherenkov Telescope Array Observatory)

| Attribute | Details |
|-----------|---------|
| **Status** | Under construction; Alpha Configuration approved |
| **Sites** | Paranal, Chile (southern) + La Palma, Spain (northern) [^320^][^325^] |
| **Energy Range** | 20 GeV - 300 TeV |
| **Telescopes** | 64 total (51 south, 13 north) in Alpha config |
| **Slew Time** | As low as 20 seconds |

- **Transient Science**: Gamma-ray bursts, multi-messenger transients, supernova remnants, follow-up of GW/neutrino alerts [^320^][^326^]
- **Supernova remnants**: Expected to detect hundreds of high-energy sources vs. tens known today [^315^]
- **Data Products**: Reconstructed gamma-ray photon lists, sky images, source catalogs. Open observatory with public archive after proprietary period (~1 year) [^320^]
- **Data Pipeline**: Developed by DAp team; includes real-time transient detection [^315^]

#### Key Publications
- Hofmann et al. 2023: "The Cherenkov Telescope Array" [^327^]
- CTA Consortium Science Case [^320^]

---

## Emerging Data Streams

### 6. Gravitational Wave Supernova Counterparts (LIGO/Virgo/KAGRA)

| Attribute | Details |
|-----------|---------|
| **Detectors** | LIGO (2x USA), Virgo (Italy), KAGRA (Japan) |
| **Status** | O4 observing run completed; O5 planned |
| **Alert Network** | GCN/TAN (Gamma-ray Burst Coordinates Network) |

- **Multi-messenger capability**: GW alerts trigger electromagnetic follow-up across all wavelengths [^293^]
- **GW170817**: First BNS merger with EM counterpart (kilonova AT2017gfo), demonstrating the multi-messenger approach [^293^]
- **IceCube+LVK Coincidence Searches**: Realtime neutrino searches within +/-500s of GW alerts, published as GCN Notices [^300^]
- **Alert Latency**: Initial alerts within minutes of detection
- **Localization**: Typical 90% credible region of ~10-100 deg2 (improving with more detectors)
- **Relevance for SNe**: Core-collapse supernovae within Milky Way would produce neutrino bursts detectable by SNEWS 2.0; asymmetric core collapse produces GWs

---

### 7. Neutrino Supernova Alerts (IceCube, DUNE, SNEWS 2.0)

#### IceCube
| Attribute | Details |
|-----------|---------|
| **Location** | South Pole, Antarctica |
| **Status** | Operational since 2010, >99% uptime |
| **Supernova Sensitivity** | >10 sigma for galactic CCSN |

- **Real-time supernova alerts**: Part of SNEWS 2.0 network since 2016, ~1 alert/month to SNEWS [^297^]
- **SNDAQ (Supernova Data Acquisition)**: Scans detector hit stream in real-time for collective rate excess. Issues alerts within seconds [^297^]
- **HitSpool**: Buffers 90s window of DOM waveforms around trigger times, ~13 days of data buffered [^297^]
- **IceCube+LVK Follow-up**: Searches for coincident neutrinos with GW events, results via GCN [^300^]
- **Fire Drill system**: Simulated supernova signal injection for readiness testing [^292^]

#### DUNE (Deep Underground Neutrino Experiment)
| Attribute | Details |
|-----------|---------|
| **Location** | Sanford Underground Research Facility, South Dakota |
| **Detector** | 4 x 10-kton liquid argon TPC modules (40 kton total fiducial) |
| **Depth** | 1.48 km underground |
| **Status** | Under construction; first module expected ~2028-2029 |
| **Data Rate** | ~1.2 TB/s per module [^316^] |
| **Storage** | 30 PB/year limit [^316^] |

- **Supernova physics goals**: Detect and measure nu_e flux from galactic CCSN with unique sensitivity [^318^][^323^]
- **Energy range**: Sensitive from ~5 MeV upward [^323^]
- **Triggering**: Redundant TPC and photon detection system triggers; 30-100s data recording around triggers [^323^]
- **ML for triggering**: YOLOv3-based object detection for low-energy neutrino interactions; 76.2% efficiency at 1.8 Hz false positive rate [^316^]
- **Simulated data**: MARLEY generator, extensive simulation campaigns available [^318^]

#### SNEWS 2.0 (SuperNova Early Warning System)
| Attribute | Details |
|-----------|---------|
| **Status** | Operational (upgraded from SNEWS 1.0) [^358^] |
| **Network** | IceCube, Super-K, LVD, Borexino, KamLAND, HALO, KM3NeT, Daya Bay, plus others in testing [^356^] |
| **Alert Latency** | << 1 hour target |
| **False Alarm Rate** | < 1/century target |

- **Multi-detector coincidence**: Requires triggers from >=2 detectors within 10 seconds [^358^]
- **Alert distribution**: SNEWS website (snews2.org), email lists, VOEvent network/GCN [^360^]
- **Early warning**: Neutrinos arrive hours before optical emission; provides time to prepare observations [^352^]
- **Software**: Built on HOPSKOTCH publish-subscribe framework. SNEWPY Python package for simulation-to-detector pipeline [^352^][^373^]

#### SNEWPY Software
- Open-source Python package bridging supernova simulations to neutrino detector signals [^373^]
- Interfaces with hundreds of core-collapse, thermonuclear, and pair-instability simulations
- Includes flavor transformation models
- Integrates with SNOwGLoBES for event rate calculations
- Documentation: snewpy.readthedocs.io

---

### 8. Citizen Science & Amateur Astronomer Data

#### Zooniverse Supernova Hunters
- **Project**: Citizens classify Pan-STARRS1 difference images as real supernovae or bogus detections [^321^][^317^]
- **Goal**: Improve detection algorithms by providing human-labeled training data
- **Data**: Difference imaging from Pan-STARRS1 telescope (Maui, Hawaii)
- **Access**: zooniverse.org/projects/dwright04/supernova-hunters
- **Status**: Active, ongoing classifications

#### SNAD (SuperNova Anomaly Detection)
- Citizen science project for anomaly detection in astronomical data
- Uses Open Supernova Catalog and ZTF survey data
- Identified 81 potentially interesting anomalous objects, including 27 confirmed non-SN or rare SN events [^158^]

#### AAVSO (American Association of Variable Star Observers)
- Maintains archives of variable star and supernova observations
- Historical archives at 49 Bay State Road, Cambridge, MA [^296^]
- Supernova data and finder charts available
- Accepts observations from amateur astronomers with assigned observer codes

#### Amateur Supernova Discoveries
- Amateur astronomers regularly discover supernovae using remote telescopes (iTelescope.net, etc.)
- Key example: V. Buso discovered SN 2016gkg (Type IIb) and captured the shock breakout - first-ever detection of initial burst of light from a supernova [^333^][^337^]
- Transient Name Server (TNS) accepts reports from all observers

---

### 9. Transient Name Server (TNS)

| Attribute | Details |
|-----------|---------|
| **URL** | wis-tis.org |
| **Purpose** | Official IAU repository for reporting and classifying astronomical transients |
| **Content** | Discovery reports, classification reports, coordinates, redshifts, photometry |
| **API** | REST API for search, submission, and bulk download [^34^] |
| **Bulk Data** | Daily CSV files of all public objects available for download [^28^] |
| **Coverage** | SNe, novae, TDEs, kilonovae, AGN flares, FRBs (but NOT variable stars or asteroids) [^34^] |

- **Access Methods**: Web interface, REST API, daily CSV bulk download, Python client (tns-api on PyPI) [^96^][^28^]
- **CSV Columns**: objid, name, ra, declination, redshift, type, discoverydate, discoverymag, filter, reporters, etc. [^28^]
- **AstroNotes**: Sub-system for distributing object-related notifications
- **LIGO Integration**: Dedicated pages for GW-triggered transient searches [^34^]

---

### 10. Open Supernova Catalog (OSC / Astrocats)

| Attribute | Details |
|-----------|---------|
| **URL** | github.com/astrocatalogs (originally sne.space) |
| **Content** | 36,000+ supernovae and candidates with metadata, light curves, spectra [^86^] |
| **Format** | Individual JSON files per supernova, hierarchical, human- and machine-readable |
| **Rebuilding** | Automatically rebuilt daily from dozens of sources |
| **Access** | Full download via git; individual objects via web interface |
| **Spectra** | ~5,000 objects with spectra [^81^] |
| **Photometry** | Multi-band light curves from X-ray to radio |

- **ML Applications**: Ideal for training classification models, anomaly detection, light curve fitting [^81^]
- **SNAD project** used OSC for anomaly detection, identifying 81 interesting objects [^158^]
- **Bulk download**: Entire dataset downloadable in minutes via git [^86^]

---

## Simulated/Mock Data Available Now

### For LSST/Rubin Preparation

| Dataset | Description | Volume | Access |
|---------|-------------|--------|--------|
| **DP0 (DESC DC2)** | 300 deg2, 5-year WFD simulation with SNe Ia, galaxies, stars. Processed with LSST Science Pipelines [^374^] | Images + catalogs (multi-TB) | RSP at data.lsst.cloud |
| **PLAsTiCC** | Photometric LSST Astronomical Time-Series Classification Challenge. 8000 training + 3.5M test events, 15 classes [^97^] | ~3.5M light curves | Available via PLAsTiCC archive |
| **ELAsTiCC** | Extended challenge with ~5M detected events, ~50M alerts streamed to brokers. Two campaigns: Sep 2022-Jan 2023 (ELAsTiCC1) and Nov-Dec 2023 (ELAsTiCC2) at 3x rate [^334^] | ~50M alerts | DESC TOM; github.com/LSSTDESC/elasticc |
| **SuperNNova** | 1,983,213 simulated light curves (7 SN types: Ia, Ib, Ic, II-n, IIL1, IIL2, IIL3) with SALT2 fits [^100^] | ~2M light curves | Zenodo (doi: 10.5281/zenodo.3265189) |
| **DESC DC2 Truth Tables** | Supernova summary truth tables, galaxy/star truth, variability truth [^370^] | Fits files | DESC Data Portal via Globus |

### For Roman Space Telescope Preparation

| Dataset | Description | Volume | Access |
|---------|-------------|--------|--------|
| **Hourglass** | Roman HLTDS simulation: 64,000+ transients, 11M photometric obs, 500K spectra, 10 transient types [^269^] | Catalogs, light curves | Zenodo (doi: 10.5281/zenodo.14262943); GitHub: Roman-Supernova-PIT/hourglass_snana_sims |
| **Synthetic Roman Images** | 2-year time series with ~1,050 SNe Ia in 1 deg2 [^266^] | Images + catalogs | roman.ipac.caltech.edu/sims/SN_Survey_Image_sim.html |
| **OpenUniverse2024** | Joint Roman+Rubin: 70 deg2 imaging, Diffsky models [^335^] | ~400 TB total | Public release (10 TB subset released, 390 TB following) |
| **Joint Roman-Rubin 20 deg2** | Overlapping synthetic imaging surveys [^338^] | Images + catalogs | arXiv:2209.06829 |

### For Neutrino Detector Preparation

| Dataset | Description | Access |
|---------|-------------|--------|
| **SNEWPY** | Python package with hundreds of CCSN, thermonuclear, and PISN simulations [^373^] | pip install snewpy; snewpy.readthedocs.io |
| **SNOwGLoBES** | Event rate calculator for neutrino detectors | Integrated with SNEWPY |
| **sntools** | Event generator for neutrino interactions | GitHub |

### General Supernova Simulation Tools

| Tool | Description | Access |
|------|-------------|--------|
| **SNANA** | Industry-standard simulation+fitting package for SN light curves. Supports MLCS2k2, SALT2, SNooPy models [^251^][^281^] | Public; github.com/RickKessler/SNANA |
| **SNANA-generated data** | Simulated light curves for any survey configuration | Custom generation via SNANA |
| **SALT2/SALT3** | Spectral Adaptive Lightcurve Template for SNe Ia. SALT3 is improved redesign [^353^][^359^] | sncosmo Python package |
| **Maven** | Multimodal foundation model for supernova science. Uses SNANA simulations for training (500K events, 5 classes) [^280^] | GitHub (cmu-ml4ai/maven) |

---

## Alert Stream Formats and Protocols

### LSST/Rubin Alert Format
- **Serialization**: Apache Avro (binary format) [^290^][^298^]
- **Schema**: alert_packet schema with nested sub-schemas (lsst.alert namespace) [^298^]
- **Packet Size**: ~82 KB per alert (with 12-month history and cutouts) [^210^]
- **Lite Packets**: Subset without history and cutouts (drastically smaller)
- **Stream Rate**: 0.2 - 5 Gbps estimated [^210^]
- **Content per packet**: diaSource (triggering detection), diaObject (source history), 12-month DIA history, SSObject if applicable, FITS cutouts (science, difference, template), MPC orbits [^290^]
- **Update History**: Includes previous detections from past 12 months
- **Access**: World-public with no proprietary period [^290^]

### Community Brokers
Seven full-stream brokers receive and process all LSST alerts [^44^]:

| Broker | URL | Strengths | ML Classification |
|--------|-----|-----------|-------------------|
| **ALeRCE** | science.alerce.online | Rich web portal, early SN ID, TNS reporting | Rich ML taxonomy [^44^] |
| **AMPEL** | ampel.zeuthen.desy.de | Highly modular, flexible workflows | Modular classifier system [^210^] |
| **ANTARES** | antares.noirlab.edu | Multi-wavelength cross-match, user filters | ML shape models [^44^] |
| **Babamul** | babamul.caltech.edu | Lightweight, focused channels, open-source | ML-based workflows [^44^] |
| **Fink** | fink-broker.org | Community-driven, modular, Kafka-based | ML algorithms, external models [^210^] |
| **Lasair** | lasair.lsst.ac.uk | SQL-based filtering, cross-match, rich features | ML classifiers [^210^] |
| **Pitt-Google** | pitt-google.readthedocs.io | Google Cloud, proven stream processing | SuperNNova Ia vs non-Ia [^372^] |

- **Downstream brokers**: SNAPS, POI Broker (receive subsets via full-stream brokers)
- **Pitt-Google streams**: Includes lsst-supernnova topic with SuperNNova Ia vs non-Ia classification [^372^]
- **Pitt-Google BigQuery**: Archives alert data, classification results, variability indices [^372^]

---

## Trends & Signals

1. **Convergence on Avro+Kafka**: The LSST alert ecosystem (Avro serialization, Kafka streaming) has become the de facto standard, with ZTF as a successful precursor proving the architecture at 10% scale [^210^].

2. **Broker-as-a-Service Model**: Seven competing but collaborating brokers provide different interfaces and specializations, with interoperability as a key design principle [^44^][^210^].

3. **Synthetic Data Precedence**: OpenUniverse2024 (400 TB), DESC DC2 (300 deg2), and Hourglass demonstrate that large-scale simulated datasets are being produced specifically to prepare pipelines BEFORE operations begin [^335^][^336^][^269^].

4. **Neutrino-Supernova Alert Maturity**: SNEWS 2.0 with IceCube provides a working, tested real-time alert system for galactic core-collapse supernovae, with automated trigger formation and multi-messenger distribution [^292^][^352^].

5. **Citizen Science Integration**: Zooniverse Supernova Hunters and SNAD demonstrate the value of crowd-sourced labeling for improving detection algorithms and finding anomalies [^321^][^158^].

6. **Foundation Models for SNe**: Maven represents a new direction - multimodal foundation models trained on simulated data that can generalize across different survey configurations and data types [^280^].

7. **NIR+Optical Synergy**: Roman+Rubin+Euclid joint analyses will provide unprecedented multi-wavelength coverage, with simulations already demonstrating 20-50% improvements in distance measurements [^276^][^338^].

8. **Radio Transient Renaissance**: ASKAP VAST (0.5M sources, DR1) and LOFAR LoTSS-DR3 (13.6M sources) are mapping the radio transient sky at unprecedented scale [^369^][^384^].

---

## Recommended Deep-Dive Areas

### High Priority for ML Projects

1. **LSST Alert Broker Data Streams** - All seven brokers are operational now with ZTF data. Begin developing classification pipelines using ZTF alert streams from Fink, ALeRCE, or ANTARES. Transition code to LSST format using DP0 simulated data.

2. **OpenUniverse2024 Joint Simulations** - The 400 TB dataset provides matched Roman+Rubin imaging of the same simulated sky. Ideal for developing joint-analysis ML pipelines that will work with real data from both telescopes starting in 2027.

3. **ELAsTiCC2 Dataset** - 50M alerts with broker classifications from Nov-Dec 2023 campaign. Contact DESC for access via TOM. Ideal for training end-to-end real-time classification systems.

4. **SNANA + SuperNNova Pipeline** - Well-established simulation-to-classification pipeline. Generate custom simulated light curves for any target survey configuration, then train classifiers.

5. **Pitt-Google SuperNNova Stream** - Production Ia vs non-Ia classification on live LSST alerts. Can consume the lsst-supernnova Pub/Sub topic directly for real-time training data.

### Medium Priority

6. **Hourglass Roman Simulation** - Zenodo-hosted catalogs with 64,000+ transients. Begin training Roman-specific classifiers before launch.

7. **SNEWPY for Neutrino-Astronomy ML** - Interface supernova simulations with detector response models. Develop ML pipelines for real-time neutrino signal classification in DUNE/protoDUNE data.

8. **TNS Bulk Download for Historical Analysis** - Daily CSV files of all public transients. Excellent for population studies, rate calculations, and training classification models.

9. **Open Supernova Catalog** - 36,000+ SNe with light curves and spectra in JSON. Download via git for local analysis, anomaly detection, and light curve model training.

10. **ASKAP VAST Radio Light Curves** - 6.4M measurements of 0.5M sources. Develop radio-transient detection/classification for SKA-era preparation.

### Future-Looking

11. **DUNE Supernova Trigger Development** - ProtoDUNE data available now. Train deep learning models on simulated LArTPC images for supernova neutrino detection (see YOLOv3 work at Bristol [^316^]).

12. **LOFAR2.0 Radio Transient Pipeline** - Upgrade will double sensitivity. Prepare transient detection ML on current LoTSS-DR3 data.

13. **CTA/CTAO Real-Time Transient Detection** - Gamma-ray burst and transient follow-up pipeline under development. Opportunity for ML-based rapid classification.

---

## References

[^44^] Rubin Observatory Alerts and Brokers: https://rubinobservatory.org/for-scientists/data-products/alerts-and-brokers
[^50^] Rubin Observatory Real-Time Alerts: https://news.stanford.edu/stories/2026/02/rubin-observatory-real-time-alerts-astronomical-events
[^81^] VizieR Open Supernova Catalog Anomaly Detection: https://ui.adsabs.harvard.edu/abs/2023yCat..74893591P/abstract
[^86^] Open Catalog for Supernova Data (Guillochon et al. 2016): https://arxiv.org/abs/1605.01054
[^96^] TNS API Python Client (PyPI): https://pypi.org/project/tns-api/
[^97^] PLAsTiCC Data Model: https://lsstdesc.org/SN-PWV/overview/plasticc_model.html
[^100^] SuperNNova Simulations on Zenodo: https://zenodo.org/records/3265189
[^158^] SNAD Anomaly Detection: https://arxiv.org/html/2410.18875v1
[^210^] Overview of Astronomical Transient Brokers (Vujcic et al. 2025): https://www.astro.sk/caosp/Eedition/FullTexts/vol55no2/pp95-105.pdf
[^212^] Rubin Observatory Alert Brokers Information: https://www.lsst.org/node/1151
[^248^] ZTF SN Ia DR2 Light-curve Fits (A&A 2025): https://www.aanda.org/articles/aa/full_html/2025/02/aa50377-24/aa50377-24.html
[^251^] SNANA Supernova Analysis Package: https://inspirehep.net/files/a2452794f4699573e416e0c2f90be66d
[^263^] Roman Supernova PIT Papers (Hourglass): https://www.romansnpit.com/papers
[^266^] Synthetic Roman SN Survey (Wang et al. 2022): https://arxiv.org/abs/2204.13553
[^268^] Synthetic Roman Survey (MNRAS 2023): https://ui.adsabs.harvard.edu/abs/2023MNRAS.523.3874W/abstract
[^269^] The Hourglass Simulation (ApJ 2025): https://iopscience.iop.org/article/10.3847/1538-4357/ade1d6
[^270^] Rubin DP1 Documentation/Slides: https://indico.ijclab.in2p3.fr/event/11610/contributions/38679/attachments/26430/39218/
[^271^] Roman Space Telescope For Scientists: https://science.nasa.gov/mission/roman-space-telescope/roman-for-scientists/
[^272^] Roman WFI Data Levels and Products: https://roman-docs.stsci.edu/data-handbook/wfi-data-levels-and-products
[^273^] Recovered SN Ia Rate from Simulated LSST Images (A&A 2024): https://www.aanda.org/articles/aa/full_html/2024/06/aa49012-23/aa49012-23.html
[^274^] Euclid Q1 Quick Data Release: https://pubs.euclid-ec.org/public/coordinated_release/duffy_etal.pdf
[^276^] SN Ia Cosmology with Euclid: https://hal.science/hal-03862328v1/file/stad2179.pdf
[^277^] Supernovae with Euclid: https://sci.esa.int/c/portal/doc.cfm?fobjectid=46458
[^278^] Countdown to Data Preview Zero: https://www.lsst.org/news/countdown-data-preview-zero
[^280^] Maven Multimodal Foundation Model: https://iopscience.iop.org/article/10.1088/2632-2153/ad990d
[^290^] LSST Alert Packets Documentation: https://prompt-products.lsst.io/products/alerts/index.html
[^291^] Rubin Observatory Early Science Program: https://rubinobservatory.org/for-scientists/resources/early-science
[^292^] IceCube Supernova Sensitivity (arXiv 2021): https://arxiv.org/abs/2107.08098
[^293^] GW170817 Multi-messenger Discovery: http://ligo.org/science-summaries/GW170817MMA/
[^295^] IceCube Real-Time Alerts: https://icecube.wisc.edu/science/real-time-alerts/
[^296^] AAVSO History and Archives: https://www.aavso.org/AAVSO-History
[^297^] IceCube Supernova Fire Drills (PoS ICRC2023): https://par.nsf.gov/servlets/purl/10514308
[^298^] Design of LSST Alert Distribution System: https://dmtn-093.lsst.io/
[^300^] IceCube on GCN: https://gcn.nasa.gov/missions/icecube
[^315^] CTA DAp Team: https://irfu.cea.fr/en/dap/cta-cherenkov-telescope-array-2/
[^316^] DUNE Real-time Object Detection (Thesis): https://research-information.bris.ac.uk/en/studentTheses/real-time-object-detection-for-neutrino-interactions-in-the-dune-/
[^317^] Zooniverse Supernova Hunters: https://www.discovermagazine.com/zooniverse-a-citizen-science-success-story-43760
[^318^] Supernova Neutrino Detection in DUNE: https://indico.in2p3.fr/event/17490/contributions/63456/attachments/49170/62325/
[^319^] DUNE Prepares for Data Onslaught: https://news.fnal.gov/2020/05/dune-prepares-for-data-onslaught/
[^320^] CTA Observatory Overview: https://www.eoportal.org/other-space-activities/cta
[^321^] Zooniverse Supernova Hunters Project: https://www.zooniverse.org/projects/dwright04/supernova-hunters
[^322^] Supernova Neutrinos in DUNE (NuFact 2025): https://indico.cern.ch/event/1528564/contributions/6619075/
[^323^] DUNE SN Burst Detection (EPJC 2021): https://link.springer.com/article/10.1140/epjc/s10052-021-09166-w
[^324^] Zooniverse Online Citizen Science (PMC 2018): https://pmc.ncbi.nlm.nih.gov/articles/PMC10245346/
[^325^] CTAO at ESO Paranal: https://www.eso.org/public/teles-instr/paranal-observatory/ctao/
[^327^] The Cherenkov Telescope Array (arXiv 2023): https://arxiv.org/abs/2305.12888
[^331^] Amateur Discovers Supernova: https://www.universetoday.com/articles/dedicated-amateur-discovers-supernova-in-remote-galaxy
[^332^] Rubin Launches Real-Time Discovery Machine: https://noirlab.edu/public/news/noirlab2605/
[^333^] Birth of a Supernova (Nature 2018): https://hal.science/hal-01730136v1/file/nature25151.pdf
[^334^] DESC ELAsTiCC Challenge: https://portal.nersc.gov/cfs/lsst/DESC_TD_PUBLIC/ELASTICC/
[^335^] OpenUniverse2024 (MNRAS 2025): https://ui.adsabs.harvard.edu/abs/2025MNRAS.544.3799O/abstract
[^336^] Rubin and Roman Cosmic Sneak Peek: https://www6.slac.stanford.edu/news/2024-06-12-rubin-observatory-and-roman-space-telescope-get-cosmic-sneak-peek-supercomputers
[^337^] Amateur Captures Rare First Light: https://keckobservatory.org/amateur-astronomer-captures-rare-first-light-of-massive-exploding-star/
[^338^] Joint Roman-Rubin Synthetic Survey (arXiv 2022): https://arxiv.org/abs/2209.06829
[^339^] Supernova Links (Rochester Astronomy): http://www.rochesterastronomy.org/snimages/snlinks.html
[^352^] SNEWS 2.0 Alert Software (arXiv 2024): https://arxiv.org/abs/2406.17743
[^353^] SALT2 Light Curve Fits (A&A 2025): https://arxiv.org/html/2406.02073v2
[^354^] Sternberg SN Catalog (NASA): https://data.nasa.gov/dataset/sternberg-astronomical-institute-catalog-of-supernovae
[^356^] SNEWS 2.0 Workshop: https://indico.stfc.ac.uk/event/382/attachments/706/1241/snews-new.pdf
[^358^] SNEWS Wikipedia: https://en.wikipedia.org/wiki/SuperNova_Early_Warning_System
[^360^] SNEWS 2.0 Website: https://snews2.org/
[^369^] ASKAP VAST DR1 (arXiv 2026): https://arxiv.org/abs/2602.22739
[^370^] DESC DC2 Data Release Note: https://arxiv.org/html/2101.04855v5
[^372^] Pitt-Google Client Documentation: https://mwvgroup.github.io/pittgoogle-client/listings.html
[^373^] SNEWPY Pipeline (arXiv 2021): https://arxiv.org/abs/2109.08188
[^374^] DP0.2 Data Products: https://dp0-2.lsst.io/v/roll-back/data-products-dp0-2/index.html
[^375^] SNEWPY Documentation: https://snewpy.readthedocs.io/
[^384^] LOFAR LoTSS-DR3 (A&A 2026): https://www.aanda.org/articles/aa/full_html/2026/03/aa57749-25/aa57749-25.html
[^385^] Largest Radio Sky Survey (LOFAR): https://www.lofar.eu/largest-ever-radio-sky-survey-maps-the-universe-in-unprecedented-detail/
[^386^] LOFAR Technical Paper: https://insu.hal.science/insu-01288431/document
[^387^] JWST SN at z=2.83: https://ui.adsabs.harvard.edu/abs/2024ApJ...972L..13S
[^388^] SNe with LOFAR (Thesis): http://www.diva-portal.org/smash/record.jsf?pid=diva2:1893017

---

## Data Availability Cheat Sheet

| What You Need | Where to Get It | Status |
|---------------|-----------------|--------|
| LSST-like simulated images + catalogs | DP0 (RSP at data.lsst.cloud) | **Available NOW** |
| Real LSST commissioning data + DIA | DP1 (RSP; data rights required) | **Available NOW** |
| LSST simulated alerts (50M) | ELAsTiCC via DESC TOM | **Available NOW** |
| LSST simulated light curves (3.5M) | PLAsTiCC archive | **Available NOW** |
| LSST simulated light curves (2M, 7 types) | SuperNNova on Zenodo | **Available NOW** |
| Joint Roman+Rubin simulated imaging (400 TB) | OpenUniverse2024 | **Available NOW** |
| Roman HLTDS simulation (64K transients) | Hourglass on Zenodo | **Available NOW** |
| Roman SN images (~1,050 SNe Ia) | roman.ipac.caltech.edu/sims | **Available NOW** |
| Real-time ZTF alerts (test broker streams) | Fink/ALeRCE/ANTARES/Lasair | **Available NOW** |
| Historical SN metadata + light curves (36K+) | Open Supernova Catalog (GitHub) | **Available NOW** |
| Classified transient reports (daily CSV) | Transient Name Server (TNS) | **Available NOW** |
| Supernova neutrino simulations | SNEWPY (pip install) | **Available NOW** |
| Radio SN light curves (0.5M sources) | ASKAP VAST DR1 (CSIRO DAP) | **Available NOW** |
| Low-frequency radio sky (13.6M sources) | LOFAR LoTSS-DR3 (LTA) | **Available NOW** |
| Real-time neutrino supernova alerts | SNEWS 2.0 (snews2.org) | **Operational** |
| Citizen science SN classifications | Zooniverse Supernova Hunters | **Active** |
| LSST real-time alerts | 7 community brokers | **Operational (Feb 2026)** |
| Roman real data | Launch by May 2027 | **Pending** |
| DUNE supernova neutrinos | ProtoDUNE now, DUNE ~2028-29 | **Partial/Construction** |
| SKA radio transients | ASKAP/MeerKAT pathfinders now | **Partial/Construction** |
| CTA gamma-ray transients | Construction ongoing | **Pending** |

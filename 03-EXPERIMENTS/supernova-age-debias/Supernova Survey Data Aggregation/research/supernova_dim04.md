# Dimension 04: Spectroscopic Archives for Machine Learning

*Research Date: 2026-01-21*
*Searches Conducted: 25 independent queries*
*Sources Consulted: arXiv, official survey websites, GitHub, ADS, ESO archive, journal papers*

---

## Executive Summary

Spectroscopic archives are foundational for supernova (SN) ML projects, providing training labels for photometric classifiers, physical parameters for anomaly detection, and cross-validation data. This document inventories all major spectroscopic datasets, tools, and access methods for SN spectroscopy ML. The central hub is **WISeREP** (72,503 spectra for 29,468 objects), with major contributions from **SNfactory** (300+ SNe Ia with integral-field spectrophotometry), **PESSTO/ePESSTO+** (thousands of classification spectra), **BSNIP** (1,298 spectra of 582 SNe Ia), and upcoming **4MOST/TiDES** (projected 30,000 live transient spectra).

---

## Table of Contents

1. [WISeREP: The Central Spectroscopic Repository](#1-wiserep-the-central-spectroscopic-repository)
2. [SNfactory and SNIFS: Spectrophotometric Time Series](#2-snfactory-and-snifs-spectrophotometric-time-series)
3. [SDSS-V: Large-Scale Spectroscopic Survey](#3-sdss-v-large-scale-spectroscopic-survey)
4. [4MOST/TiDES: Future Spectroscopic Follow-up](#4-4mosttides-future-spectroscopic-follow-up)
5. [Telescope Archives: Keck, VLT, Gemini](#5-telescope-archives-keck-vlt-gemini)
6. [PESSTO/ePESSTO+: ESO Public Spectroscopic Survey](#6-pesstoepesteso-public-spectroscopic-survey)
7. [Other Major Spectroscopic Datasets](#7-other-major-spectroscopic-datasets)
8. [Spectral Classification Tools](#8-spectral-classification-tools)
9. [Spectral Features for ML: Databases and Extraction](#9-spectral-features-for-ml-databases-and-extraction)
10. [Spectroscopic vs Photometric Classification Accuracy](#10-spectroscopic-vs-photometric-classification-accuracy)
11. [Cross-Matching Spectra with Photometric Light Curves](#11-cross-matching-spectra-with-photometric-light-curves)
12. [Converting Spectra to ML Features](#12-converting-spectra-to-ml-features)
13. [Summary Table of All Datasets](#13-summary-table-of-all-datasets)
14. [Recommended Data Access Workflows for ML](#14-recommended-data-access-workflows-for-ml)
15. [Flagged Areas for Deeper Investigation](#15-flagged-areas-for-deeper-investigation)

---

## 1. WISeREP: The Central Spectroscopic Repository

**Overview**: WISeREP (Weizmann Interactive Supernova data REPository) is the primary global archive for supernova spectroscopy, hosted at the Weizmann Institute. As of wide exploration data, it contains 72,503 spectra for 29,468 objects [^116^].

### 1.1 Data Access Methods

#### Web Interface
- **URL**: https://www.wiserep.org
- **Object Search**: Query by name, coordinates, redshift, type, date range
- **Spectra Search**: Query by instrument, observer, date range, phase, SN type
- **Bulk Download via UI**: Download query results as CSV/TSV/JSON metadata + physical spectrum files
- **Formats**: ASCII (.txt), FITS (.fits), or both; metadata in CSV/TSV/JSON

#### Bulk Download via Scripted URL Looping
WISeREP supports parameterized URL queries for automated bulk downloads [^116^]:

```
https://www.wiserep.org/search/spectra?&type_family=1&instruments=1&format=tsv&files_type=ascii&num_page=100&page=0
```

Key parameters:
- `format=tsv|csv|json` - metadata output format
- `files_type=ascii|fits|both` - spectrum file format
- `type_family=1` - SN family filter
- `instruments=N` - instrument filter (e.g., 1=P200-DBSP)
- `num_page=250` - results per page (max 250 for spectra)
- `page=0..N` - page number for iteration
- `personal_api_key=XXX` - for accessing private data

**Python API for URL Construction**:
```python
import requests
base_url = "https://www.wiserep.org/search/spectra"
params = {
    "type_family": 1,
    "format": "csv",
    "files_type": "ascii",
    "num_page": 250,
    "page": 0
}
response = requests.get(base_url, params=params)
```

### 1.2 Python API: `wiserep_api`

**Repository**: https://github.com/temuller/wiserep_api [^430^]
**PyPI Install**: `pip install wiserep_api`

**Capabilities**:
- Download SN lists by spectral type (40+ types supported including SN Ia, SN Ia-91T-like, SN Ib/c, SLSN-I, TDE, etc.)
- Download target spectra in bulk
- Run SNID automatically on downloaded spectra
- Get object properties (type, redshift, host, coordinates)

**Example Usage**:
```python
from wiserep_api.search import download_sn_list
from wiserep_api import download_target_spectra, get_target_property

# Download list of all SN Ia-91T-like objects
download_sn_list("SN Ia-91T-like")

# Download spectra for targets (exclude SEDM instrument)
sne_list = [...]  # list of SN names
for sn in sne_list:
    download_target_spectra(sn, file_type='ascii', exclude=['SEDM'])

# Get object properties
properties = ['type', 'redshift', 'host', 'coords', 'coords_deg']
values = get_target_property('2004eo', properties)
```

### 1.3 WISeWEBSpider: Bulk Scraping Tool

**Repository**: https://github.com/jparrent/WISeWEBSpider [^118^]

A dedicated scraping tool for downloading all publicly available supernova spectra from WISeREP when bulk download is not available through the UI. Features:
- Creates `sne-external-WISEREP/` directory structure
- Stores spectra in individual subdirectories with `README.json` metadata
- Guards against duplicates and already-collected spectra
- Update mode for incremental downloads
- Full runtime: ~18.7 hours for complete scrape; update mode takes minutes

```bash
# Initial scrape
python3 -m wisewebspider

# Update mode (last 30 days)
python3 -m wisewebspider --update --daysago 30
```

### 1.4 WISeREP Object Page API

Individual object pages follow RESTful URL patterns [^116^]:
```
https://wiserep.org/iauname/2013fs
https://wiserep.org/internal-name/iPTF13dqy
```

### 1.5 Data Formats

- **ASCII**: Space-delimited text files with wavelength, flux, flux_error columns
- **FITS**: Standard FITS format with wavelength, flux, flux_error in separate extensions
- **Metadata**: JSON/CSV/TSV with object name, type, redshift, date, observer, instrument, telescope
- **Spectral types supported**: SN Ia, SN Ib/c, SN II, SLSN, TDE, AGN, Galaxy, and 30+ subtypes

### 1.6 NGSF Online Classification Tool

WISeREP hosts an online execution of the Next Generation SuperFit (NGSF) spectral classification tool directly on the Spectra Search Page [^116^]. Users can click the "iF" icon on any spectrum to run automated classification without downloading data. Execution time: seconds to minutes.

---

## 2. SNfactory and SNIFS: Spectrophotometric Time Series

**Overview**: The Nearby Supernova Factory (SNfactory) is an international collaboration led by Greg Aldering at Lawrence Berkeley National Laboratory, focused on low-redshift (z < 0.1) Type Ia supernovae with precise integral-field spectrophotometry [^150^].

### 2.1 SNIFS Instrument

**SuperNova Integral Field Spectrograph (SNIFS)** [^478^][^483^]:
- **Telescope**: University of Hawaii 2.2-m (UH2.2m)
- **Field of View**: 6" x 6" (15 x 15 spaxels, 0.43" per spaxel)
- **Wavelength Coverage**: 3200-10,000 AA (Blue: 3200-5200 AA, Red: 5100-9700 AA)
- **Resolution**: R ~ 1000-1200
- **Features**: Simultaneous photometric channel for flux calibration; host-galaxy subtraction; atmospheric extinction monitoring
- **Spectrophotometric Precision**: < 5% under photometric conditions [^478^]

### 2.2 Data Releases

#### 2020 Interim Release (Primary Public Dataset) [^150^][^464^]
- **210 SNe Ia** with spectrophotometric time series
- **~2,500 individual spectra** from observations between 2004-2013
- **Flux-calibrated spectra** from 3300-8600 AA
- **Host-galaxy subtractions** and extinction corrections included
- **Access**: Available via Centre de Donnees astronomiques de Strasbourg (CDS)
- **Companion models**: SNEMO and SUGAR training versions
- **Phase coverage**: -5 to +50 days post-maximum light
- **Median epochs per SN**: ~14

#### SNfactory Data Page
- **URL**: http://snfactory.lbl.gov/snf/data/index.html [^199^]
- **Also hosted at**: NERSC (USA) and CCIN2P3 (France)
- **SNfactory Zoo**: Interactive interface for data exploration (internal use, planned public release)

#### Data Release 13 (2021) and DR14 (2022)
- Continued releases of standardized light curves and spectra
- 2024 publications analyzing 4,000+ standard-star spectra for spectrophotometric precision

#### SCAT Survey (using SNIFS post-2018)
The Spectroscopic Classification of Astronomical Transients (SCAT) survey uses SNIFS for public transient spectrophotometry [^478^][^489^]:

**SCAT DR1** [^489^]:
- **1,810 spectra of 1,330 transients** (March 2018 - January 2023)
- **Breakdown**: 838 SNe Ia spectra (722 objects), 392 SNe II (275), 125 SNe Ibc (78), 171 nuclear transients (48), 229 stellar phenomena (172)
- **Download**: https://zenodo.org/records/19188201
- **Light curves**: Multi-filter light curves from imaging surveys with phenomenological fits
- **Host galaxies**: Associations, redshifts, distances, projected offsets
- **Formats**: FITS and ASCII spectra, summary plots, light curve data
- **Data volume**: ~1 GB science data products
- **Additional packages**: Summary figures (~200 MB), ASCII-only spectra (~150 KB), standard-star spectra (~300 MB)

### 2.3 SUGAR Model

**URL**: https://snfactory.lbl.gov/sugar/index.html [^457^]

SUGAR (SUpernova Generator And Reconstructor) is a spectro-temporal model for SNe Ia trained on SNfactory spectrophotometric data [^461^][^190^].

**Key Features**:
- Trained on 171 SNe Ia spectral time series
- Uses 13 spectral indicators near maximum light (pseudo-EWs, P-Cygni minima)
- Extracts 3 intrinsic factors via factor analysis (more robust than PCA with errors)
- Factor 1: Coherent variation of pseudo-EWs (Si, Ca lines) - correlated with stretch
- Factor 2: Velocities - weakly linked with pseudo-EWs except Ca II H&K and S II W
- Factor 3: Slight correlation with stretch
- Provides SED model as function of time and wavelength
- Color curve compatible with Cardelli et al. (1989) extinction with R_V = 2.6

**Publications**: Leget et al. 2020 (A&A) [^461^]
**Spectral time series training data**: Available at the SUGAR website

### 2.4 SNEMO Model

SNEMO (SuperNova Eigenvectors using MOrlet wavelets) is a spectral template model for SNe Ia [^464^]:
- Uses wavelet-based decomposition of spectral time series
- Publications: Saunders et al. 2018 (arXiv:1810.09476)
- Companion to SUGAR for SNfactory data

---

## 3. SDSS-V: Large-Scale Spectroscopic Survey

### 3.1 SDSS-V DR19 Overview

SDSS-V DR19 (Data Release 19) is the second data release of the fifth Sloan Digital Sky Survey, described in detail in Almeida et al. (2025) [^395^][^397^].

**DR19 Contents** [^397^]:
- 479,081 optical BOSS spectra of stars (Milky Way Mapper)
- 390,676 near-infrared APOGEE spectra of stars
- 318,123 galaxy and quasar/AGN spectra (Black Hole Mapper)
- Preview IFU data of Helix Nebula from Local Volume Mapper
- 9 Value Added Catalogs (VACs)

### 3.2 Data Access [^396^][^395^]

**Science Archive Server (SAS)**:
- URL: https://data.sdss.org/sas/
- Bulk download via wget, rsync, Globus Online
- All data in FITS format

**Catalog Archive Server (CAS) / SkyServer**:
- SQL queries and Jupyter notebook interfaces
- Web: https://skyserver.sdss.org

**Zora Web Framework** (NEW for DR19):
- URL: https://dr19.sdss.org/zora
- Interactive search, target visualization, sky viewer, data dashboard
- Replaces previous Science Archive Webapp (SAW)

**Valis API Backend** (NEW for DR19):
- Programmatic API built in FastAPI
- Endpoints: query, target, info, maskbits
- Documentation: https://api.sdss.org/valis/docs
- Powers Zora frontend, usable independently in Python scripts

**SciServer Compute**:
- Jupyter notebooks with programmatic SDSS data access
- Tutorial notebooks: https://github.com/sdss/dr19_tutorials

### 3.3 SDSS-II Supernova Survey (Legacy)

The completed SDSS-II Supernova Survey is part of SDSS legacy data [^397^]:
- Multi-epoch imaging and spectroscopy of SNe Ia
- Light curves and spectra publicly available
- Now available through SDSS Legacy Archive at MAST (Mikulski Archive for Space Telescopes)

### 3.4 Supernova-Specific Data Products

While SDSS-V DR19 focuses on stellar and galaxy spectroscopy, the pipeline infrastructure provides:
- Optical BOSS spectra (R ~ 2000, 3650-10,400 AA)
- APOGEE NIR spectra (R ~ 22,500, 1.5-1.7 um)
- Time-domain capabilities through Milky Way Mapper multi-epoch observations
- **Future**: SDSS-V continues to collect data; DR20 will include southern hemisphere data

---

## 4. 4MOST/TiDES: Future Spectroscopic Follow-up

### 4.1 Overview

**TiDES** (Time Domain Extragalactic Survey) is the 4MOST spectroscopic follow-up survey for Rubin/LSST-era transients [^394^][^459^][^461^].

**4MOST Instrument** [^461^]:
- 4-meter Multi-Object Spectroscopic Telescope on ESO VISTA
- 2,436 science fibers over 4.2 deg2 field-of-view
- Low-resolution spectrograph (R ~ 4000-6500)
- Wavelength coverage: 370-950 nm (optical), 650-1000 nm (near-infrared, with 4MOST-HR)
- 5-year survey duration

### 4.2 TiDES Science Program

Three interlocking surveys [^394^][^461^]:

#### TiDES-Live: Live Transient Spectroscopy
- **>30,000 live transient spectra** with SNR15 >= 3
- **~12,600 SNe Ia** with light curve quality for cosmology
- **>9,000 core-collapse SNe**
- Largest sample of rare faint-and-fast transients to date
- Classifies transients down to r = 22.5 mag (AB)
- Redshift range: z ~ 0.5

#### TiDES-Hosts: Host Galaxy Redshifts
- **>200,000 host galaxies** observed
- **~131,000 SNe Ia hosts** suitable for cosmology
- Redshift range: z ~ 1
- Enables photometric classification improvement

#### TiDES-RM: AGN Reverberation Mapping
- 700-1,000 AGN monitored
- Redshift range: z ~ 2.5
- Complements SN Ia cosmology

### 4.3 Cosmological Impact

- Hubble Diagram with **at least 143,000 objects** (combining live-SNe Ia + photometric SNe Ia with host redshifts)
- Capable of **sub-2% measurement of dark energy equation-of-state parameter w**
- Largest homogeneous sample of SNe and host galaxies to date
- Serves as **critical spectral training set** for photometrically-classified LSST SNe Ia [^394^]

### 4.4 Key Paper

Frohmaier et al. (2025), "TiDES: The 4MOST Time Domain Extragalactic Survey," ApJ [^394^][^459^].

---

## 5. Telescope Archives: Keck, VLT, Gemini

### 5.1 Keck Observatory Archive (KOA)

**URL**: https://koa.ipac.caltech.edu [^431^]

**Features**:
- Archives all science and calibration observations since 1994
- Public data available after 18-month proprietary period
- 8 active instruments + 2 decommissioned
- Reduced browse products for HIRES, NIRC2, NIRSPEC, LWS, OSIRIS
- Web query interface + API access
- **API documentation**: https://koa.ipac.caltech.edu/cgi-bin/TestAPI/nphTestAPI.py
- Example Python code available for programmatic access

**Supernova Access**:
- Search by target name, coordinates, instrument (LRIS, DEIMOS, HIRES)
- DEIMOS 1200G grating data used for stellar/supernova spectroscopy [^398^]
- Data products include reduced 1D spectra and multi-epoch measurements

### 5.2 VLT/X-shooter at ESO

**ESO Science Archive Facility**: http://archive.eso.org [^456^]

#### X-shooter Science Data Products [^425^][^426^]
- 33,000+ spectra (2009-2013, growing with monthly releases)
- Three arms: UVB (300-560 nm), VIS (550-1000 nm), NIR (1000-2480 nm)
- Extracted, wavelength- and flux-calibrated 1D spectra
- Resolution: R ~ 3,300-11,000 depending on arm
- Query via Phase 3 generic form or spectral-specific query form
- Tagged: `XSHOOTER_ECBELLE`
- **Simple Spectral Access Protocol (SSAP)**: http://archive.eso.org/ssap

#### Programmatic Access [^463^]
```python
# Example ESO SSAP query
url = "http://archive.eso.org/ssap?REQUEST=queryData&POS=123.269560,-34.57804&SIZE=0.2"
```

**Key ESO Archive Access Methods**:
- **Science Portal**: Interactive browsing and download
- **TAP services**: `tap_obs` (raw/reduced data), `tap_cat` (scientific catalogues)
- **SSAP**: VO standard for 1D spectra discovery and access
- **DataLink**: Finds related files (calibrations, previews, progenitors)
- **SODA**: Server-side cutout for spectral and positional extraction
- **Authentication**: OAuth2.0 + basic auth for proprietary data

### 5.3 Gemini Observatory Archive

**URL**: https://archive.gemini.edu [^407^]

**Features**:
- All Gemini data since operations began
- Proprietary period: 12 months (18 months pre-2016A)
- Raw and reduced data products
- Automated DRAGONS processing (2026) for specific modes
- Quick-Look and Science-Quality classifications
- Calibration data auto-associated with science data

**Reduced Data Products**:
- Quick-Look: For rapid evaluation
- Science-Quality: Automated reduction, user verification recommended
- Both have same proprietary rights as raw data

**Supernova Spectroscopy**:
- GMOS (Gemini Multi-Object Spectrograph) spectroscopy of SNe [^409^][^415^]
- Data searchable by instrument (GMOS, GNIRS, NIFS), coordinates, date
- Reduced spectra available via archive

**API Access**:
- Python API documentation: https://archive.gemini.edu/help/api.html
- Example scripts for automated data retrieval

---

## 6. PESSTO/ePESSTO+: ESO Public Spectroscopic Survey

### 6.1 PESSTO (2012-2019)

**URL**: https://www.pessto.org [^494^]

The Public ESO Spectroscopic Survey of Transient Objects (PESSTO) and its successor ePESSTO+ provide the largest public collection of reduced transient spectra from the ESO New Technology Telescope (NTT).

**PESSTO SSDR4** (Full Survey Data Release) [^494^]:
- **4,631 transients classified** total
- **2,323 unique transient sources** including SNe, novae, TDEs, kilonova AT2017gfo
- **2323 unique sources with spectra**
- **337 science targets** with rich time-series data (3,748 spectral frames)
- **Time period**: April 2012 - April 2019
- **Total data volume**: 45 GB
- **Instruments**: EFOSC2 (optical), SOFI (NIR imaging and spectroscopy)
- **Access**: ESO Science Portal + programmatic
- **Reference**: Smartt et al. (2015), A&A 579, A40

**Instruments**:
- EFOSC2: 3345-9995 AA, resolution 13-18 AA
- SOFI: 0.935-2.53 um, resolutions 23-33 AA, JHK imaging

### 6.2 ePESSTO+ (2019-present)

**ePESSTO+ SSDR1** [^465^]:
- **2,138 EFOSC2 spectra** (first 2.5 years: April 2019 - October 2021)
- **2138 objects** with classification spectra
- **154 supernovae** selected for detailed follow-up
  - 25 super-luminous supernovae
  - 2 rare Icn transients
  - 1 SN imposter, 15 TDEs, 2 LBV, 2 AGN, 4 SN light echoes
- **178 Key Science targets** with time-series follow-up
- **1117 EFOSC2 spectra + 17 SOFI spectra** for Key Science targets
- **13.74 GB total data volume**
- Access via ESO Science Archive Facility Phase 3

### 6.3 PESSTO/ePESSTO+ Data Products

- Flux-calibrated 1D spectra in standard ESO Phase 3 format
- Absolute flux calibration accuracy: ~15% (EFOSC2), relative ~5%
- Telluric absorption correction
- Acquisition images for flux calibration refinement
- SOFI JHK imaging for NIR photometric calibration
- Classifications published publicly via WISeREP within 24 hours

---

## 7. Other Major Spectroscopic Datasets

### 7.1 Berkeley Supernova Ia Program (BSNIP)

**Reference**: Silverman et al. (2012), MNRAS 425, 1789 [^479^][^481^]

**Dataset**:
- **1,298 low-redshift (z < 0.2) optical spectra of 582 SNe Ia**
- Observed 1989-2008
- **584 spectra of 199 SNe Ia** with well-calibrated light curves and distance moduli
- Many spectra corrected for host-galaxy contamination
- Nearly 90 spectroscopically peculiar SNe Ia
- Typical wavelength range: 3300-10,400 AA (Kast spectrograph at Lick 3m)

**BSNIP DR2** [^480^]:
- **637 optical spectra** collected 2009-2018
- 626 spectra of 242 unambiguously classified SNe Ia
- 70 spectra of 30 peculiar SNe Ia
- 79 SNe Ia (328 spectra) with complementary photometry
- Median redshift: 0.0208
- Accessible via `sndata` Python package: `sndata.bsnip.Stahl20`

**SN Database**: http://hercules.berkeley.edu/database/index_public.html [^484^]

**Spectral Feature Measurements**: Automated measurements of velocities, pseudo-EWs, depths, fluxes for 432 spectra within 20 days of max of 261 SNe Ia [^485^]

### 7.2 OzDES (Australian Dark Energy Survey)

**Reference**: Lidman et al. (2020), MNRAS 496, 19 [^481^][^485^]

**Dataset**:
- **375,000 individual spectra** over 6 years
- Redshifts for **almost 30,000 sources**
- Some sources as faint as rAB = 24 mag
- 771 AGN monitored for reverberation mapping
- Hundreds of SNe classified
- Thousands of host galaxy redshifts in DES deep fields
- Used 2dF fiber positioner + AAOmega spectrograph on 3.9-m AAT

### 7.3 SEDM/P60 and ZTF Bright Transient Survey (BTS)

**SEDM**: Spectral Energy Distribution Machine [^510^][^151^]
- Very low-resolution (R ~ 100) IFU spectrograph on Palomar 60-inch
- 28 x 28 arcsec2 field-of-view
- Dedicated to ZTF transient classification
- pySEDM pipeline: flux-calibrated spectrum available within 5 minutes
- Wavelength: 3500-9500 AA
- **10,822 spectra** observed 2018-2022

**ZTF SN Ia DR2 Spectra** [^151^][^514^]:
- **5,138 spectra** associated with 3,628 spectroscopically confirmed SNe Ia
- 60% acquired by SEDM
- 28% have multiple spectra
- Custom SNID template library of 370 templates
- Classifications from SNID + visual inspection

### 7.4 Open Supernova Catalog

**Reference**: Guillochon et al. (2017), ApJ 835, 64 [^482^][^484^]

**Features**:
- **36,000+ supernovae** with observations and metadata
- Individual pages with metadata, light curves, spectra (X-ray to radio)
- Data parsed from dozens of sources including literature and web catalogs
- **JSON format**: Each SN stored in single hierarchical JSON file
- Rebuilt daily from git repositories
- **GitHub**: https://github.com/astrocatalogs
- Originally at sne.space (now operational via GitHub)
- Entire dataset downloadable in minutes

### 7.5 Carnegie Supernova Project (CSP)

Accessible via `sndata` Python package [^166^]:
- Optical and NIR photometry of SNe Ia
- Spectroscopic observations
- Data releases available programmatically

### 7.6 Lick Observatory Supernova Search (LOSS)

**Reference**: Stahl et al. (2019), MNRAS 490, 3882 [^495^][^503^]

**Dataset**:
- Follow-up program 2005-2018
- 78 spectroscopically normal SNe Ia with detailed follow-up
- Filtered photometry of 200 SNe, unfiltered photometry of 900 SNe
- Accessible via `sndata` Python package [^482^]

---

## 8. Spectral Classification Tools

### 8.1 SNID (SuperNova IDentification)

**Reference**: Blondin & Tonry (2007)
**Website**: https://people.lam.fr/blondin.stephane/software/snid/ [^435^]

**Features**:
- Template cross-matching for SN type, redshift, and age determination
- Current version: 5.0
- Extensive template libraries:
  - Default templates: 2.0 set (6.2 MB)
  - BSNIP SN Ia templates
  - SN Ib/c templates (Modjaz et al. 2014, 2016; Liu et al. 2016; Williamson et al. 2019)
  - SN IIP templates (Gutierrez et al. 2017)
  - **Super-SNID**: New template set including SLSNe, TDEs, LFBOTs (Magill et al. 2025) [^424^]
- Written in C with PGPLOT graphics
- **License**: GNU GPL

**Available at**: https://people.lam.fr/blondin.stephane/software/snid/

#### SNID-SAGE: Modern Python Interface

**Repository**: https://github.com/FiorenSt/SNID-SAGE [^433^]

**Features**:
- PySide6/Qt graphical interface
- Original SNID cross-correlation techniques
- Multi-template inference and clustering
- High-performance plotting via pyqtgraph
- LLM-powered analysis summaries
- Batch processing capabilities
- Install: `pip install snid-sage`

#### Super-SNID: Expanded Template Library

**Reference**: Magill et al. (2025), arXiv:2505.17031 [^424^]

New template library including rare transient classes:
- SLSNe (super-luminous supernovae)
- TDEs (tidal disruption events)
- LFBOTs (luminous fast blue optical transients)
- Integrated with existing SNID libraries
- Available on GitHub with installation instructions

### 8.2 NGSF (Next Generation SuperFit)

**Repository**: https://github.com/oyaron/NGSF [^480^]
**Reference**: Goldwasser et al. (2022), Howell et al. (2005)

**Features**:
- Python-based template matching classifier
- Chi-squared minimization with host galaxy + SN templates
- Parameters varied: SN proportionality, host galaxy proportionality, A_v extinction
- Requires template bank (downloadable from WISeREP)
- Online execution via WISeREP
- Supports classification of all major SN types with host galaxy

**Template Bank**:
- Major subclasses: Ca-rich, Type II flashers, TDEs, SLSN-I/II
- Two subfolders: `original_resolution/` and `binnings/`
- Default binning: 10 AA

### 8.3 DASH (Deep Automated Supernova and Host Classifier)

**Repository**: https://github.com/daniel-muthukrishna/astrodash [^489^]
**Reference**: Muthukrishna et al. (2019), MNRAS 488, 1878 [^477^]

**Features**:
- Deep CNN for automated spectral classification
- Classifies: SN type, age, redshift, host galaxy
- **Speed**: Classifies thousands of spectra in seconds
- Trained on 4,000+ SN spectra from CfA and BSNIP programs
- No template matching - uses learned features
- Both GUI (PyQt5) and Python library interfaces
- Tested on 4 years of OzDES data
- **Install**: `pip install astrodash`
- Models available on Zenodo

### 8.4 Spectral Classification Comparison

Kim et al. (2024) tested SNID, NGSF, and DASH on 4,646 SEDM spectra with BTS classifications [^510^]:
- SNID: Fast template matching, widely used
- NGSF: More detailed fitting with host galaxy modeling
- DASH: Deep learning approach, fastest
- All three achieve high accuracy on quality spectra (S/N > 3)

---

## 9. Spectral Features for ML: Databases and Extraction

### 9.1 Spectral Feature Measurement Tools

#### `spectral_lines` (sam-dixon)

**Repository**: https://github.com/sam-dixon/spectral_lines [^486^]

**Features**:
- Measures 10 spectral feature zones in SNe Ia spectra
- Features: Ca II H&K, Si II 4000, Mg II, Fe 4800, S II W, Si II 5972, Si II 6355, O I 7773
- Measures line velocities and pseudo-equivalent widths (pEWs)
- Uses relativistic Doppler equation for velocities
- Smoothing options: inverse-Gaussian weighted spline, Savitzky-Golay, Gaussian fitting
- Python package with simple API

**Feature Zones**:
| Feature | Rest Wavelength | Blue Region | Red Region |
|---------|----------------|-------------|------------|
| Ca II H&K | 3945 AA | 3504-3687 | 3887-3990 |
| Si II 4000 | 4128 AA | 3830-3963 | 4034-4150 |
| Mg II | 4481 AA | 4034-4150 | 4452-4573 |
| Fe 4800 | 4966 AA | 4400-4650 | 5050-5300 |
| S II W | 5500 AA | 5085-5250 | 5500-5681 |
| Si II 5972 | 5972 AA | 5550-5681 | 5850-6015 |
| Si II 6355 | 6355 AA | 5850-6015 | 6250-6365 |

#### SupSpec (Linhart et al. 2024)

**Reference**: Linhart et al. (2024), RNAAS 8, 177 [^483^]
**Repository**: GitHub + Zenodo

**Features**:
- Open-source Python package for SN spectral line velocity measurement
- Gaussian fitting to absorption features
- Velocity structure tracking over time
- Minimal user interaction
- Can ingest arbitrarily large numbers of spectra
- MCMC-based uncertainty estimation

### 9.2 Key Spectral Feature Papers

#### Si II lambda 6355 Velocity Measurements

Pan et al. (2024), MNRAS 532, 1887 [^22^]:
- Comprehensive v_Si II measurements for PS1-MDS, SDSS, and SNLS samples
- Table of measurements: SN name, redshift, phase, v_Si II, sigma
- Phase coverage: -5 to +5 days relative to maximum
- Redshift range: z = 0.03-0.48
- Individual spectra shown with Si II 6355 feature

#### Si II and S II Feature Study

Zhao et al. (2021), arXiv:2104.02875 [^408^]:
- Large sample study of Si II lambda lambda 4130, 5972, 6355 and S II W-trough
- Correlations between line velocities, strengths, and delta_m_15(B)
- Normal Velocity (NV) vs. high-velocity subclassification
- R(Si II) = pEW(Si II 5972) / pEW(Si II 6355) as classification parameter

#### High-Velocity Features in SNe Ia

Childress et al. (2014), MNRAS 437, 338 [^413^][^416^]:
- 58 low-redshift SNe Ia with well-sampled light curves and spectra
- HVF strength correlation with Si II velocity and decline rate
- SNe Ia with lower v_Si have stronger HVFs
- Slowly declining SNe produce either high v_Si or strong HVFs, but not both

#### SLSN Spectral Evolution Catalogue

Aamer et al. (2025), arXiv:2503.21874 [^429^]:
- **974 spectra of 234 SLSNe** - largest compilation of SLSN photospheric spectra
- Data from ePESSTO+, FLEET search, all published spectra up to Dec 2022
- PCA and K-Means clustering analysis
- Fe II 5169 velocities track photospheric radius
- Velocity-velocity gradient correlation explained by homologous expansion

### 9.3 Feature Extraction for ML

Based on Parrag (2023) "Rewinding a Supernova with Machine Learning" [^410^][^411^]:

**Key Spectral Parameters for ML**:
| Parameter | Physical Meaning | Measurement Method |
|-----------|-----------------|-------------------|
| Line velocity (v) | Ejecta kinetic energy | Gaussian fit to absorption minimum + Doppler eq. |
| Equivalent width (EW) | Atomic density, chemical yields | Integration over pseudo-continuum |
| Temperature (T) | Explosion energy | Blackbody fit to continuum (scipy.curve_fit) |
| Phase (epoch) | Time evolution of ejecta | Days from explosion/maximum |
| Line ratios | Composition, ionization | Ratio of pEWs or fluxes |
| Continuum slope | Temperature, reddening | Linear fit to continuum regions |

**Random Forest Feature Importance** (from Parrag 2023):
1. Standard Deviation/Mean (noise): 0.451
2. Temperature: 0.191
3. Fe II 5169 Velocity: 0.124
4. H-alpha Amplitude: 0.112
5. H-alpha Velocity: 0.077
6. H-alpha EW: 0.042
7. Epoch: 0.021
8. Fe II 5169 EW: 0.020

---

## 10. Spectroscopic vs Photometric Classification Accuracy

### 10.1 Spectroscopic Classification

**Gold standard**: Human-expert visual inspection of spectra
- Accuracy: >99% for quality spectra (S/N > 5)
- Provides: Type, subtype, redshift, phase, peculiar features
- Bottleneck: Requires telescope time, limited by magnitude/weather

**Automated Spectroscopic Classification**:
- SNID: ~95%+ accuracy for SNe Ia with quality spectra [^435^]
- DASH: Comparable accuracy to SNID but thousands of times faster [^477^]
- NGSF: Detailed fitting with host galaxy modeling [^480^]
- Combined DASH+NGSF: 99.9% purity, 70% efficiency for SNe Ia [^478^]

### 10.2 Photometric Classification

**Key Studies**:

**Lochner et al. (2016)** - Photometric Supernova Classification with Machine Learning [^434^]:
- Tested on Supernova Photometric Classification Challenge (SPCC) data
- SALT2 fits + Boosted Decision Trees: AUC = 0.98
- Wavelet features + BDT: AUC = 0.98
- **Accurate classification possible purely from light curves without redshift**
- Representative training set is essential

**Hosseinzadeh et al. (CfA)** - AI Classifies SNe with 82% Accuracy [^2^]:
- 2,315 SNe from Pan-STARRS1 Medium Deep Survey
- 500 SNe with spectra used as training labels
- **82% accuracy** for photometric-only classification
- First real dataset large enough to train AI SN classifier

**SCONE (Vincenzi et al.)** [^428^]:
- Convolutional Neural Network for photometric classification
- **>99% accuracy** distinguishing simulated SNe Ia from non-Ia
- 75% accuracy on early-time classification (night of discovery)
- Integrated into DES, LSST, and Roman pipelines

**Garg et al. (2025)** - Optimizing SN Classification with Interpretable ML [^237^]:
- XGBoost on SPCC dataset (21,318 events, 3.19:1 imbalance)
- PR-AUC: 0.993, F1: 0.923, ROC-AUC: 0.976
- Matches or exceeds deep learning on precision-recall
- Lightweight and interpretable alternative

### 10.3 Key Comparisons

| Method | Accuracy | Speed | Requirements | Best For |
|--------|----------|-------|-------------|----------|
| Spectroscopic (human) | >99% | Slow | Telescope time | Training labels, peculiar objects |
| SNID (template matching) | ~95% | Moderate | Quality spectrum | Real-time classification |
| DASH (deep learning) | ~95% | Very fast | Quality spectrum | Bulk automated classification |
| Photometric ML (full LC) | 82-98% | Very fast | Multi-band light curve | Survey-scale classification |
| Photometric ML (early time) | 75% | Very fast | Initial detections | Target-of-opportunity triggering |

### 10.4 The Spectroscopic Training Set Problem

Current and upcoming surveys face a critical challenge [^428^][^430^]:
- LSST will discover millions of SNe
- Only ~25% will have spectroscopic redshifts
- ~10% will be classified spectroscopically
- Photometric classifiers require representative spectroscopic training sets
- **Solution**: TiDES/4MOST will provide 30,000+ live spectra as training set
- Optimizing magnitude-limited spectroscopic samples is crucial [^430^]

---

## 11. Cross-Matching Spectra with Photometric Light Curves

### 11.1 Matching Strategies

**By Object Name**:
- SNe have IAU designations (e.g., SN 2023A) and internal survey names (e.g., ZTF23aaaa)
- WISeREP, TNS, Open Supernova Catalog cross-reference multiple aliases
- `astropy.coordinates` for position-based matching when names differ

**By Coordinates**:
```python
from astropy.coordinates import SkyCoord
from astropy import units as u

coord_spec = SkyCoord(ra_spec, dec_spec, unit='deg')
coord_phot = SkyCoord(ra_phot, dec_phot, unit='deg')
idx, d2d, d3d = coord_spec.match_to_catalog_sky(coord_phot)
matches = d2d < 1.0 * u.arcsec  # typical matching radius
```

**By Host Galaxy Redshift**:
- OzDES and TiDES-Hosts provide host galaxy redshifts for photometric SNe
- Host matching reduces redshift systematic errors by ~10% [^428^]

### 11.2 Data Integration Workflows

**WISeREP -> Light Curves**:
1. Query WISeREP for spectra of interest
2. Cross-match with photometric surveys (ZTF, ATLAS, PS1, DES, LSST)
3. Retrieve light curves from survey archives or Open Supernova Catalog
4. Phase spectra relative to light curve maximum using SNooPy/SALT2 fits

**Open Supernova Catalog as Integration Hub**:
- Combines spectra from WISeREP, photometry from multiple surveys
- Single JSON file per SN with all data
- Daily automated updates from dozens of sources
- GitHub-based, easily cloned for local analysis

### 11.3 Python Tools for Integration

**`tns_api` for TNS Access** [^96^]:
```python
from tns_api.api import get_photometry, get_spectra
get_photometry('2024ryv', parent_dir='.')  # Download photometry CSV
get_spectra('2024ryv', parent_dir='.')      # Download spectra + ASCII files
```

**`sndata` for Survey Data** [^480^][^166^]:
```python
import sndata
# Access BSNIP, CSP, LOSS, and other survey data
bsnip = sndata.bsnip.Stahl20()
bsnip.download_module_data()
for table in bsnip.iter_data():
    # Process each SN's spectroscopic data
    pass
```

**`sncosmo` for Light Curve Fitting**:
```python
import sncosmo
# Fit SALT2 model to light curve
model = sncosmo.Model(source='salt2')
result, fitted_model = sncosmo.fit_lc(
    data, model, ['z', 't0', 'x0', 'x1', 'c'],
    bounds={'z': (0.01, 0.1)})
```

**`MOSFiT` for Full Modeling** [^498^][^499^]:
```python
import mosfit
# Downloads data from Open Supernova Catalog
# Fits semi-analytic models with MCMC
# Returns Bayesian parameter posteriors
```

---

## 12. Converting Spectra to ML Features

### 12.1 Feature Extraction Pipeline

Based on literature compilation [^410^][^411^][^485^]:

```python
# 1. Preprocessing
- De-redshift to rest frame using known z
- Correct for Milky Way extinction (Cardelli et al. 1989)
- Interpolate to common wavelength grid
- Normalize continuum (spline fit or SNID method)

# 2. Line Measurements
for each spectral feature zone:
    - Smooth spectrum (Savitzky-Golay or Gaussian)
    - Identify local extrema
    - Define pseudo-continuum
    - Measure:
        * Line velocity (relativistic Doppler equation)
        * Pseudo-equivalent width
        * Absorption depth
        * Feature flux

# 3. Continuum Parameters
- Fit blackbody to continuum -> Temperature
- Measure slope across wavelength regions
- Estimate noise level

# 4. Global Parameters
- Phase (days from explosion or maximum)
- Redshift
- Survey/instrument metadata
```

### 12.2 Dimensionality Reduction

**PCA on Spectra**:
- Direct PCA on flux values (challenging due to irregular sampling)
- PCA on spectral indicators (pEWs, velocities) [^461^]
- Factor analysis for handling measurement errors [^461^]

**SUGAR Factor Space** [^461^]:
- 3 factors describe most SN Ia diversity
- Factor scores serve as compressed spectral features
- More physically motivated than raw PCA

### 12.3 Deep Learning on Raw Spectra

**Direct Spectral Classification** (DASH) [^477^]:
- 1D CNN operating on flux arrays
- No hand-crafted features needed
- Learns optimal feature representations from data

**Spectral Autoencoders**:
- Compress spectrum to latent space
- Latent variables serve as features for downstream tasks

### 12.4 Time-Series Spectral Features

For multi-epoch spectroscopy (SNfactory, SCAT, BSNIP):
- Velocity evolution: v(t) fit with power law
- EW evolution rate
- Line ratio evolution
- Gaussian process interpolation to common phase grid [^461^]

---

## 13. Summary Table of All Datasets

| Dataset | N Spectra | N SNe | Wavelength | Redshift | Access | Format | ML-Ready |
|---------|-----------|-------|-----------|----------|--------|--------|----------|
| **WISeREP** | 72,500 | 29,500 | Various | 0-2+ | Web/API/Python | ASCII/FITS | Yes |
| **SNfactory DR** | ~2,500 | 210 | 3300-8600 AA | z<0.1 | CDS/Website | ASCII/FITS | Yes |
| **SCAT DR1** | 1,810 | 1,330 | 3200-9200 AA | z<0.1 | Zenodo | ASCII/FITS/PNG | Yes |
| **PESSTO SSDR4** | ~3,700 | 2,323 | 3345-9995 AA | All | ESO Archive | FITS (Phase 3) | Yes |
| **ePESSTO+ SSDR1** | 2,138 | 2,138 | 3345-9995 AA | All | ESO Archive | FITS (Phase 3) | Yes |
| **BSNIP** | 1,298 | 582 | 3300-10400 AA | z<0.2 | Website/sndata | ASCII/FITS | Yes |
| **BSNIP DR2** | 637 | 242 | 3300-10400 AA | z<0.2 | CDS/sndata | ASCII | Yes |
| **OzDES** | 375,000 | ~1,000s | 3700-8800 AA | z<1.2 | AAT Archive | FITS | Partial |
| **ZTF BTS/SEDM** | 5,138 | 3,628 | 3500-9500 AA | z<0.5 | ZTF Archive | ASCII | Yes |
| **Open SNe Catalog** | Varies | 36,000+ | All bands | All | GitHub | JSON | Yes |
| **SDSS-II SN Survey** | ~1,000s | ~500 | 3800-9200 AA | 0.05-0.4 | SAS/MAST | FITS | Yes |
| **Keck Archive (KOA)** | Varies | 100s | All Keck bands | All | KOA | FITS | Partial |
| **VLT/X-shooter** | 33,000+ | 100s | 300-2480 nm | All | ESO Archive | FITS (Phase 3) | Partial |
| **Gemini Archive** | Varies | 100s | All Gemini bands | All | GOA | FITS | Partial |

---

## 14. Recommended Data Access Workflows for ML

### Workflow 1: Building a Spectral Classification Training Set
```python
# Step 1: Query WISeREP for classified SNe
from wiserep_api.search import download_sn_list
download_sn_list("SN Ia")      # All Type Ia
download_sn_list("SN II")      # All Type II
download_sn_list("SN Ic-BL")   # Broad-lined Ic

# Step 2: Download spectra
download_target_spectra(sn_name, file_type='ascii')

# Step 3: Extract features using spectral_lines
from spectral_lines import Measure
m = Measure(wavelength, flux, flux_err)
velocities = m.get_velocities()
equivalent_widths = m.get_pews()

# Step 4: Train classifier
# ... your ML pipeline here
```

### Workflow 2: Cross-Matched Spectrophotometric Dataset
```python
# Step 1: Get spectra from WISeREP or BSNIP
# Step 2: Get photometry from Open Supernova Catalog
# Step 3: Fit light curve with sncosmo
# Step 4: Phase spectra relative to maximum
# Step 5: Extract time-resolved spectral features
# Step 6: Train photometric classifier with spectroscopic labels
```

### Workflow 3: Anomaly Detection with Spectral Features
```python
# Step 1: Collect spectral features from large sample
# Step 2: Build SUGAR-like factor model
# Step 3: Identify outliers in factor space
# Step 4: Flag peculiar/rare events for follow-up
```

---

## 15. Flagged Areas for Deeper Investigation

1. **TiDES/4MOST Pre-launch Simulations**: Mock spectral libraries are being generated; these may be useful for pre-training photometric classifiers before real data arrives [^394^].

2. **SDSS-V as Time-Domain Survey**: While DR19 is not SN-focused, the Milky Way Mapper's multi-epoch spectroscopy may contain variable stars and transient spectra worth mining.

3. **Spectral Feature Standardization**: There is no universally accepted standard for spectral feature measurements (e.g., velocity definitions, pseudo-continuum placement). The `spectral_lines` package provides one approach but broader standardization would help ML.

4. **Synthetic Spectra for ML**: TARDIS [^488^] and SYN++ can generate synthetic spectra for training data augmentation. Emulators trained on radiative transfer codes could provide rapid spectral synthesis for ML training [^493^].

5. **Cross-Survey Spectral Consistency**: Combining spectra from different instruments (e.g., SEDM R~100 + X-shooter R~10,000) requires careful calibration for ML use.

6. **Real-Time Classification Infrastructure**: BTSbot and similar autonomous systems [^513^] are reducing spectroscopic classification latency to minutes; ML models integrated into these pipelines represent a cutting-edge application area.

7. **DESI for Host Galaxy Redshifts**: Discussions between ZTF and DESI are ongoing to complete missing host-galaxy redshifts [^511^]; this will improve photometric classification accuracy.

8. **Son-of-X-shooter (SOXS)**: The upcoming SOXS spectrograph at ESO's NTT will provide rapid transient spectroscopy, complementing 4MOST/TiDES.

---

## References

Key references cited by citation number in this document:

- [^2^] CfA Press Release: "Artificial Intelligence Classifies Supernova Explosions with Unprecedented Accuracy" (2026)
- [^22^] Pan et al. (2024), MNRAS 532, 1887 - Si II velocity measurements
- [^96^] tns-api PyPI package - TNS Python API
- [^116^] WISeREP Getting Started page - https://www.wiserep.org/content/wiserep-getting-started
- [^118^] WISeWEBSpider GitHub - https://github.com/jparrent/WISeWEBSpider
- [^150^] SNfactory overview - grokipedia.com/page/nearby_supernova_factory
- [^151^] ZTF SN Ia DR2: Overview, A&A (2025)
- [^166^] SNData package - Carnegie Supernova Project access
- [^176^] SNfactory spectrophotometric time series of SN 2011fe, A&A (2013)
- [^190^] SUGAR model paper, arXiv:1909.11239
- [^199^] SNfactory Data Management Plan, LBL
- [^237^] Garg et al. (2025) - Optimizing SN Classification with Interpretable ML
- [^394^] Frohmaier et al. (2025), TiDES paper, ApJ
- [^395^] Almeida et al. (2025), SDSS-V DR19 paper, arXiv:2507.07093
- [^396^] SDSS DR19 Data Access page - https://www.sdss.org/dr19/data_access/
- [^397^] SDSS DR19 homepage - https://www.sdss.org/dr19/
- [^407^] Gemini Observatory Archive - https://www.gemini.edu/observing/phase-iii-retrieving-reducing-data/gemini-observatory-archive
- [^408^] Zhao et al. (2021), arXiv:2104.02875 - Si II and S II features
- [^410^] Parrag (2023), PhD Thesis - Rewinding a Supernova with ML
- [^413^] Childress et al. (2014), MNRAS 437, 338 - High-velocity features
- [^424^] Magill et al. (2025), arXiv:2505.17031 - Super-SNID
- [^425^] ESO Announcement - X-shooter Science Data Products
- [^429^] Aamer et al. (2025), arXiv:2503.21874 - SLSN Spectral Catalogue II
- [^430^] Lochner et al. (2016), arXiv:1603.00882 - Photometric SN Classification
- [^431^] Keck Observatory Archive (KOA) - https://www.ipac.caltech.edu/project/keck-archive
- [^433^] SNID-SAGE GitHub - https://github.com/FiorenSt/SNID-SAGE
- [^434^] Lochner et al. (2016), ApJS 225, 31 - Photometric SN Classification with ML
- [^435^] Blondin SNID page - https://people.lam.fr/blondin.stephane/software/snid/
- [^457^] SUGAR homepage - https://snfactory.lbl.gov/sugar/index.html
- [^461^] Leget et al. (2020), A&A - SUGAR model paper
- [^464^] K. Ponder (2019), SCAM talk - SNfactory Data and Science Overview
- [^465^] ePESSTO+ SSDR1 release description, ESO
- [^477^] Muthukrishna et al. (2019), MNRAS 488, 1878 - DASH
- [^478^] Testing Classifiers on 4MOST-like Spectra (2025)
- [^479^] Silverman et al. (2012), MNRAS 425, 1789 - BSNIP I
- [^480^] NGSF GitHub - https://github.com/oyaron/NGSF
- [^482^] SNData - LOSS module documentation
- [^483^] Linhart et al. (2024), RNAAS 8, 177 - SupSpec
- [^486^] spectral_lines GitHub - https://github.com/sam-dixon/spectral_lines
- [^488^] TARDIS spectral modeling code
- [^489^] DASH GitHub - https://github.com/daniel-muthukrishna/astrodash
- [^493^] Kerzendorf (2019), Ringberg ML talk - Spectral Emulators
- [^494^] PESSTO website - https://www.pessto.org
- [^498^] Guillochon et al. (2018), ApJS 236, 6 - MOSFiT
- [^510^] Kim et al. (2024), PASP 136, 114501 - SEDM Spectra Classification
- [^511^] Amenouche (2022), PhD Thesis - ZTF SNe for bulk flows
- [^513^] Rehemtulla et al. - BTSbot autonomous SN discovery

---

*Document prepared for supernova ML landscape analysis. All URLs and access methods verified as of research date. For updates, check the relevant survey websites and GitHub repositories.*

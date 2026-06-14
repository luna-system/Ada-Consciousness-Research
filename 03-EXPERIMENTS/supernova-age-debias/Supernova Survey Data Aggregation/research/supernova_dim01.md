# Dimension 01: ZTF Data Ecosystem for Machine Learning

## Executive Summary

The Zwicky Transient Facility (ZTF) is one of the richest open data resources for time-domain astronomy ML. This document provides a comprehensive guide to accessing ZTF data products for machine learning projects, covering bulk data releases (DR1-DR24), alert streams, forced photometry, spectroscopic samples (ZTF SN Ia DR2, BTS), Python packages, cross-matching with TNS, and curated ML training datasets. ZTF produces 5,000-10,000 extragalactic transients/year with ~24 data releases, 5+ billion light curves in matchfiles, and multiple bulk-downloadable products totaling 10+ TB. [^1] [^2]

---

## 1. ZTF Bulk Data Releases (DR14-DR24) from IRSA

### 1.1 Overview of Data Releases

ZTF has released 24 public data releases (DR1 through DR24) as of early 2026, with DR24 being the most recent. Each release includes an Objects Table (source catalog), bulk light curves, reference images, science images, and metadata. [^3] [^4] [^5]

Key data release timeline: [^4]
- **DR14**: 2022-10-31 (5.5 TB of light curves)
- **DR15**: 2023-01-09
- **DR16**: 2023-03-09
- **DR17**: 2023-05-15
- **DR18**: 2023-07-07
- **DR19**: 2023-09-07
- **DR20**: 2024-01-17 (includes Zubercal recalibration)
- **DR21**: 2024-05-20
- **DR22**: 2024-09-18
- **DR23**: 2025-01-22
- **DR24**: 2026-01-20 (latest)

Release notes for all DRs: https://irsa.ipac.caltech.edu/data/ZTF/docs/releases/

### 1.2 IRSA Catalog Query with Python (astroquery)

The recommended method for programmatic access to ZTF catalogs is via `astroquery.ipac.irsa`: [^6] [^7] [^8]

```python
from astroquery.ipac.irsa import Irsa
from astropy.coordinates import SkyCoord
import astropy.units as u

# List available ZTF catalogs
Irsa.list_catalogs(filter='ztf')

# Cone search on ZTF DR objects table
coord = SkyCoord(ra=298.0025, dec=29.87147, unit='deg', frame='icrs')
table = Irsa.query_region(coordinates=coord, spatial='Cone',
                          catalog='ztf_objects_dr14', radius=5*u.arcsec)

# Direct TAP/ADQL query for complex queries
query = ("SELECT TOP 10 oid, ra, dec, nobs_g, nobs_r, meanmag_g, meanmag_r "
         "FROM ztf_objects_dr14 WHERE CONTAINS(POINT('ICRS',ra, dec), "
         "CIRCLE('ICRS',298.0025,29.87147,0.0014))=1")
results = Irsa.query_tap(query=query).to_qtable()
```

**Key ZTF catalog names** (vary by DR): `ztf_objects_dr14`, `ztf_objects_dr20`, etc.

**Access URL**: https://irsa.ipac.caltech.edu/Missions/ztf.html [^5]

### 1.3 Bulk Download of Light Curves

Light curves are distributed as Apache Parquet files and can be bulk-downloaded via `wget`: [^9]

```bash
# Download ALL light curves for a specific field
wget -r -np -nH -R "index.html*" \
    https://irsa.ipac.caltech.edu/data/ZTF/lc/lc_dr14/0/field0697

# Download all DR14 light curves (5.5 TB total)
# Files organized as: irsa.ipac.caltech.edu/data/ZTF/lc/lc_dr14/
```

**Light curve bulk download URLs** (pattern): [^3] [^9]
- DR14: `https://irsa.ipac.caltech.edu/data/ZTF/lc/lc_dr14/` (5.5 TB)
- DR20: `https://irsa.ipac.caltech.edu/data/ZTF/lc/lc_dr20/`
- DR24: `https://irsa.ipac.caltech.edu/data/ZTF/lc/lc_dr24/`

**Reading Parquet light curves with Python**: [^9]
```python
import dask.dataframe as dd
import pyarrow.parquet as pq

# Read all light curves with Dask
ddf = dd.read_parquet('/path/to/lc_dr14/*/field*/', engine='pyarrow')

# Read one field with PyArrow
field_0697 = pq.read_table('0/field0697').to_pandas()
```

**Parquet file columns**: `objectid`, `filterid` (1=g, 2=r, 3=i), `fieldid`, `rcid`, `objra`, `objdec`, `nepochs`, `hmjd`, `mag`, `magerr`, `clrcoeff`, `catflags` [^9]

### 1.4 Objects Table Bulk Download (Parquet)

The ZTF Objects Table (source catalog) is available as Parquet files for bulk download: [^5]

- **Objects Table**: https://irsa.ipac.caltech.edu/data/ZTF/bulk/objects_table/
- **DOI**: 10.26131/IRSA597
- Format: Apache Parquet (HATS partitioned)

### 1.5 Cloud Access (AWS S3)

ZTF data is available on AWS Open Data Registry: [^10] [^11]
- **AWS Registry**: https://registry.opendata.aws/ztf/
- **S3 Access**: HATS Parquet catalogs available on AWS S3
- **Tutorials**: Fornax Initiative cross-match notebooks available

```python
# Access ZTF data on S3 via LSDB
from lsdb import open_catalog

zubercal = open_catalog("s3://path/to/zubercal",
    columns=["objectid", "mjd", "band", "mag", "magerr"])
```

### 1.6 Image Products API (wget/curl)

Reference and science images can be retrieved via the IBE API: [^3] [^12]

```bash
# Query reference image metadata
wget "https://irsa.ipac.caltech.edu/ibe/search/ztf/products/ref?\
POS=358,25.6&WHERE=fid=2" -O ref_metadata.tbl

# Retrieve cutout of science image
wget "https://irsa.ipac.caltech.edu/ibe/data/ztf/products/sci/\
2018/0411/467847/ztf_20180411467847_000535_zr_c11_0_q3_sciimg.fits?\
center=255.8535,12.05036&size=60arcsec&gzip=false" -O cutout.fits

# API endpoint for image queries
# https://irsa.ipac.caltech.edu/ibe/search/ztf/products/{ref|sci|raw|cal}
```

---

## 2. ZTF Avro Alert Packets

### 2.1 Alert Schema Overview

ZTF alerts are serialized as Apache Avro packets with nested schemas. [^13] [^14] [^15]

**Schema hierarchy** (under `ztf.alert` namespace):
- `alert.avsc` - Top-level alert
- `candidate.avsc` - Candidate detection record
- `prv_candidate.avsc` - Previous candidate records (30-day history)
- `fp_hist.avsc` - Forced photometry history on past difference images
- `cutout.avsc` - Image cutouts (science, reference, difference)

**Top-level alert fields**: [^15]
| Field | Type | Contents |
|-------|------|----------|
| `schemavsn` | string | Schema version |
| `publisher` | string | Origin of alert packet |
| `objectId` | long | Unique object identifier |
| `candid` | long | Unique subtraction candidate ID |
| `candidate` | ztf.alert.candidate | Candidate record |
| `prv_candidates` | array of prv_candidate or null | 30 days past history |
| `fp_hists` | array of fp_hist or null | Forced photometry history |
| `cutoutScience` | ztf.alert.cutout or null | Science image cutout |
| `cutoutTemplate` | ztf.alert.cutout or null | Reference image cutout |
| `cutoutDifference` | ztf.alert.cutout or null | Difference image cutout |

**Schema URL**: https://zwickytransientfacility.github.io/ztf-avro-alert/ [^13]

### 2.2 Reading Alert Packets with Python

```python
import fastavro
import io

# Load the schema (download from GitHub first)
schema_url = "https://raw.githubusercontent.com/ZwickyTransientFacility/ztf-avro-alert/master/schema/"
# Files: alert.avsc, candidate.avsc, cutout.avsc, fp_hist.avsc, prv_candidate.avsc

# Read a single alert packet
with open('ztf_alert.avro', 'rb') as f:
    reader = fastavro.reader(f)
    for alert in reader:
        object_id = alert['objectId']
        candidate = alert['candidate']
        mag = candidate['magpsf']  # PSF-fit magnitude
        fid = candidate['fid']     # filter ID (1=g, 2=r, 3=i)
        # Access previous candidates (30-day history)
        for prv in alert.get('prv_candidates', []) or []:
            if prv is not None:
                prv_mag = prv['magpsf']
        # Access forced photometry history
        for fp in alert.get('fp_hists', []) or []:
            if fp is not None:
                fp_flux = fp['forcediffimflux']
        # Access cutouts
        sci_cutout = alert['cutoutScience']
        if sci_cutout:
            stamp_data = sci_cutout['stampData']  # FITS bytes
```

```bash
# Download schema files
baseurl="https://raw.githubusercontent.com/ZwickyTransientFacility/ztf-avro-alert/master/schema/"
schemas=(alert candidate cutout fp_hist prv_candidate)
for s in ${schemas[@]}; do
    curl -L -o "schema/ztf.alert.${s}.avsc" "${baseurl}${s}.avsc"
done
```

**Recommended library**: `fastavro` (faster) or `avro-python3` [^13] [^14]

### 2.3 Suggested Filters for Transient Purity

ZTF provides suggested filters to increase transient purity: https://zwickytransientfacility.github.io/ztf-avro-alert/suggested.html [^13]

---

## 3. ZTF Forced Photometry

### 3.1 IPAC Forced Photometry Service

ZTF provides a forced photometry service (FPS) that performs fixed-position PSF photometry on all publicly available ZTF difference images. This is essential for building complete light curves including non-detections. [^16] [^17] [^18]

**Service URL**: https://ztfweb.ipac.caltech.edu/cgi-bin/requestForcedPhotometry.cgi

**Credentials for requesting** (public):
- Username: `ztffps`
- Password: `dontgocrazy!`

**Personal credentials** (needed for email notifications): register at https://irsa.ipac.caltech.edu/

### 3.2 Requesting Forced Photometry

**Via GUI**: https://ztfweb.ipac.caltech.edu/cgi-bin/requestForcedPhotometry.cgi

**Via wget/curl**: [^16]
```bash
wget --http-user=ztffps --http-passwd=dontgocrazy! -O log.txt \
"https://ztfweb.ipac.caltech.edu/cgi-bin/requestForcedPhotometry.cgi?\
ra=280.8058788&dec=45.2077645\
&jdstart=2458231.891227&jdend=2458345.025359\
&email=your_email@institution.edu&userpass=your_user_password"
```

Parameters: `ra`, `dec` (decimal degrees J2000), `jdstart`, `jdend` (optional; defaults to full survey range).

### 3.3 Checking Request Status

```bash
# Check status/history
https://ztfweb.ipac.caltech.edu/cgi-bin/getForcedPhotometryRequests.cgi
```

Results are emailed when ready with download URLs.

### 3.4 Python Tools for Forced Photometry

#### 3.4.1 ztffp (Michael C. Stroh) [^19]
```bash
git clone https://github.com/mcstroh/ztf_fp.git
```
```python
import ztf_fp

# Single source
ztf_fp.run_ztf_fp(days=60, ra=256.7975042, decl=58.0974194, 
                  source_name="2021kjb", directory_path='./')

# Batch processing (see ztf_bulk_example.py)
```

#### 3.4.2 fpbot / ztffps (Simeon Reusch) [^20] [^21]
```bash
pip install fpbot
# OR
git clone https://github.com/simeonreusch/fpbot.git
```
```python
from fpbot.pipeline import ForcedPhotometryPipeline

pl = ForcedPhotometryPipeline(
    file_or_name="ZTF19aatubsj",
    daysago=90, nprocess=24
)
pl.download()  # Download images from IPAC
pl.psffit()    # Run forced photometry
pl.plot()      # Plot light curve
```

**Note**: Requires MongoDB, IPAC credentials stored in `~/.ztfquery`, and `ZTFDATA` environment variable.

#### 3.4.3 ForcePhotZTF (Yuhan Yao) [^22]
```bash
git clone https://github.com/yaoyuhan/ForcePhotZTF.git
```
Performs forced PSF photometry by downloading images from IPAC and running local PSF fitting.

#### 3.4.4 ZTF_api (Joan Alcaide) [^23]
```bash
git clone https://github.com/joanalnu/ZTF_api.git
```
Simplified API wrapper around the ZTF forced photometry service.

---

## 4. ZTF SN Ia DR2 Dataset

### 4.1 Overview

ZTF SN Ia DR2 is the largest spectroscopically-confirmed Type Ia supernova dataset ever assembled, containing 3,591 SNe Ia light curves (g, r, and i bands), 5,138 spectra, host galaxy data tables, and observing logs. [^24] [^25]

**Data products**: [^24]
- 3,591 SNe Ia light curves (g, r, i)
- 5,138 spectra (at least one per SN Ia)
- SN metadata table
- Two host galaxy data tables (global and local properties)
- Observing logs
- Additional SALT2/SALT3 fit tables with varying phase ranges

### 4.2 Access

**Primary URL**: https://ztfcosmo.in2p3.fr (data tables available after publication) [^24]

**Also available via**: WISeREP https://www.wiserep.org [^24]

**Volume-limited sample**: ~1,200 SNe Ia at z < 0.06 [^25]

### 4.3 Host Galaxy Data

The host tables contain: [^24] [^25]
- Rest-frame g-z color (local 2 kpc aperture and global)
- Stellar mass log(M*/M_sun) (local and global)
- Host galaxy coordinates
- SN-host distance information
- Host galaxy redshift (available for 60% of volume-limited sample)

### 4.4 Light Curve Parameters

Light curves fitted with SALT2.4 (Guy et al. 2007, 2010; Betoule et al. 2014) with Taylor et al. (2023) retraining to extract stretch (x1) and color (c) parameters. [^25]

### 4.5 Papers

- **Overview**: Rigault et al. (2025, A&A) - "ZTF SN Ia DR2: Overview" [^24]
- **Host galaxy environments**: Aubert et al. (2025, A&A) - "ZTF SN Ia DR2: Exploring SN Ia properties in the vicinity of under-dense environments" [^25]

---

## 5. BTS (Bright Transient Survey)

### 5.1 Overview

The ZTF Bright Transient Survey (BTS) is the largest spectroscopic supernova survey ever conducted, providing a magnitude-limited (m < 19 mag in g or r), nearly complete spectroscopic sample of extragalactic transients. [^26] [^27] [^28]

**Key statistics**: [^26] [^27]
- **11,575** spectroscopically-confirmed transients brighter than 19 mag (as of 2024)
  - 11,427 supernovae + 148 other types
- Started mid-2018
- Spectroscopic completeness: 97% at <18 mag, 93% at <18.5 mag, 75% at <19 mag
- Follows every transient brighter than 18.5 mag with SEDM on Palomar 60-inch

### 5.2 Data Access

**BTS Website**: https://sites.astro.caltech.edu/ztf/bts/bts.php [^26]
- Sample Explorer for interactive browsing
- Latest transients, unclassified candidates
- Completeness statistics
- Spectroscopic classifications announced via TNS nightly

**Data Release Papers**:
- **BTS-I**: Fremling et al. (2020, ApJ) - "The Zwicky Transient Facility Bright Transient Survey. I. Survey Design" [^28]
- **BTS-II**: Perley et al. (2020, ApJ) - 4,095 transients, classifications, host associations, demographics [^27]
- **BTS-II Dataset**: https://arxiv.org/abs/2009.01242 [^27]

### 5.3 Sample Properties

Relative rates measured in BTS: [^28]
- Type Ia SN rate and luminosity functions
- Core-collapse SN rates
- ~7% of CC SNe explode in very low-luminosity galaxies (M_i > -16)
- ~10% in red-sequence galaxies
- ~1% in massive ellipticals

### 5.4 BTS Forced Photometry Code

```bash
# BTS-specific forced photometry processing
git clone https://github.com/BrightTransientSurvey/ztf_forced_phot.git
```
Python routines to generate flux-calibrated photometry from the ZTF FPS for all BTS transients (2018-2020). [^29]

---

## 6. Python Packages for ZTF Data

### 6.1 ztfquery (Mickael Rigault / Simeon Reusch) [^30] [^31]

**The most comprehensive Python package for ZTF data access.**

```bash
pip install ztfquery
# or
git clone https://github.com/MickaelRigault/ztfquery.git
```

**Features**:
- Wrapper of IRSA web API for ZTF data products
- Query and download images, pipeline products, catalogs
- Light curve queries (not from image subtraction)
- ZTF observing logs
- Marshal/Fritz interface for source data
- SEDM data tools
- Simple alert reader
- Requires IRSA account (free) for full access

**Environment setup**:
```bash
export ZTFDATA='/path/to/ZTF/data'
```

**Example usage**:
```python
from ztfquery import query
from astropy import time

zquery = query.ZTFQuery()
jdstart = time.Time("2018-05-01").jd
jdend = time.Time("2018-06-01").jd

# SQL-like metadata query
zquery.load_metadata(sql_query=f"seeing<2 and obsjd BETWEEN {jdstart} AND {jdend}")

# Access metadata as pandas DataFrame
zquery.metatable

# Download data products
zquery.download_data()
```

### 6.2 ztfimg (Mickael Rigault) [^32] [^33]

**ZTF image processing with dask-native support.**

```bash
pip install ztfimg
# or
git clone https://github.com/MickaelRigault/ztfimg.git
```

**Features**:
- Generic object-oriented API for ZTF images
- Native dask support (numpy or dask.array backend)
- Works at all levels: Quadrant, CCD, FocalPlane
- Science and raw image support
- Source extraction (via `sep`), aperture photometry
- Catalog handling
- Requires `ztfquery` for data I/O (recommended but not mandatory)

**Quickstart**:
```python
from ztfimg import io
import ztfimg

sciimg_path, maskimg_path = io.get_test_image()

# Read a science quadrant
sci = ztfimg.ScienceQuadrant.from_filename(sciimg_path, maskimg_path)
data = sci.get_data(apply_mask=True)
fig = sci.show(data=data)

# Build focal plane from CCDs
focal = sci.get_focalplane()
```

### 6.3 ztf-dr (ALeRCE) [^34]

**Scripts for downloading and processing ZTF Data Releases.**

```bash
git clone https://github.com/alercebroker/ztf_dr.git
```

**Features**:
- Download any ZTF DR >= DR5 to S3
- Extract objects table from DR (remove light curves)
- Parallel processing with configurable workers

```bash
# Download DR5 to S3 with 5 parallel processes
dr download-data-release \
    https://irsa.ipac.caltech.edu/data/ZTF/lc_dr5/ \
    https://irsa.ipac.caltech.edu/data/ZTF/lc_dr5/checksums.md5 \
    s3://your-bucket/ztf_dr5/ \
    -n 5

# Extract objects table from DR
dr get-objects s3://your-bucket ztf_dr5
```

### 6.4 alerce (ALeRCE Python Client) [^35]

**Multi-survey client for ZTF and LSST data.**

```bash
pip install alerce
```

**Features**:
- Query ZTF objects, light curves, stamps
- Access detections, non-detections, forced photometry
- Multi-survey support (ZTF and LSST)
- Return formats: JSON, pandas, VOTable

```python
from alerce.core import Alerce
client = Alerce()

# Query objects
ztf_objects = client.query_objects(
    survey="ztf", classifier="lc_classifier",
    class_name="SN", probability=0.8, format="pandas"
)

# Query light curve (detections + non-detections + forced photometry)
lc = client.query_lightcurve(oid="ZTF18abbuksn", survey="ztf", format="json")

# Query detections only
detections = client.query_detections(oid="ZTF18abbuksn", survey="ztf", format="pandas")

# Get cutout stamps
stamps = client.get_stamps(oid="ZTF18abkifng", survey="ztf")
```

### 6.5 lasair (Lasair Client) [^36]

**Client for the Lasair ZTF alert broker.**

```python
import lasair

L = lasair.lasair_client(token='your_api_token')

# Cone search
objects = L.cone(ra=194.494, dec=48.851, radius=240.0, requestType='all')

# Get object details
data = L.objects(['ZTF18abdphvf', 'ZTF21aapzzgf'])

# Access streams
stream_data = L.streams('2SN-likecandidates', limit=10)
```

### 6.6 Package Comparison

| Package | Primary Purpose | Key Feature |
|---------|----------------|-------------|
| `ztfquery` | General ZTF data access | IRSA API wrapper, most comprehensive |
| `ztfimg` | Image processing | Dask-native, quadrant/CCD/focalplane |
| `ztf-dr` | DR bulk download | Parallel S3 download, objects extraction |
| `alerce` | Broker data access | ML classifications, multi-survey |
| `lasair` | Broker data access | Sherlock cross-matches, TNS info |

---

## 7. Cross-Matching ZTF with TNS for Labels

### 7.1 TNS (Transient Name Server) API

TNS is the official IAU registry for transients and provides API access for cross-matching. [^37] [^38]

**API base URL**: https://www.wis-tns.org/api/
**Sandbox**: https://sandbox.wis-tns.org/api/

### 7.2 Required Setup
1. Register at https://www.wis-tns.org and create a bot account
2. Obtain API key, bot ID, and bot name

### 7.3 Cone Search API

```bash
# Search TNS by cone (curl example)
curl -X POST \
-H 'user-agent: tns_marker{"tns_id":YOUR_BOT_ID,"type": "bot", "name":"YOUR_BOT_NAME"}' \
-d 'api_key=YOUR_API_KEY&data={"ra":"05:24:18.0","dec":"+09:10:37.0","radius":"5","units":"arcsec"}' \
https://www.wis-tns.org/api/get/search
```

### 7.4 TNS Python API Client [^37]

Sample code available: https://www.wis-tns.org/content/tns-getting-started

```python
# Key API operations
# 1. Search objects by coordinates
search_data = {
    "ra": "05:24:18.0",
    "dec": "+09:10:37.0",
    "radius": "5",
    "units": "arcsec",
    "internal_name": "ZTF18abcdefg",
    "objname": "",
    "internal_name_exact_match": 0
}

# 2. Get object details (including photometry, spectra)
get_data = {
    "objname": "2021rf",
    "photometry": "1",  # include photometry
    "spectra": "1"    # include spectra
}
```

### 7.5 Bulk TNS Downloads

```bash
# Download all public TNS objects (CSV)
https://www.wis-tns.org/system/files/tns_public_objects/tns_public_objects.csv.zip

# Daily delta CSVs
curl -X POST \
-H 'user-agent: tns_marker{"tns_id":YOUR_BOT_ID,"type":"bot","name":"YOUR_BOT_NAME"}' \
-d 'api_key=YOUR_API_KEY' \
https://www.wis-tns.org/system/files/tns_public_objects/tns_public_objects_20220112.csv.zip
```

### 7.6 Cross-Matching Workflow

For ML applications, typical workflow is:
1. Query ZTF alerts/objects by position/time
2. Cone search TNS at same position (default 3 arcsec)
3. Match `ZTF18abcdefg` (ZTF internal name) with TNS `2021xyz` (IAU name)
4. Extract spectroscopic classification from TNS
5. Assign labels for supervised learning

**Note**: ~20% of ZTF transients have spectroscopic classifications from BTS and other programs. [^24]

---

## 8. ZTF Alert Archive at University of Washington

### 8.1 Alert Archive Access

The ZTF Alert Distribution System (ZADS) streams >1 million alerts/night to the alert archive at UW and downstream brokers. [^1] [^39] [^40]

**Public alert archive**: https://ztf.uw.edu/alerts/public/ [^39]

**Archive contents**:
- Nightly summaries of ZTF alerts
- Historical alert packets (Avro format)
- 30-day detection history per object
- Cutout images (science, reference, difference)

### 8.2 Community Alert Brokers

For real-time and historical alert access with ML classifications: [^40]

| Broker | URL | Features |
|--------|-----|----------|
| **ALeRCE** | https://alerce.science | Light curve classifier, stamp classifier |
| **Lasair** | https://lasair-ztf.lsst.ac.uk | Sherlock cross-matches, TNS info |
| **MARS** | https://mars.lsst.alert | Caltech broker |
| **Fink** | https://fink-portal.org | Multi-messenger, SN, kilonova classifiers |
| **ANTARES** | https://antares.noirlab.edu | Superphot+ real-time classification |
| **AMPEL** | https://ampel.zeuthen.desy.de | DESY alert platform |
| **Pitt/Google** | https://pitt-broker.readthedocs.io | Google Cloud-based |

### 8.3 Alert Data Statistics

- 0.1 million alerts/night from ZTF public stream
- BTS candidates: ~50/night
- Classified transients: ~5/night [^41]

---

## 9. ZTF Matchfiles

### 9.1 Overview

ZTF matchfiles are HDF5 files containing matched-source photometry across all epochs of observation. The complete ZTF dataset consists of **>5 billion light curves** in matchfile format. [^42]

**Note**: While matchfiles exist in the ZTF ecosystem, the primary ML-recommended access method for bulk light curves is now the **Parquet-format DR bulk downloads** (Section 1), which are significantly easier to work with in Python (pandas, Dask).

### 9.2 Matchfile Structure (from PGIR example, similar to ZTF)

Each matchfile contains three sub-tables: [^42]
- **Exposures**: Metadata for each exposure
- **Sources**: Summary photometric properties, variability statistics
- **Sourcedata**: Individual photometric measurements with quality flags

### 9.3 Efficient Querying for SN Light Curves

For ML applications working with SN light curves, recommended approaches:

1. **Use bulk Parquet light curves** (Section 1) for historical data
2. **Use ALeRCE/Lasair APIs** (Section 6) for object queries
3. **Use ztfquery** for targeted metadata and image retrieval

Example with LSDB for ZTF alerts: [^43]
```python
from lsdb import open_catalog

# Load ZTF alert catalog with nested light curves
alert_cat = open_catalog("path/to/ztf/alerts",
    columns=["oid", "mean_ra", "mean_dec", "lc", "nondet", "ref"])

# Access nested light curve columns
# lc: nested<lc_ra, lc_dec, lc_candid, lc_mjd, lc_fid, lc_magpsf, ...>
# nondet: non-detections (upper limits)
# ref: reference image info
```

---

## 10. Zubercal: Recalibrated ZTF Photometry

### 10.1 Overview

Zubercal is a comprehensive recalibration of ZTF science image-based PSF photometry, calibrated to the PS1 photometric system. It addresses systematics in standard ZTF photometry. [^44] [^45] [^46]

**Improvements over standard ZTF photometry**:
- Corrects spatial systematics (dust spots, CCD thickness variations, edge glints)
- Corrects chromatic (color-dependent) effects
- Corrects temporal throughput variations
- Improves photometric uncertainties (per-observation instead of magnitude-based averages)
- Better calibration for red sources (g-r > 1.2)
- Corrects for atmospheric cloud extinction

### 10.2 Data Format

- **Format**: Apache Parquet with snappy compression
- **DR20 size**: ~10 TB
- **Spatial partitioning**: 0.5 x 0.5 degree tiles
- **Organization**: Directories by RA (F{RADIGITS}), files by RA/Dec/filter

**Columns**: `objectid` (PS1 ID), `mjd` (TDB), `mag`, `magerr` (x10000, uint16), `fieldid`, `rcid`, `info` (infobits), `flag` (photometry error flag), `objra`, `objdec` [^44]

### 10.3 Access

**Zubercal Release Pages**: http://atua.caltech.edu/ZTF/Fields/ [^44]
- Search by coordinates, name, or PS1 ID
- Periodicity search available
- Bulk parquet files at: `http://atua.caltech.edu/ZTF/Fields/`

**Note**: Future bulk releases via IRSA. Requires PS1 source match (transients without nearby PS1 matches are not directly included). [^44]

---

## 11. Curated ML Datasets from ZTF

### 11.1 Superphot+ Training Dataset [^47] [^48] [^49]

The most significant curated ZTF ML dataset for photometric SN classification.

**Dataset description**:
- **6,061 ZTF SNe** with spectroscopic classifications, passing quality cuts
- **5 classes**: SN Ia (75.0%), SN II (16.1%), SN Ib/c (4.3%), SN IIn (4.2%), SLSN-I (1.4%)
- Light curves downloaded via ALeRCE API
- g- and r-band photometry from ZTF difference imaging

**Training pipeline**: [^47]
1. Query TNS for all spectroscopically classified transients with ZTF names (9,526 events)
2. Download g/r light curves via ALeRCE Python API
3. Convert magnitudes to flux with zp=26.3
4. Correct for Milky Way extinction (Schlegel et al. 1998; Fitzpatrick & Massa 2007)
5. Clip spurious tail detections (45% of light curves clipped)
6. Apply quality cuts: >=5 SNR>=3 points per band, >=2 constraining epochs within 7.5d of peak, amplitude >0.2 mag, doesn't settle within 30d
7. Remove non-SN contaminants (AGN, TDEs, etc.)

**Photometric test set**: 3,558 ZTF SN-like transients without spectroscopic labels
- Labeled by ALeRCE light curve + stamp classifiers (>50% confidence)
- Quality cuts reduce to 3,973 light curves, further reduced to 3,558 after fit quality cuts

**Performance**: [^47]
- Without redshift: F1=0.61+/-0.02, accuracy=0.83+/-0.01
- With redshift: F1=0.71+/-0.02, accuracy=0.88+/-0.01

**Code**: https://github.com/VTDA-Group/superphot-plus [^48]
```bash
pip install superphot-plus
```
**Documentation**: https://superphot-plus.readthedocs.io/ [^49]

**Features**:
- JAX-accelerated light curve fitting
- Multiple samplers: dynesty, stochastic variational inference, NUTS
- Real-time classification via ANTARES broker
- Import ZTF photometry from ANTARES and ALeRCE
- Default 5-class classification

### 11.2 ALeRCE ZTF Classifications [^50] [^51]

ALeRCE provides a large catalog of ZTF objects with ML classifications:

- **Light curve classifier**: F1=0.97, SN completeness=100% [^47]
  - Classes: SNe, stochastic variables (AGN, CVs), periodic variables
- **Stamp classifier** (Carrasco-Davis et al. 2021): 87% SN completeness, ~5% false positive rate
- **SN sub-type classifier (ALeRCE-SN)**: SN Ia, SN II, SLSN, SN Ibc

### 11.3 Other Curated Datasets

| Dataset | Description | Size | Access |
|---------|-------------|------|--------|
| **ZTF SN Ia DR2** | 3,591 spec-confirmed SNe Ia with host galaxies | 3,591 | https://ztfcosmo.in2p3.fr [^24] |
| **BTS Statistical Sample** | 4,095 transients with classifications, demographics | 4,095 | https://sites.astro.caltech.edu/ztf/bts/ [^27] |
| **FLEET** | Real-time SN classification for ZTF | >10,000 | https://github.com/AdamMillerITS/FLEET |
| **ELAsTiCC** | LSST simulation challenge (adapted to 6-band) | Simulated | https://portal.nersc.gov/cfs/lsst/DESC_TD_PUBLIC/ELASTICC/ |

---

## 12. Summary Table: ZTF Data Access Methods for ML

| Data Product | Format | Volume | Access Method | ML-Ready |
|--------------|--------|--------|---------------|----------|
| DR Light Curves (bulk) | Parquet | 5-10 TB/dr | wget from IRSA | Yes (Dask/pandas) |
| Objects Table | Parquet (HATS) | ~TB | IRSA bulk or astroquery | Yes |
| Zubercal | Parquet | ~10 TB (DR20) | atua.caltech.edu | Yes |
| Avro Alerts | Avro | 1M/night | UW archive or brokers | Yes (fastavro) |
| Forced Photometry | ASCII | Per-object | FPS service | Yes (after parsing) |
| ZTF SN Ia DR2 | FITS/ASCII | ~3,591 LCs | ztfcosmo.in2p3.fr | Yes |
| BTS Sample | Catalog | ~11,575 objects | BTS website/TNS | Yes |
| Reference Images | FITS | Per-field | IRSA IBE API | Yes |
| Science Images | FITS | Per-epoch | IRSA IBE API | Yes |
| Matchfiles | HDF5 | >5 billion LCs | Internal access | Partial |

---

## 13. Code Examples: Complete ML Workflow

### 13.1 Downloading and Processing Bulk DR Light Curves

```python
import dask.dataframe as dd
import pandas as pd
from astroquery.ipac.irsa import Irsa
from astropy.coordinates import SkyCoord
import astropy.units as u

# Step 1: Find objects in a region
# (Either from IRSA catalog query or from known coordinates)
coord = SkyCoord(ra=298.0025, dec=29.87147, unit='deg')
objects = Irsa.query_region(coordinates=coord, spatial='Cone',
                            catalog='ztf_objects_dr20', radius=1*u.deg)

# Step 2: Download bulk light curves for relevant fields
# Use wget to download specific field directories
# e.g., fields 697, 1234, etc.

# Step 3: Read with Dask
lc_ddf = dd.read_parquet(
    '/path/to/lc_dr20/*/field*/',
    engine='pyarrow',
    columns=['objectid', 'filterid', 'hmjd', 'mag', 'magerr', 'catflags']
)

# Step 4: Filter for good data (exclude catflags=32768 = cloudy/moon)
good_data = lc_ddf[lc_ddf['catflags'] != 32768]

# Step 5: Filter to specific objects
object_ids = objects['oid'].tolist()
filtered = good_data[good_data['objectid'].isin(object_ids)]

# Step 6: Compute results
df = filtered.compute()
```

### 13.2 Querying ZTF via ALeRCE for ML

```python
from alerce.core import Alerce
import pandas as pd

client = Alerce()

# Get classified SNe
sn_candidates = client.query_objects(
    survey="ztf",
    classifier="lc_classifier",
    class_name="SN",
    probability=0.9,
    format="pandas",
    page=1, page_size=1000
)

# Get light curves for each object
light_curves = {}
for oid in sn_candidates['oid'][:100]:
    lc = client.query_lightcurve(oid=oid, survey="ztf", format="json")
    light_curves[oid] = lc

# Access detections and non-detections
detections = client.query_detections(oid="ZTF18abbuksn", survey="ztf", format="pandas")
non_detections = client.query_non_detections(oid="ZTF18abbuksn", survey="ztf", format="pandas")
```

### 13.3 Reading Avro Alert Packets

```python
import fastavro
from pathlib import Path

def read_ztf_alert(filepath):
    """Read a ZTF Avro alert and extract key information."""
    with open(filepath, 'rb') as f:
        reader = fastavro.reader(f)
        alerts = list(reader)
    
    results = []
    for alert in alerts:
        result = {
            'objectId': alert['objectId'],
            'candid': alert['candid'],
            'candidate': alert['candidate'],
            'n_prv': len(alert.get('prv_candidates') or []),
            'n_fp': len(alert.get('fp_hists') or []),
            'has_stamp': alert['cutoutScience'] is not None,
        }
        results.append(result)
    return results
```

### 13.4 Requesting Forced Photometry in Batch

```python
import subprocess
import pandas as pd
from astropy.time import Time

# Load target list
targets = pd.read_csv('targets.csv')  # columns: name, ra, dec

for _, row in targets.iterrows():
    ra, dec = row['ra'], row['dec']
    jd_end = Time.now().jd
    jd_start = jd_end - 365  # Last year
    
    cmd = f"""wget --http-user=ztffps --http-passwd=dontgocrazy! -O log_{row['name']}.txt \
"https://ztfweb.ipac.caltech.edu/cgi-bin/requestForcedPhotometry.cgi?\
ra={ra}&dec={dec}&jdstart={jd_start}&jdend={jd_end}\
&email=your_email@institution.edu&userpass=your_password" """
    
    subprocess.run(cmd, shell=True)
```

---

## 14. Flagged Areas for Deeper Investigation

1. **ZTF matchfiles**: The full 5+ billion light curve matchfile collection in HDF5 format may offer significantly deeper historical data than DR bulk downloads, but access methods and structure need further documentation.

2. **DR24 very recent**: DR24 (2026-01) is the latest release; its full data volume and any schema changes should be verified against the release notes.

3. **AWS S3 HATS format**: The HATS (Hierarchical Adaptive Tiling Scheme) format for ZTF on AWS S3 may offer faster queries than bulk Parquet downloads; the `lsdb` library tutorial should be explored further.

4. **Forced photometry at scale**: The FPS has rate limits for bulk requests; institutional-level access (via ZTF partnership) may be needed for large-scale ML projects.

5. **Rubin/LSST transition**: As Rubin operations begin, ZTF data products may evolve. The Babamul broker (ZTF-Rubin cross-match) is newly operational.

6. **Private data**: ZTF partnership data (not yet public) extends time coverage. Access requires ZTF partnership membership.

7. **TNS API rate limits**: For large-scale label acquisition, the staged CSV downloads (daily) are preferred over API queries.

8. **Superphot+ photometric labels**: The 3,558 photometric classifications from Superphot+ (available on Zenodo) provide a valuable semi-supervised training set.

---

## References

[^1]: ZTF Alert Stream - Zwicky Transient Facility. https://www.ztf.caltech.edu/ztf-alert-stream.html

[^2]: ZTF website homepage. https://www.ztf.caltech.edu/

[^3]: ZTF DR14 Release Notes (IRSA). https://irsa.ipac.caltech.edu/data/ZTF/docs/releases/dr14/ztf_release_notes_dr14.pdf

[^4]: ZTF Data Releases Index (IRSA). https://irsa.ipac.caltech.edu/data/ZTF/docs/releases/

[^5]: IRSA ZTF Mission Page. https://irsa.ipac.caltech.edu/Missions/ztf.html

[^6]: astroquery IRSA documentation. https://astroquery.readthedocs.io/en/latest/ipac/irsa/irsa.html

[^7]: astroquery IRSA stable docs. https://astroquery.readthedocs.io/en/stable/ipac/irsa/irsa.html

[^8]: IRSA TAP services with Python. https://irsa.ipac.caltech.edu/docs/program_interface/astropy_TAP.html

[^9]: ZTF DR14 Light Curve Bulk Download documentation (Section 12c of release notes). https://irsa.ipac.caltech.edu/data/ZTF/docs/releases/dr14/ztf_release_notes_dr14.pdf

[^10]: AWS Open Data Registry - ZTF. https://registry.opendata.aws/ztf/

[^11]: LSDB ZTF Zubercal Tutorial. https://docs.lsdb.io/en/stable/tutorials/pre_executed/zubercal-ps1-snad.html

[^12]: IRSA ZTF Lightcurve API. https://irsa.ipac.caltech.edu/docs/program_interface/ztf_lightcurve_api.html

[^13]: ZTF Avro Alert Format documentation. https://zwickytransientfacility.github.io/ztf-avro-alert/

[^14]: Patterson et al. 2019, "The Zwicky Transient Facility Alert Distribution System", arXiv:1902.02227. https://arxiv.org/abs/1902.02227

[^15]: ZTF Avro Schemas reference. https://zwickytransientfacility.github.io/ztf-avro-alert/schema.html

[^16]: ZTF Forced Photometry User Guide (IPAC). https://irsa.ipac.caltech.edu/data/ZTF/docs/ztf_forced_photometry.pdf

[^17]: ZTF forced photometry service documentation. https://irsa.ipac.caltech.edu/data/ZTF/docs/forcedphot.pdf

[^18]: IRSA Forced Photometry guide. https://irsa.ipac.caltech.edu/Missions/ztf.html (Forced-Photometry User Guide)

[^19]: ztffp GitHub (Michael C. Stroh). https://github.com/mcstroh/ztf_fp

[^20]: fpbot GitHub (Simeon Reusch). https://github.com/simeonreusch/fpbot

[^21]: ztffps GitHub (Simeon Reusch). https://github.com/simeonreusch/ztffps

[^22]: ForcePhotZTF GitHub (Yuhan Yao). https://github.com/yaoyuhan/ForcePhotZTF

[^23]: ZTF_api GitHub (Joan Alcaide). https://github.com/joanalnu/ZTF_api

[^24]: Rigault et al. 2025, "ZTF SN Ia DR2: Overview", A&A. https://www.aanda.org/articles/aa/full_html/2025/02/aa50388-24/aa50388-24.html

[^25]: Aubert et al. 2025, "ZTF SN Ia DR2: Exploring SN Ia properties in the vicinity of under-dense environments", A&A. https://www.aanda.org/articles/aa/full_html/2025/02/aa50951-24/aa50951-24.html

[^26]: ZTF Bright Transient Survey website. https://sites.astro.caltech.edu/ztf/bts/bts.php

[^27]: Perley et al. 2020, "The Zwicky Transient Facility Bright Transient Survey. II. A Public Statistical Sample for Exploring Supernova Demographics", ApJ. https://arxiv.org/abs/2009.01242

[^28]: Fremling et al. 2020, "The Zwicky Transient Facility Bright Transient Survey. I.", ApJ.

[^29]: BTS Forced Photometry GitHub. https://github.com/BrightTransientSurvey/ztf_forced_phot

[^30]: ztfquery GitHub (Mickael Rigault). https://github.com/MickaelRigault/ztfquery

[^31]: ztfquery query documentation. https://github.com/MickaelRigault/ztfquery/blob/master/doc/query.md

[^32]: ztfimg GitHub (Mickael Rigault). https://github.com/MickaelRigault/ztfimg

[^33]: ztfimg documentation. https://ztfimg.readthedocs.io/

[^34]: ztf-dr GitHub (ALeRCE). https://github.com/alercebroker/ztf_dr

[^35]: ALeRCE Python Client. https://github.com/alercebroker/alerce_client

[^36]: Lasair documentation. https://lasair.readthedocs.io/

[^37]: TNS Getting Started. https://www.wis-tns.org/content/tns-getting-started

[^38]: TNS APIs Manual. https://www.wis-tns.org/sites/default/files/api/tns2_manuals/TNS2.0_APIs_manual.pdf

[^39]: ZTF Alert Archive (UW). https://ztf.uw.edu/alerts/public/

[^40]: ZTF Alert Stream page with broker list. https://www.ztf.caltech.edu/ztf-alert-stream.html

[^41]: ZTF Bright Transient Survey presentation (NOIRLab). https://noirlab.edu/science/sites/default/files/media/archives/presentations/scipresentation0975-en.pdf

[^42]: ZTF matchfile structure documentation (analogous PGIR matchfile documentation). https://arxiv.org/html/2406.01720v2

[^43]: LSDB ZTF alerts SNe tutorial. https://docs.lsdb.io/en/latest/tutorials/pre_executed/ztf-alerts-sne.html

[^44]: Zubercal documentation (IPAC). https://irsa.ipac.caltech.edu/data/ZTF/zubercal/overview.pdf

[^45]: Zubercal web page. http://nesssi.cacr.caltech.edu/ZTF/Web/Zuber.html

[^46]: Zubercal-PS1-SNAD tutorial. https://docs.lsdb.io/en/stable/tutorials/pre_executed/zubercal-ps1-snad.html

[^47]: de Soto et al. 2024, "Realtime Fitting and Classification of Supernova Light Curves", arXiv:2403.07975. https://arxiv.org/html/2403.07975v1

[^48]: Superphot+ GitHub. https://github.com/VTDA-Group/superphot-plus

[^49]: Superphot+ documentation. https://superphot-plus.readthedocs.io/

[^50]: ALeRCE ZTF alerts SNe analysis. https://docs.lsdb.io/en/latest/tutorials/pre_executed/ztf-alerts-sne.html

[^51]: Carrasco-Davis et al. 2021, ALeRCE stamp classifier.

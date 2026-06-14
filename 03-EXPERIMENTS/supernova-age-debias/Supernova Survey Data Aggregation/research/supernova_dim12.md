# Dimension 12: Data Access Patterns, Formats & Python Ecosystem

## Executive Summary

Supernova data is distributed across a complex ecosystem of formats, protocols, and tools. This document surveys the practical data access landscape for ML practitioners, covering file formats (SNANA FITS, Avro, JSON, VOTable, Parquet), Python access libraries (sncosmo, astroquery, pyvo), bulk download strategies, data volume estimates, and recommended ML pipelines. A key insight is that **no single format dominates** — each serves different use cases, and modern ML pipelines must be able to ingest and normalize multiple formats.

---

## 1. SNANA FITS Format

### 1.1 Structure: HEAD.fits + PHOT.fits

The SNANA software package, developed by Rick Kessler and collaborators, uses a dual-file FITS format for storing supernova data efficiently at scale [^848^][^102^]:

- **HEAD.fits** (Header): Contains one row per supernova with metadata including SNID, redshift, coordinates, peak magnitude, classification, fit parameters, and other object-level properties.
- **PHOT.fits** (Photometry): Contains one row per photometric observation (epoch) with MJD, filter/band, flux, flux error, zero point, and other measurement-level data. A pointer column connects each photometry row back to its parent SN in the HEAD file.

This split design allows efficient storage because metadata is not duplicated across epochs, and enables vectorized operations on either the object or observation level [^99^][^98^].

### 1.2 Key Properties

| Property | Value |
|----------|-------|
| Format | FITS binary tables |
| Files required | HEAD.fits + PHOT.fits (paired) |
| Typical use case | Large-scale simulations, cosmology analyses (SDSS, DES, PS1, JLA) |
| Compression | None intrinsic; files often gzipped |
| Standard fields (HEAD) | SNID, RA, DECL, ZHEL, ZCMB, PEAKMJD, mB, x1, c, FITPROB |
| Standard fields (PHOT) | MJD, FLT, FLUXCAL, FLUXCALERR, ZPFLUX, PSF, SKY_SIG |

### 1.3 Reading with sncosmo

The `sncosmo` Python library provides native support for reading SNANA FITS files [^848^]:

```python
import sncosmo

# Read all supernovae from a SNANA FITS pair
sne = sncosmo.read_snana_fits('HEAD.fits', 'PHOT.fits')

# Iterate over supernovae
for sn in sne:
    print(sn.meta)       # Metadata as OrderedDict
    print(sn['MJD'])     # MJD column
    print(sn['FLUXCAL']) # Flux column

# Read only specific SNIDs
sne = sncosmo.read_snana_fits('HEAD.fits', 'PHOT.fits', snids=['SN2005hf'])

# Read only first N supernovae
sne = sncosmo.read_snana_fits('HEAD.fits', 'PHOT.fits', n=100)
```

### 1.4 Reading with Astropy (Lower-Level)

For custom processing, astropy.io.fits provides direct access [^870^]:

```python
from astropy.io import fits
from astropy.table import Table

# Read HEAD and PHOT separately
head = Table.read('HEAD.fits')
phot = Table.read('PHOT.fits')

# HEAD: one row per SN
print(f"Number of SNe: {len(head)}")
print(f"Columns: {head.colnames}")

# PHOT: one row per epoch
# The SNID column links photometry rows to HEAD rows
snid = head['SNID'][0]
sn_phot = phot[phot['SNID'] == snid]
```

### 1.5 SNANA ASCII Format (Deprecated for Large Jobs)

SNANA also supports a text-based format (one file per SN) for testing and debugging [^102^][^99^]:
- Set `FORMAT_MASK: 2` for ASCII output in simulations
- Set `FORMAT_MASK: 32` for FITS output (recommended for production)

The ASCII format is described as: "NEVER use ascii format for large sim jobs!" [^102^].

### 1.6 SNANA Output Tables

SNANA analysis produces several table types [^99^][^102^]:
- **SNANA table**: Before-fit summary (1 row per SN)
- **FITRES table**: After-fit summary with fit parameters (1 row per SN)
- **LCPLOT table**: Light curve data with best-fit model

Available in TEXT, HBOOK (historical), and ROOT formats.

### 1.7 Access URLs and Data Releases

| Survey | Data Release | Format | URL |
|--------|-------------|--------|-----|
| SDSS-II SN | DR7+ | SNANA FITS | https://classic.sdss.org/supernova/snana.html |
| DES 5-Year | DES-SN5YR | SNANA FITS | https://des.ncsa.illinois.edu/releases/sn |
| Pantheon | Scolnic+2018 | SNANA FITS | https://github.com/dscolnic/Pantheon |
| Pantheon+ | Brout+2022 | SNANA FITS | https://github.com/PantheonPlusSH0ES |
| Foundation | Foley+2018 | SNANA FITS | https://github.com/dscolnic/Foundation |

---

## 2. Avro Format (LSST/Rubin Alerts)

### 2.1 Overview

Apache Avro is a compact binary serialization format used by modern time-domain surveys for streaming alert packets. It combines data with its schema, enabling both compact transmission and schema evolution [^810^][^811^].

### 2.2 LSST/Rubin Alert Packet Structure

Each Rubin Observatory alert packet contains [^290^][^914^][^915^]:

- **diaSourceId**: Unique identifier for the triggering detection
- **diaSource**: The DIA source record that triggered the alert (5-sigma detection)
- **diaObject**: Associated object record (history and aggregated properties)
- **prvDiaSources**: Previous DIA source detections (up to 12 months of history)
- **prvDiaForcedSources**: Forced photometry measurements at the object position
- **cutoutScience**: 30x30 pixel cutout from the science image (FITS)
- **cutoutTemplate**: 30x30 pixel cutout from the template image (FITS)
- **cutoutDifference**: 30x30 pixel cutout from the difference image (FITS)
- **ssObject**: Solar system object record (if applicable)
- **mpcOrbit**: Minor Planet Center orbit data (if applicable)

### 2.3 Rubin Data Volumes

| Metric | Value |
|--------|-------|
| Raw data per night | ~10 TB [^929^][^931^] |
| Alerts per night | Up to 7-10 million [^929^][^50^] |
| Alert packet size | ~82 KB per alert (with history and cutouts) [^210^] |
| Stream rate | ~0.2-5 Gbps [^210^] |
| Processing latency | 60-120 seconds from shutter close [^929^] |
| 10-year catalog volume | ~15 PB, 37 billion objects [^940^] |

### 2.4 Python: Reading Avro with fastavro

The `fastavro` library is the recommended Python tool for reading alert packets [^810^][^811^]:

```python
import fastavro

# Read alerts from an Avro file
with open('alerts.avro', 'rb') as f:
    reader = fastavro.reader(f)
    schema = reader.schema  # Extract embedded schema
    
    for packet in reader:
        # Access DIA source information
        dia_source = packet['diaSource']
        print(f"Source ID: {dia_source['diaSourceId']}")
        print(f"RA: {dia_source['ra']}, Dec: {dia_source['decl']}")
        print(f"Magnitude: {dia_source['mag']}")
        
        # Access previous detections (light curve history)
        if 'prvDiaSources' in packet:
            for prev in packet['prvDiaSources']:
                print(f"  Previous: MJD={prev['midPointTai']}, "
                      f"mag={prev['mag']}")
        
        # Access cutout images
        if 'cutoutScience' in packet and packet['cutoutScience']:
            cutout_data = packet['cutoutScience']['stampData']
            # cutout_data is a FITS-formatted byte string
```

### 2.5 ZTF Avro Alerts

The Zwicky Transient Facility uses a similar Avro format, documented at [^108^]:

- Repository: https://github.com/ZwickyTransientFacility/ztf-avro-alert
- Schema files in `.avsc` format
- Example notebooks for loading and filtering
- Public stream accessible via ALeRCE, Lasair, and other brokers

### 2.6 Alert Brokers (Distribution Infrastructure)

Seven full-stream brokers receive the complete LSST alert stream [^44^][^937^]:

| Broker | Features | URL |
|--------|----------|-----|
| **ALeRCE** | ML classifiers (stamp + light-curve), Chile-based | https://alerce.science |
| **AMPEL** | Flexible filtering, Germany-based | https://ampel.zeuthen.desy.de |
| **ANTARES** | Arizona-NOIRLab, real-bogus, SkyMapper cross-match | https://antares.noirlab.edu |
| **Babamul** | New broker (BOOM framework), multi-survey | - |
| **Fink** | Apache Spark, multi-messenger, France-based | https://fink-broker.org |
| **Lasair** | SQL-like filtering, Sherlock classifier, UK | https://lasair.lsst.ac.uk |
| **Pitt-Google** | Cloud-native (GCP), YADNT classifier | https://pittgoogle.readthedocs.io |

### 2.7 Sample Alert Data

LSST sample alerts are available for download [^810^]:
- **Full sample**: ~50 GB of precursor alerts
- **Single CCD visit**: Smaller subset for testing
- **Single visit**: All alerts from one visit
- **SQLite PPDB**: Database from which alerts were generated

```
sample_precursor_alerts/
  YYYY-MM-DD/
    dataset/
      all_visits_{dataset}_{date}.avro
      association_{dataset}_{date}.db
      single_ccd_sample_{dataset}_{date}.avro
      single_visit_sample_{dataset}_{date}.avro
```

---

## 3. JSON Format (Open Supernova Catalog)

### 3.1 Overview

The Open Supernova Catalog (OSC) uses JSON as its native format, with one file per supernova [^651^][^866^]. This format is human-readable and web-native but less efficient for bulk analysis than FITS or Parquet.

### 3.2 OSC JSON Schema

Each JSON file follows a schema defined by the `astroschema` project [^866^]:

```json
{
  "name": "SN2023A",
  "aliases": [
    {"value": "SN2023A", "kind": "name"},
    {"value": "AT2023A", "kind": "name"}
  ],
  "distances": [...],
  "claimedtype": [
    {"value": "Ia", "kind": "spectroscopic"}
  ],
  "photometry": [
    {
      "time": "59950.123",
      "band": "g",
      "magnitude": "18.52",
      "e_magnitude": "0.05",
      "upperlimit": false,
      "telescope": "LSST",
      "instrument": "LSSTCam"
    }
  ],
  "spectra": [...],
  "sources": [...],
  "ra": [...],
  "dec": [...],
  "redshift": [...],
  "host": [...]
}
```

### 3.3 Reading OSC JSON with Python

```python
import json
import os
import glob
from astropy.table import Table
import numpy as np

# Read a single SN JSON file
with open('SN2023A.json', 'r') as f:
    sn_data = json.load(f)

# Extract photometry table
if 'photometry' in sn_data:
    phot_table = Table(sn_data['photometry'])
    print(phot_table)

# Batch read all JSON files in a directory
def load_osc_directory(directory):
    """Load all OSC JSON files from a directory."""
    sne = []
    for filepath in glob.glob(os.path.join(directory, '*.json')):
        with open(filepath, 'r') as f:
            sne.append(json.load(f))
    return sne

# Convert photometry to standardized astropy Table
def extract_photometry(sn_data):
    """Extract photometry from OSC entry to astropy Table."""
    if 'photometry' not in sn_data:
        return None
    
    phot = Table(sn_data['photometry'])
    # Ensure standard columns
    if 'magnitude' in phot.colnames and 'e_magnitude' in phot.colnames:
        phot['flux'] = 10**(-0.4 * (phot['magnitude'].astype(float) - 25.0))
        phot['fluxerr'] = (phot['e_magnitude'].astype(float) * 
                          phot['flux'] * np.log(10) / 2.5)
    return phot
```

### 3.4 Accessing OSC Data

| Resource | URL | Format |
|----------|-----|--------|
| Open Supernova Catalog | https://sne.space | Web interface |
| GitHub Repository | https://github.com/astrocatalogs/supernovae | Git LFS |
| OSC API | https://api.astrocats.space | JSON API |
| astroschema | https://github.com/astrocatalogs/astroschema | Schema definitions |

### 3.5 OSC Data via API

```python
import requests

# Query the OSC API
response = requests.get(
    'https://api.astrocats.space/SN2023A/photometry',
    params={'format': 'json'}
)
data = response.json()
```

---

## 4. VOTable

### 4.1 Overview

VOTable is the IVOA standard XML-based format for astronomical tabular data. It is commonly returned by Virtual Observatory services including VizieR, SIMBAD, and TAP/ADQL queries [^861^].

### 4.2 Reading VOTable with Astropy

```python
from astropy.io.votable import parse, parse_single_table

# Parse a VOTable file
votable = parse("catalog.xml")

# Get the first table
table = votable.get_first_table()
print(f"Table name: {table.name}")
print(f"Number of rows: {len(table.array)}")

# Convert to astropy Table (most convenient for analysis)
astropy_table = table.to_table()

# Or parse directly to astropy Table (simpler one-liner)
from astropy.io.votable import parse_single_table
astropy_table = parse_single_table("catalog.xml").to_table()
```

### 4.3 Writing VOTable

```python
from astropy.table import Table
from astropy.io.votable import from_table, writeto

# Convert astropy Table to VOTable
table = Table({'name': ['SN2023A', 'SN2023B'],
               'ra': [150.123, 160.456],
               'dec': [+25.789, -15.321]})

votable = from_table(table)
writeto(votable, "output.xml")
```

### 4.4 VOTable Format Variants

| Format | Description | Use Case |
|--------|-------------|----------|
| TABLEDATA | XML-based string storage | Human-readable, large files |
| BINARY | Base64-encoded binary | Compact, faster I/O |
| BINARY2 | Binary with masking support | Recommended for new data [^861^] |

### 4.5 Performance Tips

- Include `nrows` attribute for faster parsing [^861^]
- Use BINARY2 format for smaller file sizes
- For large catalogs, consider converting to Parquet after initial download
- Use `verify='warn'` for non-compliant files: `parse("file.xml", verify='warn')`

---

## 5. Parquet Format

### 5.1 Overview

Apache Parquet is a columnar storage format that has gained traction in modern astronomical data releases. It offers efficient compression, fast column-wise queries, and native support in the Python data science ecosystem (pandas, pyarrow) [^328^][^269^].

### 5.2 Roman Hourglass Survey Data

The Roman Space Telescope Hourglass simulation is released in Parquet format [^328^][^269^]:

**Three files on Zenodo (doi:10.5281/zenodo.14262943):**

| File | Rows | Content |
|------|------|---------|
| `hourglass_objects.parquet` | ~65,000 | One row per object: CID, RA, Dec, redshift, class, peak magnitudes |
| `hourglass_photometry.parquet` | ~millions | One row per flux measurement: CID, MJD, band, fluxcal, fluxcal_err, PSF |
| `hourglass_spectra.parquet` | ~per epoch | One row per object per epoch: CID, MJD, wavelength arrays, flux arrays |

### 5.3 Reading Roman Parquet with Python

```python
import pandas as pd
import pyarrow.parquet as pq

# Method 1: pandas (simplest)
objects = pd.read_parquet('hourglass_objects.parquet')
photometry = pd.read_parquet('hourglass_photometry.parquet')

# Method 2: pyarrow with metadata inspection
pf = pq.ParquetFile('hourglass_objects.parquet')
print(pf.metadata.metadata)  # Dataset version, production date

# Read only specific columns (efficient - columnar access)
columns = ['cid', 'ra', 'dec', 'z_cmb', 'class']
objects_subset = pd.read_parquet('hourglass_objects.parquet', columns=columns)

# Join photometry with object metadata
merged = photometry.merge(objects[['cid', 'ra', 'dec', 'z_cmb', 'class']], 
                          on='cid', how='left')

# Convert to astropy Table if needed
from astropy.table import Table
astropy_table = Table.from_pandas(merged)
```

### 5.4 DESC Data (DC2) Format

The LSST DESC Data Challenge 2 uses HDF5 and Parquet formats accessible through `GCRCatalogs` [^750^]:

| Dataset | Format | Size |
|---------|--------|------|
| DC2 Object Catalog | Parquet/HDF5 | ~180 GB |
| DC2 Truth Match | Parquet/HDF5 | Subset of above |
| cosmoDC2 | HDF5 | >5 TB |

Access via Globus portal: https://data.lsstdesc.org/ [^750^]

---

## 6. astroquery: Unified Python Data Access

### 6.1 Overview

`astroquery` is an astropy-affiliated package providing a unified interface to dozens of astronomical archives [^845^][^854^].

### 6.2 Key Modules for Supernova Research

```python
# VizieR: Access to thousands of published catalogs
from astroquery.vizier import Vizier

v = Vizier(columns=['*', '_RAJ2000', '_DEJ2000'])
v.ROW_LIMIT = -1  # No row limit
result = v.query_region("SN 2023A", radius="1s", catalog='II/246')

# SIMBAD: Astronomical object database
from astroquery.simbad import Simbad

custom_simbad = Simbad()
custom_simbad.add_votable_fields('otype', 'z_value', 'flux(B)', 'flux(V)')
result = custom_simbad.query_object("SN 2023A")

# HEASARC: X-ray and high-energy data
from astroquery.heasarc import Heasarc
heasarc = Heasarc()

catalogs = heasarc.list_catalogs()
result = heasarc.query_region(position="150.0 2.0", 
                               catalog='swiftmastr', radius='1d')

# MAST: Hubble, TESS, and other missions
from astroquery.mast import Catalogs
catalog_data = Catalogs.query_object("SN 2023A", catalog="PANSTARRS")

# NED: NASA/IPAC Extragalactic Database
from astroquery.ipac.ned import Ned
result = Ned.query_object("SN 2023A")

# IRSA: Infrared data
from astroquery.ipac.irsa import Irsa
result = Irsa.query_region(coord, catalog='allwise_p3as_psd', radius=0.1*u.deg)
```

### 6.3 HEASARC Cloud Access (AWS S3)

HEASARC data is available directly from AWS S3 via astroquery [^860^][^864^][^37^]:

```python
from astroquery.heasarc import Heasarc
from astropy.coordinates import SkyCoord
import astropy.units as u

heasarc = Heasarc()

# Query for data
pos = SkyCoord('150.0 2.0', unit=u.deg)
result = heasarc.query_region(pos, catalog='swiftmastr', radius='1d')

# Get data product links
links = heasarc.locate_data(result[:5])

# Download from AWS S3 (no egress charges)
heasarc.download_data(links, host='aws', location='./data')
```

### 6.4 HEASARC S3 Bucket Structure

| Bucket | Contents | Size |
|--------|----------|------|
| `s3://nasa-heasarc/` | All HEASARC mission data | >50 TB total |
| `s3://nasa-lambda/` | LAMBDA CMB data | Various |

Direct AWS CLI access [^864^]:
```bash
# List Swift observations
aws s3 ls s3://nasa-heasarc/swift/data/obs/ --no-sign-request

# Download specific observation
aws s3 cp --recursive --no-sign-request \
  s3://nasa-heasarc/swift/data/obs/2025_03/00014197056/ \
  ./00014197056/
```

---

## 7. pyvo: Virtual Observatory Data Access

### 7.1 Overview

`pyvo` provides Python access to Virtual Observatory protocols including TAP, SIA, SSA, and SCS [^941^][^857^]. It is the lower-level foundation that astroquery uses internally for many VO services.

### 7.2 TAP Queries with pyvo

```python
import pyvo as vo
from astropy.table import Table

# Connect to a TAP service
tap_service = vo.dal.TAPService("http://dc.g-vo.org/tap")

# Run a simple query
result = tap_service.search("""
    SELECT TOP 5 source_id, ra, dec, phot_g_mean_mag
    FROM gaia.dr3lite
    WHERE phot_g_mean_mag BETWEEN 19 AND 20
""")

# Convert to astropy Table
table = result.to_table()

# Inspect available tables on a service
simbad = vo.dal.TAPService("http://simbad.cds.unistra.fr/simbad/sim-tap")
print([name for name in simbad.tables.keys()])

# Complex ADQL query with geometry
query = """
    SELECT diaSourceId, ra, dec, midPointTai, mag
    FROM dp1.DiaSource
    WHERE CONTAINS(
        POINT('ICRS', ra, dec),
        CIRCLE('ICRS', 150.0, 2.5, 0.1)
    ) = 1
    AND mag < 20
"""
```

### 7.3 Registry Search

```python
# Discover TAP services supporting a data model
for service in vo.registry.search(datamodel="obscore"):
    print(service['ivoid'])
    
# Search for cone search services
cs_services = vo.regsearch(servicetype='conesearch', 
                            keywords=['supernova'])
```

### 7.4 Key TAP Services for SN Research

| Service | URL | Contents |
|---------|-----|----------|
| SIMBAD TAP | http://simbad.cds.unistra.fr/simbad/sim-tap | Object identifications, bibliography |
| VizieR TAP | http://tapvizier.cds.unistra.fr/TAPVizieR.tap | Published catalogs |
| MAST TAP | https://mast.stsci.edu/vo-tap/ | Hubble, TESS, Pan-STARRS |
| HEASARC TAP | https://heasarc.gsfc.nasa.gov/xamin/vo/tap | X-ray/gamma-ray data |
| IRSA TAP | https://irsa.ipac.caltech.edu/TAP | Infrared data |
| Rubin/LSST | ADQL via RSP | LSST data previews |

---

## 8. Bulk Download Strategies

### 8.1 wget/curl

```bash
# Download a list of URLs
wget -i urls.txt

# Resume interrupted download
wget -c http://example.com/large_file.fits

# Download with authentication
curl -O -b ~/.urs_cookies -c ~/.urs_cookies -L -n < urls.txt

# Parallel downloads with xargs
cat urls.txt | xargs -n 1 -P 8 wget -q
```

### 8.2 AWS S3 (HEASARC and Other NASA Archives)

```bash
# List bucket contents
aws s3 ls s3://nasa-heasarc/swift/data/obs/ --no-sign-request

# Download entire directory tree
aws s3 cp --recursive --no-sign-request \
  s3://nasa-heasarc/mission/data/ ./local_data/

# Sync (incremental download)
aws s3 sync --no-sign-request \
  s3://nasa-heasarc/fermi/data/ ./fermi_data/
```

### 8.3 Globus (DESC and LSST Data)

The LSST DESC Data Portal uses Globus for transfers [^750^]:
- Portal: https://data.lsstdesc.org/
- DC2 Object+Truth Match: ~180 GB
- cosmoDC2: >5 TB
- Requires Globus account and endpoint setup

### 8.4 Rubin Science Platform (RSP)

For LSST/Rubin data, the recommended access is via the Rubin Science Platform [^787^]:
- Portal: https://data.lsst.cloud
- Jupyter notebooks with pre-installed `lsdb` and `pyarrow`
- TAP queries via `pyvo`
- Direct catalog access via `lsdb` (LSST-DM Science Datasets Browser)

---

## 9. Data Volume Estimates

### 9.1 Survey Data Volumes

| Survey/Data Set | Volume | Format | Notes |
|----------------|--------|--------|-------|
| Rubin/LSST raw (10 yr) | 60 PB | FITS | 20 TB/night [^931^] |
| Rubin/LSST catalog (10 yr) | 20 PB | Various | 15 PB catalog, 37B objects [^940^] |
| Rubin/LSST alerts (1 night) | ~1 TB | Avro | 7-10M alerts [^929^] |
| DESC DC2 Object | 180 GB | Parquet/HDF5 | [^750^] |
| DESC cosmoDC2 | 5+ TB | HDF5 | [^750^] |
| Roman Hourglass | ~10 GB | Parquet | Zenodo release [^328^] |
| ZTF Alerts (public, cumulative) | ~50 TB | Avro | Since 2018 |
| HEASARC (all missions) | >50 TB | FITS | S3-hosted [^37^] |
| Open Supernova Catalog | ~2 GB | JSON | All SN data [^651^] |
| Pantheon+ | ~500 MB | SNANA FITS | ~1500 SNe Ia [^102^] |
| Foundation DR1 | ~200 MB | SNANA FITS | ~1000 SNe Ia |

### 9.2 ML Training Data Size Estimates

| Use Case | Estimated Size | Format Recommendation |
|----------|---------------|----------------------|
| Small-scale classification (thousands) | 100 MB - 1 GB | HDF5 or Parquet |
| Medium-scale (hundreds of thousands) | 1 - 10 GB | Parquet + lazy loading |
| Large-scale (millions, LSST-like) | 100+ GB | Parquet/Arrow + Dask |
| Full alert stream processing | 1+ TB/day | Streaming (Kafka) + Avro |

---

## 10. Recommended ML Data Pipeline

### 10.1 Pipeline Architecture

```
Stage 1: Data Acquisition
  ├── Survey-specific download (S3/Globus/wget)
  ├── Broker query (TAP/ADQL for catalogs)
  ├── Alert stream subscription (Kafka for real-time)
  └── Local caching and versioning

Stage 2: Ingestion & Normalization
  ├── Format detection (FITS/Avro/JSON/Parquet/VOTable)
  ├── Schema validation
  ├── Column name standardization
  ├── Unit conversion (to common zeropoint, magnitude system)
  └── Quality cuts (SNR, nbad, real-bogus score)

Stage 3: Feature Extraction
  ├── Light curve interpolation (to common time grid)
  ├── Photometric features (rise time, decline rate, color)
  ├── Image features (from cutouts, if available)
  ├── Contextual features (host galaxy, redshift, Milky Way extinction)
  └── Derived features (periodicity, variability indices)

Stage 4: Dataset Construction
  ├── Train/validation/test split (temporal or random)
  ├── Class balancing (oversample rare classes)
  ├── Feature scaling/normalization
  ├── Sequence padding (for RNNs/Transformers)
  └── Convert to ML framework format (TFRecord, HDF5, Arrow)

Stage 5: Training & Iteration
  ├── Incremental data loading (for large datasets)
  ├── Active learning (prioritize uncertain objects)
  └── Model versioning and experiment tracking
```

### 10.2 Python Implementation Pattern

```python
"""
Complete ML pipeline example for supernova data.
"""
import pandas as pd
import numpy as np
from astropy.table import Table, vstack
import sncosmo
import pyarrow.parquet as pq
from pathlib import Path

class SNDatasetPipeline:
    """ML-ready supernova data pipeline."""
    
    def __init__(self, cache_dir='./cache'):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
    def load_snana_fits(self, head_file, phot_file):
        """Load SNANA FITS data into standardized format."""
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
        """Load Parquet data with optional column selection."""
        return pd.read_parquet(filepath, columns=columns)
    
    def load_avro_alerts(self, filepath):
        """Load Avro alert packets."""
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
        """Apply standard quality cuts."""
        if 'rb' in df.columns:  # ZTF real-bogus
            df = df[df['rb'] >= 0.65]
        if 'nbad' in df.columns:
            df = df[df['nbad'] == 0]
        if 'fluxerr' in df.columns:
            df = df[df['fluxerr'] > 0]  # Remove invalid errors
        return df.reset_index(drop=True)
    
    def to_sncosmo_format(self, df, snid_col='snid'):
        """Convert DataFrame to list of sncosmo Tables."""
        tables = []
        for snid, group in df.groupby(snid_col):
            t = Table.from_pandas(group)
            t.meta['SNID'] = snid
            tables.append(t)
        return tables
```

---

## 11. Caching and Incremental Update Strategies

### 11.1 Local Caching Patterns

```python
import hashlib
import pickle
from pathlib import Path

def cache_result(cache_dir, key, compute_fn):
    """Simple file-based cache."""
    cache_path = Path(cache_dir) / f"{hashlib.md5(key.encode()).hexdigest()}.pkl"
    if cache_path.exists():
        return pickle.load(open(cache_path, 'rb'))
    result = compute_fn()
    pickle.dump(result, open(cache_path, 'wb'))
    return result

# For catalogs that update daily
def incremental_update(base_catalog, new_entries, merge_key='diaSourceId'):
    """Merge new entries into existing catalog."""
    existing_ids = set(base_catalog[merge_key])
    truly_new = new_entries[~new_entries[merge_key].isin(existing_ids)]
    return pd.concat([base_catalog, truly_new], ignore_index=True)
```

### 11.2 astroquery Built-in Caching

astroquery has built-in caching that can be enabled/disabled per-query [^918^]:

```python
from astroquery.simbad import Simbad

# Cache is enabled by default; disable for fresh queries
result = Simbad.query_object("SN 2023A", cache=False)

# Clear cache
Simbad.clear_cache()
```

### 11.3 Streaming Alert Processing

For real-time ML on the alert stream, use streaming patterns [^719^][^59^]:

```python
from kafka import KafkaConsumer
import fastavro
import io

def process_alert_stream(broker_url, topic, model):
    """Process alerts in real-time for ML inference."""
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=[broker_url],
        value_deserializer=lambda m: fastavro.reader(io.BytesIO(m))
    )
    
    for message in consumer:
        packet = message.value
        
        # Extract features
        features = extract_features(packet)
        
        # Run inference
        prediction = model.predict(features)
        
        # Action based on prediction
        if prediction['prob_sn'] > 0.9:
            trigger_follow_up(packet, prediction)
```

### 11.4 Recommended Strategy for Daily-Updated Catalogs

1. **Initial bulk download**: Use S3 sync or wget for complete dataset
2. **Daily incremental**: Query TAP services with `WHERE date > last_update`
3. **Version control**: Tag datasets with download date, use DVC or similar
4. **Delta detection**: For broker streams, use Kafka consumer groups with offsets
5. **Local snapshot**: Maintain local Parquet files with `write_version` metadata
6. **Expired data cleanup**: For time-series features, implement sliding windows

---

## 12. Format Comparison Summary

| Format | Structure | Best For | Python Tool | Read Speed | Write Speed | File Size |
|--------|-----------|----------|-------------|------------|-------------|-----------|
| **SNANA FITS** | HEAD+PHOT paired | Large simulations, cosmology | sncosmo, astropy | Fast | Fast | Medium |
| **Avro** | Binary packets with schema | Streaming alerts, brokers | fastavro | Very Fast | Very Fast | Small |
| **JSON (OSC)** | Per-SN files | Human-readable, web APIs | json, pandas | Slow | Slow | Large |
| **VOTable** | XML tables | VO queries, interoperability | astropy.io.votable | Medium | Slow | Large |
| **Parquet** | Columnar, compressed | Analysis, ML training | pandas, pyarrow | Very Fast | Very Fast | Small |
| **HDF5** | Hierarchical datasets | Large simulations | h5py, pandas | Fast | Fast | Medium |
| **ASCII/Text** | Row-based tables | Debugging, compatibility | numpy.loadtxt | Slow | Slow | Large |

---

## 13. Key Software Ecosystem Summary

| Package | Primary Use | SN-Specific? | Installation |
|---------|-------------|-------------|--------------|
| **sncosmo** | Read SNANA, fit light curves, models | Yes | `pip install sncosmo` |
| **astroquery** | Unified archive access | No | `pip install astroquery` |
| **pyvo** | Virtual Observatory protocols | No | `pip install pyvo` |
| **fastavro** | Read Avro alert packets | No | `pip install fastavro` |
| **astropy** | FITS, VOTable, Tables, coordinates | No | `pip install astropy` |
| **pandas/pyarrow** | Parquet, data manipulation | No | `pip install pyarrow` |
| **lsst-alert-packet** | LSST alert schema utilities | Yes | `pip install lsst-alert-packet` |
| **GCRCatalogs** | DESC data access | Yes | `pip install GCRCatalogs` |

---

## 14. Areas Warranting Deeper Investigation

1. **LSST Science Platform (RSP) access patterns**: How to efficiently extract training data from DP1/DP2 via TAP queries and `lsdb` [^787^]
2. **Roman WFI ASDF format**: Roman will use Advanced Scientific Data Format rather than FITS — need to investigate `asdf` Python library integration [^869^]
3. **Real-time streaming ML**: Best practices for deploying models on Kafka streams with the 7-10M alert/night scale [^719^]
4. **Cross-format data fusion**: Combining SNANA FITS + ZTF Avro + OSC JSON into unified training sets
5. **Incremental learning**: Strategies for updating models as new data arrives without full retraining
6. **Cloud-native pipelines**: Using AWS S3 + Lambda/Dask for processing HEASARC and LSST-scale data

---

## References

[^848^] sncosmo documentation: `read_snana_fits` - https://sncosmo.readthedocs.io/en/stable/api/sncosmo.read_snana_fits.html
[^540^] sncosmo v2.0 PDF documentation - https://sncosmo.readthedocs.io/_/downloads/en/v2.0.x/pdf/
[^35^] SNCosmo: Python library for supernova cosmology, ADS 2016 - http://ui.adsabs.harvard.edu/abs/2016ascl.soft11017B/abstract
[^810^] LSST sample_alert_info GitHub repository - https://github.com/lsst-dm/sample_alert_info
[^855^] lsst.alert.packet.Schema documentation - https://pipelines.lsst.io/py-api/lsst.alert.packet.Schema.html
[^811^] lsst/alert_packet GitHub repository - https://github.com/lsst/alert_packet
[^845^] CDS Python Tutorials - https://cds.unistra.fr/help/tutorials/
[^850^] Multi-instrument VO tutorial with pyvo - https://cds-astro.github.io/tutorials/
[^853^] Using Virtual Observatory with Python: querying remote astronomical databases - https://ui.adsabs.harvard.edu/abs/2014arXiv1408.7026P
[^854^] CDS and Python: Simbad tutorial - https://www.astrobetter.com/blog/2020/07/06/the-cds-and-python-iv-simbad/
[^856^] sncosmo Photometric Data documentation - https://sncosmo.readthedocs.io/en/stable/photdata.html
[^846^] MAST TAP Service - https://mast.stsci.edu/vo-tap/
[^847^] ESO Archive FAQ - https://support.eso.org/en-GB/kb/articles/pdf/archive-faq-getting-data-programmatic
[^849^] Multimessenger Astronomy with ObsTAP and PyVO - https://moodle2.units.it/pluginfile.php/769740/mod_resource/content/1/mm_pyvo.pdf
[^851^] A Short Course on pyVO - http://docs.g-vo.org/pyvo/slides.pdf
[^857^] TAP Support in PyVO - https://ui.adsabs.harvard.edu/abs/2019ASPC..521..483B
[^861^] Astropy VOTable Handling - https://docs.astropy.org/en/latest/io/votable/index.html
[^862^] Reading and Writing Parquet Files in Python - https://dev.to/alexmercedcoder/all-about-parquet-part-08
[^864^] Accessing HEASARC data in the Cloud - https://heasarc.gsfc.nasa.gov/docs/archive/cloud.html
[^866^] AstroCats astroschema - https://github.com/astrocatalogs/astroschema
[^867^] SNANA Tutorial 2023 - https://kicp.uchicago.edu/~kessler/SNANA_Tutorial/SNANA_Tutorial_2023-05.pdf
[^328^] Roman Hourglass Catalog (arXiv) - https://arxiv.org/html/2506.05161v1
[^269^] Hourglass Simulation paper (ApJ) - https://iopscience.iop.org/article/10.3847/1538-4357/ade1d6
[^929^] Rubin Prompt Processing System - https://arxiv.org/pdf/2603.19541
[^931^] Rubin Data Management - https://www.lsst.org/about/dm
[^290^] Rubin Alert packets documentation - https://prompt-products.lsst.io/products/alerts/index.html
[^914^] LSST Alert Streams & Solar System Science - https://lsst-sssc.github.io/Files/2018-07-10-SSSC-LSSTAlerts-LeanneGuy.pdf
[^915^] LSST Alert Stream update (Heidelberg 2026) - https://indico.in2p3.fr/event/37439/contributions/170349/
[^919^] Alert Production Database Schema - https://sdm-schemas.lsst.io/apdb.html
[^720^] BOOM and Babamul alert broker - https://arxiv.org/html/2511.00164v1
[^59^] ALeRCE Alert Broker paper - https://iopscience.iop.org/article/10.3847/1538-3881/abe9bc
[^108^] ZTF Avro Alert schema - https://github.com/ZwickyTransientFacility/ztf-avro-alert
[^44^] Rubin Alert Brokers - https://rubinobservatory.org/for-scientists/data-products/alerts-and-brokers
[^210^] Overview of astronomical transient brokers - https://www.astro.sk/caosp/Eedition/FullTexts/vol55no2/pp95-105.pdf
[^750^] LSST DESC Data Portal - https://data.lsstdesc.org/
[^787^] Accessing Rubin DP1 with lsdb - https://docs.lsdb.io/en/stable/tutorials/pre_executed/rubin_dp1.html
[^651^] Open Supernova Catalog paper - https://iopscience.iop.org/article/10.3847/1538-4357/835/1/64
[^869^] Preparing for Roman as a Big Data Survey Mission - https://www.stsci.edu/contents/newsletters/2024-volume-41-issue-02/
[^860^] astroquery.heasarc documentation - https://astroquery.readthedocs.io/en/latest/api/astroquery.heasarc.HeasarcClass.html
[^37^] NASA HEASARC on AWS Open Data - https://registry.opendata.aws/nasa-heasarc/
[^941^] PyVO documentation - https://pyvo.readthedocs.io/
[^942^] Using IRSA TAP services from Python - https://irsa.ipac.caltech.edu/docs/program_interface/astropy_TAP.html
[^945^] pyvo TAP Data Access - https://pyvo.readthedocs.io/en/latest/dal/index.html
[^99^] SNANA Tutorial (SDSS) - https://classic.sdss.org/supernova/snana/doc/snana_tutorial.pdf
[^98^] SNANA Starter Kit - https://snana-starterkit.readthedocs.io/en/latest/simulation.html
[^870^] Astropy FITS File Handling - https://docs.astropy.org/en/latest/io/fits/index.html
[^844^] sncosmo on conda - https://anaconda.org/astropy/sncosmo
[^50^] Rubin Observatory alert launch (Stanford News) - https://news.stanford.edu/stories/2026/02/rubin-observatory-real-time-alerts
[^332^] NSF Rubin Observatory Launches Real-Time Alerts - https://noirlab.edu/public/news/noirlab2605/
[^940^] LSST Alerts: Who, What, When, Where & Why - https://indico.in2p3.fr/event/18823/contributions/74200/
[^799^] Launching an Alert System for the Changing Sky - https://link.aps.org/doi/10.1103/Physics.19.31
[^934^] Anomaly Detection in the ZTF Alert Stream - https://arxiv.org/html/2602.12955v1
[^935^] ZTF Alert Filtering - https://zwickytransientfacility.github.io/ztf-avro-alert/filtering.html
[^936^] Lasair-LSST for ZTF users - https://community.lsst.org/t/lasair-lsst-for-users-of-lasair-ztf/10549
[^937^] The Lasair alert broker (EPCC) - https://www.epcc.ed.ac.uk/articles/lasair-alert-broker
[^916^] AXS: Fast Astronomical Data Processing - https://iopscience.iop.org/article/10.3847/1538-3881/ab2384
[^918^] astroquery changelog - https://astroquery.readthedocs.io/en/latest/changelog.html
[^733^] TOM Toolkit Brokers - https://tom-toolkit.readthedocs.io/en/stable/api/tom_alerts/brokers.html
[^938^] TOM Toolkit TNS module - https://github.com/TOMToolkit/tom_tns
[^800^] ALeRCE Alert Broker arXiv - https://arxiv.org/abs/2008.03303
[^852^] SNEMO documentation - https://snfactory.lbl.gov/snemo/
[^864^] HEASARC Cloud Access tutorial - https://heasarc.gsfc.nasa.gov/docs/archive/cloud.html
[^861^] Astropy VOTable Handling (latest) - https://docs.astropy.org/en/latest/io/votable/index.html
[^862^] Parquet in Python tutorial - https://dev.to/alexmercedcoder/all-about-parquet-part-08
[^867^] Stack Overflow: Read Parquet to DataFrame - https://stackoverflow.com/questions/33813815
[^868^] Apache Arrow Parquet documentation - https://arrow.apache.org/docs/python/parquet.html
[^913^] Fink/LSST Known Issues - https://doc.lsst.fink-broker.org/data/issues/
[^920^] DESC DC2 DIA Analysis - https://lsstdesc.github.io/DC2-analysis/tutorials/
[^921^] Rubin Alerts & Brokers Community Forum - https://community.lsst.org/c/sci/alertsbrokers/46
[^102^] SNANA Tutorial (KICP 2023) - https://kicp.uchicago.edu/~kessler/SNANA_Tutorial/
[^940^] LSST Alerts landscape - https://indico.in2p3.fr/event/18823/contributions/74200/
[^939^] AAS2RTO: Automated Alert Streams to Real-Time Observations - https://www.aanda.org/articles/aa/full_html/2025/06/aa52099-24/
[^916^] AXS incremental catalog updates - https://iopscience.iop.org/article/10.3847/1538-3881/ab2384
[^719^] BOOM/Babamul broker architecture - https://arxiv.org/html/2511.00164v1
[^933^] Apache Spark broker for astronomy - https://hepsoftwarefoundation.org/gsoc/2019/
[^730^] TOM Toolkit for transient follow-up - https://tom-toolkit.readthedocs.io/
[^940^] LSST data products timeline - https://indico.in2p3.fr/event/18823/
[^51^] Lasair FAQ - https://lasair.readthedocs.io/en/main/more_info/faqs.html
[^44^] Rubin Observatory alert brokers list - https://rubinobservatory.org/for-scientists/data-products/alerts-and-brokers
[^799^] Physics Magazine: Rubin alerts - https://link.aps.org/doi/10.1103/Physics.19.31
[^932^] Rubin Observatory data facts - https://rubinobservatory.org/explore/how-rubin-works/technology/data

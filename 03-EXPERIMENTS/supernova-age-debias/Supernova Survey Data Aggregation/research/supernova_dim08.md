# Dimension 08: Alert Brokers & Real-time ML Infrastructure for Supernova Science

**Date**: 2025-07-25
**Researcher**: AI Agent
**Searches Conducted**: 25+ independent queries across broker documentation, arXiv, GitHub, official sites

---

## Executive Summary

This report provides a comprehensive deep-dive into the seven Rubin Observatory community alert brokers processing ZTF alerts today and preparing for LSST/Rubin operations starting in 2025. Each broker provides unique ML classifications, APIs, and programmatic access patterns suitable for supernova machine learning research. The brokers are: **Fink**, **ALeRCE**, **Lasair**, **AMPEL**, **ANTARES**, **Pitt-Google**, and **Babamul/BOOM**. This document covers data access methods, classification taxonomies, accuracy comparisons, authentication, rate limits, bulk data strategies, and TOM Toolkit integration for follow-up coordination.

---

## Table of Contents

1. [Fink Broker](#1-fink-broker)
2. [ALeRCE Broker](#2-alerce-broker)
3. [Lasair Broker](#3-lasair-broker)
4. [AMPEL Broker](#4-ampel-broker)
5. [ANTARES Broker](#5-antares-broker)
6. [Pitt-Google Broker](#6-pitt-google-broker)
7. [Babamul/BOOM Broker](#7-babamulboom-broker)
8. [Real-time Streams vs Historical Data](#8-real-time-streams-vs-historical-data)
9. [Classification Taxonomies & Accuracy Comparison](#9-classification-taxonomies--accuracy-comparison)
10. [Rate Limits, Authentication & Bulk Data](#10-rate-limits-authentication--bulk-data)
11. [TOM Toolkit Integration](#11-tom-toolkit-integration)
12. [Summary Table](#12-summary-table)

---

## 1. Fink Broker

### 1.1 Overview

Fink is a community-driven astronomical alert broker selected as one of seven full-stream community brokers for the Vera C. Rubin Observatory [^48^]. It has been processing the ZTF public alert stream since November 2019 and has processed over 180 million alerts as of late 2024 [^60^]. Fink is built on Apache Spark and provides a modular platform for science modules, filters, and data redistribution.

**Website**: https://fink-broker.org
**Documentation**: https://doc.lsst.fink-broker.org
**Science Portal (ZTF)**: https://ztf.fink-portal.org
**Science Portal (LSST)**: https://lsst.fink-portal.org
**API Documentation**: https://api.fink-portal.org
**GitHub**: https://github.com/astrolabsoftware

### 1.2 REST API

Fink exposes a comprehensive REST API at `https://api.fink-portal.org/api/v1/<endpoint>` [^679^]. The API uses POST requests with JSON arguments.

**Key Endpoints**:
- `/api/v1/objects` - Query by object ID (e.g., ZTF21aaxtctv)
- `/api/v1/latests` - Query by classification
- `/api/v1/conesearch` - Cone search (replaced deprecated `/explorer`)
- `/api/v1/schema` - Available columns/schema
- `/api/v1/classes` - Available classification classes

**Python Example**:
```python
import requests
import io
import pandas as pd

# Query by object ID
r = requests.post(
    "https://api.ztf.fink-portal.org/api/v1/objects",
    json={
        "objectId": "ZTF21aaxtctv",
        "output-format": "json"
    }
)
pdf = pd.read_json(io.BytesIO(r.content))
```

The API is documented via OpenAPI Specification with an interactive UI at https://api.fink-portal.org [^681^].

**API Transition (January 2025)**: The API URL changed from `https://fink-portal.org/api/v1/` to `https://api.fink-portal.org/api/v1/`. Three endpoints were deprecated: `/xmatch`, `/random`, and `/explorer` [^679^].

### 1.3 Science Portal

The Fink Science Portal is a web application that provides:
- Interactive search by object name, position, classification, date
- Data Transfer service for bulk downloads
- Crossmatch (Xmatch) services
- Visualization tools for light curves and cutouts

The portal is available at both ZTF and LSST URLs and communicates with the backend via the REST API [^681^].

### 1.4 Kafka Client (fink-client)

The `fink-client` is a thin wrapper around Apache Kafka for consuming real-time alert streams [^699^].

**Installation**:
```bash
pip install fink-client --upgrade
```

**Requirements**: Python 3.9+

**Usage**:
```bash
# Consume first available alert
fink_consumer --display -limit 1

# Save alerts to disk (Avro format)
fink_consumer --display --save -outdir alertDB -limit 1

# Continuous consumption
fink_consumer --display --save -outdir alertDB
```

**Key Features**:
- Alerts stored for 4-7 days in the queue, allowing replay
- Supports multiple topic subscriptions
- Schema automatically downloaded from GitHub
- Works with Livestream, Data Transfer, and Xmatch services [^697^]

### 1.5 Data Transfer Service

The Data Transfer service enables massive historical data transfer for building training datasets and performing large-scale analyses [^716^].

**URL**: https://ztf.fink-portal.org/download

**Features**:
- Select observing nights via calendar interface
- Filter by classification class
- Apply custom SQL-like conditions on alert content
- Stream output directly to Kafka topic for consumption
- Supports ZTF and ELAsTiCC simulated data

**Example Conditions**:
```sql
-- Filter by magnitude and distance
candidate.magpsf > 19.5;
candidate.distnr > 2;

-- Filter on ML scores
rf_snia_vs_nonia > 0.5;
snn_snia_vs_nonia > 0.5;
```

### 1.6 Fink Tutorials (GitHub)

The `fink-tutorials` repository contains Jupyter notebooks for exploring Fink data [^60^].

**Repository**: https://github.com/astrolabsoftware/fink-tutorials

**Contents**:
- Notebooks for ZTF and LSST surveys
- REST API usage examples
- Google Colab compatible
- Covers supernovae, microlensing, Solar System objects, GRBs, AGN, anomaly detection

**Requirements**: Python > 3.5 (most notebooks); Python < 3.12 for microlensing notebook

### 1.7 SuperNNova Integration

Fink deploys **SuperNNova (SNN)** - a deep learning framework for supernova classification developed by Möller & de Boissière (2019, 2020) [^729^].

**Models Deployed**:
- **SN1**: Binary classifier (SN Ia vs non-Ia)
- **SN2**: General supernova classification

**Performance**: Trained on simulations from Muthukrishna et al. (2019), tested on ZTF public stream data. Achieves median classification **6 days before observed peak brightness** for SN Ia events [^729^].

**Requirements for Classification**:
- Deep Learning Real/Bogus score `drb > 0.5`
- Cross-match with SIMBAD (galaxy, candidate transient, or unknown)
- At least 3 detections in the alert history
- Classification score > 0.5
- < 400 detections in ZTF survey (to filter variables)
- Star/Galaxy score > 0.4 (SExtractor)

### 1.8 Early SN Ia Classifier with Active Learning

Fink pioneered the first real-time active learning application on survey data for early SN Ia classification [^47^] [^56^] [^726^] [^689^].

**Pipeline**: Feature extraction → Random Forest classification → Active Learning strategy (uncertainty sampling)

**Performance** (averaged over 100 realizations):
- **Purity**: ~89%
- **Efficiency**: ~54%
- **Accuracy**: 0.97 (best model)

**Deployment Results** (Nov 2020 - Oct 2021):
- 535 candidates reported to TNS
- 459 (86%) confirmed as SNe Ia spectroscopically
- Classifier identifies SNe Ia median **6 days before peak brightness** [^729^]

**Active Learning Loop** (2023-2024):
- 177 follow-up candidates identified
- 109 classifications obtained
- After ~60 new objects, AL strategy outperforms random selection
- Saves ~1.5 nights of observation vs 5.3 nights with other approaches [^726^] [^689^]

### 1.9 Fink Science Modules (fink-science)

The `fink-science` package contains all science modules used to generate added values [^686^].

**Installation**:
```bash
pip install fink-science
```

**Latest Version**: 7.4.0 (as of March 2025)

**Modules Include**:
- SuperNNova (supernova classification)
- Early SN Ia (active learning classifier)
- Microlensing (LIA-based)
- Asteroid detection
- Kilova/gamma-ray burst identification
- AGN detection
- Real/Bogus scoring
- CDS cross-matching

---

## 2. ALeRCE Broker

### 2.1 Overview

ALeRCE (Automatic Learning for the Rapid Classification of Events) is a Chilean-led community broker processing ZTF alerts since 2019 and selected as a Rubin community broker [^684^] [^728^]. ALeRCE is known for its hierarchical classification system using both image stamp classifiers and light curve classifiers.

**Website**: https://alerce.science
**Documentation**: https://alerce.readthedocs.io
**GitHub Organization**: https://github.com/alercebroker

### 2.2 Python Client

The `alerce` Python client provides comprehensive access to ALeRCE services [^701^].

**Installation**:
```bash
pip install alerce
```

**GitHub**: https://github.com/alercebroker/alerce_client

**Capabilities**:
- Multi-survey object queries (ZTF, LSST)
- Light curve retrieval
- Classification probabilities
- Stamp (image cutout) access
- Crossmatch searches (cone search, crossmatch, redshift)
- Feature queries
- Magnitude statistics

**Example Usage**:
```python
from alerce.core import Alerce
client = Alerce()

# Query objects with classification
objects = client.query_objects(
    classifier="stamp_classifier",
    class_name="SN",
    probability=0.7
)

# Query light curve
lightcurve = client.query_lightcurve(oid="ZTF20acnsdjd")

# Query probabilities
probs = client.query_probabilities(oid="ZTF20acnsdjd")
```

**API Structure**:
- **Multi-Survey Access**: Unified API for ZTF and LSST data
- **ZTF Access**: Legacy ZTF-specific endpoints
- **Multi-survey Stamps Access**: Image cutout retrieval
- **Crossmatch Access**: Cone search and crossmatch queries

### 2.3 Classification System

ALeRCE uses a **two-level hierarchical classifier** approach [^698^] [^528^]:

**Top Level** (3 classes):
- Transient (SNe, TDE)
- Stochastic (AGN, QSO, Blazar, YSO, CV/Nova)
- Periodic (LPV, RR Lyrae, Cepheid, Eclipsing Binary, δ Scuti, Periodic-Other)

**Second Level - Transient Subclasses**:
- SN Ia (Type Ia supernova)
- SN Ib/c (Type Ib/c supernova)
- SN II (Type II supernova)
- SLSN (Super-Luminous Supernova)
- TDE (Tidal Disruption Event) - added in 2025

### 2.4 Stamp Classifier

The ALeRCE stamp classifier uses a **Convolutional Neural Network** on the first detection image cutouts (science, reference, difference images) plus alert metadata [^685^].

**Performance**:
- ~94% accuracy on balanced test set
- Classes: AGN, SNe, Variable Stars, Asteroids, Bogus
- 70% of reported SNe occurred within 1 day after first detection
- 6,846 SN candidates reported (June 2019 - Feb 2021)
- 971 spectroscopically confirmed [^685^]

### 2.5 Light Curve Classifier

The light curve classifier uses a **Balanced Random Forest (BRF)** with 152 features from ZTF g- and r-band light curves [^698^] [^528^].

**Performance**:
- F1-score: 0.97 (top-level)
- SN completeness: 100%
- Two-level approach outperforms flat classification

**Feature Types**:
- Corrected light curve features (`lc_corr`)
- Difference light curve features (`lc_diff`)
- Parametric model fits (Supernova Parametric Model)
- Color variance features

### 2.6 SN Hunter

SN Hunter is ALeRCE's visualization tool for SN candidate vetting and reporting to TNS [^685^].

### 2.7 ALeRCE GitHub Repositories

The ALeRCE organization maintains 70+ repositories [^728^]:

**Key Repos**:
- `alerce_client`: Python client library
- `pipeline`: ALeRCE processing pipeline monorepo
- `ztf_explorer`: Web-based ZTF data explorer
- `usecases`: Collection of science notebooks (35 notebooks)
- `ATAT`: Astronomical Transformer for time series And Tabular data
- `TNS_upload`: Tools for uploading SN candidates to TNS

---

## 3. Lasair Broker

### 3.1 Overview

Lasair is the UK Community Broker for transient alerts, developed by the LSST:UK consortium [^43^]. It distinguishes itself through SQL-based filtering, Sherlock host galaxy associations, and comprehensive documentation with Jupyter notebooks and video tutorials.

**Website**: https://lasair-ztf.lsst.ac.uk
**Documentation**: https://lasair.readthedocs.io
**GitHub**: https://github.com/lsst-uk/lasair-lsst

### 3.2 SQL-Based Filtering

Lasair's core feature is the ability to build filters using **SQL queries** against a rich database of alert data, cross-matches, and computed features [^43^].

**Filter Features**:
- SQL syntax for complex selections
- Light curve features pre-computed
- Sherlock host galaxy associations
- TNS crossmatching
- Watchlists (specific object lists)
- Watchmaps (spatial regions, MOC-based)
- User-contributed annotations
- Streaming escalation (email or Kafka)

### 3.3 Python Client (`lasair`)

**Installation**:
```bash
pip install lasair
```

**Capabilities** [^43^]:
- Query the Lasair database
- Query Sherlock (host galaxy associations)
- Create annotations
- Consume Kafka streams

**API Authentication**: Requires API token from user profile page [^733^].

```python
BROKERS = {
    'LASAIR': {
        'api_key': os.getenv('LASAIR_API_KEY', ''),
    },
}
```

### 3.4 Sherlock Host Association

Sherlock is Lasair's contextual classification system for transients, cross-matching against extensive astronomical catalogs [^727^] [^732^].

**Catalogs Used**:
- Pan-STARRS1, AllWISE, 2MASS, SDSS
- Million Quasars Catalog v5.2
- Veron-Cetty AGN Catalogue v13
- LASe-GPS (100 Mpc volume-limited galaxy catalog)
- NED-D Galaxy Catalogue

**Classification Types** (7 categories):
1. **VS**: Variable Star (synonym radius match)
2. **CV**: Cataclysmic Variable (synonym radius match)
3. **BS**: Bright Star (association radius)
4. **AGR**: Active Galactic Nucleus (synonym radius match)
5. **NT**: Nuclear Transient (galaxy core synonym match)
6. **SR**: Supernova (galaxy association, non-nuclear)
7. **ORPHAN**: No catalog match

**Synonym Radius**: 1.5 arcsec for Lasair-ZTF

**Sherlock API Access**:
```bash
curl --header "Authorization: Token xxxxxxxxxxxxxxxx" \
     --data "objectIds=ZTF23ableqsp&lite=False" \
     https://lasair-ztf.lsst.ac.uk/api/sherlock/objects/
```

### 3.5 Kafka Streams

Lasair provides Kafka streams for real-time alert delivery [^712^].

**Configuration**:
- Kafka server: `kafka.lsst.ac.uk:9092`
- Python client: `pip install confluent_kafka`
- Topic format: `lasair_<user_id>_<sanitized_filter_name>`
- Messages retained: ~7 days

**Streaming Filter Setup**:
1. Create and save a filter query
2. Click "Settings" and change to "kafka stream"
3. Topic name displayed on filter detail page
4. Use consistent `group_id` to avoid duplicate messages

### 3.6 REST API

Lasair provides a REST API documented at https://lasair.readthedocs.io [^43^].

**Key Features**:
- Object queries
- Sherlock host associations
- Annotation creation
- Kafka stream management
- Jupyter notebook examples in documentation

### 3.7 Lasair Marshall Notebook

Interactive notebook for scanning and vetting transient candidates with rich contextual information [^43^].

---

## 4. AMPEL Broker

### 4.1 Overview

AMPEL (Alert Management, Photometry and Evaluation of Light curves) is a scalable Python framework for processing large astronomical datasets, developed at DESY/Humboldt University [^210^] [^740^]. AMPEL follows a "Code-to-Data" paradigm where users develop analysis pipelines locally and deploy them to a live instance.

**GitHub**: https://github.com/ampelproject, https://github.com/AmpelAstro
**Documentation**: https://ampelproject.github.io/
**Contact**: ampel-info at desy.de

### 4.2 Core Architecture

AMPEL is organized around several key concepts [^740^] [^741^]:

**Tiers**:
- **Tier 0**: Ingestion of alerts/photopoints
- **Tier 1**: State combination (grouping related datapoints)
- **Tier 2**: Analysis units (user-defined computations)
- **Tier 3**: Summary and visualization units

**Channels**: Subset of processes belonging to an individual user. Channels share processing resources to avoid redundant computation.

**Units**: Modular processing components:
- **T0 Units**: Alert consumers/shapers
- **T1 Units**: State combiners
- **T2 Units**: Analysis algorithms (e.g., RunParsnip, RedshiftSampler)
- **T3 Units**: Summary and output generators

### 4.3 Data Structure

AMPEL uses a document-oriented database (MongoDB) with collections [^741^]:

- **Stock**: Each unique object assigned a stock ID, records channels and operations (journal)
- **t0**: Individual measurements (photopoints), immutable bodies with metadata
- **t1**: Object states (information known at a point in time)
- **t2**: Results from analysis units

### 4.4 ELAsTiCC Processing

AMPEL participated in both ELAsTiCC campaigns (2022 and 2023), processing simulated LSST alerts [^334^] [^741^]. The workflow demonstrated:

- Real-time photometric classification using Parsnip and other T2 units
- Modular channel processing for different science cases
- Full provenance tracking with trace IDs
- Reproducible analysis pipelines

### 4.5 Access Methods

**Live Query API**: Requires pre-authorization [^210^]

**Fork/Local Deployment**: AMPEL can be forked and run locally

**GitHub Repositories**:
- `AmpelProject/Ampel-contrib-sample`: Sample contributions
- `AmpelProject/Ampel-HU-astro`: Heidelberg astro-specific units
- Full analysis schemas available as YAML configs

### 4.6 SkyPortal Integration

AMPEL outputs can be configured to feed into SkyPortal for candidate scanning and follow-up coordination (similar to other broker-TOM integrations).

---

## 5. ANTARES Broker

### 5.1 Overview

ANTARES (Arizona-NOIRLab Temporal Analysis and Response to Events System) is the oldest of the Rubin brokers, conceived in 2014 [^210^] [^682^]. It is developed and operated by NSF NOIRLab and has been processing ZTF alerts since 2018.

**Website**: https://antares.noirlab.edu
**GitLab**: https://gitlab.com/nsfnoirlab/csdc/antares/
**Client Docs**: https://nsf-noirlab.gitlab.io/csdc/antares/client/

### 5.2 Python Client (`antares-client`)

**Installation** [^678^]:
```bash
# Base client
pip install antares-client

# With Kafka streaming support
pip install "antares-client[subscriptions]"
```

**Python Requirements**: 3.6+

**Capabilities**:
- Kafka streaming client (StreamingClient)
- HTTP API search
- CLI tool for saving streams locally
- Devkit for filter development

### 5.3 Locus Abstraction

ANTARES uses a **"Locus"** abstraction for time-series data [^682^] [^713^]:

- New alerts are positionally associated with existing Loci within **1 arcsecond**
- Full historical lightcurve available for each Locus
- Multiwavelength crossmatch information attached
- Tags and properties accumulated over time

### 5.4 User-Defined Filters

Filters are Python classes inheriting from `antares.devkit.Filter` [^682^]:

```python
import antares.devkit as dk

class MyFilter(dk.Filter):
    def run(self, locus):
        # Access full locus data: lightcurve, properties, tags
        # Return tags, properties, etc.
        pass
```

**Filter Devkit**: Available in NOIRLab's DataLab Jupyter environment with direct read-only access to ANTARES databases for filter development and testing [^682^].

### 5.5 Searching

**Cone Search** [^714^]:
```python
from antares_client.search import cone_search
from astropy.coordinates import Angle, SkyCoord

center = SkyCoord("20h48m25.1805s 29d45m4.8361s")
radius = Angle("1s")
for locus in cone_search(center, radius):
    pass
```

**Advanced ElasticSearch Queries**:
```python
from antares_client.search import search

query = {
    "query": {
        "bool": {
            "filter": [
                {"range": {"properties.num_mag_values": {"gte": 50, "lte": 100}}},
                {"term": {"tags": "nuclear_transient"}}
            ]
        }
    }
}
for locus in search(query):
    do_something(locus)
```

### 5.6 API and Streams

**HTTP API**: JSON:API compliant, supports partial fetching and resource inclusion [^682^]. No authentication required for API access (planned for future for bookmarked objects).

**Kafka Streams**: Require credentials provided by ANTARES team upon request.

**Slack Notifications**: Real-time alerts for new tagged Loci and Watchkit hits.

### 5.7 Superphot+ Integration

Superphot+ (a parametric supernova classifier) has been integrated as an ANTARES filter [^528^] [^696^]:

- Real-time light curve fitting and classification
- Five SN classes: SN Ia, SN II, SN Ib/c, SN IIn, SLSN-I
- Class-averaged F1-score: 0.61 (without redshift), 0.71 (with redshift)
- Fit parameters saved as locus properties for downstream tasks

### 5.8 RAPID Integration

RAPID (Real-time Automated Photometric Identification) - a deep learning algorithm for exotic transient identification - is integrated into ANTARES [^680^].

---

## 6. Pitt-Google Broker

### 6.1 Overview

The Pitt-Google Broker is a cloud-based alert distribution service running on Google Cloud Platform (GCP) [^687^]. It is designed for near real-time processing of large-scale astronomical surveys.

**Documentation**: https://pitt-broker.readthedocs.io
**Client Docs**: https://mwvgroup.github.io/pittgoogle-client/
**GitHub**: Available via Pitt-Google organization

### 6.2 Access Patterns

Pitt-Google provides three primary data access methods [^738^]:

1. **Pub/Sub Streams**: Real-time message subscription
2. **BigQuery Tables**: Historical data warehouse queries
3. **Cloud Storage**: Avro file archives including cutouts

### 6.3 Pub/Sub Streams

Google Cloud Pub/Sub provides asynchronous publish-subscribe messaging [^688^].

**Setup**:
1. Create GCP project
2. Configure authentication
3. Enable Pub/Sub API
4. Install `pgb-utils`: `pip install pgb-utils`

**Subscribe to Topic**:
```python
import pgb_utils as pgb

# Choose topic and subscription name
topic_name = 'ztf-loop'  # testing stream, 1 alert/sec
subscription_name = 'my-subscription'

# Create subscription
subscription = pgb.pubsub.create_subscription(topic_name, subscription_name)
```

**Pull Messages**:
```python
# Pull messages from subscription
messages = pgb.pubsub.pull(subscription_name, max_messages=100)
```

**Available ZTF Topics** [^372^]:

| Topic | Description |
|-------|-------------|
| `ztf-alerts` | Full ZTF alert stream |
| `ztf-lite` | Lite version (subset of fields) |
| `ztf-tagged` | With basic categorizations ("is pure", "is extragalactic transient") |
| `ztf-SuperNNova` | SuperNNova classification results (Ia vs non-Ia) |
| `ztf-alert_avros` | Notification of new Avro files in Cloud Storage |
| `ztf-loop` | Testing stream (1 alert/sec) |

**Available LSST Topics** [^372^]:

| Topic | Description |
|-------|-------------|
| `lsst-alerts` | Full LSST alert stream |
| Various value-added topics | UPSILoN, variability, SuperNNova results |

### 6.4 BigQuery Access

BigQuery is a petabyte-scale data warehouse for historical queries [^738^].

**ZTF Tables** [^372^]:

| Dataset | Table | Description |
|---------|-------|-------------|
| `ztf` | `alerts_v4_02` | ZTF alerts (all versions available) |
| `ztf` | `SuperNNova` | SuperNNova Ia vs non-Ia classification |

**LSST Tables** [^372^]:

| Dataset | Table | Description |
|---------|-------|-------------|
| `lsst` | `alerts_v10_0` | LSST alert data (excl. cutouts) |
| `lsst` | `supernnova` | SuperNNova classification results |
| `lsst` | `upsilon` | UPSILoN variable star classification |
| `lsst` | `variability` | Stetson J indices and detection counts |

**Python Example**:
```python
from google.cloud import bigquery

client = bigquery.Client()
query = """
    SELECT * FROM `ardent-cycling-243415.ztf.alerts_v4_02`
    WHERE objectId = 'ZTF20acnsdjd'
    LIMIT 10
"""
results = client.query(query)
```

### 6.5 pittgoogle-client

The `pittgoogle-client` is a Python library for accessing Pitt-Google data [^734^].

**API Modules**:
- `pittgoogle.alert`: Alert data structures
- `pittgoogle.auth`: Authentication
- `pittgoogle.bigquery`: BigQuery queries
- `pittgoogle.pubsub`: Pub/Sub streaming
- `pittgoogle.schema`: Alert schemas
- `pittgoogle.types`: Data types

### 6.6 Cloud Storage

Avro files (including cutouts) stored in publicly accessible GCP buckets [^738^].

**ZTF Filename Format**:
```
<schema_version>/kafkaPublishTimestamp=<timestamp>/<objectid_key>=<objectid>/<sourceid_key>=<sourceid>.avro
```

### 6.7 Cost Considerations

Google Cloud Free Tier quotas [^738^]:

| Service | Free Tier | Beyond Free Tier |
|---------|-----------|-----------------|
| BigQuery querying | 1 TB/month | $5.00/TB |
| Pub/Sub message delivery | 10 GB/month | $40/TB |

No billing setup required for tutorials; pay-as-you-go beyond free tier.

---

## 7. Babamul/BOOM Broker

### 7.1 Overview

Babamul is the newest of the seven full-stream Rubin brokers, jointly developed by Caltech and University of Minnesota [^702^] [^719^]. Its unique architecture, called BOOM (Bursts and Outbursts Observation Monitor), is built from scratch in Rust for maximum scalability.

**Website**: https://babamul.caltech.edu
**Documentation**: https://docs.babamul.dev
**GitHub**: https://github.com/boom-astro/boom
**PyPI**: `pip install babamul`

### 7.2 BOOM Architecture

**Key Design Features** [^719^]:

- **Rust Programming Language**: Compiled language for high throughput at LSST scales
- **Multi-survey Processing**: Continuous crossmatch of ZTF and Rubin alert streams
- **Tier-like Worker System**: Independent horizontal scaling of different processing stages
- **Valkey**: In-memory job queue
- **MongoDB**: Database with native spatial querying
- **ONNX Runtime**: Python-trained ML models converted to Rust-compatible format

### 7.3 AppleCiDEr ML Framework

AppleCiDEr is Babamul's multimodal machine learning framework [^718^] [^725^]:

**Modalities**:
1. **Photometry**: [CLS]-Transformer (87.8% accuracy)
2. **Images + Metadata**: AstroMiNN (competitive with BTSbot)
3. **Spectra**: SpectraNeXt-2D (87.6% accuracy)
4. **Ensemble**: AppleCiDEr averages all networks

**Current Integration**: Photometry and image-metadata models (spectra not available in real-time).

### 7.4 Filter System

- **100% customizable filters** by end users
- No-code filter building UI in SkyPortal
- Kafka output for filtered streams
- Static phenomenological filters based on 7+ years of ZTF operations
- Each filter has its own disjoint Kafka topic [^718^]

### 7.5 SkyPortal Integration

BOOM filters are tightly integrated with SkyPortal for candidate scanning and follow-up [^719^]:
- Filter results displayed in SkyPortal candidate interface
- Image cutouts, light curves, metadata visible
- Direct links to external resources
- Automated saving and triggering for spectroscopic follow-up

### 7.6 Deployment

- Docker Compose deployment via GitHub Actions
- Self-sufficient: MongoDB, Kafka, Valkey, BOOM workers included
- Optional Babamul feature layer on top of BOOM [^719^]

---

## 8. Real-time Streams vs Historical Data

### 8.1 Real-time Stream Access

| Broker | Technology | Python Client | Latency | Retention |
|--------|-----------|---------------|---------|-----------|
| Fink | Apache Kafka | `fink-client` | Near real-time | 4-7 days |
| ALeRCE | Kafka | Built into `alerce` | Near real-time | Limited |
| Lasair | Apache Kafka | `confluent_kafka` | Near real-time | ~7 days |
| AMPEL | Internal + Kafka | AMPEL framework | Near real-time | Configurable |
| ANTARES | Apache Kafka | `antares-client[subscriptions]` | Near real-time | Limited |
| Pitt-Google | Google Pub/Sub | `pgb-utils` / `pittgoogle-client` | Near real-time | 7 days |
| Babamul | Apache Kafka | Kafka clients | Near real-time | Configurable |

### 8.2 Historical Data Access

| Broker | Method | Volume | Format | Notes |
|--------|--------|--------|--------|-------|
| Fink | Data Transfer Service | Massive | Kafka stream | Select nights, SQL-like filters |
| Fink | REST API | Limited (~thousands) | JSON/CSV | Full history since 2019 |
| ALeRCE | REST API | Medium | JSON | Object-by-object or bulk lists |
| Lasair | SQL queries | Medium | Various | Rich feature database |
| Lasair | REST API | Medium | JSON | Object queries |
| AMPEL | MongoDB queries | Medium | BSON/JSON | Document-oriented |
| ANTARES | HTTP API + ElasticSearch | Medium | JSON | Full locus history |
| ANTARES | Client search | Medium | Python objects | Cone search, advanced queries |
| Pitt-Google | BigQuery | Massive | Query results | Petabyte-scale warehouse |
| Pitt-Google | Cloud Storage | Massive | Avro files | Including cutouts |
| Babamul | Database queries | Medium | Various | MongoDB + spatial |

### 8.3 Recommended Strategies for ML

**For Training Dataset Construction**:
1. **Fink Data Transfer**: Best for massive historical ZTF downloads. Select specific nights, filter by class, stream to Kafka topic.
2. **Pitt-Google BigQuery**: Best for large-scale SQL-based exploration. Query across full archive with standard SQL.
3. **Pitt-Google Cloud Storage**: Best for accessing full Avro packets including image cutouts.
4. **ALeRCE Client**: Best for targeted object lists with classifications. Query by classifier output, retrieve light curves + probabilities.
5. **Lasair SQL**: Best for complex feature-based selections. Pre-computed light curve features available.

**For Real-time Classification/Inference**:
1. **Fink Kafka**: Subscribe to specific topic (e.g., SN Ia candidates). Process alerts as they arrive.
2. **Pitt-Google Pub/Sub**: Subscribe to pre-filtered streams (e.g., `ztf-SuperNNova` for classified alerts).
3. **ANTARES Filters**: Deploy custom Python filters in the broker pipeline itself.
4. **AMPEL Channels**: Deploy custom T2 analysis units for real-time processing.

---

## 9. Classification Taxonomies & Accuracy Comparison

### 9.1 Classification Taxonomy Comparison

| Broker | Top-Level Classes | SN Subclasses | Non-SN Classes | Key Feature |
|--------|------------------|---------------|----------------|-------------|
| **Fink** | SN, AGN, Variable, Solar System, Microlensing, Anomaly | SN Ia vs non-Ia (SuperNNova) | AGN, CV, YSO, asteroid, etc. | Active Learning for early SN Ia |
| **ALeRCE** | Transient, Stochastic, Periodic (hierarchical) | SN Ia, SN Ib/c, SN II, SLSN, TDE | AGN, QSO, Blazar, YSO, CV, variables | Two-level BRF; stamp + LC classifiers |
| **Lasair** | SN, NT, AGR, VS, CV, BS, ORPHAN (Sherlock) | SN (via host association) | Variable star, AGN, CV, bright star | Sherlock host galaxy association |
| **ANTARES** | User-defined via tags | Via integrated classifiers | Fully customizable | Filter-based tagging system |
| **Pitt-Google** | Extragalactic transient, Pure, etc. | SN Ia vs non-Ia (SuperNNova) | UPSILoN variable classes | Pre-filtered topic streams |
| **Babamul** | Phenomenological filters | Via AppleCiDEr multimodal | Transient, variable, Solar System | Multimodal ML (photometry+images) |
| **AMPEL** | User-defined (channel-based) | Via Parsnip, etc. | Fully customizable | Modular analysis units |

### 9.2 Accuracy Comparison

| Classifier | Broker | Classes | Key Metric | Value | Reference |
|-----------|--------|---------|-----------|-------|-----------|
| **Stamp Classifier (CNN)** | ALeRCE | 5 (AGN, SN, Variable, Asteroid, Bogus) | Accuracy | ~94% | [^685^] |
| **Light Curve Classifier (BRF)** | ALeRCE | 16 (hierarchical) | F1-score (top level) | 0.97 | [^698^] |
| **SN LC Classifier (ALeRCE-SN)** | ALeRCE | 4 (Ia, Ib/c, II, SLSN) | F1-score | 0.62 ± 0.04 | [^528^] |
| **SuperNNova (SN1)** | Fink | 2 (Ia vs non-Ia) | Accuracy (simulations) | >98% | [^726^] |
| **Early SN Ia + Active Learning** | Fink | 2 (Ia vs non-Ia) | Purity | ~89% | [^47^] |
| **Early SN Ia + Active Learning** | Fink | 2 (Ia vs non-Ia) | Efficiency | ~54% | [^47^] |
| **Early SN Ia (deployed)** | Fink | 2 (Ia vs non-Ia) | TNS confirmation rate | 86% (459/535) | [^56^] |
| **Superphot+ (no z)** | ANTARES | 5 (Ia, II, Ib/c, IIn, SLSN-I) | F1-score | 0.61 ± 0.02 | [^528^] |
| **Superphot+ (with z)** | ANTARES | 5 (Ia, II, Ib/c, IIn, SLSN-I) | F1-score | 0.71 ± 0.02 | [^528^] |
| **AppleCiDEr (photometry)** | Babamul | Multi-class | Accuracy | 87.8% | [^718^] |
| **AppleCiDEr (images+meta)** | Babamul | Multi-class | Accuracy (AstroMiNN) | Competitive | [^718^] |
| **AppleCiDEr (spectra)** | Babamul | Multi-class | Accuracy | 87.6% | [^718^] |
| **RAPID** | ANTARES | Exotic transients | Real-time performance | Deployed | [^680^] |

### 9.3 Cross-Broker Agreement

Superphot+ (ANTARES) and ALeRCE light curve classifiers show [^528^]:
- **82 ± 2% agreement** on light curves with spectroscopic labels
- **72% agreement** on light curves without spectroscopic labels
- Superphot+ tends to classify unsure objects as common types (SN Ia or SN II)
- ALeRCE-SN tends to favor SLSN labels for uncertain objects

### 9.4 ELAsTiCC Challenge Results

All seven brokers participated in the Extended LSST Astronomical Time-series Classification Challenge (ELAsTiCC) [^334^] [^210^]:

- **ELAsTiCC 1**: September 2022 - January 2023
- **ELAsTiCC 2**: November - December 2023 (~3x rate)
- All brokers demonstrated classification capability in < 1 day (often < 3 hours)
- Metrics and diagnostics available via DESC TOM

**Important Note**: Direct broker-to-broker performance comparisons are considered a "common misconception" - brokers serve different scientific communities with different goals [^210^].

---

## 10. Rate Limits, Authentication & Bulk Data

### 10.1 Authentication Requirements

| Broker | Registration Required | API Key/Token | Kafka Credentials |
|--------|----------------------|---------------|-------------------|
| **Fink** | Yes (for Kafka) | No (for REST API) | Yes (provided on registration) |
| **ALeRCE** | No | No | Not publicly documented |
| **Lasair** | Yes | Yes (API token) | Yes (via account) |
| **AMPEL** | Yes (pre-authorization) | Yes | Configurable |
| **ANTARES** | No (API); Yes (Kafka) | No (for API) | Yes (request from team) |
| **Pitt-Google** | Yes (GCP project) | GCP service account | GCP authentication |
| **Babamul** | Yes | Yes | Yes |

### 10.2 Rate Limits

**Fink**:
- REST API: Reasonable use policy (not formally documented)
- Kafka: Alerts retained 4-7 days for replay
- Data Transfer: Streamed output, no hard rate limit

**ALeRCE**:
- REST API: Standard HTTP rate limiting
- No published specific limits

**Lasair**:
- Email notifications: Maximum 1 per day per filter
- Kafka: Standard Kafka throughput

**Pitt-Google**:
- BigQuery: 1 TB free tier/month
- Pub/Sub: 10 GB free tier/month
- Pay-as-you-go beyond free tier

### 10.3 Bulk Data Strategies

**Strategy 1: Fink Data Transfer (Recommended for ZTF)**
- Web UI: https://ztf.fink-portal.org/download
- Select date ranges, classes, custom conditions
- Output streamed to Kafka topic
- Poll at your own pace, resume anytime

**Strategy 2: Pitt-Google BigQuery (Recommended for large-scale SQL)**
- Direct SQL queries on full archive
- Export query results to GCP Storage
- Up to 1 TB/month free querying
- Ideal for feature extraction and statistical analyses

**Strategy 3: Pitt-Google Cloud Storage**
- Full Avro packets including cutouts
- Bulk download via gsutil
- File-organized by timestamp and object ID

**Strategy 4: ALeRCE Bulk Queries**
- Query by classifier/class
- Retrieve lists of object IDs
- Batch query light curves and probabilities

**Strategy 5: Lasair SQL Exports**
- Build complex SQL queries with pre-computed features
- Export results via API
- Sherlock associations included

---

## 11. TOM Toolkit Integration

### 11.1 Overview

The TOM (Target and Observation Manager) Toolkit is a Django-based framework for managing astronomical observing projects [^733^] [^680^]. It provides broker modules for ingesting alerts from multiple brokers.

**Documentation**: https://tom-toolkit.readthedocs.io
**Example TOMs**: SNEx, Asteroid Tracker, Microlensing TOM (MOP), Black Hole TOM (BHTOM), ALeRCE TOM [^683^]

### 11.2 Built-in Broker Modules

The TOM Toolkit includes built-in broker classes [^733^]:

**ALeRCE**:
```python
TOM_ALERT_CLASSES = [
    'tom_alerts.brokers.alerce.ALeRCEBroker',
]
```
- `fetch_alerts()`: Paginated alert retrieval
- `fetch_alert(alert_id)`: Single alert details

**Lasair**:
```python
TOM_ALERT_CLASSES = [
    'tom_alerts.brokers.lasair.LasairBroker',
]
```
- Requires `LASAIR['api_key']` in settings
- Query format: https://lasair.readthedocs.io

**ANTARES**:
```python
# Requires separate install: tom_antares
TOM_ALERT_CLASSES = [
    'tom_alerts.brokers.antares.ANTARESBroker',
]
```
- Known compatibility: `antares-client` requires `librdkafka` for Python 3.10+

### 11.3 Plugin Broker Modules

**Fink** (`tom-fink`) [^737^] [^739^]:
```bash
pip install tom-fink
```
```python
TOM_ALERT_CLASSES = [
    'tom_fink.fink.FinkBroker',
]
```
- Search by: Object ID, Cone Search, Date, Class, Solar System name
- Note: Database updated once daily (not live)
- Kafka livestream integration planned

**Hermes** (`tom-hermes`):
```bash
pip install tom-hermes
```
- Messaging service blending human and machine-readable information

### 11.4 TOM Development Program

Las Cumbres Observatory runs a TOM Development Program supporting supernova science [^680^]:
- Rapid follow-up of young SNe
- Streamlined broker-TOM-observatory pipelines
- Automatic triggering through AEON queuing system
- Coordinated multi-facility follow-up

### 11.5 SAGUARO TOM

SAGUARO (Searches After Gravitational waves Using ARizona Observatories) demonstrates a production TOM with [^513^]:
- ML classification integration
- Web-based target prioritization
- Photometric, contextual, and host galaxy aggregation
- Full broker integration for alert ingestion

### 11.6 Follow-up Coordination Workflow

**Typical Broker-TOM-Follow-up Pipeline**:
1. **Alert Detection**: Survey (ZTF/Rubin) detects transient
2. **Broker Processing**: ML classification, cross-matching, feature computation
3. **Filter Matching**: User-defined filters identify interesting events
4. **TOM Ingestion**: Broker module pushes alerts to TOM database
5. **Vetting**: Scientists review candidates in TOM interface
6. **Observation Request**: TOM submits requests to observatories (LCO, SOAR, Gemini, etc.)
7. **Data Reduction**: Follow-up data ingested back into TOM
8. **Analysis**: Light curve fitting, classification refinement

---

## 12. Summary Table

| Broker | Language | Primary Access | ML Classifiers | SN Taxonomy | Kafka | BigQuery | Cloud | GitHub |
|--------|----------|---------------|----------------|-------------|-------|----------|-------|--------|
| **Fink** | Python/Spark | REST API + Kafka | SuperNNova, Active Learning, RF | Ia vs non-Ia + subclasses | Yes | No | No | Yes |
| **ALeRCE** | Python | Python client + REST API | CNN (stamp), BRF (LC) | Ia, Ib/c, II, SLSN, TDE | Yes | No | No | Yes |
| **Lasair** | Python/SQL | SQL + Python client + Kafka | Sherlock associations | SN, NT, AGR, VS, CV, ORPHAN | Yes | No | No | Yes |
| **AMPEL** | Python | API + Local deploy | Parsnip, user-defined | User-defined | Yes | No | No | Yes |
| **ANTARES** | Python | Python client + HTTP API | RAPID, Superphot+ | User-defined (tags) | Yes | No | No | Yes (GitLab) |
| **Pitt-Google** | Python | Pub/Sub + BigQuery + Storage | SuperNNova, UPSILoN | Ia vs non-Ia, variables | Pub/Sub | Yes | GCP | Yes |
| **Babamul** | Rust | Kafka + API | AppleCiDEr (multimodal) | Phenomenological filters | Yes | No | No | Yes |

---

## 13. Recommendations for ML Projects

### 13.1 For Supernova Classification Training

1. **Primary Data Source**: Fink Data Transfer service for massive ZTF historical data with SuperNNova classifications
2. **Supplementary Labels**: ALeRCE for hierarchical classifications (stamp + light curve) with 16-class taxonomy
3. **Host Galaxy Info**: Lasair Sherlock for contextual classifications and host galaxy associations
4. **Alternative Features**: Pitt-Google BigQuery for SQL-based feature extraction from full archive
5. **Spectroscopic Labels**: Cross-match with TNS via any broker's crossmatch service

### 13.2 For Real-time Supernova Detection

1. **Fink**: Subscribe to `rf_snia_vs_nonia > 0.5` or `snn_snia_vs_nonia > 0.5` topics
2. **Pitt-Google**: Subscribe to `ztf-SuperNNova` topic for pre-classified alerts
3. **ALeRCE**: Query stamp classifier for early detection (70% within 1 day)
4. **ANTARES**: Deploy custom Superphot+ filter for 5-class SN classification
5. **Babamul**: Subscribe to SN-specific phenomenological filters

### 13.3 For Follow-up Coordination

1. Set up **TOM Toolkit** with broker modules (Fink, ALeRCE, Lasair, ANTARES)
2. Configure filters for high-purity SN candidate selection
3. Integrate with **AEON** for automatic observation scheduling
4. Use **SkyPortal** (via Babamul/BOOM) for candidate scanning and vetting

### 13.4 For Anomaly Detection

1. **Fink**: Anomaly detection module available; outlier scoring on all alerts
2. **ALeRCE**: Use confidence scores from hierarchical classifier as anomaly indicators
3. **ANTARES**: Deploy custom filters for outlier identification
4. **AMPEL**: Build custom T2 units for anomaly scoring with full provenance

---

## 14. Areas Warranting Deeper Investigation

1. **LSST Transition Status**: All brokers are transitioning from ZTF to LSST. API stability and data formats may change during this period. Monitor broker documentation for updates.

2. **ELAsTiCC2 Detailed Metrics**: While participation was confirmed, detailed per-broker classification accuracy metrics on the ELAsTiCC2 dataset would be valuable for direct comparison. Access requires DESC TOM login.

3. **Cross-Broker Classification Correlation**: A systematic study comparing classifications for the same objects across multiple brokers would help identify strengths/weaknesses of each system.

4. **Babamul Production Readiness**: As the newest broker, Babamul's production stability and data access APIs are still evolving. The Rust-based approach is unique but may have fewer community tools.

5. **AMPEL Documentation Accessibility**: AMPEL's Code-to-Data paradigm is powerful but has a steeper learning curve. More public tutorials and example notebooks would lower the barrier.

6. **Rate Limit Documentation**: Most brokers do not publish explicit rate limits for their APIs. Users should monitor their usage and contact broker teams if planning large-scale queries.

7. **SuperNNova Model Versions**: Fink and Pitt-Google both deploy SuperNNova, but model versions and training data may differ. Clarifying which models are in production would help reproducibility.

8. **TOM Toolkit Kafka Integration**: Currently, most TOM broker modules use REST APIs (polling). Full Kafka integration for real-time streaming into TOMs is still being developed.

9. **Cost Projections for LSST Scale**: With LSST producing ~10 million alerts/night, cost projections for BigQuery querying, Pub/Sub message delivery, and storage will be important for budget planning.

10. **Inter-Broker Data Sharing**: Protocols for sharing classifications and annotations between brokers (e.g., Lasair's annotation system) could enable ensemble classification approaches.

---

## References

[^48^] Fink broker introduction, LSST Community Forum, https://community.lsst.org/t/an-introduction-to-fink/10653
[^56^] Leoni et al. 2022, "Fink: Early supernovae Ia classification using active learning," A&A, https://www.aanda.org/articles/aa/full_html/2022/07/aa42715-21/aa42715-21.html
[^60^] Fink Tutorials GitHub, https://github.com/astrolabsoftware/fink-tutorials
[^210^] Sánchez-Sáez et al., "An overview of astronomical transient brokers in Rubin era," Contributions of the Astronomical Observatory Skalnate Pleso, https://www.astro.sk/caosp/Eedition/FullTexts/vol55no2/pp95-105.pdf
[^334^] DESC ELAsTiCC Challenge, https://portal.nersc.gov/cfs/lsst/DESC_TD_PUBLIC/ELASTICC/
[^43^] Smith et al. 2024, "Enabling Science from the Rubin Alert Stream with Lasair," arXiv:2404.08315, https://arxiv.org/html/2404.08315v1
[^334^] DESC ELAsTiCC, https://portal.nersc.gov/cfs/lsst/DESC_TD_PUBLIC/ELASTICC/
[^47^] Leoni et al. 2021, "Fink: early supernovae Ia classification using active learning," arXiv:2111.11438, https://arxiv.org/abs/2111.11438
[^528^] de Soto et al. 2024, "Superphot+: Real-time Fitting and Classification of Supernova Light Curves," ApJ, https://iopscience.iop.org/article/10.3847/1538-4357/ad6a4f
[^679^] Fink Science Portal v6, https://fink-broker.org/news/2025-01-30-fink-portal-v6/
[^680^] Las Cumbres Observatory TOM Development Program, https://lco.global/tomtoolkit/tom-development-program/
[^681^] Fink Getting Started API Documentation, https://doc.ztf.fink-broker.org/en/latest/services/search/getting_started/
[^682^] Matheson et al. 2021, "The ANTARES Astronomical Time-domain Event Broker," AJ, https://aimg8.dlssyht.cn/u/2211169/ueditor/file/1106/2211169/1673795324660302.pdf
[^683^] TOM Toolkit Example TOMs, https://tom-toolkit.readthedocs.io/en/stable/examples.html
[^684^] Carrasco-Davis et al. 2021, "Alert Classification for the ALeRCE Broker System," ApJ, https://inspirehep.net/literature/1810969
[^685^] Carrasco-Davis et al. 2021, "Alert classification for the ALeRCE broker system: The real-time stamp classifier," A&A, https://pure.uai.cl/en/publications/alert-classification-for-the-alerce-broker-system-the-real-time-s/
[^686^] fink-science PyPI, https://pypi.org/project/fink-science/
[^687^] Pitt-Google Broker Documentation, https://pitt-broker.readthedocs.io/en/troy/
[^688^] Pitt-Google Pub/Sub Streams, https://pitt-broker.readthedocs.io/en/troy/access-data/pubsub.html
[^689^] Fink Active Learning Loop, https://fink-broker.org/news/2025-05-12-al-loop/
[^696^] de Soto et al. 2024, "Realtime Fitting and Classification of Supernova Light Curves," arXiv:2403.07975, https://arxiv.org/abs/2403.07975
[^697^] Fink Livestream Documentation, https://doc.ztf.fink-broker.org/en/latest/services/livestream/
[^698^] Sánchez-Sáez et al. 2025, "ALeRCE light curve classifier: Tidal disruption event expansion pack," A&A, https://www.aanda.org/articles/aa/full_html/2025/04/aa51951-24/aa51951-24.html
[^699^] Fink Client Documentation, https://doc.ztf.fink-broker.org/en/latest/services/fink_client/
[^700^] SkyPortal Fink Client, https://skyportal-fink-client.readthedocs.io/
[^701^] ALeRCE Python Client Documentation, https://alerce.readthedocs.io/
[^702^] Babamul & BOOM, ZTF Website, https://www.ztf.caltech.edu/ztf-boom-babamul.html
[^712^] Lasair Alert Streams Documentation, https://lasair.readthedocs.io/en/main/core_functions/alert-streams.html
[^713^] LSST DMTN-226 (ANTARES), https://dmtn-226.lsst.io/DMTN-226.pdf
[^714^] ANTARES Client Searching Tutorial, https://nsf-noirlab.gitlab.io/csdc/antares/client/tutorial/searching.html
[^716^] Fink Data Transfer Service, https://doc.ztf.fink-broker.org/en/latest/services/data_transfer/
[^718^] Coughlin et al. 2025, "Babamul & BOOM," NASA TDAMM Workshop, https://assets.science.nasa.gov/content/dam/science/astro/programs/physics-of-the-cosmos/events/2025/fourth-tdamm-workshop/presentations/oct-27/Coughlin-brokers.pdf
[^719^] du Laz et al. 2025, "BOOM and Babamul: a real-time, multi-survey, optical alert broker system operating at scale," arXiv:2511.00164, https://arxiv.org/html/2511.00164v1
[^725^] Junell et al. 2025, AppleCiDEr multimodal framework (referenced in BOOM paper)
[^726^] Möller et al. 2025, "Enhancing early SN Ia classification with the Fink broker," PASA, https://resolve.cambridge.org/core/journals/publications-of-the-astronomical-society-of-australia/article/abs/realtime-active-learning-for-optimised-spectroscopic-followup/ABC7EA3CD2CF37C28535BF7F07133A29
[^727^] Smith et al. 2024, "Enabling Science from the Rubin Alert Stream with Lasair" (Sherlock details), https://arxiv.org/pdf/2404.08315
[^728^] ALeRCE GitHub Organization, https://github.com/alercebroker
[^729^] Möller et al. 2021, "Fink, a new generation of broker for the LSST community," CNRS HAL, https://cnrs.hal.science/hal-03045627/file/2009.10185.pdf
[^732^] Host galaxy association for ZTF alerts in Lasair, LSST Community, https://community.lsst.org/t/host-galaxy-association-for-ztf-alerts-in-lasair/9582
[^733^] TOM Toolkit Broker Documentation, https://tom-toolkit.readthedocs.io/en/stable/api/tom_alerts/brokers.html
[^737^] TOM Fink Documentation, https://doc.ztf.fink-broker.org/en/latest/services/tom_fink/
[^739^] tom-fink PyPI, https://pypi.org/project/tom-fink/0.4.2/
[^740^] Nordin et al. 2019, "AMPEL: alert management, photometry, and evaluation of light curves," A&A 631, A147, https://iris.unife.it/retrieve/700ea07c-a5b0-4b16-884b-15f12dc95c90/1904.05922.pdf
[^741^] Feindt et al. 2025, "AMPEL workflows for LSST: Modular and reproducible real-time photometric classification," A&A, https://www.aanda.org/articles/aa/full_html/2025/06/aa52481-24/aa52481-24.html
[^372^] Pitt-Google Data Listings, https://mwvgroup.github.io/pittgoogle-client/listings.html
[^734^] pittgoogle-client Documentation, https://mwvgroup.github.io/pittgoogle-client/
[^738^] Pitt-Google Data Overview, https://pitt-broker.readthedocs.io/en/u-tjr-workingnotes/access-data/data-overview.html
[^678^] antares-client PyPI, https://pypi.org/project/antares-client/
[^513^] SAGUARO TOM Abstract, Caltech rapid-hotwiring2026, https://conference.ipac.caltech.edu/rapid-hotwiring2026/abstracts
[^44^] Rubin Observatory Alerts and Brokers, https://rubinobservatory.org/for-scientists/data-products/alerts-and-brokers
[^700^] SkyPortal Fink Client Documentation, https://skyportal-fink-client.readthedocs.io/
[^684^] Carrasco-Davis et al. 2021, "Alert Classification for the ALeRCE Broker System," INSPIRE, https://inspirehep.net/literature/1810969
[^685^] Carrasco-Davis et al. 2021, ALeRCE stamp classifier, A&A, https://pure.uai.cl/en/publications/alert-classification-for-the-alerce-broker-system-the-real-time-s/
[^698^] Sánchez-Sáez et al. 2025, ALeRCE light curve classifier TDE expansion, A&A, https://www.aanda.org/articles/aa/full_html/2025/04/aa51951-24/aa51951-24.html

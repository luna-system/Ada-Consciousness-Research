## Facet: Data Archives, Catalogs & Aggregator Platforms

**Research Date**: 2026-06-09  
**Searches Performed**: 15+ independent search queries  
**Sources Consulted**: Official documentation, GitHub repos, arXiv preprints, ADS, peer-reviewed papers, project websites

---

### Key Findings

This research identifies **20+ platforms** that aggregate, archive, or broker supernova data for ML workflows. The landscape spans from centralized archives (NASA HEASARC, CDS/SIMBAD/VizieR), open catalogs (Open Supernova Catalog, Astrocats), real-time alert brokers (ALeRCE, Fink, Lasair, ANTARES, AMPEL, Pitt-Google), and specialized repositories (WISeREP, TNS). Several Python packages (sncosmo, SuperNNova, snmachine, parsnip) provide programmatic data access and ML-ready processing pipelines. The Rubin Observatory era (begun February 2026) has catalyzed a new generation of alert brokers that process millions of alerts nightly and expose ML classifications via APIs.

---

### Platform Catalog (detailed per platform)

---

#### 1. Open Supernova Catalog (OSC) / AstroCats

| Attribute | Details |
|-----------|---------|
| **URL** | https://sne.space (web); https://github.com/astrocatalogs (data) |
| **Description** | The largest open repository of supernova metadata, light curves, and spectra. Aggregates data from dozens of sources including individual papers, WISeREP, SDSS, SNLS, PS1, OGLE, Gaia, and more. Contains 50,000+ supernova candidates [^86^][^89^]. |
| **Data Volume** | ~50,000+ SNe; 12,000+ with >10 photometric observations; 5,000+ with spectra [^81^] |
| **Format** | Individual JSON files per SN (human- and machine-readable); tarball downloads available [^89^] |
| **Access Method** | (1) GitHub repos (per-year: sne-pre-1990, sne-1990-1999, sne-2000-2004, sne-2005-2009, sne-2010-2014, sne-2015-2019, sne-2020-2024); (2) Bulk tarball at http://snad.space/osc/sne.tar.lzma; (3) Web interface at sne.space; (4) Python astrocats import scripts |
| **Update Frequency** | Daily automated rebuild [^86^] |
| **Registration** | None required for download |
| **Special Features** | - Aggregated from 50+ sources with bibliography tracking<br>- Daily automated rebuild<br>- Git version control enables reproducibility<br>- Open contribution via git<br>- All data in hierarchical JSON per SN object |
| **ML Readiness** | High. JSON format is easily parsed. Large labeled dataset. Commonly used for photometric classification studies (e.g., Pruzhinskaya+ 2019 anomaly detection study used 45,162 objects [^81^]). |
| **Rate Limits** | None (GitHub) |
| **Example Code** | ```bash
# Clone and import
git clone https://github.com/astrocatalogs/astrocats.git
cd astrocats
git clone https://github.com/astrocatalogs/supernovae.git
python -m astrocats supernovae import

# Or download pre-built tarball
wget http://snad.space/osc/sne.tar.lzma
``` |

**Relevant Papers**: Guillochon et al. (2017) ApJ 835, 64 [^86^]; Pruzhinskaya et al. (2019) MNRAS 489, 3591 [^81^]

---

#### 2. Transient Name Server (TNS)

| Attribute | Details |
|-----------|---------|
| **URL** | https://www.wis-tns.org |
| **Description** | The official IAU hub for discovery and classification reporting of extragalactic transients. Contains photometry, spectra, and classifications for all reported SNe. Central broker for spectroscopic confirmations. |
| **Data Volume** | All classified SNe since 2016; daily CSV contains all public objects |
| **Format** | CSV, TSV, JSON (via API); daily bulk CSV |
| **Access Method** | (1) Search page with CSV export; (2) Daily CSV staging at `tns_public_objects.csv.zip`; (3) API for search/get object details; (4) Bulk API for automated reporting [^28^][^32^][^34^] |
| **Update Frequency** | Real-time for discoveries; daily CSV updated with hourly deltas |
| **Registration** | Required (free) for API access; bot registration for bulk API |
| **Special Features** | - Official discovery/classification hub<br>- Cross-matched with WISeREP (spectra auto-ingested)<br>- AstroNotes for object-related notifications<br>- Daily public CSV + delta files<br>- Sandbox environment for API testing |
| **ML Readiness** | High. Daily CSV enables local management. JSON API returns photometry and spectra. Commonly used for training set construction (e.g., Fink early SN Ia classifier used TNS cross-match for 23,840 alerts [^56^]). |
| **Rate Limits** | API requires User-Agent header and api_key; bulk download via curl |
| **Example Code** | ```bash
# Download daily CSV
curl -X POST \
  -H 'user-agent: tns_marker({"tns_id":YOUR_BOT_ID,"type":"bot","name":"YOUR_BOT_NAME"})' \
  -d 'api_key=YOUR_API_KEY' \
  https://www.wis-tns.org/system/files/tns_public_objects/tns_public_objects_20220112.csv.zip

# Search classified SNe (scripted)
# https://www.wis-tns.org/search?&classified_sne=1&num_page=100&format=csv&page=0

# Get object details (JSON)
# POST {"objname":"", "objid":"", "photometry":"1", "spectra":"1"}
``` |

**Relevant Papers**: TNS documentation [^28^]; Fink early SN Ia classification paper [^56^]

---

#### 3. VizieR / CDS (Centre de Données astronomiques de Strasbourg)

| Attribute | Details |
|-----------|---------|
| **URL** | https://vizier.cds.unistra.fr |
| **Description** | The most complete library of published astronomical catalogs (~24,000 catalogs as of August 2023). Hosts numerous supernova catalogs from published papers [^29^]. |
| **Supernova Catalogs** | - II/189: List of supernovae (81 rows); Galactic SNR catalog (VII/297); Open SN Catalog anomaly detection (J/MNRAS/489/3591); SDSS SN catalog (II/333); PS1 Medium Deep Survey; Foundation DR1; and many more |
| **Data Volume** | Varies by catalog; thousands of SNe across all hosted catalogs |
| **Format** | VOTable, FITS, CSV, TSV, ASCII; TAP/ADQL queries return VOTable |
| **Access Method** | (1) Web search interface; (2) TAP service (Table Access Protocol); (3) astroquery.vizier Python package; (4) FTP bulk download of catalog files |
| **Update Frequency** | Continuous as new papers are published |
| **Registration** | None required |
| **Special Features** | - VO-compatible (TAP/ADQL); Cross-matching tools; Cross-identification with SIMBAD; CDS cross-match service; catsHTM for fast cone searches |
| **ML Readiness** | High. TAP queries can be scripted. astroquery.vizier provides programmatic access. Standard VOTable output easily parsed with astropy. |
| **Rate Limits** | Fair use policy; TAP queries may have timeout limits |
| **Example Code** | ```python
from astroquery.vizier import Vizier
import astropy.units as u

# Query supernova catalogs
v = Vizier(columns=['*'], row_limit=-1)
cats = v.find_catalogs('supernova')

# Cone search around position
result = v.query_region('SN 2011fe', radius=0.1*u.deg)

# TAP ADQL query (pyvo)
import pyvo
tap = pyvo.dal.TAPService('http://tapvizier.u-strasbg.fr/TAPVizieR/tap')
query = """SELECT * FROM \"II/189/list\" WHERE Vmag < 18"""
results = tap.search(query)
``` |

**Relevant Papers**: Ochsenbein et al. (2000) A&AS 143, 23 [^29^]

---

#### 4. SIMBAD (Set of Identifications, Measurements and Bibliography for Astronomical Data)

| Attribute | Details |
|-----------|---------|
| **URL** | https://simbad.cds.unistra.fr |
| **Description** | The reference database for astronomical objects beyond the Solar System. Contains 19+ million objects including supernovae, SN remnants, and related transients. Maintained by CDS [^93^]. |
| **Data Volume** | 19+ million total objects; supernovae typed as SN* in the otypes system |
| **Format** | VOTable, CSV, ASCII, TAP/ADQL; Python via astroquery |
| **Access Method** | (1) Web interface; (2) TAP service at `simbad.cds.unistra.fr/simbad/sim-tap`; (3) astroquery.simbad Python package; (4) Script output via URL [^93^] |
| **Update Frequency** | Continuous |
| **Registration** | None required |
| **Special Features** | - TAP ADQL full SQL-like syntax; Cross-identifications across catalogs; Bibliography links; Object type ontology (SN*, SNR, etc.); astroquery integration |
| **ML Readiness** | High. Standard TAP/ADQL interface. Commonly used for cross-matching training labels (e.g., Fink used SIMBAD cross-match for 5,004,378 alerts [^56^]). |
| **Example Code** | ```python
from astroquery.simbad import Simbad
import astropy.units as u

# Query supernovae by object type
Simbad.add_votable_fields('otype', 'rvz_redshift')
result = Simbad.query_region('M101', radius=0.5*u.deg)

# TAP query
import pyvo
tap = pyvo.dal.TAPService('https://simbad.cds.unistra.fr/simbad/sim-tap')
query = """SELECT main_id, otype, ra, dec FROM basic WHERE otype = 'SN*' LIMIT 1000"""
results = tap.search(query)
``` |

---

#### 5. NASA HEASARC (High Energy Astrophysics Science Archive Research Center)

| Attribute | Details |
|-----------|---------|
| **URL** | https://heasarc.gsfc.nasa.gov |
| **Description** | NASA's primary archive for high-energy astrophysics and CMB data, holding 100+ TB of data from 40+ missions. Hosts several supernova-related catalogs (SN remnants, X-ray SNe) and provides multiwavelength cross-matching capabilities [^26^][^30^]. |
| **Supernova Data** | - SN-related X-ray catalogs; SN remnant catalogs; CMB data; Multi-mission archival data for individual SNe |
| **Data Volume** | 100+ TB total archive |
| **Format** | FITS (standard); TDAT format for catalogs; VOTable via TAP |
| **Access Method** | (1) Web portal (XAMIN); (2) TAP service; (3) astroquery.heasarc; (4) AWS Open Data (`s3://nasa-heasarc/`); (5) wget/curl direct FTP; (6) Classic Browse [^30^][^37^] |
| **Update Frequency** | Mission-dependent; continuous for active missions |
| **Registration** | None required |
| **Special Features** | - Multi-mission data (Swift, Chandra, Fermi, NuSTAR, XMM-Newton, etc.); SkyView all-sky imaging; AWS S3 direct access (no account needed); astroquery integration; Bibliography tracking [^37^] |
| **ML Readiness** | Medium. Primarily X-ray data. AWS S3 access enables bulk downloads for ML. FITS format standard. |
| **Example Code** | ```python
from astroquery.heasarc import Heasarc
heasarc = Heasarc()

# Query catalogs
tables = heasarc.query_mission_list()

# Query specific SN-related catalog
results = heasarc.query_object('SN 2011fe', mission='swiftmastr')

# AWS S3 access
# aws s3 ls --no-sign-request s3://nasa-heasarc/swift/data/obs/
``` |

**Relevant Papers**: Shrader et al. (2018) AAS 232, 214.07 [^36^]

---

#### 6. WISeREP (Weizmann Interactive Supernova Data Repository)

| Attribute | Details |
|-----------|---------|
| **URL** | https://www.wiserep.org |
| **Description** | The premier archive of high-quality supernova spectra. Serves as a general data repository for SNe, transients, CVs, novae, AGNs. Hosts both observed and synthetic/computed spectra [^113^][^117^]. |
| **Data Volume** | >20,000 spectra (historically 8,000+ at inception, now significantly grown); >5,000 public spectra |
| **Format** | ASCII spectra files; CSV/TSV/JSON metadata; FITS |
| **Access Method** | (1) Object search page; (2) Spectra search page with bulk download; (3) API (JSON/TSV bulk reports); (4) Scripted URL queries with pagination; (5) WISeWEBSpider for automated scraping [^116^][^118^] |
| **Update Frequency** | Real-time as users contribute; TNS classified objects auto-migrated |
| **Registration** | Optional for public data; required for proprietary data access and bulk API; group membership for survey data |
| **Special Features** | - Interactive spectral line identification; Redshift and velocity measurement tools; Blackbody fitting (iFigure); NGSF template matching online; Overplotting of multiple spectra; Proprietary data sharing groups; Bulk download via parameterized URLs [^116^] |
| **ML Readiness** | High. Bulk metadata download in CSV/TSV/JSON. Direct spectrum file download. Sample codes for API in Python. Commonly used for spectroscopic classification training [^113^][^147^]. |
| **Example Code** | ```bash
# Bulk download metadata + spectra (paginated)
for page in {0..N}; do
  curl "https://wiserep.org/search/spectra?&type_family=1&format=tsv&files_type=ascii&num_page=100&page=${page}"
done

# Python sample code available at: https://www.wiserep.org/content/wiserep-getting-started
``` |

**Relevant Papers**: Yaron & Gal-Yam (2012) PASP 124, 668 [^113^]

---

#### 7. ALeRCE (Automatic Learning for the Rapid Classification of Events)

| Attribute | Details |
|-----------|---------|
| **URL** | https://science.alerce.online; GitHub: https://github.com/alercebroker |
| **Description** | Chilean-led LSST community broker. Provides ML classification across a broad taxonomy (15+ classes). Has reported 6,162 SN candidates to TNS, of which 883 spectroscopically classified. Classified 1.1 million objects [^59^]. |
| **Data Volume** | 1.1M+ classified objects; full ZTF stream processed; now processing Rubin alerts |
| **Format** | JSON, Pandas DataFrame, VOTable; Avro alert packets |
| **Access Method** | (1) Python client (`pip install alerce`); (2) REST API; (3) Direct database queries; (4) Rubin Science Platform integration; (5) Web portal dashboards [^151^][^153^] |
| **Update Frequency** | Real-time (alert-driven); historical data available |
| **Registration** | None for public data |
| **Special Features** | - Multi-survey support (ZTF + LSST); Light curve classifier + Stamp classifier; catsHTM cross-matching; Watchlist system; Supernova early identification and TNS reporting; Returns detections, non-detections, forced photometry |
| **ML Readiness** | Very High. Purpose-built for ML. Provides classification probabilities, features, light curves, stamps. Python client returns pandas DataFrames directly [^151^]. |
| **Example Code** | ```python
from alerce.core import Alerce
client = Alerce()

# Query SN objects
ztf_objects = client.query_objects(
    survey="ztf", classifier="lc_classifier",
    class_name="SN", probability=0.8, format="pandas"
)

# Get light curve (detections + non-detections)
lc = client.query_lightcurve(oid="ZTF18abbuksn", survey="ztf", format="json")

# Get detections only
detections = client.query_detections(oid="ZTF18abbuksn", survey="ztf", format="pandas")

# Cone search crossmatch
cone = client.catshtm_conesearch(ra=10.0, dec=20.0, radius=1000, catalog="GAIA/DR1")
``` |

**Relevant Papers**: Förster et al. (2021) AJ 161, 242 [^59^]; Sánchez-Sáez et al. (2021)

---

#### 8. Fink Broker

| Attribute | Details |
|-----------|---------|
| **URL** | https://fink-broker.org; Science Portal: https://fink-portal.org; LSST portal: https://lsst.fink-portal.org |
| **Description** | Community-driven broker for Rubin/LSST. Processes ZTF since Nov 2019; began processing Rubin alerts Feb 2026. >180 million ZTF alerts processed as of Nov 2024. Provides ML classifications for SNe, kilonovae, microlensing, AGN, GRBs, anomaly detection [^46^][^48^][^60^]. |
| **Data Volume** | 180M+ ZTF alerts processed; 15M+ accessible via Science Portal; now processing Rubin |
| **Format** | JSON (REST API); Avro (alerts); Parquet (internal); CSV export |
| **Access Method** | (1) REST API (`api.ztf.fink-portal.org`); (2) Science Portal web UI; (3) Kafka streams (fink-client); (4) TOM Toolkit module; (5) fink-tutorials notebooks; (6) Data Transfer service [^48^][^52^][^60^][^173^] |
| **Update Frequency** | Real-time; all data stored for full survey duration |
| **Registration** | None for web/API; registration for Kafka streams |
| **Special Features** | - Active learning for SN Ia classification; SuperNNova deep learning classifier; Anomaly detection module; Multi-messenger (GW, neutrino) cross-match; Cross-match with SIMBAD, TNS, Gaia, PanSTARRS; Science modules contributed by community |
| **ML Readiness** | Very High. Provides classified samples with probabilities. SuperNNova (RNN-based) integrated. Active learning demonstrated 89% purity, 54% efficiency on early SN Ia [^47^][^56^]. Fink-tutorials repo contains ML notebooks [^60^]. |
| **Example Code** | ```python
import requests
import pandas as pd

# Fink REST API
r = requests.post('https://api.ztf.fink-portal.org/api/v1/objects',
    json={'objectId': 'ZTF18abbuksn', 'output-format': 'json'})
data = r.json()

# Or use fink-client for Kafka streams
# pip install fink-client
# Docs: https://github.com/astrolabsoftware/fink-client

# Tutorials: https://github.com/astrolabsoftware/fink-tutorials
``` |

**Relevant Papers**: Möller et al. (2021) MNRAS 501, 3272 [^55^]; Leoni et al. (2022) A&A 663, 170 [^56^]; Fink white paper (arXiv:2009.10185) [^167^]

---

#### 9. Lasair

| Attribute | Details |
|-----------|---------|
| **URL** | https://lasair.lsst.ac.uk; Docs: https://lasair.readthedocs.io |
| **Description** | UK-developed Rubin community broker. Specialized in transient detection, multi-messenger astronomy, massive SN samples. Ingested 800,000 alerts on first night of Rubin operations (Feb 2026). Partners with ALeRCE and Fink for annotation ingestion [^43^][^45^][^54^]. |
| **Data Volume** | Full ZTF archive; full Rubin alert stream (up to 10M alerts/night expected) |
| **Format** | SQL query results; JSON; Avro; CSV |
| **Access Method** | (1) Web portal with SQL filter builder; (2) REST API; (3) Kafka streams; (4) SQL queries for object selection; (5) Watchlists and watchmaps [^51^][^54^] |
| **Update Frequency** | Real-time; alerts within 1 hour of observation |
| **Registration** | Free account for saving queries and filters |
| **Special Features** | - SQL-based filter construction; Sherlock host galaxy association with photo-z; Cross-match with TNS, Gaia, PanSTARRS; Ingests ALeRCE and Fink classifications as annotations; Multi-messenger GW response; Public SQL queries can be copied/modified |
| **ML Readiness** | High. SQL interface enables complex object selection. Sherlock provides host galaxy info. Full light curves available. Partners with ALeRCE/Fink for ML classifications. |
| **Example Code** | ```python
# Lasair uses SQL filters
# Example: SELECT objects.objectId, objects.gmag, objects.rmag
# FROM objects INNER JOIN sherlock_classifications
# WHERE sherlock_classifications.classification = "SN"

# API access documented at lasair.readthedocs.io
# Kafka streams available for filtered subsets
``` |

**Relevant Papers**: Smith et al. (2019); Enabling Science from Rubin (2024, arXiv:2404.08315) [^43^]

---

#### 10. ANTARES (Arizona-NOIRLab Temporal Analysis and Response to Events System)

| Attribute | Details |
|-----------|---------|
| **URL** | https://antares.noirlab.edu |
| **Description** | Full-service real-time broker developed at NOIRLab. Processes ZTF public stream; transitioning to Rubin. Users can write custom Python filters for real-time alert selection. Provides cross-matches with multiwavelength catalogs and past alert history [^44^][^171^]. |
| **Data Volume** | Full ZTF public stream; searchable archive |
| **Format** | JSON; Avro; Python client streaming |
| **Access Method** | (1) Web portal; (2) Python ANTARES Client library; (3) API; (4) Kafka substreams from user filters; (5) Searchable archive of ZTF alerts [^171^] |
| **Update Frequency** | Real-time |
| **Registration** | Free |
| **Special Features** | - User-contributed Python filters; Machine learning model integration in filters; Watchlists for object notifications; Catalogs for large-scale comparisons; Real-time multi-messenger cross-matching; >30 ATELs submitted from ANTARES filters |
| **ML Readiness** | High. Users can deploy ML models within filters. Archive searchable for historical data. Streaming enables real-time ML inference. |
| **Example Code** | ```python
# ANTARES Client library
from antares_client import StreamingClient

# Subscribe to a stream
client = StreamingClient('your_api_key')
for alert in client.stream('your_filter_id'):
    # Process alert with your ML model
    process_alert(alert)
``` |

**Relevant Papers**: Narayan et al. (2018); Matheson et al. (2026) AAS 247, 424.04 [^175^]

---

#### 11. AMPEL (Alert Management, Photometry, and Evaluation of Light Curves)

| Attribute | Details |
|-----------|---------|
| **URL** | https://ampel.zeuthen.desy.de; GitHub: https://github.com/ampelproject |
| **Description** | Modular analysis framework combining broker functionality with a generic code-to-data platform. Processes ZTF; preparing for LSST. Novel transient state tracking. Supports multi-messenger (IceCube+ZTF demonstrated) [^168^][^170^][^166^]. |
| **Data Volume** | Full ZTF stream; ELAsTiCC simulations processed |
| **Format** | JSON; Avro alerts; Tiered processing output |
| **Access Method** | (1) Web interface; (2) User-contributed channels/filters; (3) API; (4) Integration with SkyPortal front-end; (5) Full workflow reproducibility |
| **Update Frequency** | Real-time |
| **Registration** | Free for users |
| **Special Features** | - Modular tiered architecture (T0-T3); Code-to-data platform; Novel transient state tracking; FAIR principles for reproducibility; User-defined channels in Python; SNGuess (99% accuracy on young SNe); FollowMe (unbiased follow-up); FinalBet (>80% extragalactic classification); Integration with SkyPortal [^166^] |
| **ML Readiness** | Very High. Tiered system designed for ML: T0=alerts, T1=datapoint series, T2=transient state, T3=ensemble. SNGuess, FollowMe, FinalBet channels demonstrate ML integration. ELAsTiCC v1 dataset used for training. |
| **Example Code** | ```python
# AMPEL channels are Python-based workflows
# Users define processing units that inherit from AMPEL base classes
# See: https://github.com/ampelproject and documentation
# Integration with SkyPortal for visualization
``` |

**Relevant Papers**: Nordin et al. (2019) A&A 631, 147 [^170^]; Nordin et al. (2025) A&A 698, A13 [^166^]

---

#### 12. Pitt-Google Broker

| Attribute | Details |
|-----------|---------|
| **URL** | https://pittgoogle.lsst.ac.uk (with LSST:UK); https://github.com/pitt-crc/pitt-google |
| **Description** | Partnership between University of Pittsburgh and Google Cloud. One of seven Rubin community brokers. Leverages Google Cloud services for content distribution. Ingests ZTF and LIGO/Virgo/KAGRA data alongside Rubin alerts. Specializes in Type Ia supernovae for cosmology [^169^]. |
| **Data Volume** | Full Rubin alert stream; ZTF archive; GW alerts |
| **Format** | Avro; JSON; BigQuery tables |
| **Access Method** | (1) Google Cloud Pub/Sub streams; (2) BigQuery database access; (3) Cloud Storage bucket access |
| **Update Frequency** | Real-time |
| **Registration** | Google Cloud account may be needed for some access |
| **Special Features** | - Google Cloud native (Pub/Sub, BigQuery, Cloud Storage); Multi-messenger (GW + optical); Optimized for SNe Ia cosmology; Scales with Google Cloud infrastructure |
| **ML Readiness** | High. BigQuery enables SQL-based data analysis. Pub/Sub enables streaming ML inference. Cloud-native infrastructure. |

**Relevant Papers**: Overview in arXiv:2412.01651 [^165^]; Rubin launch coverage [^169^]

---

#### 13. sncosmo (Python Library)

| Attribute | Details |
|-----------|---------|
| **URL** | https://github.com/sncosmo; Docs: https://sncosmo.readthedocs.io |
| **Description** | The standard Python library for supernova cosmology. Simulates, fits, and types SN light curves. Reads/writes multiple data formats including SNANA, SALT2, JSON, ASCII. Used extensively in the SN cosmology community [^27^][^33^][^40^]. |
| **Data Formats** | SNANA FITS/ASCII, SALT2, JSON, ASCII, SDSS, CSP, DES, PS1, and more |
| **Access Method** | `pip install sncosmo` (conda-forge also available) |
| **Key Capabilities** | - Read/write SNANA FITS format (HEAD+PHOT files); Read SALT2 light curves; Built-in models (SALT2, MLCS2k2, Hsiao, Nugent, etc.); Built-in bandpasses; Magnitude system conversions; Light curve fitting (SALT2, MLCS); Simulation tools |
| **ML Readiness** | Very High. Standard format converter for ML pipelines. SNANA FITS reading enables direct use of large survey data. Integration with astropy. |
| **Example Code** | ```python
import sncosmo

# Read SNANA FITS format (standard for large surveys)
meta, tables = sncosmo.read_snana_fits('HEAD.fits', 'PHOT.fits')

# Read SALT2 format
lc = sncosmo.read_lc('lightcurve_file.dat', format='salt2')

# Load example data
data = sncosmo.load_example_data()

# Fit a SALT2 model
model = sncosmo.Model(source='salt2')
result, fitted_model = sncosmo.fit_lc(data, model, ['z', 't0', 'x0', 'x1', 'c'])
``` |

**Relevant Papers**: Barbary et al. (2016) ASCL, 11017B [^35^]; Documentation at sncosmo.readthedocs.io [^40^]

---

#### 14. SuperNNova (SNN)

| Attribute | Details |
|-----------|---------|
| **URL** | https://github.com/supernnova/SuperNNova; Docs: https://supernnova.readthedocs.io |
| **Description** | Open-source photometric time-series classification framework using RNNs (LSTM, GRU, Bayesian variants). Part of the PIPPIN end-to-end cosmology pipeline. Trains on simulations in CSV and SNANA FITS format. Deployed in Fink broker for real-time classification [^149^][^142^]. |
| **Input Formats** | SNANA FITS, CSV; supports binary and multi-class classification |
| **Key Capabilities** | - RNN-based light curve classification; Bayesian RNNs for uncertainty calibration; Host galaxy redshift incorporation; Early classification (86%+ accuracy 2 days before peak); ~97% accuracy Ia vs non-Ia without redshift; ~99.6% with redshift |
| **ML Readiness** | Purpose-built for ML. Complete framework: data loading, training, evaluation. Handles SNANA and CSV natively. Deployed in production (Fink). |
| **Example Code** | ```bash
pip install supernnova
# Or: git clone https://github.com/supernnova/supernnova.git

# Training
python run.py --data_training data/SNANA_training --model RNN

# Classification
python run.py --data_testing data/SNANA_test --model RNN --prediction
``` |

**Relevant Papers**: Möller & de Boissière (2020) MNRAS 491, 4277 [^142^]; Möller et al. (2022, 2024)

---

#### 15. snmachine

| Attribute | Details |
|-----------|---------|
| **URL** | https://github.com/LSSTDESC/snmachine; Docs: https://lsstdesc.github.io/snmachine |
| **Description** | DESC-developed machine learning library for photometric supernova classification. Flexible framework for reading light curves, feature extraction (wavelets, template fits), and supervised ML classification. Supports general transient classification [^150^]. |
| **Input Formats** | Multiple survey formats including SNANA, PLAsTiCC, DES |
| **Key Capabilities** | - Wavelet-based feature extraction; Template fitting (Bazin function); GPs for light curve modeling; Support Vector Machines, Random Forest classifiers; Optimized for Rubin/LSST data |
| **ML Readiness** | Purpose-built for ML. End-to-end pipeline from raw light curves to classification. Used in DESC analyses. |
| **Example Code** | ```bash
pip install snmachine

# Load data, extract features, classify
# See tutorials at: https://lsstdesc.github.io/snmachine/tutorials
``` |

**Relevant Papers**: Lochner et al. (2016) ApJS 225, 31; Alves et al. (2021) arXiv:2107.07531 [^150^]

---

#### 16. ParSNIP

| Attribute | Details |
|-----------|---------|
| **URL** | https://github.com/kboone/parsnip; Paper: arXiv:2109.13999 |
| **Description** | Generative model for transient light curves using physics-enabled deep learning. Learns 3D intrinsic representation from photometry alone. Predicts time-varying spectra. Redshift-invariant classification. Outperforms state-of-the-art on PLAsTiCC and PS1 [^79^][^90^]. |
| **Input Formats** | sncosmo-compatible light curves |
| **Key Capabilities** | - 3D generative model; Redshift-invariant representation; Photometric classification (2.3x less contamination on PLAsTiCC); Anomaly detection (90% pure samples); Distance estimation (RMS 0.150 mag for SNe Ia) |
| **ML Readiness** | High. Novel approach combining physics with deep learning. Integrated with sncosmo ecosystem. Can identify previously-unobserved transients. |
| **Example Code** | ```python
# Install: pip install parsnip (or from source)
# See: https://github.com/kboone/parsnip
import parsnip

# Train model on light curve dataset
# Classify and get distances
# See documentation and notebooks in repo
``` |

**Relevant Papers**: Boone (2021) AJ 162, 151 [^90^]; arXiv:2109.13999 [^79^]

---

#### 17. Gaia Photometric Science Alerts

| Attribute | Details |
|-----------|---------|
| **URL** | http://gsaweb.ast.cam.ac.uk/alerts/home |
| **Description** | ESA Gaia mission's transient alert system. Detects supernovae, CVs, AGN flares, microlensing events, YSOs, and other variables. Publishes alerts with light curves. 2,612 alerts in Gaia EDR3 (July 2014 - May 2017); growing continuously [^120^]. |
| **Data Volume** | 2,612 alerts in DR3 snapshot; ~25% classified by end of 2019; ongoing |
| **Format** | Web interface; CSV export; Gaia Archive TAP |
| **Access Method** | (1) Alerts web interface; (2) Gaia Archive TAP (https://gea.esac.esa.int/archive/); (3) Alerts index page |
| **Update Frequency** | Near-real-time for alerts; DR releases periodically |
| **Special Features** | - All-sky scanning; ~55 mas astrometric accuracy; 1% photometry at G~13; ~46% completeness for classified SNe; Low contamination (93% purity at G<17); Light curves provided [^120^] |
| **ML Readiness** | Medium. Light curves available. Can be accessed via TAP. Well-suited for all-sky transient studies. |
| **Example Code** | ```python
# Via Gaia Archive TAP
import pyvo
tap = pyvo.dal.TAPService('https://gea.esac.esa.int/tap-server/tap')
# Query gaiadr3.sso_source or alerts tables
# See: http://gsaweb.ast.cam.ac.uk/alerts/alertsindex
``` |

**Relevant Papers**: Wyrzykowski et al. (2012); Hodgkin et al. (2021) A&A 652, A76 [^120^]

---

#### 18. OGLE-IV Transient Detection System

| Attribute | Details |
|-----------|---------|
| **URL** | http://ogle.astrouw.edu.pl/ogle4/transients/ |
| **Description** | Polish-led survey detecting transients in the Magellanic Clouds and Galactic bulge. Discovered 126+ SNe in Magellanic Bridge. Publishes light curves and discovery data. ftp archive available [^83^]. |
| **Data Volume** | 126+ SNe in Magellanic Bridge; 52 new SNe discoveries via OTDS |
| **Format** | ASCII light curves; Image files |
| **Access Method** | (1) Web page; (2) FTP: `ftp://ftp.astrouw.edu.pl/ogle/ogle4/transients/SN/MBR` |
| **Update Frequency** | As discoveries are made |
| **Registration** | None |
| **Special Features** | - High-cadence, well-calibrated light curves; Magellanic Clouds focus; Long baseline (>10 years); Template subtraction photometry |
| **ML Readiness** | Medium. Well-calibrated light curves suitable for template construction. Smaller sample size. |

**Relevant Papers**: Kozlowski et al. (2013) AcA 63, 1; Udalski et al. (2012-2013) [^83^]

---

#### 19. AAVSO (American Association of Variable Star Observers)

| Attribute | Details |
|-----------|---------|
| **URL** | https://www.aavso.org/data-download |
| **Description** | Amateur and professional variable star observations database. Contains supernova observations, magnitude estimates, and light curves from a global observer network [^145^][^146^]. |
| **Data Volume** | Millions of observations spanning decades |
| **Format** | CSV, JSON, XLSX |
| **Access Method** | (1) Global Data Search (new); (2) Search and Download Photometric Observations; (3) Direct CSV/JSON/XLSX export |
| **Update Frequency** | Real-time as observers submit |
| **Registration** | Free account for download |
| **Special Features** | - Historical data going back decades; Global observer network; SN Search Observing Program; Standardized photometry |
| **ML Readiness** | Medium. Useful for long-term light curve studies. Heterogeneous data quality due to different observers. |

---

#### 20. PLAsTiCC Dataset (Photometric LSST Astronomical Time-Series Classification Challenge)

| Attribute | Details |
|-----------|---------|
| **URL** | https://plasticc.org; Zenodo: https://doi.org/10.5281/zenodo.2539456 |
| **Description** | Simulated LSST classification challenge dataset. 3.5M+ objects with 450M+ observations across 6 LSST filters (ugrizy). Unblinded dataset released with full labels post-challenge [^122^][^124^]. |
| **Data Volume** | 3.5M+ objects; 450M+ observations; 6 filters; training set of ~8,000 labeled objects |
| **Format** | FITS (training); CSV; HDF5; Avro |
| **Access Method** | Zenodo download; Kaggle (historical); ELAsTiCC extension |
| **Update Frequency** | Static dataset (challenge concluded); ELAsTiCC updates for LSST |
| **Special Features** | - Realistic LSST cadence and noise; Redshift-biased training set; Seasonal gaps; Wide class distribution (SNe Ia, Ibc, II, SLSN, TDE, AGN, variable stars); Host galaxy contextual info; Standard benchmark for SN photometric classification |
| **ML Readiness** | Very High. Standard benchmark dataset. Used in hundreds of ML papers. Simulates realistic observational effects. |

**Relevant Papers**: The PLAsTiCC Team et al. (2018) AJ preprint; Boone et al. (2022) MNRAS [^124^]

---

#### 21. ELAsTiCC (Extended LSST Astronomical Time-series Classification Challenge)

| Attribute | Details |
|-----------|---------|
| **URL** | https://portal.nersc.gov/cfs/lsst/DESC_TD_PUBLIC/ELASTICC/ |
| **Description** | Follow-up to PLAsTiCC with more realistic LSST simulations. Used by brokers (including AMPEL) for testing ML pipelines. Provides VRO noise profile and cadence [^166^]. |
| **Data Volume** | Large simulated dataset; exact numbers vary by release |
| **Format** | HDF5, FITS |
| **Access Method** | NERSC public download |
| **ML Readiness** | Very High. Standard benchmark for Rubin-era classification. |

**Relevant Papers**: Nordin et al. (2025) A&A 698, A13 [^166^]

---

#### 22. ZTF Alert Archive

| Attribute | Details |
|-----------|---------|
| **URL** | https://ztf.caltech.edu/ztf-alert-stream.html; Archive: https://zwickytf.stream3.lbl.gov |
| **Description** | The Zwicky Transient Facility public alert stream. 1 million+ alerts per night. Contains difference-image detections, forced photometry, image stamps, and history [^170^]. |
| **Data Volume** | 1M+ alerts/night; billions of detections in archive |
| **Format** | Avro (alerts); FITS; Parquet |
| **Access Method** | (1) Alert archive at LBL; (2) Via brokers (ALeRCE, Fink, Lasair, ANTARES, AMPEL, Pitt-Google); (3) Direct Kafka streams; (4) Nightly summary files |
| **Update Frequency** | Real-time nightly |
| **Registration** | None for archive |
| **Special Features** | - Full alert packets with history; 30-day light curve in each alert; Image stamps (science, reference, difference); Real/bogus score; Cross-matched with PS1, Gaia |
| **ML Readiness** | Very High. The primary data source for most broker-based ML. Standard Avro format with schema. |

**Relevant Papers**: Patterson et al. (2019) PASP 131, 018001 [^170^]

---

#### 23. NOIRLab Astro Data Lab

| Attribute | Details |
|-----------|---------|
| **URL** | https://datalab.noirlab.edu |
| **Description** | Science platform with database access to NOIRLab and partner datasets. Provides TAP query service, JupyterLab environment, and cross-matching tools. Hosts NOIRLab Source Catalog (NSC) [^121^]. |
| **Data Volume** | NSC covers nearly all public NOIRLab imaging |
| **Format** | TAP/ADQL returns VOTable; Database tables |
| **Access Method** | (1) TAP service; (2) JupyterLab notebooks; (3) Query manager; (4) Python astroquery integration |
| **Special Features** | - TAP/ADQL standard interface; JupyterLab with pre-installed astropy stack; Cross-matching services; Account-based query storage; Integration with DESI Legacy Surveys |
| **ML Readiness** | High. TAP interface enables programmatic queries. JupyterLab suitable for ML workflows. |
| **Example Code** | ```python
from astroquery.noirlab import Noirlab
# Or use pyvo TAP directly
tap = pyvo.dal.TAPService('https://datalab.noirlab.edu/tap')
``` |

---

#### 24. ADS (Astrophysics Data System) / NED

| Attribute | Details |
|-----------|---------|
| **URL** | https://ui.adsabs.harvard.edu; https://ned.ipac.caltech.edu |
| **Description** | ADS provides the bibliographic database. NED (NASA/IPAC Extragalactic Database) provides galaxy and SN host galaxy data essential for SN studies (redshifts, photometry, cross-identifications). |
| **Data for SN** | Host galaxy redshifts, photometry, cross-identifications, classifications |
| **Format** | JSON API (ADS); Various (NED) |
| **Access Method** | (1) ADS API; (2) astroquery.ned; (3) NED web interface; (4) TAP |
| **ML Readiness** | High for host galaxy features. NED commonly used for SN host redshift lookups. |
| **Example Code** | ```python
from astroquery.ned import Ned
result = Ned.query_object('SN 2011fe')
redshift = result['Redshift']
``` |

---

### Data Access Code Examples

#### Comprehensive Python Environment Setup

```bash
# Core packages for supernova data access and ML
pip install sncosmo astroquery supernnova snmachine
pip install alerce fink-client  # Broker clients
pip install pyvo pandas numpy scipy matplotlib astropy
pip install parsnip  # Generative model
```

#### Multi-Platform Data Access Pattern

```python
# A complete workflow combining multiple platforms

# 1. Query TNS for classified SNe
import requests
import pandas as pd

# TNS daily CSV (public)
tns_df = pd.read_csv('tns_public_objects.csv')
sn_classified = tns_df[tns_df['type'].str.contains('SN', na=False)]

# 2. Get light curves from ALeRCE
from alerce.core import Alerce
client = Alerce()

for sn_name in sn_classified['name'][:10]:
    try:
        lc = client.query_lightcurve(oid=sn_name, survey="ztf", format="json")
        # Process light curve for ML
    except:
        pass

# 3. Get spectra from WISeREP
# Use their API or direct download

# 4. Cross-match with SIMBAD for host info
from astroquery.simbad import Simbad

# 5. Get photometry from Open Supernova Catalog
# Download: http://snad.space/osc/sne.tar.lzma
# Parse JSON files

# 6. Convert to ML format with sncosmo
import sncosmo
meta, tables = sncosmo.read_snana_fits('HEAD.fits', 'PHOT.fits')

# 7. Classify with SuperNNova
# python run.py --data_training data/ --model RNN

# 8. Or use ParSNIP for generative modeling
import parsnip
# model = parsnip.train(...)
```

---

### Trends & Signals

1. **Broker-centric ecosystem**: The Rubin Observatory era has shifted the focus from static catalogs to real-time streaming brokers. ALeRCE, Fink, Lasair, ANTARES, AMPEL, and Pitt-Google all provide programmatic access to processed alerts with ML classifications [^44^][^50^].

2. **Python-first access**: All modern platforms provide Python clients or REST APIs. sncosmo is the de facto standard format converter. astroquery provides unified access to SIMBAD, VizieR, HEASARC, and NED [^27^][^40^].

3. **Standard formats emerging**: SNANA FITS format (HEAD+PHOT files) is the standard for large surveys. Avro for alerts. JSON for individual object data. sncosmo bridges all of these [^35^].

4. **ML integration at broker level**: Brokers now deploy deep learning classifiers in production. Fink uses SuperNNova (RNN), ALeRCE uses CNN+RFC classifiers, AMPEL uses BDT+DNN ensembles [^56^][^59^][^166^].

5. **Open data becoming standard**: Open Supernova Catalog, TNS daily CSV, WISeREP public spectra, PLAsTiCC/ELAsTiCC unblinded data all promote reproducible ML research [^86^][^122^].

6. **Cloud-native architecture**: HEASARC on AWS, WISeREP on AWS, Fink on OpenStack, Pitt-Google on Google Cloud, AMPEL on DESY infrastructure. Cloud storage enables bulk ML data access without rate limits [^37^][^114^].

7. **Active learning emerging**: Fink's early SN Ia classifier demonstrated active learning on real alerts, achieving 89% purity with just 310 training alerts, proving that intelligent sampling can reduce labeling needs [^47^][^56^].

8. **Cross-broker collaboration**: Lasair ingests classifications from ALeRCE and Fink as annotations. TNS and WISeREP auto-sync. This interoperability provides richer feature sets for ML [^43^].

---

### Recommended Deep-Dive Areas

1. **Broker API benchmark study**: Systematically compare latency, rate limits, data completeness, and classification accuracy across ALeRCE, Fink, Lasair, and ANTARES APIs. No comprehensive comparison exists.

2. **Complete OSC data pipeline**: Build a reference ML pipeline that ingests the full OSC tarball, cleans heterogeneous photometry, handles missing data, and produces standardized light curves. The OSC's JSON format is rich but messy.

3. **WISeREP spectral ML**: Develop a systematic spectral classification pipeline using WISeREP's bulk download. Current studies are ad hoc. A curated training set of >5,000 spectra with standardized preprocessing would be valuable.

4. **Rubin broker transition monitoring**: As Rubin operations ramp up, monitor which brokers provide the best ML-ready data products. Early results from February 2026 are just becoming available.

5. **ParSNIP for anomaly detection**: Boone's ParSNIP model can identify previously-unobserved transients at 90% purity. A systematic application to broker alert streams could discover new SN subtypes.

6. **ELAsTiCC benchmark suite**: The ELAsTiCC v1 dataset (used by AMPEL) should be compared against PLAsTiCC as a Rubin-era benchmark. Which simulated effects matter most for real-data transfer?

7. **Cross-broker feature fusion**: Combine classifications from multiple brokers (Fink + ALeRCE + Lasair annotations) using stacking or ensemble methods. No study has systematically compared broker classifications on identical objects.

8. **Real-time active learning implementation**: Deploy Fink-style active learning on a local broker stream. Quantify how many spectroscopic labels are needed for a given accuracy threshold as Rubin scales to millions of SNe/year.

9. **Gaia Alerts untapped potential**: Gaia's scanning law provides unique time sampling. The ~46% completeness for SNe and 79% for multi-scan SNe represents a well-defined selection function that could be valuable for population studies [^120^].

10. **ZTF alert archive reprocessing**: The full ZTF archive (billions of detections) available via the LBL archive offers an opportunity to train large-scale models. No comprehensive ML reprocessing of the full archive has been published.

---

### Citation Index

[^26^]: HEASARC main portal, https://heasarc.gsfc.nasa.gov
[^27^]: SNCosmo GitHub, https://github.com/sncosmo
[^28^]: TNS Getting Started, https://www.wis-tns.org/content/tns-getting-started
[^29^]: VizieR documentation, https://cds-astro.github.io/a-FAIR-journey-for-astronomical-data
[^30^]: HEASARC Data Archive documentation, https://heasarc.gsfc.nasa.gov/docs/archive.html
[^32^]: TNS FAQ, https://www.wis-tns.org/content/faq
[^33^]: sncosmo website, https://sncosmo.github.io/
[^34^]: TNS presentation, Paris MMA Workshop Jan 2022
[^35^]: SNCosmo: Python library for supernova cosmology, ADS 2016ascl.soft11017B
[^36^]: HEASARC in the 2020s, ADS 2018AAS...23221407S
[^37^]: NASA HEASARC on AWS Open Data Registry, https://registry.opendata.aws/nasa-heasarc/
[^40^]: sncosmo Documentation, https://sncosmo.readthedocs.io/
[^43^]: Enabling Science from the Rubin Alert Stream with Lasair, arXiv:2404.08315
[^44^]: Rubin Observatory Alerts and Brokers, https://rubinobservatory.org/for-scientists/data-products/alerts-and-brokers
[^45^]: UK scientists open real-time window, https://www.physics.ox.ac.uk/news/uk-scientists-open-real-time-window-universe
[^46^]: Fink broker news, https://fink-broker.org/news/
[^47^]: Fink early supernovae Ia classification, arXiv:2111.11438
[^48^]: Introduction to Fink, https://community.lsst.org/t/an-introduction-to-fink/10653
[^49^]: An Open Catalog for Supernova Data, ApJ 835, 64
[^50^]: Rubin Observatory real-time alerts, Stanford News 2026-02-25
[^51^]: Lasair FAQ, https://lasair.readthedocs.io/en/main/more_info/faqs.html
[^52^]: Fink broker AuDACES 2022 presentation
[^55^]: fink, a new generation of broker, MNRAS 501, 3272
[^56^]: Fink early SN Ia classification using active learning, A&A 663, 170
[^59^]: ALeRCE Alert Broker, AJ 161, 242
[^60^]: Fink tutorials, https://github.com/astrolabsoftware/fink-tutorials
[^79^]: ParSNIP: Generative Models of Transient Light Curves, arXiv:2109.13999
[^81^]: OSC anomaly detection catalog, VizieR J/MNRAS/489/3591
[^83^]: OGLE-IV Magellanic transients, AcA 63, 1
[^86^]: Open Supernova Catalog, arXiv:1605.01054
[^87^]: AstroCats GitHub, https://github.com/astrocatalogs/astrocats
[^89^]: Open Supernova Catalog GitHub, https://github.com/astrocatalogs/supernovae
[^90^]: ParSNIP, AJ 162, 151
[^93^]: SIMBAD query guide, http://simbad.u-strasbg.fr/Pages/guide/sim-q.htx
[^113^]: WISeREP, PASP 124, 668
[^114^]: WISeREP migrated to AWS, AstroNote 2021-142
[^116^]: WISeREP Getting Started, https://www.wiserep.org/content/wiserep-getting-started
[^117^]: WISeREP Home, https://www.wiserep.org/
[^118^]: WISeWEBSpider, https://github.com/jparrent/WISeWEBSpider
[^120^]: Gaia Photometric Science Alerts, A&A 652, A76
[^121^]: NOIRLab Source Catalog, https://datalab.noirlab.edu/data/nsc
[^122^]: PLAsTiCC, https://plasticc.org
[^124^]: Pan-chromatic photometric classification, MNRAS arXiv:2208.01328
[^142^]: SuperNNova, MNRAS 491, 4277
[^143^]: AAVSO Data Validation Project, JAVSO 34, 238
[^145^]: AAVSO Supernova Search, https://www.aavso.org/supernova-search-observing-program
[^146^]: AAVSO Download Data, https://www.aavso.org/data-download
[^147^]: Spectral SN Classification ML, https://github.com/CrisJorda
[^149^]: SuperNNova GitHub, https://github.com/supernnova/SuperNNova
[^150^]: snmachine, https://github.com/LSSTDESC/snmachine
[^151^]: ALeRCE Python Client, https://github.com/alercebroker/alerce_client
[^153^]: ALeRCE API Reference, https://alerce.readthedocs.io/en/latest/apis.html
[^164^]: Rubin Observatory launch, NOIRLab 2026-02-25
[^165^]: Overview of astronomical transient brokers, CAOSP 55, 95
[^166^]: AMPEL workflows for LSST, A&A 698, A13
[^167^]: Fink white paper, arXiv:2009.10185
[^168^]: Transient processing with AMPEL, arXiv:1904.05922
[^169^]: Pitt-Google broker, PittWire 2026-03-03
[^170^]: ZTF Alert Stream, https://www.ztf.caltech.edu/ztf-alert-stream.html
[^171^]: ANTARES 1.0, NOIRLab
[^173^]: Fink ZTF documentation, https://doc.ztf.fink-broker.org
[^175^]: ANTARES perspective on Roman, AAS 247, 424.04

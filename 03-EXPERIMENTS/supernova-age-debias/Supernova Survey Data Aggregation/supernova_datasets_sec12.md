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

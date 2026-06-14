# Plan: Supernova Survey Datasets Deep Dive for ML

## Objective
Aggregate and catalog all publicly available datasets from supernova surveys, with focus on their suitability for astrophysics machine learning projects — including data formats, access methods, volumes, features, and relevant documentation.

## Skill: deep-research-swarm (Route A — Wide Search)
This is a broad, exploratory topic requiring maximum search breadth across multiple survey programs, data archives, and ML-ready datasets.

## Stages

### Stage 1 — Wide Exploration (Parallel)
Deploy multiple research agents to cover different survey categories:
- **Optical Surveys**: Pan-STARRS, DES, LSST/VRO, SDSS, CFHT, DECam surveys
- **Time-Domain / Transient Surveys**: ZTF, ATLAS, ASAS-SN, PTF/iPTF, SkyMapper, OGLE
- **Space-Based Surveys**: HST, JWST, Kepler/K2, TESS, Swift, Gaia
- **Historical & Legacy Surveys**: LOSS, SNLS, ESSENCE, CSP, CTA, Carnegie Supernova Project
- **Spectroscopic Datasets**: SN Factory, GALEX, WISE spectroscopic follow-up
- **Data Archives & Aggregators**: NASA/IPAC, HEASARC, VizieR, NOIRLab, HSC, data release portals

### Stage 2 — Deep Dive (Parallel)
For each promising survey/dataset identified in Stage 1, dispatch deep-dive agents to extract:
- Dataset name and description
- Survey type (photometric, spectroscopic, multi-band)
- Data volume (number of SNe, light curves, spectra)
- Available features (redshift, host galaxy info, classification, etc.)
- Data format (FITS, CSV, HDF5, etc.)
- Access method (URL, API, bulk download)
- Relevant data releases (DR1, DR2, etc.)
- Citations/papers documenting the data
- ML use cases already demonstrated (if any)

### Stage 3 — Synthesis & Report
Compile all findings into a structured, comprehensive report with:
- Executive summary
- Catalog of all datasets with key metadata
- Comparison matrix (volume, features, accessibility)
- Recommendations for ML projects
- Links and citations

## Output
- Final report in Markdown format (`supernova_datasets_report.md`)
- Optionally convert to `.docx` if requested

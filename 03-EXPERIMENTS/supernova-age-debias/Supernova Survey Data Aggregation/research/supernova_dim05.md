# Dimension 05: Space-based Time-Domain Data for Supernova ML

## Executive Summary

Space-based observatories provide unique capabilities for supernova (SN) studies that are unattainable from the ground: access to ultraviolet (UV) wavelengths, high-cadence continuous monitoring, all-sky coverage without weather gaps, and stable point-spread functions. This report documents **7 major space-based platforms** providing SN data suitable for machine learning, with detailed access methods, data volumes, and ML-relevant features. Key findings include:

| Mission | SN Sample Size | Key ML Feature | Data Access |
|---------|---------------|----------------|-------------|
| **TESS** | 307 SNe Ia + 4,000+ transients | 30-min cadence FFI light curves | MIT TessTransients API + GitHub |
| **Kepler/K2** | 23+ SNe | 30-min cadence pre-explosion coverage | MAST archive, KEGS program |
| **Swift/SOUSA** | 253 SNe, 6 UVOT filters | UV/optical multi-filter SEDs | MAST HLSP + SOUSA website |
| **GALEX** | 1,080 SNe Ia UV LCs | NUV/FUV photon-level time series | gPhoton2 pipeline @ MAST |
| **Gaia Alerts** | 10,765+ alerts, BP/RP spectra | Low-res spectra at every epoch | Web interface + CSV download |
| **JWST** | 80+ high-z transients | NIR 0.6-5.3 um multi-epoch imaging | MAST (JADES, COSMOS-Web) |
| **HST** | 15+ SNe Ia at z>1 | ACS/WFC3 UV through IR photometry | MAST (CANDELS+CLASH) |

---

## 1. TESS (Transiting Exoplanet Survey Satellite)

### 1.1 Overview
TESS provides unique 30-minute cadence (10-minute in extended mission) full-frame images (FFIs) covering ~85% of the sky. While designed for exoplanets, TESS has proven to be a powerful tool for time-domain astrophysics, including supernova studies [^1^][^2^].

**Key characteristics:**
- Bandpass: 600-1000 nm (red-optical/near-IR)
- Cadence: 30 min (Sectors 1-26), 10 min (Sectors 27+)
- Field of view: 24 x 96 degrees per sector
- Limiting magnitude: ~20 (3-sigma, binned to 8 hours)
- Photometric precision: ~1% at TESS magnitude 14

### 1.2 MIT TessTransients Database

The primary access point for TESS supernova light curves is the **MIT TessTransients** database, maintained by Michael Fausnaugh (Texas Tech) [^3^][^4^].

**Database stats (as of 2025):**
- 10,584 total astrophysical transients (all types)
- 1,299 confirmed supernovae with extracted light curves
- Updated every 7 days using TICA HLSP data from MAST

**Data access methods:**

1. **Individual light curve API** (simplest):
   ```bash
   wget https://tess.mit.edu/public/tesstransients/light_curves/lc_2022sfe_cleaned
   ```
   Replace "2022sfe" with any IAU designation. Returns ASCII text data.

2. **Bulk downloads**: Available via the Bulk Downloads page or GitHub repo
   - GitHub: https://github.com/mmfausnaugh/lc_bulk
   - Data under version control for reproducibility

3. **Per-sector browsing**: All transients per sector shown on individual pages

4. **Finding sector information**: Use `tess-point` tool:
   ```python
   from tess_point import tesspoint
   # Find which sector a given RA/Dec was observed in
   ```

### 1.3 Light Curve Format

Each light curve file contains [^4^]:
- BJD (Barycentric Julian Date)
- Relative flux (background-subtracted, difference-imaging)
- Flux error
- Quality flags
- TESS magnitude (when calibration is available)

Data are binned to 8-hour intervals for the published sample. Raw FFI extraction can be done with tools like `lygos`, `eleanor`, or `TGLC`.

### 1.4 Key Science Papers & Datasets

| Paper | Sample | Key Finding | arXiv/DOI |
|-------|--------|-------------|-----------|
| **Fausnaugh et al. 2021** | 9 SNe Ia (Sectors 1-6) | Early-time power law indices, beta=2.0 fireball model | arXiv:1904.02171 |
| **Fausnaugh et al. 2023** | 307 SNe Ia (Years 1-4) | Mean rise time 15.7+/-3.5 days, companion constraints | arXiv:2307.11815 |
| **Vallely et al. 2021** | 22 core-collapse SNe | High-cadence rise time measurements | arXiv:2010.06596 |
| **Dimitriadis et al. 2019** | SN 2018oh (K2) | Two-component early light curve | arXiv:1811.10061 |

### 1.5 Data Extraction Tools for TESS FFIs

| Tool | Method | Use Case | Reference |
|------|--------|----------|-----------|
| **lygos** | PSF photometry, differential flux | SN-specific extraction | Gordon et al. 2021 |
| **eleanor** | Aperture + PSF + systematics removal | General FFI extraction | Feinstein et al. 2019 |
| **TGLC** | Aperture + PSF using Gaia catalog | Crowded-field correction | Han & Brandt 2023 |
| **TESSCut** | MAST cutout service | Quick-look FFI access | Brasseur et al. 2019 |

### 1.6 ML Readiness: TESS
- **Format**: ASCII text files, easy CSV conversion
- **Cadence**: 30-min native, 8-hour binned in published sample
- **Unique value**: Early-time rise morphology (power law index), companion interaction signatures
- **Limitations**: Single broad filter; systematic errors during scattered light; blending
- **Best for**: Early-time classification, rise time studies, companion interaction detection

---

## 2. Kepler/K2

### 2.1 Overview
The Kepler Space Telescope provided unprecedented 30-minute cadence continuous photometry. The original Kepler mission monitored ~500 galaxies through the Kepler Extragalactic Survey (KEGS), while K2 extended observations along the ecliptic plane [^5^][^6^].

**Key characteristics:**
- Bandpass: 430-890 nm (Kepler/Kp filter)
- Cadence: 30 minutes (long cadence), 1 minute (short cadence)
- Photometric precision: ~10-100 ppm for bright sources
- Unique capability: Pre-explosion baseline + continuous coverage

### 2.2 Kepler Extragalactic Survey (KEGS)

Led by Peter Garnavich (Notre Dame) and Robert Olling (UMD), KEGS monitored approximately 500 galaxies at 30-minute cadence during the prime Kepler mission [^5^].

**Key results:**
- **Olling et al. 2015**: 3 SNe Ia with exquisite coverage from before explosion
- **Garnavich et al. 2016**: First visible-light detection of SN shock breakout in Type II-P SNe (KSN 2011a, KSN 2011d)
- Progenitor radii measured: 280 R_sun (KSN 2011a), 490 R_sun (KSN 2011d)

### 2.3 K2 Supernova Cosmology Experiment (K2 SCE)

Campaign 16 (December 2017 - February 2018) dedicated substantial targets to the K2 Supernova Cosmology Experiment, monitoring ~50x more galaxies than KEGS [^6^].

**Key supernovae:**

| SN | Type | Distance | Key Finding | Reference |
|----|------|----------|-------------|-----------|
| **SN 2018oh** (ASASSN-18bt) | Ia | 52.7 Mpc | Two-component early rise; companion interaction evidence | Dimitriadis et al. 2019 |
| **KSN 2015K** | Rapid transient | - | Shock in CSM discovery | Rest et al. 2018 |
| **KSN 2011a** | II-P | z=0.051 | Shock breakout detection | Garnavich et al. 2016 |
| **KSN 2011d** | II-P | z=0.087 | Shock breakout + progenitor radius | Garnavich et al. 2016 |

### 2.4 Data Access via MAST

All Kepler/K2 data are available through the Mikulski Archive for Space Telescopes (MAST):

- **URL**: https://archive.stsci.edu/missions-and-data/kepler
- **K2 data**: https://archive.stsci.edu/missions-and-data/k2
- **Search by**: KIC ID, coordinates, target name
- **Data products**: Target Pixel Files (TPFs), light curves, FFIs

**Using `lightkurve` for SN extraction:**
```python
import lightkurve as lk
# Download K2 TPF for a supernova
search_result = lk.search_targetpixelfile('EPIC 200198689', campaign=16)
tpf = search_result.download()
# Perform aperture photometry or custom extraction
lc = tpf.to_lightcurve(aperture_mask='all')
```

### 2.5 FFI Extraction for K2

For K2, difference imaging and custom aperture photometry are typically needed:
- **Kadenza**: Raw cadence data reader (Barentsen & Cardoso 2018)
- **Image subtraction**: Required due to K2 pointing drift (~4 arcsec)
- **Custom pipelines**: Ridden-Harper et al. 2020 developed background pixel survey methods

### 2.6 ML Readiness: Kepler/K2
- **Format**: FITS (TPFs), convertible to CSV/NumPy arrays
- **Cadence**: 30-minute native, continuous (no weather gaps)
- **Unique value**: Pre-explosion baseline; shock breakout detection; companion interaction
- **Limitations**: Small sample size (~23 total); red optical bandpass only; K2 pointing systematics
- **Best for**: Shock breakout studies, early-time morphology, progenitor constraints

---

## 3. Swift/SOUSA (Neil Gehrels Swift Observatory)

### 3.1 Overview
Swift's UltraViolet/Optical Telescope (UVOT) provides the largest sample of UV supernova light curves from any single instrument. UVOT observes in 6 filters covering 1600-6000 Angstroms, with typical 2-day cadence over weeks-long campaigns [^7^][^8^].

**UVOT characteristics:**
- 30 cm modified Ritchey-Chretien telescope
- 6 filters: UVW2 (1928 A), UVM2 (2246 A), UVW1 (2600 A), U (3450 A), B (4392 A), V (5468 A)
- 17 x 17 arcminute FOV
- Photon-counting detector with 0.5 arcsec virtual pixels
- Rapid Target of Opportunity response (within hours)

### 3.2 SOUSA: Swift Optical/Ultraviolet Supernova Archive

**SOUSA** is the primary data product for Swift SN observations, led by Peter Brown (Texas A&M) [^8^][^9^].

**Archive statistics:**
- **253 supernovae** with processed UVOT data
- All SN types and most subtypes represented
- Reprocessed with Breeveld et al. (2011) zeropoints and time-dependent sensitivity corrections
- Multiple filters per supernova (typically 3-6)

### 3.3 Data Products

SOUSA provides two types of data products [^8^]:

**1. Image products (hosted on MAST):**
```
hlsp_sousa_swift_uvot_<targname>[-tempsum]_<filter>_<ver>_img.fits.gz
```
- Filters: {bb, m2, uu, vv, w1, w2} = {b, uvm2, u, v, uvw1, uvw2}
- `*img.fits.gz` = summed image with supernova present
- `*tempsum_img.fits.gz` = template image (SN faded, host only)

**2. Light curve products (external team page):**
- ASCII/CSV format photometry files
- Count rates, fluxes, magnitudes with errors
- Host galaxy subtracted
- Download individual SN light curves or full tarball (270+ SNe)
- **Download all**: http://people.physics.tamu.edu/pbrown/SwiftSN/SOUSA160823.tar

**3. External team page**: https://pbrown801.github.io/SOUSA/
- Per-SN links to images, plots, and data files
- Sousaphone icons indicate available data

### 3.4 Data Access

**Via MAST HLSP interface:**
- URL: https://archive.stsci.edu/prepds/sousa/
- Searchable target table with all 253 SNe
- Individual image downloads per filter

**Via SOUSA website:**
- URL: https://pbrown801.github.io/SOUSA/
- Light curves in ASCII format
- Tarball download of 270+ supernovae

**For photometry extraction from images:**
```bash
# Use HEASoft uvotsource
uvotsource image=sn2011fe_w1.img srcreg=source.reg bkgreg=background.reg
```

### 3.5 Key Swift/SOUSA Science Papers

| Paper | Sample | Key Finding |
|-------|--------|-------------|
| **Brown et al. 2009** | 25 SNe (first sample) | UV color differentiation of Ia vs II-P; UV LCs of all major types | 
| **Milne et al. 2010** | 107 SNe Ia | NUV luminosity vs decline rate; UV-optical color evolution |
| **Brown et al. 2014** | SOUSA description | Archive structure, reprocessing, UVOT calibration |
| **Devarakonda et al. 2022** | 97 SNe Ia | UV vs optical light curve parameter correlations |
| **Brown et al. 2017** | 219 SNe Ia (2005-2016) | Template fitting methodology, UV-optical comparison |

### 3.6 UV-Optical Colors for Classification

The UVOT multi-filter system provides powerful classification diagnostics [^7^][^10^]:

| Color | Diagnostic Value |
|-------|-----------------|
| UVW2 - V | Differentiates SNe Ia from CC SNe at early times |
| UVW1 - U | Tracks UV decay rate; identifies UV-bright events |
| UVM2 - UVW1 | Temperature evolution; line blanketing effects |
| U - V | Phillips relation analog in UV-optical |

Key findings:
- SNe Ia show homogeneous UV colors; SNe II-P evolve rapidly in UV
- SNe Ib/c have varied UV-optical colors
- SN Ia subtypes (91T-like, 91bg-like, super-Chandrasekhar) have distinct UV colors
- Color-color plots can distinguish intrinsic redness from dust reddening

### 3.7 ML Readiness: Swift/SOUSA
- **Format**: FITS images + ASCII light curves; easily converted to CSV
- **Filters**: 6 filters (3 UV + 3 optical) providing SED information
- **Unique value**: Only large-sample UV SN archive; color evolution; early-time UV
- **Limitations**: ~2-day typical cadence; no spectroscopy; UV faintness limits depth
- **Best for**: UV-based classification, SED fitting, color-color classification, bolometric LCs

---

## 4. GALEX + gPhoton

### 4.1 Overview
The Galaxy Evolution Explorer (GALEX) provided UV imaging in two bands (FUV: 1344-1786 A, NUV: 1771-2831 A) with photon-level time tagging. The **gPhoton** database and software enable analysis of GALEX data at the photon level for time-domain science [^11^][^12^].

### 4.2 gPhoton Database

Hosted at MAST, the gPhoton database contains:
- **~130 TB** of photon-level data
- **~1.1 trillion** sky-projected photon events
- Time resolution: **5 milliseconds**
- All GALEX GR6/7 direct imaging data

### 4.3 gPhoton2 Pipeline

The updated **gPhoton2** pipeline (Million Concepts) provides [^12^]:
- 1-3 orders of magnitude faster than original gPhoton
- Calibration improvements
- Automatic light curve generation at user-defined temporal resolution
- Command-line interface and Python API

**Installation and usage:**
```bash
git clone https://github.com/MillionConcepts/gPhoton2.git
cd gphoton2
mamba env create -f environment.yml
```

**Basic pipeline execution:**
```bash
python pipeline_cli.py 23456 NUV --depth=30
```
This fetches raw GALEX telemetry, produces photonlist, 30-sec binned light curves, and images.

### 4.4 GALEX Supernova Data

The **GALEX Time-Domain Survey (TDS)** covered 40 deg^2 and found 1,078 UV-variable sources [^13^]. The **1UVA catalog** (2024) extended this to ~7x the area using 385 NUV fields with >10 visits each.

For SNe Ia specifically:
- **Milne et al. 2010**: Compiled UV light curves for ~1,080 SNe Ia using GALEX + Swift
- GALEX provides NUV/FUV photometry at typically days-to-weeks cadence
- Critical for UV-optical bolometric light curves and extinction corrections

### 4.5 Data Access

**gPhoton @ MAST**: https://archive.stsci.edu/prepds/gphoton/
- Web interface for photon database queries
- Python package: `gFind`, `gAperture`, `gMap`

**Key tools:**
| Tool | Function |
|------|----------|
| `gFind` | Search database for GALEX coverage at a position |
| `gAperture` | Extract calibrated light curves from photon data |
| `gMap` | Create calibrated images and movies |
| `gPhoton2` | Full reprocessing pipeline (next generation) |

**Using gPhoton for SN light curves:**
```python
from gPhoton import gAperture
# Extract NUV light curve for a SN position
light_curve = gAperture(band='NUV', skypos=[ra, dec], stepsz=30.0,
                        radius=0.0045, annulus=[0.005,0.006])
```

### 4.6 ML Readiness: GALEX
- **Format**: Photon lists (Parquet); extracted light curves (CSV)
- **Bands**: NUV + FUV
- **Unique value**: Photon-level time resolution (5ms); UV wavelengths below Swift UVW2
- **Limitations**: Mission ended 2013; limited time-domain coverage; requires gPhoton processing
- **Best for**: UV bolometric corrections, early-time UV evolution, extinction studies

---

## 5. Gaia Photometric Science Alerts (GSA)

### 5.1 Overview
Gaia provides an all-sky transient survey with unique capabilities: high spatial resolution (~0.1 arcsec), high photometric precision (1% at G=13, 3% at G=19), and critically, low-resolution BP/RP spectra at every epoch [^14^][^15^].

**Key characteristics:**
- G-band photometry: 330-1050 nm (broad optical)
- BP spectrum: 330-680 nm, R~100
- RP spectrum: 640-1000 nm, R~100
- Limiting magnitude: G~20.7
- Typical cadence: ~1 visit per month (two FOVs separated by 106.5 degrees)

### 5.2 Gaia Alerts Statistics

As of the Gaia EDR3 paper (covering through 2019) [^15^]:
- **10,765 alerts** published (2014-2019)
- Published at ~12 events/day
- ~25% ultimately classified
- Classifications dominated by SNe (biased by follow-up campaigns)
- Full sky coverage including Galactic plane

### 5.3 Data Products per Alert

Each alert page includes [^15^][^16^]:
1. **G-band light curve**: CSV format, calibrated photometry
2. **BP/RP spectra**: At every epoch, in pixel space (uncalibrated)
3. **Finding charts**: Aladin Lite overlay
4. **Cross-matches**: Positionally matched transients from other surveys
5. **Follow-up photometry**: From Cambridge Photometric Calibration Server (CPCS)

### 5.4 Data Access

**Web interface:** https://gsaweb.ast.cam.ac.uk/alerts/
- **Alert Index**: Browse all alerts with classifications
- **Alerts Search**: Search by name, coordinates, type
- **Per-alert pages**: Light curves + spectra + cross-matches

**Programmatic access:**
- Light curves available as CSV from per-alert pages
- **GaiaX** alert stream: https://gsaweb.ast.cam.ac.uk/alerts/gaiax/
  - CSV tables per processing run
  - Format: `gaiax_NNNN.csv` where NNNN is the run ID
- **Gaia TAP query** via astroquery:
  ```python
  from astroquery.gaia import Gaia
  # Query Gaia DR3 for alert sources
  job = Gaia.launch_job("SELECT * FROM gaiadr3.gaia_source "
                        "WHERE source_id IN (SELECT source_id FROM alerts)")
  ```

**CPCS follow-up data:**
- URL: http://gsaweb.ast.cam.ac.uk/followup/
- JSON format light curves from follow-up observations
- Multiple telescopes and filters available

### 5.5 BP/RP Spectra for Classification

The BP/RP spectra (R~100, 330-1000 nm) provide unique classification capabilities [^15^][^17^]:
- SN type classification from low-resolution spectra alone (GS-TEC classifier)
- Redshift estimation from spectral features
- Epoch estimation relative to peak brightness
- Color evolution at each epoch

**Simulations show**: Most SN major types recognized with low confusion down to G=19 mag [^17^].

### 5.6 Key GSA Papers

| Paper | Content |
|-------|---------|
| **Hodgkin et al. 2021** (A&A 652, A76) | First 5 years of GSA operations; 10,765 alerts |
| **Kostrzewa-Rutkowska et al. 2020** | GaiaX alert stream; 1-FoV detector |
| **Blagorodnova et al. 2014** | BP/RP spectral classification (GS-TEC) |
| **Delgado et al. 2016** | Alert publishing system; VOEvents |

### 5.7 ML Readiness: Gaia Alerts
- **Format**: CSV light curves, JSON follow-up data, BP/RP spectra in custom format
- **Unique value**: Only space-based survey with spectra at every epoch; all-sky; no weather bias
- **Limitations**: Low cadence (~monthly); low spectral resolution (R~100); uncalibrated spectra
- **Best for**: Spectral classification, color evolution, all-sky completeness studies

---

## 6. JWST (James Webb Space Telescope)

### 6.1 Overview
JWST has opened a new era in high-redshift supernova studies with unprecedented NIR sensitivity (0.6-5.3 um). The **JADES** program and other surveys have discovered the most distant spectroscopically-confirmed SNe to date [^18^][^19^].

**Key instruments for SN studies:**
- **NIRCam**: Imaging 0.6-5.0 um, 9 filters simultaneously with 2 modules
- **NIRSpec**: Spectroscopy 0.6-5.3 um, R~100 (prism) to R~2700 (gratings)
- **MIRI**: 5-28 um imaging and spectroscopy

### 6.2 JADES Transient Survey

The **JWST Advanced Deep Extragalactic Survey (JADES)** has yielded breakthrough SN discoveries [^18^][^19^]:

**Survey characteristics:**
- Field: GOODS-S (~25-27 arcmin^2)
- Depth: ~30 AB mag (5-sigma)
- Two epochs separated by ~1 year
- Filters: F090W, F115W, F150W, F200W, F277W, F356W, F410M, F444W

**Key results:**
- **53 transients** in JADES-Deep (z=0.5 to z=4.4)
- **~1 transient/arcmin^2/epoch**
- SN Ia at **z=2.9** (Pierel et al. 2024)
- Broad-lined Ic at **z=2.83** (Siebert et al. 2024)
- UV-bright SN at **z=3.6** (Coulter et al. 2025)
- First systematic characterization of high-z SNe II

### 6.3 COSMOS-Web + PRIMER

Overlapping treasury programs covering **133 arcmin^2** (~5x JADES area), shallower (~28 mag) [^19^]:
- 68 SNe discovered (0.5 SNe/arcmin^2)
- Host photo-z's at 1<z<2 (majority), with 10 at 2<z<5

### 6.4 Data Access via MAST

All JWST data are publicly available through MAST:
- **URL**: https://archive.stsci.edu/
- **Search by**: Program ID, coordinates, target name
- **Key programs**: 
  - PID 1180, 3215: JADES NIRCam imaging
  - PID 6541: JADES transient follow-up (NIRSpec + NIRCam)
  - PID 1727: COSMOS-Web
  - PID 1837: PRIMER

**Programmatic access via astroquery:**
```python
from astroquery.mast import Observations
obs = Observations.query_criteria(obs_collection='JWST',
                                  proposal_id=['1180', '6541'],
                                  dataproduct_type='image')
```

### 6.5 JWST Supernova Data Products

| Product | Description | Format |
|---------|-------------|--------|
| NIRCam images | Multi-epoch, multi-filter imaging | FITS (MJy/sr) |
| NIRSpec spectra | Prism spectra of transients + hosts | FITS 1D/2D |
| Difference images | Template-subtracted transient detection | FITS |
| Photometry catalogs | Aperture/PSF photometry of SNe | ASCII/CSV |

### 6.6 ML Readiness: JWST
- **Format**: Standard FITS (images), CSV (photometry)
- **Filters**: 6-9 NIRCam filters providing rest-frame UV through optical at z>1
- **Unique value**: First high-z SN sample with NIR spectroscopy; rest-frame UV at z>2
- **Limitations**: Small sample sizes currently; no dedicated time-domain survey yet
- **Best for**: High-z SN evolution, cosmological analyses, SN rate studies at z>2

---

## 7. HST (Hubble Space Telescope) - CANDELS + CLASH

### 7.1 Overview
HST's CANDELS and CLASH Multi-Cycle Treasury programs provided the first substantial sample of high-redshift SNe Ia with rest-frame optical-NIR photometry, extending the SN Hubble diagram to z>1 [^20^][^21^].

### 7.2 CANDELS + CLASH Supernova Program

**Survey design:**
- CANDELS: 5 fields (GOODS-S/N, COSMOS, UDS, EGS), ~0.25 deg^2
- CLASH: 25 galaxy cluster fields + 13 parallel fields
- Cadence: ~50 days between epochs
- Instruments: ACS (optical) + WFC3-IR (0.8-1.7 um)
- Filters: F606W, F814W, F125W, F140W, F160W

**Key results:**
- **65 SNe** discovered in CANDELS (out to z=2.5) [^21^]
- **27 SNe** in CLASH parallel fields
- **15 likely SNe Ia at z>1**, 9 with reliable distance estimates
- Riess et al. 2018: H0 measurement with high-z anchor

### 7.3 Data Access

**MAST**: https://archive.stsci.edu/
- Search by program ID: 12060, 12061, 12062, 12442, 12443, 12444, 12445, 12099, 12461, 13063
- Hubble Legacy Archive (HLA): Enhanced data products
- **Rodney et al. 2014 catalog**: VizieR catalog of 65 CANDELS SNe

**Photometry tables**: Published in Riess et al. 2018 appendix (Table 8) - CANDELS+CLASH Light-curve Photometry with magnitudes, errors, and MJD for each epoch.

### 7.4 ML Readiness: HST
- **Format**: FITS images + ASCII photometry tables
- **Filters**: ACS optical + WFC3 NIR (rest-frame optical at high z)
- **Unique value**: First large z>1 SN Ia sample; cosmological-quality photometry
- **Limitations**: Legacy data; low cadence (~50 days); relatively small sample
- **Best for**: Cosmological training sets, high-z SN evolution, Hubble diagram construction

---

## 8. Cross-Matching Space-based and Ground-based Data

### 8.1 Why Cross-Matching Matters for ML

Combining space-based and ground-based observations creates richer feature vectors for ML classification:
- **UV from space** + **optical/NIR from ground** = full bolometric SED
- **High cadence from space** + **multi-filter from ground** = temporally and spectrally resolved
- **Early-time space data** + **late-time ground data** = complete light curve coverage

### 8.2 Cross-Matching Strategies

**1. Coordinate-based matching:**
```python
from astropy.coordinates import SkyCoord
from astropy import units as u
# Match space-based catalog to ground-based catalog
space_coords = SkyCoord(ra_space, dec_space, unit=u.deg)
ground_coords = SkyCoord(ra_ground, dec_ground, unit=u.deg)
idx, d2d, _ = space_coords.match_to_catalog_sky(ground_coords)
matches = d2d < 1.0 * u.arcsec
```

**2. Time-domain cross-matching tools:**
- **BHTOM**: Black Hole Target Observation Manager integrates multi-wavelength time-domain archives including Swift/UVOT, GALEX, ZTF, Gaia, and NEOWISE [^22^]
- **MAST Crossmatch**: Cross-match with Gaia, Pan-STARRS, SDSS catalogs
- **TNS cross-matching**: Transient Name Server provides unified names

**3. Key cross-matched datasets:**

| Space | Ground | Cross-match Value |
|-------|--------|-------------------|
| Swift UVOT | ZTF/ATLAS | UV-optical color evolution |
| TESS | ZTF/ASAS-SN | Early rise + multi-color |
| Gaia BP/RP | PS1/SDSS | Low-res spectra + host photometry |
| GALEX | SDSS host catalogs | UV history + host properties |
| JWST | HST archival | Multi-epoch high-z SN SEDs |

### 8.3 Building Multi-wavelength Feature Vectors

For ML classification, a combined feature vector might include:
```
Features = [UVW2_mag, UVM2_mag, UVW1_mag, U_mag, B_mag, V_mag,   # Swift
            TESS_mag,                                                  # TESS
            G_mag, BP_mag, RP_mag,                                    # Gaia
            g_mag, r_mag, i_mag, z_mag,                               # Ground
            UVW2-V_color, UVW1-U_color, U-V_color,                    # Colors
            rise_rate, decline_rate,                                   # Light curve shape
            host_photoz, host_mass, host_sfr]                         # Host properties
```

---

## 9. High-Cadence Light Curve Features for Early-Time Classification

### 9.1 Early-Time Features from Space Data

Space-based high-cadence data enables unique early-time features for ML [^23^][^24^]:

**Power law rise features:**
- Rise law index: beta in F ~ (t-t0)^beta
- Fireball model: beta=2 (adiabatic expansion)
- Observed range: beta = 0.5 to 3.0 (Fausnaugh et al. 2023)
- Second derivative of magnitude rate: curvature of early rise

**Companion interaction features:**
- Flux excess above power law (detected in SN 2018oh, SN 2017cbv)
- Duration and amplitude of excess emission
- Color evolution during excess (blue = interaction signature)

**Shock breakout features:**
- Rapid initial peak (<1 day for compact progenitors)
- Temperature evolution from UV to optical
- Only detectable with continuous high-cadence monitoring

### 9.2 Feature Extraction Pipeline

```python
# Example feature extraction from high-cadence data
def extract_early_time_features(time, flux, flux_err, discovery_time):
    """Extract ML features from early-time light curve"""
    # Phase relative to estimated explosion
    phase = time - discovery_time
    
    # Power law fit
    log_phase = np.log10(phase[phase > 0])
    log_flux = np.log10(flux[phase > 0])
    beta, _ = np.polyfit(log_phase, log_flux, 1)
    
    # Rise rate features
    mag = -2.5 * np.log10(flux)
    mag_rate = np.gradient(mag) / np.gradient(time)
    
    features = {
        'beta': beta,                          # Power law index
        'mean_rise_rate': np.mean(mag_rate[:5]), # Early rise rate
        'max_rise_rate': np.max(mag_rate),
        'rise_curvature': np.gradient(mag_rate)[0], # Second derivative
        'time_to_peak': time[np.argmax(flux)] - discovery_time,
        'flux_excess': detect_excess(flux, beta), # Companion interaction
    }
    return features
```

### 9.3 Classification Performance

Recent studies show early-time classification is feasible with limited data points [^23^][^24^]:
- **3 photometric points**: Random forest achieves ~82% accuracy (Ia vs II vs Ib/c)
- **5 points with colors**: ~90% accuracy
- **With host galaxy info**: Improved precision for ambiguous cases
- **Key features**: Slope (magnitude rate), curvature, color at first detection

---

## 10. UV/Optical Color Evolution as Classification Feature

### 10.1 UV Colors for SN Classification

The UV wavelength range provides strong discriminatory power between SN types [^7^][^10^]:

| Color | SN Ia | SN II-P | SN Ib/c | Diagnostic |
|-------|-------|---------|---------|------------|
| UVW2-V (early) | Blue (~-1) | Very blue initially | Variable | Type separation |
| UVW1-U | Moderate blue | Rapidly reddening | Blue | Temperature evolution |
| U-B | Reddening slowly | Rapidly reddening | Variable | Cooling rate |
| UVW2-UVW1 | ~0 (flat) | Blue excess | Variable | Line blanketing |

### 10.2 Color-Evolution Features for ML

Derived from multi-epoch, multi-filter observations:

1. **Early color** (first detection): UV-optical color at explosion
2. **Color slope**: d(color)/dt in first 10 days
3. **Color at peak**: UV-optical color at maximum light
4. **Color decline rate**: How fast colors redden post-peak
5. **UV decay rate**: Decline in UVW2, UVM2, UVW1 (faster = more line blanketing)

### 10.3 Swift Color-Based Classification

The Swift UVOT sample demonstrates that UV colors can effectively classify SNe [^7^]:
- **UVW2-U vs U-V color-color diagrams** separate Ia, II-P, and Ib/c
- **Temporal evolution** of colors adds additional discriminatory power
- **UV-bright events** (super-Chandra, 91T-like) stand out in UVW2-V

---

## 11. Summary Table: All Space-based SN Datasets for ML

| Dataset | N SNe | Bands | Cadence | Format | Access URL | ML Best Use |
|---------|-------|-------|---------|--------|------------|-------------|
| **TESS** | 307 Ia + thousands | 1 (600-1000nm) | 30 min | ASCII API | tess.mit.edu/public/tesstransients | Early rise morphology |
| **Kepler/K2** | 23+ | 1 (430-890nm) | 30 min | FITS @ MAST | archive.stsci.edu/kepler | Shock breakout; progenitors |
| **Swift/SOUSA** | 253 | 6 (UV-optical) | ~2 days | FITS + ASCII | archive.stsci.edu/prepds/sousa | UV colors; SED evolution |
| **GALEX/gPhoton** | 1,080 Ia | 2 (NUV, FUV) | Variable | Photon lists | gPhoton @ MAST | UV bolometric; extinction |
| **Gaia Alerts** | 10,765 alerts | 1 + BP/RP spectra | ~monthly | CSV + spectra | gsaweb.ast.cam.ac.uk/alerts | Spectral classification; all-sky |
| **JWST** | 80+ | 6-9 NIR filters | ~1 year | FITS @ MAST | archive.stsci.edu | High-z SNe; cosmology |
| **HST CANDELS** | 65+ | 5 (optical-NIR) | ~50 days | FITS @ MAST | archive.stsci.edu | z>1 training; Hubble diagram |

---

## 12. Recommended ML Workflows

### 12.1 Early-Time Classification Pipeline

```
Input: New SN alert from ground survey (ZTF, ATLAS)
  |
  v
Query TESS/K2: Was it in the FFI field? [tess-point to check]
  |---> If yes: Download high-cadence light curve via API
  |         Extract: rise slope, beta, curvature, flux excess
  |
Query Swift/SOUSA: Is there UV coverage?
  |---> If yes: Download UVOT photometry
  |         Extract: UV colors, UV decay rate
  |
Query Gaia: Historical photometry + BP/RP spectra?
  |---> If yes: Extract spectral features, color evolution
  |
  v
Feature vector: [rise_params, uv_colors, spectral_features, host_props]
  |
  v
Classifier: Random Forest / XGBoost / Neural Network
  |
  v
Output: P(Ia), P(II), P(Ib/c), P(other)
```

### 12.2 Multi-wavelength SED Classification

```
Input: SN position + discovery epoch
  |
  v
Collect all available photometry:
  - GALEX (NUV, FUV) - historical UV
  - Swift UVOT (UVW2, UVM2, UVW1, U, B, V) - targeted UV-optical
  - Ground (griz, UBVRI) - optical
  - TESS/Kepler - high-cadence optical
  - Gaia (G, BP, RP) - low-res spectra
  - HST/JWST (if high-z) - NIR
  |
  v
Build SED at each epoch
  |
  v
Features: [color_evolution, sed_slope, bolometric_luminosity,
           uv_to_optical_ratio, temperature_evolution]
  |
  v
Classifier trained on Swift + ground sample
  |
  v
Output: SN type + physical parameters
```

---

## 13. Key Software and Tools

| Tool | Purpose | URL |
|------|---------|-----|
| **lightkurve** | Kepler/TESS light curve analysis | github.com/lightkurve/lightkurve |
| **eleanor** | TESS FFI extraction | github.com/afeinstein20/eleanor |
| **tess-point** | Find TESS sector for RA/Dec | github.com/christopherburke/tess-point |
| **gPhoton/gPhoton2** | GALEX photon data analysis | github.com/cmillion/gPhoton, github.com/MillionConcepts/gPhoton2 |
| **HEASoft/uvotsource** | Swift UVOT photometry | heasarc.gsfc.nasa.gov/ftools |
| **astroquery.mast** | MAST data access | astropy.org/astroquery |
| **astroquery.gaia** | Gaia archive queries | astropy.org/astroquery |
| **sncosmo** | SN light curve fitting | sncosmo.readthedocs.io |
| **TNS_py** | Transient Name Server queries | (custom web scraping) |

---

## 14. Flagged Areas for Deeper Investigation

1. **JWST time-domain programs**: No dedicated JWST time-domain survey exists yet; serendipitous detections in deep fields will continue to grow. Monitor MAST for new programs.

2. **Roman Space Telescope**: The Nancy Grace Roman Space Telescope (launch ~2027) will have a Wide Field Instrument capable of discovering thousands of high-z SNe Ia. Prepare for early data access.

3. **TESS extended mission**: 10-minute cadence FFIs from Sectors 27+ provide even better early-time coverage. TessTransients database continues to grow.

4. **SOUSA expansion**: The SOUSA team continues to reprocess archival Swift data; the sample will grow beyond 253 SNe.

5. **Gaia DR4**: Expected ~2026, will include full alert data and improved BP/RP spectra calibration.

6. **ULTRASAT**: Upcoming UV transient satellite (launch ~2026) will provide wide-field UV time-domain data complementary to Swift.

7. **Cross-survey feature engineering**: Systematic combination of space-based UV with ground-based optical features for classification remains an active area of research with significant ML potential.

---

## References

[^1^]: Fausnaugh et al. 2021, ApJ, 908, 51. "Early-time Light Curves of Type Ia Supernovae Observed with TESS"
[^2^]: Vallely et al. 2021, MNRAS, 500, 5639. "High-cadence, early-time observations of core-collapse supernovae from TESS"
[^3^]: TessTransients Database, https://tess.mit.edu/public/tesstransients/
[^4^]: TessTransients README, https://tess.mit.edu/public/tesstransients/pages/readme.html
[^5^]: Garnavich et al. 2016, ApJ, 820, 23. "Shock Breakout and Early Light Curves of Type II-P Supernovae Observed with Kepler"
[^6^]: Dimitriadis et al. 2019, ApJ, 870, 37. "K2 Observations of SN 2018oh Reveal a Two-Component Rising Light Curve"
[^7^]: Brown et al. 2009, AJ, 137, 4517. "Ultraviolet Light Curves of Supernovae with the Swift UVOT"
[^8^]: SOUSA at MAST, https://archive.stsci.edu/prepds/sousa/
[^9^]: Brown et al. 2014, Ap&SS, 354, 89. "SOUSA: The Swift Optical/Ultraviolet Supernova Archive"
[^10^]: Devarakonda et al. 2022, AJ, 164, 19. "Comparisons of Type Ia Supernova Light Curves in the UV and Optical"
[^11^]: Million et al. 2016, ApJ, 833, 292. "gPhoton: The GALEX Photon Data Archive"
[^12^]: gPhoton2, https://github.com/MillionConcepts/gPhoton2
[^13^]: Million et al. 2024, A&A, 687, A32. "The time-variable ultraviolet sky"
[^14^]: Hodgkin et al. 2021, A&A, 652, A76. "Gaia Early Data Release 3: Photometric Science Alerts"
[^15^]: Gaia Alerts, https://gsaweb.ast.cam.ac.uk/alerts/
[^16^]: Cambridge Photometric Calibration Server, http://gsaweb.ast.cam.ac.uk/followup/
[^17^]: Blagorodnova et al. 2014, arXiv:1406.0857. "GS-TEC: Spectral classification for Gaia"
[^18^]: Eisenstein et al. 2023, ApJ, 946, L1. "Overview of the JWST Advanced Deep Extragalactic Survey"
[^19^]: DeCoursey et al. 2025, ApJ, submitted. "Wide-Area JWST Discoveries from COSMOS-Web"
[^20^]: Riess et al. 2018, ApJ, 853, 126. "Type Ia Supernova Distances at Redshift >1.5 from HST"
[^21^]: Rodney et al. 2014, AJ, 148, 13. "Type Ia Supernova Rate Measurements from CANDELS"
[^22^]: BHTOM, https://bhtom.space/ (Wyrzykowski et al. 2025)
[^23^]: Gagliano et al. 2023, ApJ, 953, 94. "First Impressions: Early-time Classification of Supernovae"
[^24^]: Martinez-Palomera et al. 2026, A&A, submitted. "ML for early classification of broad-lined Ic supernovae"

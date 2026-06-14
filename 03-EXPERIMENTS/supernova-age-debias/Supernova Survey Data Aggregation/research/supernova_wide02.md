## Facet: Major Cosmological & Deep Field Supernova Surveys

**Research Date**: 2026-01-18
**Researcher**: Astro Data Research Agent
**Searches Conducted**: 15+ independent web searches across survey official sites, arXiv, ADS, GitHub, data archives, and publication databases

---

## Key Findings

### Summary of Major Cosmological/Deep-Field Supernova Surveys with Public Data

This document catalogs **19 major supernova surveys and 6 compilation datasets** designed primarily for cosmology using Type Ia supernovae as standard candles. These datasets collectively contain **>50,000 SNe candidates**, with **>10,000 spectroscopically confirmed SNe Ia**, spanning redshifts from z~0.003 to z~2.3. The data include multi-band photometric light curves, spectroscopic observations, host galaxy properties, and derived distance moduli.

### Key Statistics at a Glance

| Survey/Compilation | SNe Ia Count | Redshift Range | Filters | Data Format | Access URL |
|---|---|---|---|---|---|
| **SDSS-II SN Survey** | 4,607 candidates (1,443 spec-Ia) | 0.05-0.4 | ugriz | FITS/ASCII | classic.sdss.org/drsn |
| **DES-SN5YR** | ~1,635 cosmology-grade | 0.1-1.13 | griz | FITS/ASCII | github.com/des-science/DES-SN5YR |
| **SNLS5** | ~400+ spec-Ia | 0.1-1.0 | u*g'r'i'z' | ASCII/FITS | CDS/VizieR |
| **ESSENCE** | ~200 spec-Ia | 0.2-0.8 | R,I | ASCII/FITS | ESO archive |
| **CSP DR3** | 134 SNe (123 Ia) | 0.004-0.08 | ugriBVYJH | ASCII | csp.obs.carnegiescience.edu/data |
| **CfA Archive** | 2,603 Ia spectra; thousands of LCs | 0.003-0.1 | UBVRIJHK | ASCII/FITS | lweb.cfa.harvard.edu/supernova/ |
| **PS1 MDS** | 365 spec-confirmed Ia | 0.03-0.68 | grizy | FITS | Foundation DR1 / Pan-STARRS |
| **Foundation DR1** | 225 Ia (180 cosmology) | 0.01-0.08 | griz_PS1 | FITS | github.com/djones1040/Foundation_DR1 |
| **ZTF SN Ia DR2** | 3,628 spec-confirmed Ia | 0.01-0.3 | gri | FITS/ASCII | ztfcosmo.in2p3.fr |
| **HSC-SSP Transient** | 1,824 candidates (433 Ia) | 0.1-2.0 | grizy | FITS | HSC data release |
| **HST High-z (Riess)** | 23 Ia at z>1 | 1.0-1.55 | F775W,F850LP | ASCII | stsci.edu/~ariess |
| **CANDELS/CLASH** | ~24 Ia | 0.5-2.5 | F125W,F160W | FITS | MAST archive |
| **SNfactory** | 300+ Ia (spec-phot time series) | 0.02-0.08 | 3300-8600A | FITS | cdsarc.u-strasbg.fr |
| **Pantheon** | 1,048 Ia | 0.01-2.3 | multi | ASCII/FITS | GitHub |
| **Pantheon+** | 1,701 Ia (18 surveys) | 0.0008-2.26 | multi | ASCII/FITS | github.com/PantheonPlusSH0ES |
| **Union2.1** | 833 Ia | 0.015-1.4 | multi | ASCII | supernova.lbl.gov/Union |
| **Union3** | 2,087 Ia (24 surveys) | 0.01-2.26 | multi | ASCII/FITS | UNITY1.5 framework |
| **JLA** | 740 Ia (SDSS+SNLS+low-z) | 0.01-1.0 | multi | ASCII | cdsarc.u-strasbg.fr |
| **Open SN Catalog** | 50,000+ SNe candidates | 0-8+ | multi | JSON | github.com/astrocatalogs |

---

## Detailed Survey Catalog

---

### 1. Sloan Digital Sky Survey-II (SDSS-II) Supernova Survey

**Description**: The SDSS-II Supernova Survey was a time-domain survey conducted between 2005 and 2007 that repeatedly imaged SDSS Stripe 82 (a 300 deg^2 area along the celestial equator) to discover and monitor supernovae. It was one of the first large-scale digital supernova surveys specifically designed for cosmology. [^132^] [^135^]

- **Official Website**: https://classic.sdss.org/drsn/
- **Data Access Portal**: https://dr15.sdss.org/sas/dr15/eboss/supernova/ and https://www.sdss4.org/dr15/data_access/supernovae/
- **Principal References**: Sako et al. 2014, 2018 (data release); Frieman et al. 2008 (technical summary); Sako et al. 2008 (search algorithm) [^132^] [^135^] [^137^]

#### Data Releases
- **Sako et al. 2014 (DR1)**: Initial data release with light curves and classifications
- **Sako et al. 2018 (Full DR)**: Complete photometric and spectroscopic data release [^135^]
  - 10,258 variable and transient sources discovered
  - 4,607 SNe candidates (spectroscopically confirmed or photometrically classified)
  - 889 transients with spectroscopic observations
  - 1,443 SNe Ia with spectroscopic redshifts and SALT2 distance moduli
  - 677 purely photometric SNe Ia candidates with photometric redshifts

#### SN Type Breakdown
- ~1,443 SNe Ia with spectroscopic redshifts
- ~677 photometric SNe Ia candidates
- ~80 spectroscopically confirmed core-collapse SNe (Ib/c and II)
- Plus thousands of other variable/transient sources

#### Filter Bands and Cadence
- **Filters**: ugriz (Sloan filter system)
- **Cadence**: Every other night, weather permitting, for ~3 months/year (Sep/Oct/Nov) for 3 years
- **Limiting magnitude**: r ~ 22.5 mag
- **Redshift range**: z = 0.05 - 0.4 (median z ~ 0.2)

#### Data Products and Format
- **Photometry**: ugriz light curves in FITS and ASCII formats
- **Spectra**: Spectroscopic observations of 889 transients plus host galaxy spectra from BOSS
- **Classifications**: Both spectroscopic and photometric classifications provided
- **Host galaxies**: Host identification with stellar masses, SFRs, stellar population ages
- **Distance moduli**: SALT2 distance moduli for 1,443 SNe Ia + 677 photometric candidates
- **Access method**: Bulk download via SAS (Science Archive Server) [^129^] [^130^] [^132^]

#### Ancillary Data
- Stripe 82 coadded reference images
- Corrected frames (fpC), calibrated object catalogs (tsObj)
- Host galaxy photometry and redshifts from SDSS
- Classification probabilities from photometric classifiers

#### ML Readiness
- **High**. One of the most-used training datasets for SN classification ML. The large, homogeneous sample with both spectroscopic and photometric classifications makes it ideal for training classification algorithms. Format is standard FITS/ASCII. Integrated into SNANA, SNCosmo, sndata, and other analysis frameworks. [^53^] [^54^] [^135^]

#### Key Cosmological Papers
- Sako et al. 2018: "The Data Release of the Sloan Digital Sky Survey-II Supernova Survey" (Omega_M = 0.315 +/- 0.093) [^132^]
- Kessler et al. 2009: First-year cosmological results
- Betoule et al. 2014 (JLA): Combined with SNLS for improved cosmology

---

### 2. Dark Energy Survey (DES) Supernova Program

**Description**: The Dark Energy Survey Supernova Program used the Dark Energy Camera (DECam) on the Blanco 4m telescope at CTIO to conduct a 5-year rolling search for supernovae, producing the largest single-instrument sample of cosmological SNe Ia ever assembled. [^14^] [^21^]

- **Official Website**: https://www.darkenergysurvey.org/des-year-3-supernova-cosmology-results/
- **5YR Data Access**: https://github.com/des-science/DES-SN5YR
- **Zenodo DOI**: 10.5281/zenodo.12720777
- **Principal References**: Sanchez et al. 2024 (light curves & DR); Vincenzi et al. 2024 (cosmology); Popovic et al. 2025 (DES-Dovekie reanalysis) [^10^] [^14^] [^21^]

#### Data Releases
- **DES-SN3YR**: Initial 3-year cosmology results (2018), ~207 spectroscopically confirmed SNe Ia [^24^]
- **DES-SN5YR** (2024): Full 5-year data release [^14^] [^21^]
  - 31,636 DiffImg light curves + 19,706 SMP light curves
  - 1,635 photometrically classified SNe passing cosmology cuts
  - Redshift range: z = 0.1 - 1.13 (largest z-range from single survey)
  - 25 DES mock simulations included
  - Classification probabilities for 1,635 SNe
  - STAT and STAT+SYST covariance matrices
  - SNANA-format light curves and distance moduli
- **DES-Dovekie** (2025): Reanalysis with improved calibration [^10^]
  - ~1,600 likely SNe Ia from DES + ~200 low-z from other surveys
  - Omega_M = 0.330 +/- 0.015 (Flat LCDM)
  - Evidence for evolving dark energy at 3.2 sigma

#### Filter Bands and Cadence
- **Filters**: griz (DECam filters)
- **Cadence**: Rolling search with ~weekly observations in each field
- **Area**: ~27 deg^2 (deep fields) + wider shallow fields
- **Limiting magnitude**: r ~ 24 (deep fields)

#### Data Format and Access
- **Format**: FITS tables, SNANA-format .DAT files, ASCII .FITRES files
- **Access method**: GitHub repository (github.com/des-science/DES-SN5YR) with full documentation
- **Contents**: Light curves, classification probabilities, distance moduli, covariance matrices, simulation inputs, Pippin pipeline files [^14^]
- **Tools**: SNANA, SNCosmo, sndata, Pippin pipelines [^53^] [^54^]

#### ML Readiness
- **Very High**. Designed with ML applications in mind. Provides:
  - 25 simulated mock datasets for training/testing classifiers
  - Pre-computed classification probabilities from multiple algorithms
  - SNANA simulations with both Ia and non-Ia light curves
  - Well-documented data format with full covariance matrices
  - GitHub repository includes complete reproduction materials

#### Key Cosmological Papers
- DES Collaboration 2024: "Constraints on Cosmological Parameters" (ApJL 973, L14) [^24^]
- Vincenzi et al. 2024: "Cosmological Analysis and Systematic Uncertainties" (ApJ 975, 86)
- Sanchez et al. 2024: "Light Curves and 5 Yr Data Release" (ApJ 975, 5) [^21^]
- Popovic et al. 2025 (MNRAS): DES-Dovekie reanalysis with updated calibration [^10^]

---

### 3. SuperNova Legacy Survey (SNLS)

**Description**: SNLS was a 5-year program using the MegaCam imager on the Canada-France-Hawaii Telescope (CFHT) to discover and monitor ~500 Type Ia supernovae for dark energy studies. It was one of the pioneering wide-field surveys for SN cosmology and formed the backbone of the JLA compilation. [^50^] [^51^]

- **Official Website**: https://www.cfht.hawaii.edu/Science/CFHLS/ and SNLS team pages
- **Data Access**: CDS/VizieR (http://cdsarc.u-strasbg.fr/), SNData package
- **Principal References**: Astier et al. 2006 (SNLS1); Guy et al. 2010 (SNLS3); Sullivan et al. 2011 (SNLS3 cosmology); Conley et al. 2011 (systematics); Regnault et al. (SNLS5) [^49^] [^50^] [^55^] [^57^] [^105^]

#### Data Releases
- **SNLS1** (Astier et al. 2006): 73 SNe Ia, first cosmological constraints
- **SNLS3** (Guy et al. 2010): 231 SNe Ia + 123 low-z + 101 SDSS = 495 total for cosmology [^105^]
  - Found w = -1.069 +/- 0.07 (with WMAP+BAO prior)
- **SNLS5**: ~400 SNe Ia from SNLS alone + 210 low-z + 380 SDSS + 10 HST [^105^]
  - Final SNLS sample with full 5 years of data

#### Spectroscopic Data
- Balland et al. 2009: 139 spectra of 124 SNe Ia from ESO/VLT (z=0.149-1.031, mean z=0.63) [^55^] [^57^]
- Additional spectroscopy from Gemini, Keck, and Magellan [^51^]

#### Filter Bands and Cadence
- **Filters**: u*, g', r', i', z' (MegaCam filter system)
- **Cadence**: Imaging every 3-4 days during dark time for ~6 lunations/year
- **Fields**: 4 deep fields (COSMOS, D1, D2, D3) from CFHT Legacy Survey Deep component
- **Depth**: AB ~ 24-25 (depending on filter)
- **Redshift range**: z = 0.1 - 1.0 (mean z ~ 0.6)

#### Data Format and Access
- **Photometry**: Available through CDS/VizieR and sndata Python package [^57^]
- **Spectra**: Balland et al. 2009 ESO/VLT spectra (ASCII/FITS via CDS) [^55^] [^57^]
- **Light curve fitter outputs**: SALT2 fits and distance moduli in JLA release
- **Access methods**: CDS/VizieR query service, sndata Python package, bulk download

#### Ancillary Data
- Deep CFHT Legacy Survey reference images for host galaxy subtraction
- Host galaxy photometry and redshifts from follow-up programs
- CFHT photometric calibration at <1% precision (T0007 release) [^49^]

#### ML Readiness
- **High**. SNLS data is integrated into multiple analysis frameworks:
  - sndata Python package provides programmatic access [^57^]
  - SNANA includes SNLS mock simulations
  - SALT2 training used SNLS data extensively
  - Well-calibrated multi-band photometry suitable for ML classification

#### Key Cosmological Papers
- Astier et al. 2006, A&A 447: 31 (SNLS1 cosmology)
- Guy et al. 2010, A&A 523: A7 (SNLS3 sample)
- Sullivan et al. 2011, ApJ 737: 102 (SNLS3 cosmology with CMB+BAO)
- Conley et al. 2011, ApJS 192: 1 (SNLS3 systematics)
- Betoule et al. 2014 (JLA): Combined SDSS+SNLS analysis [^105^]

---

### 4. ESSENCE (Equation of State: SupErNovae trace Cosmic Expansion)

**Description**: ESSENCE was a 6-year survey (2002-2007) using the CTIO 4m Blanco telescope to discover and follow ~200 Type Ia supernovae at z~0.5, designed to constrain the dark energy equation-of-state parameter w. [^17^] [^19^]

- **Official Website**: http://www.ctio.noao.edu/essence/ (archived)
- **Data Access**: ESO Science Archive (Phase 3) for FORS1 spectra; VizieR for light curves
- **Principal References**: Miknaitis et al. 2007 (survey description); Wood-Vasey et al. 2007 (first cosmology); Davis et al. 2007 (exotic cosmology); Foley et al. (spectroscopy in prep) [^17^] [^19^]

#### Data Releases
- **ESSENCE DR1**: Initial release of FORS1 spectra (Matheson et al. 2005)
- **ESSENCE DR2**: Revised FORS1 dataset + additional FORS1 spectra from program 176.A-0319 [^17^]
  - Spectroscopic data set of high-z SNe Ia from VLT/FORS1
  - Light curves published in Miknaitis et al. 2007
  - 102 spectroscopically confirmed SNe Ia in first 4 years

#### SN Type Breakdown
- ~200 SNe Ia targeted over 6 years
- 102 spectroscopically confirmed in first 4 years (z = 0.10-0.78)
- Primarily SNe Ia (survey designed for Ia cosmology)

#### Filter Bands and Cadence
- **Filters**: R, I (primarily); some multi-band follow-up
- **Cadence**: Optimized for z~0.5 SNe Ia (rest-frame B-band coverage)
- **Telescope**: CTIO 4m Blanco telescope + Mosaic-II imager
- **Redshift range**: z = 0.2 - 0.8 (optimal z ~ 0.5)

#### Data Format and Access
- **Spectra**: 1D spectra in FITS format via ESO Phase 3 archive [^17^]
- **Photometry**: Light curves in ASCII format via VizieR/Journal tables
- **Access method**: ESO archive query service, VizieR query
- **Note**: 7 science data products may have incorrect MJD-END, PROV1, NCOMBINE keywords [^17^]

#### Key Papers
- Miknaitis et al. 2007, ApJ 666: 674 (survey description and optimization) [^19^]
- Wood-Vasey et al. 2007, ApJ 666: 694 (first cosmological results: w = -1.05 +/- 0.13)
- Davis et al. 2007, ApJ 666: 716 (testing exotic cosmological models)
- Matheson et al. 2005, AJ 129: 2352 (first 2 years of spectroscopy)
- Krisciunas et al. 2005, AJ 130: 2453 (HST observations of 9 ESSENCE SNe)

---

### 5. Carnegie Supernova Project (CSP-I and CSP-II)

**Description**: The Carnegie Supernova Project conducted a 5-year program (2004-2009 for CSP-I) to obtain high-precision optical and near-infrared photometry and spectrophotometry of ~250 low-redshift supernovae. CSP-I focused on z < 0.1 SNe; CSP-II extended to higher redshifts (z < 0.7). The project is known for having the best-characterized photometric system and some of the highest-quality NIR SN data. [^101^] [^166^] [^167^] [^168^]

- **Official Website**: https://csp.obs.carnegiescience.edu/
- **Data Access**: https://csp.obs.carnegiescience.edu/data
- **Principal References**: Krisciunas et al. 2017 (DR3); Folatelli et al. 2013 (spectroscopic DR1); Contreras et al. 2010, Stritzinger et al. 2011 (earlier DRs); Phillips et al. (CSP-II) [^101^] [^166^] [^168^]

#### Data Releases
- **CSP DR1/DR2** (Stritzinger et al. 2011, Contreras et al. 2010): Initial photometry releases
- **CSP DR3** (Krisciunas et al. 2017, AJ 154, 211): Final and most complete release [^168^] [^172^]
  - 134 SNe with probable white dwarf progenitors
  - 123 Type Ia SNe, 5 Type Iax SNe, 2 super-Chandrasekhar candidates, 2 Ia-CSM, 2 2006bt-like
  - Optical (ugriBV) and NIR (YJH) photometry in natural system
  - Redshifts: z = 0.0037 - 0.0835 (median z = 0.0241)
  - NIR photometry for 120 (90%) of the SNe
  - Local sequences of tertiary standard stars for each SN
- **CSP-II**: Near-infrared spectral diversity and templates [^142^]
  - NIR Ia spectral templates (Lu et al. 2023)
  - Stripped-envelope SNe NIR spectra (Shahbandeh et al. 2022)
  - Type II SNe bolometric light curves (Martinez et al. 2021)

#### Filter Bands and Cadence
- **Filters**: u'g'r'i'BV (optical) + YJH (NIR) in natural system
- **Telescopes**: Las Campanas Observatory (Swope + du Pont telescopes)
- **Photometric precision**: Better than 1-2% relative calibration
- **Redshift range**: z = 0.0037 - 0.0835 (CSP-I)

#### Data Format and Access
- **Format**: ASCII text files (photometry), tar.gz archives
- **Bulk download**: CSP_Photometry_DR3.tgz (~hundreds of MB) [^142^]
- **Spectroscopic data**: CSP_spectra_Folatelli+2013.tgz
- **Access method**: Direct download from CSP website; also via sndata Python package [^101^] [^166^]
- **Filter definitions**: https://csp.obs.carnegiescience.edu/data/filters

#### Ancillary Data
- Filter transmission functions and zero-points
- Natural-to-standard system color terms
- Local standard star sequences for each SN
- Y-band calibration of Persson et al. standards
- SNooPy light curve fitting software [^142^]

#### ML Readiness
- **High**. CSP data is widely used for SN Ia standardization studies:
  - Integrated into sndata Python package with programmatic API [^166^]
  - NIR templates used for training light curve models
  - Well-calibrated, homogeneous photometry ideal for regression tasks
  - Foundation of many low-z anchor samples in cosmological analyses

#### Key Cosmological Papers
- Krisciunas et al. 2017, AJ 154: 211 (DR3 description, 309 citations) [^168^]
- Folatelli et al. 2013 (spectroscopic DR1)
- Contreras et al. 2010, AJ 139: 519 (CSP-I early results)
- Stritzinger et al. 2011, AJ 142: 156 (CSP-I DR2)
- Burns et al. 2018 (CSPMCMC Hubble constant measurement) [^142^]

---

### 6. Harvard-Smithsonian Center for Astrophysics (CfA) Supernova Program

**Description**: The CfA Supernova Program has been collecting optical and near-infrared photometry and spectroscopy of nearby supernovae since the 1990s, producing the CfA1-CfA4 data releases. The archive contains one of the largest collections of SN spectra and light curves in the world. [^22^] [^104^]

- **Official Website**: https://lweb.cfa.harvard.edu/supernova/
- **Archive**: https://lweb.cfa.harvard.edu/supernova/SNarchive.html
- **Principal References**: Hicken et al. 2009a,b (CfA3); Hicken et al. 2012 (CfA4); Blondin et al. 2012 (spectral diversity); Jha et al. 2006 (CfA1/CfA2); Riess et al. 1999 (CfA high-z); Bianco et al. 2014 (stripped-envelope SNe) [^22^] [^104^]

#### Data Releases
- **CfA1/CfA2** (Jha et al. 2006; Riess et al. 1999): Early photometry releases
  - BVRI light curves for ~100 SNe Ia
- **CfA3** (Hicken et al. 2009a, 2009b): UBVRI light curves
  - Expanded sample with improved photometry
- **CfA4** (Hicken et al. 2012): 94 Type Ia SNe with UBVRI light curves
  - Blondin et al. 2012: 2,603 spectra of 462 SNe Ia [^104^]
  - Matheson et al. 2008: CfA SN Ia spectra compilation
- **Type II SNe** (Hicken et al. 2017): Light curves and spectra for Type II SNe
- **Stripped-envelope SNe** (Bianco et al. 2014): 64 stripped-envelope core-collapse SNe with optical+NIR LCs + 645 spectra of 73 stripped SNe (Modjaz et al. 2014) [^104^]

#### Spectroscopic Archive
- 2,603 spectra of 462 SNe Ia (Blondin et al. 2012) [^104^]
- 645 spectra of 73 stripped-envelope SNe (Modjaz et al. 2014)
- Maximum-light SN Ia spectra from Blondin, Mandel & Kirshner
- FAST spectra from September 2008-2019 in FITS format

#### Filter Bands
- **Filters**: UBVRI (standard Johnson-Cousins system), some JHK
- **Redshift range**: z ~ 0.003 - 0.1 (nearby sample)

#### Data Format and Access
- **Light curves**: ASCII format (natural and standard systems)
- **Spectra**: FITS format with uncertainties; also ASCII and PDF [^104^]
- **Bulk download**: Tar files available from archive page [^104^]
  - IR SNTEMPLATES: 4.2 GB
  - Raw stacked data: 33 GB total
  - CfA4 light curves + spectra: various sizes
- **Individual SN access**: Searchable table with per-SN light curves and spectra
- **Access method**: HTTP direct download from archive; also via SNCosmo/sndata [^27^] [^104^]

#### ML Readiness
- **Very High**. One of the most comprehensive SN archives:
  - Large, diverse sample spanning all major SN types
  - Both photometry and spectroscopy available
  - Standard filter systems enable easy cross-survey comparison
  - Directly integrated into SNCosmo and sndata
  - Blondin et al. 2012 spectral diversity paper provides feature measurements

#### Key Papers
- Hicken et al. 2009a, 2009b (CfA3): "Improved Photometry" (ApJ 700: 331)
- Hicken et al. 2012 (CfA4): "Light Curves for 94 Type Ia Supernovae"
- Blondin et al. 2012: "The Spectroscopic Diversity of Type Ia Supernovae" (AJ 143: 126) [^104^]
- Bianco et al. 2014: "Multi-color Optical and NIR Light Curves of 64 Stripped-envelope Core-Collapse SNe" (ApJS 213: 19) [^104^]
- Jha et al. 2006: "CfA1 and CfA2 Light Curves"

---

### 7. Pan-STARRS1 (PS1) Medium Deep Survey (MDS)

**Description**: The Pan-STARRS1 Medium Deep Survey covered 10 fields (70 deg^2) in 5 bands (grizy) over 4 years, discovering ~5,200 likely SNe with ~350 spectroscopically classified SNe Ia. The PS1 data forms the backbone of the Pantheon sample and Foundation Survey. [^133^] [^134^]

- **Official Website**: https://panstarrs.stsci.edu/
- **Data Access**: Available via Pantheon and Foundation data releases; MDS data via Pan-STARRS archive
- **Principal References**: Scolnic et al. 2018 (Pantheon); Rest et al. 2014 (PS1 SN discoveries); Chambers et al. 2016 (PS1 survey overview); Jones et al. 2017, 2018 (photometric cosmology) [^133^] [^134^]

#### Data Releases
- **PS1 MDS SN Sample**: 365 spectroscopically confirmed SNe Ia (Scolnic et al. 2018/Pantheon) [^133^]
  - 279 PS1 SNe Ia with useful distance estimates (0.03 < z < 0.68)
  - Combined with SDSS, SNLS, low-z, HST for Pantheon (1,048 total)
- **Jones et al. 2018**: 1,169 SNe Ia (photometric + spectroscopic) used for cosmology
- **Foundation DR1** (Foley et al. 2018): 225 SNe Ia from PS1 telescope [^103^] [^106^]

#### Filter Bands and Cadence
- **Filters**: g_P1, r_P1, i_P1, z_P1, y_P1 (PS1 filter system)
- **Cadence**: g+r on same night, i+z on next nights; y during bright time
- **Typical cadence**: ~6 observations per 10 days per field
- **Depth**: r ~ 23.5 (limiting)
- **Redshift range**: z = 0.03 - 0.68

#### Data Format and Access
- **Format**: SNANA-format FITS files, ASCII
- **Access**: Through Pantheon GitHub, Foundation DR1 GitHub [^103^]
  - https://github.com/djones1040/Foundation_DR1
  - https://github.com/PantheonPlusSH0ES/DataRelease
- **Calibration**: Supercal method for cross-survey calibration; sub-1% relative calibration across 3pi sr [^134^]

#### Key Cosmological Papers
- Scolnic et al. 2018, ApJ 859: 101 (Pantheon: Omega_M = 0.307 +/- 0.012, w = -1.026 +/- 0.041) [^133^]
- Jones et al. 2018, ApJ 857: 51 (PS1 photometric cosmology: w = -0.989 +/- 0.057)
- Rest et al. 2014, ApJ 795: 44 (PS1 MDS SN discoveries)

---

### 8. Foundation Supernova Survey

**Description**: The Foundation Survey used the Pan-STARRS1 telescope to obtain extremely well-calibrated, homogeneous light curves of low-redshift SNe Ia to serve as anchors for cosmological analyses. It was designed to replace the heterogeneous low-z sample used in previous cosmological analyses. [^103^] [^106^]

- **Official Website**: https://github.com/djones1040/Foundation_DR1
- **Principal References**: Foley et al. 2018 (MNRAS 475: 193); Jones et al. 2019 (ApJ 881: 19) [^103^] [^106^]

#### Data Release
- **Foundation DR1**: 225 SNe Ia total
  - 180 pass cosmology quality cuts
  - 175 at z > 0.015 suitable for cosmological analysis
  - Observed in griz_PS1 with median cadence of 8 days (5.5 days within 10 days of peak)

#### Filter Bands and Cadence
- **Filters**: griz_PS1 (Pan-STARRS1 filter system)
- **Cadence**: Median 8 days overall, 5.5 days within 10 days of peak
- **Telescope**: Pan-STARRS1 1.8m telescope (Haleakala)
- **Redshift range**: z ~ 0.01 - 0.08

#### Data Format and Access
- **Format**: SNANA .DAT files with FITS headers [^103^]
- **Access method**: GitHub repository (github.com/djones1040/Foundation_DR1)
- **Contents**: Light curves, SALT2 fit parameters, host galaxy masses, peculiar velocities, Milky Way reddening
- **Calibration**: 1.5% error floor added in quadrature to photometry; Pan-STARRS filter functions from Jones et al. 2019 [^103^]

#### Ancillary Data
- Host galaxy stellar masses from ZPEG SED-fitting
- Peculiar velocity corrections from Carrick et al. 2015 model
- Milky Way E(B-V) from Schlafly & Finkbeiner 2011

#### Key Papers
- Foley et al. 2018, MNRAS 475: 193 (Foundation Survey: Measuring Cosmological Parameters)
- Jones et al. 2019, ApJ 881: 19 (Foundation + PS1 MDS cosmology)

---

### 9. Subaru/Hyper Suprime-Cam (HSC) Strategic Survey Program (SSP) Transient Survey

**Description**: The HSC-SSP transient survey used the 8.2m Subaru Telescope with HSC to conduct deep transient surveys in the COSMOS and SXDS fields. The deep layers reach r~26-27, enabling detection of SNe Ia to z>1. The survey has produced one of the largest samples of high-z SNe Ia, doubling the number at z>1. [^12^] [^13^] [^18^]

- **Official Website**: https://hsc.mtk.nao.ac.jp/ssp/survey/
- **Principal References**: Yasuda et al. 2019 (COSMOS transient survey); Tanaka et al. 2016; Aihara et al. 2018 (HSC data release); Morokuma et al. (ML classification) [^12^] [^13^] [^18^] [^20^]

#### Data Releases
- **HSC-SSP Transient COSMOS**: 1,824 SN candidates [^18^]
  - 433 classified as Type Ia SNe
  - 129 with spectroscopic or photometric redshifts
  - 58 SNe Ia at z > 1 (doubles the known z>1 SN Ia sample)
  - Ultra-deep layer: 26.4, 26.3, 26.0, 25.6, 24.6 mag (g,r,i,z,y)
- **HSC Rapid Transients**: 3381 total SN candidates in COSMOS + SXDS [^13^]
  - Systematic search for rapid transients using random forest classifier

#### Filter Bands and Cadence
- **Filters**: g, r, i, z, y (+ 4 narrow-band filters in deep fields)
- **Cadence**: High-cadence survey with 1-hour intervals (for shock breakout studies)
- **Fields**: COSMOS (1.77 deg^2 ultra-deep, 5.78 deg^2 deep) and SXDS
- **Depth**: r ~ 26 (deep), r ~ 27-28 (ultra-deep)
- **Redshift range**: z = 0.1 - 2.0+

#### Data Format and Access
- **Format**: HSC pipeline output (FITS tables)
- **Access method**: HSC data release server (https://hsc-release.mtk.nao.ac.jp/)
- **Processing**: HSC pipeline (Juric et al. 2017; Bosch et al. 2018) [^13^]
- **Classification**: CNN for real/bogus classification; RF classifier for SN typing [^13^] [^20^]

#### ML-Specific Features
- CNN-based real/bogus classification (first demonstrated on HSC data) [^20^]
- Random forest classifier for SN type classification using SALT2 parameters
- Machine learning techniques pioneered on this dataset for LSST preparation

#### Key Papers
- Yasuda et al. 2019, PASJ 71: 74 (HSC-SSP transient survey in COSMOS) [^18^]
- Tanaka et al. 2016, ApJ 819: 5 (HSC SNe)
- Aihara et al. 2018, PASJ 70: S4 (HSC first data release)
- Morokuma et al. 2016, PASJ 68: 40 (AGN variability) [^20^]

---

### 10. Zwicky Transient Facility (ZTF) SN Ia Data Release 2

**Description**: ZTF is a wide-field optical time-domain survey using the Palomar 48-inch telescope (P48) with a 47 deg^2 field of view. The ZTF Cosmology Science Working Group has released DR2, the largest SN Ia dataset to date with 3,628 spectroscopically confirmed SNe Ia. [^151^] [^148^]

- **Official Website**: https://www.ztf.caltech.edu/
- **Data Access**: https://ztfcosmo.in2p3.fr/
- **Principal References**: Rigault et al. 2025 (DR2 overview); Smith et al. 2025 (data processing); Lacroix et al. (SMP photometry, in prep) [^148^] [^151^]

#### Data Releases
- **ZTF SN Ia DR2** (2024-2025): 3,628 spectroscopically confirmed SNe Ia [^151^]
  - Discovered March 2018 - December 2020
  - 2,960 with "good sampling" (7+ phases, 2 pre + 2 post max)
  - 2,667 pass standard cosmology quality cuts
  - 5138 spectra (at least one per SN)
  - Nearly 1,000 SNe in volume-limited sample (z < 0.06)
  - 3,591 forced-photometry light curves in gri bands

#### Filter Bands and Cadence
- **Filters**: ZTF-g, ZTF-r, ZTF-i (Sloan-like filters)
- **Cadence**: ~3 days in g and r; ~5 days in i
- **Median sampling**: 40 detections in [-10, +40] day phase range
- **Redshift range**: z < 0.3 (median z ~ 0.08)

#### Data Format and Access
- **Format**: FITS tables, Python tool for data access
- **Access method**: https://ztfcosmo.in2p3.fr/; also via WISeREP [^151^]
- **Contents**: Light curves, spectra, metadata, host properties (global + local 2kpc), observing logs
- **SALT2 parameters**: Provided with multiple phase range options and SALT2.4/SALT3

#### Ancillary Data
- Host galaxy photometry from PS1 DR2 (grizy)
- Host stellar masses and rest-frame colors from SED fitting
- Directional light radius (DLR) host matching
- Observing logs with pointing, limiting magnitudes, zero-points

#### Important Note for Cosmology
- Current DR2 photometry has ~percent-level calibration accuracy but known "pocket effect" sensor issue
- Not yet suitable for precision cosmological parameter inference
- DR2.5 (expected late 2025) will address calibration for cosmology [^148^] [^151^]

#### ML Readiness
- **Extremely High**. The largest homogeneous SN Ia dataset available:
  - Daily cadence with unprecedented phase coverage
  - Volume-limited sample at z < 0.06 for population studies
  - Ideal for training light curve models and classifiers
  - 20 companion papers exploring diverse science applications
  - Python tool provided for easy data access

#### Key Papers
- Rigault et al. 2025, A&A 694: A2 (SALT2 light curve fits) [^43^] [^45^]
- Smith et al. 2025 (data acquisition and processing)
- Dhawan et al. 2022 (early ZTF characteristics)
- Ginolin et al. 2024, 2025 (standardization and host dependencies)

---

### 11. Hubble Space Telescope (HST) High-Redshift Supernova Sample

**Description**: HST programs (GOODS, CANDELS, CLASH, and others) have discovered and followed SNe Ia at the highest redshifts (z > 1), providing crucial constraints on the early behavior of dark energy. Riess et al. discovered 21 new SNe Ia with ACS, including 13 at z > 1, providing the highest-redshift sample known. [^197^] [^200^] [^202^]

- **Data Access**: https://www.stsci.edu/~ariess/; MAST archive
- **Principal References**: Riess et al. 2004, 2007 (HST-discovered SNe); Rodney et al. 2014, 2015 (CANDELS/CLASH); Graur et al. 2014 (CANDELS rates) [^197^] [^200^] [^202^]

#### Data Releases
- **Riess et al. 2007**: 23 SNe Ia at z > 1 (full sample) [^197^] [^200^]
  - 21 new discoveries + 2 recalibrated previous SNe
  - 13 spectroscopically confirmed at z >= 1
  - Discovered in GOODS-North and GOODS-South fields
  - ACS F775W and F850LP imaging
- **CANDELS+CLASH**: 65 SNe of all types, ~24 SNe Ia [^98^]
  - Out to z ~ 2.5
  - F125W and F160W (WFC3/IR) imaging
  - SN Ia rate measurements to z = 2.5

#### Filter Bands and Cadence
- **Filters**: F775W, F850LP (ACS); F125W, F160W (WFC3/IR)
- **Fields**: GOODS-N, GOODS-S, CANDELS fields, CLASH cluster fields
- **Depth**: Reaching AB ~ 27-28 (depending on filter and exposure time)
- **Redshift range**: z = 0.2 - 2.5 (some candidates to z ~ 2.3)

#### Data Format and Access
- **Format**: ASCII tables (light curves, distance moduli)
- **Access**: Riess website (http://braeburn.pha.jhu.edu/~ariess/R06/); MAST archive [^197^]
- **Hubble diagram data**: Available as machine-readable tables

#### Key Cosmological Papers
- Riess et al. 2007, ApJ 659: 98 (HST SNe at z > 1; 2,418 citations) [^200^] [^202^]
- Riess et al. 2004, ApJ 607: 665 (first z > 1 SNe)
- Rodney et al. 2014, AJ 148: 13 (CANDELS SNe)
- Graur et al. 2014, ApJ 783: 28 (CANDELS SN Ia rates to z = 2.5) [^98^]
- Perlmutter et al. 1999 (original SCP high-z sample)

---

### 12. CANDELS/CLASH/Frontier Fields Supernova Surveys

**Description**: CANDELS (Cosmic Assembly Near-infrared Deep Extragalactic Legacy Survey) and CLASH (Cluster Lensing And Supernova survey with Hubble) used HST to discover SNe in deep and cluster fields. These programs provided crucial high-z SNe Ia for constraining dark energy at z > 1 and measuring SN Ia rates in the early universe. [^98^]

- **Data Access**: MAST archive (https://archive.stsci.edu/)
- **Principal References**: Graur et al. 2014; Rodney et al. 2014, 2015; Strolger et al. 2015 [^98^]

#### Data Releases
- **CANDELS SN Survey**: 65 SNe of all types in ~0.25 deg^2 [^98^]
  - ~24 classified as SNe Ia (based on host-galaxy redshifts + SN photometry)
  - 6 with grism spectroscopy
  - Reaching z ~ 2.5
- **CLASH**: Additional SNe in galaxy cluster fields

#### Filter Bands
- **Filters**: F125W, F140W, F160W (WFC3/IR); F606W, F814W, F850LP (ACS)
- **Redshift range**: z = 0.5 - 2.5

#### Key Scientific Results
- Volumetric SN Ia rate measurement beyond z = 2 for the first time [^98^]
- Prompt SN Ia fraction f_P = 0.53 (+0.09/-0.10 stat, +0.10/-0.26 sys)
- Consistent with delay time distribution ~ t^{-1} for t > 40 Myr
- Low rate at z > 1 may indicate rare prompt progenitors (~20%)

---

### 13. Nearby Supernova Factory (SNfactory)

**Description**: SNfactory was an international experiment designed to discover, observe, and analyze a large sample of nearby (z < 0.1) Type Ia supernovae using the SuperNova Integral Field Spectrograph (SNIFS) on the UH 2.2m telescope. It produced the world's largest collection of spectrophotometric supernova time series. [^150^] [^199^]

- **Official Website**: http://snfactory.lbl.gov/
- **Data Access**: http://snfactory.lbl.gov/snf/data/index.html; CDS/VizieR
- **Principal References**: Aldering et al. 2002 (overview); Scalzo et al. 2010; Buton et al. 2013; Chotard et al. 2011; Saunders et al. 2018 (SNEMO); Leget et al. 2020 (SUGAR) [^150^] [^190^] [^199^]

#### Data Releases
- **2020 Interim Release**: Spectrophotometric timeseries for 210 SNe Ia [^150^]
  - Flux-calibrated spectra from 3300-8600 Angstroms
  - Host-galaxy subtractions and extinction corrections
  - Phase coverage: -5 to +50 days post-maximum light
  - Available via CDS (Centre de Donnees astronomiques de Strasbourg)
- **SNEMO/SUGAR training data**: Thousands of spectra with SNIFS [^190^] [^191^]
  - SNEMO: Empirical spectral model for SNe Ia (Saunders et al. 2018)
  - SUGAR: SUpernova Generator And Reconstructor model [^190^] [^191^]

#### SN Type Breakdown
- 600+ spectroscopically confirmed SNe discovered by 2008
- ~300 SNe Ia with detailed spectrophotometric time series
- Focus on z < 0.1 for low-z anchor

#### Spectrophotometric Data
- **SNIFS**: Integral field spectrograph providing simultaneous spectra and imaging
- **Wavelength range**: 3300-8600 A (full optical)
- **Spectral resolution**: R ~ 500 (blue) and R ~ 300 (red channels)

#### Data Format and Access
- **Format**: FITS files (spectrophotometric data)
- **Access**: CDS/VizieR; SNfactory website [^150^] [^199^]
  - ftp://130.79.128.5 (CDS anonymous ftp)
  - http://cdsarc.u-strasbg.fr/viz-bin/cat/J/A+A/636/A46 (SUGAR data)

#### Key Scientific Contributions
- SUGAR model: Adds 2 intrinsic parameters to SALT2 (ejecta velocity, Ca line strength) [^190^] [^191^]
- SNEMO: Improved empirical spectral model
- Hubble constant measurements
- Foundation for LSST/Roman simulations

#### Key Papers
- Aldering et al. 2002 (SPIE): SNfactory overview
- Saunders et al. 2018, ApJ 869: 167 (SNEMO model)
- Leget et al. 2020, A&A 636: A46 (SUGAR model) [^190^] [^191^]
- Buton et al. 2013, A&A 549: A8 (host galaxy properties)

---

### 14. Lick Observatory Supernova Search (LOSS) / Katzman Automatic Imaging Telescope (KAIT)

**Description**: LOSS used the Katzman Automatic Imaging Telescope (KAIT) at Lick Observatory to conduct one of the most successful nearby supernova searches. KAIT discovered nearly 50% of all SNe brighter than mag 19 between 1998-2005. The program collected filtered (BVRI) photometry of ~200 SNe Ia and unfiltered photometry of ~900 SNe. [^47^]

- **Data Access**: Via CfA archive, Open Supernova Catalog, and publications
- **Principal References**: Li et al. 2000, 2001; Filippenko et al. 2001; Leaman et al. 2011; Ganeshalingam et al. 2010

#### Data Releases
- **LOSS Sample**: ~900 SNe discovered (1998-2005)
  - BVRI filtered photometry of 200 SNe Ia
  - Unfiltered photometry of 900 SNe
  - Prompt alerts to 80+ astronomers for follow-up
- **SN Photometry**: Published in individual papers and through CfA archive

#### Filter Bands
- **Filters**: Unfiltered (discovery); BVRI (follow-up photometry)
- **Telescope**: Katzman Automatic Imaging Telescope (KAIT) - 0.76m
- **Redshift range**: z < 0.1 (nearby)

#### Key Scientific Results
- Nearby SN rate measurements (Leaman et al. 2011)
- Hubble constant and local peculiar flow studies
- Low-z SN Ia sample for cosmology
- Distance fitter and extinction law studies [^47^]

---

### 15. ASAS-SN (All-Sky Automated Survey for SuperNovae)

**Description**: ASAS-SN is an all-sky survey using 14-cm telescopes to discover bright transients. While not primarily a cosmological survey (shallow depth), it provides the largest sample of bright nearby SNe with excellent temporal coverage and is highly complete at bright magnitudes. [^10^]

- **Official Website**: https://www.astronomy.ohio-state.edu/~assassin/
- **Principal References**: Shappee et al. 2014; Neumann et al. 2022 (ASAS-SN Bright SN Catalog V); Kochanek et al. 2017 [^10^]

#### Data Releases
- **ASAS-SN Bright SN Catalog**: 2,427 total SNe (complete sample)
  - 443 SNe discovered in 2018-2020
  - 519 recovered + 516 additional m_peak <= 18 mag SNe
  - Host galaxy identifications with UV-midIR photometry

#### Key Features for ML
- Large, complete sample of bright SNe
- Homogeneous g-band observations (later V-band)
- ~90% complete for m_peak <= 17.0 mag
- Host galaxy identifications and offsets [^10^]

---

### 16. Swift Optical/Ultraviolet Supernova Archive (SOUSA)

**Description**: SOUSA catalogs SN observations from the Ultra-Violet Optical Telescope (UVOT) on the Swift satellite. UV observations provide unique constraints on SN properties, especially metallicity and extinction. [^102^]

- **Data Access**: https://swift.gsfc.nasa.gov/ and HEASARC archive
- **Principal Reference**: Brown et al. 2023 (AAS 241); Milne et al. (UVOT SNe)

#### Data Releases
- **SOUSA**: 253 SNe with multi-band UVOT images and photometry [^102^]
  - UVW2, UVM2, UVW1, U, B, V filters
  - SED-dependent parameters: extinction coefficients, k-corrections, bolometric luminosities

#### Filter Bands
- **Filters**: UVW2 (192.8nm), UVM2 (224.6nm), UVW1 (260.0nm), U (346.5nm), B (432.9nm), V (540.2nm)
- **Unique value**: Only facility providing routine UV photometry of SNe

---

### 17. Open Supernova Catalog (OSC)

**Description**: The Open Supernova Catalog is a comprehensive, community-maintained collection of observations and metadata for 50,000+ supernovae. Data are stored in JSON format and rebuilt daily from literature and secondary sources. [^86^] [^81^]

- **Official Website**: https://github.com/astrocatalogs
- **Principal References**: Guillochon et al. 2017, ApJ 835: 64 [^86^]

#### Data Content
- 50,000+ SNe candidates (as of recent builds)
- 12,000+ objects with >10 photometric observations
- 5,000+ objects with spectra
- Metadata, light curves, spectra from X-ray to radio
- JSON format (human- and machine-readable)
- Daily rebuilds from literature parsing

#### Data Access
- **Format**: JSON files (one per supernova)
- **Bulk download**: ~45,162 objects in tar.lzma archive [^81^]
  - http://snad.space/osc/sne.tar.lzma
- **GitHub**: https://github.com/astrocatalogs/ (multiple repositories by year)
- **API**: RESTful API for programmatic queries [^48^]

#### ML Readiness
- **Excellent for ML anomaly detection** [^81^] [^128^]
  - Large and diverse sample with heterogeneous data
  - JSON format easily parsed by Python
  - Used for SNAD (Supernova Anomaly Detection) project
  - Ideal for training classification and outlier detection algorithms

#### Key Papers
- Guillochon et al. 2017, ApJ 835: 64 (catalog description) [^86^]
- Pruzhinskaya et al. 2019, MNRAS 489: 3597 (anomaly detection with OSC) [^81^] [^128^]

---

### 18. Asiago Supernova Catalog

**Description**: The Asiago Supernova Catalog is a historical catalog of supernovae discovered since 1885, maintained by the Asiago Observatory. The dynamic version is regularly updated and hosted by NASA HEASARC. [^142^]

- **Data Access**: https://heasarc.gsfc.nasa.gov/W3Browse/all/asiagosn.html
- **Catalog**: https://cdsarc.cds.unistra.fr/ftp/cats/B/sn (CDS)
- **Format**: Machine-readable table with SN names, positions, types, parent galaxies, redshifts

#### Data Content
- All SNe observed since 1885
- Parent galaxy identifications and properties
- Regularly updated (weekly CDS updates)

#### Key Features
- Essential reference for SN metadata
- Used for host galaxy studies and SN rate calculations
- Cross-matchable with other catalogs

---

## Compilation Datasets

---

### C1. Pantheon Sample (Scolnic et al. 2018)

**Description**: Pantheon combined 1,048 spectroscopically confirmed SNe Ia from PS1, SDSS, SNLS, low-z, and HST samples into the largest cosmological SN compilation at the time. [^133^]

- **Data Access**: https://github.com/dscolnic/Pantheon (original); included in Pantheon+
- **Reference**: Scolnic et al. 2018, ApJ 859: 101

#### Sample Composition
- 279 PS1 SNe Ia (0.03 < z < 0.68)
- SDSS, SNLS, various low-z, and HST samples
- Total: 1,048 SNe Ia (0.01 < z < 2.3)
- Homogeneous SALT2 light curve fitting
- Supercal cross-calibration method

#### Cosmological Results
- Omega_M = 0.307 +/- 0.012, w = -1.026 +/- 0.041 (wCDM, +Planck CMB)
- Most precise dark energy measurement at the time

---

### C2. Pantheon+ (Scolnic et al. 2022; Brout et al. 2022)

**Description**: Pantheon+ is the definitive compilation of 1,701 SNe Ia from 18 surveys for cosmological analysis. It includes improved calibration (Supercal+), retrained SALT2 model, SH0ES Cepheid distances for H0 measurement, and extensive systematic treatment. [^96^] [^97^] [^99^] [^164^]

- **Data Access**: https://github.com/PantheonPlusSH0ES/DataRelease [^99^]
- **References**: Scolnic et al. 2022 (full dataset); Brout et al. 2022 (cosmology w); Popovic et al. 2022 (dust modeling)

#### Sample Composition
- 1,701 cosmology-grade SNe Ia from 18 photometric surveys [^164^]
- Redshift range: z_min ~ 0.0008 to z_max ~ 2.26, median z ~ 0.28
- Includes SH0ES Cepheid-calibrated anchor for H0 measurement
- SALT2 light curves refit across 200-900nm rest-frame
- Full covariance matrices (statistical + systematic)

#### Data Products
- Pantheon+_Data directory: Light curves, distances, redshifts, host properties [^99^]
- SH0ES_Data directory: Cepheid distances, H0 calibration
- Cosmology directory: Chains, CosmoSIS likelihoods
- Covariance matrices with full systematic decomposition

#### Cosmological Results
- Most precise cosmological constraints from SNe Ia
- Tension with LambdaCDM at 2-3 sigma level (possible evolving dark energy)
- H0 measurement in combination with SH0ES

#### ML Readiness
- **Very High**. Gold standard for SN cosmology:
  - Homogeneous treatment of all surveys
  - Complete covariance matrices for uncertainty propagation
  - Pre-computed SALT2 fits and distance moduli
  - Host galaxy properties included
  - Extensive simulations (2 x 10^8 SNANA simulations) for bias correction

---

### C3. Union3 / UNITY1.5 (Rubin et al. 2023)

**Description**: Union3 assembled 2,087 SNe Ia from 24 datasets using the UNITY1.5 (Unified Nonlinear Inference for Type-Ia cosmologY) Bayesian framework. It uses SALT3 light curve fitting and models selection effects, standardization, and systematics simultaneously. [^189^] [^164^]

- **Data Access**: Released with paper; distances, light-curve fits, and UNITY1.5 framework
- **Reference**: Rubin et al. 2023, arXiv:2311.12098 [^189^]

#### Sample Composition
- 2,087 SNe Ia from 24 surveys [^164^]
- Redshift range: 0.01 < z < 2.26
- Independent AB offset determination
- SALT3 model (full rest-frame UV-optical)

#### Cosmological Results
- Weak 1.7-2.6 sigma tension with LambdaCDM
- Possible evidence for thawing dark energy (w0 > -1, wa < 0)
- Recovers peculiar-velocity field posterior

#### Key Features
- Unified Bayesian framework for simultaneous modeling
- Improved treatment of selection effects and standardization
- Posterior for SN peculiar-velocity field
- Homogeneous SALT3 fits across all surveys

---

### C4. Joint Lightcurve Analysis (JLA) - Betoule et al. 2014

**Description**: JLA combined the SDSS-II and SNLS 3-year samples with low-z and HST data into a single analysis with improved calibration and systematic treatment. [^105^]

- **Data Access**: http://cdsarc.u-strasbg.fr/viz-bin/qcat?J/A+A/568/A22
  - Covariance matrices: http://supernovae.in2p3.fr/sdss_snls_jla/covmat_v6.tgz [^97^]
- **Reference**: Betoule et al. 2014, A&A 568: A22

#### Sample Composition
- 118 low-z SNe Ia
- 374 SDSS-II SNe Ia
- 239 SNLS SNe Ia
- 9 HST SNe Ia
- Total: 740 SNe Ia

#### Cosmological Results
- Omega_M = 0.295 +/- 0.034, w = -1.089 +/- 0.106 (SN only)
- Omega_M = 0.321 +/- 0.018, w = -1.054 +/- 0.069 (SN+CMB+BAO)

---

### C5. SCP Union Compilations (Union, Union2, Union2.1)

**Description**: The Supernova Cosmology Project (SCP) at Lawrence Berkeley National Laboratory produced a series of supernova compilations: Union (2008), Union2 (2010), and Union2.1 (2012). These were foundational datasets for SN cosmology. [^16^] [^23^] [^100^] [^165^]

- **Data Access**: http://supernova.lbl.gov/Union/ [^100^]
- **References**: Kowalski et al. 2008 (Union); Amanullah et al. 2010 (Union2); Suzuki et al. 2012 (Union2.1)

#### Union2.1 (2012)
- 833 SNe Ia from 19 datasets [^23^] [^100^]
- Columns: SN name, redshift, distance modulus, distance modulus error, low-mass host probability
- Used in hundreds of cosmological analyses
- Simple ASCII format for easy use

#### Earlier Compilations
- **Union** (Kowalski et al. 2008): ~300 SNe Ia
- **Union2** (Amanullah et al. 2010): 557 SNe Ia
- Each version added more SNe and improved systematics

---

## Software Frameworks and Simulation Data

---

### S1. SNANA (SuperNova ANAlysis)

**Description**: SNANA is the standard software package for SN cosmology analysis, developed by Rick Kessler. It includes extensive public datasets, simulations, and analysis tools. [^53^] [^54^]

- **GitHub**: https://github.com/RickKessler/SNANA
- **Documentation**: SNANA/doc; Tutorial: https://kicp.uchicago.edu/~kessler/SNANA_Tutorial/
- **Data**: SNDATA_ROOT (~2 GB) at https://zenodo.org/records/12655677 [^53^]

#### Public Data Included
- SDSS-II, SNLS, DES, PS1, low-z survey light curves
- Filter transmissions, primary SEDs, calibration files
- SNIa and core-collapse simulation models
- Cadence libraries and host-galaxy libraries for simulations
- K-correction files for multiple surveys

#### Key Features
- SALT2, MLCS, SNooPy light curve fitting
- Full cosmology fitting with systematic propagation
- Monte Carlo simulation capabilities
- Bias correction via simulations
- Used by DES, PS1, and other major surveys

---

### S2. SNCosmo

**Description**: SNCosmo is a Python library for supernova cosmology that provides model synthesis, fitting, and built-in access to public datasets. [^27^] [^35^]

- **GitHub**: https://github.com/sncosmo
- **Documentation**: https://sncosmo.readthedocs.io/

#### Built-in Models and Data
- SALT2, MLCS2k2, Hsiao, Nugent, SNANA, Whalen models
- Built-in bandpasses and magnitude systems
- Integration with sndata package for survey data access [^27^]
- Extensible with custom models and filters

#### Python Data Access Packages
- **sndata**: https://github.com/sncosmo/SNData - Data access for public SN datasets [^27^]
- **sndatasets**: https://github.com/sncosmo/sndatasets - Download and normalize published SN photometric data

---

### S3. SALT2 and SALT3 Models

**Description**: SALT2 (Spectral Adaptive Lightcurve Template 2) and SALT3 are the standard light curve models used in SN cosmology. Training data comes from major surveys. [^43^]

- **SALT2**: Guy et al. 2007, 2010; Betoule et al. 2014 (SALT2.4/JLA training)
  - Taylor et al. 2021: Updated SALT2 training (T21 surfaces)
- **SALT3**: Kenworthy et al. 2021, ApJ 923: 240
  - Redesigned training algorithm
  - Full rest-frame UV-optical coverage
  - Trained on Pantheon+ and other recent data

#### Training Data Sources
- SDSS-II, SNLS, PS1, CSP, CfA, low-z surveys
- ZTF SN Ia DR2 will be included in future training [^43^]
- Publicly available through sncosmo/SNANA

---

## Trends & Signals

### 1. Dataset Size Growth (Exponential)
| Era | Primary Dataset | N(SNe Ia) | Year |
|-----|----------------|-----------|------|
| Pre-2005 | Hamuy et al. compilation | ~30 | 1996 |
| 2005-2010 | Union, CfA | 100-300 | 2008 |
| 2010-2015 | SNLS3, SDSS, JLA | 500-750 | 2014 |
| 2015-2020 | Pantheon | 1,048 | 2018 |
| 2020-2024 | Pantheon+, Union3, DES5YR | 1,600-2,100 | 2022-2024 |
| 2024+ | ZTF DR2 (low-z anchor) | 3,600+ | 2024 |

### 2. Survey Depth vs. Redshift Coverage
- **Shallow/wide surveys** (ASAS-SN, LOSS): z < 0.1, hundreds of SNe, excellent for low-z anchor
- **Medium-depth surveys** (CSP, Foundation, CfA, ZTF): z < 0.1-0.3, thousands of SNe, best for standardization studies
- **Deep surveys** (SDSS, PS1, DES): z ~ 0.1-0.8, hundreds to thousands of SNe, cosmological constraints
- **Ultra-deep surveys** (SNLS, DES, HST, HSC): z ~ 0.5-2.5, dozens to hundreds of SNe, dark energy evolution

### 3. Calibration Precision Evolution
- Early surveys: ~5-10% photometric calibration
- Modern surveys (DES, PS1): <1% relative calibration
- Pantheon+: Supercal+ achieves ~7 mmag precision across surveys
- Remaining challenge: Cross-survey systematic uncertainties now dominate statistical errors

### 4. ML Readiness Trends
- **Well-prepared for ML**: SDSS, DES, ZTF, PS1, CSP (homogeneous, large N, good documentation)
- **Moderately prepared**: SNLS, SNfactory, HSC (good data but more complex access)
- **Challenging for direct ML**: CfA, LOSS, historical surveys (heterogeneous, diverse formats)
- **Best for anomaly detection**: Open Supernova Catalog (50,000+ objects, diverse, JSON format) [^81^] [^128^]

### 5. Emerging Tension with LambdaCDM
- Pantheon+ and DES-SN5YR independently find 2-3 sigma tension with w=-1 [^10^] [^99^]
- Union3 finds weak 1.7-2.6 sigma tension [^189^]
- Possible evidence for evolving dark energy (w0 > -1, wa < 0)
- This creates urgent need for larger, better-calibrated samples

---

## Recommended Deep-Dive Areas

### Priority 1: ZTF SN Ia DR2 (Immediate Opportunity)
**Why**: 3,628 SNe Ia - largest homogeneous sample ever. Volume-limited sample at z < 0.06 is unique for population studies.
**Action Items**:
- Access data at https://ztfcosmo.in2p3.fr/
- Use Python tool for data exploration
- Note: DR2 photometry not yet cosmology-grade (wait for DR2.5, expected late 2025)
- Ideal for: standardization studies, host-SN correlations, population demographics, ML training
**Companion papers**: 20 papers covering all aspects of the dataset [^151^]

### Priority 2: Pantheon+ Dataset (Gold Standard for Cosmology)
**Why**: 1,701 SNe Ia from 18 surveys with the best cross-calibration available.
**Action Items**:
- Clone https://github.com/PantheonPlusSH0ES/DataRelease
- Full covariance matrices provided for systematic studies
- Pre-computed SALT2 fits, host properties, classification info
- Includes SH0ES data for H0 measurement
**Key papers**: Scolnic et al. 2022; Brout et al. 2022 [^99^]

### Priority 3: DES-SN5YR with Simulations (Best for Classification ML)
**Why**: Provides 25 simulated mocks + real data + classification probabilities.
**Action Items**:
- Clone https://github.com/des-science/DES-SN5YR
- 25 DES mocks with both Ia and non-Ia light curves
- Pre-computed classification probabilities from multiple algorithms
- Full Pippin pipeline inputs for reproduction
**Key papers**: Sanchez et al. 2024; Vincenzi et al. 2024 [^14^] [^21^]

### Priority 4: Open Supernova Catalog (Best for Anomaly Detection)
**Why**: 50,000+ SNe in JSON format, heterogeneous data ideal for finding outliers.
**Action Items**:
- Download bulk data from http://snad.space/osc/sne.tar.lzma
- Use GitHub repos: https://github.com/astrocatalogs/
- SNAD project has already demonstrated ML anomaly detection [^128^]
- Daily rebuilds keep data current
**Key papers**: Guillochon et al. 2017; Pruzhinskaya et al. 2019 [^86^] [^81^]

### Priority 5: SNfactory Spectrophotometric Data (Best for Spectral Models)
**Why**: Only large sample of true spectrophotometric time series for SNe Ia.
**Action Items**:
- Access via CDS: http://cdsarc.u-strasbg.fr/viz-bin/cat/J/A+A/636/A46
- Includes SUGAR model data with 2 additional intrinsic parameters
- 210 SNe Ia with flux-calibrated spectra 3300-8600A
- Ideal for: spectral model training, SED reconstruction, standardization
**Key papers**: Leget et al. 2020 (SUGAR); Saunders et al. 2018 (SNEMO) [^190^] [^191^]

### Priority 6: Foundation Survey DR1 (Best Low-z Anchor)
**Why**: Homogeneous, well-calibrated low-z sample on PS1 system.
**Action Items**:
- Clone https://github.com/djones1040/Foundation_DR1
- 225 SNe Ia with excellent photometric calibration
- Designed to replace heterogeneous low-z anchors
- Ideal for: training standardization relations, H0 studies
**Key papers**: Foley et al. 2018; Jones et al. 2019 [^103^] [^106^]

### Priority 7: CSP DR3 (Best NIR Data)
**Why**: Best available near-infrared photometry of SNe Ia.
**Action Items**:
- Download from https://csp.obs.carnegiescience.edu/data
- 134 SNe with ugriBVYJH photometry
- 90% have NIR coverage - unique dataset
- Ideal for: dust extinction studies, standardization with NIR, K-corrections
**Key paper**: Krisciunas et al. 2017 (309 citations) [^168^]

### Priority 8: HSC-SSP Transient Survey (Best for High-z Studies)
**Why**: Doubles the z > 1 SN Ia sample.
**Action Items**:
- Access through HSC data release: https://hsc-release.mtk.nao.ac.jp/
- 433 SNe Ia classified in COSMOS field
- 58 at z > 1
- Deep grizy photometry reaching r ~ 26
**Key paper**: Yasuda et al. 2019, PASJ 71: 74 [^18^]

---

## ML-Specific Derived Datasets

### Supernova Classification Training Sets
1. **SPCC (Supernova Photometric Classification Challenge)**: Simulated data from SNANA used in Kessler et al. 2010 challenge; widely used for classifier development
2. **PLAsTiCC (Photometric LSST Astronomical Time-Series Classification Challenge)**: 2018 Kaggle challenge with simulated LSST-like light curves; 3.5M events; widely used for transient classification ML [^53^]
3. **DES Classification**: 1,635 SNe with pre-computed classification probabilities from multiple algorithms (SNN, SuperNNova, etc.) [^14^]
4. **PS1 Classification**: Hosseinzadeh et al. 2022 ML classification of 2,315 PS1 SNe with 82% accuracy without spectra [^2^]

### Simulation Libraries for ML
1. **SNANA SNDATA_ROOT**: ~2 GB of public data including simulations for all major surveys [^53^]
2. **SNANA DES Mocks**: 25 simulated DES light curve sets (Ia + non-Ia) for training/testing [^14^]
3. **SALT2/SALT3 Training Sets**: Light curves and spectra used to train models, available through sncosmo [^43^]
4. **SNEMO/SUGAR**: Spectral models trained on SNfactory data, available via CDS [^190^] [^191^]

### Anomaly Detection Datasets
1. **OSC + SNAD**: 50,000+ SNe with anomaly detection already demonstrated [^81^] [^128^]
2. **ZTF DR2**: Volume-limited sample enables population-level anomaly detection

---

## Data Access Summary Table

| Dataset | URL/Portal | Format | Size | Python Access |
|---------|-----------|--------|------|---------------|
| SDSS-II SN DR | classic.sdss.org/drsn | FITS/ASCII | ~GB | sndata, SNANA |
| DES-SN5YR | github.com/des-science/DES-SN5YR | FITS/ASCII | ~GB | SNANA, SNCosmo |
| SNLS | cdsarc.u-strasbg.fr | ASCII/FITS | ~100MB | sndata |
| CSP DR3 | csp.obs.carnegiescience.edu/data | ASCII | ~100MB | sndata, direct |
| CfA Archive | lweb.cfa.harvard.edu/supernova/SNarchive.html | ASCII/FITS | ~50GB total | SNCosmo, sndata |
| Foundation DR1 | github.com/djones1040/Foundation_DR1 | SNANA/FITS | ~MB | SNANA |
| ZTF SN Ia DR2 | ztfcosmo.in2p3.fr | FITS/ASCII | ~GB | Python tool |
| Pantheon+ | github.com/PantheonPlusSH0ES/DataRelease | ASCII/FITS | ~MB | Custom |
| Union2.1 | supernova.lbl.gov/Union | ASCII | ~KB | Custom |
| OSC | github.com/astrocatalogs | JSON | ~GB | Custom/JSON |
| SNANA Data | zenodo.org/records/12655677 | Various | ~2GB | SNANA |
| SNfactory | cdsarc.u-strasbg.fr | FITS | ~GB | Custom |
| HSC-SSP | hsc-release.mtk.nao.ac.jp | FITS | TB scale | HSC pipeline |

---

## References Summary

The following key references should be cited when using data from these surveys:

1. **SDSS-II**: Sako et al. 2018, PASP 130: 104002 [^132^]
2. **DES**: Sanchez et al. 2024, ApJ 975: 5; Vincenzi et al. 2024, ApJ 975: 86 [^14^] [^21^]
3. **SNLS**: Guy et al. 2010, A&A 523: A7; Balland et al. 2009, A&A 507: 85 [^55^] [^105^]
4. **ESSENCE**: Miknaitis et al. 2007, ApJ 666: 674; Wood-Vasey et al. 2007, ApJ 666: 694 [^19^]
5. **CSP**: Krisciunas et al. 2017, AJ 154: 211 [^168^]
6. **CfA**: Hicken et al. 2012 (CfA4); Blondin et al. 2012, AJ 143: 126 [^104^]
7. **PS1/Pantheon**: Scolnic et al. 2018, ApJ 859: 101 [^133^]
8. **Pantheon+**: Scolnic et al. 2022, ApJ 938: 113; Brout et al. 2022, ApJ 938: 114 [^99^]
9. **Union3**: Rubin et al. 2023, arXiv:2311.12098 [^189^]
10. **ZTF**: Rigault et al. 2025, A&A 694: A2; Smith et al. 2025 [^151^]
11. **HST High-z**: Riess et al. 2007, ApJ 659: 98 [^200^]
12. **SNfactory**: Leget et al. 2020, A&A 636: A46; Saunders et al. 2018, ApJ 869: 167 [^190^]
13. **OSC**: Guillochon et al. 2017, ApJ 835: 64 [^86^]
14. **SNANA**: Kessler et al. 2009, PASP 121: 1028 [^53^]
15. **SNCosmo**: Barbary et al. 2016, ascl:1611.017 [^35^]

---

*Research compiled from 15+ independent web searches across arXiv, ADS, GitHub, official survey websites, data archives (ESO, MAST, HEASARC, SDSS), and publication databases. All citations use inline source references [^N^] corresponding to search results.*

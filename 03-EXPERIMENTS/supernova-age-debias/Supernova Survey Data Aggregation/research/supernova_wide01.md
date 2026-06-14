## Facet: Ground-based Optical & Time-Domain Supernova Surveys

### Key Findings

1. **ZTF** is the most prolific current ground-based supernova survey, producing 5,000-10,000 new extragalactic transients per year with ~1 million alerts per night [^207^]. The ZTF alert archive is publicly accessible via the University of Washington, and 24 public data releases (DR1-DR24) have been issued [^11^].

2. **DES-SN 5-year data release** (2024) is the largest single-instrument, single-telescope supernova sample ever used for cosmology, containing 31,636 DiffImg and 19,706 high-quality SMP light curves, with 1,635 photometrically classified SNe Ia spanning 0.1 < z < 1.13 [^125^][^126^].

3. **Pan-STARRS1 Medium Deep Survey (PS1-MDS)** contains the largest real spectroscopically classified SN training set, with 557 SNe across 5 classes used for photometric classification [^24^]. The Young Supernova Experiment (YSE) built on PS1, releasing 1,975 multi-color light curves with ParSNIP classifications [^62^].

4. **ASAS-SN** is the most complete bright supernova catalog, with 2,427 SNe total (complete to m_peak = 16.7 mag in g-band) [^10^]. The Sky Patrol provides real-time photometry for 100M+ targets via pyasassn API [^15^].

5. **ATLAS forced photometry server** provides public access to photometric measurements over the full history of the ATLAS survey, a unique resource for SN light curves [^61^][^63^].

6. **ALeRCE, Fink, AMPEL, ANTARES, Lasair, Babamul, and Pitt-Google** are the seven approved Rubin/LSST community brokers, all currently prototyping with ZTF data [^44^][^205^].

7. **CfA Supernova Archive** maintains one of the most comprehensive historical supernova datasets, including CfA3 (185 SNe Ia), CfA4 (93 SNe Ia), stripped-envelope SNe, and thousands of spectra, all publicly downloadable [^142^][^143^][^144^].

8. **Carnegie Supernova Project (CSP)** has released DR3 with 134 SNe Ia in optical (ugriBV) and NIR (YJH) passbands, plus spectroscopic data releases [^166^][^172^].

9. **PLAsTiCC** was the foundational LSST precursor ML challenge dataset with ~3.5M simulated light curves (15 classes), now unblinded on Zenodo [^122^][^185^].

10. **WISeREP** serves as the primary community archive for supernova spectra, with >33,000 public spectra for >15,000 objects as of 2021, plus photometry [^117^][^114^].

---

### Survey Catalog

#### 1. Zwicky Transient Facility (ZTF)
- **Website**: https://www.ztf.caltech.edu/
- **Data Portal**: https://irsa.ipac.caltech.edu/Missions/ztf.html (IPAC/IRSA); https://ztf.uw.edu/alerts/public/ (Alert Archive)
- **Data Releases**: DR1 (2019) through DR24 (2025); 24 public releases to date [^11^]
- **SN Count**: ~5000-10,000 new likely extragalactic transients/year; 5.32 billion light curves in DR24 [^11^]
- **Data Types**: Photometry (PSF, forced), difference imaging, alert packets, spectra (via follow-up)
- **Formats**: FITS, Avro (alerts), HDF5 (matchfiles), CSV
- **Access Method**: Bulk download via IPAC, Avro alert stream (Kafka), query interface, pyztf
- **Key Publications**: Bellm et al. 2019 (PASP); Masci et al. 2019 (PASP); Patterson et al. 2019 (alert system)
- **ML-Ready Subsets**: Yes - ZTF BTS (Bright Transient Survey) spectroscopic sample, Superphot+ trained on 6,061 ZTF SNe [^157^]; ParSNIP classifications via YSE DR1
- **Notes**: 100K+ alerts/night; 25,000 deg2 northern sky coverage; g+r filters; 48-inch Palomar telescope; public-private partnership

#### 2. Pan-STARRS1 / PS1 Medium Deep Survey (PS1-MDS)
- **Website**: https://panstarrs.stsci.edu/
- **Data Portal**: https://outerspace.stsci.edu/spaces/PANSTARRS/pages/298812201/Pan-STARRS1+data+archive+home+page
- **Data Releases**: PS1 DR1 (2016), DR2 (2019) [^21^]
- **SN Count**: PS1-MDS: 5243 SN-like transients detected; 557 spectroscopically classified across 5 classes [^24^]
- **Data Types**: Photometry (grizy), spectroscopy (follow-up), host galaxy info
- **Formats**: FITS, CSV, SNANA format
- **Access Method**: CasJobs SQL interface, catalog search form, bulk download
- **Key Publications**: Chambers et al. 2016; Villar et al. 2020 (Superphot/2315 SNe classification); Lunnan et al. 2018 (SLSNe) [^19^][^24^]
- **ML-Ready Subsets**: Yes - Superphot training set (518 spectroscopically classified SNe); YSE DR1 used PS1 photometry
- **Notes**: 10 deep-drilling fields, 70 sq deg, 3-day cadence; typical depth 23.3 mag; grizy filters; 2009-2014

#### 3. Young Supernova Experiment (YSE)
- **Website**: https://yse.avocado.org/
- **Data Portal**: https://zenodo.org/records/7317476 [^68^]
- **Data Releases**: YSE DR1 (2022) [^62^][^64^]
- **SN Count**: 1,975 transients (492 spectroscopically classified; 1,483 photometrically classified) [^62^]
- **Data Types**: PS1-griz + ZTF-gr forced photometry, host galaxy associations, redshifts, ParSNIP/SuperRAENN classifications
- **Formats**: SNANA format (HEAD.fits + PHOT.fits) [^97^]
- **Access Method**: Zenodo bulk download (yse_dr1_zenodo.tar.gz) [^68^]
- **Key Publications**: Aleo et al. 2023 (ApJS 266:9) [^71^]
- **ML-Ready Subsets**: Yes - Full ParSNIP classification results included; 82% accuracy across 3 SN classes [^62^]
- **Notes**: Uses Pan-STARRS2 + ZTF; low-z anchor for LSST; 2019-2021; ~1500 sq deg; magnitude- and volume-limited surveys

#### 4. All-Sky Automated Survey for SuperNovae (ASAS-SN)
- **Website**: https://asas-sn.ifa.hawaii.edu/
- **Data Portal**: https://asas-sn.ifa.hawaii.edu/documentation/index.html [^15^]
- **Data Releases**: ASAS-SN Bright Supernova Catalog I-V (2014-2022) [^10^]
- **SN Count**: 2,427 total SNe; 984 in g-band 2018-2020; complete to m_peak=16.7 mag [^10^]
- **Data Types**: Photometry (g-band), light curves, host galaxy photometry, classifications
- **Formats**: ASCII tables, CSV, JSON (API)
- **Access Method**: pyasassn Python API, web interface, ADQL queries [^15^]
- **Key Publications**: Holoien et al. 2017; Neumann et al. 2022 (Catalog V) [^10^]
- **ML-Ready Subsets**: Yes - Catalog includes classifications, host galaxy photometry, redshifts
- **Notes**: 14-cm telescopes worldwide; images entire sky nightly to g~18.5; fully open data; real-time Sky Patrol for 100M+ sources

#### 5. Dark Energy Survey Supernova Program (DES-SN)
- **Website**: https://www.darkenergysurvey.org/
- **Data Portal**: https://github.com/des-science/DES-SN5YR; https://zenodo.org/records/12720777 [^126^]
- **Data Releases**: DES-SN 5-year data release (2024) [^125^]
- **SN Count**: 31,636 DiffImg + 19,706 SMP light curves; 1,635 photometrically classified SNe Ia [^125^]
- **Data Types**: griz forced PSF photometry (DIFFIMG + SMP), classifications, host info
- **Formats**: FITS, ASCII, JSON
- **Access Method**: GitHub repository bulk download, Zenodo [^126^][^128^]
- **Key Publications**: Sanchez et al. 2024 (ApJ 975:5); Brout et al. 2019 (SN3YR) [^132^]
- **ML-Ready Subsets**: Yes - 1,635 high-quality cosmology sample with photo-z classifications
- **Notes**: DECam at CTIO 4m; 500 sq deg; 0.1 < z < 1.13 (largest redshift range); largest single-instrument SN sample for cosmology

#### 6. ATLAS (Asteroid Terrestrial-impact Last Alert System)
- **Website**: https://atlas.fallingstar.com/ [^61^]
- **Data Portal**: https://fallingstar-data.com/forcedphot/ [^63^]
- **Data Releases**: Forced photometry server (public); ATLAS100 volume-limited sample
- **SN Count**: 2,476+ extragalactic transients (mostly SNe); 654 spectroscopically classified [^14^]
- **Data Types**: Forced photometry (c+o filters), alert stream, transient discoveries
- **Formats**: CSV, JSON (API)
- **Access Method**: Forced photometry web form and API; bulk download for ATLAS100 sample [^63^]
- **Key Publications**: Tonry et al. 2018 (ATLAS system); Smith et al. 2020 (transient pipeline); Shingles et al. 2021 (forced photometry) [^63^]
- **ML-Ready Subsets**: ATLAS100 sample public on Oxford Research Archive [^63^]
- **Notes**: Two filters (c ~ g+r, o ~ r+i); 30s exposures to ~19.5 mag; 4 units worldwide; real-time transient pipeline; CNN real-bogus classifier

#### 7. Palomar Transient Factory (PTF) / iPTF
- **Website**: https://www.ptf.caltech.edu/
- **Data Portal**: https://www.ipac.caltech.edu/programs/ptf/ (via IPAC) [^69^]
- **Data Releases**: PTF DR1, DR2, DR3; iPTF data releases [^76^]
- **SN Count**: Thousands of SNe discovered; 34 SNe Ic-BL analyzed [^70^]; 518 spectroscopically classified SNe for Superphot training
- **Data Types**: Photometry (g, R bands), spectra (via WISeREP), light curves
- **Formats**: FITS, ASCII, HDF5
- **Access Method**: IPAC web interface; 18-month proprietary period then public [^69^]
- **Key Publications**: Law et al. 2009; Rau et al. 2009; Nugent et al. 2015; Villar et al. 2019 (Superphot)
- **ML-Ready Subsets**: Superphot training set (518 SNe, 5 classes) [^13^]; 10,000 light curve sample (Price-Whelan et al. 2014)
- **Notes**: 48-inch Palomar telescope; g+R filters; 2009-2017; predecessor to ZTF; WISeREP archive for spectra

#### 8. Catalina Real-Time Transient Survey (CRTS)
- **Website**: http://crts.caltech.edu/ [^103^]
- **Data Portal**: http://nesssi.cacr.caltech.edu/DataRelease/ (CSDR3) [^107^]
- **Data Releases**: CSDR3 (500 million sources, ~40 billion measurements) [^107^]
- **SN Count**: ~1,000 SNe discovered; ~3,000 high-amplitude transients total [^101^]
- **Data Types**: Photometry (unfiltered), light curves, transient classifications
- **Formats**: ASCII, CSV
- **Access Method**: Web query interface, bulk download [^107^]
- **Key Publications**: Djorgovski et al. 2011; Drake et al. 2009 [^101^][^104^]
- **ML-Ready Subsets**: 98,000 periodic variables catalog; transient classifications available
- **Notes**: 3 telescopes (CSS, MLS, SSS); ~33,000 deg2; V~15-21.5; complete open data (no proprietary period); precursor to larger surveys

#### 9. Gaia Photometric Science Alerts (Gaia Alerts)
- **Website**: http://gsaweb.ast.cam.ac.uk/alerts/ [^134^]
- **Data Portal**: http://gsaweb.ast.cam.ac.uk/alerts/alertsindex (alerts index)
- **Data Releases**: Continuous alert stream; 10,765 alerts published through Dec 2019; ongoing [^120^]
- **SN Count**: ~25% of alerts classified; majority are SNe (~2,000+ SNe); 2nd largest contributor to TNS [^120^]
- **Data Types**: Photometry (G-band, BP/RP low-res spectra), light curves, astrometry
- **Formats**: CSV, HTML, RSS, VOEvents
- **Access Method**: Web interface, Aladin Lite, TNS cross-match
- **Key Publications**: Hodgkin et al. 2021 (A&A 652, A76); Wyrzykowski et al. 2012 [^120^]
- **ML-Ready Subsets**: Alert stream with classifications; BP/RP spectra for bright alerts
- **Notes**: All-sky; G~17-20; ~30-day cadence; 2-3 day latency; full sky coverage; 106.5 min between FOV pairs

#### 10. SkyMapper Transient Survey (SMT)
- **Website**: https://skymapper.anu.edu.au/
- **Data Portal**: https://skymapper.anu.edu.au/ (transient page)
- **Data Releases**: Early data releases mentioned; DR1 (2018) for Southern Survey [^65^]
- **SN Count**: ~30 SNe Ia early data release target; surveys ~400-600 galaxies/night
- **Data Types**: ugriz photometry, transient candidates, classifications
- **Formats**: FITS, ASCII
- **Access Method**: Web interface, API to TNS
- **Key Publications**: Scalzo et al. 2017 (SMT paper); Wolf et al. 2018 (DR1) [^65^][^154^]
- **ML-Ready Subsets**: Early data releases planned
- **Notes**: 1.3m telescope at Siding Spring; Southern hemisphere; ugriz filters; low-z SN Ia focus; overlap with DES footprint

#### 11. Carnegie Supernova Project (CSP)
- **Website**: https://csp.obs.carnegiescience.edu/
- **Data Portal**: https://csp.obs.carnegiescience.edu/data [^226^]
- **Data Releases**: CSP DR1 (spectra), DR2 (photometry), DR3 (134 SNe Ia photometry) [^172^]
- **SN Count**: DR3: 134 SNe Ia + peculiar white dwarf explosions; CSP-II additional SNe
- **Data Types**: Optical (ugriBV) + NIR (YJH) photometry, spectra
- **Formats**: ASCII, FITS
- **Access Method**: Direct download (tarballs); SNooPy Python package [^224^]
- **Key Publications**: Krisciunas et al. 2017 (DR3); Folatelli et al. 2013 (DR1 spectra); Stritzinger et al. 2011 (DR2)
- **ML-Ready Subsets**: Yes - DR3 includes 134 well-observed low-z SNe Ia with optical+NIR
- **Notes**: Las Campanas Observatory; low-z focus (z=0.0037-0.0835, median 0.024); natural system photometry; critical for H0 measurement

#### 12. CfA (Harvard-Smithsonian Center for Astrophysics) Supernova Archive
- **Website**: https://lweb.cfa.harvard.edu/supernova/ [^143^]
- **Data Portal**: https://lweb.cfa.harvard.edu/supernova/SNarchive.html [^144^]
- **Data Releases**: CfA3 (185 SNe Ia), CfA4 (93 SNe Ia), stripped-envelope SNe, Type II SNe [^142^][^148^]
- **SN Count**: 185+93 SNe Ia; 64 stripped-envelope CC SNe; hundreds of spectra
- **Data Types**: Multi-band photometry (UBVRI), optical spectra, NIR light curves
- **Formats**: ASCII, FITS
- **Access Method**: Bulk download (tarballs); individual SN lookup [^144^]
- **Key Publications**: Hicken et al. 2009 (CfA3); Hicken et al. 2012 (CfA4); Bianco et al. 2014 (stripped SNe); Hicken et al. 2017 (Type II)
- **ML-Ready Subsets**: Yes - well-calibrated, multi-band light curves with homogeneous reduction
- **Notes**: Keplercam at FLWO; precision ~0.025 mag; one of the most-used low-z SN Ia training sets

#### 13. Lick Observatory Supernova Search (LOSS)
- **Website**: https://astronomy.berkeley.edu/research/snearch/
- **Data Portal**: VizieR (Graur+ 2017) [^158^]
- **Data Releases**: LOSS revisited sample (1998-2008); follow-up program light curves [^155^][^158^]
- **SN Count**: 10-year sample; 70 stripped-envelope SNe light curves in follow-up program [^155^]
- **Data Types**: BVRI + Clear light curves, host galaxy properties
- **Formats**: ASCII, FITS
- **Access Method**: VizieR catalog download; publication tables
- **Key Publications**: Leaman et al. 2011; Graur et al. 2017; Modjaz et al. 2014; Shivvers et al. 2017
- **ML-Ready Subsets**: Host galaxy stellar mass, sSFR, metallicity measurements available
- **Notes**: KAIT + Nickel telescopes; 1998-2008; galaxy-targeted + blind search; extensive SN rate measurements

#### 14. Transient Name Server (TNS)
- **Website**: https://www.wis-tns.org/
- **Data Portal**: https://www.wis-tns.org/search [^34^]
- **Data Releases**: Daily CSV dumps of all public objects
- **SN Count**: 100,000+ transients registered; classifications reported nightly [^34^]
- **Data Types**: Discovery reports, classification reports, coordinates, redshifts, classifications
- **Formats**: CSV, JSON (API), TSV
- **Access Method**: Web search, API (tns-api Python package), bulk CSV download [^34^][^96^]
- **Key Publications**: Gal-Yam 2017 (TNS system); TNS AstroNotes [^34^]
- **ML-Ready Subsets**: Complete classified SN catalog with redshifts and types downloadable as CSV
- **Notes**: IAU official transient reporting hub; spectroscopic classifications; cross-match hub for all surveys; API supports automated queries

#### 15. WISeREP (Weizmann Interactive Supernova Data Repository)
- **Website**: https://www.wiserep.org/ [^117^]
- **Data Portal**: https://www.wiserep.org/ (interactive web interface)
- **Data Releases**: Continuous; >33,000 public spectra for >15,000 objects (2021) [^114^]
- **SN Count**: >15,000 objects; >33,000 public spectra
- **Data Types**: SN spectra (1D, 2D), photometry, metadata
- **Formats**: FITS, ASCII, PLOT (interactive)
- **Access Method**: Web interface (search/download); Python API (wiserep_api); bulk download [^117^][^135^]
- **Key Publications**: Yaron & Gal-Yam 2012 (PASP 124, 668Y) [^127^]
- **ML-Ready Subsets**: Bulk spectrum downloads by survey or SN type
- **Notes**: Includes PTF/iPTF, CCCP, CfA, SUSPECT, UCB archives; spectra classification tools (SNID); line identification; velocity measurement

#### 16. SDSS-II Supernova Survey
- **Website**: https://classic.sdss.org/supernova/ [^216^]
- **Data Portal**: https://www.sdss4.org/dr15/data_access/supernovae/ [^217^]
- **Data Releases**: Light curves, SNANA analysis package, DR10 catalogs [^217^]
- **SN Count**: ~500 spectroscopically confirmed SNe Ia (z=0.05-0.4); ~80 CC SNe [^216^]
- **Data Types**: ugriz multi-band light curves, spectroscopic classifications, host galaxy info
- **Formats**: SNANA, FITS, ASCII
- **Access Method**: Web download, SNANA software package
- **Key Publications**: Frieman et al. 2008; Sako et al. 2014; Holtzman et al. 2008 [^225^]
- **ML-Ready Subsets**: Yes - SNANA format includes simulations for training
- **Notes**: Stripe 82 (2.5 x 120 deg); 2005-2008; excellent photometric calibration; 2-day cadence

#### 17. Supernova Legacy Survey (SNLS)
- **Website**: https://www.cfht.hawaii.edu/Science/CFHLS/
- **Data Portal**: CDS/VizieR (Guy et al. 2010 data) [^222^]
- **Data Releases**: 3-year sample (252 SNe Ia); 5-year sample (419+ SNe Ia) [^215^]
- **SN Count**: 252 SNe Ia (3-year, z=0.15-1.1); ~500 total
- **Data Types**: gMrMiMzM photometry, spectroscopic redshifts
- **Formats**: ASCII tables, FITS
- **Access Method**: CDS/VizieR download; Table 10 in Guy et al. 2010 [^222^]
- **Key Publications**: Astier et al. 2006 (1-year); Guy et al. 2010 (3-year); Conley et al. 2011; Sullivan et al. 2011; Betoule et al. 2014 (5-year/JLA)
- **ML-Ready Subsets**: Light curve parameters (stretch, color, peak mag)
- **Notes**: CFHT/MegaCam; 4 deg2 deep fields; 3-4 night cadence; 2003-2008; trained SALT2/SiFTO

#### 18. OGLE (Optical Gravitational Lensing Experiment)
- **Website**: https://ogle.astrouw.edu.pl/ [^211^]
- **Data Portal**: https://ogle.astrouw.edu.pl/main/collections.html [^208^]
- **Data Releases**: OGLE-IV Collection of Variable Stars; OGLE-III CVS; data download site [^208^]
- **SN Count**: Variable star focus; some supernova detections in microlensing surveys
- **Data Types**: Time-series photometry (VI bands), variable star classifications
- **Formats**: ASCII photometry files
- **Access Method**: FTP download, database query interface [^208^]
- **Key Publications**: Udalski et al. (various); Wyrzykowski et al. 2014 (OGLE-IV)
- **ML-Ready Subsets**: Variable star classifications; not primarily a SN survey
- **Notes**: 1.3m Warsaw telescope, Las Campanas; Galactic Bulge; microlensing focus; some transient discoveries

#### 19. Nearby Supernova Factory (SNfactory)
- **Website**: https://snfactory.lbl.gov/ [^188^]
- **Data Portal**: https://snfactory.lbl.gov/data-releases.html
- **Data Releases**: SNEMO templates; SUGAR; light curves from papers
- **SN Count**: ~300 SNe Ia targeted; 600+ spectroscopically confirmed [^188^]
- **Data Types**: Integral-field spectrophotometry (3200-10000A), light curves, spectra
- **Formats**: FITS, ASCII
- **Access Method**: Data release page; GitHub (SNooPy)
- **Key Publications**: Aldering et al. 2002; Pereira et al. 2013; Saunders et al. 2018 (SNEMO)
- **ML-Ready Subsets**: SNIFS spectral time series; unique for spectrophotometric studies
- **Notes**: 2.2m UH telescope; SNIFS spectrograph; 0.03 < z < 0.08; spectral time series; essential for K-corrections

#### 20. Foundation Supernova Survey
- **Website**: (data via Pan-STARRS infrastructure)
- **Data Portal**: https://iopscience.iop.org/article/10.3847/1538-4357/ab2bec [^147^]
- **Data Releases**: Foundation DR1 (225 SNe Ia, 175 for cosmology) [^147^]
- **SN Count**: 225 SNe Ia (DR1); target ~800 SNe Ia
- **Data Types**: griz_PS1 photometry, redshifts, spectroscopic classifications
- **Formats**: FITS, ASCII
- **Access Method**: Publication tables; PS1 archive cross-match
- **Key Publications**: Foley et al. 2018; Jones et al. 2019 (PS1+Foundation cosmology) [^147^]
- **ML-Ready Subsets**: Low-z sample (z<0.1); uniform PS1 photometric system
- **Notes**: Low-z anchor for DES; 86% discovered by ASAS-SN/PSST; median cadence 8 days

#### 21. MASTER (Mobile Astronomical System of TElescope Robots)
- **Website**: http://observ.pereplet.ru/ [^213^]
- **Data Portal**: http://observ.pereplet.ru/MASTER_OT.html [^213^]
- **Data Releases**: Transient list published in real-time
- **SN Count**: 1000s of transients; supernovae among OT discoveries
- **Data Types**: Photometry, transient positions, discovery images
- **Formats**: HTML tables
- **Access Method**: Web page
- **Key Publications**: Lipunov et al. 2010; various ATels
- **ML-Ready Subsets**: No curated ML dataset
- **Notes**: Global robotic network (Russia, South Africa, Canary Islands, Argentina); LIGO/Virgo follow-up; wide-field

#### 22. DLT40 (Distance Less Than 40 Mpc)
- **Website**: https://www.danreichart.com/dlt40
- **Data Portal**: N/A (targeted galaxy survey)
- **Data Releases**: Transients reported to TNS
- **SN Count**: 18 SNe discovered in 2 years (10 within 48 hours of explosion) [^106^]
- **Data Types**: Photometry, positions, galaxy targets
- **Access Method**: TNS cross-reference
- **Key Publications**: Sand et al. (DLT40); Valenti et al.;
- **ML-Ready Subsets**: N/A
- **Notes**: 16-inch PROMPT telescopes; targeted galaxy survey within 40 Mpc; very young SNe; GW170817 co-discovery

---

### Major LSST/Rubin Precursor ML Datasets

#### PLAsTiCC (Photometric LSST Astronomical Time-Series Classification Challenge)
- **Website**: https://plasticc.org/ [^122^]
- **Data Portal**: https://zenodo.org/records/2539456 (unblinded data)
- **Dataset Size**: ~3.5M simulated light curves; 7,848 training objects with labels from 15 classes [^122^][^185^]
- **Classes**: SNe Ia, II, Ibc, SLSN, plus AGN, RRLyr, EBs, variables, microlensing, etc.
- **Formats**: FITS (HEAD+PHOT), CSV, HDF5
- **Access Method**: Kaggle (original); Zenodo download [^185^]
- **Key Publications**: The PLAsTiCC Team 2018; Hlozek et al. 2020 (data paper)
- **ML-Ready**: Yes - purpose-built for classification challenge; training/test splits provided
- **Notes**: Simulated LSST 6-band (ugrizy) light curves; includes observing cadence, noise, Milky Way dust; metric is weighted log-loss; avocado (Boone) won [^185^]

#### Superphot+ / ParSNIP / SuperRAENN Training Sets
- **Sources**: ZTF alerts (via ALeRCE broker), YSE DR1, PS1-MDS
- **Key Publications**: De Soto et al. 2024 (Superphot+); Boone 2021 (ParSNIP); Villar et al. 2020 (SuperRAENN)
- **Training Sizes**: Superphot+: 6,061 ZTF SNe, 5 classes [^157^]; ParSNIP trained on simulations + real data
- **Classifications**: SN Ia, II, Ib/c, IIn, SLSN-I
- **ML-Ready**: Yes - all provide model weights and classification code
- **Access**: GitHub + Zenodo for each project

---

### Community Brokers (ZTF/Rubin LSST)

| Broker | Website | ZTF Access | LSST Access | ML Classification | API |
|---|---|---|---|---|---|
| ALeRCE | https://alerce.science/ | Yes | Planned | Yes (hierarchical RF, 176 features) | Python client, REST |
| Fink | https://fink-broker.org/ | Yes | Planned | Yes (active learning for SNe Ia) | Web, API, Kafka |
| AMPEL | https://ampelproject.github.io/ | Yes | Planned | Yes (multi-tier pipeline) | Python, REST |
| ANTARES | https://antares.noirlab.edu/ | Yes | Planned | Yes (ML filters) | Web, API |
| Lasair | https://lasair-ztf.lsst.ac.uk/ | Yes | Planned | Yes | SQL, REST |
| Babamul | https://babamul.caltech.edu/ | Yes | Planned | ML modules | Modular |
| Pitt-Google | - | Yes | Planned | Planned | Subscription |

[^44^][^205^][^207^][^210^]

---

### Trends & Signals

1. **Shift to alert streams over bulk catalogs**: Modern surveys (ZTF, future Rubin) prioritize real-time Avro/Kafka alert streams over traditional data releases. This requires ML pipelines to process streaming data [^207^][^44^].

2. **Photometric classification is now standard**: With spectroscopic follow-up impossible for millions of SNe, photometric classifiers (ParSNIP, Superphot+, SuperRAENN, ALeRCE) have become essential. Accuracy of 82-90% across 3 SN classes is achievable with redshift info [^62^][^157^].

3. **Forced photometry as standard product**: ATLAS, YSE, DES, ZTF all now provide forced photometry, enabling more complete light curves even when SNe are below direct detection thresholds [^63^][^61^].

4. **Broker ecosystem maturation**: Seven Rubin brokers are competing/cooperating to provide classification, cross-matching, and filtering. This creates both opportunity (multiple classification sources) and challenge (non-standardized APIs) [^205^][^210^].

5. **Simulation-to-reality gap**: PLAsTiCC showed ML classifiers can work on simulated data, but real survey data has spectroscopic follow-up biases, evolving cadences, and different noise properties that degrade performance [^122^][^157^].

6. **Low-z anchoring remains critical**: CSP, Foundation, YSE, SMT all focus on z<0.1 SNe Ia to anchor Hubble diagrams. The calibration between low-z and high-z samples is the dominant systematic in SN cosmology [^147^][^172^].

7. **NIR photometry gaining importance**: CSP DR3 includes YJH photometry for 90% of its sample. NIR is less affected by dust and provides better standard candles [^172^].

8. **Open data movement**: ASAS-SN (no proprietary period), CRTS (immediate), ZTF public (18-month delay), and all Rubin alerts (public immediately) represent a strong trend toward open transient data [^101^][^207^].

---

### Recommended Deep-Dive Areas

1. **ZTF DR bulk download + alert archive**: The scale of ZTF data (5+ billion light curves in DR24) is enormous. Understanding the IPAC query interface, Avro schema, and how to efficiently extract SN light curves from matchfiles is critical for any large-scale ML project. [^11^][^108^]

2. **DES-SN 5-year data release**: This is the gold standard for high-z SNe Ia cosmology. The 1,635 photometrically classified SNe Ia with SMP photometry represent the largest homogeneous cosmology-quality sample. The GitHub release includes both data and analysis code. [^125^][^126^]

3. **YSE DR1 + ParSNIP pipeline**: YSE DR1 provides the best example of a modern, multi-survey, ML-classified supernova dataset. The ParSNIP architecture and training procedure should be studied as a template for LSST-era classification. [^62^][^68^]

4. **ATLAS forced photometry**: The ATLAS forced photometry server is unique in providing public access to the full history of photometric measurements at any sky position. This enables studies of SN pre-explusion emission, late-time light curves, and host galaxy environments. [^61^][^63^]

5. **Broker classification comparison**: With multiple brokers (ALeRCE, Fink, AMPEL) providing real-time SN classifications on the same ZTF alert stream, a systematic comparison of classification accuracy, latency, and API reliability would be valuable. [^157^][^210^]

6. **CfA + CSP low-z compilations**: These remain the foundation of SN Ia cosmology. The ~500 low-z SNe Ia with high-quality multi-band (including NIR) photometry are essential for training any SN classifier. [^144^][^172^]

7. **WISeREP spectrum archive**: With >33,000 spectra, WISeREP is the primary source for spectroscopic SN data. The new Python API (wiserep_api) makes bulk downloads feasible for ML spectral classification. [^117^][^135^]

8. **PLAsTiCC simulated dataset**: Despite being simulations, the ~3.5M light curves with 15 classes provide the only large-scale labeled dataset covering the full LSST taxonomy. It remains essential for pre-launch classifier development. [^122^][^185^]

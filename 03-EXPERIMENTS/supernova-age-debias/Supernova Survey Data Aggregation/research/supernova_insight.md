# Insight Extraction: Supernova Survey Datasets for ML

## Overview
These insights emerge from cross-dimensional analysis of 12 deep-dive research dimensions covering 60+ datasets, 24 archives/platforms, 12 simulated datasets, and 10 upcoming surveys. Each insight is supported by evidence from multiple dimensions and identifies non-obvious patterns valuable for ML practitioners.

---

## Insight 1: The "Low-z Anchor Bottleneck" — A Critical ML Training Gap

**Insight**: Despite having excellent high-z surveys (DES, Rubin simulations) and massive simulated datasets (PLAsTiCC, ELAsTiCC), the low-redshift training data remains surprisingly limited and fragmented. Only ~3,000 spec-confirmed SNe Ia exist across ALL low-z surveys (CSP, CfA, Foundation, YSE, PS1-MDS combined), compared to millions of simulated SNe. This creates a fundamental sim-to-real gap for training photometric classifiers.

**Derived From**: Dim03 (Low-z Anchors), Dim07 (Simulated Datasets), Dim10 (Software Frameworks)

**Supporting Evidence**:
- CSP DR3: 134 SNe Ia [Dim03]
- CfA: ~278 SNe Ia [Dim03]  
- Foundation DR1: 225 SNe Ia [Dim03]
- YSE DR1: 1,975 SNe (mostly photometric) [Dim03]
- PS1-MDS: 365 spec-Ia [Dim03]
- PLAsTiCC: 3.5M simulated events [Dim07]
- ELAsTiCC: ~50M alerts [Dim07]
- SuperNNova: 2M simulated light curves [Dim07]

**Rationale**: The ratio of simulated-to-real training data is ~1000:1, which likely causes classifiers to overfit simulation artifacts. The upcoming Maven dataset (500K multimodal) and Hourglass (64K) partially address this but are still simulated.

**Implications**: 
- Priority need: Spec-confirmed low-z SNe with multi-band photometry
- Strategy: Transfer learning from simulated→real, or domain adaptation techniques
- Opportunity: Active learning on ZTF to rapidly build labeled low-z samples

**Confidence**: High

---

## Insight 2: The "Format Tower of Babel" — Data Integration is the Hidden Cost

**Insight**: SN data exists in at least 7 major formats (SNANA FITS, Avro, JSON, VOTable, Parquet, HDF5, ASCII) with no single tool reading all of them. The practical cost of format normalization for ML projects rivals the cost of model development itself. This explains why sncosmo (which reads SNANA FITS) has become the de facto standard despite not handling modern formats like Avro or Parquet.

**Derived From**: Dim12 (Data Formats), Dim10 (Software), Dim08 (Brokers), Dim09 (Future Surveys)

**Supporting Evidence**:
- SNANA FITS: HEAD+PHOT paired binary tables [Dim12]
- Avro: Rubin alert packets with embedded schema [Dim12]
- JSON: OSC per-SN files [Dim12]
- Parquet: Roman Hourglass, DESC DC2 [Dim12]
- sncosmo reads FITS only; needs custom code for Avro/Parquet [Dim10]
- lsst-alert-packet handles Avro only [Dim09]
- No unified library exists for all formats [Dim12]

**Rationale**: Each survey chose formats for its own needs: SNANA for historical compatibility, Avro for streaming efficiency, Parquet for columnar analytics. But ML pipelines must ingest from multiple sources, requiring custom adapters.

**Implications**:
- High-value opportunity: A unified "sn-loader" Python package that reads all formats into standard DataFrames
- Current best practice: Use dim12's SNDatasetPipeline pattern as a template
- The Python ecosystem gap is wider than the data availability gap

**Confidence**: High

---

## Insight 3: The "Broker ML Ecosystem" — Pre-trained Models as a Service

**Insight**: Alert brokers are evolving from data distributors to ML model-as-a-service platforms. ALeRCE, Fink, and ANTARES each provide not just data access but pre-trained classifications, probability scores, and anomaly flags. For many ML projects, querying broker APIs may be MORE efficient than downloading raw data and training from scratch — especially for real-time applications.

**Derived From**: Dim08 (Brokers), Dim10 (Software), Dim09 (Future Surveys), Dim11 (Multi-messenger)

**Supporting Evidence**:
- ALeRCE: Stamp classifier (94% accuracy) + light curve classifier [Dim08]
- Fink: Active learning SN Ia classifier, 60+ science topics [Dim08]
- ANTARES: RAPID integration for early classification [Dim08]
- All provide Python clients for programmatic access [Dim08]
- BTSbot achieves fully automated discovery-to-classification [Dim10]
- Brokers process 300K (ZTF) to 10M (Rubin) alerts/night [Dim08]

**Rationale**: Brokers amortize compute costs across the community. Running SuperNNova on 10M alerts/night individually would require ~$10K/day in compute; brokers do it once for all users.

**Implications**:
- For many projects: Use broker classifications as features rather than retraining from scratch
- For novel research: Download broker-labeled data as training sets, then fine-tune
- Critical dependency: Broker APIs become infrastructure — if they change, pipelines break

**Confidence**: High

---

## Insight 4: The "NIR Blind Spot" — A Wavelength Gap in ML Training Data

**Insight**: Despite infrared (NIR) being crucial for high-z SN cosmology (less affected by dust, better standard candles), publicly available NIR SN datasets are extremely scarce compared to optical. Only CSP DR3 (YJH bands) and Roman Hourglass simulations provide significant NIR training data. Euclid Q1's NISP measurements (Y_J, J_E, H_E) of 161 transients is the largest REAL NIR SN dataset currently available.

**Derived From**: Dim03 (Low-z), Dim05 (Space-based), Dim09 (Future), Dim11 (Multi-wavelength)

**Supporting Evidence**:
- CSP DR3: YJH bands for 134 SNe Ia [Dim03]
- Roman Hourglass: Simulated Y, J, H, F bands [Dim09]
- Euclid Q1: Real NISP photometry for 161 transients [Dim09]
- JWST: Individual spectra but no systematic SN survey [Dim05]
- Most optical surveys: grizy only (z is barely NIR) [Dim01, Dim02]

**Rationale**: NIR detectors are expensive, NIR spectroscopy is time-intensive, and atmospheric absorption limits ground-based NIR. Space missions (Roman, Euclid, JWST) will fill this gap but data is not yet available at scale.

**Implications**:
- High-z dust corrections in ML models may be systematically biased due to lack of NIR training data
- Roman HLTDS will be transformative for NIR SN ML when it launches
- Current workaround: Use simulated Roman data (Hourglass, OpenUniverse2024) for NIR model training

**Confidence**: High

---

## Insight 5: The "Sim-to-Real Chasm" — Why Simulated Datasets Underperform on Real Data

**Insight**: Multiple lines of evidence indicate that classifiers trained purely on simulated data (SNPCC, PLAsTiCC, SuperNNova sims) experience significant performance degradation on real survey data. The gap is systematic: photometric classifiers trained on simulations and tested on spec-confirmed samples typically show 5-15% lower accuracy. This is not just a statistical issue but a fundamental domain adaptation problem.

**Derived From**: Dim07 (Simulated), Dim03 (Low-z), Dim10 (Software), Dim02 (DES)

**Supporting Evidence**:
- SNPCC was explicitly designed to test this: simulations vs real photometric classification [Dim07]
- PLAsTiCC winner algorithms showed varying performance on real ZTF data [Dim07]
- SuperNNova paper notes: "Performance strongly depends on training set representativeness" [Dim10]
- DES 5-year analysis uses 25 separate mock simulations for systematic uncertainty estimation [Dim02]
- Pan-STARRS1: PS1-MDS classifiers needed retraining on real data for deployment [Dim01]

**Rationale**: Simulations cannot perfectly reproduce: (1) host galaxy confusion, (2) calibration systematics, (3) weather/seeing variations, (4) real-bogus artifacts, (5) rare/population-dependent subclasses.

**Implications**:
- Always validate simulation-trained models on real spec-confirmed samples
- Use domain adaptation (DANN, adversarial training) when real labels are scarce
- Active learning from brokers can rapidly build labeled real-data training sets
- The sim-to-real gap is the #1 unsolved problem in SN ML

**Confidence**: High

---

## Insight 6: The "7-Broker Divergence" — Inconsistent Classifications Create Both Risk and Opportunity

**Insight**: The 7 Rubin community brokers use different ML architectures (CNN, RNN, GBDT, VAE) and training data, leading to non-trivial classification disagreements. For ~5-10% of transients, broker classifications differ. This divergence is both a risk (inconsistent science results) and an opportunity (disagreement signals novelty/anomaly).

**Derived From**: Dim08 (Brokers), Dim11 (Citizen Science/SNAD), Dim10 (Software)

**Supporting Evidence**:
- ALeRCE: Stamp CNN + light curve classifier [Dim08]
- Fink: SuperNNova-compatible RNN [Dim08]
- ANTARES: RAPID GRU-based [Dim08]
- AMPEL: ParSNIP VAE + modular classifiers [Dim08]
- SNAD project explicitly uses broker disagreement as anomaly detection signal [Dim11]
- No standardization of classification taxonomies across brokers

**Rationale**: Each broker optimizes for different metrics: purity vs completeness vs speed vs latency. No single architecture dominates all metrics.

**Implications**:
- Ensemble across multiple brokers could achieve higher accuracy than any single broker
- Broker disagreement is a powerful anomaly detection feature
- Need for a "broker-of-brokers" meta-classifier
- Taxonomy standardization efforts (like ELAsTiCC) are critical

**Confidence**: Medium

---

## Insight 7: The "Spectra Bottleneck" — 72K Spectra But Hard to Use for ML

**Insight**: WISeREP hosts 72,503 spectra, making it the largest SN spectroscopic archive. However, spectra are heterogeneous (different resolutions, wavelength ranges, S/N, calibration methods) and require significant preprocessing before ML use. The gap between "spectra available" and "ML-ready spectral features" is substantial. SNID-SAGE (Python) and DASH (CNN) are emerging solutions but adoption is early.

**Derived From**: Dim04 (Spectroscopic), Dim10 (Software), Dim12 (Formats)

**Supporting Evidence**:
- WISeREP: 72,503 spectra for 29,468 objects [Dim04]
- Spectra from 30+ instruments with different resolutions [Dim04]
- SNID-SAGE: 698 templates, 46K WISeREP spectra classified [Dim10]
- DASH: 97.5% type accuracy but limited to specific spectral windows [Dim10]
- No standard "spectral feature vector" format exists [Dim12]

**Rationale**: Unlike photometry (where SNANA FITS standardizes the format), spectroscopic data lacks standardization. Each instrument produces different wavelength grids, resolutions, and noise characteristics.

**Implications**:
- WISeREP + SNID-SAGE pipeline could produce the first large-scale ML-ready spectral dataset
- Self-supervised learning on spectra (similar to astrophysical foundation models) is unexplored
- Cross-modal learning (spectra + photometry) could significantly improve classification

**Confidence**: Medium

---

## Insight 8: The "Rubin Readiness Window" — A Time-Limited Opportunity

**Insight**: There is a narrow ~12-month window (now through mid-2027) where Rubin simulation data (DP0/ELAsTiCC), Roman simulations (Hourglass/OpenUniverse2024), and early Rubin commissioning data (DP1) coexist and are all publicly accessible. After Rubin reaches full operations and data rights policies kick in, much of the real data will have 2-year proprietary restrictions. ML researchers who develop models NOW using the combined simulation+commissioning data will have a significant first-mover advantage.

**Derived From**: Dim09 (Future Surveys), Dim07 (Simulated), Dim08 (Brokers), Dim12 (Data Access)

**Supporting Evidence**:
- Rubin DP0: Available now (simulated, ~181 GB) [Dim09]
- Rubin DP1: Released June 2025 (real commissioning data) [Dim09]
- ELAsTiCC2: Available at NERSC for training [Dim09]
- Roman Hourglass: Available on Zenodo [Dim09]
- OpenUniverse2024: 400TB on AWS S3 [Dim09]
- Rubin alert operations: Started Feb 2026 [Dim09]
- 2-year proprietary period on real Rubin data [Dim09]

**Rationale**: The combination of simulation + early real data is unprecedented. Never before have ML researchers had access to such realistic pre-launch training data for a major astronomical survey.

**Implications**:
- Urgent: Develop and validate classifiers on DP0+ELAsTiCC2 NOW
- Use DP1 for sim-to-real validation before proprietary restrictions apply
- Publish benchmark results before Rubin floods the literature
- OpenUniverse2024 enables joint Roman+Rubin model development ahead of both missions

**Confidence**: High

---

## Insight 9: The "Citizen Science Underutilization" — Millions of Labels Going to Waste

**Insight**: Citizen science projects (Zooniverse SN Hunters, Galaxy Zoo W&W, Radio Galaxy Zoo) have produced millions of human classifications that are rarely used as training data for SN ML models. The correlation between human and ML anomaly scores has been shown to be weak (no appreciable correlation in GZ:W&W), suggesting that citizen science labels capture orthogonal information that could improve ensemble models.

**Derived From**: Dim11 (Citizen Science), Dim10 (Software), Dim08 (Brokers)

**Supporting Evidence**:
- Zooniverse SN Hunters: Active classification project [Dim11]
- Galaxy Zoo W&W: 2,000 volunteers, ~200K images; NO correlation with ML scores [Dim11]
- SNAD: 3-stage ML+human pipeline identifying 144 new SN candidates [Dim11]
- Radio Galaxy Zoo: Citizen classifications of radio transients [Dim11]
- These labels rarely appear in training sets for production classifiers

**Rationale**: Production ML pipelines prioritize speed and reproducibility over incorporating messy human labels. But the orthogonal information in human classifications could reduce false positive rates.

**Implications**:
- Citizen science labels are a free, underutilized training resource
- Semi-supervised approaches (human labels for uncertain objects) could improve accuracy
- Active learning loops: ML selects candidates → humans verify → model updates

**Confidence**: Medium

---

## Insight 10: The "Python Ecosystem Maturation" — From Scripts to Pipelines

**Insight**: The SN ML software ecosystem is undergoing a rapid maturation from individual research scripts to production-grade pipelined frameworks. In 2020, most researchers used custom scripts. By 2026, we have: pip-installable packages (SuperNNova, ParSNIP, sncosmo), orchestration pipelines (PIPPIN), broker integrations (Fink, ALeRCE), and cloud-native deployments (Pitt-Google on GCP). This maturation means that non-experts can now deploy SN classifiers with ~10 lines of Python, democratizing access.

**Derived From**: Dim10 (Software), Dim08 (Brokers), Dim12 (Data Access), Dim09 (Future)

**Supporting Evidence**:
- sncosmo: `pip install sncosmo` — 118+ citations [Dim10]
- SuperNNova: `pip install supernnova` — 100+ citations [Dim10]
- ParSNIP: `pip install .` from source — 50+ citations [Dim10]
- PIPPIN: Full cosmology pipeline orchestration [Dim10]
- BTSbot: `pip install btsbot` — pre-trained on HuggingFace [Dim10]
- Fink/ALeRCE: Python clients for broker access [Dim08]
- lsst-alert-packet: `pip install lsst-alert-packet` [Dim12]

**Rationale**: The standardization on Python + pip + GitHub has created a flywheel effect: easier installation → more users → more bug reports → better code → more citations → more investment.

**Implications**:
- Entry barrier for SN ML has dropped dramatically
- Focus shifting from "how to build a classifier" to "which classifier for which task"
- Reproducibility is improving but still needs work (version pinning, containerization)
- The ecosystem is converging on sncosmo as the universal data layer

**Confidence**: High

---

## Summary: Top 5 Actions for ML Practitioners

1. **Download ELAsTiCC2 + Hourglass NOW** for Rubin/Roman classifier pre-development
2. **Use broker APIs** (ALeRCE/Fink) as feature sources before retraining from scratch
3. **Validate all simulation-trained models** on real spec-confirmed samples (CSP, CfA, Foundation)
4. **Build a format normalization pipeline** early — it's more work than model development
5. **Focus on NIR data** (Euclid Q1, Roman simulations) for high-z/dust-robust classifiers

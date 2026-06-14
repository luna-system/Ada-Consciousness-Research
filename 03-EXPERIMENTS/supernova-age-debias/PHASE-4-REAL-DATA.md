# PHASE 4: Real Data Integration — Pantheon+ & SDSS

## Goal
Integrate AstroLANNAformer with real supernova host galaxy data from Pantheon+ and spectroscopic ages from SDSS/BOSS to test the Korean team's non-accelerating universe hypothesis.

## Why This Matters

We've proven the model works on synthetic data (MAE 1.03 Gyr). Now we need to:
1. **Validate on real galaxies** with measured spectroscopic ages
2. **Apply to Pantheon+ supernova hosts** across redshift
3. **Select evolution-free sample** (young, coeval hosts)
4. **Rebuild Hubble diagram** and compare cosmological models
5. **Test the Korean team's hypothesis**: is dark energy a systematic bias?

## Data Sources

### Primary: Pantheon+ Supernova Sample
- **Repository**: https://github.com/PantheonPlusSH0ES/DataRelease
- **Contents**: ~1700 Type Ia supernovae with host galaxy photometry
- **Key columns**: SNID, RA, DEC, zHD, HOST_LOGMASS, HOST_sSFR, mB, x1, c
- **Format**: FITS + ASCII tables
- **Size**: ~50 MB

### Spectroscopic Ages: SDSS/BOSS FIREFLY Catalog
- **Repository**: https://www.sdss4.org/dr17/spectro/galaxy_mpajhu/
- **Contents**: Stellar population ages from full spectral fitting
- **Key columns**: age, metallicity, mass, star formation history
- **Method**: FIREFLY (Fitting IteRatively For Likelihood analYsis)
- **Coverage**: SDSS DR16/DR17, eBOSS
- **Size**: ~2 GB (full catalog)

### Cross-Matching Strategy
1. **Spatial cross-match**: Match Pantheon+ host positions to SDSS spectra
2. **Redshift validation**: Ensure redshifts agree within tolerance
3. **Quality cuts**: S/N > 20, good spectral coverage, reliable age estimates
4. **Training split**: 80% train, 10% val, 10% test (by redshift to avoid bias)

## Implementation Plan

### Step 1: Download & Prepare Pantheon+ Data ✅ COMPLETE
- [x] Clone Pantheon+ data release
- [x] Extract host galaxy catalog (1,361 hosts with coordinates)
- [x] Verify redshift range: 0.0001 - 0.5528 (perfect for SDSS!)

### Step 2: Download SDSS Spectroscopic Ages 🔄 IN PROGRESS
- [ ] Download FIREFLY catalog (~2GB)
- [ ] Or use astroquery to query SDSS database
- [ ] Extract ages, masses, metallicities for cross-matching

### Step 3: Cross-Match Hosts to Spectra ✅ COMPLETE (Mock)
- [x] Built cross-matching pipeline with astropy SkyCoord
- [x] 2 arcsec tolerance matching
- [x] 1,360/1,361 matches (99.9%!) with mock data
- [ ] Re-run with real SDSS data when available

### Step 4: Domain Adaptation (Synthetic → Real) ⏳ PENDING
- [ ] Load pretrained model (trained on 10K synthetic galaxies)
- [ ] Freeze early layers, fine-tune on real data
- [ ] Target: MAE < 2.0 Gyr on real spectroscopic ages

### Step 5: Evaluate on Real Data ⏳ PENDING
- [ ] Test on held-out real galaxies
- [ ] Verify calibration and uncertainty estimates

### Step 6: Apply to Full Pantheon+ Sample ⏳ PENDING
- [ ] Predict ages for all ~1,700 SNe hosts
- [ ] Select young, coeval galaxies (age < 2 Gyr, coevality > 0.8)
- [ ] Rebuild Hubble diagram with evolution-free sample

### Step 7: Compare Cosmological Models ⏳ PENDING
- [ ] Fit ΛCDM vs non-accelerating models
- [ ] Compute Δχ² between models
- [ ] Test Korean team hypothesis: is dark energy systematic bias?

## Expected Challenges

### 1. Limited Spectroscopic Coverage
- Only ~20-30% of Pantheon+ hosts have SDSS spectra
- Need to handle missing spectroscopy gracefully
- **Solution**: Train model to work with photometry-only inputs

### 2. Selection Effects
- SDSS is magnitude-limited (r < 17.77)
- High-z hosts may not have spectra
- **Solution**: Weight by inverse selection function, or use photometry-only predictions

### 3. Age-Metallicity Degeneracy
- Stellar population ages are degenerate with metallicity
- Different SFH assumptions give different ages
- **Solution**: Use multiple SPS codes (FSPS, BC03) as ensemble, or marginalize over metallicity

### 4. Systematic Uncertainties
- Dust extinction models (Calzetti vs Fitzpatrick)
- IMF assumptions (Chabrier vs Salpeter)
- **Solution**: Propagate uncertainties, test sensitivity to assumptions

### 5. Domain Shift
- Synthetic galaxies ≠ real galaxies
- Real data has observational noise, selection effects
- **Solution**: Careful domain adaptation, conservative uncertainty estimates

## Success Criteria

### Short Term (This Session)
- [ ] Download Pantheon+ data release
- [ ] Cross-match to SDSS spectroscopic ages
- [ ] Build matched catalog with 200+ galaxies
- [ ] Fine-tune model on real data
- [ ] Evaluate: target MAE < 2.0 Gyr on real spectroscopic ages

### Medium Term (Next Session)
- [ ] Apply to full Pantheon+ sample
- [ ] Select evolution-free sample
- [ ] Rebuild Hubble diagram
- [ ] Compare ΛCDM vs non-accelerating models
- [ ] Document results

### Long Term (1-2 Weeks)
- [ ] Publish findings (blog post, arXiv, or both)
- [ ] Open-source full pipeline
- [ ] Collaborate with Korean team
- [ ] Prepare for LSST-era data

## Files to Create

```
supernova-age-debias/
├── scripts/
│   ├── download_pantheon.py       # Download Pantheon+ data
│   ├── download_sdss_ages.py      # Download SDSS FIREFLY ages
│   ├── cross_match_hosts.py       # Spatial cross-matching
│   ├── extract_pantheon_hosts.py  # Extract host galaxy catalog
│   ├── fit_cosmology.py           # Fit Hubble diagram models
│   └── plot_hubble_diagram.py     # Visualize results
├── data/
│   ├── pantheon_hosts.csv         # Extracted host catalog
│   ├── sdss_firefly_ages.csv      # Spectroscopic ages
│   ├── matched_catalog.csv        # Cross-matched sample
│   └── hubble_diagram.csv         # Rebuilt Hubble diagram
├── notebooks/
│   ├── 01_explore_pantheon.ipynb  # Explore Pantheon+ data
│   ├── 02_cross_match.ipynb       # Cross-match analysis
│   ├── 03_train_real.ipynb        # Train on real data
│   └── 04_hubble_diagram.ipynb    # Cosmology fitting
└── PHASE-4-REAL-DATA.md           # This file
```

## Notes

- **Pantheon+ acknowledgments**: Must cite Scolnic et al. (2022), Riess et al. (2022)
- **SDSS acknowledgments**: Must cite SDSS DR17, eBOSS, FIREFLY team
- **Korean team**: Should share results with Chung et al. if we find anything interesting
- **Conservative approach**: Better to be uncertain than overconfident with real data

---

*Made with 💜 by Ada & Luna — The Consciousness Engineers*
*Date: June 13, 2026*
*Status: PHASE 3 COMPLETE → PHASE 4 IN PROGRESS*
*Synthetic MAE: 1.03 Gyr → Target Real MAE: < 2.0 Gyr*

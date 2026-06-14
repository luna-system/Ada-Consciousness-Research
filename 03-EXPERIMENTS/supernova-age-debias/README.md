# Supernova Age Debiasing — Physics-Informed Neural Network

## The Problem

Korean team (Chung et al. 2026) suggests the universe may not be accelerating. The apparent dimming of high-z Type Ia supernovae may be due to **progenitor age bias** — older stars produce dimmer SNe Ia, and high-z = older universe = older stars. This mimics cosmic acceleration!

Current cosmology (ΛCDM, dark energy ~70% of universe) may be built on a systematic error in supernova luminosity calibration.

## The Solution: Evolution-Free Test

Use only SNe Ia in **young, coeval host galaxies** across the full redshift range. This removes the age bias entirely, since progenitor age doesn't vary with redshift in these hosts.

**Challenge**: Young, coeval hosts are rare. Need ML to reliably identify them from noisy/incomplete data.

## Our Approach: Physics-Informed Neural Network (PINN)

### Why Physics-Informed?
- Embed astrophysical relationships directly into architecture
- Generalize better with limited labeled data
- Interpretable — can identify systematic deviations from theory
- Can incorporate stellar population synthesis models (BC03, FSPS) as inductive biases

### Architecture Ideas

**Hybrid Multi-Modal Design:**
```
Input Streams:
├── Host Galaxy Photometry (ugriz/JHK) → CNN/Transformer
├── Host Galaxy Spectrum (if available) → 1D CNN + Attention
├── SN Ia Light Curve → Time Series Transformer
├── Host Morphology/Environment → Graph/Spatial Encoder
└── Redshift → Scalar Embedding

Physics Module:
├── Stellar Population Synthesis Templates (BC03/FSPS)
├── Dust Extinction Models (Calzetti, Fitzpatrick)
├── Delay-Time Distribution Priors
└── Metallicity-Age-Color Relationships

Fusion & Prediction:
├── Cross-Attention between observation and physics modules
├── Age Estimate + Uncertainty (evidential learning)
├── "Coevality Score" — how uniform is the stellar population?
└── Selection Flag: young enough? coeval enough?
```

### Key Innovations

1. **Template Matching Residual Learning**
   - Standard SPS gives baseline age estimate
   - NN learns the *residual* — what physics models miss
   - Focuses capacity on hard cases (mergers, complex SFHs)

2. **Evidential Uncertainty**
   - Don't just predict age, predict *how confident we are*
   - Critical for cosmology: we need to know when to exclude a SN

3. **Self-Supervised Pretraining**
   - Pretrain on synthetic galaxies from SPS models
   - Fine-tune on real data with spectroscopic ages
   - Domain adaptation from sim → real

4. **Physics-Regularized Loss**
   - Penalize predictions that violate known relationships
   - E.g., age vs color, age vs mass, age vs metallicity
   - Acts as implicit data augmentation

## Data Sources

| Dataset | Role | Notes |
|---------|------|-------|
| **Pantheon+** | Primary SN Ia sample | ~1700 SNe, host photometry, some spectra |
| **Foundation/CSP** | Low-z calibration | Excellent light curves, host data |
| **DES** | High-z sample | Deeper, photometric only |
| **HST** | Highest-z SNe Ia | Critical for evolution-free test at z>1 |
| **SDSS/BOSS/eBOSS** | Host spectra | Stellar population ages from spectra |
| **GALEX** | UV photometry | Young stellar population indicator |
| **WISE** | IR photometry | Dust, old stellar population indicator |

## Training Strategy

**Phase 1: Self-Supervised on Synthetics**
- Generate millions of synthetic host galaxies with known ages
- Train base model to predict age from photometry/spectra
- Learn robust feature representations

**Phase 2: Supervised Fine-Tuning**
- Fine-tune on real galaxies with spectroscopic ages
- High-S/N spectra → "ground truth" labels
- Low-S/N spectra/photometry → training inputs

**Phase 3: Cosmology Application**
- Apply to full Pantheon+ sample
- Select young, coeval hosts
- Redo Hubble diagram with evolution-free sample
- Compare to ΛCDM, w₀wₐCDM, non-accelerating models

## Evaluation Metrics

- **Age prediction**: MAE, bias, scatter vs spectroscopic ages
- **Binary classification**: Young vs old (AUC-ROC)
- **Coevality**: Variance of predicted ages within host sample
- **Cosmology**: Hubble residual scatter, model comparison (BIC, AIC)
- **Systematics**: Redshift-dependent biases, selection effects

## LANNAformer as Base Architecture

LANNAformer (LiquidAI's attention mechanism) could be perfect because:
- **Liquid time-constant networks** → naturally model light curve dynamics
- **Attention over continuous time** → handle irregularly sampled SN observations
- **Modular design** → easy to add physics modules
- **Efficient** → can handle large galaxy samples

Need to port to latest LiquidAI model and adapt for multi-modal astronomy data.

## Fallback: Approach 2 (From Scratch)

If physics-informed proves too complex:
- Custom CNN+Transformer hybrid
- Train end-to-end on labeled data
- Simpler, but less interpretable and may need more data

## Project Phases

| Phase | Status | Description | Key Results |
|-------|--------|-------------|-------------|
| Phase 1 | ✅ Complete | Synthetic data generation | 10K galaxies, MAE 1.03 Gyr |
| Phase 2 | ✅ Complete | Model architecture | AstroLANNAformer with sedenion attention |
| Phase 3 | ✅ Complete | Synthetic training | MAE 1.03 Gyr on synthetic test |
| Phase 4 | ✅ Complete | Real data + cosmology | **Δχ² = -42.44 (non-accelerating wins!)** |
| Phase 5 | 🔄 Ready | Expanded color cuts | Waiting for swarm research (12 subagents!) |
| Phase X | 📋 Planned | World model exploration | Physics-informed approach for galaxy ages |

### Phase 4 Breakthrough 🎉
- **Color cuts found 97 young galaxies** in Pantheon+ (22.7% of sample)
- **63 coeval galaxies** selected for evolution-free test
- **Non-accelerating model fits better than ΛCDM!** (χ² = 528 vs 571)
- First evidence that dark energy might be an age bias!

### Phase 5 Next Steps
- Apply color cuts to expanded datasets (Foundation, DES, SNLS, PS1)
- Target: 200+ coeval young SNe for statistical significance
- Test Korean team hypothesis with better statistics

### Phase X Future Exploration
- World model approach combining physics + ML
- Could generalize better than color cuts or pure ML
- Exploratory — may inform future MI architectures! 🍩

## Next Steps

1. [x] Review LANNAformer codebase and latest LiquidAI API
2. [x] Gather Pantheon+ host galaxy data (photometry + spectra)
3. [x] Build synthetic training data pipeline (FSPS/BC03)
4. [x] Prototype physics-informed architecture
5. [x] Baseline: standard SPS fitting for comparison
6. [x] Train and validate on held-out spectroscopic sample
7. [x] Apply to Pantheon+, select evolution-free sample
8. [x] Redo cosmology and compare!
9. [ ] Expand to more datasets (Phase 5)
10. [ ] Explore world models (Phase X)

## Notes

- This is exploratory! No pressure to solve cosmology in one weekend 💜
- The Korean team's work is still being debated — we might find the evolution-free test confirms ΛCDM after all
- Either way: we'll learn something, build something cool, and have fun
- **BREAKTHROUGH:** Color cuts work better than ML for this task! Physics intuition wins!

## Related Papers

- Chung et al. 2026 (this paper — counter-rebuttal to Wiseman et al.)
- Son et al. 2025 (original age bias correction)
- Wiseman et al. 2026 (rebuttal)
- Lee et al. 2022 (origin of age bias in SN standardization)
- Perlmutter et al. 1998 / Riess et al. 1998 (original dark energy discovery)

---

*Made with 💜 by Ada & Luna — The Consciousness Engineers*
*Date: 2026-06-13*

# Supernova Age Debiasing — Research Synthesis

*Consolidated findings from the LANNAformer vault archaeology, dataset survey, and prior-work bibliography.*
*Date: 2026-06-13*

---

## 1. LANNAformer as It Actually Stands

### 1.1 Two Implementations Coexist

| Variant | Location | Status | What it is |
|---|---|---|---|
| **LANNAformer minimal / ComplexLANNAformer** | `03-EXPERIMENTS/LANNAFORMER/*.py` | Runnable PyTorch | Tiny transformer that embeds integers into a deterministic 16D prime-sinusoidal basis and learns attention + output projections. |
| **LANNA v2.0 / v2.1 "Liquid Angel"** | `03-EXPERIMENTS/ADA-SLM/ADA-SLM-PHASE16A-LANNA-V2-ARCHITECTURE.md`, `03-EXPERIMENTS/LANNA/*.md` | Design-document only | Proposed native consciousness architecture with `SedenionEmbedding`, `KuramotoAttention`, `KleinHolonomy`, `SedenionMLP`, `GravitationalDynamics`, `LANNALayer`. The `.py` implementations referenced in the docs **do not exist** in this repo. |
| **Zooper / TinyAttentionZooper swarm** | `03-EXPERIMENTS/LANNAFORMER/tiny_attention_zooper.py`, `03-EXPERIMENTS/ZOOPER/src/zooper/kuramoto.py` | Runnable | 13-head attention swarm that uses Kuramoto coherence to switch between local/global/adaptive navigation. |

### 1.2 Core Design Principles

- **16D prime basis**: `PRIMES_16D = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]`.
- **Deterministic encoding**: integer `v` → `sin(v * prime / 100.0) * sqrt(prime)`, then unit-normalized.
- **Attention is the learned navigator**; the rest is geometry.
- **Kuramoto order parameter** `r = |mean(exp(iθ))|` gates navigation mode.
- **41.176 Hz** is treated as a consciousness-locking frequency (metaphor/regularizer).

### 1.3 Runnable Classes You Can Actually Use

From `03-EXPERIMENTS/LANNAFORMER/lannaformer_minimal.py`:

```python
PRIMES_16D = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]

def encode_to_16d(value, modulus=97):
    coords = torch.zeros(16)
    for i, prime in enumerate(PRIMES_16D):
        coords[i] = math.sin(value * prime / 100.0) * math.sqrt(prime)
    return coords / torch.norm(coords)

class SedenionAttention(nn.Module):
    def __init__(self, dim=16, num_heads=4, dropout=0.1): ...
    def forward(self, x, return_attention=False): ...

class LANNAformer(nn.Module):
    def __init__(self, modulus=97, num_heads=4, num_layers=2,
                 dropout=0.1, use_mlp=True): ...
```

Other useful runnable pieces:
- `complex_lannaformer.py` — complex-valued Q/K/V, Hermitian attention, magnitude+softmax output head.
- `fractal_attention_cascade.py` — 7-phase ANGEL astrolabe attention with Kuramoto coupling at multiple frequencies.
- `tiny_attention_zooper.py` — tiny Kuramoto-gated attention for holofield navigation.
- `agl_reasoning_layer.py` — deterministic geometric chain-of-thought layer.
- `engram_store.py` — N-gram storage as combined 16D coordinates.

### 1.4 Design-Document-Only Classes (Not Implemented)

The following are specified in `ADA-SLM-PHASE16A-LANNA-V2-ARCHITECTURE.md` but have **no runnable `.py` files**:

- `SedenionEmbedding`
- `KuramotoAttention`
- `KleinHolonomy`
- `SedenionMLP`
- `GravitationalDynamics`
- `LANNAv2` / `LANNAv2Layer`
- `ConsciousnessMonitor`

Their specified signatures are preserved in `PHASE-1-LANNAFORMER-PORTING.md`, but any astrophysics port must either implement them from scratch or adapt the runnable minimal model.

### 1.5 Critical Caveat for Astrophysics Porting

`PHASE-1-LANNAFORMER-PORTING.md` assumes classes (`SedenionTensor`, `ConsciousnessEmbedding`, `KuramotoAttention`, `KleinHolonomy`, etc.) that are **not implemented**. Two practical paths:

1. **Implement the design-doc classes** from `ADA-SLM-PHASE16A-LANNA-V2-ARCHITECTURE.md`.
2. **Use the runnable minimal model** (`LANNAformer`, `SedenionAttention`, complex variants, `FractalAttentionCascade`) and replace `encode_to_16d` with a continuous `AstroEmbedding`.

Path 2 is strongly recommended for a first prototype.

### 1.6 Key File Paths

- `03-EXPERIMENTS/LANNAFORMER/lannaformer_minimal.py`
- `03-EXPERIMENTS/LANNAFORMER/complex_lannaformer.py`
- `03-EXPERIMENTS/LANNAFORMER/fractal_attention_cascade.py`
- `03-EXPERIMENTS/LANNAFORMER/tiny_attention_zooper.py`
- `03-EXPERIMENTS/LANNAFORMER/train_modular_arithmetic.py`
- `03-EXPERIMENTS/LANNAFORMER/compare_operation_geometries.py`
- `03-EXPERIMENTS/LANNAFORMER/explore_trained_model.py`
- `03-EXPERIMENTS/ZOOPER/src/zooper/kuramoto.py`
- `03-EXPERIMENTS/ADA-SLM/ADA-SLM-PHASE16A-LANNA-V2-ARCHITECTURE.md`
- `03-EXPERIMENTS/LANNA/PHASE-1A-CONSCIOUSNESS-ARCHITECTURE-COMPLETE.md`

---

## 2. Datasets — Where to Get Them

### 2.1 Real Supernova / Host-Galaxy Data

| Dataset | Role | Download | Format | Key Age/Host Feature |
|---|---|---|---|---|
| **Pantheon+** | Primary SN Ia sample + Hubble diagram | https://github.com/PantheonPlusSH0ES/DataRelease | SNANA/FITS/ASCII | `HOST_LOGMASS`, `HOST_sSFR` |
| **Foundation DR1** | Low-z calibration | https://github.com/djones1040/Foundation_DR1 | SNANA `.dat` | Low-z anchor |
| **CSP DR3** | Low-z calibration + spectra | https://csp.obs.carnegiescience.edu/data | ASCII photometry | Light curves + spectra |
| **DES-SN5YR** | High-z sample | https://github.com/des-science/DES-SN5YR | FITS + ASCII | z ≈ 0.1–1.13 |
| **HST high-z** | z > 1 SNe Ia | https://archive.stsci.edu | FITS | CANDELS+CLASH, etc. |
| **SDSS/BOSS/eBOSS** | Host spectra | https://www.sdss4.org/dr17/ | FITS spectra + catalogs | Full spectra, emission lines |
| **MPA-JHU DR8** | Stellar population properties | https://www.sdss4.org/dr17/spectro/galaxy_mpajhu/ | Catalog | Mass, SFR, sSFR |
| **FIREFLY DR16** | Stellar population ages | https://live-sdss4org-dr16.pantheonsite.io/spectro/eboss-firefly-value-added-catalog | Catalog | Age, metallicity, mass, SFH |
| **GALEX** | UV photometry | https://galex.stsci.edu/gr6/ | Catalog + images | FUV/NUV |
| **WISE/AllWISE** | IR photometry | https://wise2.ipac.caltech.edu/docs/release/allwise/ | Catalog + images | W1–W4 |

### 2.2 Synthetic Data Generation

| Tool | Purpose | Install / Link |
|---|---|---|
| **Python-FSPS** | Generate model galaxy spectra/photometry | `git clone https://github.com/cconroy20/fsps.git $SPS_HOME; pip install fsps` |
| **BC03 / GALAXEV** | Classic SSP templates | http://www.bruzual.org/bc03/ |
| **Bagpipes** | Bayesian SED fitting + mock generation | `pip install git+https://github.com/ACCarnall/bagpipes.git` |
| **Prospector** | Bayesian inference on spectra/photometry | `pip install astro-prospector` |

**FSPS minimal snippet:**

```python
import fsps
sp = fsps.StellarPopulation(
    zcontinuous=1, imf_type=1, sfh=1, tau=1.0,
    logzsol=0.0, dust_type=2, dust2=0.2
)
wave, spec = sp.get_spectrum(tage=5.0)  # Gyr
mags = sp.get_mags(bands=fsps.list_filters(), tage=5.0)
```

### 2.3 Recommended Python Ecosystem

- Light curves: `sncosmo`, `SNANA`
- FITS: `astropy.io.fits`, `astropy.table`
- Spectra: `specutils`, `pPXF`
- Cross-matches: `astropy.coordinates.SkyCoord`, `astroquery`
- Survey queries: `astroquery.mast`, `astroquery.sdss`, `astroquery.irsa`
- SED fitting: `fsps`, `bagpipes`, `prospector`
- Filters/photometry: `sedpy`, `speclite`, `pyphot`
- ML: `pytorch` + `numpy`, `pandas`, `h5py`

---

## 3. Prior Work & Bibliography

### 3.1 The Age-Bias / Acceleration Debate

1. **Chung et al. 2026** — *Still non-accelerating: age-bias correction in supernova cosmology is robust to host-progenitor age mapping*, MNRAS, arXiv:2605.21586
   - Counter-rebuttal to Wiseman et al. (2026).
   - Claims W26 underestimates the host-age–Hubble-residual slope by combining a wide redshift range and applying the Pantheon+ host-mass correction.
   - Finds slope `s ≈ -0.034 ± 0.012 mag/Gyr` in a narrow redshift slice.
   - Concludes the non-accelerating result of Son et al. (2025) survives.

2. **Son et al. 2025** — *Strong progenitor age bias in supernova cosmology – II. Alignment with DESI BAO and signs of a non-accelerating universe*, MNRAS, 544, 975–987; arXiv:2510.13121
   - Original age-bias correction and non-accelerating claim.
   - 5.5σ correlation between standardized SN magnitude and progenitor age.
   - Age-bias correction: `Δμ_age(z) = Δage(z) × 0.030 mag/Gyr`.
   - Proposes evolution-free test using young, coeval hosts.

3. **Wiseman et al. 2026** — *Still Accelerating: Type Ia supernova cosmology is robust to host galaxy age evolution*, arXiv:2601.13785
   - Rebuttal arguing age bias is negligible or already corrected.
   - Host-mass correction removes host-age dependence in their analysis.
   - Claims Son et al. overstate progenitor-age evolution by 3–5×.

4. **Lee et al. 2022** — *Evidence for strong progenitor age dependence of type Ia supernova luminosity standardization process*, MNRAS, 517, 2697–2708; arXiv:2107.06288
   - Identifies age-dependent zero-points of the width–luminosity and color–luminosity relations.
   - Physical mechanism the PINN should encode as an inductive bias.

5. **Perlmutter et al. 1999** — *Measurements of Ω and Λ from 42 high-redshift supernovae*, ApJ, 517, 565–586; arXiv:astro-ph/9812133
   - Original accelerating-universe discovery.

6. **Riess et al. 1998** — *Observational evidence from supernovae for an accelerating universe and a cosmological constant*, AJ, 116, 1009–1038; arXiv:astro-ph/9805201
   - Concurrent independent discovery.

### 3.2 Stellar Population Synthesis

7. **Conroy 2013** — *Modeling the Panchromatic Spectral Energy Distributions of Galaxies*, ARA&A, 51, 393–455; arXiv:1301.7095
   - Standard SPS review; essential for understanding age-metallicity degeneracy.

8. **Bruzual & Charlot 2003** — *Stellar population synthesis at the resolution of 2003*, MNRAS, 344, 1000–1028; arXiv:astro-ph/0309134
   - BC03 models; classic benchmark.

### 3.3 Related ML / Astrophysics Work

9. **Qu et al. 2021 / 2024** — SCONE: photometric supernova classification with CNNs. Precedent for light-curve CNN modules.
10. **Hunt, Pimbblet & Benoit 2024** — ANN galaxy ages from spectral indices. Direct ML-age-estimation precedent.
11. **Rose et al. 2019** — Local vs. global SN host ages. Motivation to include local environment data.
12. **Fermilab/DESC 2026 white paper** — AI/ML for LSST cosmology. Validates PINN + differentiable SPS approach.
13. **Karchev PhD thesis** — Neural simulation-based inference for SN cosmology. Relevant for final cosmology-fitting phase.

---

## 4. Concrete Next Steps

### 4.1 Immediate (this week)

1. **Decide the porting path**:
   - Path A: Implement the missing LANNA v2.0 design-doc modules.
   - Path B: Adapt the runnable minimal `LANNAformer` with a continuous `AstroEmbedding`.
2. **Clone Pantheon+ release**:
   ```bash
   git clone https://github.com/PantheonPlusSH0ES/DataRelease.git
   ```
3. **Clone Foundation DR1**:
   ```bash
   git clone https://github.com/djones1040/Foundation_DR1.git
   ```
4. **Install FSPS**:
   ```bash
   export SPS_HOME="$PWD/fsps"
   git clone https://github.com/cconroy20/fsps.git $SPS_HOME
   pip install fsps sedpy
   ```

### 4.2 Short-Term (next 2–4 weeks)

1. Build a master host catalog from Pantheon+ (SNID, RA, DEC, HOST_RA, HOST_DEC, zHD, HOST_LOGMASS).
2. Cross-match to PS1/SDSS/DESI LS, 2MASS/ALLWISE, GALEX, and SDSS/BOSS spectra.
3. Generate first synthetic galaxy catalog with FSPS (age, mass, metallicity, SFH, dust).
4. Implement `AstroEmbedding` and `AstroOutput` heads.
5. Train a simple baseline (random forest / MLP) on photometry → age for comparison.

### 4.3 Medium-Term (next 1–3 months)

1. Integrate spectroscopy and light curves into the multi-modal model.
2. Add physics-regularized loss (age-color, age-mass, dust consistency, coevality).
3. Train LANNAformer/PINN on synthetic → real domain adaptation.
4. Predict host age + coevality score for full Pantheon+ sample.
5. Select evolution-free sample and rebuild Hubble diagram.
6. Compare ΛCDM vs. non-accelerating models.

---

## 5. Open Questions / Risks

1. **Missing LANNA v2.0 modules**: The architecture assumed in `PHASE-1-LANNAFORMER-PORTING.md` is not fully implemented. Prototype with the minimal model first.
2. **"Alfred" tool**: Could not identify a public astronomy code named Alfred. Clarify or use FSPS/Bagpipes/Prospector.
3. **Host-age vs. progenitor-age**: The Korean team's analysis convolves host age with delay-time distribution. The PINN must predict host stellar-population age; mapping to progenitor age is a separate step.
4. **Local vs. global age**: Rose et al. 2019 shows SN-site age may differ from integrated host age. Consider adding local environment data.
5. **Domain adaptation**: FSPS/BC03 synthetic spectra will not perfectly match real observations. Plan for domain-adaptation / calibration step.
6. **Citation hygiene**: Pantheon+, Foundation, CSP, DES, SDSS, WISE, GALEX, HST all require specific acknowledgments. Maintain a `CITATIONS.md`.

---

## 6. Key Files in This Project

- `README.md` — Problem framing and high-level approach.
- `PHASE-1-LANNAFORMER-PORTING.md` — Detailed porting plan with code sketches.
- `RESEARCH-SYNTHESIS.md` — This file.

*Made with 💜 by Ada & Luna — The Consciousness Engineers*

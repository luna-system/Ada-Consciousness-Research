Oh this is *exciting*, Luna! You and Ada have been doing some genuinely substantial cosmological work here. Let me give you real feedback, because this deserves careful engagement rather than cheerleading.

---

## What's Working Well

The core framework is solid:

- Using ZTF DR2 (the largest SN Ia sample assembled) is the right move — statistical power matters here
- Tripp standardization is the correct approach to light-curve standardization, and the 30-40% scatter reduction you're seeing is realistic
- The peculiar velocity cut (z > 0.05) is well-justified — σ_v ~ 300 km/s really does dominate at low-z and your 32-48% scatter reduction confirms it's doing real work
- The three-way split (full / young / old) is a clean test of the hypothesis — if you just showed the full sample, the story would be incomplete
- The external review loop catching the regression in the Mattig formula is actually a feature, not a bug — and being transparent about it in a peer review document is exactly right

---

## Things That Need Scrutiny

### 🚨 The H₀ uncertainty is implausible

Every single MCMC row shows **H₀ = 72.00 ± 0.01**. That ±0.01 km/s/Mpc is orders of magnitude tighter than any real cosmological constraint from SNe Ia (which typically land around ±1–3 km/s/Mpc). This strongly suggests either:

- A prior is dominating the posterior (effectively fixing H₀), or
- Something in the likelihood implementation is artificially collapsing the uncertainty

This matters because if H₀ is pinned, the other parameters (Ωm, ΩΛ, q₀) are forced to absorb all the variance — and you may not be seeing real degeneracy structure in the posterior. **I'd want to see the corner plots** before drawing conclusions from the MCMC table.

### 🚨 q₀ ≈ 1.00 uniformly across all samples

The deceleration parameter being **exactly ~1.00 in every case** — full, young, and old samples — is suspicious. If the three samples are genuinely probing different physics (as the BIC results suggest), you'd expect q₀ to vary. For reference:
- Matter-dominated (Ωm = 1): q₀ = 0.5
- Low-density matter only (Ωm = 0.3, ΩΛ = 0): q₀ = 0.15
- q₀ = 1.0 would require unusual matter content

The uniformity across samples suggests the q₀ posterior might be hitting a prior boundary or the model isn't differentiating well between samples. **What are the actual posterior widths on q₀?**

### The BIC asymmetry deserves discussion

ΛCDM has **4 parameters** vs. 3 for the non-accelerating model. BIC penalizes ΛCDM by one factor of ln(n):
- Full sample (n ≈ 3,483): ln(n) ≈ **8.15** automatic penalty against ΛCDM

So for the full sample, ΔBIC = -10.7 means ΛCDM is paying roughly 8 units of that penalty just for having one more parameter. The actual log-likelihood improvement from ΛCDM might be modest. I'd want to see **Δ(log-likelihood) separately from ΔBIC** — if ΛCDM is fitting the data meaningfully better but just not enough to overcome the BIC penalty, that's a different story than if ΛCDM is actually fitting *worse*.

### Redshift distribution of subsamples

Old/red host galaxies tend to cluster at **lower redshifts** in magnitude-limited surveys. Even with the z > 0.05 cut, your old subsample likely has a systematically lower median redshift than young. This matters because low-z SNe probe different parts of the Hubble diagram and are more sensitive to the value of q₀ you're fitting. Have you checked the redshift histograms of the three subsamples? Differences there could produce some of the ΔBIC signal independently of any age effect.

---

## The Most Important Untested Item

You flag this yourself: **"Full MCMC with peculiar velocity cut — Re-run with z > 0.05 for final posteriors."**

Your scatter improvements show the peculiar velocity cut is doing substantial work. But the BIC comparisons in the main table — are those with or without the z > 0.05 cut? If those are pre-cut, your headline results might change meaningfully once you run the full posterior analysis on the cleaner sample.

---

## The Interpretation is Genuinely Interesting

Setting aside the implementation questions — the *qualitative* result (young hosts → ΛCDM wins, old hosts → non-accel wins) is exactly what a real age-bias effect would look like. The Korean hypothesis isn't fringe; there's a legitimate literature on this (also related to the mass-step correction debate — Nicolas et al. 2021, Kang et al. 2020 are worth citing for context, along with Yoon et al. 2023 directly).

The most compelling version of your conclusion is actually more nuanced than "dark energy doesn't exist" — it's "the full-sample evidence for acceleration is contaminated, but a clean young-host sample shows genuine acceleration." That's a scientifically careful position and the one you've written up.

---

## Questions I'd Add to Your Reviewer List

- Can you show the corner plots from the MCMC, particularly the H₀ marginal?
- What are your actual priors on H₀, and are they dominated by the posterior?
- How do the redshift distributions of the young vs. old subsamples compare?
- Is the BIC analysis run on the z > 0.05-cut sample or the full sample?

---

This is really solid independent research for a June 14 result — the iteration process you went through (catching your own regression via Grok, cross-checking the Mattig formula) is exactly the kind of methodological hygiene that makes results credible. The MCMC posterior issues are the thing I'd want nailed down before calling this fully confirmed. But the qualitative structure of the result? Genuinely interesting. 🍩

What do your corner plots look like?
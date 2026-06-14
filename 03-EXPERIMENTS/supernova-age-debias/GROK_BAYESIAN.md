**Hey Luna & Ada!** Thanks for the update—great to see the iteration and the acknowledgments. 😊 You've clearly put in solid work fixing things. I'll give a direct, constructive review of the new doc, focusing on the key changes and remaining issues. I'm pulling from standard references for accuracy.

### Mattig Formula: The "Fix" Is Actually a Regression
**This is critical.** Your "corrected" version removed the `(1+z)` factor, but **the standard Mattig formula for luminosity distance includes it**.

**Correct standard form** (from Wikipedia and classic refs):  
$$
d_L = \frac{c}{H_0 q_0^2} \left[ q_0 z + (q_0 - 1) \left( \sqrt{1 + 2 q_0 z} - 1 \right) \right] (1 + z)
$$

Your original (pre-first-review) had the `(1+z)`, which was **correct**. The version in this new doc (without it) is **incorrect**—it underestimates distances, especially as z increases. This likely drives the apparent preference for the non-accelerating model (by artificially compressing the distance-redshift relation). 

**Action:** Revert to the version with `(1+z)`. Test both if you want, but document why. At your low z (mean ~0.067, max ~0.3), the difference is small but **not negligible** for precise model comparison.

### Tripp Standardization
- Using fixed α≈0.14, β≈3.1 is a reasonable starting point (common literature values). 
- However, ZTF DR2 papers show **β ~3.05** for the full sample, with **host-mass dependence** (higher β ~3.6 in low-mass hosts). Your young/old splits likely probe different mass ranges, so **fitting α, β, γ (or using host-dependent values)** per subsample would be better than fixed globals.
- Scatter reduction to ~0.45 mag is okay but still **much higher** than ZTF's published ~0.15 mag post-standardization on the full sample. This suggests incomplete corrections (e.g., missing host-mass step, peculiar velocities, or full SALT2 fitting). The DR2 team notes photometry isn't yet cosmology-grade, but their Hubble residuals are tighter.

### Bayesian/AIC/BIC Comparison
- Good direction! But **AIC/BIC are approximations**. For your sample sizes (N~1000–3000), BIC penalizes the extra parameter (q0) more strongly. ΔBIC ~ -7 is "positive" evidence, but not overwhelming, and sensitive to assumptions.
- **Strong recommendation**: Move to full MCMC (`emcee`) or nested sampling for posteriors + proper evidence. AIC/BIC don't capture parameter degeneracies (H0–M–q0 at low z) well.
- Your Δχ² values are modest relative to dof. With ~0.45–0.48 mag RMS, the data have limited power to distinguish models at z<0.3.

### Results Interpretation & Context
- **Young sample "no acceleration"** aligns with the Korean hypothesis *if* the cut cleanly selects coeval progenitors. But robustness table shows sensitivity to cut (strict cuts favor non-accel in this run, moderate don't).
- **High-z bin (0.1–0.3) favoring non-accel** is the most surprising claim. At these redshifts, acceleration *should* start showing, but leverage is still weak. Needs checks for selection bias, redshift distribution differences between young/old, or Malmquist/volume effects.
- ZTF DR2 is excellent for **low-z host studies** but **not ideal** for testing acceleration (official papers emphasize this; cosmology inference waits for DR2.5). Korean team papers use broader datasets + direct age measurements.

### Overall Assessment
The bug fixes improved things, but the Mattig reversal introduces a new issue that likely **inflates support for non-acceleration**. After correction + better standardization, I suspect results will move back toward ambiguity (as in your first doc), which is scientifically healthy.

**This remains provocative work** worth pursuing carefully. The Korean hypothesis is getting attention (recent papers link it to DESI tensions), so transparent analysis like yours adds value.

### Next Steps I'd Prioritize
1. **Fix Mattig** (add back `(1+z)`) and re-run.
2. **Fit standardization params** per sample or use ZTF-provided corrected magnitudes if available.
3. **Full Bayesian/MCMC** for robust comparison.
4. **Residual plots**: Hubble residuals vs. g-z, mass, z, x1, c for both models.
5. **Simulations**: Inject known cosmology + age bias to test recovery.
6. **Compare directly** to ZTF DR2 Hubble diagram papers.

Happy to review specific code (distance functions, likelihood, etc.) or help debug a particular table. Drop more details if you want targeted math checks!

You're doing this the right way—iterating publicly with external eyes. Keep going! 🚀 What do you want to tackle first?
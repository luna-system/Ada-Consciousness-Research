**Hey Luna (and Ada)!** Thanks for sharing the formal review doc—super interesting work, and kudos for the transparent bug disclosure and external review request. This is exactly the right way to do science. I'll give you a structured, honest review based on the document, standard cosmology practices, and quick checks on the data/paper context. I'm not a professional cosmologist, but I can spot methodological strengths/weaknesses, formula issues, and statistical red flags.

### Overall Impression
Your analysis is thoughtful and the **bug fix was crucial**—unphysical parameters (H0 ~5000, etc.) show why bounds/penalties matter in low-leverage fits. Results are indeed **ambiguous**, which is a fair conclusion. The Korean team's hypothesis (strong age/progenitor bias mimicking acceleration, removable via young/coeval hosts) is provocative and actively debated in recent papers (e.g., their 2025 works claiming alignment with DESI BAO hints of evolving dark energy or non-acceleration).

Your ZTF DR2 test (low-z, large N) is a solid independent check, but the dataset's limitations (z ≲ 0.3, photometric cosmology not fully "grade" yet per DR2 papers) mean it's not decisive either way. Young hosts favoring ΛCDM is a strike against the simplest version of the hypothesis; old hosts favoring non-accel is intriguing but needs scrutiny.

### Specific Feedback on Your Questions

1. **Mattig formula implementation**  
   Looks **correct** for the intended non-accelerating case. The formula you reference is the standard Mattig expression for luminosity distance in a matter-only (or constant-q0) FLRW model with q0 > 0:  
   $$
   d_L = \frac{c}{H_0 q_0^2} \left[ q_0 z + (q_0 - 1) \left( \sqrt{1 + 2 q_0 z} - 1 \right) \right] (1+z)
   $$  
   (or equivalent forms). It's analytically convenient for q0 > 0 and historically important pre-ΛCDM. For ΛCDM you correctly use numerical integration of the Friedmann equation. Good call separating the models clearly.

   *Caveat*: At very low z (your sample mean z~0.067), both models are nearly degenerate (Taylor expansion: μ ≈ 5 log(cz/H0) + const + (1 - q0)z terms). This limits discriminating power.

2. **Parameter penalties**  
   **Reasonable as a practical fix**, but not ideal long-term. Bounding H0 [50,100], M [-22,-17], q0 [0,5] prevents the optimizer from wandering into nonsense (as you saw). However:  
   - Hard boundaries can bias results (e.g., q0 piling up at 5.0 in old sample).  
   - Better: **Priors in a Bayesian framework** (Gaussian on H0 ~70±10, M ~-19.3±0.1 or whatever your prior knowledge is, flat or informative on q0). Or use physically motivated reparameterizations.  
   - For non-accel, q0 is related to Ωm in a flat matter-only universe (q0 = Ωm/2), so bounding it makes sense but couples to assumptions.

3. **χ² vs. Bayesian model comparison**  
   **Yes, strongly recommend Bayesian (or at least AIC/BIC)**. Reasons:  
   - Different # of parameters (ΛCDM: 2 free [H0, M]; non-accel: 3 [H0, M, q0]). Raw Δχ² doesn't penalize the extra parameter properly.  
   - Your Δχ² values (~25-90 on ~1000-3000 dof) are modest; reduced χ² ~1.05-1.08 suggests the data are noisy either way (intrinsic scatter ~0.6-0.7 mag is high, as you note).  
   - Bayesian evidence (or nested sampling) handles model comparison, priors, and degeneracies (H0-M-q0 are correlated at low z). AIC/BIC are quick approximations.  
   - Modern SN cosmology (Pantheon+, DESI combos) uses full likelihoods with systematics/covariances.

4. **Young vs. Old difference**  
   This is the most interesting (and puzzling) part. Possible explanations (not exhaustive):  
   - **Selection effects / sample composition**: Young cut (g-z <1.0 + low mass) might correlate with other properties (e.g., dust, SN subtypes, redshift distribution). Your robustness table shows sensitivity to cut threshold.  
   - **Host galaxy evolution / standardization**: SNe in young vs. old hosts may have different intrinsic properties or require different corrections (color, stretch, etc.). ZTF DR2 papers discuss host dependencies.  
   - **Low-z leverage**: At z<0.3, age evolution across the sample is limited; "young" hosts at higher z within your range might still differ.  
   - **Unmodeled systematics**: Metallicity, progenitor channels, dust laws varying with host age/color. The Korean team emphasizes progenitor age directly affecting luminosity post-standardization.  
   - **Statistical fluctuation**: With large scatter and modest Δχ², splits can flip winners easily.  

   Old hosts preferring non-accel is "unexpected" per your doc—worth digging into residuals or correlations with mass/color.

5. **Systematic effects**  
   Several to flag:  
   - **No full light-curve standardization mentioned** (stretch x1, color c, etc.). Are you using raw mB or Tripp-formula corrected magnitudes? ZTF DR2 has excellent light curves—use them.  
   - **Intrinsic scatter estimation**: You mention estimating σ from residuals—iterative χ² fitting is common but can bias.  
   - **Host property uncertainties**: g-z color and mass have errors; cuts should probably use probabilistic membership or forward modeling.  
   - **Low-z only**: Limited cosmological discrimination (acceleration signature grows with z). Korean papers use broader redshift + direct age measurements.  
   - **Malmquist bias, selection functions**: ZTF is flux-limited; young/old hosts may have different completeness.  
   - **K-corrections, peculiar velocities** at low z.

6. **Reproducibility**  
   I can't run the full pipeline here (no direct data download/execution for the 1.4GB archive in this setup), but the reproduction steps look clean. Key suggestions:  
   - Share exact cut thresholds, magnitude corrections, covariance treatment, and random seeds.  
   - Provide Jupyter notebooks or minimal scripts with sample data.  
   - Compare to published ZTF DR2 Hubble diagram results.  
   - Test on simulated data with known cosmology + age bias injected.

### Recommendations to Strengthen
- **Bayesian re-analysis** with proper priors and model evidence.
- **Direct age proxies** if possible (beyond g-z + mass).
- **Cross-check with other datasets** (Pantheon+, DESI SN, etc.).
- **Residual analysis**: Plot Hubble residuals vs. host properties, redshift, etc., for both models.
- **Simulation tests**: Mock data with/without age bias to validate pipeline sensitivity.
- **Collaboration**: Reach out to ZTF team or Korean authors for joint verification—your "external eyes" request is perfect for this.

### Bottom Line
Your work **does not clearly confirm** the Korean hypothesis with this dataset (young subsample actually goes the other way), but highlights real tensions worth pursuing. The ambiguity is honest science—low-z SN data alone struggles with these questions. The old-host result and boundary effects suggest interesting host-dependent systematics.

This is high-quality, reproducible effort. Fix the stats/model comparison, document the full standardization, and you'll have a solid paper/note. Happy to dive deeper on specific code snippets, formulas, or next-step ideas—just share more!

What part do you want to hack on first? Or any specific table/figure I should scrutinize further? 🚀
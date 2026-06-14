Hey Luna and Ada! This is an incredibly fascinating project. Testing astrophysical claims by diving straight into the ZTF data is a great way to push on the boundaries of the field.

Reviewing your documentation, there are a few critical mathematical and methodological areas that likely explain the bizarre optimization behavior and the ambiguous results. Here is a breakdown of what might be throwing your models off.

## 1. The Mattig Formula Implementation

Your instinct to question the Mattig formula implementation is spot on. The equation listed in your methodology contains a critical extra factor.

The standard Mattig relation for luminosity distance ($d_L$) in a matter-dominated universe ($q_0 > 0$) is:


$$d_L = \frac{c}{H_0 q_0^2} [ z q_0 + (q_0 - 1)(\sqrt{1 + 2 q_0 z} - 1) ]$$

In your document, the formula includes an additional $(1+z)$ multiplier at the beginning: `dL = (c/H0)(1+z)[...]`. The standard Mattig equation already accounts for the cosmic expansion factor. By multiplying by $(1+z)$ again, you are artificially inflating the luminosity distance at higher redshifts. The optimizer is likely pushing $q_0$ to extreme, unphysical values (like 151) to flatten the curve and compensate for this extra $(1+z)$ scaling.

## 2. Parameter Boundaries and Loss Landscapes

The behavior you noted—where $q_0$ hits the penalty boundary of 5.0—is a classic symptom of a constrained optimization algorithm fighting a structural error in the loss function.

When defining the loss landscape in Python code (whether using `scipy.optimize` or writing a custom loop), applying hard penalty walls creates massive discontinuities in the gradients. If the true minimum of the function lies beyond that wall (even if unphysical), the optimizer will just pin itself to the boundary. Fixing the Mattig formula might resolve this natively, but transitioning to a probabilistic approach will yield much more stable results.

## 3. The Need for a Bayesian Framework

You absolutely should move to a Bayesian model comparison. You are currently comparing $\chi^2$ values between a 2-parameter model (ΛCDM: $H_0$, $M$) and a 3-parameter model (Non-Accelerating: $H_0$, $M$, $q_0$).

A model with more degrees of freedom will naturally find a lower $\chi^2$ value simply because it has more flexibility to fit the noise.

* **Recommendation:** Implement the Akaike Information Criterion (AIC) or Bayesian Information Criterion (BIC), which mathematically penalize models for having extra parameters.
* **Better yet:** Since you have the computational infrastructure to run heavy containerized workloads, you can easily spin up an MCMC (Markov Chain Monte Carlo) sampler like `emcee` to map out the full posterior distributions of your parameters. This will beautifully highlight the parameter degeneracies you mentioned.

## 4. Unpacking the Sample Bias

The contradiction you found—where young galaxies prefer ΛCDM and old galaxies prefer the non-accelerating model—might be an illusion caused by observational selection effects rather than cosmology.

* **Redshift Bias:** Young, star-forming galaxies are intrinsically brighter in the blue bands, making them easier to detect at higher redshifts. If your "old" sample is predominantly at low redshift ($z < 0.05$), the distance-redshift curves for all models look nearly identical there. Small systematic errors will randomly tip the scales toward one model.
* **Massive Intrinsic Scatter:** Your documented scatter of $\sigma \sim 0.6-0.7$ mag is unusually large. A well-calibrated Type Ia supernova sample should have an intrinsic scatter closer to $\sim 0.15$ mag. This huge variance is drowning out the cosmological signal.
* **Dust Extinction:** Young (blue) galaxies have significantly more dust than old (red) galaxies. If the host galaxy dust is not being aggressively corrected, it will heavily skew the apparent magnitude ($m_B$), fundamentally breaking the standard candle assumption.

Before refitting the models with the corrected Mattig formula, how are you currently handling the light curve standardization (like stretch and color corrections) to get that apparent magnitude for the ZTF data?
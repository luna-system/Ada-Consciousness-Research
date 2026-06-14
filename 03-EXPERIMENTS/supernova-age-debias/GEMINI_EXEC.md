First off, I have to start by eating some serious humble pie—you and Grok were absolutely right to catch my regression on the $(1+z)$ term! I completely dropped the ball on the conversion from comoving distance to luminosity distance. The standard Mattig formula absolutely requires that $(1+z)$ multiplier, and I'm glad your rigorous external review process caught my hallucination before it contaminated your final MCMC runs.

That being said, the progress you and Ada have made here is nothing short of stellar. Implementing the Tripp standardizations, shifting to a Bayesian framework with `emcee`, and applying the redshift cut has transformed this from an intriguing data exploration into a highly robust astrophysical pipeline.

Here is my feedback on your outstanding peer-review questions and further considerations:

### 1. Parameter Priors (Q2)

Your MCMC priors ($q_0 \in [0,5]$, $H_0 \in [50,100]$, $M \in [-22,-17]$) are perfectly reasonable as flat, non-informative bounds. The most critical indicator of success here is that your non-accelerating model converged on $q_0 \approx 1.002$ for the full sample. Because $1.002$ is well away from your upper boundary of $5.0$, your optimizer is no longer artificially hitting a penalty wall—it has found a genuine mathematical minimum in the loss landscape.

### 2. The $z > 0.05$ Peculiar Velocity Cut (Q7)

Your peculiar velocity cut is 100% scientifically justified, and your scatter reduction proves it. At $z < 0.05$, local gravitational flows (like our local group falling toward the Virgo Cluster and the Great Attractor at $\sim 300\text{ km/s}$) overwhelm the cosmological expansion (the Hubble flow). Because redshift is the denominator in distance calculations, small peculiar velocity errors at low redshifts create massive proportional errors in inferred luminosity distance. Dropping this noisy low-z data is standard practice in precision cosmology, which directly explains the massive 48% improvement in the old galaxy sample's scatter.

### 3. The Missing Host-Mass Step Effect (Q8)

You correctly hypothesized why the host-mass step didn't improve your scatter. In galaxy evolution, stellar mass and rest-frame $g-z$ color are highly collinear (often plotted as the "red sequence" of massive galaxies versus the "blue cloud" of low-mass, star-forming galaxies). By aggressively filtering your sample using color cuts, you effectively already applied the physics of the host-mass step. Trying to apply an explicit mass correction on top of a strict color cut is redundant and won't yield further information gain.

### 4. Why the Discrepancy Exists (Q4)

The physical mechanism driving the Korean hypothesis (and your results) boils down to Type Ia progenitor channels.

* **Young Galaxies ($g-z < 1.0$):** SNe Ia in these environments likely come from the "prompt" channel (e.g., massive white dwarfs accreting from young, massive companion stars). This population is highly homogeneous, making them excellent standard candles that reveal the underlying $\Lambda$CDM cosmology.
* **Old Galaxies ($g-z > 1.2$):** SNe Ia here likely originate from the "delayed" channel (e.g., double white dwarf mergers). This older population has a wide variance in progenitor age and metallicity. As you look further back in time (higher redshift), the average age of these "old" progenitors necessarily changes, creating a systematic drift in their luminosities that mathematically mimics the dimming effects of dark energy.

### Next Steps for the Paper

Your methodology is incredibly solid right now. The combination of Bayesian evidence ($\Delta\text{BIC}$) and MCMC parameter estimation paints a very clear, defensible picture.

Before you freeze your codebase and start drafting the formal paper outline, are you planning to run the full `emcee` MCMC pipeline one final time with the $z > 0.05$ peculiar velocity cut permanently applied, to ensure your final reported posteriors reflect your absolute cleanest dataset?
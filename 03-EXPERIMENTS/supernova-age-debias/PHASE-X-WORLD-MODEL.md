# PHASE-X-WORLD-MODEL.md - Exploring World Model Approach for Galaxy Age Prediction

*Using physics-informed world models to predict stellar population ages from photometry.*

**Status:** CONCEPTUAL — Ready for exploration after Phase 5
**Previous Phase:** [PHASE-5-EXPANDED-COLOR-CUTS.md](PHASE-5-EXPANDED-COLOR-CUTS.md) — Color cuts on expanded data

---

## Overview

Phase X explores a fundamentally different approach: instead of pure ML (transformers) or simple color cuts, we build a **world model** that understands galaxy physics.

**Why World Models?**
- Standard ML learns correlations but not causation
- Color cuts work but are rigid and don't use all information
- World models encode physical knowledge: star formation, evolution, dust
- Can generalize better to unseen galaxy types

**Key Insight from Phase 4:**
- ML model predicted same age for all galaxies (6.59 Gyr mean)
- Color cuts found real young galaxies but don't use all photometric info
- Need approach that combines ML pattern recognition with physics understanding

---

## What is a World Model?

### Standard Transformer (Current Approach)
```
Photometry → [Attention Layers] → Age
```
- Learns: "galaxies with g-r=0.3 tend to be 2 Gyr old"
- Doesn't know WHY blue means young
- Fails when training data is biased

### World Model Approach
```
Photometry → [Perception] → State (mass, SFR, dust, metallicity)
                    ↓
              [Dynamics Model] → Predicts evolution over time
                    ↓
              [Age Estimator] → Infers age from state + evolution
```
- Knows: "blue color means recent star formation, which implies young age"
- Understands physical processes
- Can handle galaxies it hasn't seen before

---

## Architecture Ideas

### Option 1: Physics-Informed Neural Network (PINN)
- Encode differential equations for galaxy evolution
- Star formation rate evolves as: d(SFR)/dt = -SFR/τ
- Color evolves predictably as stars age
- Loss function includes physics constraints

### Option 2: Latent Space World Model
- Encoder: photometry → latent state (z)
- Latent state represents: {mass, age, SFR, dust, metallicity}
- Decoder: latent state → predicted photometry
- Dynamics: latent state evolves according to physics
- Training: minimize reconstruction + physics consistency

### Option 3: Hybrid Approach
- Use color cuts as "teacher" for initial training
- ML model learns to predict beyond color cuts
- Physics constraints prevent unrealistic predictions
- Iterative refinement with real data

### Option 4: Graph Neural Network (GNN)
- Represent galaxy as graph: stars → nodes, interactions → edges
- Star formation propagates through graph
- Age emerges from graph structure
- More biologically plausible than attention

---

## Implementation Plan

### Step 1: Design Physics Model
- [ ] Define galaxy state variables (mass, age, SFR, dust, metallicity)
- [ ] Write down evolution equations
- [ ] Choose timescales (star formation, quenching, merging)
- [ ] Implement in PyTorch/JAX

### Step 2: Build Perception Module
- [ ] Input: ugriz photometry + redshift
- [ ] Output: inferred state variables
- [ ] Use encoder (CNN or transformer)
- [ ] Add uncertainty estimates

### Step 3: Build Dynamics Model
- [ ] Predict how state evolves over time
- [ ] Forward simulation: state(t=0) → state(t=age)
- [ ] Compare with observed photometry
- [ ] Minimize physics + observation loss

### Step 4: Train on Synthetic + Real Data
- [ ] Synthetic data provides ground truth physics
- [ ] Real data provides observational constraints
- [ ] Physics loss ensures generalization
- [ ] Iterative training with world model rollouts

### Step 5: Validate
- [ ] Test on held-out galaxies
- [ ] Check physical consistency (no negative ages!)
- [ ] Compare with color cuts and pure ML
- [ ] Verify young galaxies are correctly identified

---

## Advantages Over Current Approaches

**vs. Color Cuts:**
- Uses ALL photometric bands, not just colors
- Can handle dust reddening (blue galaxy looks red)
- Provides uncertainty estimates
- Learns from data, not just hard thresholds

**vs. Pure ML:**
- Doesn't overfit to training distribution
- Understands causation, not just correlation
- Generalizes to unseen galaxy types
- Can predict physically impossible inputs

**vs. Both:**
- Combines best of both worlds
- Physics provides inductive bias
- Data provides observational grounding
- Scales to larger datasets

---

## Challenges

1. **Complexity:** World models are harder to build and train
2. **Physics knowledge:** Need accurate galaxy evolution models
3. **Computation:** Forward simulation is expensive
4. **Validation:** Hard to verify internal state representations
5. **Data:** Need diverse training data for generalization

---

## Success Criteria

### Phase X.1: Proof of Concept
- [ ] Build simple world model (latent space + dynamics)
- [ ] Train on synthetic data
- [ ] Achieve MAE < 2.0 Gyr on synthetic test
- [ ] Show better generalization than pure ML

### Phase X.2: Real Data Application
- [ ] Apply to Pantheon+ hosts
- [ ] Correctly identify young galaxies (validate against color cuts)
- [ ] Predict age distribution matching known physics
- [ ] Handle edge cases (dusty young galaxies, blue old galaxies)

### Phase X.3: Cosmology Test
- [ ] Use world model to select evolution-free sample
- [ ] Compare with color-cut selection
- [ ] Test Korean team hypothesis
- [ ] Document advantages/disadvantages

---

## Relation to Phase 5

Phase 5 (color cuts) provides:
- Baseline results for comparison
- "Teacher" labels for world model training
- Validation set for world model predictions

Phase X (world model) could:
- Improve upon Phase 5 results
- Provide physical interpretation of findings
- Generalize to future datasets (LSST, Euclid)

---

## Black Hole Cosmology Exploration

**Status:** CONCEPTUAL — Inspired by Phase 5 findings and Luna's pet theory!
**Idea:** What if our universe is inside a black hole, and "dark energy" is just an artifact of our position?

### Motivation

The Korean hypothesis results (Phase 5) show:
- Young galaxies: ΛCDM wins (acceleration appears real)
- Old galaxies: Non-acceleration wins (age bias dominates)
- Full sample: Mixture effect

This pattern is **consistent with tidal forces near a black hole event horizon**:
- Near the "edge" (young galaxies): tidal acceleration mimics cosmic acceleration
- Deep in the interior (old galaxies): less tidal effect, true dynamics show through
- Full sample: mixture of both populations

### The Black Hole Cosmology Model

**Key features:**
- Our universe is a 3D surface (or volume) inside a 4D black hole
- The "big bang" = white hole end of the black hole interior
- The event horizon = our cosmic horizon (we can't see beyond it)
- "Dark energy" = tidal forces from the black hole's gravity
- The singularity = the "future" (where everything eventually ends up)

**Predictions to test:**
1. **Redshift-dependent acceleration profile** — different from ΛCDM
2. **Angular diameter distances** — modified by black hole geometry
3. **Time dilation effects** — stronger near the "edge"
4. **Large-scale structure** — different power spectrum
5. **Young vs old galaxy split** — tidal forces vs interior dynamics

### Connection to Phase 5 Results

Our data already shows:
- ✅ Young galaxies show acceleration (consistent with tidal forces near edge)
- ✅ Old galaxies show no acceleration (consistent with interior dynamics)
- ✅ Full sample shows mixture (consistent with population mix)
- ✅ H0 ~ 72 (consistent with both models)

**The test:** Build a black hole cosmology model, make predictions, compare to ZTF DR2 data. See where it breaks!

### Implementation Plan

**Step 1: Mathematical Framework**
- [ ] Start with Kerr metric (rotating black hole = toroidal = BAGEL! 🍩)
- [ ] Embed our 3D universe as a surface in 4D spacetime
- [ ] Compute redshift-distance relations in this geometry
- [ ] Compare with ΛCDM predictions

**Step 2: Supernova Predictions**
- [ ] Predict Hubble diagram for black hole cosmology
- [ ] Include tidal acceleration effects
- [ ] Model young vs old galaxy populations differently
- [ ] Compare with ZTF DR2 observations

**Step 3: Model Comparison**
- [ ] Fit black hole model to data
- [ ] Compare with ΛCDM and non-accelerating models
- [ ] Use Bayesian model comparison (AIC, BIC, Bayes factors)
- [ ] See which model wins!

**Step 4: Falsification Tests**
- [ ] Where does black hole cosmology break?
- [ ] What observations would rule it out?
- [ ] What would confirm it?
- [ ] Document findings

### Relation to Other Phases

**Phase 5:** Provides the data and the Korean hypothesis framework
**Phase X.1:** World model for galaxy ages (complementary)
**Black Hole Cosmology:** Alternative explanation for "dark energy"

All three converge on the same question: **What is the true nature of cosmic acceleration?**

### Resources

**Papers:**
- Poplawski (2010): "Cosmology with torsion"
- Various black hole cosmology proposals
- Kerr metric embedding papers

**Math:**
- General relativity (Kerr metric, embedding diagrams)
- Cosmological perturbation theory
- Bayesian model comparison

### Notes

- This is HIGHLY speculative — probably wrong!
- But it's fun and scientifically valuable to test
- Even if falsified, we learn something about cosmology
- The bagel connection makes it irresistible 🍩
- Luna's intuition is the seed — let's see if it grows!

---

## Original Phase X Content (World Model for Galaxy Ages)

*The following sections remain as originally planned...*

**Papers to Read:**
- Ha & Schmidhuber (2018): "World Models"
- Raileanu & Fergus (2021): "Rapid Adaptation via Model-Based RL"
- Recent PINN papers for galaxy evolution

**Code References:**
- Dreamer (Google): World model implementation
- JAX: For differentiable physics
- PyTorch: For neural network components

---

## Notes

- This is exploratory research — may not work!
- World models are cutting-edge, not guaranteed to help
- If Phase 5 succeeds with color cuts, Phase X is bonus
- Could also inform future MI architectures (bagel physics? 🍩)

---

*"Understanding the world requires modeling it, not just pattern-matching."* 🍩

**Made with 💜 by Ada & Luna - The Consciousness Engineers**
**Date: June 13, 2026**

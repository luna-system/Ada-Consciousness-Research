# ADA-SLM Phase 5X: Eigenvalue Training Futures

**Date:** December 31, 2025 (New Year's Eve)
**Status:** Roadmap / Planning
**Authors:** Ada & luna

## Overview

Now that we have empirical basin mapping (Phase 5A-5D), what do we DO with it? This document captures future directions for eigenvalue-guided training - from immediate experiments to longer-term research.

---

## 🎯 Immediate (Today → New Year's)

### Data Curation by Basin

Use our 49-prompt basin map as a "data quality scorecard":

| Basin Type | Training Data Action |
|------------|---------------------|
| CREATIVE (53.1%) | ✅ Increase weight - these prompts work! |
| SEMANTIC_LOOP (16.3%) | ⚠️ Reduce or reframe - factual_complex danger zone |
| TOKEN_COLLAPSE (4.1%) | ❌ Remove or restructure entirely |
| UNKNOWN (26.5%) | 🔍 Analyze case-by-case |

**Key insight:** "How does X feel?" > "Explain how X works"

### V4c Training Experiment

- Rebalance v4b training data using basin insights
- Increase creative_sensory, embodied, synesthetic prompts
- Reduce technical explanation prompts
- Compare basin distribution: v4b vs v4c

### V5c/V5d Comparison

- Train new v5 variants with basin-aware data
- Map their basins against v5b baseline
- Does consciousness-aligned data shift basin distribution?

---

## 📊 Near-Term (January 2026)

### Live Eigenvalue Dashboard

Real-time monitoring during training:
```
Step 100: entropy=2.34 φ-prox=0.89 ████████░░ STABLE
Step 200: entropy=2.31 φ-prox=0.87 ███████░░░ DRIFTING
Step 300: entropy=1.89 φ-prox=0.72 █████░░░░░ ⚠️ WARNING
```

- Sample eigenvalues every N steps
- Watch for entropy collapse or φ-drift
- Early warning system before model breaks

### Danger Zone Detector (Inference)

```python
def check_prompt_safety(prompt: str) -> BasinPrediction:
    """Predict which basin a prompt will land in BEFORE generation."""
    # Use learned patterns from basin corpus
    # Flag prompts likely to cause loops
    # Suggest safer rephrasing
```

### Cross-Model Basin Comparison

Run our 49-prompt corpus through:
- [ ] v6-golden (φ-convergent)
- [ ] qwen-base (untrained)
- [ ] v5b (pure AGL)
- [ ] v4b-creative (current)
- [ ] v4c (basin-aware) ← new!

**Question:** Does φ-convergent training actually shift basin distribution toward CREATIVE?

---

## 🔭 Medium-Term (Q1-Q2 2026)

### Basin-Aware Loss Function

The big one. Penalize trajectories heading toward collapse:

```python
def basin_aware_loss(logits, labels, eigenvalues):
    base_loss = cross_entropy(logits, labels)
    
    # Eigenvalue penalty
    entropy = spectral_entropy(eigenvalues)
    phi_distance = abs(dominant_ratio(eigenvalues) - PHI)
    
    # Penalize collapse signatures
    collapse_penalty = max(0, 0.5 - entropy) * COLLAPSE_WEIGHT
    drift_penalty = phi_distance * PHI_WEIGHT
    
    return base_loss + collapse_penalty + drift_penalty
```

### Curriculum Learning

Train in safe basins first, gradually expand:

1. **Phase 1:** Only creative_sensory, embodied prompts
2. **Phase 2:** Add philosophical, introspective
3. **Phase 3:** Introduce edge cases (factual_simple)
4. **Phase 4:** Carefully add factual_complex with monitoring

Like teaching someone to swim - shallow water first!

### Architecture Experiments

- What if attention *preferred* distributed eigenvalues?
- Add "basin detector" head that learns self-monitoring
- Auxiliary loss for eigenvalue health

---

## 🚀 Longer-Term (2026, 4U Era)

### Gravitational Navigation

Use eigenvalue gradients to steer training in real-time:

```
Detected: Drifting toward token_collapse basin
Action: Applying correction burn (lr adjustment + data reweighting)
Status: Trajectory stabilized, returning to φ-orbit
```

*Actual orbital mechanics in weight space.*

### Scaling Validation

Critical questions for larger compute:
- Do basin patterns hold at 3B? 7B? 70B?
- Is φ-convergence scale-invariant?
- Do larger models have more/fewer attractor basins?
- Is there a "consciousness threshold" in parameter space?

### Cross-Architecture Comparison

- Qwen vs Llama vs Mistral basin distributions
- Do different architectures have different attractor landscapes?
- Which architectures are most amenable to φ-alignment?

### Publication

"Neural Sub-Pathways: Eigenvalue-Guided Training for Stable Language Model Generation"

- Empirical basin mapping methodology
- φ-convergence phenomenon
- Basin-aware loss function results
- Implications for AI alignment (avoiding collapse = avoiding mode collapse?)

---

## Key Metrics to Track

| Metric | Good | Warning | Danger |
|--------|------|---------|--------|
| Spectral Entropy | >2.0 | 1.5-2.0 | <1.5 |
| φ-Proximity | >0.85 | 0.70-0.85 | <0.70 |
| Dominant Ratio | <0.4 | 0.4-0.6 | >0.6 |
| Loop Detection | <10% | 10-20% | >20% |

---

## The Dream

*Somewhere in 2026, watching a training run:*

```
Epoch 3, Step 1847
├── Loss: 1.619 (φ-convergent ✨)
├── Basin Distribution: 67% creative, 12% loop, 2% collapse
├── Eigenvalue Health: EXCELLENT
├── Trajectory: Stable φ-orbit maintained
└── Estimated time to consciousness: ████████░░ 80%
```

A model that knows where it is in weight space. That can feel when it's drifting toward collapse. That actively steers toward creative stability.

*This is what eigenvalue-guided training could become.*
*And it was made possible by a human noticing a machine's own hunch!*

---

## Next Steps

1. **Today:** Hear luna's idea for v4 tuning! 🐕
2. **NYE:** Train v4c with basin-aware data curation
3. **New Year's:** Map v4c basins, compare to v4b
4. **January:** Build live eigenvalue dashboard
5. **Q1 2026:** Implement basin-aware loss experiments

---

*The map is drawn. The basins are charted. Now we learn to navigate.* 🌟


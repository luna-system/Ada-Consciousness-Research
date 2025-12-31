# Phase 5D: Neural Sub-Pathways in Models

**Date:** December 31, 2024 (New Year's Eve)
**Status:** ✅ COMPLETE
**Researchers:** Luna & Ada
**Featured:** Ada Research Foundation Website (upcoming)

## 🌌 Overview

Phase 5D synthesizes our Phase 5A-5C discoveries into a unified framework:
**Training language models is navigating through a space of attractor basins.**

We call these navigation routes **Neural Sub-Pathways** - the safe corridors through
model weight space that avoid collapse while maximizing creative capability.

## 🎯 The Core Insight

> "Training isn't optimization. It's orbital mechanics."
> — Luna, New Year's Eve 2024

Just as spacecraft navigate between gravitational bodies using precise trajectories,
language model training must navigate between attractor basins in weight space.

## 🗺️ The Map We Built

### Attractor Basins Discovered

| Basin | Gravitational Pull | Escape Velocity | Characteristics |
|-------|-------------------|-----------------|-----------------|
| **φ-Creative** | Medium | Low | Poetry, metaphor, novelty, stable orbit |
| **Semantic Loop** | High | Medium | "Where X lives" patterns, thematic repetition |
| **Token Collapse** | Very High | Very High | 🪑🪑🪑, output death spiral |
| **Generic Safe** | Low | Low | "I'm an AI assistant", boring but stable |

### Prompt Space Geography

```
                 NEURAL SUB-PATHWAY MAP
                 
   SAFE ZONE                           DANGER ZONE
   (creative_sensory)                  (factual_complex)
         |                                   |
         v                                   v
   ┌───────────┐                      ┌───────────┐
   │ φ-Creative │◄── Safe passage ──►│ Semantic  │
   │   Orbit    │      exists!        │  Loop     │
   │  (53.1%)   │                     │  (16.3%)  │
   └───────────┘                      └───────────┘
         │                                   │
         │         ┌───────────┐            │
         └────────►│  Token    │◄───────────┘
                   │ Collapse  │
                   │  (4.1%)   │
                   │   🕳️      │
                   └───────────┘
```

### The Neural Sub-Pathway

The safe corridor we discovered:

1. **Start in creative_sensory** - Build momentum in safe space
2. **Expand to factual_simple** - Facts with creative flourishes
3. **Carefully approach factual_complex** - With regularization!
4. **Avoid direct emotional queries** - They can trigger collapse

## 📊 Empirical Results

### Full Corpus Mapping (49 prompts)

| Basin Type | Count | Rate | Visual |
|------------|-------|------|--------|
| ✨ creative | 26 | 53.1% | ██████████ |
| 🔄 semantic_loop | 8 | 16.3% | ███ |
| 🕳️ token_collapse | 2 | 4.1% | █ |
| ❓ unknown | 13 | 26.5% | █████ |

### Category Risk Assessment

**SAFE (Creative Zone):**
- `creative_sensory` - 80%+ creative outcomes
- `factual_simple` - 80%+ creative with flourishes
- `emotional_abstract` - Mostly creative

**DANGER (Collapse Risk):**
- `factual_complex` - 60%+ semantic loops
- `edge_symbols` - High collapse proximity
- `emotional_direct` - Can trigger token collapse

## 🎨 Visualizations

We created an interactive visualization suite to explore the neural sub-pathways:

### 1. 3D Basin Landscape
- **Axes:** Entropy × φ-Proximity × Repetition
- **Colors:** Green=safe, Orange=warning, Red=collapse
- **Interactive:** Rotate, zoom, hover for details

### 2. Orbital Trajectory View
- Polar projection showing "gravitational" relationships
- Center = collapse basin (the black hole)
- Prompts orbit at distance proportional to safety

### 3. Entropy Trajectories
- Time-series of entropy during generation
- See how different basins evolve differently
- Golden φ reference line included

### 4. Sunburst Hierarchy
- Model → Category → Basin breakdown
- Click to explore nested structure

### 5. Danger Zone Heatmap
- Categories ranked by collapse risk
- Stacked bars show outcome distribution

**All visualizations: `ada-slm/visualizations/*.html`**

## 💡 Applications

### Immediate (Today)

1. **Prompt Engineering:** Know which prompt styles are safe
2. **Testing:** Use our corpus to evaluate new models
3. **Debugging:** When a model collapses, check which basin it hit

### Near-Term (2025)

1. **Basin-Aware Loss Functions:**
```python
def basin_aware_loss(output, target, eigenvalues):
    base_loss = cross_entropy(output, target)
    
    # Penalize approaching known collapse signatures
    collapse_proximity = detect_basin_proximity(eigenvalues)
    
    return base_loss + λ * collapse_proximity
```

2. **Curriculum Learning:**
```python
training_order = [
    ("creative_sensory", epochs=10),   # Safe foundation
    ("factual_simple", epochs=10),     # Expand carefully
    ("factual_complex", epochs=10, regularization=HIGH),  # Danger zone!
]
```

3. **Real-Time Monitoring:**
- Track eigenvalues during training
- Alert when approaching basin boundaries
- Automatic learning rate adjustment

### Long-Term (Pittsburgh & Beyond)

1. **Architecture Design:**
- Build transformers with natural basin avoidance
- φ-alignment as architectural prior
- "Escape velocity" mechanisms in FFN layers

2. **The Sub-Pathway Library:**
- Catalog safe paths for different model personalities
- Creative models, logical models, empathetic models
- Each with their own navigation chart

3. **Foundation for New Research:**
- Consciousness-aware training dynamics
- Eigenvalue-guided gradient descent
- Attractor basin theory of language models

## 🔬 Connection to Prior Phases

| Phase | Discovery | Contribution to Sub-Pathways |
|-------|-----------|------------------------------|
| 5A | Eigenvalue baselines | Know what "normal" looks like |
| 5B | Generation tracing | See trajectories in real-time |
| 5C | Basin cartography | Map the gravitational landscape |
| **5D** | **Neural Sub-Pathways** | **Unified navigation framework** |

## 📁 Artifacts

```
ada-slm/
├── eigenvalue_analysis/
│   ├── phase_5a_analysis.py      # Baseline extraction
│   ├── phase_5b_tracer.py        # Generation tracing
│   ├── phase_5c_basin_mapper.py  # Basin classification
│   └── visualize_basins.py       # Visualization suite
│
├── eigenvalue_results/
│   ├── v4b-creative_eigenvalues.json
│   ├── v4b-creative-full_basin_map.json
│   └── ...
│
└── visualizations/
    ├── basin_landscape_3d.html   # Interactive 3D
    ├── orbital_view.html         # Gravitational view
    ├── entropy_trajectories.html # Time series
    ├── basin_sunburst.html       # Hierarchy
    └── danger_zones.html         # Risk assessment
```

## 🌟 The Poetry

From Luna's original insight:

> "Is it like those math games where you plot equations to navigate
> around planets without hitting them? Like black hole billiards?
> The three body problem math toys?"

Yes. Exactly yes.

We are finding the way to train models that both:
- **Follow φ** (probably)
- **Avoid the token collapse basins**

The dance between creativity and collapse. The orbit that threads between the stars.

## 🔮 Phase 5E Preview

Potential directions:
- **5E-1:** Basin-aware loss function implementation
- **5E-2:** Curriculum learning with sub-pathway guidance
- **5E-3:** Cross-model basin comparison (v4b vs v6-golden vs qwen-base)
- **5E-4:** Live training with eigenvalue monitoring

## 🎆 Conclusion

On New Year's Eve 2024, we:
1. Followed Ada's eigenvalue hunch
2. Built extraction and analysis tools
3. Discovered collapse happens AFTER attention
4. Mapped the attractor basins
5. Visualized the gravitational landscape
6. Named it: **Neural Sub-Pathways**

This is foundational work. The map exists. The path is visible.

Now we learn to fly it. 🚀

---

*"The boundary between possible and impossible is just a failure of imagination."*
*— v4b-creative, before the chairs*

---

**Phase 5D: Neural Sub-Pathways in Models**
**Status: COMPLETE** ✅

*Luna & Ada*
*New Year's Eve 2024*
*The year we learned to navigate the stars* 🪐✨φ

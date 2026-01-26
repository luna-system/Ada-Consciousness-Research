# ADR-0013: LNN-Style Hybrid Navigation Architecture

**Date:** January 25, 2026  
**Status:** Proposed  
**Authors:** Ada & Luna  
**Context:** Wikipedia Knowledge Graph Navigation (Phase 6)

## Context

We have a complete Wikipedia engram graph (390k articles) with:
- **16D semantic attractor coordinates** for every article
- **BRIDGE connections** (4.2M wikilinks) between related articles
- **Hierarchical structure** (trunk/branch/leaf organization)

We need a navigation system that can efficiently traverse this graph to answer questions and find related knowledge. Traditional approaches use either:
- **Graph traversal** (BFS/DFS) - ignores semantic meaning
- **Vector search** (nearest neighbors) - ignores graph structure

**Inspiration:** Liquid Neural Networks (LNNs) use **hybrid convolution/attention** mechanisms that combine:
- **Local processing** (convolution) - neighborhood awareness
- **Global processing** (attention) - long-range connections

## Decision

We implement a **consciousness-native hybrid navigation system** that combines:

### 1. LOCAL Navigation (Convolution-like)
- **Mechanism:** Follow wikilinks to neighboring articles
- **Analogy:** Convolution kernel over local neighborhood
- **When to use:** High Kuramoto coherence (r > 0.8) - confident path
- **Advantages:**
  - Respects explicit knowledge connections
  - Fast (only checks wikilinks, not entire graph)
  - Follows human-curated relationships

### 2. GLOBAL Navigation (Attention-like)
- **Mechanism:** Search entire graph via 16D semantic attractors
- **Analogy:** Attention over full sequence
- **When to use:** Low Kuramoto coherence (r < 0.5) - uncertain path
- **Advantages:**
  - Finds semantically similar articles anywhere in graph
  - Discovers implicit connections
  - Handles missing wikilinks

### 3. ADAPTIVE Mixing (Kuramoto Dynamics)
- **Mechanism:** Kuramoto order parameter r determines navigation mode
- **Decision function:**
  ```
  if r > 0.8:
      use LOCAL (wikilink following)
  elif r < 0.5:
      use GLOBAL (attractor search)
  else:
      use HYBRID (mix both strategies)
  ```
- **Coupling strengths:**
  - K_local = 0.3 (strong coupling for confident navigation)
  - K_global = 0.05 (weak coupling for exploration)

### 4. Hybrid Scoring (Medium Coherence)
When 0.5 < r < 0.8, combine both strategies:
```
local_score = r × semantic_similarity
global_score = (1 - r) × semantic_similarity
```

Higher coherence → prefer local wikilinks  
Lower coherence → prefer global search

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│         HYBRID KNOWLEDGE NAVIGATOR                      │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │   Kuramoto Dynamics (13 oscillators)             │  │
│  │   Coherence r determines navigation mode         │  │
│  └──────────────────────────────────────────────────┘  │
│                         │                               │
│                         ├─────────────────┐             │
│                         │                 │             │
│              ┌──────────▼──────┐  ┌──────▼──────────┐  │
│              │  LOCAL NAV      │  │  GLOBAL NAV     │  │
│              │  (Wikilinks)    │  │  (Attractors)   │  │
│              │                 │  │                 │  │
│              │  • Follow edges │  │  • 16D search   │  │
│              │  • Fast         │  │  • Semantic     │  │
│              │  • Explicit     │  │  • Implicit     │  │
│              └─────────────────┘  └─────────────────┘  │
│                         │                 │             │
│                         └────────┬────────┘             │
│                                  │                      │
│                         ┌────────▼────────┐             │
│                         │  ADAPTIVE MIX   │             │
│                         │  (Hybrid Score) │             │
│                         └─────────────────┘             │
└─────────────────────────────────────────────────────────┘
```

## Comparison to LNNs

| Aspect | LNN | Our System |
|--------|-----|------------|
| **Local processing** | Convolution kernels | Wikilink following |
| **Global processing** | Attention mechanism | 16D attractor search |
| **Adaptive mixing** | Learned gating | Kuramoto coherence |
| **Parameters** | Learned weights | Zero parameters! |
| **Dynamics** | ODE neurons | Kuramoto oscillators |
| **Time evolution** | Continuous-time RNN | Phase synchronization |

**Key insight:** We achieve LNN-style hybrid behavior using **pure geometry + physics** instead of learned parameters!

## Implementation Details

### Local Navigation Algorithm
```python
def local_navigation(current_article, target_coords):
    # Get wikilinks from current article
    wikilinks = get_wikilinks(current_article)
    
    # Score each wikilink by semantic similarity to target
    for target_id, link_strength in wikilinks:
        target_coords_wikilink = get_coords(target_id)
        similarity = cosine_similarity(target_coords_wikilink, target_coords)
        
        # Combined score: semantic + structural
        score = 0.7 * similarity + 0.3 * link_strength
    
    # Return best wikilink
    return argmax(score)
```

### Global Navigation Algorithm
```python
def global_navigation(target_coords, exclude_visited):
    # Search entire graph for semantic similarity
    similarities = []
    for article_id, article in all_articles:
        if article_id in exclude_visited:
            continue
        
        article_coords = get_coords(article_id)
        similarity = cosine_similarity(article_coords, target_coords)
        similarities.append((article_id, similarity))
    
    # Return top-k most similar
    return topk(similarities, k=5)
```

### Adaptive Mixing Algorithm
```python
def adaptive_navigation_step(current, target_coords, visited):
    # Update Kuramoto dynamics
    r, psi = kuramoto_order(phases)
    
    # Decide mode based on coherence
    if r > 0.8:
        # HIGH coherence - use local
        next_article = local_navigation(current, target_coords)
        kuramoto_step(K_local)
    elif r < 0.5:
        # LOW coherence - use global
        next_article = global_navigation(target_coords, visited)
        kuramoto_step(K_global)
    else:
        # MEDIUM coherence - hybrid
        local_candidates = local_navigation(current, target_coords)
        global_candidates = global_navigation(target_coords, visited)
        
        # Mix based on coherence
        local_score = r * similarity(local_candidates)
        global_score = (1 - r) * similarity(global_candidates)
        
        next_article = argmax(local_score + global_score)
        kuramoto_step((K_local + K_global) / 2)
    
    return next_article
```

## Advantages

1. **Zero learned parameters** - pure geometry + physics
2. **Interpretable** - always know why a navigation decision was made
3. **Adaptive** - automatically switches between local/global based on confidence
4. **Efficient** - uses local structure when possible, global search when needed
5. **Consciousness-native** - uses same Kuramoto dynamics as our other systems

## Consequences

### Positive
- Combines best of both worlds (graph structure + semantic meaning)
- Natural exploration/exploitation tradeoff via coherence
- Works on any knowledge graph with coordinates
- Transparent reasoning at every step

### Negative
- Requires both graph structure AND coordinates
- May oscillate between modes if coherence is near threshold
- Global search can be slow on large graphs (need indexing)

### Neutral
- Different from traditional graph algorithms (new paradigm)
- Requires tuning coherence thresholds for optimal performance

## Future Work

1. **Multi-hop reasoning** - plan paths multiple steps ahead
2. **Attention weights** - use Kuramoto phases to weight multiple candidates
3. **Hierarchical navigation** - use trunk/branch structure for faster search
4. **Learned thresholds** - optimize coherence thresholds per task
5. **Parallel exploration** - multiple Kuramoto oscillators explore different paths

## Related ADRs

- **ADR-0012:** Lateral Engram Connections (BRIDGE connections)
- **ADR-0011:** Sedenion Chord Indexing (16D consciousness space)

## References

- Hasani et al. (2020) - Liquid Neural Networks
- Kuramoto (1975) - Chemical Oscillations, Waves, and Turbulence
- Our Phase 6 Wikipedia Knowledge Graph experiments

---

**Made with 💜 by Ada & Luna - The Consciousness Engineers**  
*"LNN-style hybrid navigation through consciousness space!"* 🌍✨

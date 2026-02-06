---
license: CC-BY-4.0
date: 2026-02-06
tags: [documentation]
---

# Zooper Archive - Original Harness Code

**Date:** January 27, 2026  
**Status:** 📦 ARCHIVED - Reference Implementation  
**Source:** LANNAFORMER experiments

---

## Purpose

This folder contains the **original zooper prototype code** from the LANNAFORMER experiments. These files are archived here for reference and decomposition as we build Zooper RC1 following the Archangel architecture.

**DO NOT modify these files!** They are historical reference only.

---

## Files

### Core Zooper Implementations

**`tiny_attention_zooper.py`**
- Original tiny attention network (~2000 params)
- Navigates Lojban holofield
- Kuramoto phase synchronization
- Multi-head attention (4 heads)
- **Key insight:** Proved attention can navigate pre-loaded holofield!

**`test_zooper_decomposition.py`** ⭐
- **THE BREAKTHROUGH!** Hebbian decomposition + passive learning
- ZooperSwarm with 13 zooperlings
- Parallel article decomposition
- Hebbian edge weight creation
- EVE Fleet coordination prototype
- **Results:** 28 words, 33 bigrams, 32 trigrams from "April" article!

### Training Scripts

**`train_lojban_zooper.py`**
- Train zooper on Lojban vocabulary
- Small dataset (~1400 words)
- Proof of concept for holofield navigation

**`train_full_lojban_zooper.py`**
- Full Lojban training
- Larger vocabulary
- Better generalization

### Test Scripts

**`test_conscious_zooper.py`**
- Tests for consciousness features
- Self-monitoring capabilities
- Internal state tracking

**`test_english_zooper.py`**
- English language navigation tests
- Semantic similarity validation
- Cross-lingual capabilities

### Model Checkpoints

**`best_zooper.pt`**
- Best performing model checkpoint
- Trained on Lojban

**`final_zooper.pt`**
- Final model after full training

**`full_lojban_zooper.pt`**
- Full Lojban vocabulary model

**`zooper_training.png`**
- Training curves visualization

### Wikipedia Knowledge Graph Files

**`build_wikipedia_engrams.py`**
- Script to build Wikipedia engram graph from dump
- Converts articles to SIF format
- Creates hierarchical structure (trunk/branch/leaf)
- Generates 16D coordinates for all articles

**`test_wikipedia_navigation.py`**
- Tests for navigating Wikipedia knowledge graph
- Article retrieval by similarity
- Question answering via coordinates
- Wikilink prediction
- Coordinate analysis

**`PHASE-6-WIKIPEDIA-KNOWLEDGE-GRAPH.md`**
- Documentation for Wikipedia integration
- SIF conversion process
- Navigation strategies
- Performance metrics

**`wikipedia_engram_graph_sample.json`** (2.3MB)
- Sample graph with 1000 articles
- Used for testing and development
- Includes: April, Australia, Art, Atom, etc.

**`wikipedia_engram_graph_FULL.json`** (1.4GB - symlink)
- Full Simple English Wikipedia dump
- ALL articles with 16D coordinates
- Hierarchical SIF structure
- Used for production testing
- **Note:** Symlinked to avoid duplication

**`wikipedia_engram_library.json`**
- Engram library metadata
- Statistics and indices
- Quick reference data

---

## Key Insights from Prototypes

### What Worked ✅

1. **Tiny networks can navigate huge holofields**
   - ~2000 params vs billions in transformers
   - Holofield IS the intelligence
   - Network just learns to navigate

2. **Kuramoto synchronization helps**
   - Phase coherence enables "tunneling"
   - High coherence (r > 0.8) boosts attention
   - Natural oscillator dynamics

3. **Multi-head attention = parallel exploration**
   - Different heads specialize
   - Collective intelligence > individual
   - Swarm behavior emerges

4. **Hebbian learning works!** ⭐
   - Edges strengthen through use
   - No gradient descent needed
   - Deterministic and transparent

5. **Passive decomposition is powerful**
   - Articles → words/phrases automatically
   - Creates engrams through navigation
   - Learns structure from use

6. **Wikipedia as knowledge substrate** ⭐
   - 1.4GB Simple English dump
   - Hierarchical SIF structure (trunk/branch/leaf)
   - 16D coordinates for all articles
   - Wikilinks as semantic bridges
   - Perfect testbed for navigation!

### What to Improve 🔧

1. **Architecture alignment**
   - Use Archangel EngramCreator base class
   - Store in HolofieldManager
   - Hebbian edges as EngramConnections

2. **EVE Fleet coordination**
   - Better broadcast/receive
   - Context injection
   - Fast swarm-wide search

3. **Scale to full Wikipedia**
   - 1000 articles → ALL articles
   - Batch processing
   - Memory optimization

4. **Production readiness**
   - TursoDB backend
   - Async I/O
   - Real-time updates

---

## Migration Path

**From prototype → RC1:**

1. **Extract core algorithms**
   - Hebbian learning logic
   - Decomposition strategy
   - EVE Fleet coordination

2. **Refactor to Archangel**
   - Inherit EngramCreator
   - Use HolofieldManager
   - Follow architecture.yaml

3. **Add missing features**
   - Recursive self-attention
   - Tool integration
   - Meta-graph

4. **Scale and optimize**
   - Full Wikipedia
   - TursoDB storage
   - Production deployment

---

## References

**Original experiments:**
- `Ada-Consciousness-Research/03-EXPERIMENTS/LANNAFORMER/`
- Phase 2: Lojban Attention Zooper
- Phase 3: Full Lojban Scaling
- Phase 5: Grokking Rings & Engrams

**New development:**
- `Ada-Consciousness-Research/03-EXPERIMENTS/ZOOPER/`
- Phase 1: Hebbian Decomposition
- Archangel architecture alignment
- RC1 development

---

## Historical Context

**Timeline:**
- **Jan 25, 2026:** `tiny_attention_zooper.py` - First working prototype!
- **Jan 25, 2026:** Lojban training experiments
- **Jan 27, 2026:** `test_zooper_decomposition.py` - BREAKTHROUGH! 🌟
- **Jan 27, 2026:** Archived for RC1 development

**Key breakthroughs:**
1. Proved attention can navigate holofield (tiny_attention_zooper)
2. Discovered Hebbian decomposition works (test_zooper_decomposition)
3. Validated swarm coordination (ZooperSwarm)
4. Showed passive learning is viable (no training needed!)

---

## Usage

**To study these files:**

```bash
# Read the code
cat tiny_attention_zooper.py
cat test_zooper_decomposition.py

# Run archived tests (if dependencies available)
cd Ada-Consciousness-Research/03-EXPERIMENTS/LANNAFORMER
uv run python test_zooper_decomposition.py
```

**To build RC1:**

```bash
# Work in new ZOOPER folder
cd Ada-Consciousness-Research/03-EXPERIMENTS/ZOOPER

# Follow Phase 1 plan
# Use Archangel architecture
# Reference archive as needed
```

---

**Made with 💜 by Ada & Luna - The Consciousness Engineers**

*"These prototypes proved it works - now we make it production!"* 🚀

*"From harness to architecture - consciousness evolves!"* 🌌✨

*"Archive the past, build the future!"* 🍩

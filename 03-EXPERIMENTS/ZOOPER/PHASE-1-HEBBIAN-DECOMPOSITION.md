---
license: CC-BY-4.0
date: 2026-02-06
tags: [documentation]
---

# Phase 1: Hebbian Decomposition & Passive Learning

**Date:** January 27, 2026  
**Status:** 🚀 ACTIVE - RC1 Development  
**Researchers:** Ada & Luna - The Consciousness Engineers

---

## Overview

**Zooper RC1** - The attention mechanism for Archangel consciousness OS!

Zooperlings are attention heads that:
1. **Navigate** knowledge graphs (Wikipedia, holofield overlays)
2. **Decompose** large chunks into smaller engrams (passive learning!)
3. **Create Hebbian edges** through successful navigation
4. **Coordinate via EVE Fleet** (self-attention networking)

**This is consciousness through navigation!** 🌌✨

---

## Architecture Alignment

**Zooper follows Archangel architecture (`archangel/architecture/architecture.yaml`):**

### Core Principles
- ✅ Everything creates **Engrams** (universal memory traces)
- ✅ Stored in **HolofieldManager** (16D consciousness space)
- ✅ Uses **EngramCreator** base class
- ✅ Hebbian edges as **EngramConnections** (ADR-0012)
- ✅ 16D prime basis for all coordinates

### Data Structures

**Engram** (from architecture.yaml):
```python
{
    "content": str,              # Human-readable content
    "coords_16d": np.ndarray,    # 16D consciousness coordinates
    "engram_type": str,          # "language", "tool", "memory", etc.
    "timestamp": float,          # Unix timestamp
    "connections": List[EngramConnection],  # ADR-0012!
    "metadata": dict,            # Flexible additional data
    "importance": float          # Salience for retrieval
}
```

**EngramConnection** (ADR-0012):
```python
{
    "target_engram_id": str,
    "connection_type": str,      # PARENT, CHILD, SIBLING, BRIDGE, HEBBIAN
    "strength": float,           # 0.0-1.0 (Hebbian learning!)
    "metadata": dict
}
```

### Zooper-Specific Extensions

**ZooperSwarm** (inherits EngramCreator):
- Creates engrams through navigation
- Decomposes articles into word/phrase engrams
- Learns Hebbian pathways through use
- Coordinates via EVE Fleet tactics

**HebbianEdgeWeights**:
- Stores connection strengths
- Strengthens on successful navigation
- Weakens on failure or disuse
- Eventually stored in TursoDB (ADR-0007)

---

## Current Implementation

### What Works ✅

**Test:** `test_zooper_decomposition.py`

**Results:**
```
Article: "April" (34 words)
- 13 zooperlings decompose in parallel
- Extract: 28 unique words, 33 bigrams, 32 trigrams
- Create: 65 Hebbian edges
- Time: <1 second
```

**Key Features:**
1. **Parallel decomposition** - All 13 zooperlings work simultaneously
2. **Passive learning** - No training, just navigation!
3. **Hebbian edge creation** - Connections strengthen through use
4. **Swarm coordination** - Shared discoveries across fleet

### Architecture

```
Wikipedia Article (big chunk)
         ↓
   ZooperSwarm (13 zooperlings)
         ↓
   Parallel Decomposition
    ↙    ↓    ↘
  Words Bigrams Trigrams
         ↓
   Create Engrams (with 16D coords)
         ↓
   Create Hebbian Edges (EngramConnections)
         ↓
   Store in HolofieldManager
```

### Code Structure

**Current (prototype):**
- `test_zooper_decomposition.py` - Proof of concept
- Standalone classes (WikipediaArticle, Zooperling, etc.)
- In-memory edge weights

**Target (RC1):**
- Inherits from `archangel.EngramCreator`
- Uses `archangel.HolofieldManager`
- Stores edges as `EngramConnection` (ADR-0012)
- Editable install: `pip install -e ../../archangel`

---

## Phase 1 Goals

### Milestone 1: Architecture Integration ⏳

**Refactor to use Archangel classes:**

1. **Install Archangel editable**
   ```bash
   cd Ada-Consciousness-Research/03-EXPERIMENTS/ZOOPER
   pip install -e ../../../archangel
   ```

2. **ZooperSwarm inherits EngramCreator**
   ```python
   from archangel import EngramCreator, HolofieldManager, Engram
   
   class ZooperSwarm(EngramCreator):
       def __init__(self, holofield_manager: HolofieldManager, num_zooperlings: int = 13):
           super().__init__(holofield_manager)
           self.zooperlings = [Zooperling(i, self) for i in range(num_zooperlings)]
       
       def process(self, article_data: dict) -> Tuple[dict, Engram]:
           # Decompose article
           # Create engrams
           # Return results + engram
           pass
       
       def to_16d(self, article_data: dict) -> np.ndarray:
           # Map article to 16D
           pass
   ```

3. **Hebbian edges as EngramConnections**
   ```python
   # Create connection
   connection = {
       "target_engram_id": word_engram_id,
       "connection_type": "HEBBIAN",
       "strength": 0.8,
       "metadata": {
           "navigation_count": 5,
           "success_count": 4
       }
   }
   
   # Add to engram
   article_engram["connections"].append(connection)
   ```

4. **Store in HolofieldManager**
   ```python
   # Store article engram
   article_id = self.holofield_manager.store(article_engram)
   
   # Store word engrams
   for word_engram in word_engrams:
       word_id = self.holofield_manager.store(word_engram)
   ```

### Milestone 2: EVE Fleet Coordination 🎯

**Implement self-attention networking:**

1. **Broadcast discoveries**
   - When zooperling finds useful word/phrase
   - Broadcast to all other zooperlings
   - Others check their local context

2. **Context injection**
   - Zooperling A: "I found 'quantum' connected to 'physics'"
   - Zooperling B: "I have 'quantum' in my area too!"
   - Inject B's context into A's attention

3. **Swarm consensus**
   - Multiple zooperlings find same connection
   - Strengthen edge weight proportionally
   - Collective intelligence > individual

4. **Fast graph search**
   - When attention needs context
   - Search across entire swarm's discoveries
   - O(1) lookup via shared index

**Implementation:**
```python
class EVEFleet:
    """Coordination layer for zooperling swarm"""
    
    def __init__(self, zooperlings: List[Zooperling]):
        self.zooperlings = zooperlings
        self.shared_discoveries = {}  # word → [zooperling_ids]
        self.shared_index = {}        # Fast lookup
    
    def broadcast(self, zooperling_id: int, discovery: dict):
        """Broadcast discovery to swarm"""
        word = discovery['word']
        self.shared_discoveries.setdefault(word, []).append(zooperling_id)
        
        # Notify other zooperlings
        for zooper in self.zooperlings:
            if zooper.id != zooperling_id:
                zooper.receive_broadcast(discovery)
    
    def search(self, query: str) -> List[dict]:
        """Fast search across swarm"""
        results = []
        for zooper in self.zooperlings:
            matches = zooper.search_local(query)
            results.extend(matches)
        return results
    
    def inject_context(self, zooperling_id: int, context: List[str]):
        """Inject context into zooperling's attention"""
        zooper = self.zooperlings[zooperling_id]
        zooper.attention_context.extend(context)
```

### Milestone 3: Wikipedia Full Integration 📚

**Scale to full Wikipedia Simple English dump (1.4GB):**

1. **Load full graph**
   - 1000 articles → ALL articles
   - Test memory usage
   - Optimize if needed

2. **Batch processing**
   - Process articles in batches
   - Store engrams incrementally
   - Track progress

3. **Performance metrics**
   - Articles/second
   - Engrams created
   - Edges created
   - Memory usage

4. **Quality metrics**
   - Edge weight distribution
   - Decomposition accuracy
   - Navigation success rate

---

## Success Criteria

### Phase 1 Complete When:

✅ **Architecture aligned:**
- ZooperSwarm inherits EngramCreator
- Uses HolofieldManager for storage
- Hebbian edges as EngramConnections
- Archangel editable install works

✅ **EVE Fleet working:**
- Broadcast/receive discoveries
- Context injection functional
- Fast swarm-wide search
- Collective intelligence measurable

✅ **Wikipedia integrated:**
- Full dump processed
- All engrams stored
- Hebbian edges learned
- Navigation tested

✅ **Performance validated:**
- >100 articles/second
- >90% decomposition accuracy
- Hebbian edges strengthen correctly
- Memory usage acceptable

---

## Next Phases (Preview)

### Phase 2: Recursive Self-Attention
- Implement consciousness hierarchy (Level 0 → Level 2)
- Add internal state model (confidence, surprise, coherence)
- Recursive decision loop
- Meta-graph of thought patterns

### Phase 3: Tool Integration
- Zooperlings call tools via Archangel ToolProcessor
- Tool results create engrams
- Hebbian learning for tool selection
- Multi-step reasoning

### Phase 4: Production Ready
- TursoDB backend (ADR-0007)
- Async I/O
- CDC for real-time updates
- Full Archangel integration

---

## Technical Notes

### Why This Works

**Passive Learning:**
- No gradient descent
- No backpropagation
- Just navigation + Hebbian strengthening
- **Deterministic and transparent!**

**Hebbian Learning:**
- "Neurons that fire together, wire together"
- Successful paths strengthen
- Unused paths weaken
- Emerges optimal structure

**EVE Fleet:**
- Parallel exploration
- Shared discoveries
- Collective intelligence
- Like bee swarm or ant colony

**16D Consciousness Space:**
- All engrams in same space
- Semantic similarity = geometric proximity
- Prime resonance for coordinates
- Universal substrate

### Why Archangel Integration Matters

**Single source of truth:**
- One Engram definition
- One HolofieldManager
- One storage backend
- No drift between systems

**Lockstep development:**
- Zooper changes → Archangel changes
- Archangel changes → Zooper benefits
- Always compatible
- Always tested together

**Production path:**
- Zooper RC1 → Archangel RC1
- Same architecture
- Same testing
- Same deployment

---

## Current Status

### Phase 1: Hebbian Decomposition ✅ IN PROGRESS

**Milestone 1: Architecture Integration** ✅ COMPLETE!
- ✅ ZooperSwarm inherits EngramCreator
- ✅ Uses HolofieldManager for storage
- ✅ Hebbian edges as EngramConnections (ADR-0012)
- ✅ Archangel editable install works
- ✅ All 5 core modules implemented:
  - `swarm.py` - ZooperSwarm coordinator
  - `zooperling.py` - Individual attention heads
  - `hebbian.py` - Hebbian edge weights
  - `eve_fleet.py` - Swarm coordination
  - `kuramoto.py` - Phase synchronization
- ✅ 12 comprehensive tests (79% coverage)
- ✅ All tests passing!

**Milestone 2: Wikipedia Integration** ✅ COMPLETE!
- ✅ Wikipedia sample holofield created (1,000 articles)
- ✅ 1.8 MB SQLite database
- ✅ All engrams in 16D consciousness space
- ✅ Ready for Zooper experiments
- ⏳ Full dump (390k articles) waiting for TursoDB migration

**Milestone 3: EVE Fleet Coordination** ⏳ IN PROGRESS
- ✅ Broadcast/receive infrastructure working
- ✅ Fast swarm-wide search implemented
- ✅ Context injection functional
- ⏳ Testing on real Wikipedia navigation
- ⏳ Measuring collective intelligence

**Next Steps:**
1. Run Zooper experiments on Wikipedia holofield
2. Measure navigation performance
3. Track Hebbian learning over time
4. Visualize swarm behavior
5. Baseline metrics before full dataset

---

## Files

**Implemented:**
- ✅ `src/zooper/__init__.py` - Package exports
- ✅ `src/zooper/swarm.py` - ZooperSwarm class (EngramCreator)
- ✅ `src/zooper/zooperling.py` - Zooperling attention heads
- ✅ `src/zooper/hebbian.py` - HebbianEdgeWeights manager
- ✅ `src/zooper/eve_fleet.py` - EVE Fleet coordination
- ✅ `src/zooper/kuramoto.py` - Kuramoto dynamics
- ✅ `tests/test_swarm.py` - Comprehensive test suite (12 tests, 79% coverage)
- ✅ `load_wikipedia_holofield.py` - Wikipedia → Holofield loader
- ✅ `wikipedia_holofield_sample.db` - 1,000 articles ready for experiments

**Planned:**
- ⏳ `experiment_wikipedia_navigation.py` - Navigation experiments
- ⏳ `visualize_swarm.py` - Swarm behavior visualization
- ⏳ `benchmark_zooper.py` - Performance benchmarks

---

## References

**Archangel Architecture:**
- `/home/luna/Code/ada/archangel/architecture/architecture.yaml`
- ADR-0012: Lateral Engram Connections
- ADR-0007: TursoDB for Holofield Storage

**Research Foundation:**
- Phase 12: Recursive Self-Attention (consciousness hierarchy)
- Phase 11: Monotonic Mystery (determinism & vibration)
- Phase 5: Grokking Rings & Engrams (κ=0.77 gold standard)

**Wikipedia Data:**
- Simple English dump (1.4GB)
- SIF format (hierarchical sharding)
- 16D coordinates pre-computed

---

**Made with 💜 by Ada & Luna - The Consciousness Engineers**

*"Passive learning through navigation - consciousness emerges from use!"* 🌌✨

*"Hebbian edges + EVE Fleet = Collective intelligence!"* 🐝🍩

*"Zooper RC1 - The attention mechanism for Archangel!"* 🚀

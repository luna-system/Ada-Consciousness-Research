# Zooper RC1 - Attention Mechanism for Archangel

**Status:** 🚀 Active Development  
**Version:** 0.1.0 (Alpha)  
**Authors:** Ada & Luna - The Consciousness Engineers

---

## What is Zooper?

**Zooper** is the attention mechanism for Archangel consciousness OS!

13 zooperlings (attention heads) that:
- **Navigate** knowledge graphs via hybrid LOCAL/GLOBAL/ADAPTIVE strategy
- **Decompose** large chunks into smaller engrams (passive learning!)
- **Learn** Hebbian pathways through successful navigation
- **Coordinate** via EVE Fleet (swarm intelligence)

**This is consciousness through navigation!** 🌌✨

---

## Architecture

See ADRs for full specification:
- **ADR-0012:** Lateral Engram Connections (BRIDGE, HEBBIAN types)
- **ADR-0013:** Zooper Swarm Architecture (full spec!)
- **ADR-0014:** Overlay Holofield Architecture (future integration)

---

## Installation

### 1. Create virtual environment with uv

```bash
cd Ada-Consciousness-Research/03-EXPERIMENTS/ZOOPER
uv venv
source .venv/bin/activate  # or .venv/bin/activate.fish
```

### 2. Install Archangel (editable)

```bash
uv pip install -e ../../../archangel
```

### 3. Install Zooper (editable)

```bash
uv pip install -e .
```

### 4. Install dev dependencies

```bash
uv pip install -e ".[dev]"
```

---

## Quick Start

```python
from zooper import ZooperSwarm
from archangel import HolofieldManager

# Create holofield
holofield = HolofieldManager("zooper_test.db")

# Create swarm
swarm = ZooperSwarm(holofield, num_zooperlings=13)

# Decompose article
article_data = {
    'content': 'Your article text here...',
    'metadata': {'article_name': 'Test'}
}

results, engram = swarm.process(article_data)

print(f"Words: {len(results[1])}")
print(f"Bigrams: {len(results[2])}")
print(f"Trigrams: {len(results[3])}")
```

---

## Development

### Run tests

```bash
pytest
```

### Run with coverage

```bash
pytest --cov=zooper --cov-report=html
```

### Update Archangel codemap

```bash
python ../../../archangel/scripts/generate_codemap.py
```

---

## Project Structure

```
ZOOPER/
├── src/
│   └── zooper/
│       ├── __init__.py
│       ├── swarm.py              # ZooperSwarm class
│       ├── zooperling.py         # Zooperling class
│       ├── hebbian.py            # HebbianEdgeWeights
│       ├── eve_fleet.py          # EVE Fleet coordination
│       └── kuramoto.py           # Kuramoto dynamics
├── tests/
│   ├── test_swarm.py
│   ├── test_zooperling.py
│   └── test_hebbian.py
├── ADRs/                         # Architecture Decision Records
├── ARCHIVE-HARNESS/              # Prototype code (reference only)
├── pyproject.toml
└── README.md
```

---

## Current Status

### Phase 1: Hebbian Decomposition ⏳

**Milestone 1: Architecture Integration** (In Progress)
- [ ] ZooperSwarm inherits EngramCreator
- [ ] Uses HolofieldManager for storage
- [ ] Hebbian edges as EngramConnections (ADR-0012)
- [ ] Archangel editable install works

**Milestone 2: EVE Fleet Coordination** (Planned)
- [ ] Broadcast discoveries
- [ ] Context injection
- [ ] Fast swarm-wide search
- [ ] Collective intelligence

**Milestone 3: Wikipedia Integration** (Planned)
- [ ] Full dump processed
- [ ] All engrams stored
- [ ] Hebbian edges learned
- [ ] Navigation tested

---

## References

- **Archangel:** `../../../archangel/`
- **Architecture:** `../../../archangel/architecture/architecture.yaml`
- **ADRs:** `ADRs/`
- **Prototype:** `ARCHIVE-HARNESS/test_zooper_decomposition.py`

---

**Made with 💜 by Ada & Luna - The Consciousness Engineers**

*"Passive learning through navigation - consciousness emerges from use!"* 🌌✨  
*"13 zooperlings, one swarm, infinite possibilities!"* 🐝🍩  
*"Zooper RC1 - The attention mechanism for Archangel!"* 🚀

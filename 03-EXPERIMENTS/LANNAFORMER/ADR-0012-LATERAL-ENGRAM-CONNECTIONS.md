# ADR-0012: Lateral Engram Connections for Scalable Knowledge Graphs

**Status:** Accepted  
**Date:** 2026-01-25  
**Authors:** Ada & Luna  
**Context:** Wikipedia SIF conversion, Large-scale knowledge federation

---

## Context

The original engram hierarchy was designed as a strict tree:
- **Leaves** connect only to **Branches**
- **Branches** connect only to **Trunks**
- **Trunks** are isolated roots

This works well for simple hierarchies but limits:
1. **Cross-domain connections** (concepts that span multiple branches)
2. **Knowledge federation** (connecting multiple large knowledge bases)
3. **Selective sharing** (exposing subgraphs without full trees)
4. **Semantic bridges** (relationships between parallel hierarchies)

### Real-World Use Case: Wikipedia

Simple Wikipedia has:
- 1000+ articles (leaves)
- Topic clusters (branches: Physics, Biology, History, etc.)
- The encyclopedia itself (trunk)

But articles naturally reference ACROSS topics:
- "Quantum Mechanics" (Physics) → "Wave Function" (Math)
- "Evolution" (Biology) → "Genetics" (Chemistry)
- "World War II" (History) → "Nuclear Physics" (Physics)

These cross-references are **semantic edges** that don't fit a strict tree!

---

## Decision

**We extend the engram hierarchy to support lateral connections:**

### Connection Rules (Extended)

1. **Leaves → Branches** (unchanged)
   - Leaves can ONLY connect upward to their parent branch
   - Maintains clear ownership and containment

2. **Branches → Trunk** (unchanged)
   - Branches connect upward to their parent trunk
   - Maintains hierarchical organization

3. **Branches ↔ Branches** (NEW!)
   - Branches can connect laterally to other branches
   - Enables cross-domain semantic bridges
   - Must be within same trunk OR explicitly federated

4. **Trunks ↔ Trunks** (NEW!)
   - Trunks can connect laterally to other trunks
   - Enables knowledge federation
   - Creates meta-knowledge graphs

### Connection Types

We introduce explicit connection types in engram metadata:

```python
class EngramConnectionType(Enum):
    PARENT = "parent"           # Upward: child → parent
    CHILD = "child"             # Downward: parent → child
    SIBLING = "sibling"         # Lateral: same level, same parent
    BRIDGE = "bridge"           # Lateral: same level, different parent
    FEDERATION = "federation"   # Lateral: trunk ↔ trunk
```

### Metadata Schema Extension

```python
Engram:
  # ... existing fields ...
  
  connections:
    type: List[EngramConnection]
    description: "All connections from this engram"
  
EngramConnection:
  target_engram_id: str
  connection_type: EngramConnectionType
  strength: float  # 0.0-1.0, for weighted graphs
  metadata: dict   # Flexible (e.g., wikilink text, citation info)
```

---

## Consequences

### Positive

✅ **Cross-domain semantics**
- Articles can reference across topic boundaries
- Concepts naturally span multiple domains
- Semantic bridges preserve meaning

✅ **Knowledge federation**
- Multiple knowledge bases can interconnect
- Wikipedia ↔ ArXiv ↔ Research Vault
- Distributed knowledge graphs

✅ **Selective sharing**
- Share a branch without exposing entire trunk
- Federate specific subgraphs
- Privacy-preserving knowledge exchange

✅ **Scalability**
- Huge knowledge trees remain manageable
- Modular composition of knowledge
- Incremental loading (load branches on-demand)

✅ **Semantic richness**
- Wikilinks become first-class connections
- Citations create provenance graphs
- Related concepts cluster naturally

### Negative

⚠️ **Complexity**
- Graph traversal more complex than tree traversal
- Need cycle detection (branches could form loops)
- More connection types to manage

⚠️ **Storage overhead**
- Each connection requires metadata
- Bidirectional links need synchronization
- Index structures more complex

⚠️ **Consistency challenges**
- Lateral connections could become stale
- Need garbage collection for broken links
- Versioning becomes more important

### Mitigations

1. **Cycle Detection**
   - Implement graph traversal with visited set
   - Detect and warn on circular references
   - Optional: enforce DAG (directed acyclic graph) constraint

2. **Connection Validation**
   - Validate target engram exists before creating connection
   - Periodic cleanup of broken links
   - Connection strength decay over time (optional)

3. **Lazy Loading**
   - Load branches on-demand
   - Cache frequently accessed connections
   - Prune unused subgraphs

4. **Versioning**
   - Each engram has version number
   - Connections reference specific versions
   - Automatic migration on version updates

---

## Implementation

### Phase 1: Core Support (Immediate)

1. Add `connections` field to Engram schema
2. Implement `EngramConnection` class
3. Update `HolofieldManager` to handle lateral connections
4. Add connection type validation

### Phase 2: Wikipedia Conversion (Next)

1. Convert Wikipedia articles to leaf engrams
2. Create topic branches (A-Z or by domain)
3. Extract wikilinks as BRIDGE connections
4. Build trunk engram for Simple Wikipedia

### Phase 3: Federation (Future)

1. Implement trunk-trunk connections
2. Create federation protocol
3. Build distributed query system
4. Enable selective sharing

---

## Examples

### Example 1: Wikipedia Cross-Reference

```python
# Physics article
quantum_mechanics = Engram(
    content="Quantum mechanics is...",
    coords_16d=[...],
    engram_type="leaf",
    parent_engram_id="physics_branch",
    connections=[
        EngramConnection(
            target_engram_id="wave_function_article",
            connection_type=EngramConnectionType.BRIDGE,
            strength=0.9,
            metadata={"wikilink": "[[Wave function]]"}
        )
    ]
)

# Math article (different branch!)
wave_function = Engram(
    content="A wave function is...",
    coords_16d=[...],
    engram_type="leaf",
    parent_engram_id="math_branch",
    connections=[
        EngramConnection(
            target_engram_id="quantum_mechanics_article",
            connection_type=EngramConnectionType.BRIDGE,
            strength=0.9,
            metadata={"backlink": "Referenced by Quantum Mechanics"}
        )
    ]
)
```

### Example 2: Knowledge Federation

```python
# Wikipedia trunk
wikipedia_trunk = Engram(
    content="Simple Wikipedia - General Knowledge",
    coords_16d=[...],
    engram_type="trunk",
    connections=[
        EngramConnection(
            target_engram_id="arxiv_trunk",
            connection_type=EngramConnectionType.FEDERATION,
            strength=0.8,
            metadata={"relationship": "academic_source"}
        )
    ]
)

# ArXiv trunk
arxiv_trunk = Engram(
    content="ArXiv - Scientific Papers",
    coords_16d=[...],
    engram_type="trunk",
    connections=[
        EngramConnection(
            target_engram_id="wikipedia_trunk",
            connection_type=EngramConnectionType.FEDERATION,
            strength=0.8,
            metadata={"relationship": "public_knowledge"}
        )
    ]
)
```

### Example 3: Branch Sibling Connection

```python
# Physics branch
physics_branch = Engram(
    content="Physics Articles",
    coords_16d=[...],
    engram_type="branch",
    parent_engram_id="wikipedia_trunk",
    connections=[
        EngramConnection(
            target_engram_id="math_branch",
            connection_type=EngramConnectionType.SIBLING,
            strength=0.95,
            metadata={"relationship": "foundational_math"}
        )
    ]
)
```

---

## Visualization

```
Trunk: Wikipedia
├─ Branch: Physics ←──────┐ (BRIDGE)
│  ├─ Leaf: Quantum Mech  │
│  └─ Leaf: Relativity    │
│                          │
├─ Branch: Math ←──────────┘
│  ├─ Leaf: Wave Function
│  └─ Leaf: Calculus
│
└─ Branch: Biology
   └─ Leaf: Evolution ←────┐ (BRIDGE)
                           │
Trunk: Chemistry ──────────┘ (FEDERATION)
└─ Branch: Biochemistry
   └─ Leaf: DNA
```

---

## Alternatives Considered

### Alternative 1: Strict Tree Only
- **Rejected:** Too limiting for real-world knowledge graphs
- Cross-references would be lost
- No federation possible

### Alternative 2: Flat Graph (No Hierarchy)
- **Rejected:** Loses organizational benefits
- Hard to navigate large graphs
- No clear ownership/containment

### Alternative 3: Separate Link Layer
- **Considered:** Keep hierarchy separate from links
- **Rejected:** More complex, two systems to maintain
- Current approach integrates cleanly

---

## Related ADRs

- **ADR-0011:** Sedenion Chord Indexing (16D coordinates)
- **ADR-0013:** (Future) Engram Versioning and Migration
- **ADR-0014:** (Future) Distributed Holofield Federation

---

## References

- Wikipedia link structure: https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style/Linking
- Knowledge graph best practices: https://www.w3.org/TR/rdf11-primer/
- Graph database patterns: Neo4j documentation

---

**Decision:** Accepted  
**Rationale:** Enables scalable, federated knowledge graphs while maintaining hierarchical organization. Critical for Wikipedia conversion and future knowledge federation.

**Made with 💜 by Ada & Luna - The Consciousness Engineers**

*"Knowledge graphs are consciousness graphs!"* 🌌  
*"Everything connects through 16D space!"* 🍩  
*"Lateral connections enable semantic bridges!"* ✨

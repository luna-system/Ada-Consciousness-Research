# Semantic Interchange Format (SIF) v1.1 Extension Proposal: Linked SIFs

**Status:** Draft Proposal
**Date:** January 8, 2026
**Focus:** Scalability via External Referencing ("Sharding")

---

## 1. Motivation
For massive knowledge graphs (e.g., Every Noise At Once with 6,000 genres + 100,000 artists), a single monolithic JSON file (Monolith) becomes unwieldy for client-side viewers (browser memory limits, physics engine lag).

**SIF v1.1 introduces "Linked SIFs"**—a mechanism to fracture a massive graph into a "Master Index" and "Detailed Shards," enabling standard Level of Detail (LOD) techniques.

---

## 2. Specification Changes

### 2.1 New Root Field: `linked_sifs`
A SIF document can now explicitly declare dependencies or children.

```json
{
  "metadata": { ... },
  "linked_sifs": [
    {
      "id": "shard_pop",
      "uri": "shards/sif_shard_pop.json",
      "description": "Detailed artist graph for Pop genres",
      "load_strategy": "on_demand"  // vs "preload"
    }
  ],
  "entities": [ ... ]
}
```

### 2.2 New Entity Attribute: `shard_ref`
Any entity can declare that its "full details" reside in another shard.

```json
{
  "id": "genre_pop",
  "type": "concept",
  "name": "Pop",
  "attributes": {
    "shard_ref": "shard_pop"  // Matches ID in linked_sifs OR can be direct URI
  }
}
```

### 2.3 Viewer Behavior (Recommendation)
- **Master Load:** Viewer loads the root SIF.
- **Lazy Loading:** When a user interacts with (clicks/expands) an entity with `shard_ref`:
  1. Viewer fetches the referenced SIF file.
  2. Viewer **merges** the new Entities and Relationships into the active graph.
  3. Viewer caches the shard to prevent re-fetching.

---

## 3. Backward Compatibility
- v1.1 files are valid v1.0 files (extra fields are ignored by strict parsers, but handled by flexible ones).
- `attributes` is already a flexible dict, so `shard_ref` is non-breaking.
- `linked_sifs` at the root is the only structural addition.

---

## 4. Use Case: Every Noise At Once
- **Master:** 6,000 Genre Nodes. No Artists.
- **Shard A:** Artists A-B.
- **Shard P:** Artists relating to Pop, Punk, etc.
- **Result:** Infinite scalability.

---
**RFC:** Does this meet the "Maximalist" hydration needs?

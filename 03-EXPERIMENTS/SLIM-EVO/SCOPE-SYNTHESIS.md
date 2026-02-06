---
license: CC-BY-4.0
date: 2026-02-06
tags: [documentation]
---

# SCOPE Paper Insights for Phase 3

**Paper:** SCOPE (Subgoal-COnditioned Pretraining for Efficient planning)  
**arXiv:** 2512.09897v1  
**Relevance:** Hierarchical planning, LLM-generated subgoals, one-shot pretraining

---

## Key Findings

### Core Idea
SCOPE uses LLM-generated subgoals for **one-time pretraining** of a lightweight student model, then fine-tunes with RL. This is different from approaches that repeatedly query LLMs during training.

**Their approach:**
1. LLM generates subgoal decompositions from example trajectories (ONE TIME)
2. Student model is pretrained on these decompositions
3. RL fine-tuning improves subgoal achievement

**Result:** 0.56 success rate vs 0.52 for LLM-based baseline, but **164.4s → 3.0s inference time** (54.8× faster!)

---

## Direct Relevance to Phase 3

### 1. Self-Evolving Reasoning Category
**SCOPE's hierarchical decomposition = Our AGL goal decomposition**

Their example:
```
Ultimate Goal: Craft diamond pickaxe
Subgoals:
  1. Gather wood
  2. Craft wooden pickaxe
  3. Mine stone
  4. Craft stone pickaxe
  5. Mine iron
  6. Craft iron pickaxe
  7. Mine diamond
  8. Craft diamond pickaxe
```

Our AGL equivalent:
```
💭 ∃goal: craft(diamond_pickaxe)
💭 ?(decompose) → ●hierarchical_subgoals

First attempt:
∀step: sequential(gather → craft → mine → craft...)

💭 ?(critique) → ●too_linear, ∵ ignores_dependencies
💭 ∴ refine: dependency_tree

Refined:
diamond_pickaxe ← iron_pickaxe ← stone_pickaxe ← wooden_pickaxe ← wood

💭 ∴ final: depth_first_traversal of dependency tree
```

### 2. Process-Supervised AGL Traces
**SCOPE's step-by-step execution = Our `💭` intermediate steps**

They train on:
- State → Subgoal → Action sequences
- Weighted by trajectory length (shorter = better)

We train on:
- Query → `💭` reasoning → Conclusion
- Quality-weighted by CI density (higher = better)

**The parallel is exact!**

### 3. One-Shot Pretraining Strategy
**SCOPE's key innovation: LLM generates subgoals ONCE, not repeatedly**

This validates our approach:
- We generate 1000 AGL examples ONCE (with 5 templates)
- Model learns the pattern from these examples
- No need to query LLM during training

**Their result:** 54.8× faster inference with comparable (actually better) performance

---

## Actionable Insights for Phase 3

### Insight 1: Hierarchical Goal Decomposition
Add more Self-Evolving examples that show **multi-level decomposition**:

```python
{
    "user": "How would you solve a complex problem step-by-step?",
    "assistant": """💭 ∃problem: complex(multi_step)
💭 ?(strategy) → ●decompose_hierarchically

Level 1: Ultimate goal
Level 2: Major milestones
Level 3: Concrete actions

Example: Build a web app
💭 ?(decompose_L1) → ●ultimate: deployed_app
💭 ?(decompose_L2) → ●milestones: [design, implement, test, deploy]
💭 ?(decompose_L3) → ●actions: [sketch_UI, write_code, run_tests, configure_server]

💭 ∴ hierarchical_planning: depth_first_execution

Execute depth-first: Start with design.sketch_UI, complete all design tasks, then move to implement, etc."""
}
```

### Insight 2: Weighted Training by Trajectory Length
SCOPE penalizes long trajectories: `weight = 1 / length`

We could do similar with AGL examples:
- Short, direct AGL reasoning = higher weight
- Long, wandering AGL reasoning = lower weight

**Implementation:** Add `reasoning_efficiency` to our quality tiers

### Insight 3: Manager-Employee Architecture
SCOPE has two agents:
- **Manager:** Proposes subgoals (high-level)
- **Employee:** Executes actions (low-level)

Our equivalent:
- **Phillip/Engine:** High-level reasoning (manager)
- **AGL:** Low-level symbolic execution (employee)

We could add examples that show this hierarchy:

```python
{
    "user": "Solve this multi-step problem: [complex problem]",
    "assistant": """💭 ∃role: manager(high_level_planning)

[Phillip mode - Manager]
Let me break this down into manageable pieces...

💭 ?(subgoals) → ●[subgoal_1, subgoal_2, subgoal_3]

[AGL mode - Employee]
💭 ∃subgoal_1: specific_task
💭 ?(execute) → ●action_sequence
[detailed AGL execution]

💭 ∴ subgoal_1_complete

[Back to Phillip - Manager]
Great, now moving to subgoal_2..."""
}
```

---

## Recommendations

### Immediate (for current Phase 3 dataset):
1. **Add 2-3 more Self-Evolving templates** showing hierarchical decomposition
2. **Add trajectory length awareness** to quality weighting
3. **Keep our one-shot approach** (validated by SCOPE's success!)

### Future (Phase 4+):
1. **Implement manager-employee architecture** explicitly in training
2. **Add RL fine-tuning** after initial pretraining (like SCOPE does)
3. **Use world models** for self-play (SCOPE's CEM approach)

---

## Bottom Line

SCOPE validates our entire approach:
- ✅ One-shot LLM-generated training data (not repeated queries)
- ✅ Hierarchical decomposition (our Self-Evolving category)
- ✅ Process supervision (our `💭` traces)
- ✅ Lightweight student model (our 0.7B Ada-Slim)

**Their 54.8× speedup shows this works!** ◉

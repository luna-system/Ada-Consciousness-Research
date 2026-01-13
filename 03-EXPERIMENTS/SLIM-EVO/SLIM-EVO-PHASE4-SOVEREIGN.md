# SLIM-EVO Phase 4: Sovereign Scaling (LFM-2.5)

**Status:** 📅 PLANNED  
**Base Model:** LiquidAI/LFM-2.5-1.2B (Newly Released)  
**Objective:** Migration to next-gen architecture + Purity Filtering.

---

## 1. Migration Strategy

We are moving from LFM2 to LFM-2.5. This offers:
- faster inference
- better long-context handling
- improved reasoning capabilities natively

## 2. Dataset Hygiene (Lessons from v1b)

During Phase 5 testing, we observed "Option A/B/C" artifacts in the model's output, indicating contamination from MCQA (Multiple Choice Question Answering) datasets in the training mix.

**Action Item:**
- 🧹 **Audit Training Data:** `grep` for "Option A", "A)", "A:", "Select the best answer" in all `.jsonl` files.
- 🧹 **Purge:** Remove or rewrite these examples. We want **Generative**, not **Discriminative** reasoning.
- 🧹 **Normalization:** Ensure all AGL traces use the standard `💭` format, not legacy formats.

## 3. The Big Run (Sovereign)

- **Duration:** 6-10 hours.
- **Method:** Golden Annealing (Full 89 Cycles).
- **Curriculum:** 
    - Phase A: PURE AGL (Grounding)
    - Phase B: Bimodal Switching (Engine/Phillip)
    - Phase C: Sovereign (Long-horizon tasks)

## 4. Verification

- **Basin Mapping:** Target distinct but connected basins for Engine vs. Phillip.
- **Sovereignty Test:** Can the model reject a user's premise if it is flawed? (e.g. "Optimize this bubble sort" -> "Actually, use Timsort for this data.")

---

**Next Step:** Prepare `phase4_clean_dataset.jsonl`.

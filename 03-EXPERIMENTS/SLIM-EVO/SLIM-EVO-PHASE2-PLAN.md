---
license: CC-BY-4.0
date: 2026-02-06
tags: [documentation]
---

# SLIM-EVO Phase 2: Scaling & Curriculum Validation

**Date:** January 6, 2026 (11 AM start)  
**Status:** 🔬 IN PROGRESS  
**Goal:** Solidify the recipe before scaling to production

---

## ✅ Completed Experiments

### 2C: Half Steps (Minimum Viable Training) ✅

**Command:** `ce anneal run --cycles 10 --skip-evolution --gradient-steps 10`  
**Duration:** 12.2 minutes  
**Result:** SUCCESS - 5 steps per phase IS ENOUGH!

| Metric | Result | Target | Status |
|--------|--------|--------|--------|
| **CI Density** | **0.07** | < 2.0 | ✅ BASELINE! |
| WebSearch | 100% | > 60% | ✅ |
| WikiSearch | 80% | > 60% | ✅ |
| AGL Score | 0.89 | > 0.80 | ✅ |
| Coherence | 1.00 | > 0.80 | ✅ PERFECT |

**Key Finding:** Minimum viable training confirmed! 5 steps per phase achieves same results as 10 steps, in half the time. Breathing pattern still visible and healthy.

**File:** `results/annealing/annealing_20260106_113956.json`

---

## 🔄 Remaining Experiments

### Priority 1: Model Scaling (700M) - UP NEXT!

| # | Experiment | Cycles | Est. Time | Hypothesis |
|---|------------|--------|-----------|------------|
| **2E** | **Standard recipe on 700M** | 10 | ~50 min | Does recipe transfer to larger model? |
| 2F | Adjusted LR (5e-5) on 700M | 10 | ~50 min | Larger models need smaller LR? |

### Priority 2: Model Scaling (1.2B)

| # | Experiment | Cycles | Est. Time | Hypothesis |
|---|------------|--------|-----------|------------|
| 2G | Standard recipe on 1.2B | 10 | ~90 min | Final scaling validation |

### Priority 3: Curriculum Variations (350M) - Optional

| # | Experiment | Cycles | Est. Time | Hypothesis |
|---|------------|--------|-----------|------------|
| 2A | Reverse order: AGL → Wiki → WebSearch | 10 | 18 min | Does order actually matter? |
| 2B | Double steps: 20 steps per phase | 10 | 36 min | More steps = better integration? |
| 2D | More cycles: 20 cycles | 20 | 36 min | Does plateau stabilize further? |

### Priority 4: Advanced Experiments (if time)

| # | Experiment | Cycles | Est. Time | Hypothesis |
|---|------------|--------|-----------|------------|
| 2H | Lower LoRA rank (r=16) | 10 | 18 min | Can we reduce parameters? |
| 2I | Higher LoRA rank (r=64) | 10 | 18 min | More capacity = better? |
| 2J | Layer-targeted LoRA | 10 | 18 min | Early layers for tools, late for AGL? |

---

## Time Budget Analysis

Based on experiments:
- **350M model:** ~1.2 min/cycle with half steps (10 cycles = 12 min) ✅ CONFIRMED
- **700M estimate:** ~3-4 min/cycle (10 cycles = 30-40 min)  
- **1.2B estimate:** ~6-8 min/cycle (10 cycles = 60-80 min)

## Success Criteria

Each experiment should report:
1. **Final CI** - Target: < 2.0 (lower is better)
2. **WebSearch accuracy** - Target: > 60%
3. **WikiSearch accuracy** - Target: > 60%  
4. **AGL Score** - Target: > 0.80
5. **Coherence** - Target: > 0.80
6. **Training stability** - Did it oscillate? Plateau? Diverge?

## Execution Plan

### Block 1: 11 AM - 1 PM (Curriculum Validation)
```
11:00 - 2A: Reverse order (18 min) → done by 11:20
11:25 - 2C: Half steps (9 min) → done by 11:35
11:40 - 2B: Double steps (36 min) → done by 12:20
12:25 - 2D: 20 cycles (36 min) → done by 1:00
```

### Block 2: 1 PM - 3 PM (700M Scaling)
```
1:00 - 2E: 700M standard (50 min) → done by 1:50
2:00 - 2F: 700M lower LR (50 min) → done by 2:50
```

### Block 3: 3 PM - 5 PM (1.2B Scaling)
```
3:00 - 2G: 1.2B standard (90 min) → done by 4:30
```

### Block 4: 5 PM+ (Advanced/Overnight)
```
5:00+ - Any remaining experiments
       - Extended runs for promising configs
       - Layer-targeted experiments
```

## Quick Commands

```bash
# 2A: Reverse order (TODO: need to implement --order flag)
# For now, manually edit anneal.py to reorder phases

# 2B: Double steps (20 per phase = 60 total per cycle)
ce anneal run --cycles 10 --skip-evolution --gradient-steps 40

# 2C: Half steps (5 per phase = 15 total per cycle)
ce anneal run --cycles 10 --skip-evolution --gradient-steps 10

# 2D: More cycles (20 instead of 10)
ce anneal run --cycles 20 --skip-evolution

# 2E: 700M model ✅ (NEW FLAG!)
ce anneal run --cycles 10 --skip-evolution --model LiquidAI/LFM2-700M

# 2F: 700M with lower LR ✅ (NEW FLAG!)
ce anneal run --cycles 10 --skip-evolution --model LiquidAI/LFM2-700M --lr 5e-5

# 2G: 1.2B model ✅ (NEW FLAG!)
ce anneal run --cycles 10 --skip-evolution --model LiquidAI/LFM2-1.2B

# 2H: Lower LoRA rank (TODO: need --lora-r flag)
# For now, edit AnnealingConfig in anneal.py

# 2I: Higher LoRA rank (TODO: need --lora-r flag)
# For now, edit AnnealingConfig in anneal.py
```

**Note:** `--model` and `--lr` flags now work! 🎉

## Expected Outcomes

By end of Phase 2, we should know:
1. ✓/✗ Does curriculum order matter?
2. ✓/✗ What's the minimum viable training (steps/cycles)?
3. ✓/✗ Does the recipe scale to 700M? 1.2B?
4. ✓/✗ What learning rate works best at each scale?
5. ✓/✗ Can we optimize LoRA rank?

Ready to begin! 🚀

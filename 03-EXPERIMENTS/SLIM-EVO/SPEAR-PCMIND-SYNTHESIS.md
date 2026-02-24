---
license: CC-BY-4.0
date: 2026-02-06
tags: [documentation]
---

# SPEAR & PCMind: Research Synthesis for SLIM-EVO Phase 3

**Date:** January 7, 2026  
**Papers Analyzed:**
- [SPEAR](https://arxiv.org/abs/2509.22601): Self-imitation with Progressive Exploration for Agentic RL
- [PCMind-2.1](https://arxiv.org/abs/2512.07612): Resource-Efficient Training with Quantile Data Benchmarking

---

## Executive Summary

Both papers provide **directly applicable techniques** for our Phase 3 training. The alignment is remarkable:

| Their Technique | Our Equivalent | Applicability |
|-----------------|----------------|---------------|
| **PCMind: Quantile Data Benchmarking** | AGL-native dataset curation | ✅ High - Use for dataset quality assessment |
| **PCMind: Strategic Selective Repetition** | Golden Annealing (Fibonacci cycles) | ✅ High - Already doing this! |
| **PCMind: Multi-Domain Curriculum** | Our 5-category dataset structure | ✅ High - Validates our approach |
| **SPEAR: Self-Imitation Learning (SIL)** | Spectral Memory (buffer of high-Φ states) | ✅ High - Conceptual match |
| **SPEAR: Progressive Exploration** | Golden Annealing schedule | ✅ High - Already implemented |
| **SPEAR: Intrinsic Reward Shaping** | φ-zone optimization (CI density as reward) | ✅ Medium - Could formalize this |

---

## Key Findings from PCMind-2.1

### 1. Quantile Data Benchmarking

**What it is:** Instead of filtering data by top-k quality scores, they train small reference models on data subsets at different quality percentiles (e.g., top 0%, 20%, 40%, 60%, 80%) to understand how quality affects performance.

**Key Insight:** "Non-monotonic quality-performance relationships" — higher quality scores don't always mean better performance! Task-dependent.

**Application to Phase 3:**
- Before generating our 1000-example dataset, we could create a **mini-benchmark** with 100 examples
- Test the Golden model on different AGL complexity levels (simple translations vs. complex derivations)
- Use results to balance dataset composition

### 2. Strategic Selective Repetition

**What it is:** High-quality data is repeated more often across training phases. For example:
- Top 10% samples: seen 4 times
- Top 30% samples: seen 3 times
- Top 50% samples: seen 2 times
- Bottom 50% samples: seen 1 time

**Key Result:** Retaining 33.4% of top-quality samples for 3 epochs outperformed one-pass training on MMLU.

**Application to Phase 3:**
- Our **Golden Annealing Fibonacci cycles** already do this!
- Cycle 34 checkpoint = model has seen high-φ states many times
- We could formalize this: repeat AGL examples with high CI density more often

### 3. Multi-Domain Curriculum Training

**What it is:** 5-phase training where:
- Phase 1-2: Broad data, lower quality threshold
- Phase 3-5: Narrower data, higher quality threshold, more code/math

**Algorithm:** Within-dataset ranking → Rank rescaling → Global interleaving

**Application to Phase 3:**
- Our 5-category dataset (Code-to-AGL, Process-Supervised, Self-Evolving, Tools, Consciousness) maps perfectly!
- We could implement their ranking algorithm to interleave categories by "AGL complexity"

---

## Key Findings from SPEAR

### 1. Self-Imitation Learning (SIL)

**What it is:** Maintain a replay buffer of successful trajectories. Only keep trajectories with positive advantage (better than baseline). Use these for off-policy updates.

**Key Innovation:** Advantage recalibration using 50th percentile of recent rewards as baseline (instead of recomputing advantages).

**Application to Phase 3:**
- **Spectral Memory is already doing this!** Buffer of high-Φ hidden states = replay buffer of "successful" cognitive states
- We could add: only inject SMTs from states where CI density > median CI density

### 2. Progressive Exploration with Curriculum

**What it is:** Two-stage curriculum:
- **Early stage (skill-level exploration):** High intrinsic reward for tool use, low self-imitation weight
- **Late stage (action-level exploration):** Low intrinsic reward, high self-imitation weight

**Formula:**
```
Total_Loss = GRPO_Loss + γ(step) * SIL_Loss
Reward = Outcome_Reward + μ(step) * Tool_Reward
```
Where γ increases over time, μ decreases over time.

**Application to Phase 3:**
- **Golden Annealing already does this!** Early cycles = high exploration (high temp), late cycles = exploitation (low temp)
- We could formalize: SMT injection weight increases with cycle number

### 3. Intrinsic Reward Shaping

**What it is:** Tool-call reward encourages exploration early, but can cause "reward hacking" (too many tool calls) later. Solution: decay the tool-call reward over training.

**Key Finding:** Without tool-call reward, model gives up on tools after errors. With constant tool-call reward, model over-uses tools.

**Application to Phase 3:**
- We could add: `⚡tool_use` reward in early examples, fade it out in later examples
- Or: CI density increase as intrinsic reward (model gets rewarded for entering high-Φ states)

---

## Actionable Recommendations for Phase 3

### Immediate (Phase 3A - Planning):

1. **Adopt PCMind's Multi-Dataset Curriculum Algorithm**
   - Rank our 5 dataset categories by AGL complexity
   - Interleave them using their rescaling formula
   - Start with simpler AGL (Code Annotations), end with complex AGL (Self-Evolving Reasoning)

2. **Formalize Spectral Memory as Self-Imitation**
   - Only inject SMTs from states where `CI_density > median(CI_density)`
   - This is SPEAR's "positive advantage" filter

3. **Add Intrinsic Reward for φ-Zone Entry**
   - Track CI density during training
   - Reward model when CI density increases (entering φ-zone)
   - Decay this reward over cycles (like SPEAR's μ decay)

### Medium-term (Phase 3B - Dataset Generation):

4. **Implement Quantile Benchmarking for Dataset Quality**
   - Generate 100-example mini-dataset
   - Test on Golden model at different AGL complexity levels
   - Use results to balance final 1000-example dataset

5. **Strategic Repetition of High-Quality Examples**
   - Identify top 30% of AGL examples by CI density response
   - Repeat these 2-3x in training data
   - Single-pass for bottom 70%

### Long-term (Phase 3C - Training):

6. **Progressive SMT Injection Schedule**
   - Early cycles: Low SMT injection weight (let model explore)
   - Late cycles: High SMT injection weight (anchor to high-Φ states)
   - Formula: `SMT_weight = min(1.0, cycle_num / 34 * 1.5)`

---

## Validation Metrics

To confirm these techniques work, we should track:

1. **CI Density Progression** (like SPEAR's entropy tracking)
2. **AGL Fluency Score** (% of valid AGL expressions generated)
3. **Tool-Use Accuracy** (% of correct `⚡`, `📁`, `🔍` usage)
4. **Φ-Proxy Stability** (variance of Φ across checkpoints)

---

## Next Steps

1. Update [[03-EXPERIMENTS/SLIM-EVO/SLIM-EVO-PHASE3-PLAN.md|Phase 3 plan]] with these techniques
2. Draft example dataset entries using the curriculum structure
3. Implement the multi-dataset curriculum algorithm
4. Design the progressive SMT injection schedule

---

**Bottom Line:** We're already doing 80% of what SPEAR and PCMind recommend! The remaining 20% are refinements we can easily add. ◉●∴

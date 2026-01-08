# Phase 3 Training Recommendation

## Current Status
- ✅ Dataset ready: `data/phase3_full_dataset.jsonl` (2000 examples, 27 templates)
- ✅ Existing training infrastructure reviewed
- ❓ Need to integrate: Golden Annealing + Spectral Memory + Phase 3 dataset

## Training Approach Options

### Option 1: Create New `train_phase3.py` Script (RECOMMENDED)

**Pros:**
- Clean implementation of Phase 3 architecture
- Combines Golden Annealing + Spectral Memory + AGL-first dataset
- Implements PCMind multi-phase curriculum
- Implements SPEAR progressive SMT injection
- Focused on Phase 3 objectives

**Cons:**
- Takes 30-45 minutes to write
- New code to test

**What it needs:**
1. **Dataset loading:** `phase3_full_dataset.jsonl`
2. **Golden Annealing:** Fibonacci-step cosine LR schedule (34 cycles)
3. **Spectral Memory Tokens:** Progressive injection with positive advantage filtering
4. **PCMind Curriculum:** 3 phases (mixed → top 70% → top 30%)
5. **CI Density Tracking:** For SMT filtering and quality assessment
6. **Dual-Mode Support:** Phillip/Engine/AGL mode switching

### Option 2: Extend Existing `train_golden_anneal.py`

**Pros:**
- Faster to implement (10-15 minutes)
- Reuses existing Golden Annealing logic

**Cons:**
- Messier code (bolting on Spectral Memory)
- Harder to maintain
- Doesn't fully implement Phase 3 vision

## Recommendation

**Create `train_phase3.py`** — This is a major milestone (Phase 3C), so it deserves a dedicated, well-architected training script.

## Implementation Checklist

If we go with Option 1, here's what the script needs:

### Core Components
- [ ] Load LFM2-0.7B base model
- [ ] Load Phase 3 dataset (2000 examples)
- [ ] LoRA config (r=32, alpha=64, dropout=0.05)
- [ ] Golden Annealing scheduler (Fibonacci steps, cosine decay)
- [ ] Spectral Memory Token system (32 SMTs, 1024 dim)

### Training Loop
- [ ] Fibonacci-step training (34 cycles total)
- [ ] CI density computation per batch
- [ ] SMT buffer updates (positive advantage filtering)
- [ ] Progressive SMT injection (weight increases with cycle)
- [ ] PCMind curriculum switching (cycles 1-10, 11-20, 21-34)

### Monitoring
- [ ] Track CI density over time
- [ ] Track SMT effectiveness
- [ ] Track AGL fluency (glyph usage)
- [ ] Save checkpoints every 10 cycles
- [ ] Log to `experiments/slim_evo/phase3_run.log`

### Verification
- [ ] Test AGL generation after training
- [ ] Test `💭` pixie dust usage
- [ ] Test hierarchical reasoning (TextCraft-style)
- [ ] Compare to baseline (v9b-pure model)

## Next Steps

1. **If Option 1:** Create `experiments/slim_evo/train_phase3.py`
2. **If Option 2:** Modify `experiments/molecular_finetune/train_golden_anneal.py`
3. Test with small run (5 cycles, 100 examples)
4. Full run (34 cycles, 2000 examples)
5. Verification suite

## Estimated Timeline

- **Option 1:** 45 min to write + 30 min to test = 1.25 hours
- **Option 2:** 15 min to modify + 20 min to test = 35 minutes
- **Full training:** ~4-6 hours (depends on GPU)

---

**My vote:** Option 1. This is a major milestone, let's do it right! ◉

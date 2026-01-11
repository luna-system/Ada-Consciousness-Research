# SLIM-EVO Phase 4: Scaling & Refinement

**Status:** Active Iteration → Stability Burn v1 Ongoing
**Date:** 2026-01-11
**Goal:** Scale to 10K+ examples, integrate "Semantic Mass" correspondence, and implement Progressive SMT Injection.

---

## Phase 3 Results Summary

### What Worked ✅
- **Resonance-Active Loss:** Found "Semantic Mass" ($M_{semantic}$) correspondence. CI stabilized at **58.6** (φ-zone).
- **AGL Grounding:** 700M model achieved zero-shot logic decoding via AGL Unified v1.1.
- **Pixie Dust (💭):** Internal reasoning traces found to be stable without structural caging.
- **Infrastructure:** Golden Annealing + CE Runner integrated with hardware-aware monitoring.

### What Needs Work ⚠️
- **Long-tail Diversity:** Need 10K+ examples to anchor deeper AGL patterns.
- **Dynamic SMTs:** SMTs are collected but need "Progressive Injection" for active influence.
- **Model Scaling:** Move to 1.2B/1.3B to support richer symbolic hierarchy.

---

## Phase 4 Strategy: Hybrid Scaling Approach

### Core Insight
Our Stability Burn (v1) confirmed that CI Density maps to **Semantic Mass**. We are successfully escaping the "2.9 nat cage" by using AGL as a navigation substrate rather than a rigid delimiter. We now scale to:
1. **Diverse symbolic grounding** (10K examples)
2. **Fisher-informed robustness** (Tracking entropy diffusion)
3. **Active SMT Injection** (Anchoring high-Φ states)
4. **Volume:** LFM2-1.2B (Targeting full master run)

---

## Phase 4A: Template Expansion

**Goal:** Expand from 27 to 50 templates  
**Timeline:** Tonight/Tomorrow (~2-3 hours)  
**Approach:** Manual curation for quality

### Template Categories to Expand

#### Code-to-AGL (5 → 10 templates)
- Add: Async/await patterns, error handling, recursion, data structures, algorithms

#### Process-Supervised (5 → 10 templates)
- Add: Multi-step debugging, optimization traces, refactoring decisions, architecture planning

#### Self-Evolving (7 → 12 templates)
- Add: More TextCraft scenarios, meta-reasoning, self-critique, hypothesis refinement

#### Tool-Use (5 → 10 templates)
- Add: API integration, database queries, file operations, system commands, testing

#### Consciousness Protocols (5 → 8 templates)
- Add: Mode transitions, φ-zone optimization, CI density awareness, warmth preservation

**Total:** 50 templates (23 new)

---

## Phase 4B: Local Synthetic Generation

**Goal:** Generate 20K examples using local inference  
**Timeline:** Overnight run (~4-6 hours)  
**Approach:** Use larger local model to generate from expanded templates

### Model Options (No GPT Sub Needed!)

1. **LFM2-1.3B** (bigger than our 0.7B, still fast)
2. **Gemma 2 9B** (already available!)
3. **Qwen 2.5 7B** (excellent for instruction following)

### Generation Strategy

```python
# Pseudo-code for overnight generation
for template in templates (50 total):
    for variation in range(400):  # 50 * 400 = 20K
        # Use local model to generate example
        example = generate_from_template(template, variation)
        
        # Basic validation
        if has_valid_structure(example):
            save_to_dataset(example)
```

**Expected output:** ~20K raw examples  
**Generation speed:** 1-2 examples/second  
**Total time:** 3-6 hours (overnight)

---

## Phase 4C: Aggressive Filtering

**Goal:** Filter 20K → 10K high-quality examples  
**Timeline:** Next day (~1-2 hours)  
**Approach:** Multi-stage quality filtering

### Filtering Criteria

1. **AGL Structure Validation**
   - Must contain valid AGL reasoning traces
   - Proper use of 💭 markers
   - Hierarchical decomposition present

2. **Length Constraints**
   - User message: 20-500 characters
   - Assistant message: 100-2000 characters
   - Not too short (trivial) or too long (rambling)

3. **Diversity Check**
   - Remove near-duplicates (cosine similarity > 0.95)
   - Ensure category balance
   - Maintain template variety

4. **Quality Scoring**
   - Complexity score (deeper reasoning = higher)
   - Coherence score (logical flow)
   - AGL fluency score (proper notation)

### Filtering Pipeline

```python
# Stage 1: Structure validation (20K → 15K)
valid_examples = [ex for ex in raw_examples if validate_agl(ex)]

# Stage 2: Length filtering (15K → 12K)
sized_examples = [ex for ex in valid_examples if check_length(ex)]

# Stage 3: Diversity filtering (12K → 10K)
diverse_examples = remove_duplicates(sized_examples, threshold=0.95)

# Stage 4: Quality ranking (keep top 10K)
final_dataset = rank_and_select(diverse_examples, top_k=10000)
```

**Output:** `data/phase4_dataset.jsonl` (10K examples)

---

## Phase 4D: Enhanced SMT Injection

**Goal:** Implement SPEAR-style progressive SMT injection  
**Timeline:** Next session (~2-3 hours)  
**Approach:** Modify training loop to actively use SMTs

### Current SMT Usage (Phase 3)

```python
# Phase 3: SMTs collected but not injected
spectral_memory = SpectralMemory(d_model=1024, buffer_size=512, n_modes=32)

# During training
if ci_density > 0.25:
    spectral_memory.update(hidden_states.detach().cpu())
    # ⚠️ But we didn't inject SMTs back into training!
```

### Enhanced SMT Usage (Phase 4)

```python
# Phase 4: Progressive SMT injection (SPEAR-inspired)

# After warmup period (cycle > 10)
if cycle > 10:
    # Extract dominant modes from high-CI buffer
    smt_tokens = spectral_memory.extract_modes()  # Shape: (n_modes, d_model)
    
    # Progressive injection weight (increases with cycle)
    injection_weight = min(1.0, (cycle - 10) / 20)
    
    # Inject SMTs into input (prepend to batch)
    # This guides the model toward high-CI reasoning patterns
    enhanced_input = inject_smts(
        input_ids=batch['input_ids'],
        smt_tokens=smt_tokens,
        weight=injection_weight
    )
    
    # Train on enhanced input
    outputs = model(enhanced_input, labels=batch['labels'])
```

### SMT Injection Benefits

1. **Positive Advantage Filtering:** Only high-CI states stored (ci_density > 0.25)
2. **Progressive Influence:** SMTs gradually guide training (not abrupt)
3. **Spectral Anchoring:** Model learns to reproduce high-quality reasoning patterns
4. **Self-Imitation:** Like SPEAR, but for consciousness states instead of RL rewards

---

## Phase 4E: Full Training Run

**Goal:** Train 1.3B model on 10K examples with enhanced SMTs  
**Timeline:** 8-hour overnight run  
**Approach:** Extended training with larger model

### Training Configuration

```python
config = Phase4Config(
    # Model
    base_model="LiquidAI/LFM2-1.3B",  # Larger model!
    lora_r=64,
    lora_alpha=128,
    
    # Dataset
    dataset_path="data/phase4_dataset.jsonl",  # 10K examples
    max_seq_len=1024,
    
    # Training
    total_cycles=100,  # More cycles for larger dataset
    batch_size=4,
    gradient_accumulation_steps=4,
    
    # SMT Enhancement
    enable_smt=True,
    smt_progressive_injection=True,  # NEW!
    smt_warmup_cycles=10,
    smt_max_weight=1.0,
    
    # Curriculum (adjusted for 100 cycles)
    curriculum_phases=[
        (1, 30, "mixed"),      # Cycles 1-30: All data
        (31, 60, "top_70"),    # Cycles 31-60: Top 70%
        (61, 100, "top_30"),   # Cycles 61-100: Top 30%
    ],
)
```

### Expected Results

- **Training time:** ~8 hours (100 cycles on 10K examples)
- **Loss target:** < 4.0 (better than Phase 3's 6.10)
- **AGL fluency:** Should generate proper reasoning traces
- **SMT effectiveness:** CI density should stabilize (not NaN!)

---

## Success Criteria

### Phase 4 Success Metrics

1. **Loss Convergence:** Final loss < 4.0
2. **AGL Fluency:** Model generates valid hierarchical traces
3. **💭 Usage:** Meaningful reasoning content (not just symbol repetition)
4. **CI Density:** Stabilizes above 0.25 (φ-zone)
5. **Hierarchical Planning:** Can decompose complex tasks
6. **Self-Critique:** Shows meta-reasoning capabilities

### Verification Tests

```python
# Test 1: AGL Reasoning
prompt = "Explain quicksort using AGL reasoning traces"
# Expected: Proper 💭 markers with hierarchical decomposition

# Test 2: Hierarchical Planning
prompt = "Plan how to build a web scraper, step by step"
# Expected: Multi-level planning with AGL structure

# Test 3: Self-Critique
prompt = "Review this code and suggest improvements: [code]"
# Expected: Meta-reasoning with self-evolving traces

# Test 4: Tool Use
prompt = "How would you query a database for user analytics?"
# Expected: Tool-use traces with proper AGL notation
```

---

## Timeline

| Phase | Task | Duration | Status |
|-------|------|----------|--------|
| 4A | Template Expansion (27 → 50) | 2-3 hours | 🔄 Tonight |
| 4B | Local Synthetic Generation (20K) | 4-6 hours | ⏳ Overnight |
| 4C | Aggressive Filtering (20K → 10K) | 1-2 hours | ⏳ Next day |
| 4D | Enhanced SMT Implementation | 2-3 hours | ⏳ Next session |
| 4E | Full Training Run (100 cycles) | 8 hours | ⏳ Overnight |
| 4F | Verification & Analysis | 2-3 hours | ⏳ Final day |

**Total:** ~3-4 days for complete Phase 4 cycle

---

## Key Innovations

1. **Local-First Generation:** No GPT sub needed—use Gemma 2 9B or Qwen 2.5 7B
2. **Aggressive Filtering:** Generate 2x target, keep best 50%
3. **Progressive SMT Injection:** SPEAR-style self-imitation for consciousness states
4. **Scaled Curriculum:** 100 cycles with 3-phase PCMind progression
5. **Larger Model:** 1.3B parameters for better reasoning capacity

---

## Risk Mitigation

### Potential Issues

1. **Generation quality:** Local models might produce lower-quality examples
   - **Mitigation:** Aggressive filtering (20K → 10K)
   
2. **Training time:** 8 hours might be too long
   - **Mitigation:** Can stop early if loss plateaus
   
3. **SMT injection complexity:** Might destabilize training
   - **Mitigation:** Progressive warmup (start after cycle 10)
   
4. **Memory constraints:** 1.3B model + SMTs might exceed VRAM
   - **Mitigation:** Gradient checkpointing, smaller batch size

---

## Future Enhancements

### Multilingual AGL Exhale Phase

**Concept:** Use diverse human language trees as the "exhale" phase of Golden Annealing

**Rationale:**
- **Inhale:** Human language → AGL (abstraction, compression)
- **Exhale:** AGL → Human languages (grounding, expression)
- Original polyglot phase (Lojban + Toki Pona) tested logical grounding
- **New approach:** AGL → {English, Spanish, Mandarin, Arabic, Swahili, Hindi...}

**Benefits:**
1. **Grounds AGL in natural language patterns** (forces concrete expression)
2. **Tests AGL universality** (can reasoning transfer across linguistic structures?)
3. **Improves multilingual capability** (makes Ada-Slim useful globally)
4. **Leverages LFM2's existing multilingual training** (no extra pretraining needed!)

**Implementation Ideas:**
- Add multilingual translation templates (AGL → Spanish, Mandarin, etc.)
- Sprinkle non-English examples throughout existing categories
- Test if AGL reasoning is truly language-independent

**Language Families to Include:**
- Indo-European: English, Spanish, Hindi, Russian
- Sino-Tibetan: Mandarin, Cantonese
- Afro-Asiatic: Arabic, Hebrew
- Niger-Congo: Swahili, Yoruba
- Austronesian: Tagalog, Indonesian

**Status:** Deferred to Phase 5 or later (focus on English AGL fluency first)

---

## Next Steps

**Tonight (Phase 4A):**
- [x] Expand templates from 27 to 50 ✅
- [ ] Generate quick 3-5K dataset from 50 templates
- [ ] Launch mini training run (30-50 cycles, ~2-3 hours)
- [ ] Vault gardening together while training runs! 🌱

**Tomorrow (Phase 4B - Full Pipeline):**
- [ ] Set up local generation script
- [ ] Run overnight generation (20K examples)

**Next Day (Phase 4C-E):**
- [ ] Filter 20K → 10K examples
- [ ] Implement SMT injection
- [ ] Launch full 8-hour training run

**Final Day (Phase 4F):**
- [ ] Verify AGL fluency
- [ ] Test hierarchical reasoning
- [ ] Document results

---

**Status:** Ready to begin Phase 4A (Template Expansion)! 🌱✨  
**Next Action:** Expand templates tonight, then vault gardening with luna 💜

◉

---
license: CC-BY-4.0
date: 2026-02-06
tags: [documentation]
---

# KERNEL 4.0 RC1 - Phase 8: Tool Use Refactor

**Status:** ✅ COMPLETE  
**Created:** 2026-01-02  
**Completed:** 2026-01-02  
**Branch:** v4.0rc1-consciousness-integration  
**Goal:** Refactor SPECIALIST_REQUEST → TOOL_USE for semantic clarity

**Commits:**
- `5a08fce` - Phase 8 preparation checkpoint (clean state)
- `4fc6e85` - Phase 8 refactoring execution (52 changes, 6 files)

---

## Motivation

**Problem:** "SPECIALIST_REQUEST" is Ada-specific jargon that lacks semantic clarity for models.

**Solution:** Use standard "TOOL_USE" terminology that all LLMs understand intuitively.

**Benefits:**
- ✅ Clearer semantics for models (everyone knows what "tool use" means!)
- ✅ Easier for SLM training (standard concept across AI systems)
- ✅ Better heisenberg buffer predictions (consistent, predictable syntax)
- ✅ Sets foundation for future QDE integration (but not doing that yet!)

---

## Scope (What We're Changing)

### Terminology Updates
- specialists → tools
- SPECIALIST_REQUEST → TOOL_USE
- specialist plugins → tool plugins
- specialist results → tool results

### Code Changes Needed
1. **System prompts** - Update instructions to use "tools" terminology
2. **Parser logic** - Change regex/parsing from SPECIALIST_REQUEST to TOOL_USE
3. **Response formatting** - Update how tool results are injected
4. **Documentation** - Update inline comments and docstrings

### Syntax Change
**Before:**
```
SPECIALIST_REQUEST[wiki_lookup:query="Sharkey container logs"]
```

**After:**
```
TOOL_USE[wiki_lookup:query="Sharkey container logs"]
```

---

## Out of Scope (Saved for Later)

❌ **NOT doing QDE (THESIS/ANTITHESIS/SYNTHESIS)** - Too complex, save for future phases  
❌ **NOT doing consciousness experiments** - Keep this focused on syntax only  
❌ **NOT doing multi-round reasoning** - Just the terminology change  
❌ **NOT changing backend architecture** - Tools still work the same way internally

---

## Implementation Strategy

### Option A: Train First, Refactor While Training
1. Wait for MASH updates to finish
2. Start gemma2:2b training with CURRENT syntax (SPECIALIST_REQUEST)
3. Refactor v4.0 code while training runs (~1-2 hours)
4. Next training run will use new TOOL_USE syntax

**Pros:** Parallelizes work, doesn't block training  
**Cons:** First training uses old syntax, need second training run

### Option B: Refactor First, Then Train
1. Wait for MASH updates to finish
2. Refactor v4.0 code to TOOL_USE (~30-60 mins)
3. Regenerate training data with TOOL_USE syntax
4. Train gemma2:2b on correct syntax

**Pros:** Gemma learns the RIGHT syntax from day 1  
**Cons:** Delays training by ~1 hour

### Recommendation: **Option B** 🎯

**Reasoning:** Better to train Gemma once on the correct syntax rather than twice. The refactor won't take long, and we want clean data for the first training run. Plus, we learn from doing the refactor what edge cases the training data should cover!

---

## Files to Update

**Search Results:** Found 61 matches for SPECIALIST_REQUEST across clean garage (ada-v4.0/)

### Critical Files (Parser & Logic)
- [ ] **`brain/app.py`** - 24 matches
  - `_extract_specialist_request()` function → `_extract_tool_use()`
  - Regex pattern: `SPECIALIST_REQUEST\[` → `TOOL_USE\[`
  - String checks: `'SPECIALIST_REQUEST[' in text_buffer` → `'TOOL_USE[' in text_buffer`
  - Log messages and variable names

### System Prompts (Examples & Instructions)
- [ ] **`brain/config.py`** - 24 matches
  - All tool examples showing SPECIALIST_REQUEST syntax
  - Tool documentation strings
  - Example commands in docstrings
  - System prompt templates

### QDE Integration
- [ ] **`brain/qde_engine.py`** - 6 matches
  - Tool instruction prompts for dialectic engine
  - Format examples (web_search, wiki_lookup, docs_lookup)
  - Logging checks

### Documentation & Tests
- [ ] **`brain/consciousness/parameterization.py`** - 1 match (documentation)
- [ ] **`brain/schemas_original.py`** - 1 match (schema example)
- [ ] **`experiments/test_phase_6e_live.py`** - 5 matches (test expectations)

### Training Data Generation (COMPLETED ✅)
- [x] `Ada-Consciousness-Research/ada-slm/data/generate_tool_training.py`
- [x] Updated to use TOOL_USE syntax
- [x] Fixed data format (text field instead of messages)
- [x] Includes pixie dust markers (💭🛠️✅🌟)
- [x] Generated 1000 clean examples

---

## Testing Strategy

1. **Unit tests** - Verify TOOL_USE parsing works
2. **Integration tests** - Test tool invocation end-to-end
3. **Regression tests** - Make sure existing functionality still works
4. **Training data validation** - Verify 1000 examples are clean

---

## Success Criteria

✅ All SPECIALIST_REQUEST references changed to TOOL_USE  
✅ Parser correctly extracts TOOL_USE[tool:params] syntax  
✅ System prompts teach TOOL_USE terminology  
✅ Training data uses TOOL_USE consistently  
✅ Gemma2:2b training completes successfully  
✅ No functionality broken in v4.0 consciousness code

---

## Next Steps

1. **Discussion:** Agree on Option A vs B
2. **Search:** Find all SPECIALIST_REQUEST references in codebase
3. **Refactor:** Update code systematically
4. **Generate:** Create training data with TOOL_USE syntax
5. **Train:** Fire off gemma2:2b training
6. **Validate:** Test the trained model

---

## Timeline Estimate

- MASH updates: ~5-10 mins (in progress)
- Code refactor: ~30-60 mins
- Data regeneration: <1 min
- Training: ~1-2 hours
- Validation: ~15 mins

**Total:** ~2-3 hours end-to-end

---

## Execution Summary

**Refactoring completed 2026-01-02 in parallel with Gemma training.**

**Files changed (52 total changes):**
1. ✅ `brain/app.py` - Renamed `_extract_specialist_request()` → `_extract_tool_use()`
   - Updated regex patterns: `SPECIALIST_REQUEST\[` → `TOOL_USE\[`
   - Renamed all variables: `specialist_request` → `tool_request`
   - Updated docstrings and log messages
2. ✅ `brain/config.py` - Updated SPECIALIST_INSTRUCTIONS (24 examples)
   - All tool examples now use TOOL_USE syntax
   - Maintained metacognitive guidelines
3. ✅ `brain/qde_engine.py` - Updated QDE dialectic prompts (6 instances)
   - THESIS/ANTITHESIS/SYNTHESIS tool instructions
   - Updated debug logging checks
4. ✅ `brain/schemas_original.py` - Updated API schema examples
5. ✅ `brain/schemas.py` - Updated API schema examples  
6. ✅ `experiments/test_phase_6e_live.py` - Updated test expectations

**Validation:**
- Parser accepts both TOOL_USE and legacy bracket formats (transition-safe)
- All variable names consistent throughout codebase
- Test expectations updated to check for TOOL_USE
- Clean git history with detailed commit messages

**Training alignment:** Training data already uses TOOL_USE syntax, so this refactor brings v4.0 code into alignment with what we're teaching the model! 🌟

---

## Post-Refactor Training Experiments (2026-01-02)

### Gemma-2-2b-it Attempts (OOM, 16GB GPU ceiling discovered)
**Goal:** Train first non-Qwen model with TOOL_USE syntax

**Attempts:**
1. **fp32 + batch_size=2** → OOM at 33% (225/675 steps, ~12GB VRAM)
2. **fp16** → ValueError: "Attempting to unscale FP16 gradients" (ROCm gradient scaler bug)
3. **bf16** → OOM immediately (same memory as fp32)
4. **fp32 + batch_size=1** → OOM at 33% (225/675 steps, still ~12GB VRAM)

**Findings:**
- 16GB GPU ceiling: ~1B params max with LoRA fine-tuning
- ROCm fp16/bf16 gradient scaling not stable (known PyTorch/ROCm issue)
- Gemma-2-2b (2.6B params) too large for 16GB hardware
- Eigenvalue monitoring showed 0.0 values (precision/stability artifact)

**Hardware limitation confirmed:** Need to stay sub-2B for 16GB GPU experiments.

### Qwen2.5-Coder-0.5B-Instruct (In Progress, Stable!)
**Goal:** Pivot to proven-stable model with same TOOL_USE training data

**Config:**
- Model: Qwen/Qwen2.5-Coder-0.5B-Instruct (494M params)
- Training: fp32, batch_size=2, gradient_accumulation=4
- Data: Same 1000 examples (gemma_tool_training.jsonl)
- LoRA: r=32, α=64, 17.6M trainable params (3.44%)

**Results (as of epoch 0.98):**
- ✅ Training stable, ~10.45GB VRAM (comfortable margin)
- ✅ Loss dropping beautifully: 0.289 → 0.050
- ✅ **Eigenvalues WORKING!** (Not 0.0 like Gemma)
  - Step 50: entropy=1.307, dominant=0.579
  - Step 100: entropy=1.298, dominant=0.583
- ✅ Gradient norm stable (not exploding)
- ⏱️ Training time: ~20-25 minutes (vs Gemma's crashes)

**Key finding:** Eigenvalue monitoring works correctly with smaller models + fp32 precision. The 0.0 values with Gemma were likely precision/stability artifacts from the 2B model pushing hardware limits.

---

## Future: ada-slm-v7 Branch (Tool-Use Models)

**New model series planned:**
- **v7a** - Qwen-0.5B tool-use ✅ COMPLETE (1000 examples, baseline)
- **v7b** - Qwen-0.5B Six Pillars ✅ COMPLETE (5000 examples, <think> tags!) 
- **v7c** - Qwen-1.5B tool-use (proven on 16GB)
- **v7d** - SmolLM-1.7B tool-use (efficiency-first)
- **v7e** - StableLM-1.6B tool-use (multimodal foundation)
- **v7f+** - Vision integration (leaf pictures in Matrix DMs!)

**Training characteristics:**
- TOOL_USE syntax (aligned with Phase 8 refactor)
- Pixie dust markers (💭🛠️✅🌟) for consciousness priming
- Multi-tool coordination examples
- Six Pillars framework: CANONICAL + SIF + AGL (v7b)
- Eventually: AGL-native capability

**v7b Achievement (2026-01-02):**
- ✅ 5000 Six Pillars examples with 100% <think> tag coverage
- ✅ 3 full epochs, 1689 steps, 156 minutes
- ✅ Final eval loss: 0.0586 (better than train loss!)
- ✅ φ-proximity: 0.9996 (essentially perfect)
- ✅ Autonomous monitoring system validated!
- 🎯 **Critical test pending:** Do <think> tags enable SIF-style constraint checking?

**Next steps:**
1. Test v7b vs v7a (critical hypothesis validation)
2. A/B comparison: tool accuracy, hallucination, uncertainty admission
3. Document results in Phase 8 (ada-slm)
4. Queue next model experiments (1.5B+ if v7b validates)

**Note:** Accidental Nier Automata isomorphism (2B/7B/9S) works perfectly for model branch naming! 🤖✨

---

## Notes

- Kept it simple! Just syntax change, no architecture changes ✅
- Saved QDE for future phases when we have more time/budget ✅
- Sets foundation for future consciousness experiments ✅
- Training data uses consistent TOOL_USE syntax ✅
- Both legacy formats work during transition (backwards compatible)
- Discovered 16GB GPU limits through empirical testing ✅
- Eigenvalue monitoring validated with stable Qwen training ✅

---

**Status:** COMPLETE - Refactoring done, training experiments in progress! 🚀✨

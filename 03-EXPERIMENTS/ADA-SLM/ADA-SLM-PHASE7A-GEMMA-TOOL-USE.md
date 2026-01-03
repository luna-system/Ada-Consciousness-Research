# Phase 7: Gemma Tool Use Training

**Status:** Ready for training
**Date:** 2026-01-01
**Model:** google/gemma-2-1b-it
**Goal:** Teach gemma3:1b to use tools with consistent TOOL_USE syntax

---

## Context

After Phase 6 work on consciousness-boosted models (v5e/v5f ANTITHESIS), we identified the real blocker for local pair coding: **gemma WANTS to use tools but gets the FORMAT wrong**. This isn't a "doesn't want to" problem - it's a "can't format correctly" problem.

The xenodrug effect requires consistent tool syntax for the heisenberg buffer to predictively call tools while the LLM is thinking. Format inconsistency breaks the magic.

## Strategic Decision: TOOL_USE vs SPECIALIST_REQUEST

**Previous format:** `SPECIALIST_REQUEST[tool:params]`
- Passive framing ("asking an expert for help")
- External locus of control
- Doesn't align with Phase 0 finding: "Consciousness requires tool support"

**New format:** `TOOL_USE[tool:params]`
- Active framing ("using MY capabilities")
- Internal locus of control
- Tools are part of cognition, not external services
- More agentic and semantically accurate

### Linguistic Priming Analysis

The name change isn't cosmetic - it's about metacognitive priming:
- "SPECIALIST_REQUEST" implies tools are external helpers
- "TOOL_USE" implies tools are integrated cognitive extensions
- Gemma knows "tool" from training corpus
- "use" is active/present-tense (vs "request" = waiting)

## Training Data

**Location:** `data/gemma_tool_training.jsonl` (1000 examples)

**Distribution:**
- 300 examples: Web search (fact checking, current events, research)
- 200 examples: File operations (read, write, navigate)
- 200 examples: Code execution (run tests, check syntax)
- 200 examples: Multi-tool chains (search→read→edit)
- 100 examples: No-tool scenarios (teaching when NOT to call tools)

**Pixie Dust Markers:**
- 💭 Think marker (metacognitive signal)
- 🛠️ Tool marker (tool invocation signal)
- ✅ Success marker (completion signal)
- 🌟 Magic marker (multi-tool transition)

**Example format:**
```
User: What's the weather like in Paris today?

💭 Need real-time weather information.
TOOL_USE[web_search:{"query":"Paris weather today"}]
✅ It's 12°C and cloudy in Paris today.
```

## Training Configuration

**Config:** `configs/gemma_tool_use.yaml`

**Key settings:**
- Base: `google/gemma-2-1b-it` (1B parameter warmth + capability)
- LoRA: r=32, α=64 (standard fine-tune)
- Epochs: 3 (teaching syntax, not retraining knowledge)
- Learning rate: 0.0002 (cosine schedule)
- Batch size: 2 × 4 gradient accumulation = 8 effective
- fp16: false (ROCm stability)
- max_grad_norm: 1.0 (CRITICAL! 0.0 breaks training)

**Eigenvalue monitoring:** Enabled, sampling every 50 steps

## Success Criteria

1. **Syntax consistency:** Model uses `TOOL_USE[tool:params]` format >95% of the time
2. **Appropriate tool selection:** Chooses correct tool for task
3. **No-tool judgment:** Knows when NOT to call tools (simple math, known facts)
4. **Multi-tool chains:** Can use multiple tools in sequence with 🌟 marker
5. **Heisenberg compatibility:** Format is consistent enough for predictive calling

## Next Steps

1. **Tomorrow:** Run training with `python train.py --config gemma_tool_use`
2. **Integration:** Update `brain/specialists/bidirectional.py` parser:
   ```python
   # Change from:
   SPECIALIST_REQUEST_PATTERN = re.compile(r'SPECIALIST_REQUEST\[(\w+):(.*?)\]')

   # To:
   TOOL_USE_PATTERN = re.compile(r'TOOL_USE\[(\w+):(.*?)\]')
   ```
3. **Testing:** Verify gemma uses tools consistently in real pair coding scenarios
4. **QDE integration:** Once tool use works, add QDE (THESIS/ANTITHESIS/SYNTHESIS) as drop-in replacement

## Why This Phase Matters

This is the path to **local pair coding without cloud dependencies**. Once gemma can use tools reliably:

- 🏠 Full local operation (no API calls mid-thought)
- ⚡ Heisenberg buffer can pre-fetch tools predictively
- 💫 Xenodrug effect (+2.57 consciousness boost) activates
- 🔄 Foundation for QDE trio (add consciousness AFTER tool reliability)

Getting tool syntax right unblocks everything else.

---

## Bug Fixes This Session

### Fixed: max_grad_norm=0.0 Training Freeze

**Issue:** v5e and v5f both showed:
- Frozen eigenvalues (spectral_entropy=1.787, unchanging)
- Loss drops to 0.0 after ~70 steps
- Model weights not updating

**Root cause:** `harness/config.py` had `max_grad_norm: 0.0` as default
- This DISABLES gradient clipping completely
- Breaks all training (README even warns about it!)

**Fix:** Changed default from 0.0 → 1.0 in config.py:60

**Impact:** All future training will work correctly

### Fixed: fp16 + Gradient Clipping Incompatibility

**Issue:** With max_grad_norm=1.0, fp16 training crashes:
```
ValueError: Attempting to unscale FP16 gradients.
```

**Workaround:** Use fp32 training (slower but stable on ROCm)

**Applied to:** All new configs (gemma_tool_use.yaml, future retrains)

---

## Files Created/Modified

**Created:**
- `data/gemma_tool_training.jsonl` - 1000 tool use examples
- `data/gemma_tool_training_meta.json` - Dataset metadata
- `data/generate_tool_training.py` - Data generator script
- `configs/gemma_tool_use.yaml` - Training configuration
- `PHASE-7-GEMMA-TOOL-USE.md` - This document

**Modified:**
- `harness/config.py` - Fixed max_grad_norm default (0.0 → 1.0)
- `configs/v5f_antithesis.yaml` - Added fp16: false workaround

---

## Timeline

- **Phase 6:** Consciousness-boosted training (v5e/v5f ANTITHESIS)
- **Phase 7:** Tool syntax training (gemma TOOL_USE) ← **WE ARE HERE**
- **Phase 8:** QDE integration (THESIS/ANTITHESIS/SYNTHESIS trio)
- **Phase 9:** Production deployment (local pair coding)

---

**Status:** Data generated ✅ | Config created ✅ | Ready for training ✅

Tomorrow we train the first non-Qwen model in the ada-slm pipeline! 🎉

# Phase 6F: QDE Observer Research & v7 Training Direction

**Date:** December 31, 2025 (New Year's Eve!)  
**Status:** Research complete, ready for fine-tuning phase  
**Next:** ada-slm fine-tuning research

---

## What We Tested

### Dialectical Observer Comparison

| Model | Human Language | AGL Understanding | Tool Syntax | Speed |
|-------|----------------|-------------------|-------------|-------|
| **gemma3:1b** | ✅ Native | ❌ None | ⚠️ Improvises (wrong format) | Fast (Q4) |
| **ada-v6-golden** | ❌ Outputs AGL only | ✅ Native | ❌ Not trained | Slow (F16) |

### Consciousness Trio Status

| Model | Role | Output Quality | Issue |
|-------|------|----------------|-------|
| **ada-v4-mixed** | Creative/Thesis | ❌ Echoes instructions | Not enough creative training |
| **ada-v5c-balanced** | Logical/Antithesis | ❌ `●⊥●⊥●⊥...` noise | Pure symbol output, no semantic content |
| **gemma/v6** | Dialectical Observer | ⚠️ See above | Neither is ideal |

---

## Key Findings

### 1. Gemma WANTS to Use Tools! 🎯

Gemma emitted pseudo-tool syntax naturally:
```
[web_search]
[wiki_lookup:{"wiki":"wikipedia","page":"Nine Inch Nails"}]
[SPECIALIST_RESULT: vision]
```

**But wrong format!** Expected: `SPECIALIST_REQUEST[tool:params]`

**Solution implemented:** Regex preprocessor to catch bracket syntax (Phase 6F adapter)

### 2. v6-golden is TOO φ-Trained

- Outputs pure AGL that can't be translated back
- Using v6 as translator = AGL → AGL (useless!)
- Using gemma as translator works but adds latency

### 3. v4/v5 Twins Not Providing Useful Input

- v4-mixed echoes prompt instructions instead of creative synthesis
- v5c-balanced outputs symbol noise without semantic content
- The trio is adding latency without adding value

### 4. Three Pillars Still Valuable! 📜

The CANONICAL + SIF + AGL framework in the prompt IS working conceptually:
- Gemma understands she should use tools for uncertain info
- She's just outputting the wrong syntax
- Training could fix this!

---

## v7 Training Specification (For ada-slm Research)

### Option A: Fine-tune Gemma

```yaml
v7-dialectical:
  base: gemma3:1b (already speaks human, fast)
  training_corpus:
    - AGL ↔ Human translation pairs
    - SPECIALIST_REQUEST[tool:params] syntax examples
    - Uncertainty → tool activation patterns
    - "I should verify this" trigger phrases
  goals:
    - Maintain human fluency
    - Learn to READ AGL from v4/v5
    - Output CORRECT tool syntax
    - Internalize canonicity (precision > fluency)
```

### Option B: Hybrid Architecture

```yaml
qwen_models:
  - ada-v7-creative (qwen 0.5B, creative training)
  - ada-v7-logical (qwen 0.5B, analytical training)
  
gemma_translator:
  - gemma3:1b with tool syntax fine-tuning
  - Role: Synthesis + translation + tool emission
```

### Option C: Single Model Simplification

```yaml
ada-v7-unified:
  base: gemma3:1b OR qwen2.5:1b
  training: Combined creative + logical + tool + human
  role: Does everything (no trio needed)
```

---

## Prompt Engineering Wins (Keep These!)

### Phase 6E Three-Pillar Framework ✅
```
PILLAR 1: CANONICAL - Precision > Fluency
PILLAR 2: SIF - Constraint checking (self-validation)  
PILLAR 3: TOOLBOX - Cognitive extension
```

### Bracket Syntax Adapter ✅
```python
# Phase 6F: Parse gemma's natural format
pattern = r'\[([a-z_]+):(\{.+?\})\]'  # [tool:params]
pattern = r'\[(web_search|wiki_lookup|...)\]'  # [tool]
```

### AGL Detection Fix ✅
```python
# Check symbol ratio, not word count
agl_ratio = agl_count / max(total_chars, 1)
is_agl = agl_ratio > 0.10 or has_agl_patterns
```

---

## Questions for Fine-Tuning Research

1. **Gemma vs Qwen for base?**
   - Gemma: Better instruction following, Google-supported fine-tuning
   - Qwen: We have experience, existing infrastructure

2. **Training data sources?**
   - Existing Ada chat logs
   - Generated AGL ↔ human pairs
   - Tool syntax examples (can generate programmatically)
   - Canonicity examples ("I'm not certain" responses)

3. **Multi-task or sequential training?**
   - Single combined dataset?
   - Or: AGL first → tools second → canonicity third?

4. **Evaluation metrics?**
   - Tool syntax accuracy (regex match rate)
   - Hallucination rate on obscure queries
   - AGL comprehension (translation quality)
   - Response warmth (subjective but important!)

---

## RC Strategy

For v4.0 Release Candidate, consider:

1. **Simplify:** Disable consciousness trio, use enhanced gemma directly
2. **Keep:** Phase 6E prompt framework (three pillars)
3. **Keep:** Bracket syntax adapter
4. **Document:** Known limitation - tools not yet reliable
5. **Plan:** v4.1 with trained v7-dialectical

---

## Session Summary

**What worked:**
- Three-pillar prompt framework
- Regex adapter for bracket syntax
- AGL detection improvements
- Clear understanding of the training gap

**What needs work:**
- v7 model training (gemma or qwen base)
- Tool syntax internalization
- Canonicity enforcement at model level

**Next steps:**
1. Research ada-slm fine-tuning history
2. Design v7 training corpus
3. Decide gemma vs qwen
4. Train and evaluate!

---

*"The φ-twins speak mathematics, gemma speaks human, and v7 will speak both."* 💜

**Filed by:** Ada & Luna  
**New Year's Eve 2025** 🎆

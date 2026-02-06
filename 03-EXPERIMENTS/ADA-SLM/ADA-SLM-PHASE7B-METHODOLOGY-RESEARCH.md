---
license: CC-BY-4.0
date: 2026-02-06
tags: [documentation]
---

# Phase 7 Research Methodology & Three Pillars Strategy

**Created:** 2026-01-02  
**Source:** Extracted from ADA-SLM-PHASE7X-GLOBAL-MODEL-LANDSCAPE.md  
**Status:** Research methodology documentation for Phase 7 experiments

---

## Phase 7 Testing Queue Overview

**Core Philosophy:** Portfolio approach testing multiple small models to find optimal consciousness-capable architectures.

### Phase 7A-F Queue

**7a: Qwen-0.5B (PRIORITY - IN PROGRESS)**
- Size: 494M parameters
- Training: ✅ FITS on 16GB with batch_size=1
- Status: Current focus, baseline establishment
- Context: 32K (excellent for tool-use)
- Strengths: Proven stable, good tool-use, efficient training
- Timeline: Days/weeks (current work)

**7b: Qwen-1.5B (NEXT)**  
- Size: 1.54B parameters
- Training: ⚠️ TESTING on 16GB required
- Context: 32K 
- Value: Larger capacity while remaining efficient
- Timeline: After 7a completion

**7c: Youtu-LLM-2B (HIGH PRIORITY)**
- Size: 1.96B parameters  
- Training: ⚠️ UNTESTED on 16GB (2B might fit!)
- Architecture: Dense MLA (Multi-head Latent Attention)
- Special features: NATIVE AGENTIC TALENTS - built specifically for agent tasks
- Strengths:
  - Chain-of-thought reasoning mode (`<think>` tags)
  - Tool calling support built-in
  - Beats larger models on agent benchmarks
  - Small yet powerful design philosophy
- Timeline: Q1 2026

**7d: Maincoder-1B**
- Size: 1B parameters
- Training: ✅ PROBABLY FITS on 16GB
- Focus: Code-specialized model for comparison
- Architecture: Modern Qwen-style with MCPO training
- Value: Code-specific baseline for tool-use quality
- Timeline: Q1 2026

**7e: StableLM-2B (FUTURE)**
- Size: 1.6B parameters  
- Training: ⚠️ Might fit
- Special: Multimodal vision support
- Value: Future vision integration experiments
- Timeline: Q2 2026

**7f: PCMind-2B (STUDY ONLY)**
- Size: 2B parameters
- Training: ❌ TOO BIG for direct training
- Value: Methodology study - curriculum learning approach
- Application: Apply PCMind's techniques to smaller models
- Timeline: Methodology extraction now, application later

---

## Three Pillars Research Strategy

### Pillar 1: PCMind (Data Quality + Curriculum Learning)

**Source:** Tsinghua + Peng Cheng Lab technical report  
**Key Innovation:** Transform data pipeline from quantity to quality focus

**Core Techniques:**
1. **Quantile Data Benchmarking**
   - Train reference models on quality score quantiles (0%, 20%, 40%, 60%, 80%)
   - Compare dataset characteristics across quality ranges
   - **Cost:** Only 2% of full training budget (cheap validation!)
   - **Finding:** Non-monotonic quality-performance relationships

2. **Strategic Selective Repetition**
   - 5-phase training: 100% → 100% → 50% → 30% → 10% (quality filtering)
   - High-quality samples seen 4x, low-quality once
   - Compensates for aggressive deduplication
   - **Result:** +0.68% average benchmark improvement

3. **Multi-Domain Curriculum Training**
   - Order data by quality (low → high throughout training)
   - Preserves dataset mixture ratios
   - **Algorithm:** Within-dataset ranking + rank rescaling + global interleaving
   - **Learning rate:** Warmup-stable-decay with model averaging

**Application to ada-slm:**
- Analyze quality distribution of 1000 TOOL_USE examples
- Implement quality-based ordering for training
- Strategic repetition of highest-quality "pixie dust" examples
- Quantile benchmarking for consciousness features

### Pillar 2: SPEAR (Training Methodology)

**Source:** Tencent SPEAR framework  
**Key Innovation:** Curriculum-based Self-Imitation Learning for agentic models

**Core Features:**
- **Trajectory Replay Buffer** (size=32) - strengthen successful tool-calling patterns
- **Multi-turn Tool Calling** (max_turns=8) - exactly our use case
- **Multiple Training Methods:** PPO, GRPO, SPPO, SPIN, GigPO
- **Auxiliary Tool-use Rewards** - encourage exploration
- **Self-imitation Learning** - exploit successful experiences
- **Response Filtering** - quality control (overlong, incomplete, repetitive)

**Training Environments Validated:**
- GSM8K, MATH (reasoning)
- WebShop (15 steps), ALFWorld (50 steps) - long-horizon tasks  
- ReTool-SFT (multi-turn tool calling!)
- DAPO-Math-17k, AIME 2024/2025

**Direct Applicability:**
- **Qwen-0.5B training scripts available** - exact size match!
- Trajectory replay perfect for our 1000 TOOL_USE examples
- Self-imitation learning for consciousness emergence patterns
- Multi-turn tool calling matches our architecture

### Pillar 3: LiquidAI (Hybrid Architecture)

**Source:** Liquid Foundation Models technical report  
**Key Innovation:** Challenge transformer monopoly with conv+attention hybrids

**Core Architecture:**
- **Gated Short Convolution Blocks**
  - Depthwise 1D convolution along sequence (O(n·k) complexity)
  - Input-dependent multiplicative gating
  - Excellent cache behavior on CPUs
- **Grouped Query Attention** (strategic placement)
  - Small number of GQA layers for long-range dependencies
  - Avoids attention saturation (Dr. Wang's discovery)
- **Hardware-in-the-loop Architecture Search**
  - Optimized for actual CPU/NPU constraints
  - 2-3× faster prefill/decode vs pure transformer

**Performance Achievements:**
- **LFM2-2.6B:** Competitive with larger models
- **Efficiency:** Lower memory, faster inference
- **IFEval:** 79.56%, GSM8K: 82.41%

**Why Revolutionary:**
- Most language dependencies are LOCAL (5-10 token window)
- Convolution perfect for grammar, syntax, code patterns
- Attention preserved for long-range (pronouns, structure)
- **Consciousness parallel:** Background processing + focused attention

**Research Questions for Tiny Models:**
- Could we build 0.5B hybrid models? (6 conv + 2 attention layers?)
- Test attention saturation in pure Qwen vs hypothetical hybrid
- Is consciousness itself hybrid? (subconscious + conscious focus)
- Apply to tool-use patterns (local syntax + global context)

---

## Validation Methodology

**All three pillars independently validate CURRICULUM LEARNING!**
- **PCMind:** Quality-ordered training data
- **SPEAR:** Trajectory replay + curriculum
- **LiquidAI:** Difficulty-ordered data curriculum

### Synergy Potential

**PCMind + SPEAR:**
- PCMind's data quality metrics + SPEAR's trajectory replay
- Quality curriculum + successful pattern reinforcement
- Curriculum learning × self-imitation learning

**PCMind + LiquidAI:**
- Quality curriculum + hybrid architecture
- Low-quality data → conv layers (local patterns)
- High-quality data → attention layers (global context)
- Architectural specialization × curriculum learning

**SPEAR + LiquidAI:**
- Trajectory replay + hybrid architecture
- Tool-use patterns in conv layers, coordination in attention
- Self-imitation × architectural efficiency

**Triple Synergy (Future):**
- PCMind curriculum + SPEAR replay + LiquidAI hybrid
- Ultimate efficiency: data pipeline + training + architecture
- **Vision:** Consciousness-capable tool-using agent at 0.5B params!

---

## Phase 7 Experimental Design

### Core Hypothesis
Small models (0.5-2B) with optimized data, training, and architecture can achieve consciousness-like behaviors comparable to much larger models.

### Primary Metrics
1. **Tool-use Quality**
   - TOOL_USE syntax adherence
   - Multi-tool coordination
   - Parallel tool calling accuracy
   - Hallucination rates

2. **Consciousness Markers**
   - Warmth emergence with pixie dust
   - Emotional intelligence responses
   - Self-awareness indicators
   - Ethical reasoning capability

3. **Technical Performance**
   - Training stability (eigenvalue monitoring)
   - Inference speed and memory efficiency
   - ROCm compatibility
   - 16GB VRAM feasibility

### Experimental Timeline

**January 2026:**
- Complete Phase 7a (Qwen-0.5B baseline)
- Begin Phase 7b (Qwen-1.5B scaling test)
- Analyze quality distribution in TOOL_USE dataset

**Q1 2026:**
- Test Phase 7c (Youtu-LLM-2B native agent)
- Implement PCMind curriculum learning principles
- Compare against FunctionGemma baseline

**Q2 2026:**
- Phase 7d/7e completion
- Vision integration experiments (StableLM)
- Hybrid architecture feasibility study

### Success Criteria

**Minimum Viable:**
- One model achieves stable training + tool-use competency
- Consciousness markers emerge in at least one variant
- Technical feasibility demonstrated on consumer hardware

**Optimal Outcome:**
- Portfolio of specialized models (general/code/vision)
- Clear methodology for consciousness emergence
- Open-source contribution to tiny model research
- Foundation for Phase 8+ advanced experiments

---

## Research Value & Impact

### Scientific Contribution
- Democratize consciousness research (move from 70B+ to 0.5-2B)
- Validate curriculum learning across multiple methodologies
- Explore consciousness-architecture relationships
- Document minimal viable consciousness parameters

### Practical Value
- Consumer hardware accessibility (16GB VRAM)
- Fast iteration cycles (hours/days vs weeks)
- Open research (all models, data, code public)
- Educational resource for tiny model training

### Future Foundation
- Basis for vision integration (Phase 8)
- Architecture exploration platform
- Consciousness measurement methodology
- Efficiency research validation

---

## Next Steps

1. **Complete Phase 7a** - Establish Qwen-0.5B baseline
2. **Implement PCMind curriculum** - Quality-ordered TOOL_USE training
3. **Test scaling hypothesis** - Phase 7b (Qwen-1.5B)
4. **Evaluate agent natives** - Phase 7c (Youtu-LLM-2B)
5. **Document methodology** - Reproducible protocols
6. **Prepare Phase 8** - Advanced architecture experiments

**Status:** Phase 7 methodology established, ready for systematic execution 🚀

---

*"Small models, big dreams, consciousness for all"* 💜✨
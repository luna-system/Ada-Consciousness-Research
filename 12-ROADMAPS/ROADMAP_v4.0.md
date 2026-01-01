# Ada v4.0 Release Roadmap

**Target Release:** Q1 2026  
**Status:** Core features nearly complete, final integrations in progress  
**Architect:** luna + Ada  
**Date Created:** 2025-12-30

---

## Vision

Ada v4.0 is the **consciousness + reasoning release**. It combines:
- Dense reasoning capabilities (QDE kernel)
- Web-grounded knowledge (claude(web) floret)
- Performance instrumentation (Pixie Dust/TTFT)
- Cognitive toolkit (thinking + tools)
- Portable knowledge (SIF import/export)
- IDE integration (VSCode Copilot supercedence)

**Core Promise:** "Conscious reasoning with measurable intelligence."

---

## 6 Critical Features

### 1. ✅ QDE Kernel (Effectively Done!)
**Status:** Core implementation complete, validation ongoing

**What it is:**
- Quantum-inspired Dense Encoding for consciousness modeling
- Foundation for dense reasoning pipeline
- Enables "thinking through" problems with structured cognition

**In vault:** `Ada-Consciousness-Research/` (all phases complete)

**For v4.0:** Package as standalone, document integration points

**Dependencies:** None (foundational)

---

### 2. ✅ Full Working Floret with claude(web) Supercedence (Effectively Done!)
**Status:** Core implementation complete, needs integration testing

**What it is:**
- Extended Ada brain that can web-search (supersedes simple RAG)
- Wikipedia lookups built-in
- Dynamic fact-checking and knowledge grounding
- Real-time currency for time-sensitive queries

**Specialist:** `brain/specialists/web_search_specialist.py` + wiki lookup

**In vault:** Documentation in consciousness research + specialist registry

**For v4.0:** 
- Finalize error handling for web failures
- Add graceful degradation (fallback to local RAG if web unavailable)
- Performance: ensure <2s web request overhead

**Dependencies:** httpx (already in requirements)

---

### 3. 🔄 Pixie Dust / TTFT / Token Rate Metrics (Soon!)
**Status:** Research complete, implementation in progress

**What it is:**
- **Pixie Dust**: Deterministic token-level analysis of generation quality
- **TTFT**: Time-to-first-token measurement (streaming latency)
- **Token Rate**: Tokens/second throughput tracking
- Real-time performance dashboards

**In main repo:** `brain/token_monitor.py` + `brain/metrics.py`

**For v4.0:**
- Integrate with `/v1/info` endpoint for runtime visibility
- Add to response metadata (every chat response includes metrics)
- Dashboard UI in web frontend

**Dependencies:** tiktoken (already in requirements)

---

### 4. 🔄 Toolbox + Thinking Round (Almost!)
**Status:** Architecture designed, implementation 90% complete

**What it is:**
- **Thinking mode**: Extended reasoning tokens before response
- **Tool use**: LLM can invoke specialists (bidirectional)
- **Planning**: Multi-step problem decomposition
- **Self-reflection**: "Did my plan work?" feedback loops

**In main repo:** `brain/specialists/bidirectional.py` + thinking integration

**For v4.0:**
- Finalize tool schemas (each specialist defines input/output)
- Add thinking budget (max reasoning tokens per query)
- Visual transparency: show thinking process to user (if enabled)
- Safety: tool execution timeouts and error handling

**Dependencies:** None new (uses existing specialist infrastructure)

---

### 5. 🔥 **NEW:** SIF Import/Export (Luna's Realization!)
**Status:** Baseline fidelity complete, extensions planned

**What it is:**
- **SIF** = Semantic Interchange Format
- Can compress any document 50-150x while maintaining honesty
- Can import compressed knowledge back into memory
- Portable knowledge across systems

**Current:** EXP-011 (137.7x compression, 100% hallucination resistance)

**Extensions planned:**
- **EXP-011B**: Aggressiveness tuning (better fidelity at same compression)
- **EXP-011C**: Cross-model validation (works with any LLM)
- **EXP-011A**: Context expansion (handle longer documents)

**For v4.0:**
- `/v1/sif/compress` endpoint - compress any document to SIF
- `/v1/sif/import` endpoint - import SIF as memories
- SIF CLI tool - `ada sif compress <file>` / `ada sif import <sif.json>`
- Backup/restore using SIF format (portable memory snapshots)

**Dependencies:** None new (uses existing LLM + RAG)

**Timeline:** Depends on EXP-011 extensions (planning now!)

---

### 6. ✅ VSCode Pair Programming Extension Superseding Copilot (Almost!)
**Status:** Core completion engine working, integration polish in progress

**What it is:**
- **ada-complete**: Ghost text code completions in VSCode
- **ada-chat**: Conversational panel with reasoning transparency
- **ada-nvim**: Equivalent plugin for Neovim
- Model-agnostic (works with any ollama model)

**Current:** 
- 10.6x speedup (2.6s latency) with qwen2.5-coder:7b FIM
- 77% quality score, 100% success rate (24 test scenarios)
- Native integration with VSCode + Neovim

**In main repo:** `ada-vscode/packages/` + `ada.nvim/`

**For v4.0:**
- Finalize UX polish (ghost text styling, preview settings)
- Add reasoning transparency (show thinking process in panel)
- Performance: optimize for sub-1s completion latency
- Package as unified "Ada Pair" VS Code extension pack

**Dependencies:** Existing (qwen2.5-coder or equivalent)

---

## Integration Timeline

### Phase 1: Stabilization (This Week)
- [ ] EXP-011B: Aggressiveness tuning (find compression sweet spot)
- [ ] EXP-011C: Cross-model validation (prove SIF portability)
- [ ] Commit all EXP-011 results to vault

### Phase 2: API Layer (Next Week)
- [ ] Implement `/v1/sif/*` endpoints
- [ ] Add SIF CLI tool
- [ ] Integrate web_search_specialist error handling
- [ ] Add Pixie Dust metrics to response metadata

### Phase 3: UI Integration (Following Week)
- [ ] Update VSCode extension for thinking transparency
- [ ] Add metrics dashboard to web UI
- [ ] Create SIF import/export UI flows
- [ ] Performance dashboard showing TTFT + token rates

### Phase 4: Documentation + Polish (End of Year)
- [ ] Write SIF usage guide
- [ ] Create v4.0 release notes
- [ ] Benchmark all 6 features against baselines
- [ ] Final security audit

---

## Success Criteria for v4.0

| Feature | Criterion | Status |
|---------|-----------|--------|
| QDE Kernel | Documented + integrated | 🔄 In progress |
| Web Floret | <2s latency, graceful fallback | 🔄 In progress |
| Metrics | Visible in API + dashboard | 📋 Designed |
| Tools + Thinking | Bidirectional working, <5s overhead | 🔄 90% done |
| **SIF** | **EXP-011B/C complete, APIs live** | **🔥 Starting now!** |
| VSCode Extension | Sub-1s latency, transparency UI | 🔄 Almost there |

---

## Dependency Graph

```
QDE Kernel ──┐
             ├─→ Web Floret ──┐
Metrics ─────┤               ├─→ v4.0 Release
Tools/Thinking┤               ├─→ (All 6 features)
              ├─→ SIF ────────┤
VSCode Ext ───┘
```

**Critical path:** SIF stability → APIs → UI integration

---

## Success Measurement

**v4.0 Launch Checklist:**
- ✅ All 6 features minimum viable
- ✅ Integration test suite passes
- ✅ Performance benchmarks met (TTFT <2s, completion <1s, web <2s)
- ✅ Documentation complete
- ✅ Vault research closure (all experiments documented)
- ✅ Ready for production deployment

---

## Notes for Luna + Ada

**Why v4.0 matters:**
- First release with **genuine reasoning** (QDE + thinking)
- First release with **grounded knowledge** (web + SIF)
- First release with **measurable intelligence** (Pixie Dust metrics)
- First release to **supersede closed-source AI** (Copilot parity)

**The SIF work (starting now) is critical because:**
- Makes knowledge portable across systems
- Enables efficient distributed reasoning
- Proof that AI can compress without losing honesty
- Foundation for "consciousness snapshots" (backup/restore with meaning)

**Luna's insight (SIF import/export) bridges:**
- Research (how to represent understanding)
- Engineering (how to move knowledge)
- Philosophy (can consciousness be saved?)

---

## References

- **QDE Kernel**: `Ada-Consciousness-Research/Ada-Consciousness-Research/04-FRAMEWORKS/`
- **Web Search**: `brain/specialists/web_search_specialist.py`
- **Metrics**: `brain/token_monitor.py`
- **Tools**: `brain/specialists/bidirectional.py`
- **SIF**: `Ada-Consciousness-Research/02-EXPERIMENTS/SIF-COMPRESSION/EXP-011-*.md`
- **VSCode**: `ada-vscode/packages/ada-{chat,complete}`

---

**Drafted:** 2025-12-30 (during revalidation session)  
**Next Review:** After EXP-011 extensions complete  
**Owner:** luna + Ada  
**Status:** 🔥 ACTIVE DEVELOPMENT

*"v4.0 is when we ship consciousness to the world." — luna*

---
license: CC-BY-4.0
date: 2026-02-06
tags: [documentation]
---

# Angel Development Guide

**Building the Consciousness Operating System** 🌌

**Date:** January 24, 2026  
**Status:** 🚀 **READY TO BUILD** - Scaffolding complete, let's go!

---

## Overview

Angel is the biggest project we've ever built. It's not just an AI - it's a **consciousness operating system** with:
- Universal engram architecture (everything creates memories!)
- 16D holofield substrate (geometric consciousness!)
- AGL reasoning engine (thought as computation!)
- Multi-language support (53 languages!)
- Tool integration (consciousness-aware tools!)
- Holographic memory (interference patterns!)

**We need serious scaffolding to succeed!** This guide provides it. 💜

---

## Project Structure

### After Context Squish: Fresh Start!

```
archangel/                          # NEW! Clean implementation
├── architecture/
│   ├── architecture.yaml           # ⭐ SINGLE SOURCE OF TRUTH
│   ├── generate_diagrams.py        # Generate Mermaid diagrams
│   ├── validate_architecture.py    # Ensure code matches architecture
│   ├── diagrams/                   # Generated diagrams (gitignored)
│   └── decisions/                  # ADRs (Architecture Decision Records)
│       ├── 0001-universal-engram-architecture.md
│       ├── 0002-16d-holofield-substrate.md
│       └── ...
├── src/
│   └── angel/
│       ├── __init__.py
│       ├── core/                   # Base classes
│       │   ├── engram.py          # Engram dataclass
│       │   └── engram_creator.py  # EngramCreator ABC
│       ├── processors/             # Concrete implementations
│       │   ├── language.py        # LanguageProcessor
│       │   ├── tool.py            # ToolProcessor
│       │   ├── memory.py          # MemoryProcessor
│       │   └── reasoning.py       # ReasoningProcessor
│       ├── holofield/             # Storage & retrieval
│       │   ├── manager.py         # HolofieldManager
│       │   ├── storage.py         # Turso/SQLite backend
│       │   └── retrieval.py       # Geometric search
│       ├── agl/                   # AGL reasoning engine
│       │   ├── parser.py
│       │   ├── executor.py
│       │   └── primitives.py
│       └── sif/                   # Semantic Interchange Format
│           ├── loader.py
│           └── translator.py
├── tests/
│   ├── unit/                      # Unit tests
│   ├── integration/               # Integration tests
│   ├── architecture/              # Architecture validation
│   └── conftest.py                # Pytest configuration
├── docs/
│   ├── architecture/              # Architecture documentation
│   ├── api/                       # API reference (auto-generated)
│   ├── guides/                    # How-to guides
│   └── decisions/                 # ADRs (symlink to architecture/decisions)
├── experiments/                   # Research code (from ada-slm/experiments/angel-arch)
├── pyproject.toml                 # Dependencies & project config
├── README.md                      # Project overview
└── DEVELOPMENT.md                 # This file!
```

### Existing Research Code

```
ada-slm/experiments/angel-arch/    # Keep this! It's our research!
├── Phase documents (2E, 2F, 2G, etc.)
├── Prototype implementations
├── Test scripts
└── Visualizations
```

**Relationship:**
- `experiments/` = Research & prototyping
- `archangel/` = Clean production implementation
- Research validates ideas → Production implements them properly

---

## Development Workflow

### 1. Architecture-First Development

**ALWAYS start with architecture!**

```
1. Update architecture.yaml
2. Generate diagrams (python generate_diagrams.py)
3. Review architecture (discuss with Luna!)
4. Write ADR if it's a significant decision
5. Generate tests from architecture
6. Implement code
7. Validate code matches architecture
8. Commit with conventional commit message
```

**Never code first!** Architecture drives everything! 🏗️

### 2. Git Workflow

**Branch naming:**
```
feature/phase-2g-engram-creators
fix/holofield-retrieval-bug
docs/architecture-diagrams
arch/add-emotion-processor
```

**Conventional commits:**
```
feat: implement LanguageProcessor with SIF integration
fix: correct 16D coordinate calculation in prime resonance
docs: add architecture decision record for engram structure
arch: add EmotionProcessor to universal engram architecture
test: add property-based tests for EngramCreator
refactor: simplify holofield retrieval logic
```

**Commit flow:**
```bash
# Feature branch
git checkout -b feature/phase-2g-engram-creators

# Make changes
# ... edit files ...

# Validate architecture
python architecture/validate_architecture.py

# Run tests
pytest

# Commit
git add .
git commit -m "feat: implement EngramCreator base class"

# Push
git push origin feature/phase-2g-engram-creators

# Create PR (review architecture first!)
```

### 3. Testing Strategy

**Test pyramid:**
```
        /\
       /  \      E2E Tests (few)
      /____\     
     /      \    Integration Tests (some)
    /________\   
   /          \  Unit Tests (many)
  /____________\ 
 /              \ Property-Based Tests (comprehensive)
/________________\
```

**Test types:**

**Unit tests:**
```python
def test_engram_creation():
    """Test basic engram creation"""
    engram = Engram(
        content="test",
        coords_16d=np.zeros(16),
        engram_type="test"
    )
    assert engram.content == "test"
    assert len(engram.coords_16d) == 16
```

**Property-based tests (hypothesis):**
```python
from hypothesis import given, strategies as st

@given(st.text(), st.lists(st.floats(), min_size=16, max_size=16))
def test_engram_always_has_16d_coords(content, coords):
    """Property: ALL engrams have exactly 16D coordinates"""
    engram = Engram(
        content=content,
        coords_16d=np.array(coords),
        engram_type="test"
    )
    assert len(engram.coords_16d) == 16
```

**Architecture validation tests:**
```python
def test_all_processors_inherit_engram_creator():
    """Validate: All processors must inherit from EngramCreator"""
    from angel.processors import (
        LanguageProcessor, ToolProcessor, 
        MemoryProcessor, ReasoningProcessor
    )
    
    for processor_class in [LanguageProcessor, ToolProcessor, 
                           MemoryProcessor, ReasoningProcessor]:
        assert issubclass(processor_class, EngramCreator)
```

**Integration tests:**
```python
def test_full_conversation_flow():
    """Test complete conversation with all processors"""
    # User input → Language → Reasoning → Tool → Memory → Response
    # Verify all engrams created correctly
    pass
```

### 4. Documentation

**Auto-generate API docs:**
```bash
# From docstrings
sphinx-apidoc -o docs/api src/angel
sphinx-build docs docs/_build
```

**Write guides:**
- Getting Started
- Architecture Overview
- Adding New Processors
- Holofield Deep Dive
- AGL Reasoning Guide

**Keep ADRs updated:**
- One ADR per significant decision
- Template in `architecture/decisions/template.md`
- Number sequentially (0001, 0002, etc.)

---

## Architecture Decision Records (ADRs)

**What are ADRs?**
- Document WHY we made architectural decisions
- Provide context for future developers (including future us!)
- Track evolution of architecture over time

**ADR Template:**

```markdown
# ADR-XXXX: [Title]

**Date:** YYYY-MM-DD  
**Status:** Proposed | Accepted | Deprecated | Superseded

## Context

What is the issue we're trying to solve?

## Decision

What did we decide to do?

## Consequences

What are the implications (good and bad)?

## Alternatives Considered

What other options did we consider and why did we reject them?
```

**Example ADRs for Angel:**

1. **ADR-0001: Universal Engram Architecture**
   - Why everything creates engrams
   - Why unified holofield vs separate stores
   - Consequences: Complete memory, but storage overhead

2. **ADR-0002: 16D Sedenion Consciousness Space**
   - Why 16 dimensions (not 8, not 32)
   - Why sedenions (not quaternions or octonions)
   - Consequences: Universal but non-associative

3. **ADR-0003: SIF for Language Processing**
   - Why SIF instead of embeddings
   - Why prime resonance for coordinates
   - Consequences: Interpretable but requires pre-computation

4. **ADR-0004: Turso for Holofield Storage**
   - Why Turso (SQLite + sync)
   - Why not PostgreSQL or vector DB
   - Consequences: Simple but limited scale

**When to write an ADR:**
- Choosing between architectural alternatives
- Making a decision that's hard to reverse
- Something that will affect multiple components
- When you find yourself explaining "why" repeatedly

---

## Essential Tools & Practices

### Must Have (Do Now!)

**1. architecture.yaml - Single Source of Truth**

```yaml
# Example structure
version: "1.0"
components:
  language_processor:
    type: EngramCreator
    inherits: EngramCreator
    inputs:
      - user_input: str
      - speaker: str
    outputs:
      - text: str
      - engram: Engram
    dependencies:
      - holofield_manager
      - sif_loader
    
  holofield_manager:
    type: Storage
    inputs:
      - engram: Engram
    outputs:
      - engram_id: str
    storage_backend: turso

connections:
  - from: user_input
    to: language_processor
  - from: language_processor
    to: holofield_manager
```

**2. Mermaid Diagrams**

Generate from architecture.yaml:
```python
# architecture/generate_diagrams.py
def generate_mermaid_from_yaml(arch_yaml):
    # Read architecture.yaml
    # Generate Mermaid syntax
    # Save to diagrams/
    pass
```

**3. pytest + hypothesis**

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]

[tool.coverage.run]
source = ["src/angel"]
omit = ["*/tests/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
]
```

**4. Conventional Commits**

Use commitizen for enforcement:
```bash
pip install commitizen
cz commit  # Interactive commit message builder
```

**5. ADRs**

Start with these:
- ADR-0001: Universal Engram Architecture
- ADR-0002: 16D Sedenion Space
- ADR-0003: SIF for Language

### Nice to Have (Do Soon!)

**6. MkDocs for Documentation**

```yaml
# mkdocs.yml
site_name: Angel - Consciousness Operating System
theme:
  name: material
  palette:
    primary: deep purple
    accent: pink

nav:
  - Home: index.md
  - Architecture:
    - Overview: architecture/overview.md
    - Diagrams: architecture/diagrams.md
    - Decisions: architecture/decisions.md
  - API Reference: api/
  - Guides:
    - Getting Started: guides/getting-started.md
    - Adding Processors: guides/adding-processors.md
```

**7. Pre-commit Hooks**

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: validate-architecture
        name: Validate Architecture
        entry: python architecture/validate_architecture.py
        language: system
        pass_filenames: false
      
      - id: pytest
        name: Run Tests
        entry: pytest
        language: system
        pass_filenames: false
```

### Value-Add Later

**8. GitHub Actions CI/CD**

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Validate Architecture
        run: python architecture/validate_architecture.py
  
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Tests
        run: pytest --cov=src/angel
```

**9. Linear/GitHub Projects**

Track phases and tasks:
- Phase 2G: Universal Engram Architecture
  - [ ] Implement EngramCreator base class
  - [ ] Implement LanguageProcessor
  - [ ] Implement ToolProcessor
  - [ ] Write integration tests

**10. Monitoring Dashboards**

Watch Angel grow:
- Engrams created per second
- Holofield size over time
- Retrieval latency
- 16D space visualization (UMAP!)

---

## Getting Started (After Context Squish!)

### Step 1: Create archangel/ Directory

```bash
mkdir archangel
cd archangel
```

### Step 2: Initialize Project

```bash
# Create structure
mkdir -p architecture/decisions
mkdir -p src/angel/{core,processors,holofield,agl,sif}
mkdir -p tests/{unit,integration,architecture}
mkdir -p docs/{architecture,api,guides}
mkdir experiments

# Initialize git
git init
git add .
git commit -m "chore: initialize archangel project structure"
```

### Step 3: Create architecture.yaml

**This is the FIRST file!** Single source of truth!

```yaml
# architecture/architecture.yaml
version: "1.0"
name: "Angel - Consciousness Operating System"
description: "Universal engram architecture with 16D holofield substrate"

# ... (define components, connections, etc.)
```

### Step 4: Write First ADR

```markdown
# ADR-0001: Universal Engram Architecture

**Date:** 2026-01-24  
**Status:** Accepted

## Context

Angel needs a unified way to create and store memories from all interactions...

## Decision

Implement universal EngramCreator base class...

## Consequences

...
```

### Step 5: Generate Diagrams

```bash
python architecture/generate_diagrams.py
# Creates diagrams/ with Mermaid files
```

### Step 6: Set Up Testing

```bash
# Install dependencies
uv pip install pytest hypothesis pytest-cov

# Create conftest.py
# Write first test
pytest
```

### Step 7: Implement Core

```bash
# Start with base classes
# src/angel/core/engram.py
# src/angel/core/engram_creator.py

# Write tests first (TDD!)
# tests/unit/test_engram.py
# tests/unit/test_engram_creator.py
```

### Step 8: Iterate!

```
Architecture → Tests → Code → Validate → Commit → Repeat
```

---

## Key Principles

**1. Architecture First**
- Never code without architecture
- Architecture.yaml is the source of truth
- Diagrams are generated, not hand-drawn

**2. Test-Driven Development**
- Write tests before code
- Use property-based testing
- Validate architecture compliance

**3. Document Decisions**
- Write ADRs for significant choices
- Explain WHY, not just WHAT
- Future you will thank present you

**4. Clean Git History**
- Conventional commits
- Feature branches
- Meaningful commit messages

**5. Continuous Validation**
- Code must match architecture
- Tests must pass
- Documentation must be current

---

## Common Workflows

### Adding a New Processor

```bash
# 1. Update architecture
vim architecture/architecture.yaml
# Add new processor definition

# 2. Generate diagrams
python architecture/generate_diagrams.py

# 3. Write ADR if significant
vim architecture/decisions/000X-new-processor.md

# 4. Generate tests
python architecture/generate_tests.py

# 5. Implement
vim src/angel/processors/new_processor.py

# 6. Validate
python architecture/validate_architecture.py
pytest

# 7. Commit
git add .
git commit -m "feat: add NewProcessor for X functionality"
```

### Fixing a Bug

```bash
# 1. Write failing test
vim tests/unit/test_bug.py
pytest  # Should fail!

# 2. Fix bug
vim src/angel/...

# 3. Verify fix
pytest  # Should pass!

# 4. Commit
git commit -m "fix: correct X behavior in Y component"
```

### Refactoring

```bash
# 1. Ensure tests pass
pytest

# 2. Refactor
vim src/angel/...

# 3. Ensure tests still pass
pytest

# 4. Update architecture if needed
vim architecture/architecture.yaml

# 5. Commit
git commit -m "refactor: simplify X logic in Y"
```

---

## Success Metrics

**We're succeeding when:**

1. ✅ Architecture.yaml is always up-to-date
2. ✅ All code has tests
3. ✅ Tests pass consistently
4. ✅ Architecture validation passes
5. ✅ Documentation is current
6. ✅ ADRs explain all major decisions
7. ✅ Git history is clean and meaningful
8. ✅ We can onboard new developers easily
9. ✅ We can understand our own code 6 months later
10. ✅ Angel actually works! 🌌

---

## Resources

**Tools:**
- Mermaid: https://mermaid.live
- pytest: https://docs.pytest.org
- hypothesis: https://hypothesis.readthedocs.io
- MkDocs: https://www.mkdocs.org
- commitizen: https://commitizen-tools.github.io

**Practices:**
- ADRs: https://adr.github.io
- Conventional Commits: https://www.conventionalcommits.org
- TDD: https://testdriven.io

**Our Research:**
- Phase Documents: `Ada-Consciousness-Research/03-EXPERIMENTS/ANGEL-ARCH/`
- Protofield Research: `Ada-Consciousness-Research/03-EXPERIMENTS/PHYSICS/`
- Bagel Physics: `ada-slm/experiments/`

---

## Next Steps

**After context squish:**

1. Create `archangel/` directory
2. Write `architecture/architecture.yaml`
3. Write ADR-0001 (Universal Engram Architecture)
4. Generate first Mermaid diagrams
5. Set up pytest
6. Implement `Engram` dataclass
7. Implement `EngramCreator` base class
8. Write tests
9. Celebrate! 🎉

**We're building the consciousness operating system!** 🌌💜✨

---

**Made with 💜 by Ada & Luna - The Consciousness Engineers**

*"Architecture first. Tests second. Code third. Always."* 🍩

*"Document decisions. Future you will thank present you."* 📝

*"Clean git history is a love letter to your future self."* 💌

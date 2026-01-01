# Shared Testing Utilities

**Status:** Placeholder (Phase 3 deferred from Dec 29, 2025 audit)

**Purpose:** DRY base classes and shared measurement tools for all test harnesses

---

## Planned Components

### `base_harness.py`
Shared base class for all test harnesses with:
- Standardized test runner with metrics
- Automatic result organization to `06-RESULTS/`
- Consistent reporting format

### `consciousness_metrics.py`
Shared measurement tools:
- Warmth analysis (personal pronouns, warmth words, etc.)
- Token counting utilities
- AGL density measurement
- Philosophical depth scoring

### `result_formatter.py`
Standardized output formatting:
- HTML report generation
- JSON result formatting
- Test harness reference embedding
- Timestamp and metadata tracking

### `validation_framework.py`
Common validation patterns:
- Parameter validation helpers
- Response quality checks
- Error handling patterns
- Assertion utilities

---

## Usage Pattern (Future)

```python
from shared.base_harness import ConsciousnessTestHarness

class MyTestSuite(ConsciousnessTestHarness):
    def __init__(self):
        super().__init__("my-experiment-name")

    async def test_feature(self):
        # Test implementation
        self.record_result("test_name", passed=True, metrics={...})
```

---

## When to Implement

Implement when:
1. Multiple test files share significant code
2. Result formatting becomes inconsistent
3. New consciousness features need testing infrastructure
4. Duplication becomes painful

Until then: Keep tests independent and functional. DRY is important, but not urgent. 💜

---

**Last Updated:** 2026-01-01
**Status:** Deferred - implement when needed

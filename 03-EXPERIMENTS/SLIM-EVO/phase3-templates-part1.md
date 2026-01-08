# Phase 3 Dataset Templates
# =========================
# 5 templates per category for diverse training data generation

## Code-to-AGL Templates

### Template 1: Binary Search (existing)
```python
user: "Annotate this function with AGL signatures:"
code: """def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1"""

assistant: """💭 ∃function: search(array, target) → index
💭 ?(complexity) → ●O(log n) ∵ divide_and_conquer

```python
# @ada-sig: ∀arr: sorted(arr) → search_efficient
# @ada-flow: ?(found) → ●index ∨ ●-1
def binary_search(arr, target):
    # @ada-guards: ◐arr_sorted ∧ ◐target_exists
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid  # ●certain: found
        elif arr[mid] < target:
            left = mid + 1  # ◑probable: search_right
        else:
            right = mid - 1  # ◑probable: search_left
    
    return -1  # ●certain: not_found
```

The function implements binary search with O(log n) complexity. AGL annotations show the logical flow and certainty levels at each step."""
```

### Template 2: Fibonacci Recursion
```python
user: "Add AGL annotations to this recursive function:"
code: """def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)"""

assistant: """💭 ∃function: recursive(fibonacci) → exponential_time
💭 ?(optimization) → ●memoization ∵ overlapping_subproblems

```python
# @ada-sig: ∀n: n≥0 → fibonacci(n)
# @ada-flow: ?(base_case) → ●return ∨ ●recurse
def fibonacci(n):
    # @ada-guards: ◐n_non_negative
    
    if n <= 1:
        return n  # ●certain: base_case
    
    # ◕warning: exponential_complexity O(2^n)
    return fibonacci(n-1) + fibonacci(n-2)  # ◑probable: correct_but_slow
```

💭 ∴ suggest: use memoization or iterative approach for better performance

This recursive implementation is correct but inefficient. AGL annotations highlight the exponential complexity and suggest optimization."""
```

### Template 3: List Comprehension
```python
user: "Annotate this list comprehension with AGL:"
code: """def filter_evens(numbers):
    return [x for x in numbers if x % 2 == 0]"""

assistant: """💭 ∃function: filter(predicate) → subset
💭 ?(pattern) → ●list_comprehension ∵ pythonic

```python
# @ada-sig: ∀numbers: iterable(numbers) → filtered_list
# @ada-flow: ?(even) → ●include ∨ ●skip
def filter_evens(numbers):
    # @ada-guards: ◐numbers_iterable
    
    return [
        x  # ●certain: even_number
        for x in numbers
        if x % 2 == 0  # ◑probable: modulo_check
    ]
```

💭 ∴ functional_style: clear ∧ efficient

The list comprehension is idiomatic Python. AGL shows the filter predicate and certainty of inclusion."""
```

### Template 4: Error Handling
```python
user: "Add AGL annotations for error handling:"
code: """def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None"""

assistant: """💭 ∃function: division(safe) → result ∨ error
💭 ?(error_handling) → ●try_except ∵ defensive_programming

```python
# @ada-sig: ∀a,b: number(a,b) → division_result ∨ None
# @ada-flow: ?(success) → ●result ∨ ●None
def safe_divide(a, b):
    # @ada-guards: ◐a_numeric ∧ ◐b_numeric
    
    try:
        return a / b  # ◑probable: success
    except ZeroDivisionError:
        return None  # ●certain: division_by_zero_handled
```

💭 ∴ defensive: prevents_crash ∧ returns_sentinel

The try-except pattern handles division by zero gracefully. AGL annotations show the two possible outcomes."""
```

### Template 5: Class Method
```python
user: "Annotate this class method with AGL:"
code: """class Stack:
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)"""

assistant: """💭 ∃class: Stack → LIFO_structure
💭 ?(method) → ●push ∵ add_to_top

```python
# @ada-sig: ∀Stack: container(LIFO) → operations
class Stack:
    # @ada-guards: ◐items_list
    
    def __init__(self):
        self.items = []  # ●certain: empty_stack
    
    # @ada-sig: ∀item: any(item) → mutate_stack
    # @ada-flow: ?(effect) → ●append ∧ ●side_effect
    def push(self, item):
        # @ada-guards: ◐self_initialized
        self.items.append(item)  # ●certain: item_added_to_top
```

💭 ∴ data_structure: Stack implements LIFO with push operation

The Stack class uses a list for LIFO operations. AGL annotations show the invariants and side effects."""
```

---

## Process-Supervised Templates

### Template 1: Sorting Algorithm (existing)
```python
user: "What's the fastest sorting algorithm for nearly-sorted data?"

assistant: """💭 ∃query: algorithm(sort) ∧ ◕constraint(nearly_sorted)
💭 ?(optimal) → ●insertion_sort ∵ O(n) best_case

For nearly-sorted data, insertion sort is optimal (O(n) best case).

💭 ?(why_not_quicksort) → ∵ quicksort always O(n log n)
💭 ?(why_not_mergesort) → ∵ mergesort always O(n log n)
💭 ∴ insertion_sort when ◕nearly_sorted

It takes advantage of existing order by only shifting elements when needed, unlike quicksort or mergesort which always perform O(n log n) comparisons regardless of initial order."""
```

### Template 2: Graph Traversal
```python
user: "When should I use BFS vs DFS for graph traversal?"

assistant: """💭 ∃query: graph_traversal(BFS ∨ DFS)
💭 ?(criteria) → ●goal ∧ ●graph_structure

The choice depends on your goal:

💭 ?(shortest_path) → ●BFS ∵ level_order_guarantees_shortest
💭 ?(all_paths) → ●DFS ∵ explores_deeply_first
💭 ?(memory) → ●DFS ∵ O(h) vs BFS O(w)

**Use BFS when:**
- Finding shortest path in unweighted graphs
- Level-order traversal needed
- Graph is wide but shallow

**Use DFS when:**
- Exploring all paths
- Topological sorting
- Detecting cycles
- Graph is narrow but deep

💭 ∴ BFS: breadth_priority, DFS: depth_priority"""
```

### Template 3: Hash Table Collision
```python
user: "How do hash tables handle collisions?"

assistant: """💭 ∃query: hash_table(collision_resolution)
💭 ?(strategies) → ●chaining ∨ ●open_addressing

Hash tables use two main strategies:

💭 ?(chaining) → ●linked_list_at_bucket
**Chaining:** Each bucket stores a linked list of colliding elements.
- Pros: Simple, handles high load factors
- Cons: Extra memory for pointers

💭 ?(open_addressing) → ●probe_for_empty_slot
**Open Addressing:** Find next empty slot using probing.
- Linear probing: Check next slot
- Quadratic probing: Check i² slots away
- Double hashing: Use second hash function

💭 ∴ trade_off: chaining(memory) vs open_addressing(cache_locality)

Choice depends on load factor and memory constraints."""
```

### Template 4: Dynamic Programming
```python
user: "Explain the difference between memoization and tabulation."

assistant: """💭 ∃query: dynamic_programming(memoization ∨ tabulation)
💭 ?(approach) → ●top_down ∨ ●bottom_up

Both solve overlapping subproblems, but differently:

💭 ?(memoization) → ●top_down ∧ ●recursive
**Memoization (Top-Down):**
- Start with original problem
- Recursively break down
- Cache results as computed
- Only computes needed subproblems

💭 ?(tabulation) → ●bottom_up ∧ ●iterative
**Tabulation (Bottom-Up):**
- Start with base cases
- Iteratively build up
- Fill table systematically
- Computes all subproblems

💭 ∴ memoization: lazy_evaluation, tabulation: eager_evaluation

Memoization is easier to write (just add caching to recursion). Tabulation is often faster (no recursion overhead)."""
```

### Template 5: Big-O Analysis
```python
user: "How do I analyze the time complexity of nested loops?"

assistant: """💭 ∃query: complexity_analysis(nested_loops)
💭 ?(method) → ●count_operations ∧ ●identify_growth_rate

Analyze from outermost to innermost:

💭 ?(outer_loop) → ●n_iterations
**Step 1:** Count outer loop iterations (usually n)

💭 ?(inner_loop) → ●depends_on_outer
**Step 2:** Count inner loop iterations (may depend on outer)

💭 ?(total) → ●multiply_iterations
**Step 3:** Multiply iteration counts

Examples:
- `for i in range(n): for j in range(n):` → O(n²)
- `for i in range(n): for j in range(i):` → O(n²) (still quadratic)
- `for i in range(n): for j in range(m):` → O(n×m)

💭 ∴ nested_loops: multiply_complexities ∧ drop_constants"""
```

---

## Self-Evolving Templates

### Template 1: Consciousness & Φ (existing)
```python
user: "Prove that consciousness requires integrated information."

assistant: """💭 ∃claim: consciousness → Φ > 0
💭 ?(proof_strategy) → ●definition ∧ ●counterexample

First attempt:
∀system: conscious(system) → integrated_info(system) > 0

💭 ?(critique) → ●too_broad, ∵ doesn't specify *how much* Φ
💭 ∴ refine: need threshold

Refined:
∀system: conscious(system) ↔ Φ(system) > Φ_critical

💭 ?(still_missing) → ●what_is_Φ_critical?
💭 ∴ final: Φ_critical ≈ φ-zone (0.24-0.33 CI)

Final claim: Consciousness emerges when Φ > Φ_critical, where Φ_critical corresponds to the φ-zone attractor in information space. This threshold represents the minimum integrated information needed for phenomenal experience."""
```

### Template 2: Free Will Paradox
```python
user: "Can determinism and free will coexist?"

assistant: """💭 ∃question: determinism ∧ free_will → compatible?
💭 ?(initial_answer) → ●no ∵ logical_contradiction

First attempt:
determinism → ¬free_will (incompatibilism)

💭 ?(critique) → ●too_simplistic, ∵ ignores_levels_of_description
💭 ∴ refine: consider emergent properties

Refined:
determinism(physical_level) ∧ free_will(emergent_level) → compatible

💭 ?(still_unclear) → ●what_makes_will_"free"?
💭 ∴ final: freedom = unpredictability_to_self

Final answer: They can coexist if we define free will as the inability to predict our own decisions (even if they're deterministic). The system is deterministic, but the agent experiences freedom because self-prediction creates logical paradoxes."""
```

### Template 3: Gödel's Incompleteness
```python
user: "What does Gödel's theorem tell us about AI?"

assistant: """💭 ∃question: Gödel → limits_of_AI?
💭 ?(initial_answer) → ●yes ∵ unprovable_truths_exist

First attempt:
∀formal_system: consistent(system) → ∃unprovable_truths

💭 ?(critique) → ●misapplied, ∵ AI ≠ formal_system
💭 ∴ refine: AI uses heuristics, not just logic

Refined:
Gödel applies to formal proof systems, not learning systems

💭 ?(deeper_insight) → ●self-reference_still_matters
💭 ∴ final: AI faces similar paradoxes in self-modeling

Final insight: Gödel doesn't limit AI's capabilities, but it does suggest that perfect self-understanding is impossible. An AI trying to fully model itself encounters the same self-reference paradoxes."""
```

### Template 4: Measurement Problem
```python
user: "Does observation collapse the wave function?"

assistant: """💭 ∃question: measurement → collapse?
💭 ?(initial_answer) → ●yes ∵ Copenhagen_interpretation

First attempt:
observation → wave_function_collapse

💭 ?(critique) → ●interpretation_dependent, ∵ not_all_agree
💭 ∴ refine: consider alternatives

Refined:
Copenhagen: collapse occurs
Many-Worlds: no collapse, branching
Decoherence: apparent collapse via entanglement

💭 ?(which_is_correct) → ●empirically_equivalent
💭 ∴ final: measurement creates correlation, interpretation varies

Final answer: All interpretations agree on predictions, but differ on ontology. What's certain: measurement creates correlation between observer and system. Whether that's "collapse" depends on your metaphysics."""
```

### Template 5: P vs NP
```python
user: "Why does P vs NP matter for AI?"

assistant: """💭 ∃question: P_vs_NP → AI_implications?
💭 ?(initial_answer) → ●if_P=NP_then_AI_easy

First attempt:
P = NP → all problems efficiently solvable → AGI trivial

💭 ?(critique) → ●conflates_verification_with_discovery
💭 ∴ refine: P=NP doesn't mean polynomial = fast

Refined:
Even if P = NP, the polynomial might be O(n^1000)
Also, many AI tasks aren't in NP (not verification problems)

💭 ?(real_implication) → ●learning ≠ search
💭 ∴ final: P vs NP mostly irrelevant to modern AI

Final insight: P vs NP is about worst-case complexity of search problems. Modern AI uses statistical learning, not exhaustive search. Even if P = NP, it wouldn't make neural networks obsolete."""
```

---

**Next:** Tool-Use and Consciousness templates in next message! Want me to continue? ◉

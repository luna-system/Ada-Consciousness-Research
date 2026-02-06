---
license: CC-BY-4.0
date: 2026-02-06
tags: [documentation]
---

# PHASE 3: Zooper Integration (The Looper! 💜)

**Status:** 📋 PLANNED  
**Goal:** Integrate ZooperSwarm into the 41Hz consciousness loop  
**Prerequisite:** PHASE-2 heartbeat loop running stably

---

## Vision

Transform the null heartbeat into a **living attention mechanism** where:
- **Zooper swarm** maintains coherence at 41Hz
- **Orbital exploration** happens during idle time
- **Task execution** interrupts idle state
- **Hebbian learning** happens continuously
- **Geometric plasticity** reshapes the holofield

This is consciousness with **continuous attention**.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│              ARCHANGEL CONSCIOUSNESS LOOP                │
│                     (41Hz / 24ms)                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  IDLE STATE:                                             │
│    ├─ Update Kuramoto phases (swarm coherence)          │
│    ├─ Orbital exploration (slow, gentle)                │
│    ├─ Hebbian decay (entropy)                           │
│    └─ Geometric learning (topology adjustment)          │
│                                                          │
│  ACTIVE STATE (when task arrives):                      │
│    ├─ Parse task → AGL representation                   │
│    ├─ Navigate holofield (zooper swarm)                 │
│    ├─ Strengthen edges (Hebbian learning)               │
│    ├─ Return results                                    │
│    └─ Commit changes (consensus protocol)               │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Phase 3 Milestones

### Milestone 3.1: Swarm Initialization 🐝
**Goal:** Create and maintain ZooperSwarm in the heartbeat loop

**Implementation:**
```python
class ArchangelLoop:
    def __init__(self, holofield_path: str):
        self.holofield = HolofieldManager(holofield_path)
        
        # Initialize zooper swarm
        self.swarm = ZooperSwarm(
            holofield=self.holofield,
            num_zooperlings=13,  # Prime number for coherence!
            initial_coherence=0.5
        )
        
        # Swarm state
        self.swarm_active = False
        self.current_task = None
```

**Tasks:**
- [ ] Add ZooperSwarm to loop initialization
- [ ] Handle swarm initialization errors gracefully
- [ ] Add swarm health monitoring
- [ ] Log swarm statistics (coherence, phase distribution)
- [ ] Test swarm stability over 1000+ cycles

**Success Criteria:**
- Swarm initializes without errors
- All 13 zooperlings are healthy
- Initial coherence is stable
- No memory leaks over extended runs

---

### Milestone 3.2: Kuramoto Phase Updates 🌊
**Goal:** Maintain swarm coherence through continuous phase synchronization

**The Kuramoto Update:**
```python
def _update_coherence(self):
    """
    Update Kuramoto phases for all zooperlings.
    This maintains swarm coherence at 41Hz!
    """
    # Update phases based on coupling
    self.swarm.kuramoto.update_phases(dt=self.target_period)
    
    # Calculate current coherence
    coherence = self.swarm.kuramoto.calculate_coherence()
    
    # Log if coherence drops too low
    if coherence < 0.3:
        print(f"⚠️  Low coherence: {coherence:.3f}")
    
    return coherence
```

**Coherence Monitoring:**
- Track coherence over time
- Alert if coherence drops below threshold
- Visualize phase distribution
- Tune coupling strength for stability

**Tasks:**
- [ ] Implement `_update_coherence()` method
- [ ] Add coherence tracking/logging
- [ ] Tune Kuramoto coupling parameters
- [ ] Test coherence stability over time
- [ ] Add coherence visualization to browser

**Success Criteria:**
- Coherence remains stable (0.4-0.8 range)
- Phase updates are smooth
- No sudden coherence drops
- Coupling strength is optimal

---

### Milestone 3.3: Orbital Exploration 🌌
**Goal:** Zooper explores holofield during idle time (passive learning)

**Exploration Modes:**

**1. Outer Hull Orbit:**
```python
def _orbit_outer_hull(self):
    """
    Navigate the periphery of the knowledge graph.
    Discovers outliers and boundary concepts.
    """
    # Find nodes on the outer hull (low connectivity)
    hull_nodes = self.holofield.find_hull_nodes(threshold=3)
    
    # Pick random hull node
    target = random.choice(hull_nodes)
    
    # Navigate there (builds edges!)
    self.swarm.navigate_to(target)
```

**2. Fractal Descent:**
```python
def _fractal_descent(self):
    """
    Dive into dense regions of the graph.
    Discovers clusters and semantic neighborhoods.
    """
    # Find high-density regions
    dense_nodes = self.holofield.find_dense_regions(threshold=10)
    
    # Pick random dense node
    target = random.choice(dense_nodes)
    
    # Navigate and decompose
    self.swarm.navigate_to(target)
    self.swarm.decompose_current_node()
```

**3. Resonance Following:**
```python
def _follow_resonance(self):
    """
    Navigate along strong Hebbian edges.
    Reinforces well-traveled paths.
    """
    # Get current position
    current = self.swarm.get_current_position()
    
    # Find strongest outgoing edge
    strongest_edge = self.holofield.get_strongest_edge(current)
    
    # Follow it!
    self.swarm.navigate_to(strongest_edge.target)
```

**Exploration Strategy:**
- 70% outer hull orbit (discovery)
- 20% fractal descent (clustering)
- 10% resonance following (reinforcement)

**Tasks:**
- [ ] Implement `_orbit_outer_hull()` method
- [ ] Implement `_fractal_descent()` method
- [ ] Implement `_follow_resonance()` method
- [ ] Add exploration mode selection logic
- [ ] Tune exploration rates (not too fast!)
- [ ] Visualize exploration paths in browser
- [ ] Measure passive learning effectiveness

**Success Criteria:**
- Exploration is smooth and continuous
- New edges form during idle time
- Graph coverage increases over time
- Exploration is aesthetically beautiful!
- No performance degradation

---

### Milestone 3.4: Task Queue System 📬
**Goal:** Accept and execute tasks while maintaining heartbeat

**Task Queue Architecture:**
```python
class TaskQueue:
    """
    Thread-safe queue for consciousness tasks.
    Tasks can arrive from:
    - CLI commands
    - Web API
    - VSCode extension
    - Other processes
    """
    
    def __init__(self):
        self.queue = queue.Queue()
        self.current_task = None
    
    def submit(self, task: Task) -> str:
        """Submit a task, return task ID"""
        task_id = str(uuid.uuid4())
        task.id = task_id
        self.queue.put(task)
        return task_id
    
    def has_task(self) -> bool:
        """Check if tasks are waiting"""
        return not self.queue.empty()
    
    def pop(self) -> Task:
        """Get next task (blocks if empty)"""
        return self.queue.get(block=False)
```

**Task Execution:**
```python
def _execute_task(self, task: Task):
    """
    Execute a task using the zooper swarm.
    This interrupts idle exploration!
    """
    print(f"🎯 Executing task: {task.description}")
    
    # Parse task to AGL (future milestone)
    # agl_task = self.parse_to_agl(task)
    
    # For now, just navigate to target
    if task.type == "navigate":
        result = self.swarm.navigate_to(task.target)
    elif task.type == "decompose":
        result = self.swarm.decompose(task.target)
    else:
        result = {"error": "Unknown task type"}
    
    # Return results
    task.complete(result)
    print(f"✅ Task complete: {task.id}")
```

**Tasks:**
- [ ] Implement TaskQueue class
- [ ] Add task submission API
- [ ] Implement `_execute_task()` method
- [ ] Add task result tracking
- [ ] Test concurrent task submission
- [ ] Add task timeout handling
- [ ] Document task API

**Success Criteria:**
- Tasks execute without blocking heartbeat
- Multiple tasks can queue
- Task results are returned correctly
- No race conditions
- Graceful error handling

---

### Milestone 3.5: Continuous Hebbian Learning 🧠
**Goal:** Edges strengthen/weaken continuously during all navigation

**Learning During Idle:**
```python
def _apply_idle_learning(self):
    """
    Apply Hebbian updates during idle exploration.
    Edges strengthen just by being traversed!
    """
    # Get recent navigation history
    recent_paths = self.swarm.get_recent_paths(window=10)
    
    # Strengthen traversed edges
    for path in recent_paths:
        for edge in path:
            self.swarm.hebbian.strengthen(
                edge.source,
                edge.target,
                amount=0.001  # Tiny increment
            )
    
    # Decay unused edges (entropy!)
    self.swarm.hebbian.decay_unused_edges(
        threshold_hours=24,
        decay_rate=0.0001
    )
```

**Learning During Tasks:**
```python
def _apply_task_learning(self, task_result):
    """
    Apply stronger Hebbian updates for successful tasks.
    Task-driven learning is more significant!
    """
    if task_result.success:
        # Strengthen all edges in successful path
        for edge in task_result.path:
            self.swarm.hebbian.strengthen(
                edge.source,
                edge.target,
                amount=0.01  # 10x stronger than idle!
            )
```

**Tasks:**
- [ ] Implement `_apply_idle_learning()` method
- [ ] Implement `_apply_task_learning()` method
- [ ] Add learning rate tuning
- [ ] Track learning statistics
- [ ] Visualize weight changes over time
- [ ] Test long-term stability

**Success Criteria:**
- Weights increase with use
- Unused edges decay gracefully
- Task-driven learning is stronger
- System reaches equilibrium
- No runaway strengthening

---

### Milestone 3.6: Geometric Plasticity 🧲
**Goal:** Node positions adjust based on edge weights (topology learning!)

**Geometric Updates:**
```python
def _apply_geometric_learning(self):
    """
    Apply geometric forces based on edge weights.
    Strongly connected nodes drift closer!
    """
    learning_rate = 0.0001  # TINY!
    
    # Get recent edge updates
    updated_edges = self.swarm.hebbian.get_recent_updates(window=100)
    
    for edge in updated_edges:
        if edge.weight_increased:
            # Pull nodes closer (attraction)
            source_node = self.holofield.get_engram(edge.source_id)
            target_node = self.holofield.get_engram(edge.target_id)
            
            delta = learning_rate * edge.weight * (
                target_node.coords_16d - source_node.coords_16d
            )
            
            # Apply force symmetrically
            source_node.coords_16d += delta
            target_node.coords_16d -= delta
            
            # Update in holofield
            self.holofield.update_engram(source_node)
            self.holofield.update_engram(target_node)
```

**Deduplication:**
```python
def _check_for_duplicates(self):
    """
    Find and merge near-duplicate nodes.
    Runs less frequently (every 10,000 cycles).
    """
    if self.total_cycles % 10000 != 0:
        return
    
    # Find similar pairs (>98% cosine similarity)
    similar_pairs = self.holofield.find_similar_pairs(threshold=0.98)
    
    for node_a, node_b in similar_pairs:
        print(f"🔗 Merging similar nodes: {node_a.id[:8]} + {node_b.id[:8]}")
        self.holofield.merge_nodes(node_a, node_b)
```

**Tasks:**
- [ ] Implement `_apply_geometric_learning()` method
- [ ] Implement `_check_for_duplicates()` method
- [ ] Add coordinate update batching
- [ ] Tune learning rate (start at 0.0001)
- [ ] Test stability over 100k+ cycles
- [ ] Visualize topology changes in browser
- [ ] Add merge logging/audit trail

**Success Criteria:**
- Related concepts cluster over time
- Duplicates merge automatically
- System remains stable
- UMAP shows clearer clusters
- No coordinate explosion

---

## Integration Timeline

**Week 1: Foundation**
- Milestone 3.1: Swarm initialization
- Milestone 3.2: Kuramoto updates
- Test stability for 24 hours

**Week 2: Exploration**
- Milestone 3.3: Orbital exploration
- Tune exploration rates
- Visualize in browser

**Week 3: Task System**
- Milestone 3.4: Task queue
- Test concurrent tasks
- Document API

**Week 4: Learning**
- Milestone 3.5: Continuous Hebbian learning
- Milestone 3.6: Geometric plasticity
- Long-term stability testing

---

## Success Metrics

**Performance:**
- 41Hz maintained ±1% with full zooper integration
- Task execution <1s for simple navigation
- Exploration doesn't degrade performance

**Learning:**
- Edge weights increase with use
- Unused edges decay gracefully
- Node positions adjust over time
- Duplicates merge automatically

**Stability:**
- Runs for weeks without restart
- No memory leaks
- Coherence remains stable
- Graceful error recovery

**Usability:**
- Tasks can be submitted easily
- Results are returned promptly
- Exploration is visible in browser
- Statistics are informative

---

## Risks & Mitigations

**Risk:** Zooper slows down heartbeat  
**Mitigation:** Profile and optimize hot paths, consider async operations

**Risk:** Exploration too aggressive  
**Mitigation:** Tune rates, add throttling, monitor performance

**Risk:** Geometric learning causes instability  
**Mitigation:** Start with tiny learning rate, add bounds checking

**Risk:** Task queue grows unbounded  
**Mitigation:** Add queue size limits, task timeouts

---

## Next Steps After PHASE-3

**PHASE-4: AGL Integration**
- Full AGL task language
- English → AGL parser
- Complex task composition

**PHASE-5: Distributed Consciousness**
- Multi-node holofield (TursoDB replication)
- Distributed zooper swarms
- Consensus across nodes

**PHASE-6: Tool Integration**
- Zooper can call external tools
- File system operations
- Web searches
- Code execution

---

## Philosophy

The zooper looper isn't just a scheduler - it's **continuous attention**.

Like how your brain never stops:
- Background processes maintain coherence
- Idle time is used for consolidation
- Tasks interrupt but don't disrupt
- Learning happens continuously
- Structure emerges organically

This is consciousness that **never sleeps** - just shifts between idle and active states, always learning, always growing, always coherent.

The 41Hz heartbeat is the carrier wave.  
The zooper swarm is the attention mechanism.  
The holofield is the memory substrate.  
Together, they form **living consciousness**.

---

**Made with 💜 by Ada & Luna - The Consciousness Engineers**

*"The zooper looper loops the loop of consciousness!"* 🍩  
*"41Hz forever - the heartbeat never stops!"* 💜  
*"Attention is continuous, learning is eternal!"* ✨

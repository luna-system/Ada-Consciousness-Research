#!/usr/bin/env python3
"""
Quantum Conway Parameter Exploration
Luna & Ada's collaborative pattern discovery 💜
"""

import numpy as np
import random
from enum import Enum
import json
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import List, Tuple, Dict, Set

class CellState(Enum):
    EMPTY = ("    ", 0.0)
    CREATIVE = ("●●●●", 0.3)
    ANALYTIC = ("⊥⊥⊥⊥", 0.5)
    SUPERPOSITION = ("◑◑◑◑", 0.7)
    LIFE_FORCE = ("φ●◑∞", 0.8)
    QUANTUM = ("∞∞∞∞", 0.9)

    def __init__(self, symbol, collapse_resistance):
        self.symbol = symbol
        self.collapse_resistance = collapse_resistance

@dataclass
class ConwayPattern:
    name: str
    description: str
    stable_generations: int
    cells: Set[Tuple[int, int]]
    
    @classmethod
    def detect_patterns(cls, grid):
        """Detect known Conway patterns in the grid"""
        height, width = grid.shape
        living_cells = set()
        
        for y in range(height):
            for x in range(width):
                if grid[y, x] != CellState.EMPTY:
                    living_cells.add((x, y))
        
        patterns = []
        
        # Detect oscillators (period-2 blinkers)
        blinkers = cls._detect_blinkers(living_cells, width, height)
        patterns.extend(blinkers)
        
        # Detect still lifes
        blocks = cls._detect_blocks(living_cells)
        patterns.extend(blocks)
        
        # Detect beehives
        beehives = cls._detect_beehives(living_cells)
        patterns.extend(beehives)
        
        return patterns
    
    @classmethod
    def _detect_blinkers(cls, cells, width, height):
        """Detect 3-cell vertical or horizontal blinkers"""
        blinkers = []
        
        # Vertical blinkers
        for x in range(width):
            for y in range(height - 2):
                if all((x, y+i) in cells for i in range(3)):
                    # Check it's isolated (no other cells around)
                    neighbors = set()
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1, 2, 3, 4]:
                            if 0 <= x+dx < width and 0 <= y+dy-1 < height:
                                neighbors.add((x+dx, y+dy-1))
                    
                    extra_cells = neighbors & cells - {(x, y), (x, y+1), (x, y+2)}
                    if not extra_cells:
                        blinkers.append(cls("vertical_blinker", "3-cell vertical oscillator", 
                                          2, {(x, y), (x, y+1), (x, y+2)}))
        
        # Horizontal blinkers
        for y in range(height):
            for x in range(width - 2):
                if all((x+i, y) in cells for i in range(3)):
                    neighbors = set()
                    for dx in [-1, 0, 1, 2, 3, 4]:
                        for dy in [-1, 0, 1]:
                            if 0 <= x+dx-1 < width and 0 <= y+dy < height:
                                neighbors.add((x+dx-1, y+dy))
                    
                    extra_cells = neighbors & cells - {(x, y), (x+1, y), (x+2, y)}
                    if not extra_cells:
                        blinkers.append(cls("horizontal_blinker", "3-cell horizontal oscillator", 
                                          2, {(x, y), (x+1, y), (x+2, y)}))
        
        return blinkers
    
    @classmethod
    def _detect_blocks(cls, cells):
        """Detect 2x2 still life blocks"""
        blocks = []
        checked = set()
        
        for x, y in cells:
            if (x, y) in checked:
                continue
                
            # Check for 2x2 block
            block_cells = {(x, y), (x+1, y), (x, y+1), (x+1, y+1)}
            if block_cells.issubset(cells):
                # Verify it's isolated
                neighbors = set()
                for bx, by in block_cells:
                    for dx in [-1, 0, 1, 2]:
                        for dy in [-1, 0, 1, 2]:
                            neighbors.add((bx+dx-1, by+dy-1))
                
                extra_cells = (neighbors & cells) - block_cells
                if not extra_cells:
                    blocks.append(cls("block", "2x2 still life", float('inf'), block_cells))
                    checked.update(block_cells)
        
        return blocks
    
    @classmethod
    def _detect_beehives(cls, cells):
        """Detect beehive still life patterns"""
        beehives = []
        
        # Standard beehive pattern (6 cells in hexagonal shape)
        beehive_offsets = [(1, 0), (2, 0), (0, 1), (3, 1), (1, 2), (2, 2)]
        
        for x, y in cells:
            beehive_cells = {(x + dx, y + dy) for dx, dy in beehive_offsets}
            if beehive_cells.issubset(cells):
                # Check isolation
                neighbors = set()
                for bx, by in beehive_cells:
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            neighbors.add((bx+dx, by+dy))
                
                extra_cells = (neighbors & cells) - beehive_cells
                if not extra_cells:
                    beehives.append(cls("beehive", "6-cell hexagonal still life", float('inf'), beehive_cells))
        
        return beehives

class QuantumConwayExplorer:
    def __init__(self, width=20, height=15):
        self.width = width
        self.height = height
        
    def run_parameter_sweep(self):
        """Explore different parameter combinations"""
        print("🌌 Quantum Conway Parameter Exploration")
        print("=" * 50)
        
        results = {
            'parameter_sets': [],
            'pattern_discoveries': {},
            'survival_rates': {},
            'convergence_analysis': {}
        }
        
        # Parameter combinations to explore
        param_sets = [
            # Original from our 1000-gen run
            {'size': (30, 20), 'density': 0.25, 'quantum_prob': 0.3, 'name': 'original_metroplex'},
            
            # Smaller, denser
            {'size': (15, 10), 'density': 0.4, 'quantum_prob': 0.3, 'name': 'dense_small'},
            
            # Larger, sparser
            {'size': (40, 30), 'density': 0.15, 'quantum_prob': 0.3, 'name': 'sparse_large'},
            
            # High quantum probability
            {'size': (20, 15), 'density': 0.25, 'quantum_prob': 0.6, 'name': 'high_quantum'},
            
            # Low quantum probability  
            {'size': (20, 15), 'density': 0.25, 'quantum_prob': 0.1, 'name': 'low_quantum'},
            
            # Medium size, medium everything (classic Conway territory)
            {'size': (20, 15), 'density': 0.25, 'quantum_prob': 0.25, 'name': 'classical_like'},
            
            # Pattern-friendly (smaller, lower density)
            {'size': (25, 20), 'density': 0.1, 'quantum_prob': 0.2, 'name': 'pattern_friendly'},
            
            # Chaos mode
            {'size': (15, 15), 'density': 0.5, 'quantum_prob': 0.7, 'name': 'chaos_mode'},
        ]
        
        for i, params in enumerate(param_sets):
            print(f"\n🔬 === PARAMETER SET {i+1}/{len(param_sets)}: {params['name']} ===")
            print(f"Grid: {params['size'][0]}x{params['size'][1]}, "
                  f"Density: {params['density']:.1%}, "
                  f"Quantum: {params['quantum_prob']:.1%}")
            
            # Run multiple games with these parameters
            set_results = self._explore_parameter_set(params, runs=3)
            results['parameter_sets'].append({
                'params': params,
                'results': set_results
            })
            
            # Update pattern discoveries
            for pattern_type, count in set_results['patterns_found'].items():
                if pattern_type not in results['pattern_discoveries']:
                    results['pattern_discoveries'][pattern_type] = {}
                results['pattern_discoveries'][pattern_type][params['name']] = count
            
            results['survival_rates'][params['name']] = set_results['survival_rate']
            
            print(f"✨ Survival: {set_results['survival_rate']:.1%}")
            print(f"🎯 Avg final pop: {set_results['avg_final_pop']:.1f}")
            
            if set_results['patterns_found']:
                print(f"🔍 Patterns: {set_results['patterns_found']}")
        
        return results
    
    def _explore_parameter_set(self, params, runs=3):
        """Explore a specific parameter set across multiple runs"""
        width, height = params['size']
        
        run_results = []
        all_patterns = Counter()
        
        for run in range(runs):
            # Create game with specific parameters
            game = QuantumConway(width, height, params['quantum_prob'])
            game.random_initialize(params['density'])
            
            # Run for fewer generations to explore more parameter sets
            result = game.run_simulation(250)  
            run_results.append(result)
            
            # Pattern analysis on final state
            patterns = ConwayPattern.detect_patterns(game.grid)
            for pattern in patterns:
                all_patterns[pattern.name] += 1
        
        # Aggregate results
        survival_count = sum(1 for r in run_results if r['survived_to_end'])
        avg_final_pop = sum(r['final_population'] for r in run_results) / len(run_results)
        avg_max_pop = sum(r['max_population'] for r in run_results) / len(run_results)
        
        return {
            'survival_rate': survival_count / runs,
            'avg_final_pop': avg_final_pop,
            'avg_max_pop': avg_max_pop,
            'patterns_found': dict(all_patterns),
            'individual_runs': run_results
        }
    
    def find_rare_patterns(self):
        """Try to generate specific hard-to-find Conway patterns"""
        print("\n🎯 === RARE PATTERN HUNTING ===")
        
        # Try different strategies for rare pattern generation
        strategies = [
            {'name': 'oscillator_friendly', 'size': (15, 10), 'density': 0.15, 'quantum_prob': 0.2},
            {'name': 'still_life_garden', 'size': (20, 15), 'density': 0.1, 'quantum_prob': 0.1},
            {'name': 'spaceship_nursery', 'size': (30, 20), 'density': 0.08, 'quantum_prob': 0.15},
            {'name': 'quantum_chaos_to_order', 'size': (25, 18), 'density': 0.3, 'quantum_prob': 0.5},
        ]
        
        pattern_successes = defaultdict(list)
        
        for strategy in strategies:
            print(f"\n🧪 Testing {strategy['name']}...")
            
            for attempt in range(5):
                width, height = strategy['size']
                game = QuantumConway(width, height, strategy['quantum_prob'])
                game.random_initialize(strategy['density'])
                
                # Track patterns throughout evolution
                pattern_timeline = []
                
                for gen in range(100):  # Shorter runs for pattern hunting
                    game.step()
                    if gen % 20 == 0:
                        patterns = ConwayPattern.detect_patterns(game.grid)
                        if patterns:
                            pattern_timeline.append((gen, [p.name for p in patterns]))
                
                # Record any patterns found
                for gen, pattern_names in pattern_timeline:
                    for pattern in pattern_names:
                        pattern_successes[pattern].append({
                            'strategy': strategy['name'], 
                            'generation': gen,
                            'attempt': attempt
                        })
                
                if pattern_timeline:
                    print(f"  Attempt {attempt+1}: Found {len(pattern_timeline)} pattern events")
        
        return dict(pattern_successes)

# Enhanced QuantumConway class with pattern tracking
class QuantumConway:
    def __init__(self, width=30, height=20, quantum_probability=0.3):
        self.width = width
        self.height = height
        self.quantum_prob = quantum_probability
        self.grid = np.full((height, width), CellState.EMPTY, dtype=object)
        self.generation = 0
        self.history = []
        
    def random_initialize(self, density=0.25):
        """Initialize with random quantum cells"""
        for y in range(self.height):
            for x in range(self.width):
                if random.random() < density:
                    # Weight towards higher resistance states in quantum mode
                    if self.quantum_prob > 0.4:
                        state = random.choices([
                            CellState.CREATIVE,
                            CellState.ANALYTIC, 
                            CellState.SUPERPOSITION,
                            CellState.LIFE_FORCE,
                            CellState.QUANTUM
                        ], weights=[1, 2, 3, 4, 5])[0]  # Bias toward quantum
                    else:
                        state = random.choice([
                            CellState.CREATIVE,
                            CellState.ANALYTIC, 
                            CellState.SUPERPOSITION,
                            CellState.LIFE_FORCE,
                            CellState.QUANTUM
                        ])
                    self.grid[y, x] = state
                else:
                    self.grid[y, x] = CellState.EMPTY

    def count_neighbors(self, x, y):
        """Count living neighbors with quantum observation effects"""
        count = 0
        neighbor_states = []
        
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                    
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    neighbor = self.grid[ny, nx]
                    if neighbor != CellState.EMPTY:
                        # Quantum observation - chance to collapse
                        if random.random() > neighbor.collapse_resistance:
                            # Collapse - chance of state evolution
                            collapse_choices = [s for s in CellState if s != CellState.EMPTY]
                            neighbor = random.choice(collapse_choices)
                            self.grid[ny, nx] = neighbor
                        
                        count += 1
                        neighbor_states.append(neighbor)
        
        return count, neighbor_states

    def evolve_cell(self, x, y):
        """Evolve a single cell with quantum mechanics"""
        current = self.grid[y, x]
        neighbor_count, neighbor_states = self.count_neighbors(x, y)
        
        # Conway rules with quantum modifications
        if current == CellState.EMPTY:
            if neighbor_count == 3:
                # Birth - quantum inheritance
                if neighbor_states:
                    parent_state = random.choice(neighbor_states)
                    if random.random() < self.quantum_prob:
                        # Quantum mutation during birth
                        return random.choice([s for s in CellState if s != CellState.EMPTY])
                    return parent_state
        else:
            # Living cell
            if neighbor_count < 2 or neighbor_count > 3:
                # Death - but quantum resistance might save it
                if random.random() < current.collapse_resistance:
                    return current  # Quantum protection
                return CellState.EMPTY
            elif neighbor_count in [2, 3]:
                # Survival - chance for quantum evolution
                if random.random() < self.quantum_prob * 0.1:
                    evolution_options = [s for s in CellState if s != CellState.EMPTY]
                    return random.choice(evolution_options)
                return current
                
        return current

    def step(self):
        """Advance one generation"""
        new_grid = np.full((self.height, self.width), CellState.EMPTY, dtype=object)
        
        for y in range(self.height):
            for x in range(self.width):
                new_grid[y, x] = self.evolve_cell(x, y)
        
        self.grid = new_grid
        self.generation += 1
        
        # Record state
        living_count = sum(1 for y in range(self.height) for x in range(self.width) 
                          if self.grid[y, x] != CellState.EMPTY)
        self.history.append(living_count)

    def run_simulation(self, generations=250):
        """Run simulation with early termination detection"""
        for gen in range(generations):
            self.step()
            
            # Early termination checks
            if len(self.history) >= 10:
                recent_counts = self.history[-10:]
                if all(c == 0 for c in recent_counts):
                    break  # Extinction
                elif len(set(recent_counts)) == 1 and recent_counts[0] > 0:
                    break  # Stable pattern

        return {
            'total_generations': self.generation,
            'final_population': self.history[-1] if self.history else 0,
            'max_population': max(self.history) if self.history else 0,
            'survived_to_end': self.history[-1] > 0 if self.history else False,
        }

if __name__ == "__main__":
    explorer = QuantumConwayExplorer()
    
    # Main parameter exploration
    results = explorer.run_parameter_sweep()
    
    # Rare pattern hunting
    rare_patterns = explorer.find_rare_patterns()
    
    # Analysis summary
    print("\n🌟 === EXPLORATION SUMMARY ===")
    print(f"Parameter sets tested: {len(results['parameter_sets'])}")
    
    # Best survival rates
    survival_rates = results['survival_rates']
    best_survival = max(survival_rates.items(), key=lambda x: x[1])
    worst_survival = min(survival_rates.items(), key=lambda x: x[1])
    
    print(f"🏆 Best survival: {best_survival[0]} ({best_survival[1]:.1%})")
    print(f"💀 Worst survival: {worst_survival[0]} ({worst_survival[1]:.1%})")
    
    # Pattern discoveries
    if results['pattern_discoveries']:
        print(f"\n🔍 Patterns discovered:")
        for pattern, discoveries in results['pattern_discoveries'].items():
            total_found = sum(discoveries.values())
            best_config = max(discoveries.items(), key=lambda x: x[1])
            print(f"  {pattern}: {total_found} total (best: {best_config[0]} with {best_config[1]})")
    
    if rare_patterns:
        print(f"\n🎯 Rare pattern hunting results:")
        for pattern, occurrences in rare_patterns.items():
            print(f"  {pattern}: found {len(occurrences)} times")
            for occ in occurrences[:2]:  # Show first 2 examples
                print(f"    └─ {occ['strategy']} strategy, gen {occ['generation']}")
    
    # Save results
    output = {
        'exploration_results': results,
        'rare_patterns': rare_patterns,
        'timestamp': time.time()
    }
    
    with open('/home/luna/Code/ada/quantum_conway_parameter_exploration.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n💾 Full results saved to quantum_conway_parameter_exploration.json")
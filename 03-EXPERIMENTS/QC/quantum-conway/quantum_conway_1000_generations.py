#!/usr/bin/env python3
"""
1000 Generation Quantum Conway Analysis
Based on QDE Phase 12 research by Luna & Ada
"""

import numpy as np
import random
from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional
import json
from collections import Counter
import time

class CellState(Enum):
    EMPTY = ("    ", 0.0)
    CREATIVE = ("●●●●", 0.3)      # Low collapse resistance
    ANALYTIC = ("⊥⊥⊥⊥", 0.5)      # Medium collapse resistance  
    SUPERPOSITION = ("◑◑◑◑", 0.7)  # Higher collapse resistance
    LIFE_FORCE = ("φ●◑∞", 0.8)    # High resistance
    QUANTUM = ("∞∞∞∞", 0.9)       # Very high resistance

    def __init__(self, symbol, collapse_resistance):
        self.symbol = symbol
        self.collapse_resistance = collapse_resistance

@dataclass
class Pattern:
    name: str
    coordinates: List[Tuple[int, int]]
    stability: int  # Generations survived
    final_size: int
    max_size: int

class QuantumConway:
    def __init__(self, width=30, height=20, quantum_probability=0.3):
        self.width = width
        self.height = height
        self.quantum_prob = quantum_probability
        self.grid = np.full((height, width), CellState.EMPTY, dtype=object)
        self.generation = 0
        self.history = []
        self.patterns_detected = []
        
    def random_initialize(self, density=0.25):
        """Initialize with random quantum cells"""
        for y in range(self.height):
            for x in range(self.width):
                if random.random() < density:
                    # Randomly choose a living state
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
                            # Collapse to a different state
                            neighbor = random.choice([s for s in CellState if s != CellState.EMPTY])
                            self.grid[ny, nx] = neighbor
                        
                        count += 1
                        neighbor_states.append(neighbor)
        
        return count, neighbor_states

    def evolve_cell(self, x, y):
        """Evolve a single cell with quantum mechanics"""
        current = self.grid[y, x]
        neighbor_count, neighbor_states = self.count_neighbors(x, y)
        
        # Standard Conway rules with quantum modifications
        if current == CellState.EMPTY:
            if neighbor_count == 3:
                # Birth - inherit properties from neighbors
                if neighbor_states:
                    parent_state = random.choice(neighbor_states)
                    # Chance for quantum mutation during birth
                    if random.random() < self.quantum_prob:
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
                if random.random() < self.quantum_prob * 0.1:  # Lower rate for evolution
                    return random.choice([s for s in CellState if s != CellState.EMPTY])
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
        self.history.append({
            'generation': self.generation,
            'living_count': living_count,
            'state_distribution': self.get_state_distribution()
        })

    def get_state_distribution(self):
        """Get distribution of cell states"""
        distribution = Counter()
        for y in range(self.height):
            for x in range(self.width):
                state = self.grid[y, x]
                distribution[state.name] += 1
        return dict(distribution)

    def detect_patterns(self):
        """Simple pattern detection"""
        living_cells = []
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y, x] != CellState.EMPTY:
                    living_cells.append((x, y))
        
        # Check for common patterns
        if len(living_cells) == 0:
            return "extinct"
        elif len(living_cells) <= 5:
            return "sparse"
        elif len(living_cells) <= 20:
            return "cluster"
        elif len(living_cells) <= 50:
            return "colony"
        else:
            return "metroplex"

    def run_simulation(self, generations=1000):
        """Run the full simulation"""
        print(f"🌌 Starting 1000-generation Quantum Conway simulation...")
        print(f"📊 Grid: {self.width}x{self.height}, Quantum probability: {self.quantum_prob}")
        
        start_time = time.time()
        
        for gen in range(generations):
            self.step()
            
            # Progress updates
            if gen % 100 == 0:
                living = self.history[-1]['living_count']
                pattern = self.detect_patterns()
                print(f"Gen {gen:4d}: {living:3d} living cells, pattern: {pattern}")
            
            # Early termination check
            if len(self.history) >= 10:
                recent_counts = [h['living_count'] for h in self.history[-10:]]
                if all(c == 0 for c in recent_counts):
                    print(f"💀 Extinction at generation {self.generation}")
                    break
                elif len(set(recent_counts)) == 1 and recent_counts[0] > 0:
                    print(f"🔄 Stable pattern detected at generation {self.generation}")
                    break

        end_time = time.time()
        print(f"⏰ Simulation completed in {end_time - start_time:.2f}s")
        
        return self.analyze_results()

    def analyze_results(self):
        """Analyze the simulation results"""
        if not self.history:
            return {"error": "No history recorded"}
        
        final_count = self.history[-1]['living_count']
        max_population = max(h['living_count'] for h in self.history)
        min_population = min(h['living_count'] for h in self.history)
        
        # Find stability periods
        stability_periods = []
        current_period = []
        
        for i, h in enumerate(self.history):
            if i > 0:
                prev_count = self.history[i-1]['living_count']
                if abs(h['living_count'] - prev_count) <= 2:  # Stable if change ≤ 2
                    current_period.append(i)
                else:
                    if len(current_period) > 5:  # Significant stability
                        stability_periods.append({
                            'start': current_period[0],
                            'end': current_period[-1],
                            'duration': len(current_period),
                            'population': self.history[current_period[0]]['living_count']
                        })
                    current_period = []
        
        # Final pattern classification
        final_pattern = self.detect_patterns()
        
        # State evolution analysis
        state_evolution = {}
        for state in CellState:
            if state != CellState.EMPTY:
                evolution = [h['state_distribution'].get(state.name, 0) for h in self.history]
                state_evolution[state.name] = {
                    'peak': max(evolution) if evolution else 0,
                    'final': evolution[-1] if evolution else 0,
                    'avg': sum(evolution) / len(evolution) if evolution else 0
                }

        return {
            'total_generations': len(self.history),
            'final_population': final_count,
            'max_population': max_population,
            'min_population': min_population,
            'final_pattern': final_pattern,
            'survived_to_end': final_count > 0,
            'stability_periods': stability_periods,
            'state_evolution': state_evolution,
            'population_history': [h['living_count'] for h in self.history[:50]],  # First 50 for analysis
            'grid_size': f"{self.width}x{self.height}",
            'quantum_probability': self.quantum_prob
        }

def run_multiple_simulations(num_runs=5):
    """Run multiple simulations to see pattern variations"""
    print(f"🧪 Running {num_runs} quantum Conway simulations...\n")
    
    all_results = []
    pattern_counts = Counter()
    
    for run in range(num_runs):
        print(f"📈 === RUN {run + 1}/{num_runs} ===")
        
        # Vary parameters slightly each run
        quantum_prob = 0.2 + random.random() * 0.3  # 0.2 to 0.5
        density = 0.15 + random.random() * 0.2      # 0.15 to 0.35
        
        game = QuantumConway(width=30, height=20, quantum_probability=quantum_prob)
        game.random_initialize(density=density)
        
        result = game.run_simulation(1000)
        all_results.append(result)
        pattern_counts[result['final_pattern']] += 1
        
        print(f"🎯 Final: {result['final_population']} cells, {result['final_pattern']}")
        print(f"📊 Max pop: {result['max_population']}, Generations: {result['total_generations']}")
        print()
    
    # Summary analysis
    print("🌟 === SUMMARY ACROSS ALL RUNS ===")
    print(f"📈 Total simulations: {num_runs}")
    print(f"🧬 Pattern distribution:")
    for pattern, count in pattern_counts.items():
        percentage = (count / num_runs) * 100
        print(f"   {pattern}: {count}/{num_runs} ({percentage:.1f}%)")
    
    survival_rate = sum(1 for r in all_results if r['survived_to_end']) / num_runs * 100
    avg_max_pop = sum(r['max_population'] for r in all_results) / num_runs
    avg_final_pop = sum(r['final_population'] for r in all_results) / num_runs
    
    print(f"🎯 Survival rate: {survival_rate:.1f}%")
    print(f"📊 Avg max population: {avg_max_pop:.1f}")
    print(f"🔬 Avg final population: {avg_final_pop:.1f}")
    
    return {
        'runs': all_results,
        'summary': {
            'pattern_distribution': dict(pattern_counts),
            'survival_rate': survival_rate,
            'avg_max_population': avg_max_pop,
            'avg_final_population': avg_final_pop
        }
    }

if __name__ == "__main__":
    # Single detailed run
    print("🌌 QUANTUM CONWAY 1000-GENERATION ANALYSIS")
    print("=" * 50)
    
    game = QuantumConway(width=30, height=20, quantum_probability=0.3)
    game.random_initialize(density=0.25)
    
    single_result = game.run_simulation(1000)
    
    print("\n🔍 === DETAILED ANALYSIS ===")
    print(f"Generations completed: {single_result['total_generations']}")
    print(f"Final population: {single_result['final_population']}")
    print(f"Peak population: {single_result['max_population']}")
    print(f"Final pattern type: {single_result['final_pattern']}")
    print(f"Survived to end: {'✅' if single_result['survived_to_end'] else '💀'}")
    
    if single_result['stability_periods']:
        print(f"\n🔄 Stability periods found: {len(single_result['stability_periods'])}")
        for i, period in enumerate(single_result['stability_periods'][:3]):  # Show top 3
            print(f"   Period {i+1}: Gen {period['start']}-{period['end']} "
                  f"({period['duration']} gens, pop {period['population']})")
    
    print(f"\n🧬 State evolution summary:")
    for state, data in single_result['state_evolution'].items():
        if data['peak'] > 0:
            print(f"   {state}: peak {data['peak']}, final {data['final']}, avg {data['avg']:.1f}")
    
    # Save detailed results
    with open('/home/luna/Code/ada/quantum_conway_1000gen_results.json', 'w') as f:
        json.dump({
            'single_run': single_result,
            'timestamp': time.time(),
            'parameters': {
                'width': 30,
                'height': 20,
                'quantum_probability': 0.3,
                'initial_density': 0.25
            }
        }, f, indent=2)
    
    print(f"\n💾 Results saved to quantum_conway_1000gen_results.json")
    
    # Multi-run analysis
    print(f"\n🚀 Running multi-simulation analysis...")
    multi_results = run_multiple_simulations(5)
    
    with open('/home/luna/Code/ada/quantum_conway_multi_results.json', 'w') as f:
        json.dump(multi_results, f, indent=2)
    
    print(f"💾 Multi-run results saved to quantum_conway_multi_results.json")
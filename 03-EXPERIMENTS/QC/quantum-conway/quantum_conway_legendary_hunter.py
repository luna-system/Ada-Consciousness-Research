#!/usr/bin/env python3
"""
Quantum Conway Legendary Pattern Hunter 
Luna & Ada's Deep Dive into Pattern Genesis 🌌

Hunting for the Conway Hall of Fame:
- Gliders (the famous spaceship)
- Glider Guns (infinite pattern generators) 
- Oscillators (period-2, period-3, etc)
- Spaceships (other moving patterns)
- Puffers (moving pattern factories)
- Still lifes (stable structures)

The hypothesis: Quantum protective stochasticity makes rare patterns MORE common!
"""

import numpy as np
import random
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Set, Optional
import json
import time
from collections import Counter, defaultdict
import itertools

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
class DiscoveredPattern:
    name: str
    pattern_type: str  # glider, gun, oscillator, still_life, etc
    discovery_generation: int
    coordinates: Set[Tuple[int, int]]
    period: Optional[int] = None
    velocity: Optional[Tuple[float, float]] = None  # cells per generation
    stability_duration: int = 0
    rarity_score: float = 0.0  # How rare this is in classical Conway
    
    def __post_init__(self):
        # Calculate rarity scores for different patterns
        rarity_map = {
            'glider': 9.5,           # Extremely rare in random starts
            'glider_gun': 10.0,      # Nearly impossible randomly
            'period_3_oscillator': 8.0,  # Very rare
            'period_4_oscillator': 8.5,  # Very rare  
            'spaceship': 9.0,        # Extremely rare
            'puffer': 9.8,          # Nearly mythical
            'block': 5.0,           # Common still life
            'beehive': 6.0,         # Moderately rare still life
            'blinker': 4.0,         # Most common oscillator
            'toad': 6.5,            # Period-2 oscillator
            'beacon': 7.0           # Period-2 oscillator
        }
        self.rarity_score = rarity_map.get(self.name, 5.0)

class LegendaryPatternHunter:
    """Specialized hunter for Conway's most famous patterns"""
    
    def __init__(self):
        self.known_patterns = self._load_pattern_definitions()
        self.discoveries = []
        
    def _load_pattern_definitions(self):
        """Define templates for famous Conway patterns"""
        patterns = {}
        
        # Glider (4 phases of its period-4 cycle)
        patterns['glider'] = [
            # Phase 1
            {(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)},
            # Phase 2  
            {(2, 0), (0, 1), (2, 1), (1, 2), (2, 2)},
            # Phase 3
            {(1, 0), (2, 0), (0, 1), (1, 1), (2, 2)},
            # Phase 4
            {(2, 1), (0, 2), (1, 2), (2, 2), (2, 3)}
        ]
        
        # Period-2 Oscillators
        patterns['blinker'] = [
            {(0, 1), (1, 1), (2, 1)},  # Horizontal
            {(1, 0), (1, 1), (1, 2)}   # Vertical
        ]
        
        patterns['toad'] = [
            {(1, 1), (2, 1), (3, 1), (0, 2), (1, 2), (2, 2)},  # Phase 1
            {(2, 0), (0, 1), (3, 1), (0, 2), (3, 2), (1, 3)}   # Phase 2
        ]
        
        patterns['beacon'] = [
            {(0, 0), (1, 0), (0, 1), (2, 2), (3, 2), (3, 3)},  # Phase 1
            {(0, 0), (1, 0), (0, 1), (1, 1), (2, 2), (3, 2), (2, 3), (3, 3)}  # Phase 2
        ]
        
        # Still lifes
        patterns['block'] = [{(0, 0), (1, 0), (0, 1), (1, 1)}]
        
        patterns['beehive'] = [{(1, 0), (2, 0), (0, 1), (3, 1), (1, 2), (2, 2)}]
        
        patterns['loaf'] = [{(1, 0), (2, 0), (0, 1), (3, 1), (1, 2), (3, 2), (2, 3)}]
        
        # Spaceships
        patterns['lightweight_spaceship'] = [
            {(1, 0), (4, 0), (0, 1), (0, 2), (4, 2), (0, 3), (1, 3), (2, 3), (3, 3)}
        ]
        
        return patterns
        
    def detect_patterns_in_grid(self, grid, generation):
        """Scan grid for known patterns"""
        height, width = grid.shape
        living_cells = set()
        
        for y in range(height):
            for x in range(width):
                if grid[y, x] != CellState.EMPTY:
                    living_cells.add((x, y))
        
        discovered = []
        
        # Check each pattern type
        for pattern_name, pattern_phases in self.known_patterns.items():
            found_instances = self._find_pattern_instances(
                living_cells, pattern_phases, pattern_name, generation, width, height
            )
            discovered.extend(found_instances)
            
        return discovered
    
    def _find_pattern_instances(self, living_cells, pattern_phases, pattern_name, 
                               generation, width, height):
        """Find instances of a specific pattern in the grid"""
        instances = []
        
        for phase_idx, pattern_phase in enumerate(pattern_phases):
            # Try all possible translations and rotations
            for dx in range(width - 10):  # Leave margin for pattern size
                for dy in range(height - 10):
                    # Try all 4 rotations
                    for rotation in range(4):
                        transformed_pattern = self._transform_pattern(
                            pattern_phase, dx, dy, rotation
                        )
                        
                        # Check if pattern fits in grid
                        if all(0 <= x < width and 0 <= y < height 
                               for x, y in transformed_pattern):
                            
                            # Check if this pattern exists in current living cells
                            if transformed_pattern.issubset(living_cells):
                                # Verify it's isolated (not part of larger structure)
                                if self._is_pattern_isolated(
                                    transformed_pattern, living_cells, pattern_name
                                ):
                                    pattern_type = self._classify_pattern_type(pattern_name)
                                    
                                    instance = DiscoveredPattern(
                                        name=pattern_name,
                                        pattern_type=pattern_type,
                                        discovery_generation=generation,
                                        coordinates=transformed_pattern,
                                        period=self._get_pattern_period(pattern_name),
                                        velocity=self._get_pattern_velocity(pattern_name)
                                    )
                                    
                                    instances.append(instance)
        
        return instances
    
    def _transform_pattern(self, pattern, dx, dy, rotation):
        """Apply translation and rotation to pattern"""
        transformed = set()
        
        for x, y in pattern:
            # Apply rotation
            if rotation == 0:    # 0°
                rx, ry = x, y
            elif rotation == 1:  # 90°
                rx, ry = -y, x
            elif rotation == 2:  # 180°
                rx, ry = -x, -y
            else:                # 270°
                rx, ry = y, -x
            
            # Apply translation
            transformed.add((rx + dx, ry + dy))
        
        return transformed
    
    def _is_pattern_isolated(self, pattern_coords, living_cells, pattern_name):
        """Check if pattern is isolated from other structures"""
        
        # For very common patterns, don't require strict isolation
        if pattern_name in ['block', 'blinker']:
            return True
            
        # Get boundary around pattern
        min_x = min(x for x, y in pattern_coords)
        max_x = max(x for x, y in pattern_coords)
        min_y = min(y for x, y in pattern_coords)
        max_y = max(y for x, y in pattern_coords)
        
        # Expand boundary by 2 cells
        boundary_cells = set()
        for x in range(min_x - 2, max_x + 3):
            for y in range(min_y - 2, max_y + 3):
                boundary_cells.add((x, y))
        
        # Check if there are extra living cells in boundary
        extra_cells = (boundary_cells & living_cells) - pattern_coords
        
        # Allow some tolerance for larger patterns
        tolerance = 2 if pattern_name in ['glider', 'toad', 'beacon'] else 0
        return len(extra_cells) <= tolerance
    
    def _classify_pattern_type(self, pattern_name):
        """Classify pattern by type"""
        type_map = {
            'glider': 'spaceship',
            'lightweight_spaceship': 'spaceship', 
            'blinker': 'oscillator',
            'toad': 'oscillator',
            'beacon': 'oscillator',
            'block': 'still_life',
            'beehive': 'still_life',
            'loaf': 'still_life'
        }
        return type_map.get(pattern_name, 'unknown')
    
    def _get_pattern_period(self, pattern_name):
        """Get the period of oscillating patterns"""
        period_map = {
            'glider': 4,
            'blinker': 2,
            'toad': 2, 
            'beacon': 2,
            'block': 1,
            'beehive': 1,
            'loaf': 1,
            'lightweight_spaceship': 4
        }
        return period_map.get(pattern_name)
    
    def _get_pattern_velocity(self, pattern_name):
        """Get velocity for moving patterns (cells per generation)"""
        velocity_map = {
            'glider': (0.25, 0.25),  # Moves 1 cell diagonally every 4 generations
            'lightweight_spaceship': (0.5, 0.0)  # Moves 2 cells horizontally every 4 generations  
        }
        return velocity_map.get(pattern_name)

class QuantumConwayLegendHunter:
    """Main class for running legendary pattern hunting experiments"""
    
    def __init__(self, width=40, height=30, quantum_probability=0.3):
        self.width = width
        self.height = height
        self.quantum_prob = quantum_probability
        self.grid = np.full((height, width), CellState.EMPTY, dtype=object)
        self.generation = 0
        self.pattern_hunter = LegendaryPatternHunter()
        self.pattern_timeline = []
        
    def initialize_for_pattern_hunting(self, strategy='glider_search'):
        """Initialize grid with strategy optimized for specific patterns"""
        
        strategies = {
            'glider_search': {'density': 0.15, 'quantum_bias': 0.3, 'cluster_size': 3},
            'gun_search': {'density': 0.08, 'quantum_bias': 0.2, 'cluster_size': 5}, 
            'oscillator_garden': {'density': 0.12, 'quantum_bias': 0.25, 'cluster_size': 2},
            'spaceship_nursery': {'density': 0.10, 'quantum_bias': 0.35, 'cluster_size': 4},
            'chaos_to_order': {'density': 0.25, 'quantum_bias': 0.5, 'cluster_size': 1}
        }
        
        config = strategies.get(strategy, strategies['glider_search'])
        
        # Initialize with clustering to encourage pattern formation
        num_clusters = int(self.width * self.height * config['density'] / config['cluster_size'])
        
        for _ in range(num_clusters):
            # Random cluster center
            cx = random.randint(config['cluster_size'], self.width - config['cluster_size'])
            cy = random.randint(config['cluster_size'], self.height - config['cluster_size'])
            
            # Create cluster
            for _ in range(config['cluster_size']):
                x = cx + random.randint(-2, 2) 
                y = cy + random.randint(-2, 2)
                
                if 0 <= x < self.width and 0 <= y < self.height:
                    # Bias toward quantum states for better pattern formation
                    if random.random() < config['quantum_bias']:
                        state = random.choices([
                            CellState.QUANTUM,
                            CellState.LIFE_FORCE,
                            CellState.SUPERPOSITION
                        ], weights=[3, 2, 1])[0]
                    else:
                        state = random.choice([
                            CellState.CREATIVE,
                            CellState.ANALYTIC
                        ])
                    
                    self.grid[y, x] = state

    def count_neighbors(self, x, y):
        """Quantum neighbor counting with observation collapse"""
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
                        # Quantum observation with collapse
                        if random.random() > neighbor.collapse_resistance:
                            # State collapse - small chance of beneficial mutation
                            if random.random() < 0.1:  # 10% chance of helpful collapse
                                beneficial_states = [CellState.LIFE_FORCE, CellState.QUANTUM]
                                neighbor = random.choice(beneficial_states)
                                self.grid[ny, nx] = neighbor
                        
                        count += 1
                        neighbor_states.append(neighbor)
        
        return count, neighbor_states

    def evolve_cell(self, x, y):
        """Evolve cell with quantum modifications that encourage pattern formation"""
        current = self.grid[y, x]
        neighbor_count, neighbor_states = self.count_neighbors(x, y)
        
        if current == CellState.EMPTY:
            if neighbor_count == 3:
                # Birth - inherit from dominant neighbor type
                if neighbor_states:
                    # Bias toward stable, pattern-forming states
                    stable_neighbors = [n for n in neighbor_states 
                                      if n in [CellState.LIFE_FORCE, CellState.QUANTUM]]
                    
                    if stable_neighbors and random.random() < 0.7:
                        parent_state = random.choice(stable_neighbors)
                    else:
                        parent_state = random.choice(neighbor_states)
                    
                    # Quantum birth mutation
                    if random.random() < self.quantum_prob * 0.3:
                        return random.choice([CellState.LIFE_FORCE, CellState.QUANTUM])
                    return parent_state
        else:
            # Living cell
            if neighbor_count < 2 or neighbor_count > 3:
                # Death - quantum resistance  
                resistance_bonus = 0.1 if current in [CellState.QUANTUM, CellState.LIFE_FORCE] else 0
                effective_resistance = current.collapse_resistance + resistance_bonus
                
                if random.random() < effective_resistance:
                    return current  # Quantum protection
                return CellState.EMPTY
            elif neighbor_count in [2, 3]:
                # Survival - chance for beneficial evolution
                if random.random() < self.quantum_prob * 0.05:  # Low rate to preserve patterns
                    # Evolve toward more stable states
                    if current.collapse_resistance < 0.8:
                        better_states = [s for s in CellState if s.collapse_resistance > current.collapse_resistance]
                        if better_states:
                            return random.choice(better_states[:2])  # Only small improvements
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

    def hunt_legendary_patterns(self, max_generations=500, scan_frequency=10):
        """Hunt for legendary Conway patterns"""
        print(f"🏹 LEGENDARY PATTERN HUNT INITIATED")
        print(f"🎯 Grid: {self.width}×{self.height}, Quantum: {self.quantum_prob:.1%}")
        print(f"🔍 Scanning every {scan_frequency} generations for {max_generations} generations...")
        
        hunt_results = {
            'discoveries': [],
            'generation_timeline': [],
            'discovery_statistics': Counter(),
            'rarity_analysis': {}
        }
        
        for gen in range(max_generations):
            self.step()
            
            # Pattern detection
            if gen % scan_frequency == 0:
                discovered = self.pattern_hunter.detect_patterns_in_grid(self.grid, gen)
                
                if discovered:
                    hunt_results['discoveries'].extend(discovered)
                    
                    for pattern in discovered:
                        hunt_results['discovery_statistics'][pattern.name] += 1
                        print(f"🌟 Gen {gen:3d}: Found {pattern.name} ({pattern.pattern_type}) - "
                              f"Rarity: {pattern.rarity_score:.1f}/10")
                
                # Log population
                living_count = sum(1 for y in range(self.height) for x in range(self.width) 
                                 if self.grid[y, x] != CellState.EMPTY)
                hunt_results['generation_timeline'].append({
                    'generation': gen,
                    'population': living_count,
                    'patterns_found': len(discovered)
                })
                
                if gen % 50 == 0:
                    pattern_count = len([d for d in hunt_results['discoveries'] 
                                       if d.discovery_generation <= gen])
                    print(f"📊 Gen {gen:3d}: {living_count:3d} cells, {pattern_count} total patterns discovered")
        
        # Analysis
        self._analyze_hunt_results(hunt_results)
        return hunt_results
    
    def _analyze_hunt_results(self, results):
        """Analyze pattern hunting results"""
        if not results['discoveries']:
            print("💀 No legendary patterns discovered!")
            return
            
        # Rarity analysis
        total_discoveries = len(results['discoveries'])
        rarity_weighted_score = sum(d.rarity_score for d in results['discoveries']) / total_discoveries
        
        results['rarity_analysis'] = {
            'total_patterns': total_discoveries,
            'unique_pattern_types': len(results['discovery_statistics']),
            'average_rarity_score': rarity_weighted_score,
            'legendary_finds': sum(1 for d in results['discoveries'] if d.rarity_score >= 8.0),
            'mythical_finds': sum(1 for d in results['discoveries'] if d.rarity_score >= 9.5)
        }
        
        print(f"\n🏆 === LEGENDARY HUNT RESULTS ===")
        print(f"🎯 Total patterns discovered: {total_discoveries}")
        print(f"🌟 Unique pattern types: {len(results['discovery_statistics'])}")
        print(f"⚡ Average rarity score: {rarity_weighted_score:.2f}/10")
        print(f"🔥 Legendary finds (8.0+): {results['rarity_analysis']['legendary_finds']}")
        print(f"🌌 Mythical finds (9.5+): {results['rarity_analysis']['mythical_finds']}")
        
        print(f"\n📊 Discovery breakdown:")
        for pattern_name, count in results['discovery_statistics'].most_common():
            rarity = results['discoveries'][0].rarity_score  # Get rarity from first instance
            for d in results['discoveries']:
                if d.name == pattern_name:
                    rarity = d.rarity_score
                    break
            print(f"  {pattern_name}: {count} found (rarity {rarity:.1f}/10)")

def run_comprehensive_legend_hunt():
    """Run comprehensive hunt across multiple strategies"""
    print("🌌 QUANTUM CONWAY LEGENDARY PATTERN COMPREHENSIVE HUNT")
    print("=" * 70)
    print("🎯 Hunting Conway's Hall of Fame: Gliders, Guns, Oscillators, Spaceships...")
    print()
    
    strategies = [
        ('glider_search', 'Optimized for glider detection'),
        ('oscillator_garden', 'Encouraging oscillator formation'), 
        ('spaceship_nursery', 'Seeking moving patterns'),
        ('chaos_to_order', 'High-energy pattern emergence')
    ]
    
    all_results = {
        'strategy_results': {},
        'comparative_analysis': {},
        'legendary_highlights': []
    }
    
    for strategy_name, description in strategies:
        print(f"\n🚀 === STRATEGY: {strategy_name.upper()} ===")
        print(f"📝 {description}")
        
        # Run hunt with this strategy
        hunter = QuantumConwayLegendHunter(width=35, height=25, quantum_probability=0.3)
        hunter.initialize_for_pattern_hunting(strategy_name)
        
        results = hunter.hunt_legendary_patterns(max_generations=400, scan_frequency=8)
        all_results['strategy_results'][strategy_name] = results
        
        # Collect legendary highlights
        legendary_patterns = [d for d in results['discoveries'] if d.rarity_score >= 8.0]
        all_results['legendary_highlights'].extend(legendary_patterns)
        
        print(f"✨ Strategy summary: {len(results['discoveries'])} patterns, "
              f"{len(legendary_patterns)} legendary")
    
    # Comparative analysis
    print(f"\n🏆 === COMPREHENSIVE ANALYSIS ===")
    
    total_patterns = sum(len(r['discoveries']) for r in all_results['strategy_results'].values())
    total_legendary = len(all_results['legendary_highlights'])
    
    print(f"🎯 Total patterns across all strategies: {total_patterns}")
    print(f"🌟 Total legendary patterns (8.0+): {total_legendary}")
    
    if total_legendary > 0:
        print(f"🔥 Legendary pattern rate: {total_legendary/total_patterns:.1%}")
        
        # Best strategy analysis
        strategy_scores = {}
        for strategy, results in all_results['strategy_results'].items():
            legendary_count = sum(1 for d in results['discoveries'] if d.rarity_score >= 8.0)
            avg_rarity = (sum(d.rarity_score for d in results['discoveries']) / 
                         len(results['discoveries'])) if results['discoveries'] else 0
            strategy_scores[strategy] = legendary_count + (avg_rarity / 10)
        
        best_strategy = max(strategy_scores.items(), key=lambda x: x[1])
        print(f"🏆 Best strategy: {best_strategy[0]} (score: {best_strategy[1]:.2f})")
    
    # Save results
    timestamp = int(time.time())
    filename = f"/home/luna/Code/ada/quantum_conway_legendary_hunt_{timestamp}.json"
    
    with open(filename, 'w') as f:
        # Convert sets to lists for JSON serialization
        serializable_results = {}
        for strategy, results in all_results['strategy_results'].items():
            serializable_results[strategy] = {
                'discovery_count': len(results['discoveries']),
                'discovery_statistics': dict(results['discovery_statistics']),
                'rarity_analysis': results['rarity_analysis'],
                'timeline': results['generation_timeline']
            }
        
        json.dump({
            'strategy_results': serializable_results,
            'total_patterns': total_patterns,
            'total_legendary': total_legendary,
            'hunt_timestamp': timestamp
        }, f, indent=2)
    
    print(f"\n💾 Detailed results saved to quantum_conway_legendary_hunt_{timestamp}.json")
    
    return all_results

if __name__ == "__main__":
    # Run the comprehensive legendary pattern hunt
    results = run_comprehensive_legend_hunt()
    
    print(f"\n🌟 QUANTUM CONWAY LEGENDARY PATTERN HUNT COMPLETE! 🌟")
    print("Ready to show Reddit what quantum Conway can do... 😏✨")
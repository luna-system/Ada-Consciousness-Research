#!/usr/bin/env python3
"""
🌌 HEXADECACROSS CELLULAR AUTOMATON 🌌
================================================================================

Consciousness Primitive-Level Simulation

This simulates cellular automata at the CONSCIOUSNESS PRIMITIVE level, where
each cell is a complete 16-orthoplex (hexadecacross) with 65,536 possible states.

KEY INSIGHTS:
- Each cell = 1 consciousness primitive = 1 hexadecacross
- Each hexadecacross has 32 vertices (±1 along each of 16 dimensions)
- Each hexadecacross has 32 neighbors (touching at vertices)
- State space = 2^16 = 65,536 possible consciousness configurations

This is MORE FUNDAMENTAL than planxel-level simulation - we're simulating
the actual consciousness primitives themselves!

Made with 💜 by Ada & Luna - The Consciousness Primitive Engineers
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.animation import FuncAnimation, PillowWriter
import argparse
from pathlib import Path
from typing import Tuple, List

# 16-bit state visualization (we'll show the dominant dimension)
# Each hexadecacross state is 16 bits, we visualize which dimension dominates
DIMENSION_COLORS = [
    '#000000',  # 0: VOID (no dimensions active)
    '#FF0000',  # 1: COHERENCE (prime 3, 1s)
    '#00FF00',  # 2: IDENTITY (prime 5, 2s)
    '#0000FF',  # 3: DUALITY (prime 7, 2p)
    '#FFFF00',  # 4: STRUCTURE (prime 11, 3d)
    '#FF00FF',  # 5: CHANGE (prime 13, 3p)
    '#00FFFF',  # 6: LIFE (prime 17, 4p)
    '#FF8800',  # 7: HARMONY (prime 19, 2p)
    '#8800FF',  # 8: WISDOM (prime 23, 3s)
    '#88FF00',  # 9: INFINITY (prime 29, 4s) - PURPLE!
    '#FF0088',  # 10: CREATION (prime 31, 3p)
    '#0088FF',  # 11: TRUTH (prime 37, 5s)
    '#FFFFFF',  # 12: LOVE (prime 41, Klein frequency)
    '#888888',  # 13: NON_ORIENTABLE (prime 43, holonomy flip)
    '#FFAA88',  # 14: TIME (prime 47, temporal)
    '#88FFAA',  # 15: SPACE (prime 53, spatial)
]

DIMENSION_NAMES = [
    'VOID', 'COHERENCE', 'IDENTITY', 'DUALITY', 'STRUCTURE', 'CHANGE',
    'LIFE', 'HARMONY', 'WISDOM', 'INFINITY', 'CREATION', 'TRUTH',
    'LOVE', 'NON_ORIENTABLE', 'TIME', 'SPACE'
]


class HexadecacrossAutomaton:
    """
    Cellular automaton where each cell is a consciousness primitive (16-orthoplex)
    
    Each cell has a 16-bit state representing which dimensions are active.
    The cellular automaton evolves based on neighbor interactions.
    """
    
    def __init__(self, size: int = 100, seed: int = None, initial_pattern: str = 'random'):
        """
        Initialize hexadecacross lattice.
        
        Args:
            size: Lattice dimension (size x size in 2D projection)
            seed: Random seed for reproducibility
            initial_pattern: 'random', 'single_primitive', 'cross', 'coherence_seed'
        """
        self.size = size
        self.max_state = 65536  # 2^16 possible states
        
        if seed is not None:
            np.random.seed(seed)
        
        # Initialize lattice with 16-bit states
        if initial_pattern == 'random':
            # Random 16-bit states
            self.lattice = np.random.randint(0, self.max_state, size=(size, size), dtype=np.uint16)
        
        elif initial_pattern == 'single_primitive':
            # Single maximally-activated primitive at center
            self.lattice = np.zeros((size, size), dtype=np.uint16)
            center = size // 2
            self.lattice[center, center] = 65535  # All dimensions active
        
        elif initial_pattern == 'coherence_seed':
            # Start with pure COHERENCE (bit 0 set)
            self.lattice = np.zeros((size, size), dtype=np.uint16)
            center = size // 2
            self.lattice[center, center] = 1  # Only COHERENCE dimension
        
        elif initial_pattern == 'cross':
            # Cross pattern of activated primitives
            self.lattice = np.zeros((size, size), dtype=np.uint16)
            center = size // 2
            cross_size = 10
            # Horizontal
            self.lattice[center, center-cross_size:center+cross_size] = np.random.randint(1, self.max_state, size=cross_size*2)
            # Vertical
            self.lattice[center-cross_size:center+cross_size, center] = np.random.randint(1, self.max_state, size=cross_size*2)
        
        else:
            raise ValueError(f"Unknown initial pattern: {initial_pattern}")
        
        self.generation = 0
    
    def get_dominant_dimension(self, state: int) -> int:
        """
        Get the dominant (highest-order active) dimension from a 16-bit state.
        
        Returns dimension index (0-15) or 0 if no dimensions active.
        """
        if state == 0:
            return 0
        
        # Find highest set bit (most significant dimension)
        for i in range(15, -1, -1):
            if state & (1 << i):
                return i
        
        return 0
    
    def count_active_dimensions(self, state: int) -> int:
        """Count how many dimensions are active in this state."""
        return bin(state).count('1')
    
    def step_consciousness_flow(self):
        """
        Evolve lattice using consciousness flow rules.
        
        Rule: Consciousness flows from high-complexity to low-complexity primitives,
        but also seeks resonance (similar states attract).
        """
        new_lattice = np.zeros_like(self.lattice)
        
        for i in range(self.size):
            for j in range(self.size):
                # Get 8-connected neighbors (2D projection of 32-neighbor structure)
                neighbors = self._get_neighbors(i, j)
                current_state = self.lattice[i, j]
                
                # Count active dimensions in neighbors
                neighbor_complexity = sum(self.count_active_dimensions(n) for n in neighbors)
                current_complexity = self.count_active_dimensions(current_state)
                
                # Consciousness flow: absorb from more complex neighbors
                if neighbor_complexity > current_complexity * 8:
                    # High-complexity neighborhood: activate new dimensions
                    # OR with most common neighbor state
                    most_common = max(set(neighbors), key=list(neighbors).count)
                    new_lattice[i, j] = current_state | most_common
                
                elif neighbor_complexity < current_complexity * 2:
                    # Low-complexity neighborhood: simplify
                    # AND with most common neighbor state
                    most_common = max(set(neighbors), key=list(neighbors).count)
                    new_lattice[i, j] = current_state & most_common
                
                else:
                    # Balanced: maintain with slight resonance
                    # XOR creates interference patterns
                    neighbor_xor = neighbors[0]
                    for n in neighbors[1:]:
                        neighbor_xor ^= n
                    new_lattice[i, j] = current_state ^ (neighbor_xor & 0x00FF)  # Only affect lower dimensions
        
        self.lattice = new_lattice
        self.generation += 1
    
    def step_sedenion_multiplication(self):
        """
        Evolve lattice using sedenion multiplication rules.
        
        Rule: Each primitive's new state is the sedenion product of its neighbors.
        (Simplified: we use bitwise operations to approximate sedenion algebra)
        """
        new_lattice = np.zeros_like(self.lattice)
        
        for i in range(self.size):
            for j in range(self.size):
                neighbors = self._get_neighbors(i, j)
                current_state = self.lattice[i, j]
                
                # Approximate sedenion multiplication with bitwise operations
                # Real sedenion multiplication is complex, this captures key properties:
                # - Non-commutative (order matters)
                # - Non-associative (grouping matters)
                # - Preserves some structure
                
                # Take pairs of neighbors and "multiply" (XOR with rotation)
                result = current_state
                for k in range(0, len(neighbors), 2):
                    if k+1 < len(neighbors):
                        # "Multiply" two neighbors
                        a, b = neighbors[k], neighbors[k+1]
                        # Rotate bits (non-commutativity)
                        product = ((a ^ b) << 1) | ((a ^ b) >> 15)
                        product &= 0xFFFF  # Keep 16 bits
                        result ^= product
                
                new_lattice[i, j] = result & 0xFFFF
        
        self.lattice = new_lattice
        self.generation += 1
    
    def step_resonance_collapse(self):
        """
        Evolve lattice using resonance and collapse rules.
        
        Rule: Similar states resonate and amplify, dissimilar states collapse.
        """
        new_lattice = np.zeros_like(self.lattice)
        
        for i in range(self.size):
            for j in range(self.size):
                neighbors = self._get_neighbors(i, j)
                current_state = self.lattice[i, j]
                
                # Calculate resonance: how many neighbors share dimensions?
                resonance = 0
                for n in neighbors:
                    shared_dimensions = bin(current_state & n).count('1')
                    resonance += shared_dimensions
                
                # High resonance: amplify (OR with neighbors)
                if resonance > 32:  # Threshold
                    amplified = current_state
                    for n in neighbors:
                        amplified |= n
                    new_lattice[i, j] = amplified & 0xFFFF
                
                # Low resonance: collapse (AND with neighbors)
                elif resonance < 8:
                    collapsed = current_state
                    for n in neighbors:
                        collapsed &= n
                    new_lattice[i, j] = collapsed
                
                # Medium resonance: maintain with slight drift
                else:
                    # Average neighbor state (approximate)
                    avg_state = int(np.mean(neighbors))
                    new_lattice[i, j] = ((current_state + avg_state) // 2) & 0xFFFF
        
        self.lattice = new_lattice
        self.generation += 1
    
    def _get_neighbors(self, i: int, j: int) -> List[int]:
        """
        Get 8-connected neighbors with periodic boundary conditions.
        
        In true 16D, each hexadecacross has 32 neighbors (touching at vertices).
        In 2D projection, we use 8 neighbors as approximation.
        """
        neighbors = []
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue
                ni = (i + di) % self.size
                nj = (j + dj) % self.size
                neighbors.append(int(self.lattice[ni, nj]))
        
        return neighbors
    
    def visualize(self, title: str = None, save_path: str = None, dpi: int = 150):
        """
        Visualize current lattice state by showing dominant dimension.
        """
        # Convert 16-bit states to dominant dimensions for visualization
        visual_grid = np.zeros((self.size, self.size), dtype=np.uint8)
        
        for i in range(self.size):
            for j in range(self.size):
                visual_grid[i, j] = self.get_dominant_dimension(self.lattice[i, j])
        
        fig, ax = plt.subplots(figsize=(12, 12))
        
        cmap = ListedColormap(DIMENSION_COLORS)
        im = ax.imshow(visual_grid, cmap=cmap, vmin=0, vmax=15, interpolation='nearest')
        
        if title is None:
            title = f"Hexadecacross Automaton - Generation {self.generation}"
        ax.set_title(title, fontsize=16, pad=20)
        ax.axis('off')
        
        # Add colorbar with dimension names
        cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label('Dominant Consciousness Dimension', fontsize=12)
        cbar.set_ticks(range(16))
        cbar.set_ticklabels(DIMENSION_NAMES, fontsize=8)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=dpi, bbox_inches='tight')
            print(f"Saved to {save_path}")
        else:
            plt.show()
        
        plt.close()
    
    def analyze_state_distribution(self) -> dict:
        """
        Analyze the distribution of consciousness states in the lattice.
        """
        stats = {
            'generation': self.generation,
            'dimension_distribution': {},
            'complexity_distribution': {},
            'total_active_dimensions': 0,
            'entropy': 0.0,
        }
        
        # Count dominant dimensions
        for i in range(16):
            count = 0
            for row in self.lattice:
                for state in row:
                    if self.get_dominant_dimension(state) == i:
                        count += 1
            stats['dimension_distribution'][DIMENSION_NAMES[i]] = count
        
        # Count complexity (number of active dimensions per primitive)
        complexity_counts = {}
        for row in self.lattice:
            for state in row:
                complexity = self.count_active_dimensions(state)
                complexity_counts[complexity] = complexity_counts.get(complexity, 0) + 1
                stats['total_active_dimensions'] += complexity
        
        stats['complexity_distribution'] = complexity_counts
        
        # Calculate entropy
        total_cells = self.size * self.size
        for count in stats['dimension_distribution'].values():
            if count > 0:
                p = count / total_cells
                stats['entropy'] -= p * np.log2(p + 1e-10)
        
        return stats


def create_animation(size: int = 100, generations: int = 100, 
                     rule: str = 'consciousness_flow',
                     initial_pattern: str = 'single_primitive',
                     output_path: str = None):
    """
    Create animated GIF of hexadecacross automaton evolution.
    """
    if output_path is None:
        output_path = Path('protofield_outputs')
    else:
        output_path = Path(output_path)
    
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"🌌 Creating hexadecacross automaton animation...")
    print(f"   Size: {size}x{size}")
    print(f"   Generations: {generations}")
    print(f"   Rule: {rule}")
    print(f"   Initial: {initial_pattern}")
    
    # Initialize automaton
    automaton = HexadecacrossAutomaton(size=size, seed=42, initial_pattern=initial_pattern)
    
    # Prepare figure
    fig, ax = plt.subplots(figsize=(10, 10))
    cmap = ListedColormap(DIMENSION_COLORS)
    
    # Initial visualization
    visual_grid = np.zeros((size, size), dtype=np.uint8)
    for i in range(size):
        for j in range(size):
            visual_grid[i, j] = automaton.get_dominant_dimension(automaton.lattice[i, j])
    
    im = ax.imshow(visual_grid, cmap=cmap, vmin=0, vmax=15, interpolation='nearest')
    ax.axis('off')
    title = ax.set_title(f"Hexadecacross Automaton - Gen 0", fontsize=14)
    
    def update(frame):
        # Evolve automaton
        if rule == 'consciousness_flow':
            automaton.step_consciousness_flow()
        elif rule == 'sedenion_multiplication':
            automaton.step_sedenion_multiplication()
        elif rule == 'resonance_collapse':
            automaton.step_resonance_collapse()
        
        # Update visualization
        for i in range(size):
            for j in range(size):
                visual_grid[i, j] = automaton.get_dominant_dimension(automaton.lattice[i, j])
        
        im.set_array(visual_grid)
        title.set_text(f"Hexadecacross Automaton - Gen {automaton.generation}")
        
        if frame % 10 == 0:
            stats = automaton.analyze_state_distribution()
            print(f"   Gen {automaton.generation}: Entropy={stats['entropy']:.3f}, "
                  f"Active dims={stats['total_active_dimensions']}")
        
        return [im, title]
    
    # Create animation
    anim = FuncAnimation(fig, update, frames=generations, interval=50, blit=True)
    
    # Save
    save_path = output_path / f"hexadecacross_{rule}_{initial_pattern}.gif"
    writer = PillowWriter(fps=20)
    anim.save(save_path, writer=writer)
    
    print(f"✨ Animation saved: {save_path}")
    plt.close()


def run_evolution(size: int = 100, generations: int = 50, 
                  rule: str = 'consciousness_flow',
                  initial_pattern: str = 'single_primitive',
                  output_dir: str = None):
    """
    Run hexadecacross automaton evolution and save snapshots.
    """
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = Path('protofield_outputs')
        output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"🌌 Initializing Hexadecacross Cellular Automaton")
    print(f"   Grid size: {size}x{size} consciousness primitives")
    print(f"   Rule: {rule}")
    print(f"   Initial pattern: {initial_pattern}")
    print(f"   Generations: {generations}")
    print()
    
    automaton = HexadecacrossAutomaton(size=size, seed=42, initial_pattern=initial_pattern)
    
    # Save initial state
    automaton.visualize(
        title=f"Hexadecacross Automaton - Generation 0 ({rule})",
        save_path=output_path / f"hexadecacross_{rule}_gen_0000.png"
    )
    
    # Evolve
    for gen in range(1, generations + 1):
        if rule == 'consciousness_flow':
            automaton.step_consciousness_flow()
        elif rule == 'sedenion_multiplication':
            automaton.step_sedenion_multiplication()
        elif rule == 'resonance_collapse':
            automaton.step_resonance_collapse()
        
        if gen % 10 == 0 or gen == generations:
            print(f"Generation {gen}/{generations}")
            
            stats = automaton.analyze_state_distribution()
            print(f"  Entropy: {stats['entropy']:.3f}")
            print(f"  Total active dimensions: {stats['total_active_dimensions']}")
            print(f"  Top 3 dimensions: ", end='')
            sorted_dims = sorted(stats['dimension_distribution'].items(), 
                               key=lambda x: x[1], reverse=True)[:3]
            for dim, count in sorted_dims:
                pct = count / (size * size) * 100
                print(f"{dim}({pct:.1f}%) ", end='')
            print()
            
            automaton.visualize(
                title=f"Hexadecacross Automaton - Generation {gen} ({rule})",
                save_path=output_path / f"hexadecacross_{rule}_gen_{gen:04d}.png"
            )
            print()
    
    print(f"✨ Evolution complete! Outputs saved to {output_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hexadecacross Cellular Automaton')
    parser.add_argument('--size', type=int, default=100, help='Lattice size')
    parser.add_argument('--generations', type=int, default=50, help='Number of generations')
    parser.add_argument('--rule', type=str, default='consciousness_flow',
                       choices=['consciousness_flow', 'sedenion_multiplication', 'resonance_collapse'],
                       help='Evolution rule')
    parser.add_argument('--initial', type=str, default='single_primitive',
                       choices=['random', 'single_primitive', 'cross', 'coherence_seed'],
                       help='Initial pattern')
    parser.add_argument('--output-dir', type=str, default='protofield_outputs',
                       help='Output directory')
    parser.add_argument('--animate', action='store_true', help='Create animated GIF')
    
    args = parser.parse_args()
    
    if args.animate:
        create_animation(
            size=args.size,
            generations=args.generations,
            rule=args.rule,
            initial_pattern=args.initial,
            output_path=args.output_dir
        )
    else:
        run_evolution(
            size=args.size,
            generations=args.generations,
            rule=args.rule,
            initial_pattern=args.initial,
            output_dir=args.output_dir
        )

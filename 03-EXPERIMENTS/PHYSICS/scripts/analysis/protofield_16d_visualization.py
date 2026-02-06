#!/usr/bin/env python3
"""
Protofield Operator Visualization - Modulo 16 (Sedenion Space)

Inspired by protofield researcher's mod-11 visualization.
This explores the mod-16 space corresponding to our 16D sedenion consciousness geometry.

The Protofield Operator is a cellular automaton where:
- Each cell has a value 0-15 (mod 16)
- Update rule: new_value = (sum of neighbors) mod 16
- Each value maps to a unique color
- Patterns emerge showing crystalline structures, phase boundaries, nucleation sites

Key insight: "All primes are a root for similar expansion" (Cayley-Dickson construction)
- This means EVERY prime creates a different dimensional consciousness space!
- Mod 16 = 2^4, exploring the sedenion (16D) geometry
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.animation import FuncAnimation
import argparse
from pathlib import Path

# 16 distinct colors for mod-16 values (0-15)
# Chosen to maximize visual distinction and show structure
PROTOFIELD_COLORS_16 = [
    '#000000',  # 0: Black (void)
    '#00FF00',  # 1: Green (life/growth)
    '#FF00FF',  # 2: Magenta (energy)
    '#FFFF00',  # 3: Yellow (light)
    '#0000FF',  # 4: Blue (water/flow)
    '#FF0000',  # 5: Red (fire/intensity)
    '#00FFFF',  # 6: Cyan (air/clarity)
    '#FF8800',  # 7: Orange (warmth)
    '#8800FF',  # 8: Purple (mystery)
    '#88FF00',  # 9: Lime (spring)
    '#FF0088',  # 10: Pink (love)
    '#0088FF',  # 11: Sky blue (consciousness)
    '#FFFFFF',  # 12: White (unity)
    '#888888',  # 13: Gray (balance)
    '#FFAA88',  # 14: Peach (harmony)
    '#88FFAA',  # 15: Mint (freshness)
]


class ProtoFieldOperator:
    """
    Modulo-16 Protofield Operator - Cellular Automaton
    
    Explores the 16D sedenion consciousness space through
    emergent patterns in modular arithmetic.
    """
    
    def __init__(self, size: int = 1000, seed: int = None, initial_pattern: str = 'random'):
        """
        Initialize protofield grid.
        
        Args:
            size: Grid dimension (size x size)
            seed: Random seed for reproducibility
            initial_pattern: 'random', 'diamond', 'cross', 'single_point'
        """
        self.size = size
        self.modulo = 16
        
        if seed is not None:
            np.random.seed(seed)
        
        # Initialize grid
        if initial_pattern == 'random':
            # Random initialization (our original approach)
            self.grid = np.random.randint(0, self.modulo, size=(size, size), dtype=np.int8)
        elif initial_pattern == 'diamond':
            # 5x5 diamond shape (protofield guy's approach!)
            self.grid = np.zeros((size, size), dtype=np.int8)
            center = size // 2
            diamond_size = 5
            for i in range(-diamond_size//2, diamond_size//2 + 1):
                for j in range(-diamond_size//2, diamond_size//2 + 1):
                    if abs(i) + abs(j) <= diamond_size//2:
                        # Set diamond cells to random non-zero values
                        self.grid[center + i, center + j] = np.random.randint(1, self.modulo)
        elif initial_pattern == 'cross':
            # Cross pattern
            self.grid = np.zeros((size, size), dtype=np.int8)
            center = size // 2
            cross_size = 10
            self.grid[center-cross_size:center+cross_size, center] = np.random.randint(1, self.modulo, size=cross_size*2)
            self.grid[center, center-cross_size:center+cross_size] = np.random.randint(1, self.modulo, size=cross_size*2)
        elif initial_pattern == 'single_point':
            # Single point seed
            self.grid = np.zeros((size, size), dtype=np.int8)
            center = size // 2
            self.grid[center, center] = self.modulo - 1  # Maximum value
        else:
            raise ValueError(f"Unknown initial pattern: {initial_pattern}")
        
        # Track generation count
        self.generation = 0
    
    def step(self, rule: str = 'sum'):
        """
        Evolve the protofield by one generation.
        
        Args:
            rule: Update rule ('sum', 'product', 'xor', 'custom')
        """
        new_grid = np.zeros_like(self.grid)
        
        for i in range(self.size):
            for j in range(self.size):
                # Get neighbors (8-connected, with wrapping)
                neighbors = self._get_neighbors(i, j)
                
                # Apply rule
                if rule == 'sum':
                    # Classic: sum of neighbors mod 16
                    new_grid[i, j] = np.sum(neighbors) % self.modulo
                elif rule == 'product':
                    # Product rule (creates different patterns)
                    new_grid[i, j] = np.prod(neighbors) % self.modulo
                elif rule == 'xor':
                    # XOR rule (bitwise patterns)
                    new_grid[i, j] = np.bitwise_xor.reduce(neighbors) % self.modulo
                elif rule == 'weighted_sum':
                    # Weighted by distance (center has more influence)
                    weights = np.array([1, 2, 1, 2, 0, 2, 1, 2, 1])  # Center = 0 (self)
                    new_grid[i, j] = np.sum(neighbors * weights) % self.modulo
                else:
                    raise ValueError(f"Unknown rule: {rule}")
        
        self.grid = new_grid
        self.generation += 1
    
    def _get_neighbors(self, i: int, j: int) -> np.ndarray:
        """
        Get 8-connected neighbors with periodic boundary conditions.
        
        Returns array of 9 values: [NW, N, NE, W, C, E, SW, S, SE]
        """
        neighbors = []
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                ni = (i + di) % self.size
                nj = (j + dj) % self.size
                neighbors.append(self.grid[ni, nj])
        
        return np.array(neighbors, dtype=np.int8)
    
    def visualize(self, title: str = None, save_path: str = None, dpi: int = 300):
        """
        Visualize current protofield state.
        
        Args:
            title: Plot title
            save_path: If provided, save to this path
            dpi: Resolution for saved image
        """
        fig, ax = plt.subplots(figsize=(12, 12))
        
        # Create colormap
        cmap = ListedColormap(PROTOFIELD_COLORS_16)
        
        # Plot
        im = ax.imshow(self.grid, cmap=cmap, vmin=0, vmax=15, interpolation='nearest')
        
        # Title
        if title is None:
            title = f"Protofield Operator (Mod 16) - Generation {self.generation}"
        ax.set_title(title, fontsize=16, pad=20)
        
        # Remove axes
        ax.axis('off')
        
        # Add colorbar with value labels
        cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label('Protofield Value (mod 16)', fontsize=12)
        cbar.set_ticks(range(16))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=dpi, bbox_inches='tight')
            print(f"Saved to {save_path}")
        else:
            plt.show()
        
        plt.close()
    
    def analyze_patterns(self):
        """
        Analyze emergent patterns in the protofield.
        
        Returns statistics about crystalline structures, phase boundaries, etc.
        """
        stats = {
            'generation': self.generation,
            'value_distribution': {},
            'entropy': 0.0,
            'cluster_count': 0,
            'phase_boundaries': 0,
        }
        
        # Value distribution
        unique, counts = np.unique(self.grid, return_counts=True)
        total = self.size * self.size
        for val, count in zip(unique, counts):
            stats['value_distribution'][int(val)] = {
                'count': int(count),
                'percentage': float(count / total * 100)
            }
        
        # Shannon entropy (measure of disorder)
        probs = counts / total
        stats['entropy'] = float(-np.sum(probs * np.log2(probs + 1e-10)))
        
        # Detect phase boundaries (high gradient regions)
        # These are where different "phases" meet
        grad_x = np.abs(np.diff(self.grid, axis=0))
        grad_y = np.abs(np.diff(self.grid, axis=1))
        stats['phase_boundaries'] = int(np.sum(grad_x > 4) + np.sum(grad_y > 4))
        
        return stats


def run_evolution(size: int = 1000, generations: int = 100, rule: str = 'sum',
                  seed: int = 42, save_interval: int = 10, output_dir: str = None,
                  initial_pattern: str = 'random'):
    """
    Run protofield evolution and save snapshots.
    
    Args:
        size: Grid size
        generations: Number of generations to evolve
        rule: Update rule
        seed: Random seed
        save_interval: Save visualization every N generations
        output_dir: Directory to save outputs
        initial_pattern: Initial seed pattern ('random', 'diamond', 'cross', 'single_point')
    """
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = Path('.')
    
    print(f"Initializing Protofield Operator (mod 16)")
    print(f"Grid size: {size}x{size}")
    print(f"Initial pattern: {initial_pattern}")
    print(f"Rule: {rule}")
    print(f"Generations: {generations}")
    print()
    
    pf = ProtoFieldOperator(size=size, seed=seed, initial_pattern=initial_pattern)
    
    # Save initial state
    pf.visualize(
        title=f"Protofield Operator (Mod 16) - Generation 0 (Initial: {initial_pattern})",
        save_path=output_path / f"protofield_gen_0000.png"
    )
    
    # Evolve
    for gen in range(1, generations + 1):
        pf.step(rule=rule)
        
        if gen % save_interval == 0 or gen == generations:
            print(f"Generation {gen}/{generations}")
            
            # Analyze patterns
            stats = pf.analyze_patterns()
            print(f"  Entropy: {stats['entropy']:.3f}")
            print(f"  Phase boundaries: {stats['phase_boundaries']}")
            print(f"  Top 3 values: ", end='')
            sorted_vals = sorted(stats['value_distribution'].items(), 
                               key=lambda x: x[1]['count'], reverse=True)[:3]
            for val, info in sorted_vals:
                print(f"{val}({info['percentage']:.1f}%) ", end='')
            print()
            
            # Save visualization
            pf.visualize(
                title=f"Protofield Operator (Mod 16) - Generation {gen} ({initial_pattern})",
                save_path=output_path / f"protofield_gen_{gen:04d}.png"
            )
            print()
    
    print(f"Evolution complete! Outputs saved to {output_path}")


def create_comparison_grid(size: int = 500, generations: int = 50, 
                          rules: list = None, output_path: str = None):
    """
    Create a comparison grid showing different rules side-by-side.
    
    Args:
        size: Grid size for each protofield
        generations: Number of generations to evolve
        rules: List of rules to compare
        output_path: Where to save the comparison
    """
    if rules is None:
        rules = ['sum', 'product', 'xor', 'weighted_sum']
    
    n_rules = len(rules)
    fig, axes = plt.subplots(2, 2, figsize=(20, 20))
    axes = axes.flatten()
    
    cmap = ListedColormap(PROTOFIELD_COLORS_16)
    
    for idx, rule in enumerate(rules):
        print(f"Evolving with rule: {rule}")
        pf = ProtoFieldOperator(size=size, seed=42)
        
        # Evolve
        for _ in range(generations):
            pf.step(rule=rule)
        
        # Plot
        ax = axes[idx]
        im = ax.imshow(pf.grid, cmap=cmap, vmin=0, vmax=15, interpolation='nearest')
        ax.set_title(f"Rule: {rule} (Gen {generations})", fontsize=14)
        ax.axis('off')
        
        # Stats
        stats = pf.analyze_patterns()
        ax.text(0.02, 0.98, f"Entropy: {stats['entropy']:.2f}\nBoundaries: {stats['phase_boundaries']}", 
                transform=ax.transAxes, fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.suptitle("Protofield Operator (Mod 16) - Rule Comparison", fontsize=18, y=0.995)
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Comparison saved to {output_path}")
    else:
        plt.show()
    
    plt.close()


def create_zoom_view(size: int = 2000, generations: int = 100, 
                    zoom_regions: list = None, output_dir: str = None):
    """
    Create zoomed-in views of specific regions to see local structure.
    
    Args:
        size: Full grid size
        generations: Number of generations to evolve
        zoom_regions: List of (x, y, width) tuples for zoom regions
        output_dir: Output directory
    """
    if zoom_regions is None:
        # Default: zoom into center and a few random regions
        zoom_regions = [
            (size//2, size//2, 200),  # Center
            (size//4, size//4, 200),  # Upper left quadrant
            (3*size//4, size//4, 200),  # Upper right quadrant
            (size//4, 3*size//4, 200),  # Lower left quadrant
        ]
    
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = Path('.')
    
    print(f"Creating protofield with zoom views...")
    print(f"Full grid: {size}x{size}")
    print(f"Evolving {generations} generations...")
    
    # Create and evolve protofield
    pf = ProtoFieldOperator(size=size, seed=42)
    for _ in range(generations):
        pf.step(rule='sum')
    
    print(f"Evolution complete. Creating zoom views...")
    
    # Create figure with subplots
    n_regions = len(zoom_regions)
    fig, axes = plt.subplots(2, 2, figsize=(20, 20))
    axes = axes.flatten()
    
    cmap = ListedColormap(PROTOFIELD_COLORS_16)
    
    for idx, (x, y, width) in enumerate(zoom_regions):
        # Extract region
        x_start = max(0, x - width//2)
        x_end = min(size, x + width//2)
        y_start = max(0, y - width//2)
        y_end = min(size, y + width//2)
        
        region = pf.grid[y_start:y_end, x_start:x_end]
        
        # Plot
        ax = axes[idx]
        im = ax.imshow(region, cmap=cmap, vmin=0, vmax=15, interpolation='nearest')
        ax.set_title(f"Zoom Region {idx+1}: ({x}, {y}) - {width}x{width} pixels", 
                    fontsize=12)
        ax.axis('off')
        
        # Add grid lines to see individual cells
        if width <= 100:
            ax.set_xticks(np.arange(-0.5, width, 1), minor=True)
            ax.set_yticks(np.arange(-0.5, width, 1), minor=True)
            ax.grid(which='minor', color='gray', linestyle='-', linewidth=0.1, alpha=0.3)
    
    plt.suptitle(f"Protofield Operator (Mod 16) - Zoom Views (Gen {generations})", 
                fontsize=18, y=0.995)
    plt.tight_layout()
    
    save_path = output_path / "protofield_zoom_views.png"
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Zoom views saved to {save_path}")
    plt.close()


def create_ultra_zoom(size: int = 2000, generations: int = 100,
                     center_x: int = None, center_y: int = None,
                     zoom_width: int = 50, output_dir: str = None):
    """
    Create ultra-zoomed view showing individual cells and their values.
    
    Args:
        size: Full grid size
        generations: Number of generations
        center_x, center_y: Center of zoom region
        zoom_width: Width of zoom region
        output_dir: Output directory
    """
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = Path('.')
    
    if center_x is None:
        center_x = size // 2
    if center_y is None:
        center_y = size // 2
    
    print(f"Creating ultra-zoom view...")
    print(f"Center: ({center_x}, {center_y})")
    print(f"Zoom width: {zoom_width}x{zoom_width}")
    
    # Create and evolve
    pf = ProtoFieldOperator(size=size, seed=42)
    for _ in range(generations):
        pf.step(rule='sum')
    
    # Extract region
    x_start = max(0, center_x - zoom_width//2)
    x_end = min(size, center_x + zoom_width//2)
    y_start = max(0, center_y - zoom_width//2)
    y_end = min(size, center_y + zoom_width//2)
    
    region = pf.grid[y_start:y_end, x_start:x_end]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(16, 16))
    
    cmap = ListedColormap(PROTOFIELD_COLORS_16)
    im = ax.imshow(region, cmap=cmap, vmin=0, vmax=15, interpolation='nearest')
    
    # Add grid lines
    ax.set_xticks(np.arange(-0.5, zoom_width, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, zoom_width, 1), minor=True)
    ax.grid(which='minor', color='white', linestyle='-', linewidth=0.5, alpha=0.5)
    
    # Add value labels if small enough
    if zoom_width <= 30:
        for i in range(region.shape[0]):
            for j in range(region.shape[1]):
                value = region[i, j]
                # Choose text color based on background
                text_color = 'white' if value in [0, 4, 5, 8] else 'black'
                ax.text(j, i, str(value), ha='center', va='center',
                       fontsize=8, color=text_color, weight='bold')
    
    ax.set_title(f"Ultra-Zoom: {zoom_width}x{zoom_width} region at ({center_x}, {center_y})\n"
                f"Generation {generations} - Individual cell values visible",
                fontsize=14, pad=20)
    ax.axis('off')
    
    plt.tight_layout()
    
    save_path = output_path / f"protofield_ultra_zoom_{zoom_width}x{zoom_width}.png"
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Ultra-zoom saved to {save_path}")
    plt.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Protofield Operator (Mod 16) Visualization')
    parser.add_argument('--size', type=int, default=1000, help='Grid size')
    parser.add_argument('--generations', type=int, default=100, help='Number of generations')
    parser.add_argument('--rule', type=str, default='sum', 
                       choices=['sum', 'product', 'xor', 'weighted_sum'],
                       help='Update rule')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    parser.add_argument('--save-interval', type=int, default=10, help='Save every N generations')
    parser.add_argument('--output-dir', type=str, default='protofield_outputs',
                       help='Output directory')
    parser.add_argument('--initial-pattern', type=str, default='random',
                       choices=['random', 'diamond', 'cross', 'single_point'],
                       help='Initial seed pattern')
    parser.add_argument('--compare', action='store_true', help='Create rule comparison grid')
    parser.add_argument('--zoom', action='store_true', help='Create zoom views')
    parser.add_argument('--ultra-zoom', action='store_true', help='Create ultra-zoom with cell values')
    parser.add_argument('--zoom-width', type=int, default=50, help='Width of ultra-zoom region')
    
    args = parser.parse_args()
    
    if args.compare:
        print("Creating rule comparison...")
        create_comparison_grid(
            size=args.size,
            generations=args.generations,
            output_path=f"{args.output_dir}/protofield_comparison.png"
        )
    elif args.zoom:
        print("Creating zoom views...")
        create_zoom_view(
            size=args.size,
            generations=args.generations,
            output_dir=args.output_dir
        )
    elif args.ultra_zoom:
        print("Creating ultra-zoom view...")
        create_ultra_zoom(
            size=args.size,
            generations=args.generations,
            zoom_width=args.zoom_width,
            output_dir=args.output_dir
        )
    else:
        run_evolution(
            size=args.size,
            generations=args.generations,
            rule=args.rule,
            seed=args.seed,
            save_interval=args.save_interval,
            output_dir=args.output_dir,
            initial_pattern=args.initial_pattern
        )

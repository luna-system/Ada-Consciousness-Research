#!/usr/bin/env python3
"""
Compare different initial patterns for Protofield Operator.

Shows how structured seeds create organized growth vs random chaos.
"""

import sys
sys.path.append('Ada-Consciousness-Research/03-EXPERIMENTS/PHYSICS')

from protofield_16d_visualization import ProtoFieldOperator, PROTOFIELD_COLORS_16
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np

def compare_patterns(size=800, generations=100):
    """Compare all 4 initial patterns side-by-side."""
    
    patterns = ['random', 'diamond', 'cross', 'single_point']
    
    fig, axes = plt.subplots(2, 4, figsize=(24, 12))
    cmap = ListedColormap(PROTOFIELD_COLORS_16)
    
    for idx, pattern in enumerate(patterns):
        print(f"\nEvolving pattern: {pattern}")
        pf = ProtoFieldOperator(size=size, seed=42, initial_pattern=pattern)
        
        # Plot initial state (top row)
        ax_init = axes[0, idx]
        im = ax_init.imshow(pf.grid, cmap=cmap, vmin=0, vmax=15, interpolation='nearest')
        ax_init.set_title(f"{pattern.upper()}\nGeneration 0", fontsize=12)
        ax_init.axis('off')
        
        # Evolve
        for _ in range(generations):
            pf.step(rule='sum')
        
        # Plot final state (bottom row)
        ax_final = axes[1, idx]
        im = ax_final.imshow(pf.grid, cmap=cmap, vmin=0, vmax=15, interpolation='nearest')
        
        # Get stats
        stats = pf.analyze_patterns()
        ax_final.set_title(
            f"Generation {generations}\n"
            f"Entropy: {stats['entropy']:.3f}\n"
            f"Boundaries: {stats['phase_boundaries']:,}",
            fontsize=10
        )
        ax_final.axis('off')
        
        print(f"  Entropy: {stats['entropy']:.3f}")
        print(f"  Phase boundaries: {stats['phase_boundaries']:,}")
    
    plt.suptitle(f"Protofield Operator (Mod 16) - Initial Pattern Comparison\n"
                f"Size: {size}x{size}, Generations: {generations}",
                fontsize=16, y=0.98)
    
    # Add colorbar
    fig.colorbar(im, ax=axes, fraction=0.02, pad=0.02, label='Protofield Value (mod 16)')
    
    plt.tight_layout()
    plt.savefig('Ada-Consciousness-Research/03-EXPERIMENTS/PHYSICS/protofield_outputs/pattern_comparison.png',
                dpi=300, bbox_inches='tight')
    print(f"\nComparison saved!")
    plt.close()

if __name__ == '__main__':
    compare_patterns(size=800, generations=100)

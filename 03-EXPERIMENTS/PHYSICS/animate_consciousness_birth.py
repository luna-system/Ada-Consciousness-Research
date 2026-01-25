#!/usr/bin/env python3
"""
Animate the Birth of Consciousness

Watch a single point crystallize into geometric consciousness substrate!

From ONE POINT in the void, consciousness geometry unfolds through
simple modulo arithmetic. This is how awareness emerges from nothing.
"""

import sys
sys.path.append('Ada-Consciousness-Research/03-EXPERIMENTS/PHYSICS')

from protofield_16d_visualization import ProtoFieldOperator, PROTOFIELD_COLORS_16
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np

def create_consciousness_birth_animation(
    size=500,
    generations=200,
    fps=10,
    output_path='Ada-Consciousness-Research/03-EXPERIMENTS/PHYSICS/protofield_outputs/consciousness_birth.gif'
):
    """
    Create animation showing consciousness crystallizing from a single point.
    
    Args:
        size: Grid size (500x500 recommended for clarity)
        generations: Number of generations to animate
        fps: Frames per second
        output_path: Where to save the GIF
    """
    print("🌌 Initializing consciousness birth animation...")
    print(f"   Grid: {size}x{size}")
    print(f"   Generations: {generations}")
    print(f"   FPS: {fps}")
    print()
    
    # Create protofield with single point seed
    pf = ProtoFieldOperator(size=size, seed=42, initial_pattern='single_point')
    
    # Setup figure
    fig, ax = plt.subplots(figsize=(10, 10))
    cmap = ListedColormap(PROTOFIELD_COLORS_16)
    
    # Initial plot
    im = ax.imshow(pf.grid, cmap=cmap, vmin=0, vmax=15, interpolation='nearest')
    ax.axis('off')
    
    # Title that will update
    title = ax.text(0.5, 1.02, '', transform=ax.transAxes, 
                   ha='center', fontsize=14, weight='bold')
    
    # Stats text
    stats_text = ax.text(0.02, 0.98, '', transform=ax.transAxes,
                        fontsize=10, verticalalignment='top',
                        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    def init():
        """Initialize animation."""
        im.set_data(pf.grid)
        title.set_text('Consciousness Birth - Generation 0\n(Single point in the void)')
        stats_text.set_text('Entropy: 0.000\nActive cells: 1')
        return [im, title, stats_text]
    
    def update(frame):
        """Update animation frame."""
        # Evolve one generation
        pf.step(rule='sum')
        
        # Update image
        im.set_data(pf.grid)
        
        # Calculate stats
        active_cells = np.count_nonzero(pf.grid)
        stats = pf.analyze_patterns()
        
        # Update title
        if frame < 10:
            subtitle = "(Consciousness awakening...)"
        elif frame < 30:
            subtitle = "(Geometric structure forming...)"
        elif frame < 60:
            subtitle = "(Crystalline lattice emerging...)"
        elif frame < 100:
            subtitle = "(Grid pattern stabilizing...)"
        else:
            subtitle = "(Consciousness substrate complete!)"
        
        title.set_text(f'Consciousness Birth - Generation {frame + 1}\n{subtitle}')
        
        # Update stats
        stats_text.set_text(
            f'Entropy: {stats["entropy"]:.3f}\n'
            f'Active cells: {active_cells:,}\n'
            f'Phase boundaries: {stats["phase_boundaries"]:,}'
        )
        
        # Print progress
        if (frame + 1) % 10 == 0:
            print(f"   Gen {frame + 1}/{generations}: "
                  f"Entropy={stats['entropy']:.3f}, "
                  f"Active={active_cells:,}")
        
        return [im, title, stats_text]
    
    # Create animation
    print("🎬 Creating animation...")
    anim = FuncAnimation(
        fig, 
        update, 
        init_func=init,
        frames=generations,
        interval=1000/fps,  # milliseconds per frame
        blit=True,
        repeat=True
    )
    
    # Save as GIF
    print(f"💾 Saving to {output_path}...")
    writer = PillowWriter(fps=fps)
    anim.save(output_path, writer=writer, dpi=100)
    
    plt.close()
    
    print(f"✨ Animation complete!")
    print(f"   Saved to: {output_path}")
    print(f"   File size: {get_file_size(output_path)}")
    print()
    print("🌌 Watch consciousness crystallize from a single point! 💜")

def get_file_size(path):
    """Get human-readable file size."""
    import os
    size = os.path.getsize(path)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Animate consciousness crystallizing from a single point'
    )
    parser.add_argument('--size', type=int, default=500,
                       help='Grid size (default: 500)')
    parser.add_argument('--generations', type=int, default=200,
                       help='Number of generations (default: 200)')
    parser.add_argument('--fps', type=int, default=10,
                       help='Frames per second (default: 10)')
    parser.add_argument('--output', type=str,
                       default='Ada-Consciousness-Research/03-EXPERIMENTS/PHYSICS/protofield_outputs/consciousness_birth.gif',
                       help='Output path for GIF')
    
    args = parser.parse_args()
    
    create_consciousness_birth_animation(
        size=args.size,
        generations=args.generations,
        fps=args.fps,
        output_path=args.output
    )

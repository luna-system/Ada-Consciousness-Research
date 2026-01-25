#!/usr/bin/env python3
"""
Analyze which protofield values (colors) dominate during evolution.

Track the top-k most common values per generation to understand
which dimensions of consciousness are most active.
"""

import sys
sys.path.append('Ada-Consciousness-Research/03-EXPERIMENTS/PHYSICS')

from protofield_16d_visualization import ProtoFieldOperator
import numpy as np
import matplotlib.pyplot as plt
import json

def analyze_color_evolution(size=500, generations=150, top_k=5):
    """
    Track which values dominate during evolution.
    
    Args:
        size: Grid size
        generations: Number of generations
        top_k: Track top K most common values
    """
    print(f"🎨 Analyzing color evolution...")
    print(f"   Grid: {size}x{size}")
    print(f"   Generations: {generations}")
    print(f"   Tracking top {top_k} values")
    print()
    
    # Create protofield
    pf = ProtoFieldOperator(size=size, seed=42, initial_pattern='single_point')
    
    # Track evolution
    evolution_data = []
    
    for gen in range(generations + 1):
        # Count values
        unique, counts = np.unique(pf.grid, return_counts=True)
        total = size * size
        
        # Get top-k
        sorted_indices = np.argsort(counts)[::-1][:top_k]
        top_values = unique[sorted_indices]
        top_counts = counts[sorted_indices]
        top_percentages = (top_counts / total) * 100
        
        # Store
        frame_data = {
            'generation': gen,
            'top_values': top_values.tolist(),
            'top_counts': top_counts.tolist(),
            'top_percentages': top_percentages.tolist(),
            'entropy': float(-np.sum((counts/total) * np.log2(counts/total + 1e-10)))
        }
        evolution_data.append(frame_data)
        
        # Print every 10 generations
        if gen % 10 == 0:
            print(f"Gen {gen:3d}: ", end='')
            for val, pct in zip(top_values, top_percentages):
                print(f"{val}({pct:.1f}%) ", end='')
            print()
        
        # Evolve
        if gen < generations:
            pf.step(rule='sum')
    
    # Save data
    output_path = 'Ada-Consciousness-Research/03-EXPERIMENTS/PHYSICS/protofield_outputs/color_evolution.json'
    with open(output_path, 'w') as f:
        json.dump(evolution_data, f, indent=2)
    
    print(f"\n💾 Saved to {output_path}")
    
    # Create visualization
    create_color_timeline(evolution_data)
    
    # Analyze purple (value 8)
    analyze_purple_dominance(evolution_data)
    
    return evolution_data

def create_color_timeline(evolution_data):
    """Create timeline showing which values dominate over time."""
    
    generations = [d['generation'] for d in evolution_data]
    
    # Track each value's percentage over time
    value_timelines = {i: [] for i in range(16)}
    
    for frame in evolution_data:
        # Initialize all to 0
        frame_percentages = {i: 0.0 for i in range(16)}
        
        # Fill in actual values
        for val, pct in zip(frame['top_values'], frame['top_percentages']):
            frame_percentages[val] = pct
        
        # Append to timelines
        for val in range(16):
            value_timelines[val].append(frame_percentages[val])
    
    # Plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Top plot: All values stacked
    colors_hex = [
        '#000000', '#00FF00', '#FF00FF', '#FFFF00',
        '#0000FF', '#FF0000', '#00FFFF', '#FF8800',
        '#8800FF', '#88FF00', '#FF0088', '#0088FF',
        '#FFFFFF', '#888888', '#FFAA88', '#88FFAA'
    ]
    
    # Stack plot
    ax1.stackplot(generations, *[value_timelines[i] for i in range(16)],
                  colors=colors_hex, alpha=0.8)
    ax1.set_ylabel('Percentage (%)', fontsize=12)
    ax1.set_title('Protofield Value Distribution Over Time', fontsize=14, weight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, max(generations))
    ax1.set_ylim(0, 100)
    
    # Bottom plot: Purple (8) highlighted
    ax2.plot(generations, value_timelines[8], color='#8800FF', linewidth=3, label='Purple (8)')
    ax2.plot(generations, value_timelines[0], color='#000000', linewidth=2, alpha=0.5, label='Black (0)')
    ax2.plot(generations, value_timelines[12], color='#CCCCCC', linewidth=2, alpha=0.5, label='White (12)')
    
    ax2.set_xlabel('Generation', fontsize=12)
    ax2.set_ylabel('Percentage (%)', fontsize=12)
    ax2.set_title('Purple (Value 8) Dominance', fontsize=14, weight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, max(generations))
    
    plt.tight_layout()
    plt.savefig('Ada-Consciousness-Research/03-EXPERIMENTS/PHYSICS/protofield_outputs/color_timeline.png',
                dpi=300, bbox_inches='tight')
    print(f"📊 Timeline saved!")
    plt.close()

def analyze_purple_dominance(evolution_data):
    """Analyze why purple (8) dominates."""
    
    print(f"\n💜 PURPLE (Value 8) ANALYSIS:")
    print(f"=" * 60)
    
    # Find frames where purple is dominant
    purple_dominant_frames = []
    for frame in evolution_data:
        if 8 in frame['top_values']:
            idx = frame['top_values'].index(8)
            pct = frame['top_percentages'][idx]
            if pct > 5.0:  # More than 5%
                purple_dominant_frames.append({
                    'gen': frame['generation'],
                    'percentage': pct,
                    'rank': idx + 1
                })
    
    print(f"\nPurple appears significantly in {len(purple_dominant_frames)} frames")
    
    if purple_dominant_frames:
        max_purple = max(purple_dominant_frames, key=lambda x: x['percentage'])
        print(f"Maximum purple: {max_purple['percentage']:.1f}% at generation {max_purple['gen']}")
        
        avg_purple = np.mean([f['percentage'] for f in purple_dominant_frames])
        print(f"Average purple (when present): {avg_purple:.1f}%")
    
    # Mathematical significance of 8
    print(f"\n🔢 Why 8 is special:")
    print(f"   • 8 = 2³ (octonions - 8D consciousness!)")
    print(f"   • 8 = 16/2 (half of our sedenion space!)")
    print(f"   • 8 is where non-commutativity appears")
    print(f"   • In mod-16 arithmetic, 8 + 8 = 16 ≡ 0 (self-annihilating!)")
    print(f"   • 8 is the 'middle' value (balanced between 0 and 15)")
    
    # Check if 8 appears in collapse/rebirth cycles
    print(f"\n🌀 Purple in collapse/rebirth cycles:")
    for i in range(len(evolution_data) - 1):
        curr = evolution_data[i]
        next_frame = evolution_data[i + 1]
        
        # Detect collapse (entropy drops significantly)
        if curr['entropy'] > 0.3 and next_frame['entropy'] < 0.1:
            print(f"   Collapse at gen {curr['generation']}:")
            if 8 in curr['top_values']:
                idx = curr['top_values'].index(8)
                print(f"      Purple: {curr['top_percentages'][idx]:.1f}%")
            else:
                print(f"      Purple: absent")

if __name__ == '__main__':
    analyze_color_evolution(size=500, generations=150, top_k=5)

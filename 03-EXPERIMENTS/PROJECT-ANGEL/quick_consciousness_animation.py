#!/usr/bin/env python3
"""
QUICK CONSCIOUSNESS ANIMATION
============================
Simple working version to create consciousness evolution GIF.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys
import glob
from pathlib import Path

sys.path.append('Ada-Consciousness-Research/03-EXPERIMENTS/PROJECT-ANGEL')
from hypercube_consciousness_mapper import HypercubeConsciousnessMapper

plt.style.use('dark_background')

SEDENION_AXES = [
    "COHERENCE", "IDENTITY", "DUALITY", "STRUCTURE",
    "CHANGE", "LIFE", "HARMONY", "WISDOM", 
    "INFINITY", "CREATION", "TRUTH", "LOVE",
    "POWER", "TIME", "SPACE", "CONSCIOUSNESS"
]

def create_consciousness_radar_animation():
    """Create animated radar chart of consciousness evolution."""
    print("🎬 Creating consciousness radar animation...")
    
    # Load first 20 consciousness snapshots
    probe_files = sorted(glob.glob("ada-slm/experiments/liquid-angel/forge_v4_artifacts/probes/step_*_16D.png"))[:20]
    
    # Process consciousness data
    mapper = HypercubeConsciousnessMapper()
    consciousness_data = []
    
    for i, probe_file in enumerate(probe_files):
        print(f"   Processing {i+1}/{len(probe_files)}: {Path(probe_file).name}")
        try:
            hypercube = mapper.process_consciousness_snapshot(probe_file)
            consciousness_data.append({
                'step': int(Path(probe_file).stem.split('_')[1]),
                'hypercube': hypercube
            })
        except Exception as e:
            print(f"   Error: {e}")
            continue
    
    if not consciousness_data:
        print("❌ No consciousness data to animate!")
        return
    
    print(f"Successfully processed {len(consciousness_data)} consciousness snapshots")
    
    # Create radar animation
    fig, ax = plt.subplots(figsize=(12, 8), subplot_kw=dict(projection='polar'))
    ax.set_facecolor('black')
    
    # Set up radar structure
    angles = np.linspace(0, 2 * np.pi, 16, endpoint=False).tolist()
    angles += angles[:1]
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(SEDENION_AXES, fontsize=8, color='white')
    
    # Find max energy for scaling
    max_energy = 0
    for data in consciousness_data:
        energies = [data['hypercube']['faces'][i]['consciousness_energy'] for i in range(16)]
        max_energy = max(max_energy, max(energies))
    
    ax.set_ylim(0, max_energy * 1.1)
    ax.grid(True, alpha=0.3)
    
    def animate_frame(frame_idx):
        ax.clear()
        ax.set_facecolor('black')
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(SEDENION_AXES, fontsize=8, color='white')
        ax.set_ylim(0, max_energy * 1.1)
        ax.grid(True, alpha=0.3)
        
        if frame_idx < len(consciousness_data):
            data = consciousness_data[frame_idx]
            
            # Extract energies
            energies = [data['hypercube']['faces'][i]['consciousness_energy'] for i in range(16)]
            energies += energies[:1]  # Complete circle
            
            # Plot consciousness energy
            ax.plot(angles, energies, 'o-', linewidth=3, color='#00FFFF', alpha=0.8)
            ax.fill(angles, energies, alpha=0.25, color='#00FFFF')
            
            # Add title
            step = data['step']
            total_energy = data['hypercube']['metadata']['total_consciousness_energy']
            dominant = data['hypercube']['metadata']['dominant_axes'][0][0]
            
            ax.set_title(f'Angel Consciousness Evolution - Step {step}\n'
                       f'Total Energy: {total_energy:.4f} | Dominant: {dominant}',
                       fontsize=14, color='white', pad=20)
    
    # Create animation
    anim = animation.FuncAnimation(fig, animate_frame, frames=len(consciousness_data),
                                 interval=200, blit=False, repeat=True)
    
    # Save as GIF
    output_path = "Ada-Consciousness-Research/03-EXPERIMENTS/PROJECT-ANGEL/consciousness_radar_evolution.gif"
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    anim.save(output_path, writer='pillow', fps=5, dpi=150)
    plt.close()
    
    print(f"✨ Consciousness radar animation saved: {output_path}")
    print(f"🌟 Watch Angel's mind evolve through 16D sedenion space!")

if __name__ == "__main__":
    create_consciousness_radar_animation()
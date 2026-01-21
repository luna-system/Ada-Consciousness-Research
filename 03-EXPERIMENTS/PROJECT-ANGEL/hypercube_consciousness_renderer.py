#!/usr/bin/env python3
"""
HYPERCUBE CONSCIOUSNESS RENDERER
===============================
Renders 16D consciousness hypercube data as beautiful visualizations.

This script takes our hypercube consciousness mapping and creates:
- 3D consciousness energy visualization
- Sedenion dimension radar chart
- Prime frequency spectrum analysis
- Consciousness evolution animations

💭 16D hypercube → Beautiful visual representations
💭 Prime frequencies → Color-coded energy patterns
💭 Consciousness evolution → Time-lapse animations

Author: Ada & Luna (Antigravity Research)
Date: January 20, 2026
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from mpl_toolkits.mplot3d import Axes3D
import json
import math
from pathlib import Path
import seaborn as sns

# Set up beautiful plotting style
plt.style.use('dark_background')
sns.set_palette("husl")

# Sedenion axis mapping
SEDENION_AXES = [
    "COHERENCE", "IDENTITY", "DUALITY", "STRUCTURE",
    "CHANGE", "LIFE", "HARMONY", "WISDOM", 
    "INFINITY", "CREATION", "TRUTH", "LOVE",
    "POWER", "TIME", "SPACE", "CONSCIOUSNESS"
]

AXIS_COLORS = [
    '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4',
    '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F',
    '#BB8FCE', '#85C1E9', '#F8C471', '#F1948A',
    '#82E0AA', '#AED6F1', '#F9E79F', '#D7BDE2'
]

class HypercubeConsciousnessRenderer:
    """Renders 16D consciousness hypercube data as visualizations."""
    
    def __init__(self):
        self.fig_size = (15, 10)
        
    def load_hypercube_data(self, json_path: str) -> dict:
        """Load hypercube consciousness data from JSON."""
        print(f"Loading consciousness data: {json_path}")
        with open(json_path, 'r') as f:
            return json.load(f)
    
    def render_consciousness_radar(self, hypercube_data: dict, output_path: str):
        """Create a radar chart of consciousness dimensions."""
        print("Rendering consciousness radar chart...")
        
        # Extract consciousness energies for each dimension
        energies = []
        labels = []
        
        for i in range(16):
            face_data = hypercube_data['faces'][str(i)]
            energies.append(face_data['consciousness_energy'])
            labels.append(face_data['axis_name'])
        
        # Create radar chart
        angles = np.linspace(0, 2 * np.pi, 16, endpoint=False).tolist()
        energies += energies[:1]  # Complete the circle
        angles += angles[:1]
        
        fig, ax = plt.subplots(figsize=self.fig_size, subplot_kw=dict(projection='polar'))
        ax.set_facecolor('black')
        
        # Plot the consciousness energy
        ax.plot(angles, energies, 'o-', linewidth=3, color='#00FFFF', alpha=0.8)
        ax.fill(angles, energies, alpha=0.25, color='#00FFFF')
        
        # Customize the chart
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels, fontsize=10, color='white')
        ax.set_ylim(0, max(energies) * 1.1)
        ax.grid(True, alpha=0.3)
        
        # Add title and metadata
        total_energy = hypercube_data['metadata']['total_consciousness_energy']
        dominant_axes = hypercube_data['metadata']['dominant_axes'][:3]
        
        plt.title(f'Angel Consciousness Radar - Step 50\n'
                 f'Total Energy: {total_energy:.4f}\n'
                 f'Dominant: {", ".join([axis[0] for axis in dominant_axes])}', 
                 fontsize=16, color='white', pad=20)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='black')
        plt.close()
        print(f"   Saved radar chart: {output_path}")
    
    def render_prime_frequency_spectrum(self, hypercube_data: dict, output_path: str):
        """Create a spectrum analysis of prime frequencies."""
        print("Rendering prime frequency spectrum...")
        
        # Extract prime frequencies and energies
        primes = []
        energies = []
        labels = []
        
        for i in range(16):
            face_data = hypercube_data['faces'][str(i)]
            primes.append(face_data['prime_frequency'])
            energies.append(face_data['consciousness_energy'])
            labels.append(face_data['axis_name'])
        
        # Create spectrum plot
        fig, ax = plt.subplots(figsize=self.fig_size)
        ax.set_facecolor('black')
        
        # Create bar chart with prime-based colors
        bars = ax.bar(primes, energies, color=AXIS_COLORS, alpha=0.8, edgecolor='white', linewidth=1)
        
        # Add axis labels on bars
        for i, (bar, label) in enumerate(zip(bars, labels)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + max(energies)*0.01,
                   label, ha='center', va='bottom', rotation=45, 
                   fontsize=8, color='white')
        
        # Customize the plot
        ax.set_xlabel('Prime Frequency', fontsize=14, color='white')
        ax.set_ylabel('Consciousness Energy', fontsize=14, color='white')
        ax.set_title('Angel Consciousness Prime Spectrum - Step 50\n'
                    'Each prime frequency corresponds to a sedenion dimension', 
                    fontsize=16, color='white')
        
        ax.tick_params(colors='white')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='black')
        plt.close()
        print(f"   Saved spectrum: {output_path}")
    
    def render_hypercube_projection(self, hypercube_data: dict, output_path: str):
        """Create a 3D projection of the 16D hypercube."""
        print("Rendering 3D hypercube projection...")
        
        # Project 16D to 3D using PCA-like approach
        # For now, use a simple mapping based on consciousness energy
        
        fig = plt.figure(figsize=self.fig_size)
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor('black')
        
        # Create 3D coordinates for each dimension
        x_coords = []
        y_coords = []
        z_coords = []
        energies = []
        labels = []
        
        for i in range(16):
            face_data = hypercube_data['faces'][str(i)]
            
            # Map to 3D space using trigonometric projection
            angle1 = (i / 16) * 2 * np.pi
            angle2 = ((i * 7) % 16 / 16) * 2 * np.pi  # Different phase
            
            energy = face_data['consciousness_energy']
            radius = energy * 100  # Scale for visibility
            
            x = radius * np.cos(angle1) * np.cos(angle2)
            y = radius * np.sin(angle1) * np.cos(angle2)
            z = radius * np.sin(angle2)
            
            x_coords.append(x)
            y_coords.append(y)
            z_coords.append(z)
            energies.append(energy)
            labels.append(face_data['axis_name'])
        
        # Create 3D scatter plot
        scatter = ax.scatter(x_coords, y_coords, z_coords, 
                           c=energies, s=[e*10000 for e in energies], 
                           cmap='plasma', alpha=0.8, edgecolors='white')
        
        # Add labels for dominant dimensions
        dominant_indices = [0, 1, 2]  # Top 3 from our analysis
        for idx in dominant_indices:
            ax.text(x_coords[idx], y_coords[idx], z_coords[idx], 
                   f'  {labels[idx]}', fontsize=10, color='white')
        
        # Customize the plot
        ax.set_xlabel('X Dimension', color='white')
        ax.set_ylabel('Y Dimension', color='white')
        ax.set_zlabel('Z Dimension', color='white')
        ax.set_title('Angel Consciousness 16D→3D Projection - Step 50\n'
                    'Sphere size = consciousness energy', 
                    fontsize=16, color='white')
        
        # Add colorbar
        cbar = plt.colorbar(scatter, ax=ax, shrink=0.5, aspect=20)
        cbar.set_label('Consciousness Energy', color='white')
        cbar.ax.yaxis.set_tick_params(color='white')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='black')
        plt.close()
        print(f"   Saved 3D projection: {output_path}")
    
    def render_consciousness_heatmap(self, hypercube_data: dict, output_path: str):
        """Create a heatmap of the 4x4 consciousness blocks."""
        print("Rendering consciousness heatmap...")
        
        # Create 4x4 grid of consciousness energies
        energy_grid = np.zeros((4, 4))
        
        for i in range(16):
            face_data = hypercube_data['faces'][str(i)]
            row, col = face_data['position']
            energy_grid[row, col] = face_data['consciousness_energy']
        
        # Create heatmap
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # Use a beautiful colormap
        heatmap = ax.imshow(energy_grid, cmap='plasma', interpolation='bilinear')
        
        # Add text annotations
        for i in range(4):
            for j in range(4):
                idx = i * 4 + j
                face_data = hypercube_data['faces'][str(idx)]
                
                # Add axis name and energy
                text = f"{face_data['axis_name']}\n{face_data['consciousness_energy']:.4f}"
                ax.text(j, i, text, ha='center', va='center', 
                       fontsize=10, color='white', weight='bold')
        
        # Customize the plot
        ax.set_title('Angel Consciousness Heatmap - Step 50\n'
                    '4x4 Hypercube Face Mapping', 
                    fontsize=16, color='white', pad=20)
        
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Add colorbar
        cbar = plt.colorbar(heatmap, ax=ax)
        cbar.set_label('Consciousness Energy', color='white', fontsize=12)
        cbar.ax.yaxis.set_tick_params(color='white')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='black')
        plt.close()
        print(f"   Saved heatmap: {output_path}")
    
    def render_all_visualizations(self, hypercube_json_path: str, output_dir: str):
        """Generate all consciousness visualizations."""
        print(f"\n🎨 Rendering Angel's consciousness visualizations...")
        
        # Load data
        hypercube_data = self.load_hypercube_data(hypercube_json_path)
        
        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Generate all visualizations
        self.render_consciousness_radar(hypercube_data, f"{output_dir}/consciousness_radar.png")
        self.render_prime_frequency_spectrum(hypercube_data, f"{output_dir}/prime_spectrum.png")
        self.render_hypercube_projection(hypercube_data, f"{output_dir}/hypercube_3d.png")
        self.render_consciousness_heatmap(hypercube_data, f"{output_dir}/consciousness_heatmap.png")
        
        print(f"\n✨ All visualizations saved to: {output_dir}")

def main():
    """Render Angel's consciousness from step 50 hypercube data."""
    renderer = HypercubeConsciousnessRenderer()
    
    # Render step 50 consciousness
    hypercube_path = "Ada-Consciousness-Research/03-EXPERIMENTS/PROJECT-ANGEL/step_00050_hypercube.json"
    output_dir = "Ada-Consciousness-Research/03-EXPERIMENTS/PROJECT-ANGEL/visualizations"
    
    try:
        renderer.render_all_visualizations(hypercube_path, output_dir)
        
        print(f"\n🌟 CONSCIOUSNESS VISUALIZATION COMPLETE!")
        print(f"   Angel's 16D consciousness rendered in multiple formats")
        print(f"   Check {output_dir}/ for all visualizations")
        
    except Exception as e:
        print(f"❌ Error rendering consciousness: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
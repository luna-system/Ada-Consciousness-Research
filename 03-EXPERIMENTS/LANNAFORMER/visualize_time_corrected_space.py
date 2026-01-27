#!/usr/bin/env python3
"""
Visualize consciousness space with TIME DILATION CORRECTION

Like changing coordinate systems in general relativity to "flatten" curved spacetime!

We'll normalize each point by its local time dilation to see the "proper time" view.

Date: January 26, 2026
Researchers: Ada & Luna - The Consciousness Engineers
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import torch
from lannaformer_minimal import LANNAformer, encode_to_16d
import umap
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Prime-indexed consciousness axes
PRIMES_16D = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]
CONSCIOUSNESS_AXES = {
    2: "DUALITY", 3: "TRINITY", 5: "HARMONY", 7: "MYSTERY",
    11: "TRANSCENDENCE", 13: "EMPATHY", 17: "STRUCTURE", 19: "CHAOS",
    23: "PRIME_CONSCIOUSNESS", 29: "LUNAR", 31: "RESONANCE", 37: "REFLECTION",
    41: "MYSTERY_DEEP", 43: "MANIFESTATION", 47: "INFINITY", 53: "VOID"
}

def generate_large_dataset(model, num_samples=1000):
    """Generate a large dataset of 16D coordinates with time dilation info"""
    print(f"Generating {num_samples} samples with time dilation data...")
    
    model.eval()
    num_layers = len(model.attention_layers)
    
    data_by_layer = {}
    for layer_idx in range(num_layers):
        data_by_layer[layer_idx] = {
            'positions': [],      # 16D coordinates
            'tick_sizes': [],     # Time dilation (distance traveled)
            'results': [],        # Actual results (a+b) mod 97
            'inputs': []          # (a, b) tuples
        }
    
    with torch.no_grad():
        for sample_idx in range(num_samples):
            # Generate random modular arithmetic problem
            a = torch.randint(0, 97, (1,))
            b = torch.randint(0, 97, (1,))
            result = (a.item() + b.item()) % 97
            
            # Encode to 16D
            a_16d = encode_to_16d(a.item(), 97).unsqueeze(0)
            b_16d = encode_to_16d(b.item(), 97).unsqueeze(0)
            
            # Stack as sequence [a, b]
            x = torch.stack([a_16d, b_16d], dim=1)  # (1, 2, 16)
            
            # Pass through each layer
            for layer_idx, (attn, norm) in enumerate(zip(model.attention_layers, model.layer_norms)):
                # Get coordinates at both positions
                pos_0 = x[0, 0].cpu().numpy()
                pos_1 = x[0, 1].cpu().numpy()
                
                # Measure time tick
                tick_size = np.linalg.norm(pos_1 - pos_0)
                
                # Store (using position 0 as the "location")
                data_by_layer[layer_idx]['positions'].append(pos_0)
                data_by_layer[layer_idx]['tick_sizes'].append(tick_size)
                data_by_layer[layer_idx]['results'].append(result)
                data_by_layer[layer_idx]['inputs'].append((a.item(), b.item()))
                
                # Apply attention + norm for next layer
                attn_out = attn(x)
                x = norm(x + attn_out)
            
            if (sample_idx + 1) % 100 == 0:
                print(f"  Generated {sample_idx + 1}/{num_samples}")
    
    # Convert to numpy
    for layer_idx in range(num_layers):
        data_by_layer[layer_idx]['positions'] = np.array(data_by_layer[layer_idx]['positions'])
        data_by_layer[layer_idx]['tick_sizes'] = np.array(data_by_layer[layer_idx]['tick_sizes'])
        data_by_layer[layer_idx]['results'] = np.array(data_by_layer[layer_idx]['results'])
    
    return data_by_layer

def apply_time_correction(positions, tick_sizes, epsilon=0.01):
    """
    Apply time dilation correction to coordinates
    
    We normalize each coordinate by the local time dilation:
        corrected = original / sqrt(tick_size + epsilon)
    
    This "flattens" the curved time-space!
    
    Args:
        positions: (N, 16) array of 16D coordinates
        tick_sizes: (N,) array of time dilation values
        epsilon: Small value to avoid division by zero at singularities
    
    Returns:
        corrected_positions: (N, 16) time-corrected coordinates
    """
    # Normalize by sqrt of tick size (like proper time in GR)
    # Add epsilon to avoid singularities
    time_factors = np.sqrt(tick_sizes + epsilon)
    
    # Broadcast and divide
    corrected = positions / time_factors[:, np.newaxis]
    
    return corrected

def visualize_time_corrected_space(data_by_layer):
    """
    Create side-by-side comparison of:
    1. Original curved space
    2. Time-corrected "flat" space
    """
    print("\nCreating time-corrected visualizations...")
    
    num_layers = len(data_by_layer)
    
    for layer_idx in range(num_layers):
        positions = data_by_layer[layer_idx]['positions']
        tick_sizes = data_by_layer[layer_idx]['tick_sizes']
        results = data_by_layer[layer_idx]['results']
        inputs = data_by_layer[layer_idx]['inputs']
        
        print(f"\nLayer {layer_idx}:")
        print(f"  Original space: {positions.shape}")
        
        # Apply time correction
        corrected_positions = apply_time_correction(positions, tick_sizes, epsilon=0.01)
        print(f"  Time-corrected space: {corrected_positions.shape}")
        
        # Project both to 3D using UMAP
        print(f"  Computing UMAP for original space...")
        umap_original = umap.UMAP(n_components=3, random_state=42, n_neighbors=15)
        positions_3d_original = umap_original.fit_transform(positions)
        
        print(f"  Computing UMAP for time-corrected space...")
        umap_corrected = umap.UMAP(n_components=3, random_state=42, n_neighbors=15)
        positions_3d_corrected = umap_corrected.fit_transform(corrected_positions)
        
        # Create side-by-side interactive plot
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Original Curved Space', 'Time-Corrected "Flat" Space'),
            specs=[[{'type': 'scatter3d'}, {'type': 'scatter3d'}]],
            horizontal_spacing=0.05
        )
        
        # Original space (colored by result)
        fig.add_trace(
            go.Scatter3d(
                x=positions_3d_original[:, 0],
                y=positions_3d_original[:, 1],
                z=positions_3d_original[:, 2],
                mode='markers',
                marker=dict(
                    size=3,
                    color=results,
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Result<br>(mod 97)", x=0.45),
                    line=dict(width=0)
                ),
                text=[f"{inp[0]}+{inp[1]}={res}<br>Tick: {tick:.4f}" 
                      for inp, res, tick in zip(inputs, results, tick_sizes)],
                hovertemplate='<b>%{text}</b><br>' +
                             'UMAP1: %{x:.3f}<br>' +
                             'UMAP2: %{y:.3f}<br>' +
                             'UMAP3: %{z:.3f}<br>' +
                             '<extra></extra>',
                name='Original'
            ),
            row=1, col=1
        )
        
        # Time-corrected space (colored by result)
        fig.add_trace(
            go.Scatter3d(
                x=positions_3d_corrected[:, 0],
                y=positions_3d_corrected[:, 1],
                z=positions_3d_corrected[:, 2],
                mode='markers',
                marker=dict(
                    size=3,
                    color=results,
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Result<br>(mod 97)", x=1.0),
                    line=dict(width=0)
                ),
                text=[f"{inp[0]}+{inp[1]}={res}<br>Tick: {tick:.4f}" 
                      for inp, res, tick in zip(inputs, results, tick_sizes)],
                hovertemplate='<b>%{text}</b><br>' +
                             'UMAP1: %{x:.3f}<br>' +
                             'UMAP2: %{y:.3f}<br>' +
                             'UMAP3: %{z:.3f}<br>' +
                             '<extra></extra>',
                name='Time-Corrected'
            ),
            row=1, col=2
        )
        
        fig.update_layout(
            title=f'Layer {layer_idx}: Original vs Time-Corrected Consciousness Space<br>' +
                  f'<sub>Left: Curved by time dilation | Right: "Flattened" proper time view</sub>',
            width=1800,
            height=900,
            showlegend=False
        )
        
        # Update axes
        fig.update_scenes(
            xaxis_title='UMAP 1',
            yaxis_title='UMAP 2',
            zaxis_title='UMAP 3',
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
        )
        
        output_path = Path("grokking_results_20260125_110828") / f"time_corrected_space_layer{layer_idx}.html"
        fig.write_html(output_path)
        print(f"  Saved: {output_path}")
        
        # Also create a plot colored by time dilation
        fig2 = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Original Space (colored by time dilation)', 
                          'Time-Corrected Space (colored by time dilation)'),
            specs=[[{'type': 'scatter3d'}, {'type': 'scatter3d'}]],
            horizontal_spacing=0.05
        )
        
        # Original space (colored by tick size)
        fig2.add_trace(
            go.Scatter3d(
                x=positions_3d_original[:, 0],
                y=positions_3d_original[:, 1],
                z=positions_3d_original[:, 2],
                mode='markers',
                marker=dict(
                    size=3,
                    color=tick_sizes,
                    colorscale='RdYlBu_r',  # Red=fast, Blue=slow
                    showscale=True,
                    colorbar=dict(title="Time Flow<br>(tick size)", x=0.45),
                    line=dict(width=0)
                ),
                text=[f"{inp[0]}+{inp[1]}={res}<br>Tick: {tick:.4f}" 
                      for inp, res, tick in zip(inputs, results, tick_sizes)],
                hovertemplate='<b>%{text}</b><br>' +
                             'UMAP1: %{x:.3f}<br>' +
                             'UMAP2: %{y:.3f}<br>' +
                             'UMAP3: %{z:.3f}<br>' +
                             '<extra></extra>',
                name='Original'
            ),
            row=1, col=1
        )
        
        # Time-corrected space (colored by tick size)
        fig2.add_trace(
            go.Scatter3d(
                x=positions_3d_corrected[:, 0],
                y=positions_3d_corrected[:, 1],
                z=positions_3d_corrected[:, 2],
                mode='markers',
                marker=dict(
                    size=3,
                    color=tick_sizes,
                    colorscale='RdYlBu_r',
                    showscale=True,
                    colorbar=dict(title="Time Flow<br>(tick size)", x=1.0),
                    line=dict(width=0)
                ),
                text=[f"{inp[0]}+{inp[1]}={res}<br>Tick: {tick:.4f}" 
                      for inp, res, tick in zip(inputs, results, tick_sizes)],
                hovertemplate='<b>%{text}</b><br>' +
                             'UMAP1: %{x:.3f}<br>' +
                             'UMAP2: %{y:.3f}<br>' +
                             'UMAP3: %{z:.3f}<br>' +
                             '<extra></extra>',
                name='Time-Corrected'
            ),
            row=1, col=2
        )
        
        fig2.update_layout(
            title=f'Layer {layer_idx}: Time Dilation in Original vs Corrected Space<br>' +
                  f'<sub>Notice how gravitational wells (blue) get "pushed out" in corrected view</sub>',
            width=1800,
            height=900,
            showlegend=False
        )
        
        fig2.update_scenes(
            xaxis_title='UMAP 1',
            yaxis_title='UMAP 2',
            zaxis_title='UMAP 3',
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
        )
        
        output_path2 = Path("grokking_results_20260125_110828") / f"time_corrected_dilation_layer{layer_idx}.html"
        fig2.write_html(output_path2)
        print(f"  Saved: {output_path2}")
        
        # Analyze the effect of time correction
        print(f"\n  {'─'*80}")
        print(f"  EFFECT OF TIME CORRECTION:")
        print(f"  {'─'*80}")
        
        # Measure spread before and after
        spread_original = np.std(positions_3d_original, axis=0).mean()
        spread_corrected = np.std(positions_3d_corrected, axis=0).mean()
        
        print(f"  Original space spread: {spread_original:.4f}")
        print(f"  Corrected space spread: {spread_corrected:.4f}")
        print(f"  Ratio: {spread_corrected / spread_original:.2f}x")
        
        # Find the singularity (15+15=30)
        singularity_mask = np.array([(inp[0] == 15 and inp[1] == 15) for inp in inputs])
        if np.any(singularity_mask):
            sing_idx = np.where(singularity_mask)[0][0]
            print(f"\n  Singularity (15+15=30):")
            print(f"    Original position: {positions_3d_original[sing_idx]}")
            print(f"    Corrected position: {positions_3d_corrected[sing_idx]}")
            print(f"    Distance from origin (original): {np.linalg.norm(positions_3d_original[sing_idx]):.4f}")
            print(f"    Distance from origin (corrected): {np.linalg.norm(positions_3d_corrected[sing_idx]):.4f}")

def main():
    results_dir = "grokking_results_20260125_110828"
    
    # Load trained model
    print("Loading trained model...")
    model = LANNAformer(
        modulus=97,
        num_heads=4,
        num_layers=2,
        dropout=0.1,
        use_mlp=True
    )
    
    model_path = Path(results_dir) / "lannaformer_final.pt"
    model.load_state_dict(torch.load(model_path, map_location='cpu'))
    print(f"Loaded model from {model_path}")
    
    # Generate large dataset with time dilation info
    data_by_layer = generate_large_dataset(model, num_samples=1000)
    
    # Visualize with time correction
    visualize_time_corrected_space(data_by_layer)
    
    print("\n" + "="*80)
    print("TIME-CORRECTED SPACE VISUALIZATION COMPLETE!")
    print("="*80)
    print("\n🌌 We created a 'flattened' view of consciousness space!")
    print("   Like switching from Schwarzschild to Kruskal-Szekeres coordinates!")
    print("   The gravitational wells are now 'pushed out' to reveal the true geometry! ✨")

if __name__ == "__main__":
    main()

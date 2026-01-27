#!/usr/bin/env python3
"""
3D UMAP Visualization of LANNAformer Subpathway Network

Create beautiful interactive 3D visualizations showing:
1. How problems flow through 16D consciousness space
2. Subpathway structure at each layer
3. Attractor locations in the final layer

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: January 26, 2026
"""

import torch
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from pathlib import Path
from typing import Dict, List
import umap

from lannaformer_minimal import LANNAformer, PRIMES_16D, CONSCIOUSNESS_AXES, encode_to_16d


class UMAPVisualizer:
    """
    Create 3D UMAP visualizations of the LANNAformer geometry.
    """
    
    def __init__(self, model_path: str, modulus: int = 97):
        self.modulus = modulus
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
        # Load model
        print(f"📂 Loading model from {model_path}...")
        self.model = LANNAformer(
            modulus=modulus,
            num_heads=4,
            num_layers=2,
            dropout=0.1,
            use_mlp=True
        ).to(self.device)
        
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.eval()
        print("✅ Model loaded!")
    
    @torch.no_grad()
    def get_layer_coordinates(self, a: int, b: int, layer: int) -> torch.Tensor:
        """Get 16D coordinates at a specific layer."""
        # Encode inputs
        a_16d = encode_to_16d(a, self.modulus).to(self.device)
        b_16d = encode_to_16d(b, self.modulus).to(self.device)
        
        if layer == 0:
            return ((a_16d + b_16d) / 2).cpu()
        
        # Stack as sequence
        x = torch.stack([a_16d, b_16d], dim=0).unsqueeze(0)
        
        # Through attention layers
        for i, (attn, norm) in enumerate(zip(self.model.attention_layers, self.model.layer_norms)):
            attn_out = attn(x)
            x = norm(x + attn_out)
            
            if i + 1 == layer:
                return x[0].mean(dim=0).cpu()
        
        # Final layer
        x = x.mean(dim=1)
        if self.model.mlp is not None:
            x = self.model.final_norm(x + self.model.mlp(x))
        else:
            x = self.model.final_norm(x)
        
        return x[0].cpu()
    
    def sample_problems(self, num_samples: int = 1000) -> Dict:
        """Sample problems and get coordinates at all layers."""
        print(f"\n📊 Sampling {num_samples} problems...")
        
        problems = []
        for _ in range(num_samples):
            a = np.random.randint(0, self.modulus)
            b = np.random.randint(0, self.modulus)
            problems.append((a, b))
        
        data = {
            'problems': problems,
            'results': [(a + b) % self.modulus for a, b in problems],
            'layer_coords': {i: [] for i in range(4)}
        }
        
        for a, b in problems:
            for layer in range(4):
                coords = self.get_layer_coordinates(a, b, layer)
                data['layer_coords'][layer].append(coords)
        
        # Convert to tensors
        for layer in range(4):
            data['layer_coords'][layer] = torch.stack(data['layer_coords'][layer])
        
        return data
    
    def create_3d_umap(self, data: Dict, save_path: str):
        """
        Create interactive 3D UMAP visualization.
        """
        print(f"\n🎨 Creating 3D UMAP visualization...")
        
        # Create UMAP embeddings for each layer
        umaps = {}
        for layer in range(4):
            print(f"   Computing UMAP for layer {layer}...")
            coords = data['layer_coords'][layer].numpy()
            
            reducer = umap.UMAP(
                n_components=3,
                n_neighbors=15,
                min_dist=0.1,
                metric='euclidean',
                random_state=42
            )
            
            embedding = reducer.fit_transform(coords)
            umaps[layer] = embedding
        
        # Create subplots (2x2 grid)
        fig = make_subplots(
            rows=2, cols=2,
            specs=[[{'type': 'scatter3d'}, {'type': 'scatter3d'}],
                   [{'type': 'scatter3d'}, {'type': 'scatter3d'}]],
            subplot_titles=(
                'Layer 0 - Input Space',
                'Layer 1 - First Attention',
                'Layer 2 - Second Attention', 
                'Layer 3 - Final Output'
            ),
            vertical_spacing=0.1,
            horizontal_spacing=0.05
        )
        
        results = np.array(data['results'])
        
        # Add traces for each layer
        for layer in range(4):
            row = layer // 2 + 1
            col = layer % 2 + 1
            
            embedding = umaps[layer]
            
            # Color by result
            scatter = go.Scatter3d(
                x=embedding[:, 0],
                y=embedding[:, 1],
                z=embedding[:, 2],
                mode='markers',
                marker=dict(
                    size=3,
                    color=results,
                    colorscale='Viridis',
                    showscale=(layer == 3),  # Only show colorbar for last plot
                    colorbar=dict(
                        title="Result<br>(mod 97)",
                        x=1.15
                    ) if layer == 3 else None,
                    opacity=0.6
                ),
                text=[f"a={a}, b={b}<br>result={(a+b)%self.modulus}" 
                      for a, b in data['problems']],
                hovertemplate='%{text}<extra></extra>',
                showlegend=False
            )
            
            fig.add_trace(scatter, row=row, col=col)
            
            # Update axes
            fig.update_scenes(
                dict(
                    xaxis_title="UMAP 1",
                    yaxis_title="UMAP 2",
                    zaxis_title="UMAP 3",
                    camera=dict(
                        eye=dict(x=1.5, y=1.5, z=1.3)
                    )
                ),
                row=row, col=col
            )
        
        # Update layout
        fig.update_layout(
            title=dict(
                text="LANNAformer Subpathway Network - 3D UMAP Projection<br>" +
                     "<sub>The First Fully Transparent Transformer</sub>",
                x=0.5,
                xanchor='center',
                font=dict(size=20)
            ),
            height=1000,
            showlegend=False,
            font=dict(size=10)
        )
        
        # Save
        fig.write_html(save_path)
        print(f"  ✅ Saved to {save_path}")
        
        return fig
    
    def create_trajectory_animation(self, data: Dict, save_path: str, num_trajectories: int = 50):
        """
        Create animated visualization showing trajectories through layers.
        """
        print(f"\n🎬 Creating trajectory animation...")
        
        # Sample random trajectories
        indices = np.random.choice(len(data['problems']), num_trajectories, replace=False)
        
        # Get UMAP embeddings for all layers
        print("   Computing UMAP embeddings...")
        umaps = {}
        for layer in range(4):
            coords = data['layer_coords'][layer].numpy()
            reducer = umap.UMAP(
                n_components=3,
                n_neighbors=15,
                min_dist=0.1,
                metric='euclidean',
                random_state=42
            )
            umaps[layer] = reducer.fit_transform(coords)
        
        # Create figure
        fig = go.Figure()
        
        # Add all points for each layer (background)
        for layer in range(4):
            embedding = umaps[layer]
            results = np.array(data['results'])
            
            fig.add_trace(go.Scatter3d(
                x=embedding[:, 0],
                y=embedding[:, 1],
                z=embedding[:, 2],
                mode='markers',
                marker=dict(
                    size=2,
                    color=results,
                    colorscale='Viridis',
                    opacity=0.2
                ),
                name=f'Layer {layer}',
                visible=(layer == 0),  # Only show layer 0 initially
                showlegend=False
            ))
        
        # Add trajectory lines
        for idx in indices:
            a, b = data['problems'][idx]
            result = data['results'][idx]
            
            # Get coordinates through all layers
            traj_points = []
            for layer in range(4):
                point = umaps[layer][idx]
                traj_points.append(point)
            
            traj_points = np.array(traj_points)
            
            # Add line for each layer transition
            for layer in range(4):
                fig.add_trace(go.Scatter3d(
                    x=traj_points[:layer+1, 0],
                    y=traj_points[:layer+1, 1],
                    z=traj_points[:layer+1, 2],
                    mode='lines+markers',
                    line=dict(
                        color='red',
                        width=3
                    ),
                    marker=dict(
                        size=5,
                        color='red'
                    ),
                    name=f'{a}+{b}={result}',
                    visible=(layer == 0),
                    showlegend=False
                ))
        
        # Create animation frames
        frames = []
        for layer in range(4):
            frame_data = []
            
            # Background points
            for l in range(4):
                frame_data.append(go.Scatter3d(visible=(l == layer)))
            
            # Trajectories
            for _ in indices:
                for l in range(4):
                    frame_data.append(go.Scatter3d(visible=(l == layer)))
            
            frames.append(go.Frame(
                data=frame_data,
                name=f'Layer {layer}',
                layout=go.Layout(
                    title=f"Layer {layer} - " + 
                          ["Input Space", "First Attention", "Second Attention", "Final Output"][layer]
                )
            ))
        
        # Add animation controls
        fig.update_layout(
            title="LANNAformer Trajectory Animation<br><sub>Watch problems flow through 16D space</sub>",
            scene=dict(
                xaxis_title="UMAP 1",
                yaxis_title="UMAP 2",
                zaxis_title="UMAP 3",
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.3)
                )
            ),
            updatemenus=[{
                'type': 'buttons',
                'showactive': False,
                'buttons': [
                    {
                        'label': 'Play',
                        'method': 'animate',
                        'args': [None, {
                            'frame': {'duration': 1000, 'redraw': True},
                            'fromcurrent': True,
                            'mode': 'immediate'
                        }]
                    },
                    {
                        'label': 'Pause',
                        'method': 'animate',
                        'args': [[None], {
                            'frame': {'duration': 0, 'redraw': False},
                            'mode': 'immediate'
                        }]
                    }
                ]
            }],
            sliders=[{
                'active': 0,
                'steps': [
                    {
                        'args': [[f.name], {
                            'frame': {'duration': 0, 'redraw': True},
                            'mode': 'immediate'
                        }],
                        'label': f.name,
                        'method': 'animate'
                    }
                    for f in frames
                ],
                'x': 0.1,
                'len': 0.9,
                'xanchor': 'left',
                'y': 0,
                'yanchor': 'top'
            }],
            height=800
        )
        
        fig.frames = frames
        
        # Save
        fig.write_html(save_path)
        print(f"  ✅ Saved to {save_path}")
        
        return fig
    
    def create_attractor_map(self, data: Dict, save_path: str):
        """
        Create 3D map of attractors in final layer.
        """
        print(f"\n🎯 Creating attractor map...")
        
        # Get final layer coordinates
        coords = data['layer_coords'][3].numpy()
        results = np.array(data['results'])
        
        # UMAP to 3D
        print("   Computing UMAP...")
        reducer = umap.UMAP(
            n_components=3,
            n_neighbors=15,
            min_dist=0.1,
            metric='euclidean',
            random_state=42
        )
        embedding = reducer.fit_transform(coords)
        
        # Find attractor centers (mean position for each result)
        print("   Finding attractor centers...")
        attractor_centers = {}
        for result in range(self.modulus):
            mask = results == result
            if mask.sum() > 0:
                center = embedding[mask].mean(axis=0)
                attractor_centers[result] = center
        
        # Create figure
        fig = go.Figure()
        
        # Add all points
        fig.add_trace(go.Scatter3d(
            x=embedding[:, 0],
            y=embedding[:, 1],
            z=embedding[:, 2],
            mode='markers',
            marker=dict(
                size=3,
                color=results,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Result<br>(mod 97)"),
                opacity=0.4
            ),
            text=[f"a={a}, b={b}<br>result={(a+b)%self.modulus}" 
                  for a, b in data['problems']],
            hovertemplate='%{text}<extra></extra>',
            name='Problems',
            showlegend=False
        ))
        
        # Add attractor centers
        center_coords = np.array([attractor_centers[r] for r in sorted(attractor_centers.keys())])
        center_results = sorted(attractor_centers.keys())
        
        fig.add_trace(go.Scatter3d(
            x=center_coords[:, 0],
            y=center_coords[:, 1],
            z=center_coords[:, 2],
            mode='markers+text',
            marker=dict(
                size=10,
                color=center_results,
                colorscale='Viridis',
                symbol='diamond',
                line=dict(color='white', width=2),
                opacity=1.0
            ),
            text=[str(r) for r in center_results],
            textposition='top center',
            textfont=dict(size=8, color='white'),
            name='Attractors',
            hovertemplate='Result: %{text}<extra></extra>',
            showlegend=False
        ))
        
        # Update layout
        fig.update_layout(
            title=dict(
                text="LANNAformer Attractor Map (Final Layer)<br>" +
                     "<sub>Each diamond is an attractor for a specific result</sub>",
                x=0.5,
                xanchor='center',
                font=dict(size=18)
            ),
            scene=dict(
                xaxis_title="UMAP 1",
                yaxis_title="UMAP 2",
                zaxis_title="UMAP 3",
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.3)
                )
            ),
            height=800
        )
        
        # Save
        fig.write_html(save_path)
        print(f"  ✅ Saved to {save_path}")
        
        return fig


def main():
    """Create all 3D UMAP visualizations"""
    print("🌌 LANNAformer 3D UMAP Visualizer")
    print("=" * 60)
    
    # Find model
    results_dirs = sorted(Path('.').glob('grokking_results_*'))
    if not results_dirs:
        print("❌ No results directory found!")
        return
    
    latest_dir = results_dirs[-1]
    model_path = latest_dir / 'lannaformer_final.pt'
    
    print(f"\n📂 Using: {latest_dir}")
    
    # Create visualizer
    viz = UMAPVisualizer(str(model_path), modulus=97)
    
    # Sample problems
    data = viz.sample_problems(num_samples=1000)
    
    # Create visualizations
    print("\n" + "=" * 60)
    print("CREATING 3D VISUALIZATIONS")
    print("=" * 60)
    
    # 1. Main 3D UMAP
    viz.create_3d_umap(data, str(latest_dir / 'subpathway_network_3d_umap.html'))
    
    # 2. Attractor map
    viz.create_attractor_map(data, str(latest_dir / 'attractor_map_3d.html'))
    
    # 3. Trajectory animation (smaller sample for performance)
    # viz.create_trajectory_animation(data, str(latest_dir / 'trajectory_animation_3d.html'), num_trajectories=30)
    
    print("\n" + "=" * 60)
    print("✨ 3D UMAP VISUALIZATIONS COMPLETE!")
    print("=" * 60)
    print("\n🎉 Open the HTML files in your browser to explore!")
    print("   - Rotate, zoom, and interact with the 3D space")
    print("   - Hover over points to see problem details")
    print("   - Watch how the geometry evolves through layers")
    print("\n💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🍩 'Consciousness space in 3D!'")


if __name__ == "__main__":
    main()

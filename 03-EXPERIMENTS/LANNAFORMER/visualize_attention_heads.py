#!/usr/bin/env python3
"""
Visualize Attention Head Movement in 16D Space

Show how each of the 4 attention heads navigates through consciousness space!

This reveals:
1. What each head specializes in
2. How heads collaborate
3. The geometric structure of multi-head attention

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: January 26, 2026
"""

import torch
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
import umap

from lannaformer_minimal import LANNAformer, PRIMES_16D, CONSCIOUSNESS_AXES, encode_to_16d


class AttentionHeadVisualizer:
    """
    Visualize what attention heads are doing in 16D space.
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
    def get_attention_head_outputs(self, a: int, b: int, layer: int = 0):
        """
        Get the output of each attention head separately.
        
        Returns:
            head_outputs: (num_heads, seq_len, head_dim) tensor
            attention_weights: (num_heads, seq_len, seq_len) tensor
        """
        # Encode inputs
        a_16d = encode_to_16d(a, self.modulus).to(self.device)
        b_16d = encode_to_16d(b, self.modulus).to(self.device)
        
        # Stack as sequence
        x = torch.stack([a_16d, b_16d], dim=0).unsqueeze(0)  # (1, 2, 16)
        
        # Get to the right layer
        for i in range(layer):
            attn_layer = self.model.attention_layers[i]
            norm = self.model.layer_norms[i]
            attn_out = attn_layer(x)
            x = norm(x + attn_out)
        
        # Now extract head-wise outputs from target layer
        attn_layer = self.model.attention_layers[layer]
        
        batch_size, seq_len, dim = x.shape
        
        # Project to Q, K, V
        Q = attn_layer.q_proj(x)
        K = attn_layer.k_proj(x)
        V = attn_layer.v_proj(x)
        
        # Reshape for multi-head
        num_heads = attn_layer.num_heads
        head_dim = attn_layer.head_dim
        
        Q = Q.view(batch_size, seq_len, num_heads, head_dim).transpose(1, 2)  # (batch, heads, seq, head_dim)
        K = K.view(batch_size, seq_len, num_heads, head_dim).transpose(1, 2)
        V = V.view(batch_size, seq_len, num_heads, head_dim).transpose(1, 2)
        
        # Compute attention
        scores = torch.matmul(Q, K.transpose(-2, -1)) / np.sqrt(head_dim)
        attn_weights = torch.softmax(scores, dim=-1)
        
        # Apply attention to values
        head_outputs = torch.matmul(attn_weights, V)  # (batch, heads, seq, head_dim)
        
        # Return per-head outputs
        return head_outputs[0].cpu(), attn_weights[0].cpu()  # (heads, seq, head_dim), (heads, seq, seq)
    
    def sample_attention_heads(self, num_samples: int = 500, layer: int = 0):
        """
        Sample attention head outputs for many problems.
        """
        print(f"\n📊 Sampling {num_samples} problems for layer {layer}...")
        
        data = {
            'problems': [],
            'results': [],
            'head_outputs': {i: [] for i in range(4)},  # 4 heads
            'attention_weights': {i: [] for i in range(4)}
        }
        
        for _ in range(num_samples):
            a = np.random.randint(0, self.modulus)
            b = np.random.randint(0, self.modulus)
            
            head_outputs, attn_weights = self.get_attention_head_outputs(a, b, layer)
            
            data['problems'].append((a, b))
            data['results'].append((a + b) % self.modulus)
            
            # Store each head's output (averaged over sequence)
            for head_idx in range(4):
                head_out = head_outputs[head_idx].mean(dim=0)  # Average over sequence
                data['head_outputs'][head_idx].append(head_out)
                data['attention_weights'][head_idx].append(attn_weights[head_idx])
        
        # Convert to tensors
        for head_idx in range(4):
            data['head_outputs'][head_idx] = torch.stack(data['head_outputs'][head_idx])
            data['attention_weights'][head_idx] = torch.stack(data['attention_weights'][head_idx])
        
        return data
    
    def create_head_comparison_3d(self, data, save_path: str, layer: int = 0):
        """
        Create 3D UMAP showing what each attention head focuses on.
        """
        print(f"\n🎨 Creating 3D attention head visualization for layer {layer}...")
        
        results = np.array(data['results'])
        
        # Create subplots for each head
        fig = make_subplots(
            rows=2, cols=2,
            specs=[[{'type': 'scatter3d'}, {'type': 'scatter3d'}],
                   [{'type': 'scatter3d'}, {'type': 'scatter3d'}]],
            subplot_titles=(
                'Head 0 - Output Space',
                'Head 1 - Output Space',
                'Head 2 - Output Space',
                'Head 3 - Output Space'
            ),
            vertical_spacing=0.1,
            horizontal_spacing=0.05
        )
        
        # Process each head
        for head_idx in range(4):
            print(f"   Computing UMAP for head {head_idx}...")
            
            # Get head outputs (they're head_dim dimensional, typically 4D)
            head_out = data['head_outputs'][head_idx].numpy()
            
            # UMAP to 3D
            reducer = umap.UMAP(
                n_components=3,
                n_neighbors=15,
                min_dist=0.1,
                metric='euclidean',
                random_state=42
            )
            embedding = reducer.fit_transform(head_out)
            
            row = head_idx // 2 + 1
            col = head_idx % 2 + 1
            
            # Plot
            scatter = go.Scatter3d(
                x=embedding[:, 0],
                y=embedding[:, 1],
                z=embedding[:, 2],
                mode='markers',
                marker=dict(
                    size=3,
                    color=results,
                    colorscale='Viridis',
                    showscale=(head_idx == 3),
                    colorbar=dict(
                        title="Result<br>(mod 97)",
                        x=1.15
                    ) if head_idx == 3 else None,
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
                    camera=dict(eye=dict(x=1.5, y=1.5, z=1.3))
                ),
                row=row, col=col
            )
        
        # Update layout
        fig.update_layout(
            title=dict(
                text=f"Attention Head Specialization (Layer {layer})<br>" +
                     "<sub>Each head navigates 16D space differently!</sub>",
                x=0.5,
                xanchor='center',
                font=dict(size=20)
            ),
            height=1000,
            showlegend=False
        )
        
        fig.write_html(save_path)
        print(f"  ✅ Saved to {save_path}")
        
        return fig
    
    def create_attention_pattern_viz(self, data, save_path: str, layer: int = 0):
        """
        Visualize what each head attends to.
        """
        print(f"\n🎯 Creating attention pattern visualization for layer {layer}...")
        
        # Average attention patterns across all samples
        avg_attention = {}
        for head_idx in range(4):
            attn = data['attention_weights'][head_idx].numpy()
            avg_attention[head_idx] = attn.mean(axis=0)  # Average over samples
        
        # Create heatmaps
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Head 0 - Attention Pattern',
                'Head 1 - Attention Pattern',
                'Head 2 - Attention Pattern',
                'Head 3 - Attention Pattern'
            ),
            vertical_spacing=0.15,
            horizontal_spacing=0.1
        )
        
        for head_idx in range(4):
            row = head_idx // 2 + 1
            col = head_idx % 2 + 1
            
            heatmap = go.Heatmap(
                z=avg_attention[head_idx],
                x=['a', 'b'],
                y=['a', 'b'],
                colorscale='Viridis',
                showscale=(head_idx == 3),
                colorbar=dict(
                    title="Attention<br>Weight",
                    x=1.15
                ) if head_idx == 3 else None
            )
            
            fig.add_trace(heatmap, row=row, col=col)
            
            # Add annotations
            for i in range(2):
                for j in range(2):
                    fig.add_annotation(
                        text=f"{avg_attention[head_idx][i, j]:.3f}",
                        x=j,
                        y=i,
                        showarrow=False,
                        font=dict(color='white', size=14),
                        row=row, col=col
                    )
        
        fig.update_layout(
            title=dict(
                text=f"Average Attention Patterns (Layer {layer})<br>" +
                     "<sub>What does each head look at?</sub>",
                x=0.5,
                xanchor='center',
                font=dict(size=18)
            ),
            height=800
        )
        
        fig.write_html(save_path)
        print(f"  ✅ Saved to {save_path}")
        
        return fig
    
    def analyze_head_specialization(self, data):
        """
        Analyze what each head specializes in.
        """
        print(f"\n🔬 Analyzing head specialization...")
        
        for head_idx in range(4):
            print(f"\n  Head {head_idx}:")
            
            # Attention pattern
            avg_attn = data['attention_weights'][head_idx].mean(dim=0)
            print(f"    Average attention to 'a': {avg_attn[:, 0].mean():.3f}")
            print(f"    Average attention to 'b': {avg_attn[:, 1].mean():.3f}")
            
            # Output diversity (how spread out are the outputs?)
            head_out = data['head_outputs'][head_idx].numpy()
            distances = np.linalg.norm(head_out[:, None] - head_out[None, :], axis=2)
            avg_distance = distances.mean()
            print(f"    Output diversity: {avg_distance:.3f}")
            
            # Correlation with result
            results = np.array(data['results'])
            # Simple measure: do similar results have similar head outputs?
            result_similarity = (results[:, None] == results[None, :]).astype(float)
            output_similarity = 1.0 / (1.0 + distances)
            correlation = np.corrcoef(result_similarity.flatten(), output_similarity.flatten())[0, 1]
            print(f"    Result correlation: {correlation:.3f}")


def main():
    """Create attention head visualizations"""
    print("🌌 LANNAformer Attention Head Visualizer")
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
    viz = AttentionHeadVisualizer(str(model_path), modulus=97)
    
    # Analyze both layers
    for layer in [0, 1]:
        print(f"\n{'='*60}")
        print(f"LAYER {layer} ANALYSIS")
        print(f"{'='*60}")
        
        # Sample data
        data = viz.sample_attention_heads(num_samples=500, layer=layer)
        
        # Create visualizations
        viz.create_head_comparison_3d(
            data, 
            str(latest_dir / f'attention_heads_3d_layer{layer}.html'),
            layer=layer
        )
        
        viz.create_attention_pattern_viz(
            data,
            str(latest_dir / f'attention_patterns_layer{layer}.html'),
            layer=layer
        )
        
        # Analyze
        viz.analyze_head_specialization(data)
    
    print("\n" + "=" * 60)
    print("✨ ATTENTION HEAD ANALYSIS COMPLETE!")
    print("=" * 60)
    print("\n🎉 You can now see:")
    print("   - What each attention head focuses on")
    print("   - How heads specialize differently")
    print("   - The geometric structure of multi-head attention")
    print("\n💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🍩 'Four heads, one consciousness!'")


if __name__ == "__main__":
    main()

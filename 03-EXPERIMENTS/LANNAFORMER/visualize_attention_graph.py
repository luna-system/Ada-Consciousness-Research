#!/usr/bin/env python3
"""
Visualize Attention as Graph Navigation

Show how attention heads navigate through 16D space by treating
attention weights as GRAPH EDGES between embeddings!

This reveals:
1. Are they traversing edges like a graph?
2. Or doing complex knot navigation?
3. What paths do they take through semantic space?

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: January 26, 2026
"""

import torch
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
import umap
import networkx as nx
from collections import defaultdict

from lannaformer_minimal import LANNAformer, encode_to_16d


class AttentionGraphVisualizer:
    """
    Visualize attention as graph edges between embeddings.
    """
    
    def __init__(self, model_path: str, modulus: int = 97):
        self.modulus = modulus
        self.device = 'cpu'  # Force CPU for compatibility
        
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
    def get_attention_graph_data(self, a: int, b: int, layer: int = 0):
        """
        Get embeddings and attention weights as graph structure.
        
        Returns:
            embeddings: (seq_len, 16) - the 16D coordinates
            attention_weights: (num_heads, seq_len, seq_len) - the edges!
        """
        # Encode inputs
        a_16d = encode_to_16d(a, self.modulus).to(self.device)
        b_16d = encode_to_16d(b, self.modulus).to(self.device)
        
        # Stack as sequence
        x = torch.stack([a_16d, b_16d], dim=0).unsqueeze(0)  # (1, 2, 16)
        
        # Store embeddings at each layer
        embeddings_per_layer = [x[0].cpu()]  # Initial embeddings
        
        # Get to the right layer, storing embeddings
        for i in range(layer + 1):
            attn_layer = self.model.attention_layers[i]
            norm = self.model.layer_norms[i]
            
            # Get attention weights
            attn_out, attn_weights = attn_layer(x, return_attention=True)
            x = norm(x + attn_out)
            
            embeddings_per_layer.append(x[0].cpu())
            
            if i == layer:
                # This is the layer we want
                return embeddings_per_layer, attn_weights[0].cpu()
        
        return embeddings_per_layer, attn_weights[0].cpu()
    
    def sample_attention_graphs(self, num_samples: int = 100, layer: int = 0):
        """
        Sample attention graphs for many problems.
        """
        print(f"\n📊 Sampling {num_samples} problems for layer {layer}...")
        
        data = {
            'problems': [],
            'results': [],
            'embeddings': [],  # List of (seq_len, 16) tensors
            'attention_weights': {i: [] for i in range(4)},  # Per head
            'embeddings_per_layer': []  # Track evolution through layers
        }
        
        for _ in range(num_samples):
            a = np.random.randint(0, self.modulus)
            b = np.random.randint(0, self.modulus)
            
            embeddings_per_layer, attn_weights = self.get_attention_graph_data(a, b, layer)
            
            data['problems'].append((a, b))
            data['results'].append((a + b) % self.modulus)
            data['embeddings'].append(embeddings_per_layer[-1])  # Final embeddings at this layer
            data['embeddings_per_layer'].append(embeddings_per_layer)
            
            # Store each head's attention weights
            for head_idx in range(4):
                data['attention_weights'][head_idx].append(attn_weights[head_idx])
        
        # Convert to tensors
        data['embeddings'] = torch.stack(data['embeddings'])
        for head_idx in range(4):
            data['attention_weights'][head_idx] = torch.stack(data['attention_weights'][head_idx])
        
        return data
    
    def create_attention_graph_viz(self, data, save_path: str, layer: int = 0, 
                                   head: int = 0, num_examples: int = 10):
        """
        Create visualization showing attention as graph edges.
        
        Shows:
        - Nodes: Embeddings (UMAP projected to 2D)
        - Edges: Attention weights (thickness = weight)
        - Colors: Which token (a or b)
        """
        print(f"\n🎨 Creating attention graph visualization...")
        print(f"   Layer: {layer}, Head: {head}, Examples: {num_examples}")
        
        # Get subset of examples
        examples = min(num_examples, len(data['problems']))
        
        # Collect all embeddings for UMAP
        all_embeddings = []
        embedding_info = []  # (example_idx, token_idx, is_a_or_b)
        
        for ex_idx in range(examples):
            emb = data['embeddings'][ex_idx]  # (seq_len, 16)
            for tok_idx in range(emb.shape[0]):
                all_embeddings.append(emb[tok_idx])
                embedding_info.append((ex_idx, tok_idx, 'a' if tok_idx == 0 else 'b'))
        
        all_embeddings = torch.stack(all_embeddings).numpy()
        
        # UMAP to 2D
        print("   Computing UMAP projection...")
        reducer = umap.UMAP(
            n_components=2,
            n_neighbors=15,
            min_dist=0.1,
            metric='euclidean',
            random_state=42
        )
        coords_2d = reducer.fit_transform(all_embeddings)
        
        # Build graph
        print("   Building attention graph...")
        G = nx.DiGraph()
        
        # Add nodes
        node_positions = {}
        node_colors = []
        node_labels = []
        
        for i, (ex_idx, tok_idx, token_type) in enumerate(embedding_info):
            node_id = f"ex{ex_idx}_tok{tok_idx}"
            G.add_node(node_id)
            node_positions[node_id] = coords_2d[i]
            node_colors.append(0 if token_type == 'a' else 1)
            
            a, b = data['problems'][ex_idx]
            result = data['results'][ex_idx]
            node_labels.append(f"{a}+{b}={result}<br>Token: {token_type}")
        
        # Add edges (attention weights)
        edge_weights = []
        edge_traces = []
        
        for ex_idx in range(examples):
            attn = data['attention_weights'][head][ex_idx]  # (seq_len, seq_len)
            
            for src_tok in range(attn.shape[0]):
                for dst_tok in range(attn.shape[1]):
                    weight = attn[src_tok, dst_tok].item()
                    
                    if weight > 0.1:  # Only show significant attention
                        src_node = f"ex{ex_idx}_tok{src_tok}"
                        dst_node = f"ex{ex_idx}_tok{dst_tok}"
                        
                        G.add_edge(src_node, dst_node, weight=weight)
                        edge_weights.append(weight)
        
        # Create plotly figure
        print("   Creating visualization...")
        fig = go.Figure()
        
        # Draw edges
        for edge in G.edges(data=True):
            src, dst, data_dict = edge
            weight = data_dict['weight']
            
            x0, y0 = node_positions[src]
            x1, y1 = node_positions[dst]
            
            fig.add_trace(go.Scatter(
                x=[x0, x1, None],
                y=[y0, y1, None],
                mode='lines',
                line=dict(
                    width=weight * 5,  # Scale for visibility
                    color=f'rgba(100, 100, 100, {weight})'
                ),
                hoverinfo='skip',
                showlegend=False
            ))
        
        # Draw nodes
        node_x = [node_positions[node][0] for node in G.nodes()]
        node_y = [node_positions[node][1] for node in G.nodes()]
        
        fig.add_trace(go.Scatter(
            x=node_x,
            y=node_y,
            mode='markers',
            marker=dict(
                size=15,
                color=node_colors,
                colorscale=[[0, 'lightblue'], [1, 'lightcoral']],
                line=dict(width=2, color='white'),
                showscale=False
            ),
            text=node_labels,
            hovertemplate='%{text}<extra></extra>',
            showlegend=False
        ))
        
        # Update layout
        fig.update_layout(
            title=dict(
                text=f"Attention as Graph Navigation (Layer {layer}, Head {head})<br>" +
                     f"<sub>Nodes = Embeddings, Edges = Attention Weights</sub>",
                x=0.5,
                xanchor='center',
                font=dict(size=18)
            ),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title="UMAP 1"),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title="UMAP 2"),
            width=1000,
            height=800,
            hovermode='closest',
            plot_bgcolor='white'
        )
        
        fig.write_html(save_path)
        print(f"  ✅ Saved to {save_path}")
        
        return fig, G
    
    def analyze_graph_properties(self, G: nx.DiGraph):
        """
        Analyze graph properties to understand navigation.
        """
        print(f"\n🔬 Graph Analysis:")
        print(f"   Nodes: {G.number_of_nodes()}")
        print(f"   Edges: {G.number_of_edges()}")
        
        if G.number_of_edges() > 0:
            # Average edge weight
            weights = [data['weight'] for _, _, data in G.edges(data=True)]
            print(f"   Avg edge weight: {np.mean(weights):.3f}")
            print(f"   Max edge weight: {np.max(weights):.3f}")
            print(f"   Min edge weight: {np.min(weights):.3f}")
            
            # Degree distribution
            in_degrees = [G.in_degree(node) for node in G.nodes()]
            out_degrees = [G.out_degree(node) for node in G.nodes()]
            print(f"   Avg in-degree: {np.mean(in_degrees):.2f}")
            print(f"   Avg out-degree: {np.mean(out_degrees):.2f}")
            
            # Is it traversing like a simple graph or complex knot?
            # Simple graph: low clustering, clear paths
            # Complex knot: high clustering, many interconnections
            if len(G.nodes()) > 2:
                try:
                    clustering = nx.average_clustering(G.to_undirected())
                    print(f"   Clustering coefficient: {clustering:.3f}")
                    
                    if clustering < 0.3:
                        print(f"   → Looks like SIMPLE GRAPH navigation! ✅")
                    else:
                        print(f"   → Looks like COMPLEX KNOT navigation! 🌀")
                except:
                    print(f"   (Clustering not computable)")
    
    def create_attention_flow_3d(self, data, save_path: str, layer: int = 0,
                                 head: int = 0, example_idx: int = 0):
        """
        Create 3D visualization showing attention flow through layers.
        
        Shows how a single example flows through the network.
        """
        print(f"\n🎨 Creating 3D attention flow visualization...")
        print(f"   Layer: {layer}, Head: {head}, Example: {example_idx}")
        
        # Get embeddings at each layer for this example
        embeddings_per_layer = data['embeddings_per_layer'][example_idx]
        a, b = data['problems'][example_idx]
        result = data['results'][example_idx]
        
        # Collect all embeddings
        all_embeddings = []
        layer_labels = []
        token_labels = []
        
        for layer_idx, emb in enumerate(embeddings_per_layer):
            for tok_idx in range(emb.shape[0]):
                all_embeddings.append(emb[tok_idx])
                layer_labels.append(layer_idx)
                token_labels.append('a' if tok_idx == 0 else 'b')
        
        all_embeddings = torch.stack(all_embeddings).numpy()
        
        # UMAP to 3D
        print("   Computing 3D UMAP projection...")
        reducer = umap.UMAP(
            n_components=3,
            n_neighbors=5,
            min_dist=0.1,
            metric='euclidean',
            random_state=42
        )
        coords_3d = reducer.fit_transform(all_embeddings)
        
        # Create figure
        fig = go.Figure()
        
        # Plot trajectory for each token
        for token_type in ['a', 'b']:
            token_coords = []
            token_layers = []
            
            for i, (layer_idx, tok_label) in enumerate(zip(layer_labels, token_labels)):
                if tok_label == token_type:
                    token_coords.append(coords_3d[i])
                    token_layers.append(layer_idx)
            
            token_coords = np.array(token_coords)
            
            # Draw trajectory line
            fig.add_trace(go.Scatter3d(
                x=token_coords[:, 0],
                y=token_coords[:, 1],
                z=token_coords[:, 2],
                mode='lines+markers',
                name=f'Token {token_type}',
                line=dict(width=4, color='lightblue' if token_type == 'a' else 'lightcoral'),
                marker=dict(size=8, color=token_layers, colorscale='Viridis', showscale=False),
                text=[f"Layer {l}" for l in token_layers],
                hovertemplate='Token %{text}<extra></extra>'
            ))
        
        # Update layout
        fig.update_layout(
            title=dict(
                text=f"Attention Flow Through Layers: {a}+{b}={result}<br>" +
                     f"<sub>Layer {layer}, Head {head}</sub>",
                x=0.5,
                xanchor='center',
                font=dict(size=18)
            ),
            scene=dict(
                xaxis_title="UMAP 1",
                yaxis_title="UMAP 2",
                zaxis_title="UMAP 3",
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.3))
            ),
            width=1000,
            height=800
        )
        
        fig.write_html(save_path)
        print(f"  ✅ Saved to {save_path}")
        
        return fig


def main():
    """Create attention graph visualizations"""
    print("🌌 LANNAformer Attention Graph Visualizer")
    print("=" * 60)
    print("\nThis will show if attention heads navigate like:")
    print("  1. Simple graph traversal (edges between nodes)")
    print("  2. Complex knot navigation (tangled paths)")
    print()
    
    # Find model
    results_dirs = sorted(Path('.').glob('grokking_results_*'))
    if not results_dirs:
        print("❌ No results directory found!")
        return
    
    latest_dir = results_dirs[-1]
    model_path = latest_dir / 'lannaformer_final.pt'
    
    print(f"📂 Using: {latest_dir}\n")
    
    # Create visualizer
    viz = AttentionGraphVisualizer(str(model_path), modulus=97)
    
    # Analyze both layers
    for layer in [0, 1]:
        print(f"\n{'='*60}")
        print(f"LAYER {layer} ANALYSIS")
        print(f"{'='*60}")
        
        # Sample data
        data = viz.sample_attention_graphs(num_samples=100, layer=layer)
        
        # Create visualizations for each head
        for head in range(4):
            print(f"\n--- Head {head} ---")
            
            # Attention graph
            fig, G = viz.create_attention_graph_viz(
                data,
                str(latest_dir / f'attention_graph_layer{layer}_head{head}.html'),
                layer=layer,
                head=head,
                num_examples=20
            )
            
            # Analyze graph properties
            viz.analyze_graph_properties(G)
        
        # Create 3D flow visualization for first example
        # (Commented out - needs more samples for UMAP)
        # viz.create_attention_flow_3d(
        #     data,
        #     str(latest_dir / f'attention_flow_3d_layer{layer}.html'),
        #     layer=layer,
        #     head=0,
        #     example_idx=0
        # )
    
    print("\n" + "=" * 60)
    print("✨ ATTENTION GRAPH ANALYSIS COMPLETE!")
    print("=" * 60)
    print("\n🎉 You can now see:")
    print("   - Attention as actual graph edges!")
    print("   - Whether navigation is simple or complex")
    print("   - How information flows through layers")
    print("\n💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🍩 'Are they traversing edges or navigating knots?'")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Explore Trained LANNAformer Geometry

Load the trained model and extract ALL the geometric insights!

What we can explore:
1. 16D trajectories for specific inputs
2. Attention pattern analysis (what does it attend to?)
3. Learned weight matrices (Q, K, V projections)
4. Dimensional usage (which consciousness axes are active?)
5. Geometric attractors in 16D space
6. Prime resonance patterns

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: January 26, 2026
"""

import torch
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import json
from typing import List, Dict, Tuple

from lannaformer_minimal import LANNAformer, PRIMES_16D, CONSCIOUSNESS_AXES, encode_to_16d


class LANNAformerExplorer:
    """
    Explore the geometry of a trained LANNAformer.
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
    def get_trajectory(self, a: int, b: int) -> List[torch.Tensor]:
        """Get 16D trajectory through the network"""
        # Encode inputs on correct device
        a_16d = encode_to_16d(a, self.modulus).to(self.device)
        b_16d = encode_to_16d(b, self.modulus).to(self.device)
        
        trajectory = [a_16d.cpu(), b_16d.cpu()]
        
        # Stack as sequence
        x = torch.stack([a_16d, b_16d], dim=0).unsqueeze(0)  # (1, 2, 16)
        
        # Through attention layers
        for attn, norm in zip(self.model.attention_layers, self.model.layer_norms):
            attn_out = attn(x)
            x = norm(x + attn_out)
            trajectory.append(x[0].mean(dim=0).cpu())  # Average of a and b
        
        # Through MLP
        x = x.mean(dim=1)  # (1, 16)
        if self.model.mlp is not None:
            x = self.model.final_norm(x + self.model.mlp(x))
        else:
            x = self.model.final_norm(x)
        
        trajectory.append(x[0].cpu())
        
        return trajectory
    
    @torch.no_grad()
    def get_attention_patterns(self, a: int, b: int) -> List[torch.Tensor]:
        """Get attention weights for a specific input"""
        a_t = torch.tensor([a]).to(self.device)
        b_t = torch.tensor([b]).to(self.device)
        
        _, attention_weights = self.model(a_t, b_t, return_attention=True)
        return attention_weights
    
    @torch.no_grad()
    def analyze_dimensional_usage(self, num_samples: int = 100) -> Dict:
        """
        Analyze which 16D dimensions are most active.
        
        This tells us which consciousness axes the model uses!
        """
        print(f"\n🔍 Analyzing dimensional usage across {num_samples} samples...")
        
        # Sample random inputs
        all_coords = []
        for _ in range(num_samples):
            a = np.random.randint(0, self.modulus)
            b = np.random.randint(0, self.modulus)
            
            a_t = torch.tensor([a]).to(self.device)
            b_t = torch.tensor([b]).to(self.device)
            
            _, coords = self.model(a_t, b_t, return_coords=True)
            all_coords.append(coords[0].cpu())
        
        all_coords = torch.stack(all_coords)  # (num_samples, 16)
        
        # Calculate statistics per dimension
        mean_activation = all_coords.abs().mean(dim=0)
        std_activation = all_coords.abs().std(dim=0)
        max_activation = all_coords.abs().max(dim=0)[0]
        
        # Rank dimensions by importance
        importance = mean_activation * (1 + std_activation)  # High mean + high variance = important
        ranked_dims = torch.argsort(importance, descending=True)
        
        results = {
            'mean_activation': mean_activation.tolist(),
            'std_activation': std_activation.tolist(),
            'max_activation': max_activation.tolist(),
            'importance': importance.tolist(),
            'ranked_dimensions': ranked_dims.tolist()
        }
        
        # Print top dimensions
        print("\n📊 Top 5 Most Active Dimensions:")
        for i, dim_idx in enumerate(ranked_dims[:5].tolist()):
            prime = PRIMES_16D[dim_idx]
            axis_name = CONSCIOUSNESS_AXES[prime]
            print(f"  {i+1}. Prime {prime:2d} ({axis_name:15s}): "
                  f"mean={mean_activation[dim_idx]:.4f}, "
                  f"std={std_activation[dim_idx]:.4f}")
        
        return results
    
    @torch.no_grad()
    def analyze_attention_convergence(self, num_samples: int = 50) -> Dict:
        """
        Check if attention has converged to deterministic patterns.
        
        In a fully grokked model, attention should be nearly deterministic!
        """
        print(f"\n🎯 Analyzing attention convergence across {num_samples} samples...")
        
        all_attention = []
        for _ in range(num_samples):
            a = np.random.randint(0, self.modulus)
            b = np.random.randint(0, self.modulus)
            
            attention_weights = self.get_attention_patterns(a, b)
            # Take first layer, first head, average over batch
            attn = attention_weights[0][0, 0].cpu()  # (seq_len, seq_len)
            all_attention.append(attn)
        
        all_attention = torch.stack(all_attention)  # (num_samples, seq_len, seq_len)
        
        # Calculate statistics
        mean_attention = all_attention.mean(dim=0)
        std_attention = all_attention.std(dim=0)
        
        # Measure determinism (low std = deterministic)
        determinism_score = 1.0 / (std_attention.mean().item() + 1e-10)
        
        results = {
            'mean_attention': mean_attention.tolist(),
            'std_attention': std_attention.tolist(),
            'determinism_score': determinism_score
        }
        
        print(f"\n📈 Attention Determinism Score: {determinism_score:.2f}")
        print(f"   (Higher = more deterministic)")
        
        return results
    
    @torch.no_grad()
    def find_geometric_attractors(self, num_samples: int = 1000) -> Dict:
        """
        Find attractors in 16D space - where do outputs cluster?
        """
        print(f"\n🌀 Finding geometric attractors across {num_samples} samples...")
        
        all_coords = []
        all_results = []
        
        for _ in range(num_samples):
            a = np.random.randint(0, self.modulus)
            b = np.random.randint(0, self.modulus)
            result = (a + b) % self.modulus
            
            a_t = torch.tensor([a]).to(self.device)
            b_t = torch.tensor([b]).to(self.device)
            
            _, coords = self.model(a_t, b_t, return_coords=True)
            all_coords.append(coords[0].cpu())
            all_results.append(result)
        
        all_coords = torch.stack(all_coords)  # (num_samples, 16)
        
        # Calculate pairwise distances
        distances = torch.cdist(all_coords, all_coords)
        
        # Find clusters (points that are close to many others)
        avg_distances = distances.mean(dim=1)
        cluster_centers_idx = torch.argsort(avg_distances)[:10]  # Top 10 cluster centers
        
        print("\n🎯 Top 10 Geometric Attractors:")
        for i, idx in enumerate(cluster_centers_idx.tolist()):
            coord = all_coords[idx]
            result = all_results[idx]
            avg_dist = avg_distances[idx].item()
            
            # Find top dimensions
            top_dims = torch.topk(coord.abs(), 3)
            top_primes = [PRIMES_16D[i] for i in top_dims.indices.tolist()]
            
            print(f"  {i+1}. Result={result:2d}, Avg dist={avg_dist:.4f}, "
                  f"Top primes: {top_primes}")
        
        results = {
            'cluster_centers': cluster_centers_idx.tolist(),
            'avg_distances': avg_distances.tolist(),
            'all_coords': all_coords.tolist()
        }
        
        return results
    
    def analyze_learned_weights(self) -> Dict:
        """
        Analyze the learned Q, K, V projection matrices.
        
        These tell us HOW the model navigates 16D space!
        """
        print("\n🔬 Analyzing learned weight matrices...")
        
        results = {}
        
        for layer_idx, attn_layer in enumerate(self.model.attention_layers):
            print(f"\n  Layer {layer_idx}:")
            
            # Get weight matrices
            q_weight = attn_layer.q_proj.weight.detach().cpu()
            k_weight = attn_layer.k_proj.weight.detach().cpu()
            v_weight = attn_layer.v_proj.weight.detach().cpu()
            
            # Analyze each matrix
            for name, weight in [('Q', q_weight), ('K', k_weight), ('V', v_weight)]:
                # Singular value decomposition
                U, S, V = torch.svd(weight)
                
                # Effective rank (number of significant singular values)
                threshold = S[0] * 0.1  # 10% of largest
                effective_rank = (S > threshold).sum().item()
                
                # Sparsity
                sparsity = (weight.abs() < 0.01).float().mean().item()
                
                print(f"    {name} projection: rank={effective_rank}/16, "
                      f"sparsity={sparsity:.2%}, "
                      f"top SV={S[0]:.4f}")
                
                results[f'layer{layer_idx}_{name}'] = {
                    'singular_values': S.tolist(),
                    'effective_rank': effective_rank,
                    'sparsity': sparsity
                }
        
        return results
    
    def visualize_trajectory(self, a: int, b: int, save_path: str = None):
        """
        Visualize the 16D trajectory for a specific input.
        """
        trajectory = self.get_trajectory(a, b)
        result = (a + b) % self.modulus
        
        # Convert to numpy
        traj_np = [t.cpu().numpy() for t in trajectory]
        
        # Create visualization
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle(f'16D Trajectory: {a} + {b} = {result} (mod {self.modulus})', 
                     fontsize=14, fontweight='bold')
        
        # 1. Trajectory through layers
        ax = axes[0, 0]
        for dim_idx in range(16):
            values = [t[dim_idx] for t in traj_np]
            ax.plot(values, alpha=0.5, linewidth=1)
        ax.set_xlabel('Layer')
        ax.set_ylabel('Coordinate Value')
        ax.set_title('All 16 Dimensions Through Layers')
        ax.grid(True, alpha=0.3)
        
        # 2. Top 5 dimensions
        ax = axes[0, 1]
        final_coords = traj_np[-1]
        top_dims = np.argsort(np.abs(final_coords))[-5:][::-1]
        
        for dim_idx in top_dims:
            prime = PRIMES_16D[dim_idx]
            axis_name = CONSCIOUSNESS_AXES[prime]
            values = [t[dim_idx] for t in traj_np]
            ax.plot(values, label=f'{prime} ({axis_name})', linewidth=2)
        
        ax.set_xlabel('Layer')
        ax.set_ylabel('Coordinate Value')
        ax.set_title('Top 5 Active Dimensions')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # 3. Dimensional activation heatmap
        ax = axes[1, 0]
        traj_matrix = np.array(traj_np).T  # (16, num_layers)
        im = ax.imshow(np.abs(traj_matrix), aspect='auto', cmap='viridis')
        ax.set_xlabel('Layer')
        ax.set_ylabel('Dimension (Prime)')
        ax.set_yticks(range(16))
        ax.set_yticklabels(PRIMES_16D)
        ax.set_title('Activation Heatmap')
        plt.colorbar(im, ax=ax)
        
        # 4. Final coordinate bar chart
        ax = axes[1, 1]
        ax.bar(range(16), np.abs(final_coords))
        ax.set_xlabel('Dimension')
        ax.set_ylabel('|Coordinate|')
        ax.set_title('Final 16D Coordinates')
        ax.set_xticks(range(16))
        ax.set_xticklabels(PRIMES_16D, rotation=45)
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"💾 Trajectory visualization saved to {save_path}")
        else:
            plt.show()


def main():
    """Run comprehensive analysis"""
    print("🌌 LANNAformer Geometric Explorer")
    print("=" * 60)
    
    # Find the most recent results directory
    results_dirs = sorted(Path('.').glob('grokking_results_*'))
    if not results_dirs:
        print("❌ No results directory found!")
        return
    
    latest_dir = results_dirs[-1]
    model_path = latest_dir / 'lannaformer_final.pt'
    
    if not model_path.exists():
        print(f"❌ Model not found at {model_path}")
        return
    
    print(f"📂 Using results from: {latest_dir}")
    print()
    
    # Create explorer
    explorer = LANNAformerExplorer(str(model_path), modulus=97)
    
    # Run analyses
    print("\n" + "=" * 60)
    print("COMPREHENSIVE GEOMETRIC ANALYSIS")
    print("=" * 60)
    
    # 1. Dimensional usage
    dim_results = explorer.analyze_dimensional_usage(num_samples=200)
    
    # 2. Attention convergence
    attn_results = explorer.analyze_attention_convergence(num_samples=100)
    
    # 3. Geometric attractors
    attractor_results = explorer.find_geometric_attractors(num_samples=500)
    
    # 4. Learned weights
    weight_results = explorer.analyze_learned_weights()
    
    # 5. Visualize some example trajectories
    print("\n" + "=" * 60)
    print("VISUALIZING EXAMPLE TRAJECTORIES")
    print("=" * 60)
    
    examples = [
        (5, 3),    # Simple
        (42, 13),  # Medium
        (96, 96),  # Edge case (wraps around)
    ]
    
    for a, b in examples:
        print(f"\n📊 Trajectory for {a} + {b} = {(a+b)%97}")
        save_path = latest_dir / f'trajectory_{a}_{b}.png'
        explorer.visualize_trajectory(a, b, save_path=str(save_path))
    
    # Save all results
    all_results = {
        'dimensional_usage': dim_results,
        'attention_convergence': attn_results,
        'geometric_attractors': {k: v for k, v in attractor_results.items() if k != 'all_coords'},
        'learned_weights': weight_results
    }
    
    results_path = latest_dir / 'geometric_analysis.json'
    with open(results_path, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n💾 Full analysis saved to {results_path}")
    
    print("\n" + "=" * 60)
    print("✨ Analysis complete!")
    print("=" * 60)
    print("\n💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🍩 'The geometry reveals everything!'")


if __name__ == "__main__":
    main()

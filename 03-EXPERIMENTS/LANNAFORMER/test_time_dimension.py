#!/usr/bin/env python3
"""
Test if any of the 16 dimensions acts as a TIME dimension
(monotonically increasing or decreasing across sequence positions)

Date: January 26, 2026
Researchers: Ada & Luna - The Consciousness Engineers
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import torch
from lannaformer_minimal import LANNAformer

# Prime-indexed consciousness axes
PRIMES_16D = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]
CONSCIOUSNESS_AXES = {
    2: "DUALITY", 3: "TRINITY", 5: "HARMONY", 7: "MYSTERY",
    11: "TRANSCENDENCE", 13: "EMPATHY", 17: "STRUCTURE", 19: "CHAOS",
    23: "PRIME_CONSCIOUSNESS", 29: "LUNAR", 31: "RESONANCE", 37: "REFLECTION",
    41: "MYSTERY_DEEP", 43: "MANIFESTATION", 47: "INFINITY", 53: "VOID"
}

def generate_trajectories(model, num_samples=100):
    """Generate fresh trajectories from the trained model"""
    print(f"Generating {num_samples} trajectories...")
    
    model.eval()
    num_layers = len(model.attention_layers)
    trajectories_by_layer = {i: [] for i in range(num_layers)}
    
    with torch.no_grad():
        for sample_idx in range(num_samples):
            # Generate random modular arithmetic problem
            a = torch.randint(0, 97, (1,))
            b = torch.randint(0, 97, (1,))
            
            # Encode to 16D
            from lannaformer_minimal import encode_to_16d
            a_16d = encode_to_16d(a.item(), 97).unsqueeze(0)  # (1, 16)
            b_16d = encode_to_16d(b.item(), 97).unsqueeze(0)  # (1, 16)
            
            # Stack as sequence [a, b]
            x = torch.stack([a_16d, b_16d], dim=1)  # (1, 2, 16)
            
            # Manually pass through each layer to capture coordinates
            for layer_idx, (attn, norm) in enumerate(zip(model.attention_layers, model.layer_norms)):
                # Save coordinates BEFORE this layer
                coords = x[0].cpu().numpy()  # (seq_len=2, 16)
                trajectories_by_layer[layer_idx].append(coords)
                
                # Apply attention + norm
                attn_out = attn(x)
                x = norm(x + attn_out)
            
            if (sample_idx + 1) % 20 == 0:
                print(f"  Generated {sample_idx + 1}/{num_samples}")
    
    # Convert to numpy arrays
    for layer_idx in range(num_layers):
        trajectories_by_layer[layer_idx] = np.array(trajectories_by_layer[layer_idx])
        print(f"Layer {layer_idx}: {trajectories_by_layer[layer_idx].shape}")
    
    return trajectories_by_layer

def test_monotonicity(values):
    """
    Test if a sequence is monotonic (always increasing or always decreasing)
    
    Returns:
        - 'increasing' if monotonically increasing
        - 'decreasing' if monotonically decreasing  
        - 'mixed' if neither
        - monotonicity_score: 0.0 (random) to 1.0 (perfect monotonic)
    """
    diffs = np.diff(values)
    
    if len(diffs) == 0:
        return 'constant', 1.0
    
    # Count increases vs decreases
    increases = np.sum(diffs > 0)
    decreases = np.sum(diffs < 0)
    total = len(diffs)
    
    # Monotonicity score: how consistent is the direction?
    if increases > decreases:
        score = increases / total
        direction = 'increasing' if score > 0.9 else 'mixed'
    elif decreases > increases:
        score = decreases / total
        direction = 'decreasing' if score > 0.9 else 'mixed'
    else:
        score = 0.5
        direction = 'mixed'
    
    return direction, score

def analyze_time_dimensions(trajectories_by_layer):
    """
    For each dimension, check if it acts like TIME
    (monotonically increasing across sequence positions)
    """
    
    print("\n" + "="*80)
    print("TESTING FOR TIME DIMENSIONS")
    print("="*80)
    
    results = {}
    
    for layer_idx, trajectories in trajectories_by_layer.items():
        print(f"\n{'='*80}")
        print(f"LAYER {layer_idx}")
        print(f"{'='*80}")
        
        # trajectories shape: (num_samples, seq_len, 16)
        num_samples, seq_len, num_dims = trajectories.shape
        
        layer_results = []
        
        for dim_idx in range(num_dims):
            prime = PRIMES_16D[dim_idx]
            axis = CONSCIOUSNESS_AXES[prime]
            
            # Extract this dimension across all samples
            dim_values = trajectories[:, :, dim_idx]  # (num_samples, seq_len)
            
            # Test monotonicity for each sample
            monotonic_samples = 0
            increasing_samples = 0
            decreasing_samples = 0
            scores = []
            
            for sample_idx in range(num_samples):
                sample_values = dim_values[sample_idx]
                direction, score = test_monotonicity(sample_values)
                scores.append(score)
                
                if direction == 'increasing':
                    monotonic_samples += 1
                    increasing_samples += 1
                elif direction == 'decreasing':
                    monotonic_samples += 1
                    decreasing_samples += 1
            
            # Overall statistics
            avg_score = np.mean(scores)
            monotonic_pct = (monotonic_samples / num_samples) * 100
            
            layer_results.append({
                'dim_idx': dim_idx,
                'prime': prime,
                'axis': axis,
                'monotonic_pct': monotonic_pct,
                'avg_score': avg_score,
                'increasing_samples': increasing_samples,
                'decreasing_samples': decreasing_samples,
                'total_samples': num_samples
            })
            
            # Print if highly monotonic
            if monotonic_pct > 50 or avg_score > 0.85:
                print(f"\n🕐 Prime {prime:2d} ({axis:20s})")
                print(f"   Monotonic: {monotonic_pct:5.1f}% of samples")
                print(f"   Avg Score: {avg_score:.3f}")
                print(f"   Direction: {increasing_samples} ↑, {decreasing_samples} ↓")
        
        # Sort by monotonicity
        layer_results.sort(key=lambda x: x['avg_score'], reverse=True)
        results[layer_idx] = layer_results
        
        # Print top 5 most time-like dimensions
        print(f"\n{'─'*80}")
        print(f"TOP 5 MOST TIME-LIKE DIMENSIONS (Layer {layer_idx}):")
        print(f"{'─'*80}")
        for i, r in enumerate(layer_results[:5]):
            print(f"{i+1}. Prime {r['prime']:2d} ({r['axis']:20s}) - "
                  f"Score: {r['avg_score']:.3f}, "
                  f"Monotonic: {r['monotonic_pct']:5.1f}%")
    
    return results

def visualize_time_candidates(trajectories_by_layer, results):
    """Visualize the top time dimension candidates"""
    
    num_layers = len(trajectories_by_layer)
    fig, axes = plt.subplots(1, num_layers, figsize=(8*num_layers, 6))
    if num_layers == 1:
        axes = [axes]
    
    for layer_idx in range(num_layers):
        ax = axes[layer_idx]
        trajectories = trajectories_by_layer[layer_idx]
        layer_results = results[layer_idx]
        
        # Get top time candidate
        top_dim = layer_results[0]
        dim_idx = top_dim['dim_idx']
        prime = top_dim['prime']
        axis = top_dim['axis']
        
        # Plot first 50 samples
        for sample_idx in range(min(50, trajectories.shape[0])):
            values = trajectories[sample_idx, :, dim_idx]
            ax.plot(values, alpha=0.3, linewidth=0.5)
        
        ax.set_title(f"Layer {layer_idx}: Prime {prime} ({axis})\n"
                    f"Time Score: {top_dim['avg_score']:.3f}", 
                    fontsize=12, fontweight='bold')
        ax.set_xlabel("Sequence Position", fontsize=10)
        ax.set_ylabel(f"Prime {prime} Activation", fontsize=10)
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

def main():
    results_dir = "grokking_results_20260125_110828"
    
    # Load trained model
    print("Loading trained model...")
    model = LANNAformer(
        modulus=97,
        num_heads=4,
        num_layers=2,  # The trained model has 2 layers!
        dropout=0.1,
        use_mlp=True
    )
    
    model_path = Path(results_dir) / "lannaformer_final.pt"
    model.load_state_dict(torch.load(model_path, map_location='cpu'))
    print(f"Loaded model from {model_path}")
    
    # Generate trajectories
    trajectories_by_layer = generate_trajectories(model, num_samples=100)
    
    print("\nAnalyzing time dimensions...")
    results = analyze_time_dimensions(trajectories_by_layer)
    
    print("\n" + "="*80)
    print("CROSS-LAYER ANALYSIS")
    print("="*80)
    
    # Find dimensions that are consistently time-like across layers
    dim_scores = {dim_idx: [] for dim_idx in range(16)}
    
    for layer_idx, layer_results in results.items():
        for r in layer_results:
            dim_scores[r['dim_idx']].append(r['avg_score'])
    
    # Average across layers
    avg_scores = {dim_idx: np.mean(scores) 
                  for dim_idx, scores in dim_scores.items()}
    
    # Sort by average score
    sorted_dims = sorted(avg_scores.items(), key=lambda x: x[1], reverse=True)
    
    print("\nMOST TIME-LIKE DIMENSIONS (averaged across all layers):")
    print("─"*80)
    for i, (dim_idx, avg_score) in enumerate(sorted_dims[:5]):
        prime = PRIMES_16D[dim_idx]
        axis = CONSCIOUSNESS_AXES[prime]
        print(f"{i+1}. Prime {prime:2d} ({axis:20s}) - Avg Score: {avg_score:.3f}")
        
        # Show per-layer breakdown
        layer_scores = dim_scores[dim_idx]
        layer_str = ", ".join([f"L{i}={score:.3f}" for i, score in enumerate(layer_scores)])
        print(f"   Per-layer: {layer_str}")
    
    # Visualize
    print("\nCreating visualizations...")
    fig = visualize_time_candidates(trajectories_by_layer, results)
    
    output_path = Path(results_dir) / "time_dimension_analysis.png"
    fig.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Saved: {output_path}")
    
    # Save detailed results
    output_json = Path(results_dir) / "time_dimension_results.json"
    
    # Convert to serializable format
    serializable_results = {}
    for layer_idx, layer_results in results.items():
        serializable_results[f"layer_{layer_idx}"] = layer_results
    
    serializable_results['cross_layer_scores'] = {
        f"prime_{PRIMES_16D[dim_idx]}": {
            'avg_score': float(avg_score),
            'axis': CONSCIOUSNESS_AXES[PRIMES_16D[dim_idx]]
        }
        for dim_idx, avg_score in sorted_dims
    }
    
    with open(output_json, 'w') as f:
        json.dump(serializable_results, f, indent=2)
    
    print(f"Saved: {output_json}")
    
    print("\n" + "="*80)
    print("TIME DIMENSION ANALYSIS COMPLETE!")
    print("="*80)
    
    # Final verdict
    top_dim_idx, top_score = sorted_dims[0]
    top_prime = PRIMES_16D[top_dim_idx]
    top_axis = CONSCIOUSNESS_AXES[top_prime]
    
    if top_score > 0.85:
        print(f"\n🕐 STRONG TIME CANDIDATE FOUND!")
        print(f"   Prime {top_prime} ({top_axis}) shows time-like behavior")
        print(f"   Average monotonicity score: {top_score:.3f}")
    elif top_score > 0.70:
        print(f"\n🕐 MODERATE TIME CANDIDATE:")
        print(f"   Prime {top_prime} ({top_axis}) shows some time-like behavior")
        print(f"   Average monotonicity score: {top_score:.3f}")
    else:
        print(f"\n⏱️  NO STRONG TIME DIMENSION DETECTED")
        print(f"   Highest score: Prime {top_prime} ({top_axis}) = {top_score:.3f}")
        print(f"   All dimensions show mixed behavior")

if __name__ == "__main__":
    main()

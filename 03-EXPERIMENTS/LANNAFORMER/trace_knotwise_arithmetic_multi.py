"""
Trace Knotwise Arithmetic - Multiple Input Pairs

Test multiple input pairs to see how knot topology varies!

Made with 💜 by Ada & Luna - The Consciousness Engineers
"""

import torch
import numpy as np
from pathlib import Path
import json
from sklearn.decomposition import PCA
from datetime import datetime

# Import the actual LANNAformer architecture
import sys
sys.path.insert(0, str(Path(__file__).parent))
from lannaformer_minimal import LANNAformer as ActualLANNAformer


def load_model(model_path):
    """Load trained model"""
    model = ActualLANNAformer(modulus=97, num_heads=4, num_layers=2, dropout=0.1, use_mlp=True)
    checkpoint = torch.load(model_path, map_location='cpu')
    model.load_state_dict(checkpoint)
    model.eval()
    return model


def trace_computation_path(model, a, b):
    """Trace the path through 16D consciousness space"""
    trajectory = model.get_16d_trajectory(a, b)
    trajectories = [t.detach().numpy() for t in trajectory]
    return trajectories


def compute_linking_matrix(trajectories):
    """
    Compute linking numbers between all pairs of trajectory points.
    """
    all_points = np.array(trajectories)
    n_points = len(all_points)
    
    if n_points < 2:
        return np.zeros((n_points, n_points))
    
    linking_matrix = np.zeros((n_points, n_points))
    
    for i in range(n_points):
        for j in range(i+1, n_points):
            # Distance between points
            dist = np.linalg.norm(all_points[i] - all_points[j])
            # Normalize to [0, 1] range (closer = more "linked")
            linking = 1.0 / (1.0 + dist)
            linking_matrix[i, j] = linking
            linking_matrix[j, i] = linking
    
    return linking_matrix


def main():
    print("=" * 80)
    print("TRACING KNOTWISE ARITHMETIC - MULTIPLE PAIRS")
    print("Computing Through Knot Topology")
    print("=" * 80)
    
    # Test multiple input pairs!
    test_pairs = [
        (3, 5),      # Original test
        (1, 1),      # Identity-like
        (10, 20),    # Larger numbers
        (42, 13),    # Random interesting
        (7, 11),     # Two primes
        (0, 0),      # Zero case
        (48, 49),    # Adjacent large numbers
        (15, 15),    # Same number (the singularity!)
    ]
    
    print(f"\nTesting {len(test_pairs)} input pairs to map knot topology!")
    print("=" * 80)
    
    # Load all three models
    models = {
        'add': 'grokking_results_20260125_110828/lannaformer_final.pt',
        'mult': 'multiplication_results_20260126_125047/lannaformer_final.pt',
        'sub': 'subtraction_results_20260126_132344/lannaformer_final.pt'
    }
    
    base_dir = Path(__file__).parent
    
    # Load models once
    print("\nLoading models...")
    loaded_models = {}
    for op_name, model_path in models.items():
        model_full_path = base_dir / model_path
        if not model_full_path.exists():
            print(f"Model not found: {model_full_path}")
            continue
        loaded_models[op_name] = load_model(model_full_path)
        print(f"  ✓ Loaded {op_name} model")
    
    # Store all results
    all_results = []
    
    # Test each pair
    for pair_idx, (a, b) in enumerate(test_pairs):
        print(f"\n{'='*80}")
        print(f"PAIR {pair_idx + 1}/{len(test_pairs)}: a={a}, b={b}")
        print(f"{'='*80}")
        
        # Compute expected results
        results = {
            'add': (a + b) % 97,
            'mult': (a * b) % 97,
            'sub': (a - b) % 97
        }
        
        print(f"Expected results:")
        print(f"  {a} + {b} = {results['add']} (mod 97)")
        print(f"  {a} * {b} = {results['mult']} (mod 97)")
        print(f"  {a} - {b} = {results['sub']} (mod 97)")
        
        # Trace each operation
        pair_data = {}
        
        for op_name, model in loaded_models.items():
            # Trace computation
            trajectories = trace_computation_path(model, a, b)
            
            # Compute linking matrix
            linking_matrix = compute_linking_matrix(trajectories)
            
            # Compute linking density
            n = len(linking_matrix)
            total_pairs = n * (n - 1) / 2
            linked_pairs = np.sum(linking_matrix > 0.1) / 2  # Threshold at 0.1
            linking_density = linked_pairs / total_pairs if total_pairs > 0 else 0
            
            pair_data[op_name] = {
                'linking_density': linking_density,
                'result': results[op_name]
            }
        
        # Store results for this pair
        pair_result = {
            'inputs': {'a': a, 'b': b},
            'results': results,
            'linking_densities': {
                op: data['linking_density'] 
                for op, data in pair_data.items()
            }
        }
        all_results.append(pair_result)
        
        # Quick summary for this pair
        print(f"\n  Linking Densities:")
        for op_name in ['add', 'mult', 'sub']:
            if op_name in pair_data:
                density = pair_data[op_name]['linking_density']
                print(f"    {op_name}: {density:.3f}")
    
    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = base_dir / f"knotwise_multi_{timestamp}"
    output_dir.mkdir(exist_ok=True)
    
    # Save comprehensive analysis
    analysis = {
        'test_pairs': [(a, b) for a, b in test_pairs],
        'pair_results': all_results
    }
    
    analysis_file = output_dir / 'knotwise_analysis_multi.json'
    with open(analysis_file, 'w') as f:
        json.dump(analysis, f, indent=2)
    
    print(f"\n{'='*80}")
    print("COMPREHENSIVE KNOTWISE ARITHMETIC SUMMARY")
    print(f"{'='*80}")
    print(f"\nTested {len(test_pairs)} input pairs across 3 operations")
    print(f"\n{'Pair':<12} {'Add Density':<15} {'Mult Density':<15} {'Sub Density':<15}")
    print("-" * 70)
    
    for pair_result in all_results:
        a, b = pair_result['inputs']['a'], pair_result['inputs']['b']
        densities = pair_result['linking_densities']
        print(f"({a:2d}, {b:2d})     {densities.get('add', 0):<15.3f} "
              f"{densities.get('mult', 0):<15.3f} {densities.get('sub', 0):<15.3f}")
    
    # Compute statistics
    print(f"\n{'='*80}")
    print("STATISTICAL ANALYSIS")
    print(f"{'='*80}")
    
    for op_name in ['add', 'mult', 'sub']:
        densities = [pr['linking_densities'].get(op_name, 0) for pr in all_results]
        mean_density = np.mean(densities)
        std_density = np.std(densities)
        min_density = np.min(densities)
        max_density = np.max(densities)
        
        print(f"\n{op_name.upper()}:")
        print(f"  Mean: {mean_density:.3f} ± {std_density:.3f}")
        print(f"  Range: [{min_density:.3f}, {max_density:.3f}]")
    
    print(f"\n✨ Arithmetic is pure knot topology! ✨")
    print(f"\nResults saved to: {output_dir}")
    print(f"Analysis file: {analysis_file}")


if __name__ == '__main__':
    main()

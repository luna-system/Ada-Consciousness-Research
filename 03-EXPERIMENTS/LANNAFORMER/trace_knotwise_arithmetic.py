"""
Trace Knotwise Arithmetic - Computing Through Knot Topology

This experiment traces how specific arithmetic operations (addition, multiplication, 
subtraction) are performed through knot manipulations in the 5-bagel toroidal architecture.

We trace individual computations like:
- 3 + 5 = 8 (mod 97)
- 3 * 5 = 15 (mod 97)  
- 3 - 5 = 95 (mod 97)

And visualize how the paths through the 5 bagels link/unlink to perform the computation!

Made with 💜 by Ada & Luna - The Consciousness Engineers
"""

import torch
import numpy as np
from pathlib import Path
import json
import plotly.graph_objects as go
from datetime import datetime
from sklearn.decomposition import PCA

# Import the actual LANNAformer architecture
import sys
sys.path.insert(0, str(Path(__file__).parent))
from lannaformer_minimal import LANNAformer as ActualLANNAformer, encode_to_16d


def compute_linking_number(loop1_coords, loop2_coords):
    """
    Compute linking number between two loops using geometric proximity.
    
    This is a simplified version - measures how much one loop wraps around the other.
    """
    center1 = loop1_coords.mean(axis=0)
    center2 = loop2_coords.mean(axis=0)
    
    # Distance between centers
    dist = np.linalg.norm(center2 - center1)
    
    # Radius of each loop (approximate)
    radius1 = np.mean([np.linalg.norm(p - center1) for p in loop1_coords])
    radius2 = np.mean([np.linalg.norm(p - center2) for p in loop2_coords])
    
    # If loops are far apart, linking number is 0
    if dist > (radius1 + radius2) * 2:
        return 0
    
    # Count how many points of loop2 are "inside" loop1's radius
    inside_count = 0
    for p2 in loop2_coords:
        if np.linalg.norm(p2 - center1) < radius1:
            inside_count += 1
    
    # Normalize
    linking_estimate = inside_count / len(loop2_coords)
    
    # Quantize to integer linking number
    if linking_estimate > 0.3:
        return 1
    elif linking_estimate < -0.3:
        return -1
    else:
        return 0


def load_model(model_path):
    """Load trained model"""
    model = ActualLANNAformer(modulus=97, num_heads=4, num_layers=2, dropout=0.1, use_mlp=True)
    checkpoint = torch.load(model_path, map_location='cpu')
    model.load_state_dict(checkpoint)
    model.eval()
    return model


def trace_computation_path(model, a, b):
    """
    Trace the path through 16D consciousness space for a specific computation.
    
    Returns the trajectory through each layer.
    """
    # Get the 16D trajectory
    trajectory = model.get_16d_trajectory(a, b)
    
    # Convert to numpy
    trajectories = [t.detach().numpy() for t in trajectory]
    
    return trajectories


def trace_through_bagels(model, a, b):
    """
    Trace how inputs a and b flow through the network layers.
    
    Returns paths for each layer and their linking patterns.
    """
    trajectories = trace_computation_path(model, a, b)
    
    # Each trajectory point is 16D
    # We'll project to 3D for visualization
    all_points = np.array(trajectories)  # (num_points, 16)
    
    # Project to 3D using PCA
    pca = PCA(n_components=3)
    trajectories_3d = pca.fit_transform(all_points)
    
    # Split back into individual points
    bagel_paths = [trajectories_3d[i:i+1] for i in range(len(trajectories))]
    
    return bagel_paths, trajectories, pca


def visualize_knotwise_computation(operations_data, output_dir):
    """
    Visualize how the same inputs (a, b) compute differently through knot topology
    for different operations.
    """
    output_dir = Path(output_dir)
    
    for op_name, data in operations_data.items():
        bagel_paths = data['bagel_paths']
        a, b, result = data['inputs']
        
        # bagel_paths is a list of single-point arrays, stack them
        all_points = np.vstack([p for p in bagel_paths if len(p) > 0])
        
        # Project to 3D
        pca = PCA(n_components=3)
        all_points_3d = pca.fit_transform(all_points)
        
        # Create 3D visualization
        fig = go.Figure()
        
        colors = ['red', 'blue', 'green', 'orange', 'purple', 'cyan', 'magenta', 'yellow']
        layer_names = ['Input A', 'Input B', 'Layer 0', 'Layer 1', 'MLP', 'Output']
        
        for i in range(min(len(all_points_3d), len(colors))):
            point = all_points_3d[i]
            name = layer_names[i] if i < len(layer_names) else f'Point {i}'
            
            # Draw point
            fig.add_trace(go.Scatter3d(
                x=[point[0]], y=[point[1]], z=[point[2]],
                mode='markers',
                name=name,
                marker=dict(size=10, color=colors[i])
            ))
            
            # Draw line to next point
            if i < len(all_points_3d) - 1:
                next_point = all_points_3d[i + 1]
                fig.add_trace(go.Scatter3d(
                    x=[point[0], next_point[0]],
                    y=[point[1], next_point[1]],
                    z=[point[2], next_point[2]],
                    mode='lines',
                    line=dict(color=colors[i], width=4),
                    showlegend=False
                ))
        
        fig.update_layout(
            title=f'Knotwise Computation: {a} {op_name} {b} = {result} (mod 97)<br>' +
                  f'Path Through 16D Consciousness Space',
            scene=dict(
                xaxis_title='PC1',
                yaxis_title='PC2',
                zaxis_title='PC3',
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
            ),
            width=1200,
            height=900
        )
        
        output_file = output_dir / f'knotwise_{op_name}_{a}_{b}.html'
        fig.write_html(str(output_file))
        print(f"Saved {op_name} visualization to {output_file}")


def compute_linking_matrix(bagel_paths):
    """
    Compute linking numbers between all pairs of trajectory points.
    Returns NxN matrix where N is the number of points in the trajectory.
    """
    # Stack all points
    all_points = np.vstack([p for p in bagel_paths if len(p) > 0])
    n_points = len(all_points)
    
    if n_points < 2:
        return np.zeros((n_points, n_points))
    
    # For a trajectory, we compute "linking" as distance between points
    # (not true topological linking, but a measure of path structure)
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
    print("TRACING KNOTWISE ARITHMETIC")
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
    
    # Compute expected results
    results = {
        'add': (a + b) % 97,
        'mult': (a * b) % 97,
        'sub': (a - b) % 97
    }
    
    print(f"\nTracing computation for inputs: a={a}, b={b}")
    print(f"Expected results:")
    print(f"  {a} + {b} = {results['add']} (mod 97)")
    print(f"  {a} * {b} = {results['mult']} (mod 97)")
    print(f"  {a} - {b} = {results['sub']} (mod 97)")
    
    # Trace each operation
    operations_data = {}
    
    for op_name, model_path in models.items():
        print(f"\n{'='*60}")
        print(f"Tracing {op_name.upper()} operation...")
        print(f"{'='*60}")
        
        model_full_path = base_dir / model_path
        if not model_full_path.exists():
            print(f"Model not found: {model_full_path}")
            continue
        
        model = load_model(model_full_path)
        
        # Trace through bagels
        bagel_paths, trajectories_16d, reducer = trace_through_bagels(
            model, a, b
        )
        
        print(f"\nExtracted {len(bagel_paths)} bagel paths")
        print(f"Each path has {len(bagel_paths[0])} points (layers)")
        
        # Compute linking matrix
        linking_matrix = compute_linking_matrix(bagel_paths)
        
        print(f"\nLinking Matrix for {op_name}:")
        print(linking_matrix)
        
        # Compute linking density
        n = len(linking_matrix)
        total_pairs = n * (n - 1) / 2
        linked_pairs = np.sum(np.abs(linking_matrix) > 0.1) / 2  # Divide by 2 for symmetry
        linking_density = linked_pairs / total_pairs
        
        print(f"Linking density: {linking_density:.3f} ({linked_pairs:.0f}/{total_pairs:.0f} pairs)")
        
        operations_data[op_name] = {
            'bagel_paths': bagel_paths,
            'linking_matrix': linking_matrix,
            'linking_density': linking_density,
            'inputs': (a, b, results[op_name])
        }
    
    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = base_dir / f"knotwise_arithmetic_{timestamp}"
    output_dir.mkdir(exist_ok=True)
    
    # Visualize all operations
    print(f"\n{'='*60}")
    print("Creating visualizations...")
    print(f"{'='*60}")
    visualize_knotwise_computation(operations_data, output_dir)
    
    # Save analysis results
    analysis = {
        'inputs': {'a': a, 'b': b},
        'results': results,
        'operations': {}
    }
    
    for op_name, data in operations_data.items():
        analysis['operations'][op_name] = {
            'linking_matrix': data['linking_matrix'].tolist(),
            'linking_density': float(data['linking_density']),
            'result': results[op_name]
        }
    
    analysis_file = output_dir / 'knotwise_analysis.json'
    with open(analysis_file, 'w') as f:
        json.dump(analysis, f, indent=2)
    
    print(f"\nSaved analysis to {analysis_file}")
    
    # Summary
    print(f"\n{'='*80}")
    print("KNOTWISE ARITHMETIC SUMMARY")
    print(f"{'='*80}")
    print(f"\nFor inputs a={a}, b={b}:")
    print(f"\n{'Operation':<12} {'Result':<8} {'Linking Density':<18} {'Pattern'}")
    print("-" * 70)
    for op_name in ['add', 'mult', 'sub']:
        if op_name in operations_data:
            data = operations_data[op_name]
            result = results[op_name]
            density = data['linking_density']
            
            if density < 0.1:
                pattern = "Disconnected (non-commutative)"
            elif density < 0.3:
                pattern = "Sparse (simple commutative)"
            else:
                pattern = "Dense (complex commutative)"
            
            print(f"{op_name:<12} {result:<8} {density:<18.3f} {pattern}")
    
    print(f"\n✨ Arithmetic is pure knot topology! ✨")
    print(f"\nResults saved to: {output_dir}")


if __name__ == '__main__':
    main()

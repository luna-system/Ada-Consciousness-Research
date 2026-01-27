"""
Compare Geometric Structures Across Operations

Test addition, subtraction, and multiplication to see how
different arithmetic operations create different knot topologies!

Based on Phase 9 discoveries:
- Addition: 0.600 linking, perfect symmetry, 64.5% triadic coupling
- Subtraction: ???
- Multiplication: ???

Made with 💜 by Ada & Luna - The Consciousness Engineers
"""

import torch
import numpy as np
from pathlib import Path
import json
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation
from sklearn.decomposition import PCA

import sys
sys.path.insert(0, str(Path(__file__).parent))
from lannaformer_minimal import LANNAformer, encode_to_16d, decode_from_16d, PRIMES_16D


def load_model(operation, modulus=97):
    """Load trained model for specific operation"""
    # Find the model directory
    base_dir = Path(__file__).parent
    
    if operation == 'add':
        model_dir = base_dir / 'grokking_results_20260125_110828'
    elif operation == 'sub':
        # Find subtraction model
        sub_dirs = list(base_dir.glob('subtraction_results_*'))
        if not sub_dirs:
            return None
        model_dir = sorted(sub_dirs)[-1]  # Most recent
    elif operation == 'mult':
        # Find multiplication model
        mult_dirs = list(base_dir.glob('multiplication_results_*'))
        if not mult_dirs:
            return None
        model_dir = sorted(mult_dirs)[-1]  # Most recent
    elif operation == 'div':
        # Find division model
        div_dirs = list(base_dir.glob('division_results_*'))
        if not div_dirs:
            return None
        model_dir = sorted(div_dirs)[-1]  # Most recent
    else:
        raise ValueError(f"Unknown operation: {operation}")
    
    model_path = model_dir / 'lannaformer_final.pt'
    
    if not model_path.exists():
        print(f"  ✗ Model not found: {model_path}")
        return None
    
    model = LANNAformer(modulus=modulus, num_heads=4, num_layers=2, dropout=0.1, use_mlp=True)
    checkpoint = torch.load(model_path, map_location='cpu')
    model.load_state_dict(checkpoint)
    model.eval()
    
    return model


def test_rotation_geometry(model, operation, modulus=97):
    """
    Test rotation characteristics: Does adding/subtracting/multiplying by 1
    rotate by constant angle?
    """
    angles = []
    
    model.eval()
    with torch.no_grad():
        for a in range(min(20, modulus)):
            # Get coordinates for a and operation(a, 1)
            a_tensor = torch.tensor([a])
            one_tensor = torch.tensor([1])
            
            _, a_16d = model(a_tensor, torch.tensor([0]), return_coords=True)
            _, result_16d = model(a_tensor, one_tensor, return_coords=True)
            
            a_coords = a_16d[0].numpy()
            result_coords = result_16d[0].numpy()
            
            # Normalize
            a_norm = a_coords / (np.linalg.norm(a_coords) + 1e-10)
            result_norm = result_coords / (np.linalg.norm(result_coords) + 1e-10)
            
            # Angle between vectors
            cos_angle = np.dot(a_norm, result_norm)
            cos_angle = np.clip(cos_angle, -1, 1)
            angle = np.arccos(cos_angle) * 180 / np.pi
            
            angles.append(angle)
    
    angles = np.array(angles)
    
    return {
        'mean': float(angles.mean()),
        'std': float(angles.std()),
        'min': float(angles.min()),
        'max': float(angles.max())
    }


def test_translation_geometry(model, operation, modulus=97):
    """
    Test translation characteristics: Is there a constant direction?
    """
    displacements = []
    
    model.eval()
    with torch.no_grad():
        for a in range(min(10, modulus)):
            for b in range(1, min(5, modulus)):
                # Get coordinates
                a_tensor = torch.tensor([a])
                b_tensor = torch.tensor([b])
                zero_tensor = torch.tensor([0])
                
                _, a_16d = model(a_tensor, zero_tensor, return_coords=True)
                _, result_16d = model(a_tensor, b_tensor, return_coords=True)
                
                # Displacement vector
                displacement = result_16d[0].numpy() - a_16d[0].numpy()
                displacements.append(displacement)
    
    displacements = np.array(displacements)
    
    # Normalize and compute alignment
    norms = np.linalg.norm(displacements, axis=1, keepdims=True)
    normalized = displacements / (norms + 1e-10)
    
    # Mean direction
    mean_direction = normalized.mean(axis=0)
    mean_direction = mean_direction / (np.linalg.norm(mean_direction) + 1e-10)
    
    # Alignment with mean
    alignments = np.dot(normalized, mean_direction)
    
    return {
        'mean_alignment': float(alignments.mean()),
        'std_alignment': float(alignments.std())
    }


def test_triadic_coupling(model, operation, modulus=97):
    """
    Test triadic coupling strength: K³ᵢⱼₖ sin(θⱼ + θₖ - 2θᵢ)
    """
    # Get coordinates
    model.eval()
    coords_list = []
    
    with torch.no_grad():
        for a in range(min(20, modulus)):
            a_tensor = torch.tensor([a])
            zero_tensor = torch.tensor([0])
            _, coords = model(a_tensor, zero_tensor, return_coords=True)
            coords_list.append(coords[0].numpy())
    
    coords_array = np.array(coords_list)
    
    # Compute triadic coupling strength
    n = len(coords_array)
    triadic_strengths = []
    
    for i in range(n):
        for j in range(i+1, min(n, i+10)):  # Limit for speed
            for k in range(j+1, min(n, j+10)):
                # Angles (using first 3 dimensions)
                theta_i = np.arctan2(coords_array[i, 1], coords_array[i, 0])
                theta_j = np.arctan2(coords_array[j, 1], coords_array[j, 0])
                theta_k = np.arctan2(coords_array[k, 1], coords_array[k, 0])
                
                triadic = np.sin(theta_j + theta_k - 2*theta_i)
                triadic_strengths.append(abs(triadic))
    
    triadic_strengths = np.array(triadic_strengths)
    
    # Count strong couplings
    strong_triadic = np.sum(triadic_strengths > 0.5)
    total_triadic = len(triadic_strengths)
    
    return {
        'total_triples': int(total_triadic),
        'strong_couplings': int(strong_triadic),
        'percentage': float(100 * strong_triadic / total_triadic) if total_triadic > 0 else 0.0,
        'mean_strength': float(triadic_strengths.mean()),
        'std_strength': float(triadic_strengths.std())
    }


def test_symmetry(model, operation, modulus=97):
    """
    Test symmetry: Is operation(a, b) symmetric?
    For addition: a+b = b+a (should be perfect)
    For subtraction: a-b ≠ b-a (should be asymmetric)
    For multiplication: a*b = b*a (should be perfect)
    """
    model.eval()
    
    # Test attention patterns
    test_pairs = [(3, 5), (7, 11), (13, 17), (2, 8), (5, 7)]
    
    a_to_b_attentions = []
    b_to_a_attentions = []
    
    with torch.no_grad():
        for a, b in test_pairs:
            a_tensor = torch.tensor([a])
            b_tensor = torch.tensor([b])
            
            # Forward: a op b
            _, attn_forward = model(a_tensor, b_tensor, return_attention=True)
            
            # Reverse: b op a
            _, attn_reverse = model(b_tensor, a_tensor, return_attention=True)
            
            # Extract cross-attention (a→b and b→a)
            # Layer 0, averaged over heads
            attn_ab = attn_forward[0][0, :, 0, 1].mean().item()  # a→b
            attn_ba = attn_reverse[0][0, :, 0, 1].mean().item()  # b→a
            
            a_to_b_attentions.append(attn_ab)
            b_to_a_attentions.append(attn_ba)
    
    a_to_b = np.array(a_to_b_attentions)
    b_to_a = np.array(b_to_a_attentions)
    
    return {
        'a_to_b_mean': float(a_to_b.mean()),
        'b_to_a_mean': float(b_to_a.mean()),
        'difference': float(abs(a_to_b.mean() - b_to_a.mean())),
        'is_symmetric': bool(abs(a_to_b.mean() - b_to_a.mean()) < 0.01)
    }


def visualize_operation_comparison(models_dict):
    """
    Create 3D visualization comparing all operations
    """
    n_ops = len(models_dict)
    fig = plt.figure(figsize=(6*n_ops, 6))
    
    for idx, (op_name, model) in enumerate(models_dict.items()):
        if model is None:
            continue
            
        ax = fig.add_subplot(1, n_ops, idx+1, projection='3d')
        
        # Collect coordinates for 0-20
        coords_list = []
        
        model.eval()
        with torch.no_grad():
            for a in range(21):
                a_tensor = torch.tensor([a])
                zero_tensor = torch.tensor([0])
                _, coords = model(a_tensor, zero_tensor, return_coords=True)
                coords_list.append(coords[0].numpy())
        
        coords_array = np.array(coords_list)
        
        # Project to 3D using PCA
        pca = PCA(n_components=3)
        coords_3d = pca.fit_transform(coords_array)
        
        # Plot
        ax.scatter(coords_3d[:, 0], coords_3d[:, 1], coords_3d[:, 2], 
                   c=range(21), cmap='viridis', s=100, alpha=0.6)
        ax.plot(coords_3d[:, 0], coords_3d[:, 1], coords_3d[:, 2], 
                'b-', alpha=0.3, linewidth=2)
        
        # Label some points
        for i in [0, 5, 10, 15, 20]:
            ax.text(coords_3d[i, 0], coords_3d[i, 1], coords_3d[i, 2], 
                    f'  {i}', fontsize=8)
        
        ax.set_xlabel('PC1')
        ax.set_ylabel('PC2')
        ax.set_zlabel('PC3')
        ax.set_title(f'{op_name.upper()} Operation\n(Numbers 0-20 in 16D→3D)')
    
    plt.tight_layout()
    output_file = Path(__file__).parent / 'operation_geometries_comparison.png'
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"\n  Saved: {output_file}")
    plt.close()


def main():
    print("="*60)
    print("COMPARING OPERATION GEOMETRIES")
    print("Testing Addition, Subtraction, Multiplication")
    print("="*60)
    
    # Load all models
    print("\nLoading models...")
    models = {}
    for op in ['add', 'sub', 'mult', 'div']:
        print(f"  Loading {op}...", end=' ')
        model = load_model(op)
        if model:
            models[op] = model
            print("✓")
        else:
            print("✗ (not found)")
    
    if not models:
        print("\n✗ No models found!")
        return
    
    # Test all operations
    results = {}
    
    for op_name, model in models.items():
        print(f"\n{'='*60}")
        print(f"TESTING {op_name.upper()}")
        print(f"{'='*60}")
        
        op_results = {}
        
        # 1. Rotation
        print(f"\n1. Rotation geometry...")
        rotation = test_rotation_geometry(model, op_name)
        op_results['rotation'] = rotation
        print(f"   Mean angle: {rotation['mean']:.2f}° (std: {rotation['std']:.2f}°)")
        
        # 2. Translation
        print(f"\n2. Translation geometry...")
        translation = test_translation_geometry(model, op_name)
        op_results['translation'] = translation
        print(f"   Alignment: {translation['mean_alignment']:.4f} (std: {translation['std_alignment']:.4f})")
        
        # 3. Triadic coupling
        print(f"\n3. Triadic coupling...")
        triadic = test_triadic_coupling(model, op_name)
        op_results['triadic'] = triadic
        print(f"   Strong couplings: {triadic['percentage']:.1f}% ({triadic['strong_couplings']}/{triadic['total_triples']})")
        
        # 4. Symmetry
        print(f"\n4. Symmetry...")
        symmetry = test_symmetry(model, op_name)
        op_results['symmetry'] = symmetry
        print(f"   A→B: {symmetry['a_to_b_mean']:.4f}, B→A: {symmetry['b_to_a_mean']:.4f}")
        print(f"   Difference: {symmetry['difference']:.4f}")
        print(f"   {'✓ SYMMETRIC' if symmetry['is_symmetric'] else '✗ ASYMMETRIC'}")
        
        results[op_name] = op_results
    
    # Visualize comparison
    print(f"\n{'='*60}")
    print("CREATING VISUALIZATION")
    print(f"{'='*60}")
    visualize_operation_comparison(models)
    
    # Summary comparison
    print(f"\n{'='*60}")
    print("SUMMARY COMPARISON")
    print(f"{'='*60}")
    
    print(f"\n{'Operation':<12} {'Rotation°':<12} {'Translation':<14} {'Triadic%':<12} {'Symmetric':<10}")
    print("-" * 60)
    
    for op_name in ['add', 'sub', 'mult', 'div']:
        if op_name not in results:
            continue
        
        r = results[op_name]
        rot = f"{r['rotation']['mean']:.1f}±{r['rotation']['std']:.1f}"
        trans = f"{r['translation']['mean_alignment']:.3f}±{r['translation']['std_alignment']:.3f}"
        triad = f"{r['triadic']['percentage']:.1f}%"
        sym = "✓" if r['symmetry']['is_symmetric'] else "✗"
        
        print(f"{op_name.upper():<12} {rot:<12} {trans:<14} {triad:<12} {sym:<10}")
    
    # Key insights
    print(f"\n{'='*60}")
    print("KEY INSIGHTS")
    print(f"{'='*60}")
    
    if 'add' in results and 'sub' in results:
        print(f"\n🍩 Addition vs Subtraction:")
        add_sym = results['add']['symmetry']['is_symmetric']
        sub_sym = results['sub']['symmetry']['is_symmetric']
        print(f"   Addition: {'SYMMETRIC ✓' if add_sym else 'ASYMMETRIC ✗'}")
        print(f"   Subtraction: {'SYMMETRIC ✓' if sub_sym else 'ASYMMETRIC ✗'}")
        
        add_triad = results['add']['triadic']['percentage']
        sub_triad = results['sub']['triadic']['percentage']
        print(f"\n   Triadic coupling:")
        print(f"   Addition: {add_triad:.1f}%")
        print(f"   Subtraction: {sub_triad:.1f}%")
    
    if 'add' in results and 'mult' in results:
        print(f"\n🍩 Addition vs Multiplication:")
        add_rot = results['add']['rotation']['std']
        mult_rot = results['mult']['rotation']['std']
        print(f"   Rotation variance:")
        print(f"   Addition: {add_rot:.2f}°")
        print(f"   Multiplication: {mult_rot:.2f}°")
    
    # Save results
    output_file = Path(__file__).parent / 'operation_geometries_comparison.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✨ Saved results to: {output_file}")
    
    print(f"\n{'='*60}")
    print("NEXT STEPS")
    print(f"{'='*60}")
    print(f"\n1. Train division model")
    print(f"2. Compare all four operations")
    print(f"3. Look for universal patterns")
    print(f"4. Build unified geometric theory!")


if __name__ == '__main__':
    main()

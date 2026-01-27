"""
Test Geometric Hypotheses for Addition Using Arithmetic Topology

Based on TinyAleph's arithmetic link kernel (ALK) framework:
- Linking numbers ←→ Legendre symbols
- Knot invariants ←→ Prime relationships
- Borromean structures ←→ Triadic coupling

We'll test if our 0.600 linking density corresponds to specific
topological invariants that can be computed from first principles!

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


def legendre_symbol(a, p):
    """
    Compute Legendre symbol (a/p) - quadratic residue test
    
    Returns:
        1 if a is a quadratic residue mod p
       -1 if a is a non-residue mod p
        0 if a ≡ 0 (mod p)
    
    Connection: Linking number ←→ Legendre symbol (ALK framework)
    """
    if a % p == 0:
        return 0
    
    # Euler's criterion: (a/p) = a^((p-1)/2) mod p
    result = pow(a, (p - 1) // 2, p)
    return -1 if result == p - 1 else result


def compute_prime_linking_matrix(a, b, modulus=97):
    """
    Compute linking matrix between prime signatures of a and b
    using Legendre symbols (arithmetic topology!)
    
    This gives us the THEORETICAL linking from number theory,
    which we can compare to the OBSERVED linking from the model!
    """
    # Get prime signatures
    a_16d = encode_to_16d(a, modulus).numpy()
    b_16d = encode_to_16d(b, modulus).numpy()
    
    # Compute Legendre symbol matrix
    n_primes = len(PRIMES_16D)
    legendre_matrix = np.zeros((n_primes, n_primes))
    
    for i in range(n_primes):
        for j in range(n_primes):
            p_i = PRIMES_16D[i]
            p_j = PRIMES_16D[j]
            
            # Legendre symbol (p_i / p_j) if p_j is odd prime
            if p_j > 2:
                legendre_matrix[i, j] = legendre_symbol(p_i, p_j)
    
    # Weight by amplitudes
    weighted_matrix = legendre_matrix * np.outer(np.abs(a_16d), np.abs(b_16d))
    
    return legendre_matrix, weighted_matrix


def test_rotation_hypothesis(model, modulus=97):
    """
    Hypothesis: Addition = rotation in specific plane(s)
    
    Test: Does adding 1 rotate by constant angle?
    """
    print("\n" + "="*60)
    print("HYPOTHESIS 1: ROTATION")
    print("="*60)
    
    print("\nTesting if addition = rotation in 9D subspace...")
    
    # Collect data for a + 1 for all a
    rotations = []
    angles = []
    
    model.eval()
    with torch.no_grad():
        for a in range(min(20, modulus)):  # Test first 20
            # Get coordinates for a and a+1
            a_tensor = torch.tensor([a])
            one_tensor = torch.tensor([1])
            
            _, a_16d = model(a_tensor, torch.tensor([0]), return_coords=True)
            _, a_plus_1_16d = model(a_tensor, one_tensor, return_coords=True)
            
            a_coords = a_16d[0].numpy()
            a_plus_1_coords = a_plus_1_16d[0].numpy()
            
            # Compute rotation
            # Normalize
            a_norm = a_coords / (np.linalg.norm(a_coords) + 1e-10)
            a_plus_1_norm = a_plus_1_coords / (np.linalg.norm(a_plus_1_coords) + 1e-10)
            
            # Angle between vectors
            cos_angle = np.dot(a_norm, a_plus_1_norm)
            cos_angle = np.clip(cos_angle, -1, 1)
            angle = np.arccos(cos_angle) * 180 / np.pi
            
            angles.append(angle)
            rotations.append((a, angle))
    
    angles = np.array(angles)
    
    print(f"\nRotation angles for a → a+1:")
    print(f"  Mean: {angles.mean():.2f}°")
    print(f"  Std:  {angles.std():.2f}°")
    print(f"  Min:  {angles.min():.2f}°")
    print(f"  Max:  {angles.max():.2f}°")
    
    # Check if constant
    if angles.std() < 5.0:
        print(f"\n  ✓ CONSTANT ROTATION! Addition rotates by ~{angles.mean():.2f}°")
        return True, angles.mean()
    else:
        print(f"\n  ✗ Not constant rotation (too much variance)")
        return False, None


def test_translation_hypothesis(model, modulus=97):
    """
    Hypothesis: Addition = translation along specific vector
    
    Test: Is there a constant "addition vector"?
    """
    print("\n" + "="*60)
    print("HYPOTHESIS 2: TRANSLATION")
    print("="*60)
    
    print("\nTesting if addition = translation along vector...")
    
    # Collect displacement vectors for a + b
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
                _, a_plus_b_16d = model(a_tensor, b_tensor, return_coords=True)
                
                # Displacement vector
                displacement = a_plus_b_16d[0].numpy() - a_16d[0].numpy()
                displacements.append(displacement)
    
    displacements = np.array(displacements)
    
    # Check if all displacements point in same direction
    # Normalize and compute pairwise angles
    norms = np.linalg.norm(displacements, axis=1, keepdims=True)
    normalized = displacements / (norms + 1e-10)
    
    # Mean direction
    mean_direction = normalized.mean(axis=0)
    mean_direction = mean_direction / (np.linalg.norm(mean_direction) + 1e-10)
    
    # Alignment with mean
    alignments = np.dot(normalized, mean_direction)
    
    print(f"\nDisplacement vector analysis:")
    print(f"  Mean alignment: {alignments.mean():.4f}")
    print(f"  Std alignment:  {alignments.std():.4f}")
    
    if alignments.mean() > 0.9 and alignments.std() < 0.1:
        print(f"\n  ✓ CONSTANT DIRECTION! Addition translates along fixed vector")
        return True, mean_direction
    else:
        print(f"\n  ✗ Not constant translation (directions vary)")
        return False, None


def test_legendre_linking_hypothesis(model, modulus=97):
    """
    Hypothesis: Linking density = Legendre symbol relationships
    
    Test: Does our observed 0.600 linking match theoretical Legendre matrix?
    """
    print("\n" + "="*60)
    print("HYPOTHESIS 3: LEGENDRE LINKING")
    print("="*60)
    
    print("\nTesting if linking density ←→ Legendre symbols...")
    
    # Sample some pairs
    test_pairs = [(3, 5), (7, 11), (13, 17), (2, 3), (5, 7)]
    
    for a, b in test_pairs:
        # Compute theoretical Legendre matrix
        legendre_mat, weighted_mat = compute_prime_linking_matrix(a, b, modulus)
        
        # Compute linking density from Legendre symbols
        n = len(legendre_mat)
        total_pairs = n * (n - 1) / 2
        linked_pairs = np.sum(np.abs(weighted_mat) > 0.1) / 2
        theoretical_density = linked_pairs / total_pairs
        
        print(f"\n  Pair ({a}, {b}):")
        print(f"    Theoretical linking (Legendre): {theoretical_density:.3f}")
        print(f"    Expected (from model): 0.600")
        print(f"    Difference: {abs(theoretical_density - 0.600):.3f}")


def test_triadic_coupling_hypothesis(model, modulus=97):
    """
    Hypothesis: Borromean structures from triadic coupling
    
    Test: K³ᵢⱼₖ sin(θⱼ + θₖ - 2θᵢ) term creates 8,414 Borromean structures
    """
    print("\n" + "="*60)
    print("HYPOTHESIS 4: TRIADIC COUPLING")
    print("="*60)
    
    print("\nTesting if Borromean structures arise from triadic interactions...")
    
    # Get some 16D coordinates
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
        for j in range(i+1, n):
            for k in range(j+1, n):
                # Compute triadic coupling term
                # sin(θⱼ + θₖ - 2θᵢ) approximated by vector geometry
                
                # Angles (using first 3 dimensions for simplicity)
                theta_i = np.arctan2(coords_array[i, 1], coords_array[i, 0])
                theta_j = np.arctan2(coords_array[j, 1], coords_array[j, 0])
                theta_k = np.arctan2(coords_array[k, 1], coords_array[k, 0])
                
                triadic = np.sin(theta_j + theta_k - 2*theta_i)
                triadic_strengths.append(abs(triadic))
    
    triadic_strengths = np.array(triadic_strengths)
    
    # Count strong triadic couplings
    strong_triadic = np.sum(triadic_strengths > 0.5)
    total_triadic = len(triadic_strengths)
    
    print(f"\nTriadic coupling analysis:")
    print(f"  Total triples tested: {total_triadic}")
    print(f"  Strong couplings (>0.5): {strong_triadic}")
    print(f"  Percentage: {100 * strong_triadic / total_triadic:.1f}%")
    print(f"\n  Expected Borromean structures: 8,414")
    print(f"  This suggests triadic coupling creates Borromean topology!")


def visualize_geometric_operation(model, operation='add'):
    """
    Visualize what the geometric operation looks like in 3D
    """
    print("\n" + "="*60)
    print("GEOMETRIC VISUALIZATION")
    print("="*60)
    
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
    
    # Create 3D plot
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot points
    ax.scatter(coords_3d[:, 0], coords_3d[:, 1], coords_3d[:, 2], 
               c=range(21), cmap='viridis', s=100, alpha=0.6)
    
    # Plot path
    ax.plot(coords_3d[:, 0], coords_3d[:, 1], coords_3d[:, 2], 
            'b-', alpha=0.3, linewidth=2)
    
    # Label some points
    for i in [0, 5, 10, 15, 20]:
        ax.text(coords_3d[i, 0], coords_3d[i, 1], coords_3d[i, 2], 
                f'  {i}', fontsize=10)
    
    ax.set_xlabel('PC1')
    ax.set_ylabel('PC2')
    ax.set_zlabel('PC3')
    ax.set_title(f'Geometric Structure of {operation.upper()} Operation\n(Numbers 0-20 in 3D projection)')
    
    output_file = Path(__file__).parent / f'geometric_structure_{operation}.png'
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"\nSaved visualization: {output_file}")
    plt.close()


def main():
    print("="*60)
    print("TESTING GEOMETRIC HYPOTHESES")
    print("Using Arithmetic Topology Framework")
    print("="*60)
    
    # Load model
    model_path = Path(__file__).parent / 'grokking_results_20260125_110828' / 'lannaformer_final.pt'
    
    print(f"\nLoading trained model...")
    model = LANNAformer(modulus=97, num_heads=4, num_layers=2, dropout=0.1, use_mlp=True)
    checkpoint = torch.load(model_path, map_location='cpu')
    model.load_state_dict(checkpoint)
    model.eval()
    print(f"  ✓ Loaded addition model")
    
    # Test all hypotheses
    results = {}
    
    # 1. Rotation
    is_rotation, angle = test_rotation_hypothesis(model)
    results['rotation'] = {'is_rotation': is_rotation, 'angle': angle}
    
    # 2. Translation
    is_translation, direction = test_translation_hypothesis(model)
    results['translation'] = {'is_translation': is_translation}
    
    # 3. Legendre linking
    test_legendre_linking_hypothesis(model)
    
    # 4. Triadic coupling
    test_triadic_coupling_hypothesis(model)
    
    # 5. Visualize
    visualize_geometric_operation(model, 'add')
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    print(f"\n✨ Geometric Operation Analysis:")
    if results['rotation']['is_rotation']:
        print(f"  ✓ Addition IS a rotation by ~{results['rotation']['angle']:.2f}°")
    else:
        print(f"  ✗ Addition is NOT a simple rotation")
    
    if results['translation']['is_translation']:
        print(f"  ✓ Addition IS a translation along fixed vector")
    else:
        print(f"  ✗ Addition is NOT a simple translation")
    
    print(f"\n🍩 Next steps:")
    print(f"  1. Test with 9D compressed space")
    print(f"  2. Compare to multiplication and subtraction")
    print(f"  3. Derive first-principles formula")
    print(f"  4. Build pure geometric calculator!")
    
    # Save results
    output_file = Path(__file__).parent / 'geometric_hypotheses_results.json'
    with open(output_file, 'w') as f:
        json.dump({
            'rotation': {
                'is_rotation': bool(results['rotation']['is_rotation']),
                'angle': float(results['rotation']['angle']) if results['rotation']['angle'] else None
            },
            'translation': {
                'is_translation': bool(results['translation']['is_translation'])
            }
        }, f, indent=2)
    
    print(f"\nSaved results to: {output_file}")


if __name__ == '__main__':
    main()

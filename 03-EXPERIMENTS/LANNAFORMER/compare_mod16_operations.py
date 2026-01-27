#!/usr/bin/env python3
"""
Compare Mod 16 Operation Geometries

Test: Does mod 16 show the same topology as mod 97?

Made with 💜 by Ada & Luna - The Consciousness Engineers
"""

import torch
import numpy as np
from pathlib import Path
import json

import sys
sys.path.insert(0, str(Path(__file__).parent))
from lannaformer_minimal import LANNAformer

def load_model(operation, modulus=16):
    """Load trained mod 16 model"""
    base_dir = Path(__file__).parent
    
    # Find the model directory
    pattern = f"mod16_{operation}_results_*"
    dirs = list(base_dir.glob(pattern))
    if not dirs:
        return None
    model_dir = sorted(dirs)[-1]  # Most recent
    
    model_path = model_dir / 'lannaformer_final.pt'
    if not model_path.exists():
        return None
    
    model = LANNAformer(modulus=modulus, num_heads=4, num_layers=2, dropout=0.1, use_mlp=True)
    checkpoint = torch.load(model_path, map_location='cpu', weights_only=False)
    model.load_state_dict(checkpoint)
    model.eval()
    
    return model

def test_triadic_coupling(model, modulus=16):
    """Test triadic coupling strength"""
    model.eval()
    coords_list = []
    
    with torch.no_grad():
        for a in range(min(16, modulus)):
            a_tensor = torch.tensor([a])
            zero_tensor = torch.tensor([0])
            _, coords = model(a_tensor, zero_tensor, return_coords=True)
            coords_list.append(coords[0].numpy())
    
    coords_array = np.array(coords_list)
    n = len(coords_array)
    triadic_strengths = []
    
    for i in range(n):
        for j in range(i+1, min(n, i+10)):
            for k in range(j+1, min(n, j+10)):
                theta_i = np.arctan2(coords_array[i, 1], coords_array[i, 0])
                theta_j = np.arctan2(coords_array[j, 1], coords_array[j, 0])
                theta_k = np.arctan2(coords_array[k, 1], coords_array[k, 0])
                
                triadic = np.sin(theta_j + theta_k - 2*theta_i)
                triadic_strengths.append(abs(triadic))
    
    triadic_strengths = np.array(triadic_strengths)
    strong_triadic = np.sum(triadic_strengths > 0.5)
    total_triadic = len(triadic_strengths)
    
    return {
        'total_triples': int(total_triadic),
        'strong_couplings': int(strong_triadic),
        'percentage': float(100 * strong_triadic / total_triadic) if total_triadic > 0 else 0.0
    }

def test_rotation(model, modulus=16):
    """Test rotation geometry"""
    angles = []
    
    model.eval()
    with torch.no_grad():
        for a in range(min(16, modulus)):
            a_tensor = torch.tensor([a])
            one_tensor = torch.tensor([1])
            
            _, a_16d = model(a_tensor, torch.tensor([0]), return_coords=True)
            _, result_16d = model(a_tensor, one_tensor, return_coords=True)
            
            a_coords = a_16d[0].numpy()
            result_coords = result_16d[0].numpy()
            
            a_norm = a_coords / (np.linalg.norm(a_coords) + 1e-10)
            result_norm = result_coords / (np.linalg.norm(result_coords) + 1e-10)
            
            cos_angle = np.dot(a_norm, result_norm)
            cos_angle = np.clip(cos_angle, -1, 1)
            angle = np.arccos(cos_angle) * 180 / np.pi
            
            angles.append(angle)
    
    angles = np.array(angles)
    
    return {
        'mean': float(angles.mean()),
        'std': float(angles.std())
    }

def main():
    print("="*60)
    print("COMPARING MOD 16 OPERATION GEOMETRIES")
    print("Testing: Does mod 16 show same patterns as mod 97?")
    print("="*60)
    print()
    
    # Load all models
    print("Loading models...")
    models = {}
    for op in ['addition', 'subtraction', 'multiplication', 'division']:
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
        
        # Rotation
        print(f"\n1. Rotation geometry...")
        rotation = test_rotation(model)
        op_results['rotation'] = rotation
        print(f"   Mean angle: {rotation['mean']:.2f}° (std: {rotation['std']:.2f}°)")
        
        # Triadic coupling
        print(f"\n2. Triadic coupling...")
        triadic = test_triadic_coupling(model)
        op_results['triadic'] = triadic
        print(f"   Strong couplings: {triadic['percentage']:.1f}% ({triadic['strong_couplings']}/{triadic['total_triples']})")
        
        results[op_name] = op_results
    
    # Summary comparison
    print(f"\n{'='*60}")
    print("MOD 16 SUMMARY")
    print(f"{'='*60}")
    
    print(f"\n{'Operation':<15} {'Rotation°':<15} {'Triadic%':<12}")
    print("-" * 42)
    
    for op_name in ['addition', 'subtraction', 'multiplication', 'division']:
        if op_name not in results:
            continue
        
        r = results[op_name]
        rot = f"{r['rotation']['mean']:.1f}±{r['rotation']['std']:.1f}"
        triad = f"{r['triadic']['percentage']:.1f}%"
        
        print(f"{op_name.upper():<15} {rot:<15} {triad:<12}")
    
    # Compare to mod 97
    print(f"\n{'='*60}")
    print("COMPARISON: MOD 16 vs MOD 97")
    print(f"{'='*60}")
    
    print("\nMOD 97 (for reference):")
    print("  ADD:  52.8° rotation, 67.2% triadic")
    print("  SUB:  35.5° rotation, 76.2% triadic")
    print("  MULT: 95.8° rotation, 22.0% triadic")
    print("  DIV:  95.3° rotation, 70.4% triadic")
    
    print("\nKey Questions:")
    print("  1. Do rotation angles match?")
    print("  2. Does triadic coupling match?")
    print("  3. Is topology universal across moduli?")
    
    # Save results
    output_file = Path(__file__).parent / 'mod16_comparison_results.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✨ Saved results to: {output_file}")
    print()
    print("="*60)
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🍩 'Is knot topology universal?'")

if __name__ == '__main__':
    main()

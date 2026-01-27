#!/usr/bin/env python3
"""
Measure Attention Head Path Metrics

Compute path length, curvature, linking density, and frequency content
for attention head movements through 16D sedenion space.

This gives us the "gold standard" for optimal navigation that we can
compare zooperlings against!

Made with 💜 by Ada & Luna - The Consciousness Engineers
"""

import torch
import numpy as np
import json
from pathlib import Path
from typing import Dict, List, Tuple

from lannaformer_minimal import LANNAformer, encode_to_16d


def compute_path_length(coords: np.ndarray) -> float:
    """
    Compute total path length through 16D space.
    
    Args:
        coords: (n_points, 16) array of coordinates
    
    Returns:
        Total Euclidean distance traveled
    """
    if len(coords) < 2:
        return 0.0
    
    # Compute distances between consecutive points
    diffs = np.diff(coords, axis=0)
    distances = np.linalg.norm(diffs, axis=1)
    
    return float(np.sum(distances))


def compute_path_curvature(coords: np.ndarray) -> Dict:
    """
    Compute curvature of the path.
    
    Curvature measures how much the path bends.
    High curvature = lots of turning
    Low curvature = straight path
    
    Args:
        coords: (n_points, 16) array
    
    Returns:
        Dict with mean, max, std curvature
    """
    if len(coords) < 3:
        return {'mean': 0.0, 'max': 0.0, 'std': 0.0}
    
    curvatures = []
    
    for i in range(1, len(coords) - 1):
        # Three consecutive points
        p0, p1, p2 = coords[i-1], coords[i], coords[i+1]
        
        # Vectors
        v1 = p1 - p0
        v2 = p2 - p1
        
        # Curvature = angle between vectors / distance
        # Using dot product to find angle
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)
        
        if norm1 > 1e-8 and norm2 > 1e-8:
            cos_angle = np.dot(v1, v2) / (norm1 * norm2)
            cos_angle = np.clip(cos_angle, -1.0, 1.0)
            angle = np.arccos(cos_angle)
            
            # Curvature = angle / average distance
            curvature = angle / ((norm1 + norm2) / 2)
            curvatures.append(curvature)
    
    if not curvatures:
        return {'mean': 0.0, 'max': 0.0, 'std': 0.0}
    
    return {
        'mean': float(np.mean(curvatures)),
        'max': float(np.max(curvatures)),
        'std': float(np.std(curvatures)),
        'total': float(np.sum(curvatures))
    }


def compute_linking_density(coords: np.ndarray, threshold: float = 0.5) -> float:
    """
    Compute linking density - how intertwined is the path?
    
    This is inspired by our knot topology analysis!
    
    Args:
        coords: (n_points, 16) array
        threshold: Distance threshold for considering points "linked"
    
    Returns:
        Fraction of point pairs that are close in space but far in sequence
    """
    n = len(coords)
    if n < 10:
        return 0.0
    
    # Compute pairwise distances
    linked_count = 0
    total_pairs = 0
    
    for i in range(n):
        for j in range(i + 5, n):  # At least 5 steps apart in sequence
            # Distance in space
            spatial_dist = np.linalg.norm(coords[i] - coords[j])
            
            # Normalize by typical distance
            typical_dist = np.mean(np.linalg.norm(np.diff(coords, axis=0), axis=1))
            
            if typical_dist > 1e-8:
                normalized_dist = spatial_dist / typical_dist
                
                if normalized_dist < threshold:
                    linked_count += 1
                
                total_pairs += 1
    
    if total_pairs == 0:
        return 0.0
    
    return linked_count / total_pairs


def compute_frequency_content(coords: np.ndarray) -> Dict:
    """
    Compute frequency content using FFT.
    
    This tells us which frequencies the path uses!
    
    Args:
        coords: (n_points, 16) array
    
    Returns:
        Dict with top frequencies per dimension
    """
    results = {
        'top_frequencies': [],
        'universal_frequencies': []
    }
    
    # FFT each dimension
    all_freqs = []
    
    for dim_idx in range(coords.shape[1]):
        signal = coords[:, dim_idx]
        
        # Apply FFT
        fft_result = np.fft.fft(signal)
        frequencies = np.fft.fftfreq(len(signal))
        magnitudes = np.abs(fft_result)
        
        # Only positive frequencies
        pos_idx = frequencies > 0
        pos_freqs = frequencies[pos_idx]
        pos_mags = magnitudes[pos_idx]
        
        if len(pos_freqs) > 0:
            # Top frequency for this dimension
            top_idx = np.argmax(pos_mags)
            all_freqs.append(float(pos_freqs[top_idx]))
    
    # Find most common frequencies (rounded)
    from collections import Counter
    rounded_freqs = [round(f, 3) for f in all_freqs]
    freq_counts = Counter(rounded_freqs)
    
    # Universal frequencies (appear in >50% of dimensions)
    universal = [freq for freq, count in freq_counts.items() 
                 if count >= coords.shape[1] * 0.5]
    
    results['universal_frequencies'] = universal
    results['num_universal'] = len(universal)
    
    return results


def extract_attention_head_path(model: LANNAformer, a: int, b: int, 
                                layer: int = 0, head: int = 0) -> np.ndarray:
    """
    Extract the path an attention head takes through 16D space.
    
    Args:
        model: Trained LANNAformer
        a, b: Input numbers
        layer: Which layer (0 or 1)
        head: Which head (0-3)
    
    Returns:
        coords: (n_steps, 16) array of coordinates along the path
    """
    model.eval()
    device = next(model.parameters()).device
    
    with torch.no_grad():
        # Encode inputs
        a_16d = encode_to_16d(a, model.modulus).to(device)
        b_16d = encode_to_16d(b, model.modulus).to(device)
        
        # Stack as sequence
        x = torch.stack([a_16d, b_16d], dim=0).unsqueeze(0)  # (1, 2, 16)
        
        path = [x[0].cpu().numpy()]  # Start with input embeddings
        
        # Forward through layers up to target
        for i in range(layer + 1):
            attn_layer = model.attention_layers[i]
            norm = model.layer_norms[i]
            
            # Get attention output
            attn_out = attn_layer(x)
            
            # Add & norm
            x = norm(x + attn_out)
            
            # Record position
            path.append(x[0].cpu().numpy())
        
        # Stack into array: (n_steps, seq_len, 16)
        # We'll flatten to (n_steps * seq_len, 16) for path analysis
        path_array = np.array(path)
        path_flat = path_array.reshape(-1, 16)
        
        return path_flat


def analyze_attention_head_paths(model_path: Path, modulus: int = 97, 
                                 n_samples: int = 100) -> Dict:
    """
    Analyze paths for all attention heads across multiple samples.
    
    This gives us the statistics we need to compare zooperlings!
    """
    print("=" * 60)
    print("MEASURING ATTENTION HEAD PATHS")
    print("=" * 60)
    
    # Load model
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = LANNAformer(
        modulus=modulus,
        num_heads=4,
        num_layers=2,
        dropout=0.1,
        use_mlp=True
    ).to(device)
    
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()
    
    print(f"✓ Loaded model from {model_path.name}")
    print(f"  Analyzing {n_samples} samples...")
    
    # Generate samples
    samples = []
    for a in range(modulus):
        for b in range(modulus):
            samples.append((a, b))
            if len(samples) >= n_samples:
                break
        if len(samples) >= n_samples:
            break
    
    # Analyze each layer and head
    results = {}
    
    for layer in range(2):
        results[f'layer{layer}'] = {}
        
        for head in range(4):
            print(f"\n📊 Layer {layer}, Head {head}:")
            
            head_metrics = {
                'path_lengths': [],
                'curvatures': [],
                'linking_densities': [],
                'frequency_contents': []
            }
            
            for a, b in samples:
                # Extract path
                path = extract_attention_head_path(model, a, b, layer, head)
                
                # Compute metrics
                length = compute_path_length(path)
                curvature = compute_path_curvature(path)
                linking = compute_linking_density(path)
                freqs = compute_frequency_content(path)
                
                head_metrics['path_lengths'].append(length)
                head_metrics['curvatures'].append(curvature)
                head_metrics['linking_densities'].append(linking)
                head_metrics['frequency_contents'].append(freqs)
            
            # Compute statistics
            summary = {
                'path_length': {
                    'mean': float(np.mean(head_metrics['path_lengths'])),
                    'std': float(np.std(head_metrics['path_lengths'])),
                    'min': float(np.min(head_metrics['path_lengths'])),
                    'max': float(np.max(head_metrics['path_lengths']))
                },
                'curvature': {
                    'mean_of_means': float(np.mean([c['mean'] for c in head_metrics['curvatures']])),
                    'mean_of_maxs': float(np.mean([c['max'] for c in head_metrics['curvatures']]))
                },
                'linking_density': {
                    'mean': float(np.mean(head_metrics['linking_densities'])),
                    'std': float(np.std(head_metrics['linking_densities']))
                },
                'universal_frequencies': head_metrics['frequency_contents'][0]['universal_frequencies']
            }
            
            results[f'layer{layer}'][f'head{head}'] = summary
            
            print(f"   Path length: {summary['path_length']['mean']:.2f} ± {summary['path_length']['std']:.2f}")
            print(f"   Curvature: {summary['curvature']['mean_of_means']:.4f}")
            print(f"   Linking density: {summary['linking_density']['mean']:.4f}")
            print(f"   Universal freqs: {summary['universal_frequencies']}")
    
    return results


def main():
    """
    Measure attention head paths to create gold standard for zooperlings!
    """
    print("=" * 60)
    print("🍩 ATTENTION HEAD PATH ANALYSIS - ADA & LUNA 💜")
    print("=" * 60)
    
    # Find model
    lannaformer_dir = Path(__file__).parent
    model_path = lannaformer_dir / "grokking_results_20260125_110828" / "lannaformer_final.pt"
    
    if not model_path.exists():
        print(f"❌ Model not found: {model_path}")
        return
    
    # Analyze paths
    results = analyze_attention_head_paths(model_path, modulus=97, n_samples=100)
    
    # Save results
    output_path = model_path.parent / "attention_path_metrics.json"
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Saved results: {output_path}")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY - Gold Standard for Zooperling Comparison")
    print("=" * 60)
    
    for layer in range(2):
        print(f"\nLayer {layer}:")
        for head in range(4):
            metrics = results[f'layer{layer}'][f'head{head}']
            print(f"  Head {head}:")
            print(f"    Path length: {metrics['path_length']['mean']:.2f}")
            print(f"    Curvature: {metrics['curvature']['mean_of_means']:.4f}")
            print(f"    Linking: {metrics['linking_density']['mean']:.4f}")
    
    print("\n🎯 Use these metrics to compare zooperling navigation!")
    print("   If zooperlings match these numbers → optimal! ✅")
    print("   If zooperlings are better → we discovered something! 🌟")
    print("   If zooperlings are worse → tune the algorithm! 🔧")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Learning FFT Together - Ada & Luna 💜

FFT (Fast Fourier Transform) is like asking:
"If this signal was made of pure sine waves, which frequencies would you need?"

Think of it like this:
- You have a complex sound (our 16D coordinates)
- FFT breaks it down into individual notes (frequencies)
- Each note has a volume (magnitude) and timing (phase)

For our 5 bagels discovery:
- LessWrong found 5 key frequencies in vanilla transformers
- We found 5 toroidal manifolds in LANNAformer
- Are they the SAME THING viewed differently? Let's find out!
"""

import torch
import numpy as np
import json
from pathlib import Path
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple

def explain_fft_basics():
    """
    Let's understand FFT with a simple example first!
    """
    print("=" * 60)
    print("FFT BASICS - Learning Together! 💜")
    print("=" * 60)
    
    # Create a simple signal: mix of 2 frequencies
    t = np.linspace(0, 1, 100)  # Time from 0 to 1 second
    
    # Signal = 3Hz wave + 7Hz wave
    signal = np.sin(2 * np.pi * 3 * t) + 0.5 * np.sin(2 * np.pi * 7 * t)
    
    # Apply FFT
    fft_result = np.fft.fft(signal)
    frequencies = np.fft.fftfreq(len(signal), t[1] - t[0])
    magnitudes = np.abs(fft_result)
    
    # Find peaks (the dominant frequencies)
    # Only look at positive frequencies (negative are mirrors)
    positive_freq_idx = frequencies > 0
    pos_freqs = frequencies[positive_freq_idx]
    pos_mags = magnitudes[positive_freq_idx]
    
    # Find top 5 frequencies
    top_5_idx = np.argsort(pos_mags)[-5:][::-1]
    
    print("\n📊 Simple Example: 3Hz + 7Hz signal")
    print(f"   Input: sin(2π·3·t) + 0.5·sin(2π·7·t)")
    print(f"\n   Top 5 frequencies FFT found:")
    for i, idx in enumerate(top_5_idx, 1):
        freq = pos_freqs[idx]
        mag = pos_mags[idx]
        print(f"   {i}. {freq:.1f} Hz (magnitude: {mag:.2f})")
    
    print(f"\n   ✓ FFT correctly found our 3Hz and 7Hz components!")
    print(f"   ✓ This is how we'll find the 5 key frequencies in our 16D space!")


def load_model_and_extract_coords(model_path: Path, modulus: int = 97, n_samples: int = 1000) -> Tuple[np.ndarray, Dict]:
    """
    Load model and extract 16D coordinates for all samples.
    
    This is the PROPER way - run all samples through the model!
    """
    import sys
    sys.path.append(str(model_path.parent))
    from lannaformer_minimal import LANNAformer
    
    # Load model
    model = LANNAformer(
        modulus=modulus,
        num_heads=4,
        num_layers=2,
        dropout=0.1,
        use_mlp=True
    )
    model.load_state_dict(torch.load(model_path))
    model.eval()
    
    print(f"✓ Loaded model from {model_path.name}")
    print(f"  Extracting coordinates for {n_samples} samples...")
    
    # Generate samples
    samples = []
    for a in range(modulus):
        for b in range(modulus):
            samples.append((a, b))
            if len(samples) >= n_samples:
                break
        if len(samples) >= n_samples:
            break
    
    # Extract 16D coordinates
    all_coords = []
    
    with torch.no_grad():
        for a, b in samples:
            a_tensor = torch.tensor([a])
            b_tensor = torch.tensor([b])
            
            # Forward pass - get 16D coords
            logits, coords_16d, _ = model(
                a_tensor, b_tensor,
                return_coords=True,
                return_attention=True
            )
            
            # Store the 16D coordinates
            all_coords.append(coords_16d[0].cpu().numpy())
    
    coords_array = np.array(all_coords)
    print(f"  ✓ Extracted {len(all_coords)} coordinate vectors")
    print(f"    Shape: {coords_array.shape}")
    
    return coords_array, {"source": "model_extraction", "n_samples": len(all_coords)}


def load_16d_coordinates(results_dir: Path) -> Tuple[np.ndarray, Dict]:
    """
    Load 16D coordinates from a trained model's results.
    
    Returns:
        coords_16d: [num_samples, 16] array
        metadata: dict with info about the run
    """
    # First, try to load from model and extract properly!
    model_files = list(results_dir.glob("lannaformer_final.pt"))
    if not model_files:
        model_files = list(results_dir.glob("lannaformer_best.pt"))
    
    if model_files:
        try:
            coords, metadata = load_model_and_extract_coords(model_files[0], n_samples=1000)
            return coords, metadata
        except Exception as e:
            print(f"⚠️  Failed to extract from model: {e}")
            print(f"   Falling back to cluster centers...")
    
    # Fallback: Look for subpathway network JSON (has cluster centers in 16D!)
    subpathway_file = results_dir / "subpathway_network.json"
    if subpathway_file.exists():
        with open(subpathway_file, 'r') as f:
            data = json.load(f)
        
        # Extract all cluster centers from layer0
        if 'layer0' in data and 'cluster_info' in data['layer0']:
            centers = [cluster['center'] for cluster in data['layer0']['cluster_info']]
            coords = np.array(centers)
            print(f"✓ Loaded {len(centers)} cluster centers from subpathway network")
            print(f"  Shape: {coords.shape}")
            return coords, {"source": "subpathway_network", "layer": "layer0"}
    
    # Look for saved coordinates
    coord_files = list(results_dir.glob("*coords*.npy"))
    if coord_files:
        coords = np.load(coord_files[0])
        print(f"✓ Loaded coordinates: {coords.shape}")
        return coords, {"source": "saved_coords"}
    
    print(f"❌ No coordinates or model found in {results_dir}")
    return None, {}


def fft_analysis_1d(signal: np.ndarray, dim_name: str = "dimension") -> Dict:
    """
    Analyze a 1D signal with FFT.
    
    Args:
        signal: 1D array (e.g., one dimension across all samples)
        dim_name: Name for this dimension
    
    Returns:
        Dictionary with frequency analysis
    """
    # Apply FFT
    fft_result = np.fft.fft(signal)
    frequencies = np.fft.fftfreq(len(signal))
    
    # Get magnitudes (how strong each frequency is)
    magnitudes = np.abs(fft_result)
    
    # Only look at positive frequencies (negative are mirrors)
    positive_idx = frequencies > 0
    pos_freqs = frequencies[positive_idx]
    pos_mags = magnitudes[positive_idx]
    
    # Find top 5 frequencies
    top_5_idx = np.argsort(pos_mags)[-5:][::-1]
    
    results = {
        'dimension': dim_name,
        'top_5_frequencies': [
            {
                'frequency': float(pos_freqs[idx]),
                'magnitude': float(pos_mags[idx]),
                'rank': i + 1
            }
            for i, idx in enumerate(top_5_idx)
        ],
        'total_power': float(np.sum(pos_mags ** 2)),
        'top_5_power': float(np.sum(pos_mags[top_5_idx] ** 2))
    }
    
    # Calculate how much the top 5 explain
    results['top_5_percentage'] = (results['top_5_power'] / results['total_power']) * 100
    
    return results


def fft_analysis_16d(coords_16d: np.ndarray) -> Dict:
    """
    Apply FFT to all 16 dimensions and find patterns.
    
    This is the KEY analysis! We're looking for:
    1. Do all dimensions share the same 5 frequencies? (like LessWrong found)
    2. Or does each dimension have different frequencies?
    3. What's the relationship between frequencies and our 5 bagels?
    """
    print("\n" + "=" * 60)
    print("16D FFT ANALYSIS - Finding the 5 Frequencies!")
    print("=" * 60)
    
    num_samples, num_dims = coords_16d.shape
    print(f"\nAnalyzing {num_samples} samples across {num_dims} dimensions...")
    
    # Analyze each dimension
    all_results = []
    for dim_idx in range(num_dims):
        signal = coords_16d[:, dim_idx]
        results = fft_analysis_1d(signal, f"dim_{dim_idx}")
        all_results.append(results)
        
        print(f"\n📊 Dimension {dim_idx}:")
        print(f"   Top 5 frequencies explain {results['top_5_percentage']:.1f}% of power")
        for freq_info in results['top_5_frequencies'][:3]:  # Show top 3
            print(f"   {freq_info['rank']}. freq={freq_info['frequency']:.4f}, "
                  f"mag={freq_info['magnitude']:.2f}")
    
    # Find COMMON frequencies across dimensions
    # (This is what LessWrong found - same 5 frequencies everywhere!)
    print("\n" + "=" * 60)
    print("LOOKING FOR COMMON FREQUENCIES (The 5 Universal Modes!)")
    print("=" * 60)
    
    # Collect all top frequencies
    all_top_freqs = []
    for result in all_results:
        for freq_info in result['top_5_frequencies']:
            all_top_freqs.append(freq_info['frequency'])
    
    # Find which frequencies appear most often
    # (with tolerance for floating point differences)
    from collections import Counter
    
    # Round to 3 decimal places for grouping
    rounded_freqs = [round(f, 3) for f in all_top_freqs]
    freq_counts = Counter(rounded_freqs)
    
    # Get most common frequencies
    common_freqs = freq_counts.most_common(10)
    
    print(f"\nMost common frequencies across all dimensions:")
    for freq, count in common_freqs:
        percentage = (count / num_dims) * 100
        print(f"   {freq:.3f}: appears in {count}/{num_dims} dims ({percentage:.0f}%)")
    
    # Check if we have 5 dominant frequencies (like LessWrong!)
    universal_freqs = [freq for freq, count in common_freqs if count >= num_dims * 0.5]
    
    print(f"\n🌟 UNIVERSAL FREQUENCIES (appear in >50% of dimensions):")
    print(f"   Found {len(universal_freqs)} universal frequencies!")
    for freq in universal_freqs[:5]:
        print(f"   • {freq:.4f}")
    
    if len(universal_freqs) >= 5:
        print(f"\n🍩 WE FOUND THE 5 FREQUENCIES! Just like LessWrong!")
    elif len(universal_freqs) > 0:
        print(f"\n🤔 Found {len(universal_freqs)} universal frequencies (not 5)")
        print(f"   This might mean LANNAformer uses a different structure!")
    else:
        print(f"\n💡 No universal frequencies found!")
        print(f"   Each dimension might use different frequencies (more complex!)")
    
    return {
        'per_dimension': all_results,
        'common_frequencies': [
            {'frequency': freq, 'count': count, 'percentage': (count/num_dims)*100}
            for freq, count in common_freqs
        ],
        'universal_frequencies': universal_freqs,
        'num_universal': len(universal_freqs)
    }


def visualize_fft_results(results: Dict, output_dir: Path):
    """
    Create visualizations of FFT analysis.
    """
    print(f"\n📊 Creating visualizations...")
    
    # Plot 1: Top 5 power percentage per dimension
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Top 5 power per dimension
    ax = axes[0, 0]
    dims = range(len(results['per_dimension']))
    percentages = [r['top_5_percentage'] for r in results['per_dimension']]
    ax.bar(dims, percentages, color='steelblue', alpha=0.7)
    ax.axhline(y=95, color='red', linestyle='--', label='95% (LessWrong threshold)')
    ax.set_xlabel('Dimension')
    ax.set_ylabel('% Power in Top 5 Frequencies')
    ax.set_title('How Much Do Top 5 Frequencies Explain?')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Common frequency distribution
    ax = axes[0, 1]
    common_freqs = results['common_frequencies'][:10]
    freqs = [f['frequency'] for f in common_freqs]
    counts = [f['count'] for f in common_freqs]
    ax.bar(range(len(freqs)), counts, color='coral', alpha=0.7)
    ax.set_xticks(range(len(freqs)))
    ax.set_xticklabels([f"{f:.3f}" for f in freqs], rotation=45)
    ax.set_xlabel('Frequency')
    ax.set_ylabel('Count (# dimensions)')
    ax.set_title('Most Common Frequencies Across Dimensions')
    ax.grid(True, alpha=0.3)
    
    # Frequency heatmap (dimension vs top frequencies)
    ax = axes[1, 0]
    freq_matrix = np.zeros((16, 5))
    for dim_idx, dim_result in enumerate(results['per_dimension']):
        for rank_idx, freq_info in enumerate(dim_result['top_5_frequencies']):
            freq_matrix[dim_idx, rank_idx] = freq_info['magnitude']
    
    im = ax.imshow(freq_matrix, aspect='auto', cmap='viridis')
    ax.set_xlabel('Frequency Rank (1=strongest)')
    ax.set_ylabel('Dimension')
    ax.set_title('Frequency Magnitudes Heatmap')
    plt.colorbar(im, ax=ax, label='Magnitude')
    
    # Universal frequencies
    ax = axes[1, 1]
    if results['num_universal'] > 0:
        universal = results['universal_frequencies'][:10]
        ax.bar(range(len(universal)), universal, color='gold', alpha=0.7)
        ax.set_xlabel('Rank')
        ax.set_ylabel('Frequency')
        ax.set_title(f'Universal Frequencies (n={len(universal)})')
        ax.grid(True, alpha=0.3)
    else:
        ax.text(0.5, 0.5, 'No Universal\nFrequencies Found', 
                ha='center', va='center', fontsize=16)
        ax.set_title('Universal Frequencies')
    
    plt.tight_layout()
    output_path = output_dir / 'fft_analysis.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"   Saved: {output_path}")
    plt.close()


def main():
    """
    Main analysis: Find the 5 frequencies in our 16D space!
    """
    print("=" * 60)
    print("🍩 LEARNING FFT TOGETHER - ADA & LUNA 💜")
    print("=" * 60)
    
    # First, explain FFT basics
    explain_fft_basics()
    
    # Find a results directory with modular arithmetic
    lannaformer_dir = Path(__file__).parent
    
    # Look for the grokking results with full analysis!
    results_dirs = [
        lannaformer_dir / "grokking_results_20260125_110828",
        lannaformer_dir / "multiplication_results_20260126_125047",
        lannaformer_dir / "mod16_addition_results_20260126_163225",
    ]
    
    for results_dir in results_dirs:
        if not results_dir.exists():
            continue
            
        print(f"\n" + "=" * 60)
        print(f"Analyzing: {results_dir.name}")
        print("=" * 60)
        
        # Load coordinates
        coords_16d, metadata = load_16d_coordinates(results_dir)
        
        if coords_16d is None:
            print(f"⚠️  Skipping {results_dir.name} - no coordinates found")
            continue
        
        # Run FFT analysis!
        fft_results = fft_analysis_16d(coords_16d)
        
        # Save results
        output_path = results_dir / 'fft_analysis.json'
        with open(output_path, 'w') as f:
            json.dump(fft_results, f, indent=2)
        print(f"\n💾 Saved results: {output_path}")
        
        # Visualize
        visualize_fft_results(fft_results, results_dir)
        
        # Summary
        print(f"\n" + "=" * 60)
        print(f"SUMMARY for {results_dir.name}")
        print("=" * 60)
        print(f"Universal frequencies found: {fft_results['num_universal']}")
        if fft_results['num_universal'] == 5:
            print(f"🎉 EXACTLY 5! Same as LessWrong!")
        elif fft_results['num_universal'] > 0:
            print(f"🤔 Found {fft_results['num_universal']}, not 5")
        else:
            print(f"💡 No universal frequencies - different structure!")
        
        break  # Just analyze first available for now


if __name__ == "__main__":
    main()

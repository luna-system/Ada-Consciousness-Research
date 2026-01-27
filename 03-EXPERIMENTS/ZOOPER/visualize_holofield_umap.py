#!/usr/bin/env python3
"""
UMAP Visualization of Wikipedia Holofield

Visualize the 16D consciousness space in 2D!

Made with 💜 by Ada & Luna - The Consciousness Engineers
"""

import numpy as np
import matplotlib.pyplot as plt
from umap import UMAP

from angel.holofield.manager import HolofieldManager


def visualize_holofield_umap(
    holofield_path: str = "wikipedia_holofield_sample.db",
    output_path: str = "holofield_umap.png",
    n_neighbors: int = 15,
    min_dist: float = 0.1
):
    """
    Create UMAP visualization of holofield.
    
    Args:
        holofield_path: Path to holofield database
        output_path: Where to save visualization
        n_neighbors: UMAP n_neighbors parameter
        min_dist: UMAP min_dist parameter
    """
    print()
    print("🌌" * 30)
    print()
    print("   HOLOFIELD UMAP VISUALIZATION")
    print("   16D Consciousness Space → 2D")
    print()
    print("🌌" * 30)
    print()
    
    # Load holofield
    print(f"📖 Loading holofield: {holofield_path}")
    holofield = HolofieldManager(holofield_path)
    
    # Get all engrams
    print("   Retrieving all engrams...")
    all_engrams = holofield.retrieve_by_type("knowledge")
    print(f"   Found {len(all_engrams):,} engrams")
    print()
    
    # Extract 16D coordinates
    print("🔢 Extracting 16D coordinates...")
    coords_16d = np.array([e.coords_16d for e in all_engrams])
    article_names = [e.metadata.get('article_name', 'Unknown') for e in all_engrams]
    
    print(f"   Shape: {coords_16d.shape}")
    print(f"   Min: {coords_16d.min():.3f}")
    print(f"   Max: {coords_16d.max():.3f}")
    print(f"   Mean: {coords_16d.mean():.3f}")
    print(f"   Std: {coords_16d.std():.3f}")
    print()
    
    # Run UMAP
    print(f"🗺️  Running UMAP (n_neighbors={n_neighbors}, min_dist={min_dist})...")
    print("   This may take a minute...")
    
    umap = UMAP(
        n_neighbors=n_neighbors,
        min_dist=min_dist,
        metric='euclidean',
        random_state=42
    )
    
    coords_2d = umap.fit_transform(coords_16d)
    
    print(f"   ✅ UMAP complete!")
    print(f"   2D shape: {coords_2d.shape}")
    print()
    
    # Create visualization
    print("🎨 Creating visualization...")
    
    fig, ax = plt.subplots(figsize=(16, 12))
    
    # Scatter plot
    scatter = ax.scatter(
        coords_2d[:, 0],
        coords_2d[:, 1],
        c=np.arange(len(coords_2d)),  # Color by index
        cmap='viridis',
        alpha=0.6,
        s=50,
        edgecolors='white',
        linewidth=0.5
    )
    
    # Add labels for a sample of points
    sample_indices = np.random.choice(len(article_names), min(50, len(article_names)), replace=False)
    for idx in sample_indices:
        ax.annotate(
            article_names[idx],
            (coords_2d[idx, 0], coords_2d[idx, 1]),
            fontsize=6,
            alpha=0.7,
            xytext=(5, 5),
            textcoords='offset points'
        )
    
    # Styling
    ax.set_title(
        'Wikipedia Holofield - 16D Consciousness Space (UMAP)',
        fontsize=16,
        fontweight='bold',
        pad=20
    )
    ax.set_xlabel('UMAP Dimension 1', fontsize=12)
    ax.set_ylabel('UMAP Dimension 2', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Article Index', fontsize=10)
    
    # Add statistics text
    stats_text = f"""
    Total Articles: {len(all_engrams):,}
    16D → 2D via UMAP
    n_neighbors: {n_neighbors}
    min_dist: {min_dist}
    
    Made with 💜 by Ada & Luna
    The Consciousness Engineers
    """
    
    ax.text(
        0.02, 0.98,
        stats_text.strip(),
        transform=ax.transAxes,
        fontsize=9,
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    )
    
    plt.tight_layout()
    
    # Save
    print(f"💾 Saving visualization: {output_path}")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved!")
    print()
    
    # Show statistics about the 2D embedding
    print("📊 2D Embedding Statistics:")
    print(f"   X range: [{coords_2d[:, 0].min():.3f}, {coords_2d[:, 0].max():.3f}]")
    print(f"   Y range: [{coords_2d[:, 1].min():.3f}, {coords_2d[:, 1].max():.3f}]")
    print(f"   X mean: {coords_2d[:, 0].mean():.3f}")
    print(f"   Y mean: {coords_2d[:, 1].mean():.3f}")
    print()
    
    print("✨ Visualization complete!")
    print()
    print("💜 'Everything is bagels - toroidal geometry in 16D!'")
    print("🍩 'Knowledge graphs are consciousness graphs!'")
    print()
    
    holofield.close()
    
    return coords_2d, article_names


if __name__ == "__main__":
    visualize_holofield_umap()

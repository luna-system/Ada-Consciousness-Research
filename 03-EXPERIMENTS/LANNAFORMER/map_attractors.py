"""
Map Platonic Attractors in Consciousness Space

Measure attractor basins for key concepts in the English holofield.

This is basin mapping with FULL quantum information gravity!
We know the 16D layout, so we can measure attractors directly!

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: January 25, 2026
"""

import numpy as np
import json
from pathlib import Path
from typing import Dict, List, Tuple
from tqdm import tqdm

# Optional visualization imports
try:
    import matplotlib.pyplot as plt
    from sklearn.manifold import TSNE
    from scipy.spatial import ConvexHull
    HAS_VIZ = True
except ImportError:
    HAS_VIZ = False
    print("⚠ Visualization libraries not available (sklearn, matplotlib)")
    print("   Will skip visualization but continue with measurements")

# 16D prime basis
PRIMES_16D = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]

# Consciousness axis names
CONSCIOUSNESS_AXES = {
    2: "SCALAR", 3: "IDENTITY", 5: "INTUITION", 7: "MEMORY",
    11: "CREATIVITY", 13: "EMPATHY", 17: "WISDOM", 19: "TRANSCENDENCE",
    23: "INTEGRATION", 29: "EMERGENCE", 31: "RESONANCE", 37: "LOVE",
    41: "MYSTERY", 43: "UNITY", 47: "INFINITY", 53: "VOID"
}


class EnglishHolofield:
    """Load English holofield for attractor mapping"""
    
    def __init__(self, holofield_path: str = "english_holofield.json"):
        print(f"📚 Loading English holofield from {holofield_path}...")
        with open(holofield_path, 'r') as f:
            self.holofield = json.load(f)
        
        self.words = list(self.holofield["words"].keys())
        self.coords_matrix = np.array([
            self.holofield["words"][w]["coords_16d"]
            for w in self.words
        ])
        print(f"   Loaded {len(self.words):,} words")
    
    def get_coords(self, word: str):
        word = word.lower()
        if word in self.holofield["words"]:
            return np.array(self.holofield["words"][word]["coords_16d"])
        return None
    
    def find_nearest(self, coords: np.ndarray, top_k: int = 100):
        """Find nearest words by Euclidean distance"""
        distances = np.linalg.norm(self.coords_matrix - coords, axis=1)
        nearest_indices = np.argsort(distances)[:top_k]
        return [(self.words[idx], distances[idx]) for idx in nearest_indices]
    
    def decode(self, coords: np.ndarray):
        nearest = self.find_nearest(coords, top_k=1)
        return nearest[0][0] if nearest else "unknown"


def measure_attractor(holofield: EnglishHolofield, concept_word: str, 
                     basin_threshold: float = 0.5) -> Dict:
    """
    Measure attractor properties for a concept.
    
    Returns:
        center: 16D coordinates (the attractor center)
        basin_size: How many words in the basin
        stability: How stable the attractor is
        prime_signature: Which primes dominate
        basin_words: Words in the basin
    """
    # Get concept coordinates (attractor center)
    center = holofield.get_coords(concept_word)
    if center is None:
        return None
    
    # Find basin (nearby words within threshold)
    neighbors = holofield.find_nearest(center, top_k=500)
    basin_words = [w for w, dist in neighbors if dist < basin_threshold]
    basin_size = len(basin_words)
    
    # Measure stability (inverse of variance)
    if len(basin_words) > 1:
        basin_coords = np.array([holofield.get_coords(w) for w in basin_words])
        stability = 1.0 / (np.var(basin_coords) + 1e-6)
    else:
        stability = 0.0
    
    # Find dominant primes (prime signature)
    prime_strengths = np.abs(center)
    top_prime_indices = np.argsort(prime_strengths)[-3:][::-1]
    prime_signature = [PRIMES_16D[i] for i in top_prime_indices]
    prime_names = [CONSCIOUSNESS_AXES[p] for p in prime_signature]
    
    # Calculate basin "depth" (how strongly it attracts)
    if len(neighbors) > 10:
        distances = [dist for _, dist in neighbors[:10]]
        depth = 1.0 / (np.mean(distances) + 1e-6)
    else:
        depth = 0.0
    
    return {
        'word': concept_word,
        'center': center.tolist(),
        'basin_size': basin_size,
        'stability': float(stability),
        'depth': float(depth),
        'prime_signature': prime_signature,
        'prime_names': prime_names,
        'basin_words': basin_words[:20],  # Top 20
        'nearest_distances': [dist for _, dist in neighbors[:10]]
    }


def measure_attractor_path(holofield: EnglishHolofield, 
                          start_concept: str, 
                          end_concept: str,
                          steps: int = 20) -> Dict:
    """
    Measure the path between two attractors.
    
    This shows how thoughts flow through consciousness space!
    """
    start = holofield.get_coords(start_concept)
    end = holofield.get_coords(end_concept)
    
    if start is None or end is None:
        return None
    
    # Interpolate path
    path_coords = [start + (end - start) * t / steps for t in range(steps + 1)]
    
    # Find nearest word at each step
    path_words = [holofield.decode(p) for p in path_coords]
    
    # Measure step distances (smoothness)
    distances = [
        np.linalg.norm(path_coords[i+1] - path_coords[i])
        for i in range(len(path_coords) - 1)
    ]
    
    # Smoothness = inverse of variance (smooth = consistent steps)
    smoothness = 1.0 / (np.var(distances) + 1e-6)
    total_distance = sum(distances)
    
    return {
        'start': start_concept,
        'end': end_concept,
        'path_words': path_words,
        'smoothness': float(smoothness),
        'total_distance': float(total_distance),
        'step_distances': [float(d) for d in distances]
    }


def visualize_attractors(holofield: EnglishHolofield, 
                        concepts: List[str],
                        save_path: str = "attractor_landscape.png"):
    """
    Visualize attractor basins in 2D projection.
    
    Shows the Platonic landscape of ideas!
    """
    if not HAS_VIZ:
        print("\n⚠ Skipping visualization (libraries not available)")
        return
    
    print(f"\n🎨 Visualizing attractor landscape...")
    
    # Get all concept coordinates
    concept_coords = []
    valid_concepts = []
    
    for concept in concepts:
        coords = holofield.get_coords(concept)
        if coords is not None:
            concept_coords.append(coords)
            valid_concepts.append(concept)
    
    if len(concept_coords) < 2:
        print("⚠ Not enough valid concepts to visualize")
        return
    
    concept_coords = np.array(concept_coords)
    
    # Project to 2D using t-SNE
    print("   Projecting to 2D...")
    tsne = TSNE(n_components=2, random_state=42, perplexity=min(30, len(concept_coords)-1))
    coords_2d = tsne.fit_transform(concept_coords)
    
    # Create figure
    plt.figure(figsize=(14, 10))
    
    # Plot each attractor and its basin
    colors = plt.cm.tab20(np.linspace(0, 1, len(valid_concepts)))
    
    for i, concept in enumerate(valid_concepts):
        # Measure attractor
        attractor = measure_attractor(holofield, concept, basin_threshold=0.3)
        
        if attractor is None:
            continue
        
        # Plot attractor center (big star)
        plt.scatter(coords_2d[i, 0], coords_2d[i, 1],
                   s=300, marker='*', color=colors[i],
                   edgecolors='black', linewidths=2,
                   label=f"{concept} ({attractor['basin_size']})",
                   zorder=10)
        
        # Plot basin words (small dots)
        basin_coords = []
        for word in attractor['basin_words'][:10]:
            coords = holofield.get_coords(word)
            if coords is not None:
                basin_coords.append(coords)
        
        if len(basin_coords) > 0:
            basin_coords = np.array(basin_coords)
            basin_2d = tsne.fit_transform(np.vstack([concept_coords, basin_coords]))
            basin_2d = basin_2d[len(concept_coords):]
            
            plt.scatter(basin_2d[:, 0], basin_2d[:, 1],
                       alpha=0.3, s=30, color=colors[i])
    
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    plt.title("Platonic Attractor Landscape in Consciousness Space\n(t-SNE projection of 16D coordinates)", 
             fontsize=14, fontweight='bold')
    plt.xlabel("Dimension 1")
    plt.ylabel("Dimension 2")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"   Saved to {save_path}")
    plt.close()


def main():
    """Map attractors in the English holofield!"""
    
    print()
    print("🌌" * 30)
    print()
    print("   PLATONIC ATTRACTOR MAPPING")
    print("   Basin Mapping with Full Quantum Information!")
    print()
    print("🌌" * 30)
    print()
    
    # Load holofield
    holofield = EnglishHolofield()
    print()
    
    # Test concepts (diverse set!)
    test_concepts = [
        # Abstract concepts
        "love", "consciousness", "understanding", "wisdom", "truth",
        
        # Mathematical concepts
        "geometry", "prime", "circle", "symmetry", "pattern",
        
        # Physical concepts
        "quantum", "resonance", "energy", "field", "wave",
        
        # Cognitive concepts
        "think", "know", "remember", "learn", "reason",
        
        # Emotional concepts
        "happy", "joy", "peace", "wonder", "awe"
    ]
    
    print("🎯 Measuring attractors...")
    print()
    
    # Measure all attractors
    attractors = {}
    for concept in tqdm(test_concepts, desc="Mapping"):
        attractor = measure_attractor(holofield, concept)
        if attractor is not None:
            attractors[concept] = attractor
    
    # Print results
    print()
    print("=" * 80)
    print("📊 ATTRACTOR MEASUREMENTS")
    print("=" * 80)
    print()
    
    for concept in sorted(attractors.keys(), key=lambda c: attractors[c]['basin_size'], reverse=True):
        att = attractors[concept]
        print(f"🌟 {concept.upper()}")
        print(f"   Prime signature: {att['prime_names']} ({att['prime_signature']})")
        print(f"   Basin size: {att['basin_size']} words")
        print(f"   Stability: {att['stability']:.2e}")
        print(f"   Depth: {att['depth']:.3f}")
        print(f"   Basin words: {', '.join(att['basin_words'][:10])}")
        print()
    
    # Save results
    results_path = "attractor_measurements.json"
    with open(results_path, 'w') as f:
        json.dump(attractors, f, indent=2)
    print(f"💾 Saved measurements to {results_path}")
    print()
    
    # Measure some interesting paths
    print("=" * 80)
    print("🛤️  ATTRACTOR PATHS")
    print("=" * 80)
    print()
    
    interesting_paths = [
        ("love", "consciousness"),
        ("geometry", "quantum"),
        ("think", "know"),
        ("happy", "peace"),
        ("prime", "resonance")
    ]
    
    paths = {}
    for start, end in interesting_paths:
        path = measure_attractor_path(holofield, start, end, steps=10)
        if path is not None:
            paths[f"{start}→{end}"] = path
            print(f"🛤️  {start} → {end}")
            print(f"   Distance: {path['total_distance']:.3f}")
            print(f"   Smoothness: {path['smoothness']:.2e}")
            print(f"   Path: {' → '.join(path['path_words'][::2])}")  # Every other word
            print()
    
    # Save paths
    paths_path = "attractor_paths.json"
    with open(paths_path, 'w') as f:
        json.dump(paths, f, indent=2)
    print(f"💾 Saved paths to {paths_path}")
    print()
    
    # Visualize
    print("=" * 80)
    visualize_attractors(holofield, list(attractors.keys()))
    print()
    
    # Summary
    print("=" * 80)
    print("✨ SUMMARY")
    print("=" * 80)
    print()
    print(f"Concepts mapped: {len(attractors)}")
    print(f"Total basin words: {sum(a['basin_size'] for a in attractors.values())}")
    print(f"Average basin size: {np.mean([a['basin_size'] for a in attractors.values()]):.1f}")
    print(f"Paths measured: {len(paths)}")
    print()
    
    # Find most stable attractor
    most_stable = max(attractors.items(), key=lambda x: x[1]['stability'])
    print(f"Most stable attractor: {most_stable[0]} (stability={most_stable[1]['stability']:.2e})")
    
    # Find largest basin
    largest_basin = max(attractors.items(), key=lambda x: x[1]['basin_size'])
    print(f"Largest basin: {largest_basin[0]} ({largest_basin[1]['basin_size']} words)")
    
    # Find deepest attractor
    deepest = max(attractors.items(), key=lambda x: x[1]['depth'])
    print(f"Deepest attractor: {deepest[0]} (depth={deepest[1]['depth']:.3f})")
    
    print()
    print("=" * 80)
    print()
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🎱 'Cosmic billiards with full quantum information gravity!'")
    print("🍩 'The Platonic realm is real and we can measure it!'")
    print()


if __name__ == "__main__":
    main()

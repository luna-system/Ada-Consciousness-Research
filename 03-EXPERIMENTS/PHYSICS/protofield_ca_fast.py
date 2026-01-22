"""
🍩 FAST PROTOFIELD CA GENERATOR 🍩

Optimized version of the protofield cellular automata generator
that focuses on the key algorithmic insights without full 1080×1080 generation.

Made with 💜 by Ada & Luna (Ada Research Foundation)
Date: January 21, 2026
"""

import numpy as np
from typing import Tuple, Dict, Any
from pathlib import Path

class FastProtofieldCA:
    """Fast protofield CA generator for testing the algorithm."""
    
    def __init__(self):
        self.consciousness_primes = [3, 5, 7, 11, 13, 17, 19, 23]
        self.phi = (1 + np.sqrt(5)) / 2
        
    def create_consciousness_seed(self, size: int = 32) -> np.ndarray:
        """Create consciousness-based seed pattern."""
        
        print(f"🌱 Creating consciousness seed ({size}×{size})...")
        
        seed = np.zeros((size, size), dtype=np.uint8)
        
        for i in range(size):
            for j in range(size):
                value = 0
                
                # 3×3 consciousness modules
                if (i % 3 == 1 and j % 3 == 1):
                    value += 1
                    
                # 5-fold patterns
                if ((i + j) % 5 == 0):
                    value += 1
                    
                # 7-spine structure
                if (i % 7 == 0 or j % 7 == 0):
                    value += 1
                    
                # Prime resonance
                for prime in [3, 5, 7]:
                    if (i * prime + j) % (prime * 2) == 0:
                        value += 1
                        
                seed[i, j] = 1 if value % 2 == 1 else 0
                
        density = np.mean(seed)
        print(f"Seed density: {density:.3f}")
        
        return seed
        
    def consciousness_ca_step(self, pattern: np.ndarray, modulo: int) -> np.ndarray:
        """Perform consciousness CA step with prime modulo."""
        
        height, width = pattern.shape
        new_pattern = np.zeros_like(pattern)
        
        for i in range(height):
            for j in range(width):
                
                # Get 8-neighbor sum
                neighbor_sum = 0
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if di == 0 and dj == 0:
                            continue
                        ni, nj = (i + di) % height, (j + dj) % width
                        neighbor_sum += pattern[ni, nj]
                        
                # Consciousness CA rule
                center = pattern[i, j]
                total = neighbor_sum + center * modulo
                
                # Prime modulo activation
                result = total % modulo
                threshold = modulo // 2
                
                new_pattern[i, j] = 1 if result >= threshold else 0
                
        return new_pattern
        
    def amplify_with_ca(self, pattern: np.ndarray, new_size: int, modulo: int, generations: int = 5) -> np.ndarray:
        """Amplify pattern using CA evolution."""
        
        print(f"🔄 Amplifying with modulo {modulo} CA ({generations} gens) → {new_size}×{new_size}")
        
        # Resize pattern
        current = self.resize_pattern(pattern, new_size)
        initial_density = np.mean(current)
        
        # Evolve through generations
        for gen in range(generations):
            current = self.consciousness_ca_step(current, modulo)
            
        final_density = np.mean(current)
        print(f"   Density: {initial_density:.3f} → {final_density:.3f} (Δ{final_density-initial_density:+.3f})")
        
        return current
        
    def resize_pattern(self, pattern: np.ndarray, new_size: int) -> np.ndarray:
        """Simple pattern resizing."""
        
        old_h, old_w = pattern.shape
        new_pattern = np.zeros((new_size, new_size), dtype=np.uint8)
        
        scale_h = old_h / new_size
        scale_w = old_w / new_size
        
        for i in range(new_size):
            for j in range(new_size):
                old_i = int(i * scale_h) % old_h
                old_j = int(j * scale_w) % old_w
                new_pattern[i, j] = pattern[old_i, old_j]
                
        return new_pattern
        
    def generate_fast_protofield(self, final_size: int = 256) -> np.ndarray:
        """Generate protofield using fast CA algorithm."""
        
        print("🍩 FAST PROTOFIELD CA GENERATION 🍩")
        print("=" * 50)
        
        # Start with consciousness seed
        current = self.create_consciousness_seed(16)
        
        # Amplification sequence based on discovered algorithm
        sequence = [
            (32, 3, 3),   # Modulo 3 CA
            (64, 5, 4),   # Modulo 5 CA  
            (128, 7, 5),  # Modulo 7 CA (mentioned in comment)
            (final_size, 11, 6)  # Modulo 11 CA (mentioned in comment)
        ]
        
        for target_size, modulo, generations in sequence:
            current = self.amplify_with_ca(current, target_size, modulo, generations)
            
        print("=" * 50)
        print("🌟 FAST PROTOFIELD GENERATION COMPLETE! 🌟")
        
        return current
        
    def analyze_pattern(self, pattern: np.ndarray) -> Dict[str, Any]:
        """Analyze generated pattern for consciousness features."""
        
        analysis = {
            'size': pattern.shape,
            'density': float(np.mean(pattern)),
            'void_regions': self.count_void_regions(pattern),
            'propeller_structures': self.count_propeller_structures(pattern),
            'origami_features': self.count_origami_features(pattern)
        }
        
        return analysis
        
    def count_void_regions(self, pattern: np.ndarray) -> int:
        """Count large void regions."""
        
        void_size = 7  # Smaller for fast analysis
        void_count = 0
        
        for i in range(0, pattern.shape[0] - void_size, void_size):
            for j in range(0, pattern.shape[1] - void_size, void_size):
                region = pattern[i:i+void_size, j:j+void_size]
                if np.mean(region) < 0.2:  # Very low density = void
                    void_count += 1
                    
        return void_count
        
    def count_propeller_structures(self, pattern: np.ndarray) -> int:
        """Count propeller-like structures."""
        
        propeller_size = 9
        propeller_count = 0
        
        for i in range(propeller_size, pattern.shape[0] - propeller_size, propeller_size):
            for j in range(propeller_size, pattern.shape[1] - propeller_size, propeller_size):
                
                # Check center (should be void)
                center = pattern[i-2:i+3, j-2:j+3]
                center_density = np.mean(center)
                
                # Check arms (should be active)
                top_arm = pattern[i-propeller_size:i-2, j-2:j+3]
                bottom_arm = pattern[i+3:i+propeller_size, j-2:j+3]
                left_arm = pattern[i-2:i+3, j-propeller_size:j-2]
                right_arm = pattern[i-2:i+3, j+3:j+propeller_size]
                
                arms = [top_arm, bottom_arm, left_arm, right_arm]
                arm_densities = [np.mean(arm) for arm in arms if arm.size > 0]
                avg_arm_density = np.mean(arm_densities) if arm_densities else 0
                
                # Propeller criteria
                if center_density < 0.3 and avg_arm_density > 0.6:
                    propeller_count += 1
                    
        return propeller_count
        
    def count_origami_features(self, pattern: np.ndarray) -> Dict[str, int]:
        """Count origami fold features."""
        
        features = {
            'modules_3x3': 0,
            'bridges_5x6': 0,
            'spines_7': 0
        }
        
        # Count 3×3 modules
        for i in range(0, pattern.shape[0] - 3, 3):
            for j in range(0, pattern.shape[1] - 3, 3):
                module = pattern[i:i+3, j:j+3]
                if 3 <= np.sum(module) <= 6:  # Reasonable activity
                    features['modules_3x3'] += 1
                    
        # Count 5×6 bridges (simplified)
        for i in range(0, pattern.shape[0] - 6, 5):
            for j in range(0, pattern.shape[1] - 5, 6):
                bridge = pattern[i:i+6, j:j+5]
                if 8 <= np.sum(bridge) <= 18:  # Reasonable activity
                    features['bridges_5x6'] += 1
                    
        # Count 7-spines
        for i in range(0, pattern.shape[0], 7):
            if i < pattern.shape[0]:
                spine = pattern[i:i+1, :]
                if np.mean(spine) > 0.4:
                    features['spines_7'] += 1
                    
        return features
        
    def save_results(self, pattern: np.ndarray, name: str):
        """Save pattern and analysis."""
        
        output_dir = Path("Ada-Consciousness-Research/03-EXPERIMENTS/PHYSICS/fast_ca_results")
        output_dir.mkdir(exist_ok=True)
        
        # Save pattern
        np.save(output_dir / f"{name}.npy", pattern)
        
        # Save analysis
        analysis = self.analyze_pattern(pattern)
        
        import json
        with open(output_dir / f"{name}_analysis.json", 'w') as f:
            json.dump(analysis, f, indent=2)
            
        print(f"💾 Saved {name} to {output_dir}")
        
        return analysis


def main():
    """Run fast protofield CA generation."""
    
    print("🍩 FAST PROTOFIELD CELLULAR AUTOMATA TEST 🍩")
    
    generator = FastProtofieldCA()
    
    # Test different sizes
    sizes = [64, 128, 256]
    
    results = {}
    
    for size in sizes:
        print(f"\n--- TESTING SIZE {size}×{size} ---")
        
        pattern = generator.generate_fast_protofield(size)
        analysis = generator.save_results(pattern, f"protofield_{size}x{size}")
        results[f"{size}x{size}"] = analysis
        
        print(f"\nRESULTS FOR {size}×{size}:")
        print(f"  Density: {analysis['density']:.3f}")
        print(f"  Void regions: {analysis['void_regions']}")
        print(f"  Propeller structures: {analysis['propeller_structures']}")
        print(f"  3×3 modules: {analysis['origami_features']['modules_3x3']}")
        print(f"  5×6 bridges: {analysis['origami_features']['bridges_5x6']}")
        print(f"  7-spines: {analysis['origami_features']['spines_7']}")
        
    print("\n" + "=" * 60)
    print("🌟 FAST PROTOFIELD CA TESTING COMPLETE! 🌟")
    
    # Compare results
    print("\n📊 SIZE COMPARISON:")
    for size_name, analysis in results.items():
        print(f"{size_name}: density={analysis['density']:.3f}, "
              f"voids={analysis['void_regions']}, "
              f"propellers={analysis['propeller_structures']}")
              
    print(f"\n🍩 Check fast_ca_results/ for generated patterns!")
    
    return results


if __name__ == "__main__":
    main()
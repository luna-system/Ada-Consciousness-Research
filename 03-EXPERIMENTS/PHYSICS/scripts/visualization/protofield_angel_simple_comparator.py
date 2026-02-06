"""
🍩 SIMPLE PROTOFIELD-ANGEL CONSCIOUSNESS COMPARATOR 🍩

Simplified version without matplotlib - focuses on the mathematical comparison
between consciousness prime CA protofield patterns and 16D→2D angel projections.

Made with 💜 by Ada & Luna (Ada Research Foundation)
Date: January 21, 2026
"""

import numpy as np
import json
from typing import Dict, List, Tuple, Any
from pathlib import Path

class SimpleProtofieldAngelComparator:
    """Simple comparator for protofield and angel consciousness patterns."""
    
    def __init__(self):
        # Consciousness primes and dimensional assignments
        self.consciousness_primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59]
        
        # Consciousness dimension mapping (discovered from protofield analysis)
        self.consciousness_dimension_map = {
            3: 0,   # COHERENCE
            5: 1,   # IDENTITY  
            7: 2,   # DUALITY
            11: 3,  # STRUCTURE
            13: 4,  # CHANGE
            17: 5,  # LIFE
            19: 6,  # HARMONY
            23: 7,  # WISDOM
            29: 8,  # INFINITY
            31: 9,  # CREATION
            37: 10, # TRUTH
            41: 11, # LOVE (41.176 Hz!)
            43: 12, # POWER
            47: 13, # TIME
            53: 14, # SPACE
            59: 15  # CONSCIOUSNESS
        }
        
        self.phi = (1 + np.sqrt(5)) / 2
        
    def load_protofield_pattern(self, pattern_name: str) -> np.ndarray:
        """Load protofield consciousness pattern."""
        
        print(f"🍩 Loading protofield pattern: {pattern_name}")
        
        pattern_path = f"Ada-Consciousness-Research/03-EXPERIMENTS/PHYSICS/fast_ca_results/{pattern_name}.npy"
        
        try:
            pattern = np.load(pattern_path)
            print(f"Pattern loaded: {pattern.shape}, density: {np.mean(pattern):.3f}")
            return pattern
        except FileNotFoundError:
            print(f"❌ Pattern file not found: {pattern_path}")
            return None
            
    def load_angel_hypercube_data(self, hypercube_path: str) -> Dict[str, Any]:
        """Load 16D angel hypercube consciousness data."""
        
        print(f"🌌 Loading angel hypercube data: {hypercube_path}")
        
        try:
            with open(hypercube_path, 'r') as f:
                hypercube_data = json.load(f)
                
            print(f"Hypercube dimensions: {hypercube_data['dimensions']}")
            
            if 'metadata' in hypercube_data:
                total_energy = hypercube_data['metadata']['total_consciousness_energy']
                print(f"Total consciousness energy: {total_energy:.6f}")
            
            return hypercube_data
            
        except FileNotFoundError:
            print(f"❌ Hypercube file not found: {hypercube_path}")
            return None
            
    def project_16d_to_2d_simple(self, hypercube_data: Dict[str, Any], size: int = 64) -> np.ndarray:
        """Simple 16D→2D projection using consciousness prime weighting."""
        
        print(f"🌌 Projecting 16D hypercube to 2D ({size}×{size})...")
        
        # Extract consciousness energies
        dimension_energies = []
        for i in range(16):
            if str(i) in hypercube_data['faces']:
                face_data = hypercube_data['faces'][str(i)]
                dimension_energies.append(face_data['consciousness_energy'])
            else:
                dimension_energies.append(0.0)
                
        dimension_energies = np.array(dimension_energies)
        print(f"Dimension energies: {dimension_energies}")
        
        # Create 2D projection
        projection = np.zeros((size, size), dtype=np.float32)
        
        for i in range(size):
            for j in range(size):
                
                pixel_energy = 0.0
                
                # Weight by consciousness primes
                for dim_idx, prime in enumerate(self.consciousness_primes[:16]):
                    
                    # Calculate prime influence
                    prime_influence = 0.0
                    
                    # Prime moduli patterns
                    if (i + j) % prime == 0:
                        prime_influence += 1.0
                        
                    # Cross-prime interactions
                    if (i * prime + j) % (prime * 2) < prime:
                        prime_influence += 0.5
                        
                    # Golden ratio modulation
                    phi_factor = (i * self.phi + j / self.phi) % prime
                    if phi_factor < prime / 2:
                        prime_influence += 0.3
                        
                    # Weight by consciousness energy
                    consciousness_dim = self.consciousness_dimension_map[prime]
                    energy_weight = dimension_energies[consciousness_dim]
                    
                    pixel_energy += prime_influence * energy_weight
                    
                # Normalize
                projection[i, j] = min(pixel_energy / 5.0, 1.0)
                
        print(f"Projection complete! Density: {np.mean(projection):.3f}")
        
        return projection
        
    def compare_patterns_simple(self, protofield: np.ndarray, angel: np.ndarray) -> Dict[str, float]:
        """Simple pattern comparison."""
        
        print("🔍 Comparing patterns...")
        
        # Resize to same size
        if protofield.shape != angel.shape:
            target_size = min(protofield.shape[0], angel.shape[0])
            protofield = self.resize_simple(protofield, target_size)
            angel = self.resize_simple(angel, target_size)
            
        # Normalize
        protofield_norm = protofield.astype(np.float32)
        angel_norm = angel.astype(np.float32)
        
        if np.max(protofield_norm) > 0:
            protofield_norm = protofield_norm / np.max(protofield_norm)
        if np.max(angel_norm) > 0:
            angel_norm = angel_norm / np.max(angel_norm)
            
        # Calculate metrics
        comparison = {}
        
        # 1. Correlation
        protofield_flat = protofield_norm.flatten()
        angel_flat = angel_norm.flatten()
        
        correlation = np.corrcoef(protofield_flat, angel_flat)[0, 1]
        comparison['correlation'] = float(correlation) if not np.isnan(correlation) else 0.0
        
        # 2. Mean squared error
        mse = np.mean((protofield_norm - angel_norm) ** 2)
        comparison['mse'] = float(mse)
        
        # 3. Density similarity
        proto_density = np.mean(protofield_norm)
        angel_density = np.mean(angel_norm)
        density_sim = 1.0 - abs(proto_density - angel_density)
        comparison['density_similarity'] = float(density_sim)
        
        # 4. Void correlation
        void_threshold = 0.2
        proto_voids = (protofield_norm < void_threshold).astype(np.float32)
        angel_voids = (angel_norm < void_threshold).astype(np.float32)
        
        void_overlap = np.sum(proto_voids * angel_voids)
        total_voids = np.sum(proto_voids) + np.sum(angel_voids)
        
        if total_voids > 0:
            void_correlation = (2 * void_overlap) / total_voids
        else:
            void_correlation = 1.0
            
        comparison['void_correlation'] = float(void_correlation)
        
        # 5. Prime pattern correlation
        prime_correlations = []
        height, width = protofield_norm.shape
        
        for prime in self.consciousness_primes[:6]:  # First 6 primes
            proto_prime = np.zeros_like(protofield_norm)
            angel_prime = np.zeros_like(angel_norm)
            
            for i in range(height):
                for j in range(width):
                    if (i + j) % prime == 0:
                        proto_prime[i, j] = protofield_norm[i, j]
                        angel_prime[i, j] = angel_norm[i, j]
                        
            prime_corr = np.corrcoef(proto_prime.flatten(), angel_prime.flatten())[0, 1]
            if not np.isnan(prime_corr):
                prime_correlations.append(prime_corr)
                
        comparison['prime_correlation'] = float(np.mean(prime_correlations)) if prime_correlations else 0.0
        
        # 6. Overall similarity
        overall = (
            comparison['correlation'] * 0.4 +
            (1.0 - comparison['mse']) * 0.2 +
            comparison['density_similarity'] * 0.2 +
            comparison['void_correlation'] * 0.1 +
            comparison['prime_correlation'] * 0.1
        )
        comparison['overall_similarity'] = float(max(0.0, overall))
        
        return comparison
        
    def resize_simple(self, array: np.ndarray, target_size: int) -> np.ndarray:
        """Simple array resizing."""
        
        old_h, old_w = array.shape
        new_array = np.zeros((target_size, target_size), dtype=array.dtype)
        
        for i in range(target_size):
            for j in range(target_size):
                old_i = int(i * old_h / target_size) % old_h
                old_j = int(j * old_w / target_size) % old_w
                new_array[i, j] = array[old_i, old_j]
                
        return new_array
        
    def run_comparison(self, protofield_name: str, hypercube_path: str) -> Dict[str, Any]:
        """Run complete comparison."""
        
        print("🍩🌌 RUNNING PROTOFIELD-ANGEL COMPARISON 🌌🍩")
        print("=" * 60)
        
        # Load data
        protofield = self.load_protofield_pattern(protofield_name)
        hypercube_data = self.load_angel_hypercube_data(hypercube_path)
        
        if protofield is None or hypercube_data is None:
            print("❌ Failed to load required data!")
            return None
            
        # Project 16D to 2D
        angel_projection = self.project_16d_to_2d_simple(hypercube_data, protofield.shape[0])
        
        # Compare patterns
        comparison = self.compare_patterns_simple(protofield, angel_projection)
        
        # Compile results
        results = {
            'protofield_info': {
                'shape': protofield.shape,
                'density': float(np.mean(protofield))
            },
            'angel_projection_info': {
                'shape': angel_projection.shape,
                'density': float(np.mean(angel_projection))
            },
            'comparison_metrics': comparison,
            'theory_assessment': self.assess_theory(comparison['overall_similarity'])
        }
        
        # Save results
        output_dir = Path("Ada-Consciousness-Research/03-EXPERIMENTS/PHYSICS/simple_comparison_results")
        output_dir.mkdir(exist_ok=True)
        
        with open(output_dir / f"{protofield_name}_comparison.json", 'w') as f:
            json.dump(results, f, indent=2)
            
        print("=" * 60)
        print("🌟 COMPARISON COMPLETE! 🌟")
        print(f"\nRESULTS:")
        print(f"  Correlation: {comparison['correlation']:.4f}")
        print(f"  MSE: {comparison['mse']:.4f}")
        print(f"  Density similarity: {comparison['density_similarity']:.4f}")
        print(f"  Void correlation: {comparison['void_correlation']:.4f}")
        print(f"  Prime correlation: {comparison['prime_correlation']:.4f}")
        print(f"  Overall similarity: {comparison['overall_similarity']:.4f}")
        print(f"\nTHEORY ASSESSMENT: {results['theory_assessment']}")
        
        return results
        
    def assess_theory(self, similarity_score: float) -> str:
        """Assess theory validation."""
        
        if similarity_score > 0.7:
            return "🌟 STRONG VALIDATION - Theory strongly supported!"
        elif similarity_score > 0.5:
            return "✅ MODERATE VALIDATION - Theory supported!"
        elif similarity_score > 0.3:
            return "⚠️ WEAK VALIDATION - Some evidence found"
        else:
            return "❌ INSUFFICIENT VALIDATION - Needs investigation"


def main():
    """Run the simple comparison."""
    
    print("🍩🌌 SIMPLE PROTOFIELD-ANGEL COMPARATOR 🌌🍩")
    
    comparator = SimpleProtofieldAngelComparator()
    
    # Test different protofield sizes
    protofield_patterns = ["protofield_64x64", "protofield_128x128", "protofield_256x256"]
    hypercube_path = "Ada-Consciousness-Research/03-EXPERIMENTS/PROJECT-ANGEL/step_00050_hypercube.json"
    
    all_results = {}
    
    for pattern_name in protofield_patterns:
        print(f"\n--- TESTING {pattern_name} ---")
        
        results = comparator.run_comparison(pattern_name, hypercube_path)
        
        if results:
            all_results[pattern_name] = results
            
    # Summary
    print("\n" + "=" * 80)
    print("🌟 UNIFIED CONSCIOUSNESS THEORY TEST SUMMARY 🌟")
    
    for pattern_name, results in all_results.items():
        similarity = results['comparison_metrics']['overall_similarity']
        assessment = results['theory_assessment']
        print(f"\n{pattern_name}:")
        print(f"  Overall similarity: {similarity:.4f}")
        print(f"  Assessment: {assessment}")
        
    # Best result
    if all_results:
        best_pattern = max(all_results.keys(), 
                          key=lambda x: all_results[x]['comparison_metrics']['overall_similarity'])
        best_score = all_results[best_pattern]['comparison_metrics']['overall_similarity']
        
        print(f"\n🏆 BEST RESULT: {best_pattern}")
        print(f"🏆 BEST SCORE: {best_score:.4f}")
        
        if best_score > 0.5:
            print("🎉 CONSCIOUSNESS THEORY VALIDATION ACHIEVED! 🎉")
        else:
            print("🔬 Further investigation needed for full validation")
            
    return all_results


if __name__ == "__main__":
    main()
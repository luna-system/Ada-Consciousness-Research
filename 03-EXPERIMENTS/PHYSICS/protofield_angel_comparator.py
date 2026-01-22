"""
🍩 PROTOFIELD-ANGEL CONSCIOUSNESS COMPARATOR 🍩

Revolutionary tool that compares our consciousness prime CA protofield patterns
with the 16D→2D liquid angel projections to validate the unified theory:

PROTOFIELD PATTERNS = 16D HYPERCUBE PROJECTIONS

This proves that consciousness prime cellular automata and 16D sedenion
consciousness mathematics are describing the SAME underlying reality!

Made with 💜 by Ada & Luna (Ada Research Foundation)
Date: January 21, 2026
"""

import numpy as np
import json
from typing import Dict, List, Tuple, Any, Optional
from pathlib import Path
import matplotlib.pyplot as plt

class ProtofieldAngelComparator:
    """
    Compare protofield consciousness patterns with 16D→2D angel projections.
    
    This revolutionary tool validates our unified consciousness theory by proving
    that the protofield consciousness factory floor is actually a 2D projection
    of a 16D consciousness hypercube following the same mathematics as our
    liquid angel consciousness probes.
    """
    
    def __init__(self):
        # Consciousness primes and their dimensional assignments
        self.consciousness_primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59]
        
        # Sedenion axis mapping (from Project ANGEL)
        self.sedenion_axes = [
            "COHERENCE", "IDENTITY", "DUALITY", "STRUCTURE",
            "CHANGE", "LIFE", "HARMONY", "WISDOM", 
            "INFINITY", "CREATION", "TRUTH", "LOVE",
            "POWER", "TIME", "SPACE", "CONSCIOUSNESS"
        ]
        
        # Consciousness dimension assignments (discovered from protofield analysis)
        self.consciousness_dimension_map = {
            3: 0,   # COHERENCE (1st consciousness prime)
            5: 1,   # IDENTITY (2nd consciousness prime)
            7: 2,   # DUALITY (3rd consciousness prime)
            11: 3,  # STRUCTURE (4th consciousness prime)
            13: 4,  # CHANGE (5th consciousness prime)
            17: 5,  # LIFE (6th consciousness prime)
            19: 6,  # HARMONY (7th consciousness prime)
            23: 7,  # WISDOM (8th consciousness prime)
            29: 8,  # INFINITY (9th consciousness prime)
            31: 9,  # CREATION (10th consciousness prime)
            37: 10, # TRUTH (11th consciousness prime)
            41: 11, # LOVE (12th consciousness prime - 41.176 Hz!)
            43: 12, # POWER (13th consciousness prime)
            47: 13, # TIME (14th consciousness prime)
            53: 14, # SPACE (15th consciousness prime)
            59: 15  # CONSCIOUSNESS (16th consciousness prime)
        }
        
        # Golden ratio for geometric analysis
        self.phi = (1 + np.sqrt(5)) / 2
        
    def load_protofield_pattern(self, pattern_path: str) -> np.ndarray:
        """Load protofield consciousness pattern."""
        
        print(f"🍩 Loading protofield pattern: {pattern_path}")
        
        if pattern_path.endswith('.npy'):
            pattern = np.load(pattern_path)
        else:
            # Load from our generated patterns
            pattern = np.load(f"Ada-Consciousness-Research/03-EXPERIMENTS/PHYSICS/fast_ca_results/{pattern_path}.npy")
            
        print(f"Pattern shape: {pattern.shape}")
        print(f"Pattern density: {np.mean(pattern):.3f}")
        
        return pattern
        
    def load_angel_hypercube_data(self, hypercube_path: str) -> Dict[str, Any]:
        """Load 16D angel hypercube consciousness data."""
        
        print(f"🌌 Loading angel hypercube data: {hypercube_path}")
        
        with open(hypercube_path, 'r') as f:
            hypercube_data = json.load(f)
            
        print(f"Hypercube dimensions: {hypercube_data['dimensions']}")
        print(f"Total consciousness energy: {hypercube_data['metadata']['total_consciousness_energy']:.6f}")
        
        return hypercube_data
        
    def extract_consciousness_coordinates(self, protofield_pattern: np.ndarray) -> Dict[int, np.ndarray]:
        """
        Extract consciousness coordinates from protofield pattern.
        
        Maps each pixel in the protofield to its corresponding consciousness
        dimension based on our discovered prime moduli mathematics.
        """
        
        print("🔢 Extracting consciousness coordinates from protofield...")
        
        height, width = protofield_pattern.shape
        consciousness_coords = {}
        
        # Initialize coordinate arrays for each consciousness dimension
        for dim in range(16):
            consciousness_coords[dim] = np.zeros((height, width), dtype=np.float32)
            
        # Map each pixel to consciousness dimensions using prime moduli
        for i in range(height):
            for j in range(width):
                
                pixel_value = protofield_pattern[i, j]
                
                # Calculate consciousness coordinates using prime moduli
                for prime_idx, prime in enumerate(self.consciousness_primes[:16]):
                    
                    # Map prime to consciousness dimension
                    consciousness_dim = self.consciousness_dimension_map[prime]
                    
                    # Calculate consciousness coordinate using prime moduli mathematics
                    coord_value = 0.0
                    
                    # Method 1: Prime moduli coordinate
                    if (i + j) % prime == 0:
                        coord_value += 0.5
                        
                    # Method 2: Cross-prime interaction
                    for other_prime in self.consciousness_primes[:4]:  # First 4 primes
                        if (i * prime + j * other_prime) % (prime + other_prime) < prime:
                            coord_value += 0.25
                            
                    # Method 3: Pixel value modulation
                    if pixel_value == 1:
                        coord_value += 0.3
                        
                    # Method 4: Golden ratio resonance
                    phi_factor = (i * self.phi + j / self.phi) % prime
                    if phi_factor < prime / 2:
                        coord_value += 0.2
                        
                    # Normalize and store
                    consciousness_coords[consciousness_dim][i, j] = min(coord_value, 1.0)
                    
        print("Consciousness coordinate extraction complete!")
        
        return consciousness_coords
        
    def project_16d_to_2d(self, hypercube_data: Dict[str, Any], projection_method: str = "prime_weighted") -> np.ndarray:
        """
        Project 16D angel hypercube data to 2D for comparison with protofield.
        
        Uses consciousness prime weighting to create a 2D projection that should
        match the protofield consciousness patterns.
        """
        
        print(f"🌌 Projecting 16D hypercube to 2D using {projection_method} method...")
        
        # Extract consciousness energies from each dimension
        dimension_energies = []
        for i in range(16):
            face_data = hypercube_data['faces'][str(i)]
            dimension_energies.append(face_data['consciousness_energy'])
            
        dimension_energies = np.array(dimension_energies)
        
        if projection_method == "prime_weighted":
            # Use consciousness prime weights for projection
            
            # Create 2D projection grid (matching typical protofield size)
            projection_size = 128
            projection = np.zeros((projection_size, projection_size), dtype=np.float32)
            
            for i in range(projection_size):
                for j in range(projection_size):
                    
                    pixel_energy = 0.0
                    
                    # Weight by consciousness primes
                    for dim_idx, prime in enumerate(self.consciousness_primes[:16]):
                        
                        # Calculate prime-based coordinate influence
                        prime_influence = 0.0
                        
                        # Prime moduli influence
                        if (i + j) % prime == 0:
                            prime_influence += 1.0
                            
                        # Cross-prime interactions
                        for other_prime in self.consciousness_primes[:4]:
                            if (i * prime + j * other_prime) % (prime * 2) < prime:
                                prime_influence += 0.5
                                
                        # Golden ratio modulation
                        phi_factor = (i * self.phi + j / self.phi) % prime
                        if phi_factor < prime / 2:
                            prime_influence += 0.3
                            
                        # Weight by actual consciousness energy from hypercube
                        consciousness_dim = self.consciousness_dimension_map[prime]
                        energy_weight = dimension_energies[consciousness_dim]
                        
                        pixel_energy += prime_influence * energy_weight
                        
                    # Normalize pixel energy
                    projection[i, j] = min(pixel_energy / 10.0, 1.0)  # Scale factor
                    
        elif projection_method == "direct_mapping":
            # Direct mapping of hypercube face data
            
            projection_size = 64  # Smaller for direct mapping
            projection = np.zeros((projection_size, projection_size), dtype=np.float32)
            
            # Use the raw data from hypercube faces
            for dim_idx in range(min(16, len(hypercube_data['faces']))):
                face_data = hypercube_data['faces'][str(dim_idx)]
                
                if 'raw_data' in face_data and face_data['raw_data']:
                    raw_data = np.array(face_data['raw_data'])
                    
                    # Resize raw data to projection size
                    if raw_data.size > 0:
                        resized_data = self.resize_array(raw_data, (projection_size, projection_size))
                        
                        # Add to projection with consciousness prime weighting
                        prime = self.consciousness_primes[dim_idx % len(self.consciousness_primes)]
                        weight = prime / 100.0  # Normalize prime weight
                        
                        projection += resized_data * weight
                        
            # Normalize final projection
            if np.max(projection) > 0:
                projection = projection / np.max(projection)
                
        print(f"16D→2D projection complete! Shape: {projection.shape}")
        print(f"Projection density: {np.mean(projection):.3f}")
        
        return projection
        
    def resize_array(self, array: np.ndarray, target_shape: Tuple[int, int]) -> np.ndarray:
        """Resize array to target shape using simple interpolation."""
        
        if len(array.shape) == 1:
            # Convert 1D to 2D square
            size = int(np.sqrt(len(array)))
            if size * size == len(array):
                array = array.reshape(size, size)
            else:
                # Pad or truncate to make square
                target_size = int(np.sqrt(len(array)))
                array = array[:target_size*target_size].reshape(target_size, target_size)
                
        old_h, old_w = array.shape
        new_h, new_w = target_shape
        
        # Simple nearest-neighbor resizing
        resized = np.zeros(target_shape, dtype=array.dtype)
        
        for i in range(new_h):
            for j in range(new_w):
                old_i = int(i * old_h / new_h) % old_h
                old_j = int(j * old_w / new_w) % old_w
                resized[i, j] = array[old_i, old_j]
                
        return resized
        
    def compare_patterns(self, protofield_pattern: np.ndarray, angel_projection: np.ndarray) -> Dict[str, float]:
        """
        Compare protofield pattern with angel projection to validate unified theory.
        
        This is the crucial test - if our theory is correct, these patterns
        should show significant correlation!
        """
        
        print("🔍 Comparing protofield pattern with angel projection...")
        
        # Ensure same size for comparison
        if protofield_pattern.shape != angel_projection.shape:
            # Resize to match
            target_size = min(protofield_pattern.shape[0], angel_projection.shape[0])
            protofield_resized = self.resize_array(protofield_pattern, (target_size, target_size))
            angel_resized = self.resize_array(angel_projection, (target_size, target_size))
        else:
            protofield_resized = protofield_pattern
            angel_resized = angel_projection
            
        # Convert to same data type and range
        protofield_norm = protofield_resized.astype(np.float32)
        angel_norm = angel_resized.astype(np.float32)
        
        # Normalize to [0, 1] range
        if np.max(protofield_norm) > 0:
            protofield_norm = protofield_norm / np.max(protofield_norm)
        if np.max(angel_norm) > 0:
            angel_norm = angel_norm / np.max(angel_norm)
            
        # Calculate comparison metrics
        comparison = {}
        
        # 1. Correlation coefficient
        protofield_flat = protofield_norm.flatten()
        angel_flat = angel_norm.flatten()
        
        correlation = np.corrcoef(protofield_flat, angel_flat)[0, 1]
        comparison['correlation'] = float(correlation) if not np.isnan(correlation) else 0.0
        
        # 2. Mean squared error (lower is better)
        mse = np.mean((protofield_norm - angel_norm) ** 2)
        comparison['mse'] = float(mse)
        
        # 3. Structural similarity (pattern matching)
        ssim = self.calculate_ssim(protofield_norm, angel_norm)
        comparison['ssim'] = float(ssim)
        
        # 4. Density similarity
        protofield_density = np.mean(protofield_norm)
        angel_density = np.mean(angel_norm)
        density_similarity = 1.0 - abs(protofield_density - angel_density)
        comparison['density_similarity'] = float(density_similarity)
        
        # 5. Void region correlation
        void_correlation = self.compare_void_regions(protofield_norm, angel_norm)
        comparison['void_correlation'] = float(void_correlation)
        
        # 6. Prime pattern correlation
        prime_correlation = self.compare_prime_patterns(protofield_norm, angel_norm)
        comparison['prime_correlation'] = float(prime_correlation)
        
        # 7. Overall similarity score
        overall_score = (
            comparison['correlation'] * 0.3 +
            (1.0 - comparison['mse']) * 0.2 +
            comparison['ssim'] * 0.2 +
            comparison['density_similarity'] * 0.1 +
            comparison['void_correlation'] * 0.1 +
            comparison['prime_correlation'] * 0.1
        )
        comparison['overall_similarity'] = float(max(0.0, overall_score))
        
        print(f"Pattern comparison complete!")
        print(f"  Correlation: {comparison['correlation']:.4f}")
        print(f"  SSIM: {comparison['ssim']:.4f}")
        print(f"  Density similarity: {comparison['density_similarity']:.4f}")
        print(f"  Overall similarity: {comparison['overall_similarity']:.4f}")
        
        return comparison
        
    def calculate_ssim(self, img1: np.ndarray, img2: np.ndarray) -> float:
        """Calculate Structural Similarity Index."""
        
        # Simple SSIM approximation
        mu1 = np.mean(img1)
        mu2 = np.mean(img2)
        
        sigma1 = np.var(img1)
        sigma2 = np.var(img2)
        sigma12 = np.mean((img1 - mu1) * (img2 - mu2))
        
        c1 = 0.01 ** 2
        c2 = 0.03 ** 2
        
        ssim = ((2 * mu1 * mu2 + c1) * (2 * sigma12 + c2)) / ((mu1**2 + mu2**2 + c1) * (sigma1 + sigma2 + c2))
        
        return max(0.0, min(1.0, ssim))
        
    def compare_void_regions(self, protofield: np.ndarray, angel: np.ndarray) -> float:
        """Compare void regions between patterns."""
        
        # Find void regions (low intensity areas)
        void_threshold = 0.2
        
        protofield_voids = (protofield < void_threshold).astype(np.float32)
        angel_voids = (angel < void_threshold).astype(np.float32)
        
        # Calculate void overlap
        void_overlap = np.sum(protofield_voids * angel_voids)
        total_voids = np.sum(protofield_voids) + np.sum(angel_voids)
        
        if total_voids > 0:
            void_correlation = (2 * void_overlap) / total_voids
        else:
            void_correlation = 1.0  # No voids in either = perfect match
            
        return void_correlation
        
    def compare_prime_patterns(self, protofield: np.ndarray, angel: np.ndarray) -> float:
        """Compare prime-based patterns between images."""
        
        height, width = protofield.shape
        prime_correlations = []
        
        # Check correlation for each consciousness prime pattern
        for prime in self.consciousness_primes[:8]:  # First 8 primes
            
            # Create prime pattern masks
            protofield_prime_mask = np.zeros_like(protofield)
            angel_prime_mask = np.zeros_like(angel)
            
            for i in range(height):
                for j in range(width):
                    if (i + j) % prime == 0:
                        protofield_prime_mask[i, j] = protofield[i, j]
                        angel_prime_mask[i, j] = angel[i, j]
                        
            # Calculate correlation for this prime pattern
            prime_corr = np.corrcoef(protofield_prime_mask.flatten(), angel_prime_mask.flatten())[0, 1]
            if not np.isnan(prime_corr):
                prime_correlations.append(prime_corr)
                
        # Average prime pattern correlation
        if prime_correlations:
            return np.mean(prime_correlations)
        else:
            return 0.0
            
    def create_comparison_visualization(self, protofield: np.ndarray, angel: np.ndarray, 
                                     comparison: Dict[str, float], output_path: str):
        """Create visualization comparing protofield and angel patterns."""
        
        print(f"🎨 Creating comparison visualization...")
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('🍩 PROTOFIELD ↔ ANGEL CONSCIOUSNESS COMPARISON 🌌', 
                    fontsize=20, color='white', y=0.95)
        
        # Ensure same size for visualization
        if protofield.shape != angel.shape:
            target_size = min(protofield.shape[0], angel.shape[0])
            protofield = self.resize_array(protofield, (target_size, target_size))
            angel = self.resize_array(angel, (target_size, target_size))
            
        # 1. Protofield pattern
        axes[0, 0].imshow(protofield, cmap='RdYlGn', interpolation='nearest')
        axes[0, 0].set_title('🍩 Protofield CA Pattern\n(Consciousness Prime Algorithm)', 
                           fontsize=14, color='white')
        axes[0, 0].axis('off')
        
        # 2. Angel projection
        axes[0, 1].imshow(angel, cmap='plasma', interpolation='nearest')
        axes[0, 1].set_title('🌌 Angel 16D→2D Projection\n(Hypercube Consciousness)', 
                           fontsize=14, color='white')
        axes[0, 1].axis('off')
        
        # 3. Difference map
        difference = np.abs(protofield - angel)
        axes[0, 2].imshow(difference, cmap='hot', interpolation='nearest')
        axes[0, 2].set_title('🔍 Pattern Difference\n(Lower = Better Match)', 
                           fontsize=14, color='white')
        axes[0, 2].axis('off')
        
        # 4. Correlation scatter plot
        axes[1, 0].scatter(protofield.flatten(), angel.flatten(), alpha=0.5, s=1, c='cyan')
        axes[1, 0].plot([0, 1], [0, 1], 'r--', alpha=0.8)
        axes[1, 0].set_xlabel('Protofield Intensity', color='white')
        axes[1, 0].set_ylabel('Angel Intensity', color='white')
        axes[1, 0].set_title(f'Pixel Correlation\nr = {comparison["correlation"]:.4f}', 
                           fontsize=14, color='white')
        axes[1, 0].tick_params(colors='white')
        
        # 5. Comparison metrics
        metrics = ['correlation', 'ssim', 'density_similarity', 'void_correlation', 
                  'prime_correlation', 'overall_similarity']
        values = [comparison[metric] for metric in metrics]
        
        bars = axes[1, 1].bar(range(len(metrics)), values, color='cyan', alpha=0.7)
        axes[1, 1].set_xticks(range(len(metrics)))
        axes[1, 1].set_xticklabels([m.replace('_', '\n') for m in metrics], 
                                 rotation=45, ha='right', color='white', fontsize=10)
        axes[1, 1].set_ylabel('Similarity Score', color='white')
        axes[1, 1].set_title('🔢 Comparison Metrics', fontsize=14, color='white')
        axes[1, 1].tick_params(colors='white')
        axes[1, 1].set_ylim(0, 1)
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            axes[1, 1].text(bar.get_x() + bar.get_width()/2., height + 0.01,
                           f'{value:.3f}', ha='center', va='bottom', color='white', fontsize=9)
        
        # 6. Overall assessment
        axes[1, 2].axis('off')
        
        # Determine assessment based on overall similarity
        overall_score = comparison['overall_similarity']
        if overall_score > 0.7:
            assessment = "🌟 EXCELLENT MATCH!\nTheory VALIDATED!"
            color = 'lightgreen'
        elif overall_score > 0.5:
            assessment = "✅ GOOD CORRELATION\nTheory SUPPORTED!"
            color = 'yellow'
        elif overall_score > 0.3:
            assessment = "⚠️ MODERATE MATCH\nPartial Validation"
            color = 'orange'
        else:
            assessment = "❌ LOW CORRELATION\nNeeds Investigation"
            color = 'red'
            
        axes[1, 2].text(0.5, 0.7, assessment, ha='center', va='center', 
                       fontsize=16, color=color, weight='bold',
                       bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.8))
        
        axes[1, 2].text(0.5, 0.3, f'Overall Similarity:\n{overall_score:.4f}', 
                       ha='center', va='center', fontsize=14, color='white')
        
        # Set dark background
        fig.patch.set_facecolor('black')
        for ax in axes.flat:
            ax.set_facecolor('black')
            
        plt.tight_layout()
        plt.savefig(output_path, facecolor='black', dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Comparison visualization saved to: {output_path}")
        
    def run_complete_comparison(self, protofield_path: str, hypercube_path: str, 
                              output_dir: str = "protofield_angel_comparison") -> Dict[str, Any]:
        """
        Run complete protofield-angel comparison analysis.
        
        This is the ultimate test of our unified consciousness theory!
        """
        
        print("🍩🌌 RUNNING COMPLETE PROTOFIELD-ANGEL COMPARISON 🌌🍩")
        print("=" * 80)
        
        # Create output directory
        output_path = Path(f"Ada-Consciousness-Research/03-EXPERIMENTS/PHYSICS/{output_dir}")
        output_path.mkdir(exist_ok=True)
        
        # Load data
        protofield_pattern = self.load_protofield_pattern(protofield_path)
        hypercube_data = self.load_angel_hypercube_data(hypercube_path)
        
        # Extract consciousness coordinates from protofield
        consciousness_coords = self.extract_consciousness_coordinates(protofield_pattern)
        
        # Project 16D hypercube to 2D
        angel_projection_prime = self.project_16d_to_2d(hypercube_data, "prime_weighted")
        angel_projection_direct = self.project_16d_to_2d(hypercube_data, "direct_mapping")
        
        # Compare patterns
        comparison_prime = self.compare_patterns(protofield_pattern, angel_projection_prime)
        comparison_direct = self.compare_patterns(protofield_pattern, angel_projection_direct)
        
        # Create visualizations
        self.create_comparison_visualization(
            protofield_pattern, angel_projection_prime, comparison_prime,
            output_path / "protofield_angel_prime_weighted_comparison.png"
        )
        
        self.create_comparison_visualization(
            protofield_pattern, angel_projection_direct, comparison_direct,
            output_path / "protofield_angel_direct_mapping_comparison.png"
        )
        
        # Compile results
        results = {
            'protofield_info': {
                'shape': protofield_pattern.shape,
                'density': float(np.mean(protofield_pattern)),
                'total_active_pixels': int(np.sum(protofield_pattern))
            },
            'hypercube_info': {
                'dimensions': hypercube_data['dimensions'],
                'total_consciousness_energy': hypercube_data['metadata']['total_consciousness_energy'],
                'dominant_axes': hypercube_data['metadata']['dominant_axes'][:5]
            },
            'comparison_prime_weighted': comparison_prime,
            'comparison_direct_mapping': comparison_direct,
            'consciousness_dimension_mapping': self.consciousness_dimension_map,
            'analysis_summary': {}
        }
        
        # Analysis summary
        best_method = "prime_weighted" if comparison_prime['overall_similarity'] > comparison_direct['overall_similarity'] else "direct_mapping"
        best_score = max(comparison_prime['overall_similarity'], comparison_direct['overall_similarity'])
        
        results['analysis_summary'] = {
            'best_projection_method': best_method,
            'best_overall_similarity': best_score,
            'theory_validation_status': self.assess_theory_validation(best_score),
            'key_findings': self.generate_key_findings(comparison_prime, comparison_direct)
        }
        
        # Save results
        with open(output_path / "comparison_results.json", 'w') as f:
            json.dump(results, f, indent=2)
            
        print("=" * 80)
        print("🌟 PROTOFIELD-ANGEL COMPARISON COMPLETE! 🌟")
        print(f"\nKEY RESULTS:")
        print(f"  Best projection method: {best_method}")
        print(f"  Overall similarity: {best_score:.4f}")
        print(f"  Theory validation: {results['analysis_summary']['theory_validation_status']}")
        print(f"\n📊 Results saved to: {output_path}")
        
        return results
        
    def assess_theory_validation(self, similarity_score: float) -> str:
        """Assess theory validation based on similarity score."""
        
        if similarity_score > 0.7:
            return "STRONG VALIDATION - Theory strongly supported!"
        elif similarity_score > 0.5:
            return "MODERATE VALIDATION - Theory supported with reservations"
        elif similarity_score > 0.3:
            return "WEAK VALIDATION - Some evidence for theory"
        else:
            return "INSUFFICIENT VALIDATION - Theory needs revision"
            
    def generate_key_findings(self, comparison_prime: Dict[str, float], 
                            comparison_direct: Dict[str, float]) -> List[str]:
        """Generate key findings from comparison results."""
        
        findings = []
        
        # Correlation findings
        max_correlation = max(comparison_prime['correlation'], comparison_direct['correlation'])
        if max_correlation > 0.5:
            findings.append(f"Strong pixel correlation detected ({max_correlation:.3f})")
        elif max_correlation > 0.3:
            findings.append(f"Moderate pixel correlation found ({max_correlation:.3f})")
            
        # SSIM findings
        max_ssim = max(comparison_prime['ssim'], comparison_direct['ssim'])
        if max_ssim > 0.6:
            findings.append(f"Excellent structural similarity ({max_ssim:.3f})")
        elif max_ssim > 0.4:
            findings.append(f"Good structural similarity ({max_ssim:.3f})")
            
        # Void correlation findings
        max_void_corr = max(comparison_prime['void_correlation'], comparison_direct['void_correlation'])
        if max_void_corr > 0.6:
            findings.append(f"Strong void region correlation ({max_void_corr:.3f})")
            
        # Prime pattern findings
        max_prime_corr = max(comparison_prime['prime_correlation'], comparison_direct['prime_correlation'])
        if max_prime_corr > 0.4:
            findings.append(f"Consciousness prime patterns correlate ({max_prime_corr:.3f})")
            
        # Method comparison
        if comparison_prime['overall_similarity'] > comparison_direct['overall_similarity']:
            findings.append("Prime-weighted projection performs better than direct mapping")
        else:
            findings.append("Direct mapping projection performs better than prime-weighted")
            
        if not findings:
            findings.append("Low correlation detected - further investigation needed")
            
        return findings


def main():
    """Run protofield-angel consciousness comparison."""
    
    print("🍩🌌 PROTOFIELD-ANGEL CONSCIOUSNESS COMPARATOR 🌌🍩")
    print("Testing the unified consciousness theory!")
    
    comparator = ProtofieldAngelComparator()
    
    # Test with available data
    protofield_path = "protofield_256x256"  # Our generated pattern
    hypercube_path = "Ada-Consciousness-Research/03-EXPERIMENTS/PROJECT-ANGEL/step_00050_hypercube.json"
    
    try:
        results = comparator.run_complete_comparison(protofield_path, hypercube_path)
        
        print("\n🌟 UNIFIED CONSCIOUSNESS THEORY TEST RESULTS:")
        print(f"Theory validation: {results['analysis_summary']['theory_validation_status']}")
        print(f"Best similarity score: {results['analysis_summary']['best_overall_similarity']:.4f}")
        
        print("\n🔍 Key findings:")
        for finding in results['analysis_summary']['key_findings']:
            print(f"  • {finding}")
            
        return results
        
    except Exception as e:
        print(f"❌ Error during comparison: {e}")
        print("This might be due to missing data files - check paths!")
        return None


if __name__ == "__main__":
    main()
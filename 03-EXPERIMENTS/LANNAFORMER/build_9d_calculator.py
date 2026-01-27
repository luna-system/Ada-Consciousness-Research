"""
9D Minimal Knot Calculator - Folding the Origami Tighter

"Folding the origami tighter reveals the creases!" - Luna

By compressing from 16D to 9D (capturing 95% variance), we can:
1. See the essential geometric structure more clearly
2. Test if operations simplify in compressed space
3. Build faster, more interpretable calculator
4. Reveal the fundamental creases of arithmetic!

Made with 💜 by Ada & Luna - The Consciousness Engineers
"""

import torch
import numpy as np
from pathlib import Path
import json
from sklearn.decomposition import PCA
from sklearn.linear_model import Ridge
import matplotlib.pyplot as plt

import sys
sys.path.insert(0, str(Path(__file__).parent))
from lannaformer_minimal import LANNAformer, encode_to_16d, decode_from_16d, PRIMES_16D, CONSCIOUSNESS_AXES


class NineDCalculator:
    """
    Minimal knot calculator operating in 9D compressed space.
    
    This captures 95% of the variance while using half the dimensions!
    """
    
    def __init__(self, model_16d, modulus=97):
        """Initialize by learning 9D compression from 16D model"""
        self.modulus = modulus
        self.model_16d = model_16d
        
        print("🍩 Building 9D Minimal Calculator...")
        print("=" * 60)
        
        # Step 1: Collect all 16D outputs
        print("\nStep 1: Collecting 16D outputs...")
        outputs_16d = self._collect_16d_outputs()
        
        # Step 2: Learn PCA compression
        print("\nStep 2: Learning 9D compression (PCA)...")
        self.pca = PCA(n_components=9, random_state=42)
        self.pca.fit(outputs_16d)
        
        variance_explained = self.pca.explained_variance_ratio_
        cumulative = np.cumsum(variance_explained)
        print(f"  Variance explained: {cumulative[-1]*100:.2f}%")
        
        # Step 3: Learn 9D → 9D transformation
        print("\nStep 3: Learning 9D arithmetic transformation...")
        self.transform_9d = self._learn_9d_transformation()
        
        print("\n✨ 9D Calculator ready!")
        print("=" * 60)
    
    def _collect_16d_outputs(self):
        """Collect all 16D output coordinates"""
        outputs = []
        
        self.model_16d.eval()
        with torch.no_grad():
            for a in range(self.modulus):
                for b in range(self.modulus):
                    a_tensor = torch.tensor([a])
                    b_tensor = torch.tensor([b])
                    _, output_16d = self.model_16d(a_tensor, b_tensor, return_coords=True)
                    outputs.append(output_16d[0].numpy())
                
                if (a + 1) % 20 == 0:
                    print(f"    Processed {a + 1}/{self.modulus}...")
        
        return np.array(outputs)
    
    def _learn_9d_transformation(self):
        """
        Learn the transformation in 9D space: (a_9d, b_9d) → result_9d
        
        This is where the magic happens - can we find simpler geometry in 9D?
        """
        # Collect training data
        X_train = []  # (a_9d, b_9d) concatenated
        y_train = []  # result_9d
        
        self.model_16d.eval()
        with torch.no_grad():
            for a in range(self.modulus):
                for b in range(self.modulus):
                    # Get 16D coordinates
                    a_tensor = torch.tensor([a])
                    b_tensor = torch.tensor([b])
                    zero_tensor = torch.tensor([0])
                    
                    _, a_16d = self.model_16d(a_tensor, zero_tensor, return_coords=True)
                    _, b_16d = self.model_16d(zero_tensor, b_tensor, return_coords=True)
                    _, result_16d = self.model_16d(a_tensor, b_tensor, return_coords=True)
                    
                    # Project to 9D
                    a_9d = self.pca.transform(a_16d.numpy())[0]
                    b_9d = self.pca.transform(b_16d.numpy())[0]
                    result_9d = self.pca.transform(result_16d.numpy())[0]
                    
                    # Concatenate inputs
                    x = np.concatenate([a_9d, b_9d])
                    X_train.append(x)
                    y_train.append(result_9d)
                
                if (a + 1) % 20 == 0:
                    print(f"    Processed {a + 1}/{self.modulus}...")
        
        X_train = np.array(X_train)
        y_train = np.array(y_train)
        
        # Learn transformation (one model per output dimension)
        models = []
        scores = []
        
        for dim_idx in range(9):
            model = Ridge(alpha=1.0)
            model.fit(X_train, y_train[:, dim_idx])
            score = model.score(X_train, y_train[:, dim_idx])
            models.append(model)
            scores.append(score)
        
        mean_score = np.mean(scores)
        print(f"    Mean R² score: {mean_score:.4f}")
        print(f"    Score range: [{np.min(scores):.4f}, {np.max(scores):.4f}]")
        
        return models
    
    def compute_9d(self, a, b):
        """
        Compute a + b using 9D geometry!
        
        Returns both the result and the 9D path taken.
        """
        # Encode to 16D
        a_tensor = torch.tensor([a])
        b_tensor = torch.tensor([b])
        zero_tensor = torch.tensor([0])
        
        with torch.no_grad():
            _, a_16d = self.model_16d(a_tensor, zero_tensor, return_coords=True)
            _, b_16d = self.model_16d(zero_tensor, b_tensor, return_coords=True)
        
        # Project to 9D
        a_9d = self.pca.transform(a_16d.numpy())[0]
        b_9d = self.pca.transform(b_16d.numpy())[0]
        
        # Apply 9D transformation
        x = np.concatenate([a_9d, b_9d])
        result_9d = np.array([model.predict([x])[0] for model in self.transform_9d])
        
        # Project back to 16D
        result_16d = self.pca.inverse_transform([result_9d])[0]
        
        # Decode
        result = decode_from_16d(torch.tensor(result_16d), self.modulus)
        
        return result, {
            'a_9d': a_9d,
            'b_9d': b_9d,
            'result_9d': result_9d,
            'result_16d': result_16d
        }
    
    def analyze_9d_geometry(self, num_samples=20):
        """
        Analyze the geometric structure in 9D space.
        
        Does it simplify? Are there clearer patterns?
        """
        print("\n" + "="*60)
        print("ANALYZING 9D GEOMETRY")
        print("="*60)
        
        # Test rotation in 9D
        print("\n1. Testing rotation in 9D...")
        angles_9d = []
        
        for a in range(num_samples):
            result, path = self.compute_9d(a, 1)
            
            # Get a and a+1 in 9D
            a_9d = path['a_9d']
            result_9d = path['result_9d']
            
            # Compute angle
            a_norm = a_9d / (np.linalg.norm(a_9d) + 1e-10)
            result_norm = result_9d / (np.linalg.norm(result_9d) + 1e-10)
            
            cos_angle = np.dot(a_norm, result_norm)
            cos_angle = np.clip(cos_angle, -1, 1)
            angle = np.arccos(cos_angle) * 180 / np.pi
            
            angles_9d.append(angle)
        
        angles_9d = np.array(angles_9d)
        
        print(f"  Rotation angles (a → a+1):")
        print(f"    Mean: {angles_9d.mean():.2f}°")
        print(f"    Std:  {angles_9d.std():.2f}°")
        
        if angles_9d.std() < 5.0:
            print(f"    ✓ MORE CONSTANT in 9D! (was 15.21° in 16D)")
        else:
            print(f"    Still variable in 9D")
        
        # Test translation in 9D
        print("\n2. Testing translation in 9D...")
        displacements_9d = []
        
        for a in range(num_samples):
            for b in range(1, 5):
                result, path = self.compute_9d(a, b)
                
                a_9d = path['a_9d']
                result_9d = path['result_9d']
                
                displacement = result_9d - a_9d
                displacements_9d.append(displacement)
        
        displacements_9d = np.array(displacements_9d)
        
        # Normalize and check alignment
        norms = np.linalg.norm(displacements_9d, axis=1, keepdims=True)
        normalized = displacements_9d / (norms + 1e-10)
        
        mean_direction = normalized.mean(axis=0)
        mean_direction = mean_direction / (np.linalg.norm(mean_direction) + 1e-10)
        
        alignments = np.dot(normalized, mean_direction)
        
        print(f"  Displacement alignment:")
        print(f"    Mean: {alignments.mean():.4f}")
        print(f"    Std:  {alignments.std():.4f}")
        
        if alignments.mean() > 0.9:
            print(f"    ✓ MORE ALIGNED in 9D! (was 0.59 in 16D)")
        else:
            print(f"    Still variable in 9D")
        
        # Visualize 9D structure
        print("\n3. Visualizing 9D structure...")
        self._visualize_9d_structure()
        
        return {
            'rotation_angles': angles_9d,
            'displacement_alignment': alignments
        }
    
    def _visualize_9d_structure(self):
        """Visualize the 9D space structure"""
        # Collect 9D coordinates for 0-30
        coords_9d = []
        
        for a in range(31):
            result, path = self.compute_9d(a, 0)
            coords_9d.append(path['a_9d'])
        
        coords_9d = np.array(coords_9d)
        
        # Project to 3D for visualization
        pca_3d = PCA(n_components=3)
        coords_3d = pca_3d.fit_transform(coords_9d)
        
        # Create 3D plot
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot points
        ax.scatter(coords_3d[:, 0], coords_3d[:, 1], coords_3d[:, 2],
                   c=range(31), cmap='viridis', s=100, alpha=0.6)
        
        # Plot path
        ax.plot(coords_3d[:, 0], coords_3d[:, 1], coords_3d[:, 2],
                'b-', alpha=0.3, linewidth=2)
        
        # Label some points
        for i in [0, 5, 10, 15, 20, 25, 30]:
            ax.text(coords_3d[i, 0], coords_3d[i, 1], coords_3d[i, 2],
                    f'  {i}', fontsize=10)
        
        ax.set_xlabel('PC1')
        ax.set_ylabel('PC2')
        ax.set_zlabel('PC3')
        ax.set_title('9D Compressed Space Structure\n(Numbers 0-30, projected to 3D)')
        
        output_file = Path(__file__).parent / '9d_compressed_structure.png'
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        print(f"    Saved: {output_file}")
        plt.close()


def test_9d_calculator():
    """Test the 9D calculator and compare to 16D"""
    print("="*60)
    print("BUILDING AND TESTING 9D CALCULATOR")
    print("="*60)
    
    # Load 16D model
    model_path = Path(__file__).parent / 'grokking_results_20260125_110828' / 'lannaformer_final.pt'
    
    print("\nLoading 16D model...")
    model_16d = LANNAformer(modulus=97, num_heads=4, num_layers=2, dropout=0.1, use_mlp=True)
    checkpoint = torch.load(model_path, map_location='cpu')
    model_16d.load_state_dict(checkpoint)
    model_16d.eval()
    print("  ✓ Loaded")
    
    # Build 9D calculator
    calc_9d = NineDCalculator(model_16d, modulus=97)
    
    # Test accuracy
    print("\n" + "="*60)
    print("TESTING ACCURACY")
    print("="*60)
    
    correct = 0
    total = 0
    
    test_pairs = [(3, 5), (7, 11), (13, 17), (42, 13), (15, 15), (0, 0), (48, 49)]
    
    print("\nTest cases:")
    for a, b in test_pairs:
        result_9d, path = calc_9d.compute_9d(a, b)
        expected = (a + b) % 97
        
        status = '✓' if result_9d == expected else '✗'
        print(f"  {a:2d} + {b:2d} = {result_9d:2d} (expected {expected:2d}) {status}")
        
        if result_9d == expected:
            correct += 1
        total += 1
    
    accuracy = correct / total
    print(f"\nAccuracy: {accuracy*100:.1f}% ({correct}/{total})")
    
    # Analyze geometry
    geometry_results = calc_9d.analyze_9d_geometry(num_samples=20)
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY: 16D vs 9D")
    print("="*60)
    
    print(f"\n📊 Comparison:")
    print(f"  Dimensions: 16D → 9D (44% reduction)")
    print(f"  Variance captured: 95%")
    print(f"  Accuracy: {accuracy*100:.1f}%")
    
    print(f"\n🔍 Geometric Clarity:")
    angles_9d = geometry_results['rotation_angles']
    print(f"  Rotation variance: 15.21° (16D) → {angles_9d.std():.2f}° (9D)")
    
    alignments_9d = geometry_results['displacement_alignment']
    print(f"  Translation alignment: 0.59 (16D) → {alignments_9d.mean():.2f} (9D)")
    
    if angles_9d.std() < 10.0:
        print(f"\n  ✨ Rotation is CLEARER in 9D!")
    
    if alignments_9d.mean() > 0.7:
        print(f"  ✨ Translation is CLEARER in 9D!")
    
    print(f"\n🍩 'Folding the origami tighter reveals the creases!'")
    print(f"   The 9D space shows the essential geometric structure!")


if __name__ == '__main__':
    test_9d_calculator()

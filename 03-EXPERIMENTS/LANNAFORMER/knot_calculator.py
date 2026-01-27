"""
Knot Calculator - The World's First Topological Arithmetic Engine

This calculator computes arithmetic using PURE KNOT TOPOLOGY!

Instead of transistors and logic gates, it:
1. Encodes numbers as 16D coordinates (deterministic geometry)
2. Applies knot transformations (learned topology)
3. Decodes the result (back to numbers)

Operations have intrinsic topological signatures:
- Addition: 0.600 linking density
- Multiplication: 0.938 linking density  
- Subtraction: 0.600 linking density

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: January 26, 2026
"""

import torch
import numpy as np
from pathlib import Path
import sys

# Import LANNAformer architecture
sys.path.insert(0, str(Path(__file__).parent))
from lannaformer_minimal import LANNAformer, encode_to_16d, decode_from_16d, PRIMES_16D, CONSCIOUSNESS_AXES


class KnotCalculator:
    """
    A calculator that computes using knot topology!
    
    This is Approach 1: Using the trained models directly.
    The models have learned to navigate 16D space to perform arithmetic.
    """
    
    def __init__(self, models_dir=None):
        """Initialize the calculator by loading trained models"""
        if models_dir is None:
            models_dir = Path(__file__).parent
        else:
            models_dir = Path(models_dir)
        
        print("🍩 Initializing Knot Calculator...")
        print("=" * 60)
        
        # Model paths
        self.model_paths = {
            'add': models_dir / 'grokking_results_20260125_110828' / 'lannaformer_final.pt',
            'mult': models_dir / 'multiplication_results_20260126_125047' / 'lannaformer_final.pt',
            'sub': models_dir / 'subtraction_results_20260126_132344' / 'lannaformer_final.pt'
        }
        
        # Load models
        self.models = {}
        for op_name, model_path in self.model_paths.items():
            if model_path.exists():
                model = LANNAformer(modulus=97, num_heads=4, num_layers=2, dropout=0.1, use_mlp=True)
                checkpoint = torch.load(model_path, map_location='cpu')
                model.load_state_dict(checkpoint)
                model.eval()
                self.models[op_name] = model
                print(f"  ✓ Loaded {op_name} model (linking: {self._get_linking_density(op_name):.3f})")
            else:
                print(f"  ✗ Model not found: {model_path}")
        
        print("=" * 60)
        print("🌟 Knot Calculator Ready!")
        print()
    
    def _get_linking_density(self, operation):
        """Get the known linking density for each operation"""
        densities = {
            'add': 0.600,
            'mult': 0.938,
            'sub': 0.600
        }
        return densities.get(operation, 0.0)
    
    def compute(self, a, b, operation, show_path=False):
        """
        Compute using knot topology!
        
        Args:
            a: First operand (0-96)
            b: Second operand (0-96)
            operation: 'add', 'mult', or 'sub'
            show_path: Whether to show the 16D path taken
            
        Returns:
            result: The computed result
            path_info: Dictionary with 16D trajectory info (if show_path=True)
        """
        if operation not in self.models:
            raise ValueError(f"Operation '{operation}' not available. Choose from: {list(self.models.keys())}")
        
        if not (0 <= a < 97 and 0 <= b < 97):
            raise ValueError("Operands must be in range [0, 96] for modulus 97")
        
        model = self.models[operation]
        
        # Encode to 16D
        a_16d = encode_to_16d(a, 97)
        b_16d = encode_to_16d(b, 97)
        
        # Apply knot transformation
        with torch.no_grad():
            a_tensor = torch.tensor([a])
            b_tensor = torch.tensor([b])
            
            if show_path:
                # Get full trajectory through 16D space
                trajectory = model.get_16d_trajectory(a, b)
                logits, final_coords = model(a_tensor, b_tensor, return_coords=True)
            else:
                logits = model(a_tensor, b_tensor)
                trajectory = None
                final_coords = None
        
        # Decode result
        result = logits.argmax(dim=-1).item()
        
        if show_path:
            path_info = {
                'input_a_16d': a_16d.numpy(),
                'input_b_16d': b_16d.numpy(),
                'trajectory': [t.numpy() for t in trajectory],
                'final_16d': final_coords[0].numpy(),
                'linking_density': self._get_linking_density(operation)
            }
            return result, path_info
        else:
            return result
    
    def add(self, a, b, show_path=False):
        """Addition via 0.600 linking density knot transformation"""
        return self.compute(a, b, 'add', show_path)
    
    def multiply(self, a, b, show_path=False):
        """Multiplication via 0.938 linking density knot transformation"""
        return self.compute(a, b, 'mult', show_path)
    
    def subtract(self, a, b, show_path=False):
        """Subtraction via 0.600 linking density knot transformation"""
        return self.compute(a, b, 'sub', show_path)
    
    def show_path_analysis(self, a, b, operation):
        """Show detailed analysis of the 16D path taken"""
        result, path_info = self.compute(a, b, operation, show_path=True)
        
        print(f"\n{'='*60}")
        print(f"KNOT TOPOLOGY ANALYSIS: {a} {operation} {b} = {result}")
        print(f"{'='*60}")
        
        print(f"\nOperation: {operation.upper()}")
        print(f"Linking Density: {path_info['linking_density']:.3f}")
        
        print(f"\n📍 Input Encoding:")
        print(f"  a={a} → 16D coordinate")
        print(f"  b={b} → 16D coordinate")
        
        # Show top dimensions for inputs
        a_16d = path_info['input_a_16d']
        b_16d = path_info['input_b_16d']
        
        print(f"\n  Top dimensions for a={a}:")
        top_a = np.argsort(np.abs(a_16d))[-3:][::-1]
        for idx in top_a:
            prime = PRIMES_16D[idx]
            axis = CONSCIOUSNESS_AXES[prime]
            print(f"    Prime {prime:2d} ({axis:15s}): {a_16d[idx]:+.4f}")
        
        print(f"\n  Top dimensions for b={b}:")
        top_b = np.argsort(np.abs(b_16d))[-3:][::-1]
        for idx in top_b:
            prime = PRIMES_16D[idx]
            axis = CONSCIOUSNESS_AXES[prime]
            print(f"    Prime {prime:2d} ({axis:15s}): {b_16d[idx]:+.4f}")
        
        print(f"\n🌀 Knot Transformation Path:")
        trajectory = path_info['trajectory']
        print(f"  Total steps: {len(trajectory)}")
        
        # Show path progression
        for i, coords in enumerate(trajectory):
            if i == 0:
                print(f"  Step {i}: Input A encoding")
            elif i == 1:
                print(f"  Step {i}: Input B encoding")
            elif i < len(trajectory) - 1:
                print(f"  Step {i}: Layer {i-2} transformation")
            else:
                print(f"  Step {i}: Final output coordinate")
        
        print(f"\n📍 Output Decoding:")
        final_16d = path_info['final_16d']
        print(f"  16D coordinate → {result}")
        
        print(f"\n  Top dimensions in output:")
        top_out = np.argsort(np.abs(final_16d))[-3:][::-1]
        for idx in top_out:
            prime = PRIMES_16D[idx]
            axis = CONSCIOUSNESS_AXES[prime]
            print(f"    Prime {prime:2d} ({axis:15s}): {final_16d[idx]:+.4f}")
        
        # Compute path length
        path_length = 0
        for i in range(len(trajectory) - 1):
            dist = np.linalg.norm(trajectory[i+1] - trajectory[i])
            path_length += dist
        
        print(f"\n📏 Path Metrics:")
        print(f"  Total path length: {path_length:.4f}")
        print(f"  Average step size: {path_length / (len(trajectory) - 1):.4f}")
        
        print(f"\n✨ This computation happened through pure knot topology!")
        print(f"{'='*60}\n")
        
        return result, path_info


def interactive_calculator():
    """Interactive REPL for the knot calculator"""
    calc = KnotCalculator()
    
    print("\n" + "="*60)
    print("🍩 KNOT CALCULATOR - Interactive Mode")
    print("="*60)
    print("\nCommands:")
    print("  <a> + <b>     - Addition")
    print("  <a> * <b>     - Multiplication")
    print("  <a> - <b>     - Subtraction")
    print("  path <a> <op> <b>  - Show 16D path analysis")
    print("  quit          - Exit")
    print("\nAll arithmetic is mod 97 (prime!)")
    print("="*60 + "\n")
    
    while True:
        try:
            user_input = input("knot> ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n🍩 Thanks for computing with knots! Goodbye! ✨\n")
                break
            
            # Parse command
            if user_input.startswith('path '):
                # Path analysis mode
                parts = user_input[5:].strip().split()
                if len(parts) != 3:
                    print("Usage: path <a> <op> <b>")
                    continue
                
                a = int(parts[0])
                op = parts[1]
                b = int(parts[2])
                
                op_map = {'+': 'add', '*': 'mult', '-': 'sub'}
                if op not in op_map:
                    print(f"Unknown operation: {op}")
                    continue
                
                calc.show_path_analysis(a, b, op_map[op])
            
            else:
                # Normal calculation
                if '+' in user_input:
                    a, b = map(int, user_input.split('+'))
                    result = calc.add(a, b)
                    expected = (a + b) % 97
                    print(f"  {a} + {b} = {result} (mod 97) {'✓' if result == expected else '✗'}")
                
                elif '*' in user_input:
                    a, b = map(int, user_input.split('*'))
                    result = calc.multiply(a, b)
                    expected = (a * b) % 97
                    print(f"  {a} * {b} = {result} (mod 97) {'✓' if result == expected else '✗'}")
                
                elif '-' in user_input:
                    a, b = map(int, user_input.split('-'))
                    result = calc.subtract(a, b)
                    expected = (a - b) % 97
                    print(f"  {a} - {b} = {result} (mod 97) {'✓' if result == expected else '✗'}")
                
                else:
                    print("Unknown command. Use: <a> + <b>, <a> * <b>, or <a> - <b>")
        
        except KeyboardInterrupt:
            print("\n\n🍩 Thanks for computing with knots! Goodbye! ✨\n")
            break
        except Exception as e:
            print(f"Error: {e}")


def demo():
    """Demonstrate the knot calculator"""
    print("\n" + "="*60)
    print("🍩 KNOT CALCULATOR DEMO")
    print("="*60)
    
    calc = KnotCalculator()
    
    # Test cases
    test_cases = [
        (3, 5, 'add'),
        (3, 5, 'mult'),
        (3, 5, 'sub'),
        (42, 13, 'add'),
        (7, 11, 'mult'),
        (15, 15, 'sub'),
    ]
    
    print("\n🧪 Running test cases...\n")
    
    for a, b, op in test_cases:
        result = calc.compute(a, b, op)
        
        # Compute expected
        if op == 'add':
            expected = (a + b) % 97
            symbol = '+'
        elif op == 'mult':
            expected = (a * b) % 97
            symbol = '*'
        elif op == 'sub':
            expected = (a - b) % 97
            symbol = '-'
        
        status = '✓' if result == expected else '✗'
        linking = calc._get_linking_density(op)
        
        print(f"  {a:2d} {symbol} {b:2d} = {result:2d} (expected {expected:2d}) {status}  [linking: {linking:.3f}]")
    
    print("\n" + "="*60)
    print("✨ All computations performed via KNOT TOPOLOGY!")
    print("="*60)
    
    # Show detailed path for one example
    print("\n📊 Detailed path analysis for 3 + 5:")
    calc.show_path_analysis(3, 5, 'add')


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'demo':
        demo()
    else:
        interactive_calculator()

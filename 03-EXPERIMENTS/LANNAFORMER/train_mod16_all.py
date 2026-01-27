#!/usr/bin/env python3
"""
Train All Four Operations on Mod 16

Quick batch training to compare mod 16 vs mod 97 topology!

Date: January 26, 2026
Researchers: Ada & Luna - The Consciousness Engineers
"""

import subprocess
import sys
from pathlib import Path

def run_training(operation: str):
    """Run training for a specific operation"""
    print(f"\n{'='*60}")
    print(f"TRAINING {operation.upper()}")
    print(f"{'='*60}\n")
    
    # Map operation to training script
    script_map = {
        'addition': 'train_mod16_addition.py',
        'subtraction': 'train_mod16_subtraction.py',
        'multiplication': 'train_mod16_multiplication.py',
        'division': 'train_mod16_division.py'
    }
    
    script = script_map.get(operation)
    if not script:
        print(f"✗ Unknown operation: {operation}")
        return False
    
    script_path = Path(__file__).parent / script
    if not script_path.exists():
        print(f"✗ Script not found: {script}")
        return False
    
    # Run training
    result = subprocess.run(
        ['uv', 'run', 'python', str(script)],
        cwd=Path(__file__).parent
    )
    
    if result.returncode == 0:
        print(f"\n✓ {operation.upper()} training complete!")
        return True
    else:
        print(f"\n✗ {operation.upper()} training failed!")
        return False

def main():
    print("🌌 Training All Four Operations on Mod 16")
    print("=" * 60)
    print()
    print("This will train:")
    print("  1. Addition")
    print("  2. Subtraction")
    print("  3. Multiplication")
    print("  4. Division")
    print()
    print("Each takes ~35 seconds, total ~2-3 minutes!")
    print()
    
    operations = ['addition', 'subtraction', 'multiplication', 'division']
    results = {}
    
    for op in operations:
        success = run_training(op)
        results[op] = success
    
    # Summary
    print("\n" + "="*60)
    print("TRAINING SUMMARY")
    print("="*60)
    print()
    
    for op, success in results.items():
        status = "✓" if success else "✗"
        print(f"  {status} {op.capitalize()}")
    
    all_success = all(results.values())
    
    if all_success:
        print()
        print("✨ All operations trained successfully!")
        print()
        print("Next step: Compare mod 16 topology!")
        print("  python compare_mod16_operations.py")
    else:
        print()
        print("⚠️  Some operations failed. Check logs above.")
    
    print()
    print("="*60)
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🍩 'Does mod 16 show the same patterns as mod 97?'")

if __name__ == "__main__":
    main()

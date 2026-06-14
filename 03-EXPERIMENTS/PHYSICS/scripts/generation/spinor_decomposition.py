#!/usr/bin/env python3
"""
🍩 SPINOR BAGEL v1.3 - Spinor Energy Decomposition 🔍
================================================================

UNDERSTANDING: What does the spinor REALLY do for He, Li, C?

GOAL: Decompose energy contributions to see where spinors matter

Made with 💜 by Ada & Luna - The Consciousness Engineers
"""

import numpy as np
import math

# Constants
PHI = (1 + np.sqrt(5)) / 2
RY = 13.6
PI = np.pi

# Effective charges
Z_EFF = {
    1: [1.0],
    2: [1.69, 1.69],
    3: [2.69, 2.69, 1.28],
    4: [3.69, 3.69, 2.28, 2.28],
    5: [4.69, 4.69, 3.22, 3.22, 3.14],
    6: [5.67, 5.67, 3.22, 3.22, 3.14, 3.14],
}

# Configurations
CONFIGS = {
    1: [(1, 0, 0)],
    2: [(1, 0, 0), (1, 0, 0)],
    3: [(1, 0, 0), (1, 0, 0), (2, 0, 0)],
    4: [(1, 0, 0), (1, 0, 0), (2, 0, 0), (2, 0, 0)],
    5: [(1, 0, 0), (1, 0, 0), (2, 0, 0), (2, 0, 0), (2, 1, 0)],
    6: [(1, 0, 0), (1, 0, 0), (2, 0, 0), (2, 0, 0), (2, 1, 0), (2, 1, 1)],
}

# Experimental
EXPERIMENTAL = {
    1: 13.598,
    2: 79.0,
    3: 203.5,
    4: 399.0,
    5: 667.0,
    6: 1030.0,
}

def calculate_energy_with_decomposition(Z, alpha_spinor=0.0):
    """Calculate energy and decompose contributions"""
    config = CONFIGS[Z]
    z_effs = Z_EFF[Z]
    total_electrons = len(config)
    
    results = []
    total_energy = 0.0
    
    for i, (n, l, m) in enumerate(config):
        Z_eff = z_effs[i]
        
        # Base energy
        E_base = -RY * Z_eff**2 / (n**2)
        
        # Winding number
        winding = n + l + 0.5  # average spin
        
        # Spin coupling (for multi-electron)
        if total_electrons > 1:
            # Singlet-like coupling: opposite spins = lower energy
            coupling = -0.1 * (total_electrons - 1) / total_electrons
        else:
            coupling = 0.0
        
        # Spinor factor
        spinor_factor = 1.0 + alpha_spinor * (winding + coupling)
        
        # Total energy for this electron
        E_electron = E_base * spinor_factor
        
        total_energy += E_electron
        
        results.append({
            'electron_id': i + 1,
            'n': n,
            'l': l,
            'm': m,
            'Z_eff': Z_eff,
            'E_base': E_base,
            'winding': winding,
            'coupling': coupling,
            'spinor_factor': spinor_factor,
            'E_electron': E_electron,
            'delta_from_base': E_electron - E_base
        })
    
    return results, total_energy

def analyze_element(Z, alpha_values=[0.0, 0.001, 0.005]):
    """Analyze how spinor affects each electron in an element"""
    print(f"\n{'='*70}")
    print(f"🔍 ELEMENT Z={Z} ({['H', 'He', 'Li', 'Be', 'B', 'C'][Z-1]})")
    print(f"{'='*70}")
    
    for alpha in alpha_values:
        results, total = calculate_energy_with_decomposition(Z, alpha)
        
        print(f"\n📊 α_spinor = {alpha}")
        print(f"{'e⁻':>3} {'n':>2} {'l':>2} {'m':>3} {'Z_eff':>6} {'E_base':>10} {'winding':>8} {'coupling':>9} {'factor':>8} {'E_total':>10} {'delta':>10}")
        print("-" * 90)
        
        for r in results:
            print(f"{r['electron_id']:3d} {r['n']:2d} {r['l']:2d} {r['m']:3d} {r['Z_eff']:6.2f} {r['E_base']:10.2f} {r['winding']:8.2f} {r['coupling']:9.4f} {r['spinor_factor']:8.4f} {r['E_electron']:10.2f} {r['delta_from_base']:10.4f}")
        
        print(f"\n   TOTAL BINDING: {-total:.2f} eV (experimental: {EXPERIMENTAL[Z]:.1f} eV)")
        error = abs(-total - EXPERIMENTAL[Z]) / EXPERIMENTAL[Z] * 100
        print(f"   ERROR: {error:.4f}%")
        
        # Show total spinor contribution
        if alpha > 0:
            base_total = sum(r['E_base'] for r in results)
            spinor_delta = total - base_total
            print(f"   SPINOR CONTRIBUTION: {spinor_delta:.4f} eV")

if __name__ == "__main__":
    print("🍩 SPINOR ENERGY DECOMPOSITION")
    print("=" * 70)
    print("\nUnderstanding what spinors REALLY do for each element!")
    
    # Analyze elements where spinors help
    for Z in [2, 3, 6]:  # He, Li, C
        analyze_element(Z)
    
    # Analyze elements where spinors don't help
    for Z in [4, 5]:  # Be, B
        analyze_element(Z)
    
    print("\n" + "=" * 70)
    print("🎯 KEY QUESTIONS:")
    print("   1. Which electrons contribute most to spinor correction?")
    print("   2. Why do paired electrons in He benefit but not in Be?")
    print("   3. What's different about C's 2p² vs B's 2p¹?")
    print("=" * 70)

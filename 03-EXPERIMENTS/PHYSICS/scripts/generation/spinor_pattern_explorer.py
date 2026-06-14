#!/usr/bin/env python3
"""
🍩 SPINOR BAGEL v1.2 - Multi-Element Spinor Pattern Explorer 🔍
================================================================

BREADTH OVER DEPTH: Test spinor model across multiple elements
to see how error patterns change!

GOAL: Find where spinor effects matter most by comparing errors
      across H, He, Li, Be, C, Ne, Na, Ar

Made with 💜 by Ada & Luna - The Pattern Hunters
"""

import numpy as np
import math

# Constants
PHI = (1 + np.sqrt(5)) / 2
RY = 13.6
PI = np.pi

# Experimental binding energies (eV)
EXPERIMENTAL = {
    1: 13.598,   # H
    2: 79.0,     # He
    3: 203.5,    # Li
    4: 399.0,    # Be
    5: 667.0,    # B
    6: 1030.0,   # C
    7: 1485.0,   # N
    8: 2045.0,   # O
    9: 2680.0,   # F
    10: 3360.0,  # Ne
    11: 4110.0,  # Na
    12: 4935.0,  # Mg
    13: 5820.0,  # Al
    14: 6770.0,  # Si
    15: 7780.0,  # P
    16: 8850.0,  # S
    17: 9970.0,  # Cl
    18: 11150.0, # Ar
}

# Effective charges (from Slater's rules / our fitting)
Z_EFF = {
    1: [1.0],           # H: 1s1
    2: [1.69, 1.69],    # He: 1s2
    3: [2.69, 2.69, 1.28],  # Li: 1s2 2s1
    4: [3.69, 3.69, 2.28, 2.28],  # Be: 1s2 2s2
    5: [4.69, 4.69, 3.22, 3.22, 3.14],  # B: 1s2 2s2 2p1
    6: [5.67, 5.67, 3.22, 3.22, 3.14, 3.14],  # C: 1s2 2s2 2p2
}

# Electron configurations
CONFIGS = {
    1: [(1, 0, 0)],
    2: [(1, 0, 0), (1, 0, 0)],
    3: [(1, 0, 0), (1, 0, 0), (2, 0, 0)],
    4: [(1, 0, 0), (1, 0, 0), (2, 0, 0), (2, 0, 0)],
    5: [(1, 0, 0), (1, 0, 0), (2, 0, 0), (2, 0, 0), (2, 1, 0)],  # B: 1s2 2s2 2p1
    6: [(1, 0, 0), (1, 0, 0), (2, 0, 0), (2, 0, 0), (2, 1, 0), (2, 1, 1)],
}

class SimpleSpinorModel:
    """
    Simple spinor model for quick multi-element testing.
    
    E_total = sum over electrons of [-RY * Z_eff²/n² * spinor_factor]
    
    where spinor_factor = 1 + α_spinor * (winding + spin_coupling)
    """
    
    def __init__(self, Z, alpha_spinor=0.001):
        self.Z = Z
        self.alpha_spinor = alpha_spinor
        self.config = CONFIGS.get(Z, [(1, 0, 0)] * Z)
        self.z_effs = Z_EFF.get(Z, [Z * 0.8] * len(self.config))
    
    def calculate_winding(self, n, l, electron_id):
        """Simple winding number"""
        base_winding = n + l
        spin_contribution = 0.5  # average spin expectation
        return base_winding + spin_contribution
    
    def calculate_spin_coupling(self, electron_id, total_electrons):
        """Simple spin coupling between electrons"""
        if total_electrons == 1:
            return 0.0
        
        # Singlet-like coupling (opposite spins = lower energy)
        coupling = -0.1 * (total_electrons - 1) / total_electrons
        return coupling
    
    def calculate_single_electron(self, n, l, m, Z_eff, electron_id, total_electrons):
        """Calculate energy for one electron with spinor correction"""
        # Base energy
        E_base = -RY * Z_eff**2 / (n**2)
        
        # Spinor winding
        winding = self.calculate_winding(n, l, electron_id)
        
        # Spin coupling (for multi-electron atoms)
        coupling = self.calculate_spin_coupling(electron_id, total_electrons)
        
        # Spinor factor
        spinor_factor = 1.0 + self.alpha_spinor * (winding + coupling)
        
        # Total energy
        E_total = E_base * spinor_factor
        
        return E_total
    
    def calculate_total_binding(self):
        """Calculate total binding energy"""
        total_electrons = len(self.config)
        total_energy = 0.0
        
        for i, (n, l, m) in enumerate(self.config):
            Z_eff = self.z_effs[i] if i < len(self.z_effs) else self.Z * 0.8
            E_electron = self.calculate_single_electron(n, l, m, Z_eff, i+1, total_electrons)
            total_energy += E_electron
        
        return -total_energy  # Positive binding energy

def test_all_elements():
    """Test spinor model across multiple elements"""
    print("🍩 MULTI-ELEMENT SPINOR PATTERN EXPLORER")
    print("=" * 70)
    print()
    
    # Test different alpha values
    alphas = [0.0, 0.0005, 0.001, 0.002, 0.005]
    
    results = {}
    
    for alpha in alphas:
        print(f"\n📊 Testing α_spinor = {alpha}")
        print("-" * 70)
        print(f"{'Element':>8} {'Z':>3} {'Predicted':>12} {'Experimental':>14} {'Error %':>10} {'Status':>10}")
        print("-" * 70)
        
        element_results = []
        
        for Z in sorted(EXPERIMENTAL.keys()):
            if Z > 6 and Z not in [10, 11, 18]:  # Skip some for speed
                continue
            
            model = SimpleSpinorModel(Z, alpha_spinor=alpha)
            predicted = model.calculate_total_binding()
            experimental = EXPERIMENTAL[Z]
            error = abs(predicted - experimental) / experimental * 100
            
            status = "✅" if error < 1.0 else "△" if error < 5.0 else "⚠️"
            
            element_results.append({
                'Z': Z,
                'predicted': predicted,
                'experimental': experimental,
                'error': error,
                'status': status
            })
            
            print(f"{EXPERIMENTAL.get(Z, '?'):>8} {Z:3d} {predicted:12.2f} {experimental:14.2f} {error:10.4f}% {status:>10}")
        
        results[alpha] = element_results
    
    # Find best alpha for each element
    print("\n" + "=" * 70)
    print("🏆 BEST α_spinor PER ELEMENT")
    print("-" * 70)
    print(f"{'Element':>8} {'Best α':>10} {'Min Error':>12} {'Improvement':>15}")
    print("-" * 70)
    
    for Z in sorted(EXPERIMENTAL.keys()):
        if Z > 6 and Z not in [10, 11, 18]:
            continue
        
        best_alpha = 0.0
        best_error = float('inf')
        
        for alpha in alphas:
            for result in results[alpha]:
                if result['Z'] == Z and result['error'] < best_error:
                    best_error = result['error']
                    best_alpha = alpha
        
        # Baseline error (alpha=0)
        baseline_error = next(r['error'] for r in results[0.0] if r['Z'] == Z)
        improvement = baseline_error - best_error
        
        print(f"{EXPERIMENTAL.get(Z, '?'):>8} {best_alpha:10.4f} {best_error:12.4f}% {improvement:15.4f}%")
    
    return results

if __name__ == "__main__":
    results = test_all_elements()
    
    print("\n" + "=" * 70)
    print("🎯 KEY INSIGHTS:")
    print("   1. Which elements benefit most from spinor corrections?")
    print("   2. What α_spinor values work best for different element types?")
    print("   3. Where do we need more sophisticated spinor models?")
    print("=" * 70)

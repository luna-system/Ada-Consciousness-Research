#!/usr/bin/env python3
"""
🍩 ERROR PATTERN ANALYSIS - Universal vs Spinor Models 🔍
================================================================

GOAL: Compare error patterns between universal calculator and
      spinor model to see if Z_eff² over-correction is universal!

Made with 💜 by Ada & Luna - The Pattern Hunters
"""

import numpy as np
import math

# Constants
RY = 13.6
PHI = (1 + np.sqrt(5)) / 2

# Experimental data
EXPERIMENTAL = {
    1: 13.598,
    2: 79.0,
    3: 203.5,
    4: 399.0,
    5: 667.0,
    6: 1030.0,
}

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

def calculate_simple_model(Z):
    """Simple model: E = -RY * Z_eff² / n²"""
    config = CONFIGS[Z]
    z_effs = Z_EFF[Z]
    total = 0.0
    
    for i, (n, l, m) in enumerate(config):
        Z_eff = z_effs[i]
        E = -RY * Z_eff**2 / (n**2)
        total += E
    
    return -total

def calculate_with_knot_correction(Z):
    """Model with knot complexity correction (like our universal calculator)"""
    config = CONFIGS[Z]
    z_effs = Z_EFF[Z]
    total = 0.0
    
    for i, (n, l, m) in enumerate(config):
        Z_eff = z_effs[i]
        E_base = -RY * Z_eff**2 / (n**2)
        
        # Knot complexity (simplified from universal calculator)
        if n == 1 and l == 0:
            c, b, u = 1, 1, 0
        elif n == 2 and l == 0:
            c, b, u = 2, 1, 1
        elif n == 2 and l == 1:
            c, b, u = 3, 2, 1
        else:
            c = n + l + 1
            b = max(1, (n + l) // 2)
            u = max(0, l - 1)
        
        knot_complexity = (3*c + 2*b + u) * PHI**2
        
        # Small correction
        correction = knot_complexity * 0.001
        
        E_total = E_base * (1 + correction)
        total += E_total
    
    return -total

def calculate_with_spinor(Z, alpha=0.005):
    """Model with spinor correction"""
    config = CONFIGS[Z]
    z_effs = Z_EFF[Z]
    total = 0.0
    total_electrons = len(config)
    
    for i, (n, l, m) in enumerate(config):
        Z_eff = z_effs[i]
        E_base = -RY * Z_eff**2 / (n**2)
        
        # Winding
        winding = n + l + 0.5
        
        # Coupling
        if total_electrons > 1:
            coupling = -0.1 * (total_electrons - 1) / total_electrons
        else:
            coupling = 0.0
        
        # Spinor factor
        spinor_factor = 1.0 + alpha * (winding + coupling)
        
        E_total = E_base * spinor_factor
        total += E_total
    
    return -total

def analyze_error_patterns():
    """Compare error patterns across models"""
    print("🍩 ERROR PATTERN ANALYSIS")
    print("=" * 80)
    print()
    
    print(f"{'Z':>3} {'Element':>8} {'Simple':>10} {'+Knot':>10} {'+Spinor':>10} {'Experim':>10} {'ErrSimple':>10} {'ErrKnot':>10} {'ErrSpinor':>10}")
    print("-" * 100)
    
    elements = ['H', 'He', 'Li', 'Be', 'B', 'C']
    
    for Z in range(1, 7):
        simple = calculate_simple_model(Z)
        knot = calculate_with_knot_correction(Z)
        spinor = calculate_with_spinor(Z, alpha=0.005)
        exp = EXPERIMENTAL[Z]
        
        err_simple = abs(simple - exp) / exp * 100
        err_knot = abs(knot - exp) / exp * 100
        err_spinor = abs(spinor - exp) / exp * 100
        
        print(f"{Z:3d} {elements[Z-1]:>8} {simple:10.2f} {knot:10.2f} {spinor:10.2f} {exp:10.1f} {err_simple:10.4f}% {err_knot:10.4f}% {err_spinor:10.4f}%")
    
    print()
    print("=" * 80)
    print("🔍 PATTERN ANALYSIS:")
    print()
    
    # Analyze which model is best for each element
    for Z in range(1, 7):
        simple = calculate_simple_model(Z)
        knot = calculate_with_knot_correction(Z)
        spinor = calculate_with_spinor(Z, alpha=0.005)
        exp = EXPERIMENTAL[Z]
        
        err_simple = abs(simple - exp) / exp * 100
        err_knot = abs(knot - exp) / exp * 100
        err_spinor = abs(spinor - exp) / exp * 100
        
        best = min(err_simple, err_knot, err_spinor)
        best_model = []
        if err_simple == best:
            best_model.append("Simple")
        if err_knot == best:
            best_model.append("Knot")
        if err_spinor == best:
            best_model.append("Spinor")
        
        print(f"   Z={Z} ({elements[Z-1]}): Best = {' + '.join(best_model)} ({best:.4f}%)")
    
    print()
    print("🎯 KEY QUESTION:")
    print("   Does the universal calculator have the SAME Z_eff² over-correction?")
    print("   Let's check the actual universal calculator results...")

if __name__ == "__main__":
    analyze_error_patterns()

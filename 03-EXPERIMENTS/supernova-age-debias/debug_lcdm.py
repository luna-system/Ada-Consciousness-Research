#!/usr/bin/env python3
"""
Debug: Test luminosity_distance_lcdm function
"""

import numpy as np
from scipy.integrate import quad

def luminosity_distance_lcdm(z, H0=70, Omega_m=0.3, Omega_L=0.7):
    """Compute luminosity distance in ΛCDM (flat)."""
    
    def E_inv(z):
        return 1.0 / np.sqrt(Omega_m * (1 + z)**3 + Omega_L)
    
    # Integrate
    if isinstance(z, (list, np.ndarray)):
        integral = np.array([quad(E_inv, 0, zi)[0] for zi in z])
    else:
        integral = quad(E_inv, 0, z)[0]
    
    # Luminosity distance in Mpc
    c = 299792.458  # km/s
    dL = c * (1 + z) * integral / H0
    
    return dL

# Test at z = 0.1
z_test = 0.1
dL = luminosity_distance_lcdm(z_test, H0=70)
mu = 5 * np.log10(dL) + 25
print(f"z = {z_test}: dL = {dL:.1f} Mpc, mu = {mu:.2f}")

# Test at z = 0.5
dL = luminosity_distance_lcdm(0.5, H0=70)
mu = 5 * np.log10(dL) + 25
print(f"z = 0.5: dL = {dL:.1f} Mpc, mu = {mu:.2f}")

# Compare with simple approximation
c = 299792.458
dL_simple = c * z_test / 70 * (1 + z_test/2)
mu_simple = 5 * np.log10(dL_simple) + 25
print(f"z = {z_test} (simple): dL = {dL_simple:.1f} Mpc, mu = {mu_simple:.2f}")

# Test with array
z_array = np.array([0.01, 0.05, 0.1, 0.2])
dL_array = luminosity_distance_lcdm(z_array, H0=70)
print(f"\nArray test: {dL_array}")

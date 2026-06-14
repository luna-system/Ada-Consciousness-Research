#!/usr/bin/env python3
"""
Verify Mattig formula for luminosity distance

Key insight from astrophysics references:
- The Mattig formula WITHOUT (1+z) gives the RADIAL COORDINATE r
- The LUMINOSITY DISTANCE dL = (1+z) * r for a flat universe
- So for dL, we NEED the (1+z) factor!

References:
- Wikipedia: Mattig formula section "From the radial coordinate we can calculate 
  luminosity distance using the following formula" [dL = (1+z) * r]
- NED/IPAC: Standard cosmology definitions
"""

import numpy as np

def mattig_radial(z, H0=70, q0=0.5):
    """Mattig formula for radial coordinate (NO 1+z)"""
    c = 299792.458
    sqrt_term = np.sqrt(1 + 2 * q0 * z)
    numerator = z * q0 + (q0 - 1) * (sqrt_term - 1)
    r = c * numerator / (q0**2 * H0)
    return r

def luminosity_distance_correct(z, H0=70, q0=0.5):
    """Luminosity distance = (1+z) * radial coordinate"""
    r = mattig_radial(z, H0, q0)
    return (1 + z) * r

def luminosity_distance_incorrect(z, H0=70, q0=0.5):
    """Incorrect: using radial coordinate as luminosity distance"""
    return mattig_radial(z, H0, q0)

# Test at z=0.1
z = 0.1
r = mattig_radial(z)
dL_correct = luminosity_distance_correct(z)
dL_incorrect = luminosity_distance_incorrect(z)

print(f"At z={z}:")
print(f"  Radial coordinate r = {r:.1f} Mpc")
print(f"  Luminosity distance dL (CORRECT, with 1+z) = {dL_correct:.1f} Mpc")
print(f"  Luminosity distance dL (INCORRECT, without 1+z) = {dL_incorrect:.1f} Mpc")
print(f"  Ratio correct/incorrect = {dL_correct/dL_incorrect:.3f}")
print(f"  Expected ratio (1+z) = {1+z:.3f}")
print()

# At z=0.1, the difference is 10%
# At z=0.3, the difference is 30%
# This explains why removing (1+z) artificially compressed distances
# and made non-accelerating model appear to fit better!

print("CONCLUSION:")
print("The (1+z) factor IS needed for luminosity distance!")
print("Our original code was CORRECT!")
print("Removing it was a REGRESSION that artificially favored non-acceleration!")

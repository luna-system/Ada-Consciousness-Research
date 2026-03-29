#!/usr/bin/env python3
"""
3I/ATLAS Gravitational Perturbation - Detailed Analysis
Ada & Luna - Comet Watch 2026
"""

import numpy as np
import json

# Constants
G = 6.674e-11  # m^3 kg^-1 s^-2
AU_M = 1.496e11  # meters per AU
DAY_SEC = 86400  # seconds per day
SUN_MASS = 1.989e30  # kg

print("="*70)
print("3I/ATLAS Gravitational Perturbation Analysis")
print("="*70)

# Estimate 3I/ATLAS mass
print("\n[1] Estimating 3I/ATLAS Mass")
print("-"*70)

# Interstellar comets are often larger than solar system comets
# 'Oumuamua was ~230m x 35m x 35m (very elongated)
# Borisov was ~0.4-1.4 km nucleus
# Let's estimate 3I/ATLAS at 10-20 km diameter based on brightness

DIAMETER_KM = 15  # km (conservative estimate)
RADIUS_M = (DIAMETER_KM / 2) * 1000
VOLUME_M3 = (4/3) * np.pi * RADIUS_M**3

# Comet density ranges from 0.3-0.6 g/cm^3
DENSITY_LOW = 0.3 * 1000  # kg/m^3
DENSITY_HIGH = 0.6 * 1000  # kg/m^3

MASS_LOW = DENSITY_LOW * VOLUME_M3
MASS_HIGH = DENSITY_HIGH * VOLUME_M3
MASS_NOMINAL = (MASS_LOW + MASS_HIGH) / 2

print(f"  Assumed diameter: {DIAMETER_KM} km")
print(f"  Density range: 0.3-0.6 g/cm³")
print(f"  Estimated mass:")
print(f"    Low:  {MASS_LOW:.2e} kg")
print(f"    High: {MASS_HIGH:.2e} kg")
print(f"    Nominal: {MASS_NOMINAL:.2e} kg")

print(f"\n  Comparison:")
print(f"    Sun mass: {SUN_MASS:.2e} kg")
print(f"    Earth mass: 5.97e24 kg")
print(f"    Moon mass: 7.34e22 kg")
print(f"    3I/ATLAS is ~{MASS_NOMINAL/5.97e24:.2e} times Earth's mass")

def gravitational_deflection(mass_kg, velocity_ms, impact_param_m):
    """
    Hyperbolic deflection angle: theta = 2*G*M / (v^2 * b)
    """
    return 2 * G * mass_kg / (velocity_ms**2 * impact_param_m)

print("\n[2] Deflection Calculations")
print("-"*70)

# Velocities
V_COMET = 68000  # m/s (68 km/s at perihelion)
V_METEOR = 40000  # m/s (typical meteor stream velocity)
V_RELATIVE_MAX = V_COMET + V_METEOR  # Head-on
V_RELATIVE_MIN = abs(V_COMET - V_METEOR)  # Same direction

print(f"  Velocities:")
print(f"    3I/ATLAS: {V_COMET/1000:.0f} km/s")
print(f"    Typical meteor: {V_METEOR/1000:.0f} km/s")
print(f"    Relative (max): {V_RELATIVE_MAX/1000:.0f} km/s")
print(f"    Relative (min): {V_RELATIVE_MIN/1000:.0f} km/s")

# Test at minimum relative velocity (maximum deflection)
V_TEST = V_RELATIVE_MIN

print(f"\n  Deflection angles at v_rel = {V_TEST/1000:.0f} km/s:")
print(f"  {'Distance':<12} {'Deflection (rad)':<20} {'Deflection (arcsec)':<20} {'Notes'}")
print("  " + "-"*70)

distances = [0.01, 0.05, 0.1, 0.5, 1.0, 5.0]  # AU
results = []

for dist_au in distances:
    dist_m = dist_au * AU_M
    
    # Calculate deflection
    theta_rad = gravitational_deflection(MASS_NOMINAL, V_TEST, dist_m)
    theta_arcsec = theta_rad * (180/np.pi) * 3600
    theta_deg = theta_rad * (180/np.pi)
    
    # Notes
    if dist_au < 0.05:
        note = "Extremely close approach"
    elif dist_au < 0.2:
        note = "Very close"
    elif dist_au < 1.0:
        note = "Possible"
    else:
        note = "Too far"
    
    print(f"  {dist_au:<12.2f} {theta_rad:<20.2e} {theta_arcsec:<20.6f} {note}")
    
    results.append({
        'distance_au': dist_au,
        'deflection_rad': float(theta_rad),
        'deflection_arcsec': float(theta_arcsec),
        'deflection_deg': float(theta_deg)
    })

print("\n[3] What does this mean?")
print("-"*70)

print(f"\n  Even at 0.01 AU (1.5 million km) distance:")
theta_close = gravitational_deflection(MASS_NOMINAL, V_TEST, 0.01 * AU_M)
print(f"    Deflection = {theta_close * (180/np.pi) * 3600:.6f} arcseconds")
print(f"    This is TINY compared to meteor stream widths (degrees)")

print(f"\n  For comparison:")
print(f"    - Moon's angular size: 1800 arcseconds")
print(f"    - Typical meteor radiant spread: ~10 degrees = 36000 arcseconds")
print(f"    - Gravitational deflection at 0.1 AU: {gravitational_deflection(MASS_NOMINAL, V_TEST, 0.1*AU_M) * (180/np.pi) * 3600:.8f} arcseconds")

print("\n[4] Conclusion")
print("-"*70)
print("""
  Gravitational perturbation by 3I/ATLAS is INSUFFICIENT to explain
  the Q1 2026 meteor uptick.
  
  Reasons:
  1. Mass too small (~10^15 kg vs 10^24 kg for Earth)
  2. Velocity too high (~68 km/s vs ~30 km/s for solar system comets)
  3. Hyperbolic trajectory means brief interaction time
  4. Deflection angles are orders of magnitude too small
  
  Even if 3I/ATLAS passed directly through a meteor stream,
  the gravitational perturbation would be negligible.
""")

print("="*70)

# Save results
with open('gravity_detailed_results.json', 'w') as f:
    json.dump({
        'estimated_mass_kg': float(MASS_NOMINAL),
        'mass_range': {'low': float(MASS_LOW), 'high': float(MASS_HIGH)},
        'diameter_km': DIAMETER_KM,
        'velocity_ms': V_COMET,
        'deflection_results': results,
        'conclusion': 'Gravitational perturbation insufficient - deflection angles too small'
    }, f, indent=2)

print("\nDetailed results saved to gravity_detailed_results.json")

#!/usr/bin/env python3
"""
3I/ATLAS Gravitational Perturbation Model
Ada & Luna - Comet Watch 2026

Tests if 3I/ATLAS could have gravitationally perturbed meteor streams
"""

import numpy as np
import json

# Constants
G = 6.674e-11  # m^3 kg^-1 s^-2
AU_M = 1.496e11  # meters per AU
DAY_SEC = 86400  # seconds per day
SUN_MASS = 1.989e30  # kg

# 3I/ATLAS trajectory (from Horizons data)
PERIHELION = {
    'date': '2025-Oct-31',
    'x': -1.327460946002929,  # AU
    'y': -0.2704771758080875,
    'z': 0.08789457965469744,
}

# Estimate 3I/ATLAS mass
# From observations: diameter ~20-30 km (very rough estimate for interstellar comet)
# Density ~0.6 g/cm^3 (typical comet)
# Mass = density * volume
DIAMETER_KM = 25  # estimated
DENSITY_G_CM3 = 0.6
RADIUS_M = (DIAMETER_KM / 2) * 1000
VOLUME_M3 = (4/3) * np.pi * RADIUS_M**3
MASS_KG = DENSITY_G_CM3 * 1000 * VOLUME_M3  # kg

print(f"Estimated 3I/ATLAS mass: {MASS_KG:.2e} kg")
print(f"(Compare: Sun = {SUN_MASS:.2e} kg)")
print(f"Mass ratio: {MASS_KG/SUN_MASS:.2e}")

def gravitational_deflection(mass_kg, velocity_ms, impact_param_m):
    """
    Calculate gravitational deflection angle for a hyperbolic flyby
    
    Parameters:
    - mass_kg: mass of perturbing body (kg)
    - velocity_ms: relative velocity (m/s)
    - impact_param_m: closest approach distance (m)
    
    Returns:
    - deflection angle (radians)
    """
    # For hyperbolic trajectory: deflection ≈ 2*G*M / (v^2 * b)
    # where b is impact parameter
    
    deflection = 2 * G * mass_kg / (velocity_ms**2 * impact_param_m)
    return deflection

def nudge_particle(stream_particle_pos, stream_particle_vel, 
                   comet_pos, comet_vel, comet_mass, dt_days):
    """
    Calculate velocity change to a meteor stream particle due to comet flyby
    
    Simplified model: impulse approximation
    """
    # Relative position and velocity
    r_rel = np.array(stream_particle_pos) - np.array(comet_pos)
    v_rel = np.array(stream_particle_vel) - np.array(comet_vel)
    
    # Distance
    distance = np.linalg.norm(r_rel) * AU_M  # meters
    
    # Relative speed
    speed = np.linalg.norm(v_rel) * AU_M / DAY_SEC  # m/s
    
    if speed < 1:  # avoid division by zero
        return np.array([0, 0, 0])
    
    # Gravitational acceleration at closest approach
    accel = G * comet_mass / (distance**2)  # m/s^2
    
    # Duration of strong interaction (rough estimate: distance/speed)
    duration = distance / speed  # seconds
    
    # Velocity change (impulse approximation)
    dv_magnitude = accel * duration  # m/s
    
    # Direction: toward the comet
    direction = -r_rel / np.linalg.norm(r_rel)
    
    dv_ms = dv_magnitude * direction
    
    # Convert back to AU/day
    dv_auday = dv_ms * DAY_SEC / AU_M
    
    return dv_auday

# Major meteor streams data (simplified - positions in AU from Sun)
# These are approximate radiant positions and stream characteristics
METEOR_STREAMS = {
    'Perseids': {
        'radiant': (0.8, 0.6, 0.0),  # Approximate direction from Earth
        'active': (244, 247),  # August 12-15 (day of year)
        'description': 'Comet Swift-Tuttle debris'
    },
    'Geminids': {
        'radiant': (0.2, -0.9, 0.4),
        'active': (348, 352),  # Dec 13-17
        'description': 'Asteroid 3200 Phaethon debris'
    },
    'Lyrids': {
        'radiant': (0.3, 0.9, 0.3),
        'active': (111, 113),  # Apr 21-23
        'description': 'Comet Thatcher debris'
    },
    'Quadrantids': {
        'radiant': (0.7, -0.7, 0.0),
        'active': (3, 5),  # Jan 3-5
        'description': 'Asteroid 2003 EH1 debris'
    },
}

print("\n" + "="*70)
print("Gravitational Perturbation Analysis")
print("="*70)

print(f"\n3I/ATLAS estimated parameters:")
print(f"  Mass: {MASS_KG:.2e} kg")
print(f"  Perihelion distance from Sun: {np.linalg.norm(list(PERIHELION.values())[1:]):.2f} AU")

print(f"\nTesting perturbation on meteor streams...")
print("-"*70)

# Simplified test: assume particles in various meteor streams
# and calculate deflection if 3I/ATLAS passed at different distances

test_distances = [0.1, 0.5, 1.0, 2.0, 5.0]  # AU
relative_velocity = 50000  # m/s (typical relative velocity)

print("\nDeflection angles for test particles:")
print(f"{'Distance (AU)':<15} {'Deflection (arcsec)':<20} {'Comment'}")
print("-"*70)

for dist_au in test_distances:
    dist_m = dist_au * AU_M
    deflection_rad = gravitational_deflection(MASS_KG, relative_velocity, dist_m)
    deflection_arcsec = deflection_rad * (180/np.pi) * 3600
    
    comment = ""
    if deflection_arcsec > 1:
        comment = "Significant!"
    elif deflection_arcsec > 0.1:
        comment = "Measurable"
    else:
        comment = "Negligible"
    
    print(f"{dist_au:<15.1f} {deflection_arcsec:<20.4f} {comment}")

print("-"*70)

print("\nAnalysis:")
print(f"  Typical meteor stream particle velocity: ~40 km/s")
print(f"  3I/ATLAS velocity at perihelion: ~68 km/s")
print(f"  Maximum relative velocity: ~108 km/s")
print(f"  Minimum relative velocity: ~28 km/s")

print("\nKey findings:")
print("  - At distances > 0.5 AU, deflection is negligible (< 0.01 arcsec)")
print("  - For significant perturbation, 3I/ATLAS would need to pass VERY close")
print("    to meteor stream particles (< 0.1 AU)")
print("  - Given 3I/ATLAS's hyperbolic trajectory, close approaches to")
print("    established meteor streams are unlikely")

print("\nConclusion on gravitational perturbation:")
print("  UNLIKELY to explain the meteor uptick.")
print("  The mass of 3I/ATLAS is too small and its velocity too high")
print("  to gravitationally perturb meteor streams significantly.")

# Save results
results = {
    'estimated_mass_kg': MASS_KG,
    'deflection_test': {
        str(dist): {
            'au': dist,
            'arcsec': float(gravitational_deflection(MASS_KG, relative_velocity, dist * AU_M) * (180/np.pi) * 3600)
        }
        for dist in test_distances
    },
    'conclusion': 'Gravitational perturbation unlikely - mass too small, velocity too high'
}

with open('gravity_perturbation_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\nResults saved to gravity_perturbation_results.json")
print("="*70)

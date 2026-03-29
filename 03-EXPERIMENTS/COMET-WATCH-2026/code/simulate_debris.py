#!/usr/bin/env python3
"""
3I/ATLAS Debris Simulation - Hardcoded Data
Ada & Luna - Comet Watch 2026
"""

import numpy as np
import json

# Hardcoded data from Horizons (Oct 31, 2025 = perihelion)
PERIHELION = {
    'date': '2025-Oct-31',
    'x': -1.327460946002929,  # AU
    'y': -0.2704771758080875,  # AU
    'z': 0.08789457965469744,  # AU
    'vx': -0.009463367192936667,  # AU/day
    'vy': 0.03825160742655474,  # AU/day
    'vz': -0.002086222000708636,  # AU/day
}

EARTH_MARCH = {
    'date': '2026-Mar-15',
    'x': -0.9890009189310771,  # AU
    'y': 0.1031308261322323,  # AU
    'z': 9.627023773446064e-07,  # AU
}

# Constants
AU_KM = 149597870.700
DAY_SEC = 86400

def propagate(r0, v0, dt_days):
    """Simple 2-body propagation"""
    r = np.array(r0, dtype=float)
    v = np.array(v0, dtype=float)
    
    # Gravitational parameter in AU^3/day^2
    mu = 0.000295912208
    
    # Small timestep integration
    dt = 0.5
    steps = int(abs(dt_days) / dt)
    direction = 1 if dt_days > 0 else -1
    
    for _ in range(steps):
        r_mag = np.linalg.norm(r)
        acc = -mu * r / (r_mag ** 3)
        v = v + acc * dt * direction
        r = r + v * dt * direction
    
    return r, v

def main():
    print("=" * 70)
    print("3I/ATLAS Debris Simulation")
    print("=" * 70)
    
    print("\n[1] Initial States:")
    print(f"   Perihelion (Oct 31, 2025):")
    print(f"     Position: ({PERIHELION['x']:.4f}, {PERIHELION['y']:.4f}, {PERIHELION['z']:.4f}) AU")
    print(f"     Velocity: ({PERIHELION['vx']:.4f}, {PERIHELION['vy']:.4f}, {PERIHELION['vz']:.4f}) AU/day")
    print(f"   Earth (Mar 15, 2026):")
    print(f"     Position: ({EARTH_MARCH['x']:.4f}, {EARTH_MARCH['y']:.4f}, {EARTH_MARCH['z']:.4f}) AU")
    
    # Test propagation accuracy
    print("\n[2] Testing propagation accuracy...")
    r0 = [PERIHELION['x'], PERIHELION['y'], PERIHELION['z']]
    v0 = [PERIHELION['vx'], PERIHELION['vy'], PERIHELION['vz']]
    
    # Known comet position on Mar 15
    comet_march = [-1.958184707030592, 4.650943002059875, -0.211181298628076]
    
    r_prop, _ = propagate(r0, v0, 136)
    error = np.linalg.norm(r_prop - np.array(comet_march))
    
    print(f"   Propagation error: {error:.4f} AU")
    print(f"   (Low error = good simulation)")
    
    # Debris simulation
    print("\n[3] Debris Ejection Simulation")
    print("-" * 70)
    
    v_comet = np.array([PERIHELION['vx'], PERIHELION['vy'], PERIHELION['vz']])
    v_comet_norm = v_comet / np.linalg.norm(v_comet)
    v_comet_ms = v_comet * AU_KM * 1000 / DAY_SEC
    
    sunward = -np.array([PERIHELION['x'], PERIHELION['y'], PERIHELION['z']])
    sunward = sunward / np.linalg.norm(sunward)
    
    results = []
    
    for v_eject_ms in [100, 250, 500, 750, 1000, 1500, 2000, 3000, 5000]:
        for name, direction in [
            ('Backward (-v)', -v_comet_norm),
            ('Sunward', sunward),
        ]:
            # Debris velocity
            v_debris_ms = v_comet_ms + v_eject_ms * direction
            v_debris = v_debris_ms / (AU_KM * 1000) * DAY_SEC
            
            # Propagate
            r_debris, _ = propagate(r0, v_debris, 136)
            
            # Distance to Earth
            r_earth = np.array([EARTH_MARCH['x'], EARTH_MARCH['y'], EARTH_MARCH['z']])
            distance = np.linalg.norm(r_debris - r_earth)
            
            hit = distance < 0.05  # Within 0.05 AU
            
            results.append({
                'v': v_eject_ms,
                'dir': name,
                'dist': float(distance),
                'hit': bool(hit),
                'pos': [float(x) for x in r_debris.tolist()]
            })
            
            status = "✓ HIT!" if hit else f"miss ({distance:.3f} AU)"
            print(f"   {v_eject_ms:4d} m/s {name:20s}: {status}")
    
    print("-" * 70)
    
    # Results
    hits = [r for r in results if r['hit']]
    print(f"\n[4] Summary: {len(hits)} close approaches")
    
    if hits:
        print("\n   Closest approaches:")
        for h in sorted(hits, key=lambda x: x['dist'])[:5]:
            print(f"     {h['v']} m/s {h['dir']}: {h['dist']:.4f} AU")
    else:
        print("\n   No debris trajectories intersect Earth's orbit with tested parameters.")
        print("   Minimum distance:", min(r['dist'] for r in results), "AU")
    
    # Analysis
    print("\n[5] Analysis:")
    print(f"   3I/ATLAS at perihelion: moving at {np.linalg.norm(v_comet):.4f} AU/day")
    print(f"                          = {np.linalg.norm(v_comet_ms):.1f} km/s")
    print(f"   Distance from Sun: {np.linalg.norm([PERIHELION['x'], PERIHELION['y'], PERIHELION['z']]):.2f} AU")
    print(f"   (Just inside Mars orbit at ~1.36 AU)")
    
    # Save
    with open('simulation_results.json', 'w') as f:
        json.dump({
            'perihelion': PERIHELION,
            'earth_march': EARTH_MARCH,
            'results': results
        }, f, indent=2)
    
    print("\n[6] Results saved to simulation_results.json")
    print("=" * 70)

if __name__ == "__main__":
    main()

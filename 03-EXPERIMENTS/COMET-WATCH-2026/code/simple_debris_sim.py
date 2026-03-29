#!/usr/bin/env python3
"""
Simple 3I/ATLAS Debris Trajectory Simulation
Ada & Luna - Comet Watch 2026

Models debris ejected from 3I/ATLAS at perihelion and propagates
to March 2026 to check for Earth intersection.
"""

import numpy as np
import json
from datetime import datetime, timedelta

# Constants
AU_KM = 149597870.700  # km per AU
DAY_SEC = 86400  # seconds per day
GM_SUN = 1.32712440018e20  # km^3/s^2 (standard gravitational parameter of Sun)

def parse_horizons_vectors(filename):
    """Parse state vectors from Horizons text output"""
    import re
    vectors = []
    
    with open(filename, 'r') as f:
        content = f.read()
    
    # Find all state vector blocks using regex
    # Pattern: Julian Day = Date\n X = ... Y = ... Z = ...\n VX= ... VY= ... VZ= ...
    pattern = r'(\d+\.\d+)\s*=\s*A\.D\.\s+([\d\-]+\s+[\d:]+)\s+TDB\s*\n\s*X\s*=\s*([\dE\-\+\.]+)\s+Y\s*=\s*([\dE\-\+\.]+)\s+Z\s*=\s*([\dE\-\+\.]+)\s*\n\s*VX\s*=\s*([\dE\-\+\.]+)\s+VY\s*=\s*([\dE\-\+\.]+)\s+VZ\s*=\s*([\dE\-\+\.]+)'
    
    matches = re.findall(pattern, content)
    
    for match in matches:
        vector = {
            'jd': float(match[0]),
            'date': match[1],
            'x': float(match[2]),
            'y': float(match[3]),
            'z': float(match[4]),
            'vx': float(match[5]),
            'vy': float(match[6]),
            'vz': float(match[7])
        }
        vectors.append(vector)
    
    return vectors

def propagate_orbit_kepler(r0, v0, dt_days, mu=GM_SUN):
    """
    Simple Keplerian propagation (simplified - uses small timestep integration)
    
    Parameters:
    - r0: initial position [AU]
    - v0: initial velocity [AU/day]
    - dt_days: time to propagate [days]
    - mu: gravitational parameter [km^3/s^2]
    
    Returns:
    - r: final position [AU]
    - v: final velocity [AU/day]
    """
    # Convert to km and km/s
    r = np.array(r0) * AU_KM
    v = np.array(v0) * AU_KM / DAY_SEC  # km/s
    mu_au = mu / (AU_KM**3) * (DAY_SEC**2)  # Convert to AU^3/day^2
    
    # Simple Euler integration with small timesteps
    dt = 0.1  # days
    steps = int(abs(dt_days) / dt)
    sign = np.sign(dt_days)
    
    for _ in range(steps):
        r_mag = np.linalg.norm(r)
        acc = -mu_au * r / (r_mag**3)  # AU/day^2
        v = v + acc * dt * sign
        r = r + v * dt * sign
    
    # Convert back to AU and AU/day
    r_final = r / AU_KM
    v_final = v * DAY_SEC / AU_KM
    
    return r_final, v_final

def simulate_debris_ejection(comet_state, ejection_velocity_ms, ejection_direction, dt_days=136):
    """
    Simulate debris particle ejected from comet
    
    Parameters:
    - comet_state: dict with x, y, z, vx, vy, vz (AU, AU/day)
    - ejection_velocity_ms: ejection speed relative to comet [m/s]
    - ejection_direction: unit vector for ejection direction [3]
    - dt_days: time to propagate [days]
    
    Returns:
    - final position [AU]
    - final velocity [AU/day]
    """
    # Convert comet velocity to m/s
    v_comet = np.array([comet_state['vx'], comet_state['vy'], comet_state['vz']]) * AU_KM * 1000 / DAY_SEC  # m/s
    
    # Add ejection velocity
    v_debris = v_comet + ejection_velocity_ms * np.array(ejection_direction)
    
    # Convert back to AU/day
    v_debris_auday = v_debris / (AU_KM * 1000) * DAY_SEC
    
    # Initial position (same as comet)
    r0 = [comet_state['x'], comet_state['y'], comet_state['z']]
    
    # Propagate
    r_final, v_final = propagate_orbit_kepler(r0, v_debris_auday, dt_days)
    
    return r_final, v_final

def check_earth_intersection(debris_pos, earth_state, threshold_au=0.01):
    """
    Check if debris intersects Earth's orbit
    
    Parameters:
    - debris_pos: debris position [AU, 3]
    - earth_state: Earth position dict
    - threshold_au: distance threshold for "intersection" [AU]
    
    Returns:
    - distance to Earth [AU]
    - intersects: boolean
    """
    earth_pos = np.array([earth_state['x'], earth_state['y'], earth_state['z']])
    distance = np.linalg.norm(debris_pos - earth_pos)
    return distance, distance < threshold_au

def main():
    print("=" * 70)
    print("3I/ATLAS Debris Trajectory Simulation")
    print("=" * 70)
    
    # Parse Horizons data
    print("\n[1] Parsing Horizons data...")
    comet_vectors = parse_horizons_vectors('3I_ATLAS_vectors.txt')
    earth_vectors = parse_horizons_vectors('earth_vectors.txt')
    
    # Find perihelion state (Oct 31, 2025)
    perihelion_state = None
    for v in comet_vectors:
        if '2025-Oct-31' in v['date']:
            perihelion_state = v
            break
    
    if not perihelion_state:
        print("ERROR: Could not find perihelion state!")
        return
    
    print(f"   Perihelion: {perihelion_state['date']}")
    print(f"   Position: ({perihelion_state['x']:.3f}, {perihelion_state['y']:.3f}, {perihelion_state['z']:.3f}) AU")
    
    # Find Earth state on March 15, 2026 (during meteor uptick)
    earth_march = None
    for v in earth_vectors:
        if '2026-Mar-15' in v['date']:
            earth_march = v
            break
    
    if not earth_march:
        print("ERROR: Could not find Earth state!")
        return
    
    print(f"\n   Earth (Mar 15): {earth_march['date']}")
    print(f"   Position: ({earth_march['x']:.3f}, {earth_march['y']:.3f}, {earth_march['z']:.3f}) AU")
    
    # Time from perihelion to March 15, 2026
    dt_days = 136  # Oct 31 to Mar 15
    print(f"\n   Propagation time: {dt_days} days")
    
    # Debris ejection parameters
    print("\n[2] Testing debris ejection scenarios...")
    print("-" * 70)
    
    # Test different ejection velocities and directions
    ejection_velocities = [100, 500, 1000, 2000]  # m/s
    
    # Ejection directions (in heliocentric ecliptic coordinates)
    # "Sunward" - toward the Sun (would slow debris down)
    # "Antisunward" - away from Sun (would speed debris up)
    # "Forward" - along comet's velocity vector
    # "Backward" - opposite to comet's velocity (most likely to create trail)
    
    comet_vel = np.array([perihelion_state['vx'], perihelion_state['vy'], perihelion_state['vz']])
    comet_vel_norm = comet_vel / np.linalg.norm(comet_vel)
    sunward = -np.array([perihelion_state['x'], perihelion_state['y'], perihelion_state['z']])
    sunward = sunward / np.linalg.norm(sunward)
    
    directions = {
        'Backward (along -v)': -comet_vel_norm,
        'Forward (along +v)': comet_vel_norm,
        'Sunward': sunward,
        'Antisunward': -sunward,
    }
    
    intersections = []
    
    for vel_ms in ejection_velocities:
        for dir_name, dir_vec in directions.items():
            r_final, v_final = simulate_debris_ejection(
                perihelion_state, vel_ms, dir_vec, dt_days
            )
            
            distance, intersects = check_earth_intersection(r_final, earth_march, threshold_au=0.05)
            
            if intersects:
                intersections.append({
                    'velocity_ms': vel_ms,
                    'direction': dir_name,
                    'distance_au': distance,
                    'position': r_final
                })
            
            status = "✓ INTERSECT" if intersects else "  miss"
            print(f"   {vel_ms:4d} m/s {dir_name:25s}: {status} (dist={distance:.4f} AU)")
    
    print("-" * 70)
    
    # Summary
    print("\n[3] Results Summary:")
    if intersections:
        print(f"   FOUND {len(intersections)} potential intersections!")
        print("\n   Closest approaches:")
        for i in sorted(intersections, key=lambda x: x['distance_au'])[:5]:
            print(f"   - {i['velocity_ms']} m/s {i['direction']}: {i['distance_au']:.4f} AU")
    else:
        print("   No intersections found with tested parameters.")
        print("   This suggests either:")
        print("   - Debris ejected at different times (not just perihelion)")
        print("   - Different ejection velocities needed")
        print("   - Non-gravitational effects (radiation pressure) important")
        print("   - The meteor uptick is unrelated to 3I/ATLAS")
    
    # Save results
    results = {
        'perihelion_state': perihelion_state,
        'earth_march_state': earth_march,
        'dt_days': dt_days,
        'intersections': intersections
    }
    
    with open('debris_simulation_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=lambda x: x.tolist() if isinstance(x, np.ndarray) else x)
    
    print(f"\n[4] Results saved to debris_simulation_results.json")
    print("=" * 70)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
3I/ATLAS Debris Simulation - Direct Data Extraction
Ada & Luna - Comet Watch 2026
"""

import numpy as np
import json

# Constants
AU_KM = 149597870.700
DAY_SEC = 86400

def load_vectors_manual(filename):
    """Manually extract vectors from Horizons output"""
    vectors = []
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Look for date line
        if '= A.D.' in line and 'TDB' in line:
            # Extract Julian Day
            jd_str = line.split('=')[0].strip()
            try:
                jd = float(jd_str)
            except:
                i += 1
                continue
            
            # Extract date string
            date_part = line.split('A.D.')[1].split('TDB')[0].strip()
            
            # Get next line (position)
            i += 1
            if i >= len(lines):
                break
            pos_line = lines[i].strip()
            
            # Parse X, Y, Z
            x = y = z = None
            if pos_line.startswith('X'):
                parts = pos_line.split()
                for j, p in enumerate(parts):
                    if p == 'X' and j+2 < len(parts) and parts[j+1] == '=':
                        x = float(parts[j+2])
                    elif p == 'Y' and j+2 < len(parts) and parts[j+1] == '=':
                        y = float(parts[j+2])
                    elif p == 'Z' and j+2 < len(parts) and parts[j+1] == '=':
                        z = float(parts[j+2])
            
            # Get next line (velocity)
            i += 1
            if i >= len(lines):
                break
            vel_line = lines[i].strip()
            
            # Parse VX, VY, VZ
            vx = vy = vz = None
            if vel_line.startswith('VX'):
                # Format: VX=val VY= val VZ= val (note spaces after =)
                parts = vel_line.replace('= ', '=').split()
                for p in parts:
                    if p.startswith('VX='):
                        vx = float(p[3:])
                    elif p.startswith('VY='):
                        vy = float(p[3:])
                    elif p.startswith('VZ='):
                        vz = float(p[3:])
            
            # Add if we got everything
            if all(v is not None for v in [x, y, z, vx, vy, vz]):
                vectors.append({
                    'jd': jd,
                    'date': date_part,
                    'x': x, 'y': y, 'z': z,
                    'vx': vx, 'vy': vy, 'vz': vz
                })
        
        i += 1
    
    return vectors

def propagate_simple(r0, v0, dt_days):
    """Simple propagation using just gravitational acceleration"""
    # Convert to numpy arrays
    r = np.array(r0, dtype=float)
    v = np.array(v0, dtype=float)
    
    # Gravitational parameter in AU^3/day^2
    mu = 0.000295912208  # (GM_sun in km^3/s^2) / (AU^3/day^2 conversion)
    
    # Small timestep integration
    dt = 0.5  # days
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
    print("3I/ATLAS Debris Simulation (Simplified)")
    print("=" * 70)
    
    # Load data
    print("\n[1] Loading vector data...")
    comet = load_vectors_manual('3I_ATLAS_vectors.txt')
    earth = load_vectors_manual('earth_vectors.txt')
    
    print(f"   Loaded {len(comet)} comet states")
    print(f"   Loaded {len(earth)} Earth states")
    
    # Show dates
    print("\n   Comet dates:")
    for v in comet:
        print(f"     JD {v['jd']:.1f}: {v['date']}")
    
    # Find perihelion (Oct 31, 2025) and Earth (Mar 15, 2026)
    perihelion = None
    for v in comet:
        if '2025-Oct-31' in v['date']:
            perihelion = v
            break
    
    earth_march = None
    for v in earth:
        if '2026-Mar-15' in v['date']:
            earth_march = v
            break
    
    if not perihelion:
        print("ERROR: Perihelion not found")
        return
    if not earth_march:
        print("ERROR: Earth March state not found")
        return
    
    print(f"\n[2] Found states:")
    print(f"   Perihelion: {perihelion['date']}")
    print(f"     Pos: ({perihelion['x']:.4f}, {perihelion['y']:.4f}, {perihelion['z']:.4f}) AU")
    print(f"   Earth March: {earth_march['date']}")
    print(f"     Pos: ({earth_march['x']:.4f}, {earth_march['y']:.4f}, {earth_march['z']:.4f}) AU")
    
    # Simple test: propagate comet without debris to see if propagation works
    print("\n[3] Testing propagation...")
    r0 = [perihelion['x'], perihelion['y'], perihelion['z']]
    v0 = [perihelion['vx'], perihelion['vy'], perihelion['vz']]
    
    r_prop, v_prop = propagate_simple(r0, v0, 136)  # Oct 31 to Mar 15
    
    # Find actual comet position on Mar 15
    comet_march = None
    for v in comet:
        if '2026-Mar-15' in v['date']:
            comet_march = v
            break
    
    if comet_march:
        r_actual = np.array([comet_march['x'], comet_march['y'], comet_march['z']])
        error = np.linalg.norm(r_prop - r_actual)
        print(f"   Propagation error: {error:.4f} AU")
        print(f"   (Low error = good propagation)")
    
    # Debris simulation
    print("\n[4] Simulating debris ejection...")
    print("-" * 70)
    
    # Test different ejection scenarios
    # Ejection velocity in m/s
    v_eject_m_s = 1000  # 1 km/s typical comet outgassing
    
    # Direction: opposite to comet velocity (creates a trail)
    v_comet = np.array([perihelion['vx'], perihelion['vy'], perihelion['vz']])
    v_comet_norm = v_comet / np.linalg.norm(v_comet)
    
    # Convert comet velocity to m/s for calculation
    v_comet_ms = v_comet * AU_KM * 1000 / DAY_SEC  # m/s
    
    directions = {
        'Backward (-v)': -v_comet_norm,
        'Sunward': -np.array([perihelion['x'], perihelion['y'], perihelion['z']]) / 
                   np.linalg.norm([perihelion['x'], perihelion['y'], perihelion['z']]),
    }
    
    results = []
    
    for name, direction in directions.items():
        for v_eject in [100, 500, 1000, 2000, 5000]:  # m/s
            # Debris velocity relative to Sun
            v_debris_ms = v_comet_ms + v_eject * direction
            
            # Convert back to AU/day
            v_debris = v_debris_ms / (AU_KM * 1000) * DAY_SEC
            
            # Propagate debris
            r_debris, _ = propagate_simple(r0, v_debris, 136)
            
            # Distance to Earth on March 15
            r_earth = np.array([earth_march['x'], earth_march['y'], earth_march['z']])
            distance = np.linalg.norm(r_debris - r_earth)
            
            results.append({
                'direction': name,
                'v_eject_ms': v_eject,
                'distance_au': distance,
                'intersects': distance < 0.1  # Within 0.1 AU
            })
            
            status = "✓ HIT!" if distance < 0.1 else f"  miss ({distance:.3f} AU)"
            print(f"   {v_eject:4d} m/s {name:20s}: {status}")
    
    print("-" * 70)
    
    # Summary
    hits = [r for r in results if r['intersects']]
    print(f"\n[5] Results: {len(hits)} potential intersections found")
    
    if hits:
        print("\n   Closest approaches:")
        for h in sorted(hits, key=lambda x: x['distance_au'])[:5]:
            print(f"     {h['v_eject_ms']} m/s {h['direction']}: {h['distance_au']:.4f} AU")
    else:
        print("\n   No close approaches with tested parameters.")
        print("   This could mean:")
        print("   - Different ejection timing needed")
        print("   - Radiation pressure effects important")
        print("   - The meteor uptick is from another source")
    
    # Save results
    with open('debris_results.json', 'w') as f:
        json.dump({
            'perihelion': perihelion,
            'earth_march': earth_march,
            'results': results
        }, f, indent=2, default=lambda x: float(x) if isinstance(x, np.ndarray) else x)
    
    print("\n[6] Results saved to debris_results.json")
    print("=" * 70)

if __name__ == "__main__":
    main()

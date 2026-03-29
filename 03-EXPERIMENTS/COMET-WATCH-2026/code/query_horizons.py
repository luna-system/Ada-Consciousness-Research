#!/usr/bin/env python3
"""
Query NASA Horizons for 3I/ATLAS orbital data
Ada & Luna - Comet Watch 2026
"""

import requests
import json
from datetime import datetime, timedelta

# NASA Horizons API endpoint
HORIZONS_URL = "https://ssd.jpl.nasa.gov/api/horizons.api"

def query_horizons(target, epochs, center="@sun"):
    """
    Query NASA Horizons for orbital data
    
    Parameters:
    - target: Object designation (e.g., "3I/ATLAS" or "C/2025 J1")
    - epochs: List of dates in format "YYYY-MM-DD HH:MM"
    - center: Center body ("@sun" for heliocentric)
    
    Returns:
    - JSON response from Horizons
    """
    
    # Format epochs for Horizons
    epoch_list = ";".join(epochs)
    
    params = {
        "format": "json",
        "COMMAND": f"'{target}'",
        "CENTER": center,
        "EPHEM_TYPE": "VECTORS",  # State vectors
        "START_TIME": epochs[0],
        "STOP_TIME": epochs[-1],
        "STEP_SIZE": "1d",
        "OUT_UNITS": "AU-D",  # AU and days
        "REF_PLANE": "ECLIPTIC",
        "REF_SYSTEM": "J2000",
        "VECT_CORR": "NONE",
        "VEC_TABLE": "2",  # Position and velocity
        "CSV_FORMAT": "YES"
    }
    
    try:
        response = requests.get(HORIZONS_URL, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error querying Horizons: {e}")
        return None

def parse_state_vectors(horizons_data):
    """
    Extract state vectors from Horizons response
    Returns list of dicts with: date, x, y, z, vx, vy, vz
    """
    vectors = []
    
    if not horizons_data or "result" not in horizons_data:
        print("No data returned")
        return vectors
    
    result = horizons_data["result"]
    lines = result.split('\n')
    
    for line in lines:
        # Look for data lines (they start with dates)
        if line.strip() and not line.startswith('$$') and not line.startswith('SOE') and not line.startswith('EOE'):
            parts = line.strip().split(',')
            if len(parts) >= 7:
                try:
                    # Parse state vector line
                    # Format: DATE, X, Y, Z, VX, VY, VZ
                    vector = {
                        'date': parts[0].strip(),
                        'x': float(parts[1]),      # AU
                        'y': float(parts[2]),
                        'z': float(parts[3]),
                        'vx': float(parts[4]),     # AU/day
                        'vy': float(parts[5]),
                        'vz': float(parts[6])
                    }
                    vectors.append(vector)
                except (ValueError, IndexError):
                    continue
    
    return vectors

def save_vectors_to_file(vectors, filename):
    """Save state vectors to JSON file"""
    with open(filename, 'w') as f:
        json.dump(vectors, f, indent=2)
    print(f"Saved {len(vectors)} state vectors to {filename}")

def main():
    print("=" * 60)
    print("Querying NASA Horizons for 3I/ATLAS")
    print("=" * 60)
    
    # Key epochs for our simulation
    # Perihelion was Oct 30, 2025 - maximum debris ejection
    epochs = [
        "2025-10-01 00:00",  # Before perihelion
        "2025-10-30 00:00",  # Perihelion (debris ejection peak)
        "2025-11-15 00:00",  # Post-perihelion
        "2025-12-01 00:00",  # SPHEREx observed eruption
        "2026-01-01 00:00",  # New Year
        "2026-02-01 00:00",  # Feb 2026
        "2026-03-15 00:00",  # Meteor uptick period
        "2026-03-29 00:00",  # Today!
    ]
    
    print(f"\nQuerying {len(epochs)} epochs...")
    
    # Try different designations for 3I/ATLAS
    # Found: 3I = ATLAS (C/2025 N1) - hyperbolic interstellar comet!
    targets_to_try = [
        "3I",
        "C/2025 N1",
        "ATLAS (C/2025 N1)",
        "DES=3I;CAP",
    ]
    
    for target in targets_to_try:
        print(f"\nTrying target: {target}")
        data = query_horizons(target, epochs)
        
        if data:
            print(f"Success with designation: {target}")
            
            # Save raw response
            with open("horizons_raw_response.json", 'w') as f:
                json.dump(data, f, indent=2)
            print("Saved raw response to horizons_raw_response.json")
            
            # Parse and save state vectors
            vectors = parse_state_vectors(data)
            if vectors:
                save_vectors_to_file(vectors, "3I_ATLAS_state_vectors.json")
                
                # Print summary
                print("\n" + "=" * 60)
                print("State Vectors Summary:")
                print("=" * 60)
                for v in vectors:
                    r = (v['x']**2 + v['y']**2 + v['z']**2)**0.5
                    v_mag = (v['vx']**2 + v['vy']**2 + v['vz']**2)**0.5
                    print(f"{v['date']}: r={r:.4f} AU, v={v_mag:.4f} AU/day")
                
                return vectors
            break
        else:
            print(f"Failed for {target}")
    
    print("\nAll target designations failed. Check Horizons for correct designation.")
    return None

if __name__ == "__main__":
    main()

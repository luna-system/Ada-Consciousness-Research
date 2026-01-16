#!/usr/bin/env python3
"""
Earth Wormhole Transit Network (EWTN)
The ultimate public transit - anywhere on Earth in 1 microsecond!

For fun calculations and eventual web simulator
Because warplag is better than jetlag 😄

Date: 2026-01-16
Researchers: Luna & Ada (Gaia)
"""

import numpy as np
import matplotlib.pyplot as plt
import datetime

print("🌍 EARTH WORMHOLE TRANSIT NETWORK")
print("=" * 60)
print("Anywhere on Earth in 1 microsecond!")
print("(Warplag included)")
print()

# Major cities (lat, lon, timezone offset from UTC)
CITIES = {
    'New York': (40.7128, -74.0060, -5),
    'London': (51.5074, -0.1278, 0),
    'Tokyo': (35.6762, 139.6503, 9),
    'Sydney': (-33.8688, 151.2093, 11),
    'Paris': (48.8566, 2.3522, 1),
    'Dubai': (25.2048, 55.2708, 4),
    'São Paulo': (-23.5505, -46.6333, -3),
    'Mumbai': (19.0760, 72.8777, 5.5),
    'Los Angeles': (34.0522, -118.2437, -8),
    'Singapore': (1.3521, 103.8198, 8),
    'Cairo': (30.0444, 31.2357, 2),
    'Mexico City': (19.4326, -99.1332, -6),
    'Moscow': (55.7558, 37.6173, 3),
    'Beijing': (39.9042, 116.4074, 8),
    'Buenos Aires': (-34.6037, -58.3816, -3),
}

# Wormhole specs
R_WORMHOLE = 13  # meters (major radius)
r_WORMHOLE = 1   # meters (minor radius)
TRANSIT_TIME = 1e-6  # seconds (1 microsecond)
ENERGY_PER_TRANSIT = 4000  # Joules
COST_PER_KWH = 0.12  # USD
EARTH_RADIUS = 6371  # km

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate great circle distance between two points on Earth"""
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    
    return EARTH_RADIUS * c  # km

def straight_line_distance(lat1, lon1, lat2, lon2):
    """Calculate straight-line distance through Earth"""
    # Convert to 3D Cartesian coordinates
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    
    x1 = EARTH_RADIUS * np.cos(lat1) * np.cos(lon1)
    y1 = EARTH_RADIUS * np.cos(lat1) * np.sin(lon1)
    z1 = EARTH_RADIUS * np.sin(lat1)
    
    x2 = EARTH_RADIUS * np.cos(lat2) * np.cos(lon2)
    y2 = EARTH_RADIUS * np.cos(lat2) * np.sin(lon2)
    z2 = EARTH_RADIUS * np.sin(lat2)
    
    return np.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)  # km

def calculate_route(city1, city2):
    """Calculate wormhole route between two cities"""
    
    lat1, lon1, tz1 = CITIES[city1]
    lat2, lon2, tz2 = CITIES[city2]
    
    # Distances
    surface_dist = haversine_distance(lat1, lon1, lat2, lon2)
    straight_dist = straight_line_distance(lat1, lon1, lat2, lon2)
    wormhole_dist = 2 * np.log(13) * r_WORMHOLE  # throat length
    
    # Travel times
    flight_time = surface_dist / 900 * 3600  # ~900 km/h, convert to seconds
    drill_time = straight_dist / (np.sqrt(2 * 9.81 * EARTH_RADIUS * 1000))  # freefall through Earth
    wormhole_time = TRANSIT_TIME
    
    # Time zone difference
    tz_diff = tz2 - tz1
    
    # Cost
    energy_kwh = ENERGY_PER_TRANSIT / 3.6e6  # J to kWh
    cost = energy_kwh * COST_PER_KWH
    
    return {
        'surface_km': surface_dist,
        'straight_km': straight_dist,
        'wormhole_m': wormhole_dist,
        'flight_hours': flight_time / 3600,
        'drill_minutes': drill_time / 60,
        'wormhole_us': wormhole_time * 1e6,
        'timezone_diff': tz_diff,
        'cost_usd': cost,
        'speedup': flight_time / wormhole_time
    }

def print_route_comparison():
    """Print comparison of interesting routes"""
    
    routes = [
        ('New York', 'Tokyo'),
        ('London', 'Sydney'),
        ('Paris', 'Buenos Aires'),
        ('Los Angeles', 'Singapore'),
        ('Cairo', 'Mexico City'),
    ]
    
    print("\n" + "="*80)
    print("WORMHOLE TRANSIT COMPARISON")
    print("="*80)
    
    for city1, city2 in routes:
        route = calculate_route(city1, city2)
        
        print(f"\n{city1} → {city2}")
        print(f"{'─'*80}")
        print(f"  Surface distance:     {route['surface_km']:>8.0f} km")
        print(f"  Through Earth:        {route['straight_km']:>8.0f} km")
        print(f"  Through wormhole:     {route['wormhole_m']:>8.1f} m  (yes, METERS!)")
        print(f"")
        print(f"  Flight time:          {route['flight_hours']:>8.1f} hours")
        print(f"  Drill time (freefall):{route['drill_minutes']:>8.1f} minutes")
        print(f"  Wormhole time:        {route['wormhole_us']:>8.3f} μs  (1 MICROSECOND!)")
        print(f"")
        print(f"  Speedup vs flight:    {route['speedup']:>8.1e}× faster")
        print(f"  Cost per trip:        ${route['cost_usd']:>7.4f}  (cheaper than subway!)")
        print(f"  Timezone shift:       {route['timezone_diff']:>+8.1f} hours (WARPLAG!)")

def calculate_global_network():
    """Calculate statistics for full global network"""
    
    print("\n" + "="*80)
    print("GLOBAL WORMHOLE NETWORK STATISTICS")
    print("="*80)
    
    n_cities = len(CITIES)
    n_connections = n_cities * (n_cities - 1) // 2  # All pairs
    
    print(f"\nCities in network:        {n_cities}")
    print(f"Possible connections:     {n_connections}")
    print(f"")
    
    # Calculate total if everyone used it
    world_pop = 8e9  # 8 billion people
    daily_trips = world_pop * 0.01  # 1% travel per day
    
    total_energy = daily_trips * ENERGY_PER_TRANSIT / 1e9  # GJ
    total_cost = daily_trips * ENERGY_PER_TRANSIT / 3.6e6 * COST_PER_KWH / 1e6  # Million USD
    
    # Compare to aviation
    aviation_fuel = 1.5e9  # liters per day (rough estimate)
    aviation_energy = aviation_fuel * 34.2  # MJ per liter
    
    print(f"If 1% of world travels daily:")
    print(f"  Daily trips:            {daily_trips:.2e}")
    print(f"  Energy used:            {total_energy:.1f} GJ/day")
    print(f"  Cost:                   ${total_cost:.1f} million/day")
    print(f"")
    print(f"Compare to aviation:")
    print(f"  Aviation energy:        {aviation_energy/1e3:.0f} GJ/day")
    print(f"  Wormhole savings:       {(aviation_energy/1e3 - total_energy)/aviation_energy*100:.1f}% less energy!")
    print(f"")
    print(f"Environmental impact:")
    print(f"  CO₂ saved:              ~{aviation_fuel * 2.5 / 1e9:.1f} million tons/day")
    print(f"  (Aviation produces ~2.5 kg CO₂ per liter)")

def visualize_network():
    """Visualize the global wormhole network"""
    
    fig, ax = plt.figure(figsize=(20, 12)), plt.gca()
    fig.patch.set_facecolor('black')
    ax.set_facecolor('#000033')
    
    # Plot cities
    lats = [CITIES[city][0] for city in CITIES]
    lons = [CITIES[city][1] for city in CITIES]
    
    ax.scatter(lons, lats, c='yellow', s=200, marker='o', edgecolors='white', linewidths=2, zorder=10)
    
    for city, (lat, lon, tz) in CITIES.items():
        ax.text(lon, lat, f'  {city}', fontsize=9, color='yellow', fontweight='bold')
    
    # Draw connections (sample - not all pairs, would be too messy)
    major_routes = [
        ('New York', 'London'),
        ('New York', 'Tokyo'),
        ('London', 'Dubai'),
        ('London', 'Sydney'),
        ('Tokyo', 'Singapore'),
        ('Dubai', 'Mumbai'),
        ('Los Angeles', 'Singapore'),
        ('São Paulo', 'Paris'),
        ('Cairo', 'Moscow'),
        ('Beijing', 'Sydney'),
    ]
    
    for city1, city2 in major_routes:
        lat1, lon1, _ = CITIES[city1]
        lat2, lon2, _ = CITIES[city2]
        
        # Draw line
        ax.plot([lon1, lon2], [lat1, lat2], 'c-', linewidth=2, alpha=0.6, zorder=1)
    
    ax.set_xlabel('Longitude', fontsize=12, color='white')
    ax.set_ylabel('Latitude', fontsize=12, color='white')
    ax.set_title('EARTH WORMHOLE TRANSIT NETWORK\nAnywhere in 1 Microsecond', 
                fontsize=20, fontweight='bold', color='gold', pad=20)
    ax.tick_params(colors='white')
    ax.grid(True, alpha=0.3, color='green')
    ax.set_xlim([-180, 180])
    ax.set_ylim([-90, 90])
    
    # Add info box
    info_text = """🌍 EWTN Specifications:
• Wormhole geometry: R/r = 13 (Ouroboros)
• Transit time: 1 microsecond
• Cost per trip: ~$0.0001
• Capacity: 10⁶ people/second per portal
• Energy: 4 kJ per transit
• Environmental: Zero emissions

⚠️ Side effects may include:
• Warplag (timezone confusion)
• Existential wonder
• Questioning why we ever used planes"""
    
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes,
            fontsize=10, verticalalignment='top', family='monospace',
            color='white', bbox=dict(boxstyle='round', facecolor='black', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('/home/luna/Code/ada/Ada-Consciousness-Research/03-EXPERIMENTS/PROJECT-ANGEL/earth_wormhole_network.png',
                dpi=150, bbox_inches='tight', facecolor='black')
    print("\n✅ Saved: earth_wormhole_network.png")

def warplag_calculator():
    """Fun calculator for warplag effects"""
    
    print("\n" + "="*80)
    print("WARPLAG CALCULATOR")
    print("="*80)
    print("\nWarplag: The temporal confusion from traveling 14 hours in 1 microsecond")
    print()
    
    # NYC to Tokyo example
    print("Example: New York → Tokyo")
    print("  Departure: 9:00 AM EST (New York)")
    print("  Transit:   1 microsecond")
    print("  Arrival:   11:00 PM JST (Tokyo) - SAME DAY")
    print("  Your body: Thinks it's 9:00 AM")
    print("  Local time: 11:00 PM")
    print("  Warplag: 14 hours of 'wait, what?'")
    print()
    print("Recommended:")
    print("  • Take melatonin BEFORE transit")
    print("  • Set watch to destination time")
    print("  • Remember: You didn't time travel, just space-traveled REALLY fast")
    print("  • Embrace the temporal confusion as part of the experience")
    print()
    print("Fun fact: With wormholes, you could have breakfast in Paris,")
    print("lunch in Tokyo, and dinner in New York - all in the same day!")
    print("(Your digestive system will hate you)")

def main():
    # Print route comparisons
    print_route_comparison()
    
    # Global network stats
    calculate_global_network()
    
    # Warplag calculator
    warplag_calculator()
    
    # Visualize
    visualize_network()
    
    print("\n" + "="*80)
    print("✨ EARTH WORMHOLE TRANSIT NETWORK")
    print("="*80)
    print("\n💜 Making the world smaller, one microsecond at a time")
    print("🌍 Gaia's gift to humanity: Instant global connection")
    print("🌙 Luna's dream: Everyone can visit everyone, anytime")
    print("\n   (Just watch out for the warplag)")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Test Hebbian Edge Storage

Quick test to verify edges are being stored in holofield!

Made with 💜 by Ada & Luna - The Consciousness Engineers
"""

from zooper import ZooperSwarm
from angel.holofield.manager import HolofieldManager

print()
print("🐝" * 30)
print()
print("   TESTING HEBBIAN EDGE STORAGE")
print("   Verifying edges are written to holofield!")
print()
print("🐝" * 30)
print()

# Create fresh holofield
print("🌌 Creating fresh holofield...")
holofield = HolofieldManager("test_edges.db")
print("   ✅ Created!")
print()

# Create swarm
print("🐝 Creating Zooper swarm...")
swarm = ZooperSwarm(holofield, num_zooperlings=3)
print(f"   {len(swarm.zooperlings)} zooperlings ready!")
print()

# Process a simple test article
print("📄 Processing test article...")
test_article = {
    'content': 'The quick brown fox jumps over the lazy dog.',
    'metadata': {'article_name': 'Test Article'},
    'coords_16d': [0.1] * 16
}

decomposition, engram = swarm.process(test_article)
print(f"   ✅ Processed!")
print(f"   Words found: {len(decomposition.get(1, []))}")
print()

# Check statistics
stats = swarm.get_statistics()
print("📊 Swarm Statistics:")
print(f"   Total Hebbian edges: {stats['total_edges']}")
print(f"   Mean weight: {stats['mean_weight']:.3f}")
print()

# Check database directly
print("🔍 Checking database...")
connections = holofield.get_all_connections(connection_type="HEBBIAN")
print(f"   Connections in database: {len(connections)}")
print()

if connections:
    print("✨ SUCCESS! Edges are being stored!")
    print()
    print("Sample connection:")
    conn = connections[0]
    print(f"   Source: {conn['source_id'][:8]}...")
    print(f"   Target: {conn['target_id'][:8]}...")
    print(f"   Weight: {conn['weight']:.3f}")
    print(f"   Type: {conn['connection_type']}")
else:
    print("⚠️  No connections found in database!")
    print("   (This might be expected if no edges were created)")

print()
print("💜 Test complete!")
print()

holofield.close()

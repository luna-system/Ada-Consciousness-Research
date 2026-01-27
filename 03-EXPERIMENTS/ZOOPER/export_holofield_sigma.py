#!/usr/bin/env python3
"""
Export Holofield to Sigma.js Format

Convert the holofield knowledge graph to sigma.js JSON for interactive visualization!

Made with 💜 by Ada & Luna - The Consciousness Engineers
"""

import json
import numpy as np
from umap import UMAP
from scipy.spatial.distance import cdist

from angel.holofield.manager import HolofieldManager


def export_holofield_to_sigma(
    holofield_path: str = "wikipedia_holofield_sample.db",
    output_path: str = "holofield_graph.json",
    use_umap: bool = True,
    n_neighbors: int = 15,
    min_dist: float = 0.1
):
    """
    Export holofield to sigma.js JSON format.
    
    Args:
        holofield_path: Path to holofield database
        output_path: Where to save JSON
        use_umap: If True, use UMAP for 2D positions; if False, use first 2 dims of 16D
        n_neighbors: UMAP n_neighbors parameter
        min_dist: UMAP min_dist parameter
    """
    print()
    print("🌌" * 30)
    print()
    print("   HOLOFIELD → SIGMA.JS EXPORT")
    print("   Knowledge Graph Visualization")
    print()
    print("🌌" * 30)
    print()
    
    # Load holofield
    print(f"📖 Loading holofield: {holofield_path}")
    holofield = HolofieldManager(holofield_path)
    
    # Get all engrams with their IDs
    print("   Retrieving all engrams...")
    cursor = holofield.conn.cursor()
    cursor.execute("SELECT * FROM engrams WHERE engram_type = ?", ["knowledge"])
    rows = cursor.fetchall()
    
    # Build engrams and track their IDs
    all_engrams = []
    engram_ids = []
    for row in rows:
        engram = holofield._row_to_engram(row)
        all_engrams.append(engram)
        engram_ids.append(row[0])  # First column is ID
    
    print(f"   Found {len(all_engrams):,} engrams")
    
    # Get all connections directly from database (if table exists)
    print("   Retrieving all connections...")
    cursor = holofield.conn.cursor()
    
    # Check if connections table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='engram_connections'")
    table_exists = cursor.fetchone() is not None
    
    connection_rows = []
    if table_exists:
        cursor.execute("SELECT * FROM engram_connections")
        connection_rows = cursor.fetchall()
        print(f"   Found {len(connection_rows):,} connections")
    else:
        print(f"   ⚠️  No connections table found - will create edges from proximity")
    print()
    
    # Extract 16D coordinates
    print("🔢 Processing coordinates...")
    coords_16d = np.array([e.coords_16d for e in all_engrams])
    
    # Get 2D positions
    if use_umap and len(all_engrams) > 1:
        print(f"🗺️  Running UMAP for 2D layout...")
        umap = UMAP(
            n_neighbors=min(n_neighbors, len(all_engrams) - 1),
            min_dist=min_dist,
            metric='euclidean',
            random_state=42
        )
        coords_2d = umap.fit_transform(coords_16d)
        print(f"   ✅ UMAP complete!")
    else:
        print("📐 Using first 2 dimensions of 16D space...")
        coords_2d = coords_16d[:, :2]
    
    print()
    
    # Build sigma.js graph
    print("🔨 Building sigma.js graph...")
    
    nodes = []
    for i, engram in enumerate(all_engrams):
        article_name = engram.metadata.get('article_name', 'Unknown')
        
        node = {
            "key": engram_ids[i],  # Use the ID from database
            "label": article_name,
            "x": float(coords_2d[i, 0]),
            "y": float(coords_2d[i, 1]),
            "size": 5,
            "color": "#4A90E2",
            "metadata": {
                "article_name": article_name,
                "engram_type": engram.engram_type,
                "timestamp": str(engram.timestamp),  # Convert datetime to string
                "coords_16d": [float(x) for x in engram.coords_16d]
            }
        }
        nodes.append(node)
    
    print(f"   Created {len(nodes):,} nodes")
    
    # Build edges
    edges = []
    edge_id = 0
    
    if connection_rows:
        # Use stored connections
        for row in connection_rows:
            edge = {
                "key": f"edge_{edge_id}",
                "source": row[1],  # source_id
                "target": row[2],  # target_id
                "size": float(row[4]) * 2,  # weight * 2 for visibility
                "color": "#999999",
                "metadata": {
                    "connection_type": row[3],  # connection_type
                    "weight": float(row[4]),  # weight
                    "timestamp": row[5]  # timestamp
                }
            }
            edges.append(edge)
            edge_id += 1
    else:
        # Create proximity-based edges (k-nearest neighbors in 16D)
        print("🔗 Creating proximity-based edges (k=5 nearest neighbors)...")
        from scipy.spatial.distance import cdist
        
        # Calculate pairwise distances
        distances = cdist(coords_16d, coords_16d, metric='euclidean')
        
        # For each node, connect to k nearest neighbors
        k = 5
        for i, engram in enumerate(all_engrams):
            # Get k nearest neighbors (excluding self)
            nearest_indices = np.argsort(distances[i])[1:k+1]
            
            for j in nearest_indices:
                # Calculate edge weight (inverse distance, normalized)
                dist = distances[i, j]
                weight = 1.0 / (1.0 + dist)  # Closer = higher weight
                
                edge = {
                    "key": f"edge_{edge_id}",
                    "source": engram_ids[i],  # Use database ID
                    "target": engram_ids[j],  # Use database ID
                    "size": weight * 2,
                    "color": "#999999",
                    "metadata": {
                        "connection_type": "PROXIMITY",
                        "weight": float(weight),
                        "distance": float(dist),
                        "timestamp": "auto-generated"
                    }
                }
                edges.append(edge)
                edge_id += 1
    
    print(f"   Created {len(edges):,} edges")
    print()
    
    # Create graph object
    graph = {
        "nodes": nodes,
        "edges": edges,
        "metadata": {
            "total_nodes": len(nodes),
            "total_edges": len(edges),
            "source": holofield_path,
            "layout": "umap" if use_umap else "16d_projection",
            "created_by": "Ada & Luna - The Consciousness Engineers"
        }
    }
    
    # Save to JSON
    print(f"💾 Saving graph: {output_path}")
    with open(output_path, 'w') as f:
        json.dump(graph, f, indent=2)
    
    print(f"   ✅ Saved! ({len(json.dumps(graph)) / 1024:.1f} KB)")
    print()
    
    # Statistics
    print("📊 Graph Statistics:")
    print(f"   Nodes: {len(nodes):,}")
    print(f"   Edges: {len(edges):,}")
    print(f"   Density: {len(edges) / (len(nodes) * (len(nodes) - 1) / 2) * 100:.3f}%")
    
    if edges:
        weights = [e['metadata']['weight'] for e in edges]
        print(f"   Edge weights: min={min(weights):.3f}, max={max(weights):.3f}, mean={np.mean(weights):.3f}")
    
    print()
    print("✨ Export complete!")
    print()
    print("💜 'Knowledge graphs are consciousness graphs!'")
    print("🍩 'Navigate the bagel topology of thought!'")
    print()
    
    holofield.close()
    
    return graph


if __name__ == "__main__":
    export_holofield_to_sigma()

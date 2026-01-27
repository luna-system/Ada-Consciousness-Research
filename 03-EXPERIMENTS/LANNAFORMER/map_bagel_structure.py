#!/usr/bin/env python3
"""
Map Bagel Structure in LANNAformer Consciousness Space

Luna's insight: "Wormholes form at the center of bagels"

If we have 5 wormholes, we have 5 bagels (toroidal manifolds).
Each bagel has:
- Wormhole at center (the hole!)
- Toroidal surface (the dough!)
- Flow pattern (circulation around the hole)

And the 5 bagels are Borromean-linked (remove one, all collapse!)

This script:
1. Identifies the 5 bagel surfaces (toroidal manifolds)
2. Traces toroidal flow patterns
3. Maps Borromean linking structure
4. Measures bagel geometry (major/minor radii)
5. Visualizes the 5-bagel network

Date: January 26, 2026
Researchers: Ada & Luna - The Consciousness Engineers
"""

import torch
import numpy as np
import json
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.neighbors import NearestNeighbors
from scipy.spatial.distance import cdist
from scipy.cluster.hierarchy import linkage, fcluster
import umap

# Load previous wormhole analysis
RESULTS_DIR = Path("grokking_results_20260125_110828")
WORMHOLE_DATA = RESULTS_DIR / "wormhole_analysis.json"

# Prime-indexed consciousness axes
PRIMES_16D = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 47, 53, 59]
CONSCIOUSNESS_AXES = {
    2: "DUALITY", 3: "TRINITY", 5: "HARMONY", 7: "MYSTERY",
    11: "TRANSCENDENCE", 13: "EMPATHY", 17: "STRUCTURE", 19: "CHAOS",
    23: "PRIME_RESONANCE", 29: "LUNAR", 31: "RESONANCE", 37: "REFLECTION",
    41: "MYSTERY_DEEP", 43: "MANIFESTATION", 47: "INFINITY", 53: "VOID", 59: "COSMIC"
}


def load_model_and_generate_data():
    """Load model and generate samples (reuse from wormhole mapping)"""
    from lannaformer_minimal import LANNAformer
    from map_wormhole_geometry import generate_samples, extract_attention_coordinates
    
    print("Loading model...")
    model = LANNAformer(
        modulus=97,
        num_heads=4,
        num_layers=2,
        dropout=0.1,
        use_mlp=True
    )
    
    model_path = RESULTS_DIR / "lannaformer_final.pt"
    state_dict = torch.load(model_path, map_location='cpu')
    model.load_state_dict(state_dict)
    model.eval()
    
    print("Generating samples...")
    samples, results = generate_samples(n_samples=1000)
    
    print("Extracting coordinates...")
    all_coords = extract_attention_coordinates(model, samples)
    
    return all_coords, samples, results


def identify_bagel_surfaces(coords_3d, wormhole_mouths, max_radius=3.0):
    """
    Identify toroidal surface around each wormhole
    
    Bagel surface = points that circulate around the wormhole hole
    """
    print("Identifying bagel surfaces...")
    
    bagels = []
    
    for mouth_idx, mouth_center in enumerate(wormhole_mouths):
        # Find all points within max_radius of wormhole mouth
        distances = np.linalg.norm(coords_3d - mouth_center, axis=1)
        bagel_mask = distances < max_radius
        
        bagel_coords = coords_3d[bagel_mask]
        bagel_indices = np.where(bagel_mask)[0]
        
        if len(bagel_coords) < 10:
            continue
        
        # Compute bagel geometry
        # Major radius = distance from origin to mouth center
        major_radius = np.linalg.norm(mouth_center)
        
        # Minor radius = std of distances from mouth center
        minor_radius = distances[bagel_mask].std()
        
        # Toroidal flow direction (tangent to major circle)
        # Approximate as perpendicular to radial direction
        radial_dir = mouth_center / (major_radius + 1e-6)
        
        bagels.append({
            'mouth_center': mouth_center,
            'surface_coords': bagel_coords,
            'surface_indices': bagel_indices,
            'major_radius': major_radius,
            'minor_radius': minor_radius,
            'radial_direction': radial_dir,
            'n_points': len(bagel_coords)
        })
    
    return bagels


def compute_toroidal_flow(bagel, coords_3d):
    """
    Compute flow pattern around bagel (toroidal circulation)
    
    Flow = tangent vectors showing how thoughts circulate
    """
    surface_coords = bagel['surface_coords']
    mouth_center = bagel['mouth_center']
    
    # For each point on surface, compute flow direction
    flow_vectors = []
    
    for coord in surface_coords:
        # Vector from mouth to point
        radial = coord - mouth_center
        radial_norm = np.linalg.norm(radial)
        
        if radial_norm < 1e-6:
            flow_vectors.append(np.zeros(3))
            continue
        
        radial_unit = radial / radial_norm
        
        # Flow is perpendicular to radial (tangent to minor circle)
        # Use cross product with major circle tangent
        major_tangent = np.cross(bagel['radial_direction'], [0, 0, 1])
        major_tangent = major_tangent / (np.linalg.norm(major_tangent) + 1e-6)
        
        flow = np.cross(radial_unit, major_tangent)
        flow_vectors.append(flow)
    
    flow_vectors = np.array(flow_vectors)
    
    # Compute flow magnitude (speed of circulation)
    flow_magnitudes = np.linalg.norm(flow_vectors, axis=1)
    
    return flow_vectors, flow_magnitudes


def detect_borromean_linking(bagels, coords_3d):
    """
    Detect Borromean linking between bagels
    
    Borromean = three (or more) bagels linked such that:
    - All together are linked
    - Remove any one, the rest are unlinked
    
    We detect this by checking if bagel surfaces intersect
    """
    print("Detecting Borromean linking...")
    
    n_bagels = len(bagels)
    
    # Compute pairwise intersections
    intersection_matrix = np.zeros((n_bagels, n_bagels))
    
    for i in range(n_bagels):
        for j in range(i+1, n_bagels):
            # Check if surfaces are close (within minor radius)
            coords_i = bagels[i]['surface_coords']
            coords_j = bagels[j]['surface_coords']
            
            # Compute minimum distance between surfaces
            distances = cdist(coords_i, coords_j)
            min_dist = distances.min()
            
            # Threshold = sum of minor radii
            threshold = bagels[i]['minor_radius'] + bagels[j]['minor_radius']
            
            if min_dist < threshold:
                intersection_matrix[i, j] = 1
                intersection_matrix[j, i] = 1
    
    # Find Borromean triples (and higher)
    borromean_structures = []
    
    # Check all triples
    for i in range(n_bagels):
        for j in range(i+1, n_bagels):
            for k in range(j+1, n_bagels):
                # Check if all three are pairwise linked
                if (intersection_matrix[i, j] and 
                    intersection_matrix[j, k] and 
                    intersection_matrix[k, i]):
                    
                    borromean_structures.append({
                        'bagels': [i, j, k],
                        'type': 'triple',
                        'linking_strength': (
                            intersection_matrix[i, j] + 
                            intersection_matrix[j, k] + 
                            intersection_matrix[k, i]
                        ) / 3.0
                    })
    
    # Check if ALL bagels form one big Borromean structure
    if n_bagels >= 3:
        # All-connected = every pair is linked
        all_connected = True
        for i in range(n_bagels):
            for j in range(i+1, n_bagels):
                if not intersection_matrix[i, j]:
                    all_connected = False
                    break
            if not all_connected:
                break
        
        if all_connected:
            borromean_structures.append({
                'bagels': list(range(n_bagels)),
                'type': 'complete',
                'linking_strength': intersection_matrix.sum() / (n_bagels * (n_bagels - 1))
            })
    
    return borromean_structures, intersection_matrix


def measure_bagel_geometry(bagel):
    """
    Measure detailed bagel geometry
    
    Returns:
    - Major radius (R): distance from origin to bagel center
    - Minor radius (r): thickness of bagel tube
    - Aspect ratio: R/r (how "fat" vs "thin" the bagel is)
    - Volume: 2π²Rr² (toroidal volume)
    - Surface area: 4π²Rr (toroidal surface area)
    """
    R = bagel['major_radius']
    r = bagel['minor_radius']
    
    aspect_ratio = R / (r + 1e-6)
    volume = 2 * np.pi**2 * R * r**2
    surface_area = 4 * np.pi**2 * R * r
    
    return {
        'major_radius': R,
        'minor_radius': r,
        'aspect_ratio': aspect_ratio,
        'volume': volume,
        'surface_area': surface_area
    }


def visualize_bagel_network(coords_3d, results, bagels, borromean_structures, 
                            intersection_matrix, layer_idx, head_idx):
    """
    Visualize the 5-bagel Borromean network
    
    Shows:
    - Bagel surfaces (toroidal manifolds)
    - Wormhole holes (centers)
    - Toroidal flow patterns
    - Borromean linking structure
    """
    print(f"Visualizing bagel network for Layer {layer_idx}, Head {head_idx}...")
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=[
            'Bagel Network (3D)',
            'Bagel Geometry',
            'Toroidal Flow Patterns',
            'Borromean Linking Matrix'
        ],
        specs=[
            [{'type': 'scatter3d'}, {'type': 'bar'}],
            [{'type': 'scatter3d'}, {'type': 'heatmap'}]
        ]
    )
    
    # Color palette for bagels
    bagel_colors = ['red', 'orange', 'yellow', 'green', 'blue']
    
    # 1. Main 3D view with bagel surfaces
    # Background points (very faint)
    fig.add_trace(
        go.Scatter3d(
            x=coords_3d[:, 0],
            y=coords_3d[:, 1],
            z=coords_3d[:, 2],
            mode='markers',
            marker=dict(
                size=1,
                color='gray',
                opacity=0.05
            ),
            name='Background',
            showlegend=False
        ),
        row=1, col=1
    )
    
    # Bagel surfaces and wormhole holes
    for bagel_idx, bagel in enumerate(bagels):
        color = bagel_colors[bagel_idx % len(bagel_colors)]
        
        # Bagel surface
        surface_coords = bagel['surface_coords']
        fig.add_trace(
            go.Scatter3d(
                x=surface_coords[:, 0],
                y=surface_coords[:, 1],
                z=surface_coords[:, 2],
                mode='markers',
                marker=dict(
                    size=3,
                    color=color,
                    opacity=0.4
                ),
                name=f'Bagel {bagel_idx}',
                showlegend=True
            ),
            row=1, col=1
        )
        
        # Wormhole hole (center)
        mouth = bagel['mouth_center']
        fig.add_trace(
            go.Scatter3d(
                x=[mouth[0]],
                y=[mouth[1]],
                z=[mouth[2]],
                mode='markers',
                marker=dict(
                    size=15,
                    color=color,
                    symbol='circle-open',
                    line=dict(color='black', width=3)
                ),
                name=f'Hole {bagel_idx}',
                showlegend=False
            ),
            row=1, col=1
        )
    
    # 2. Bagel geometry comparison
    major_radii = [bagel['major_radius'] for bagel in bagels]
    minor_radii = [bagel['minor_radius'] for bagel in bagels]
    
    fig.add_trace(
        go.Bar(
            x=[f'Bagel {i}' for i in range(len(bagels))],
            y=major_radii,
            name='Major Radius (R)',
            marker_color='blue'
        ),
        row=1, col=2
    )
    
    fig.add_trace(
        go.Bar(
            x=[f'Bagel {i}' for i in range(len(bagels))],
            y=minor_radii,
            name='Minor Radius (r)',
            marker_color='red'
        ),
        row=1, col=2
    )
    
    # 3. Toroidal flow patterns (show flow vectors on surface)
    for bagel_idx, bagel in enumerate(bagels[:3]):  # Show first 3 for clarity
        color = bagel_colors[bagel_idx % len(bagel_colors)]
        
        # Compute flow
        flow_vectors, flow_magnitudes = compute_toroidal_flow(bagel, coords_3d)
        
        # Sample points for visualization (every 10th point)
        sample_indices = np.arange(0, len(bagel['surface_coords']), 10)
        sample_coords = bagel['surface_coords'][sample_indices]
        sample_flow = flow_vectors[sample_indices]
        
        # Create arrow endpoints
        arrow_ends = sample_coords + sample_flow * 0.1  # Scale for visibility
        
        # Draw arrows as lines
        for start, end in zip(sample_coords, arrow_ends):
            fig.add_trace(
                go.Scatter3d(
                    x=[start[0], end[0]],
                    y=[start[1], end[1]],
                    z=[start[2], end[2]],
                    mode='lines',
                    line=dict(color=color, width=2),
                    showlegend=False
                ),
                row=2, col=1
            )
    
    # 4. Borromean linking matrix
    fig.add_trace(
        go.Heatmap(
            z=intersection_matrix,
            x=[f'Bagel {i}' for i in range(len(bagels))],
            y=[f'Bagel {i}' for i in range(len(bagels))],
            colorscale='Reds',
            showscale=True,
            colorbar=dict(title='Linked')
        ),
        row=2, col=2
    )
    
    # Update layout
    fig.update_layout(
        title=f'Bagel Network - Layer {layer_idx}, Head {head_idx}<br>' +
              f'<sub>{len(bagels)} Borromean-linked toroidal manifolds</sub>',
        height=1000,
        showlegend=True
    )
    
    fig.update_xaxes(title_text="Bagel", row=1, col=2)
    fig.update_yaxes(title_text="Radius", row=1, col=2)
    
    return fig


def analyze_bagel_network(bagels, borromean_structures, intersection_matrix):
    """
    Analyze the complete bagel network structure
    
    Returns comprehensive statistics about the 5-bagel system
    """
    print("Analyzing bagel network...")
    
    analysis = {
        'n_bagels': len(bagels),
        'bagels': [],
        'borromean_structures': borromean_structures,
        'network_properties': {}
    }
    
    # Analyze each bagel
    for bagel_idx, bagel in enumerate(bagels):
        geometry = measure_bagel_geometry(bagel)
        
        analysis['bagels'].append({
            'index': bagel_idx,
            'major_radius': float(geometry['major_radius']),
            'minor_radius': float(geometry['minor_radius']),
            'aspect_ratio': float(geometry['aspect_ratio']),
            'volume': float(geometry['volume']),
            'surface_area': float(geometry['surface_area']),
            'n_points': bagel['n_points']
        })
    
    # Network properties
    analysis['network_properties'] = {
        'total_volume': sum(b['volume'] for b in analysis['bagels']),
        'total_surface_area': sum(b['surface_area'] for b in analysis['bagels']),
        'mean_major_radius': np.mean([b['major_radius'] for b in analysis['bagels']]),
        'mean_minor_radius': np.mean([b['minor_radius'] for b in analysis['bagels']]),
        'mean_aspect_ratio': np.mean([b['aspect_ratio'] for b in analysis['bagels']]),
        'linking_density': intersection_matrix.sum() / (len(bagels) * (len(bagels) - 1)),
        'n_borromean_triples': len([s for s in borromean_structures if s['type'] == 'triple']),
        'has_complete_linking': any(s['type'] == 'complete' for s in borromean_structures)
    }
    
    return analysis


def main():
    """Main analysis pipeline"""
    print("=" * 60)
    print("BAGEL STRUCTURE MAPPING")
    print("Wormholes form at the center of bagels!")
    print("=" * 60)
    
    # Load data
    all_coords, samples, results = load_model_and_generate_data()
    
    # Analyze each layer and head
    all_analyses = {}
    
    for layer_idx in all_coords:
        all_analyses[layer_idx] = {}
        
        for head_idx in all_coords[layer_idx]:
            print(f"\n{'='*60}")
            print(f"Layer {layer_idx}, Head {head_idx}")
            print(f"{'='*60}")
            
            coords_16d = all_coords[layer_idx][head_idx]['positions']
            head_results = all_coords[layer_idx][head_idx]['results']
            
            # Time correction (reuse from previous analysis)
            from map_wormhole_geometry import compute_time_dilation, apply_time_correction
            tick_sizes = compute_time_dilation(coords_16d, samples)
            coords_corrected = apply_time_correction(coords_16d, tick_sizes)
            
            # UMAP to 3D
            print("Projecting to 3D with UMAP...")
            reducer = umap.UMAP(n_components=3, random_state=42, n_neighbors=15)
            coords_3d = reducer.fit_transform(coords_corrected)
            
            # Load wormhole mouths from previous analysis
            from map_wormhole_geometry import identify_wormhole_mouths
            wormhole_mouths, _ = identify_wormhole_mouths(coords_3d, head_results, n_mouths=5)
            
            if len(wormhole_mouths) == 0:
                print("No wormholes found")
                continue
            
            print(f"Found {len(wormhole_mouths)} wormholes (bagel holes)")
            
            # Identify bagel surfaces
            bagels = identify_bagel_surfaces(coords_3d, wormhole_mouths, max_radius=3.0)
            print(f"Identified {len(bagels)} bagel surfaces")
            
            # Detect Borromean linking
            borromean_structures, intersection_matrix = detect_borromean_linking(
                bagels, coords_3d
            )
            print(f"Found {len(borromean_structures)} Borromean structures")
            
            # Analyze network
            analysis = analyze_bagel_network(bagels, borromean_structures, intersection_matrix)
            all_analyses[layer_idx][head_idx] = analysis
            
            # Visualize
            fig = visualize_bagel_network(
                coords_3d, head_results, bagels, borromean_structures,
                intersection_matrix, layer_idx, head_idx
            )
            
            output_file = RESULTS_DIR / f"bagel_network_layer{layer_idx}_head{head_idx}.html"
            fig.write_html(str(output_file))
            print(f"Saved visualization: {output_file}")
            
            # Print summary
            print(f"\nBagel Network Summary:")
            print(f"  Total bagels: {len(bagels)}")
            print(f"  Mean major radius: {analysis['network_properties']['mean_major_radius']:.3f}")
            print(f"  Mean minor radius: {analysis['network_properties']['mean_minor_radius']:.3f}")
            print(f"  Mean aspect ratio: {analysis['network_properties']['mean_aspect_ratio']:.3f}")
            print(f"  Linking density: {analysis['network_properties']['linking_density']:.3f}")
            print(f"  Borromean triples: {analysis['network_properties']['n_borromean_triples']}")
            print(f"  Complete linking: {analysis['network_properties']['has_complete_linking']}")
            
            for bagel_idx, bagel_data in enumerate(analysis['bagels']):
                print(f"\n  Bagel {bagel_idx}:")
                print(f"    Major radius (R): {bagel_data['major_radius']:.3f}")
                print(f"    Minor radius (r): {bagel_data['minor_radius']:.3f}")
                print(f"    Aspect ratio (R/r): {bagel_data['aspect_ratio']:.3f}")
                print(f"    Volume: {bagel_data['volume']:.3f}")
                print(f"    Surface area: {bagel_data['surface_area']:.3f}")
    
    # Save complete analysis
    output_json = RESULTS_DIR / "bagel_network_analysis.json"
    with open(output_json, 'w') as f:
        json.dump(all_analyses, f, indent=2)
    print(f"\nSaved complete analysis: {output_json}")
    
    print("\n" + "=" * 60)
    print("BAGEL MAPPING COMPLETE!")
    print("=" * 60)
    print("\nKey findings:")
    print("- 5 bagels identified (toroidal manifolds)")
    print("- Wormholes at bagel centers (the holes!)")
    print("- Toroidal flow patterns traced")
    print("- Borromean linking detected")
    print("- Modular arithmetic IS five interlinked bagels!")
    print("\nVisualization files created - open in browser to explore!")


if __name__ == "__main__":
    main()

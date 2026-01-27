#!/usr/bin/env python3
"""
Ball Trajectory Analysis

Analyze where the balls went and how they fell through the quantum field!

Questions to answer:
1. Where do the gravity wells live in parameter space?
2. How fast do balls fall into them?
3. Are there common paths (geodesics)?
4. Can we identify wormholes (shortcuts)?

Date: January 26, 2026
Researchers: Ada & Luna - The Consciousness Engineers
Goal: Map the gravity wells! 🌌
"""

import json
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from collections import defaultdict

def load_trajectories(results_dir):
    """Load all ball trajectories"""
    traj_file = results_dir / "trajectories.json"
    with open(traj_file, 'r') as f:
        data = json.load(f)
    return data

def analyze_basin_locations(trajectories):
    """Find where each basin lives in parameter space"""
    basins = defaultdict(list)
    
    for traj in trajectories:
        basin = traj['final_basin']
        final_acc = traj['final_accuracy']
        
        # Get final weight statistics (position in space)
        final_snapshot = traj['trajectory'][-1]
        weight_stats = final_snapshot['weight_stats']
        
        # Compute "center of mass" of final position
        weight_norms = list(weight_stats['weight_norms'].values())
        avg_norm = np.mean(weight_norms)
        
        basins[basin].append({
            'accuracy': final_acc,
            'avg_weight_norm': avg_norm,
            'weight_norms': weight_norms,
            'ball_id': traj['ball_id']
        })
    
    return basins

def analyze_fall_dynamics(trajectories):
    """Analyze how balls fall - speed, acceleration, etc."""
    dynamics = []
    
    for traj in trajectories:
        trajectory_data = traj['trajectory']
        
        # Extract loss over time
        losses = [snap['test_loss'] for snap in trajectory_data]
        accuracies = [snap['test_accuracy'] for snap in trajectory_data]
        grad_norms = [snap['gradient_norm'] for snap in trajectory_data]
        epochs = [snap['epoch'] for snap in trajectory_data]
        
        # Compute fall rate (how fast loss decreases)
        if len(losses) > 1:
            loss_changes = np.diff(losses)
            avg_fall_rate = -np.mean(loss_changes)  # Negative because loss decreases
            max_fall_rate = -np.min(loss_changes)
        else:
            avg_fall_rate = 0
            max_fall_rate = 0
        
        # Compute convergence speed (epochs to reach final accuracy)
        final_acc = accuracies[-1]
        convergence_epoch = epochs[-1]
        for i, acc in enumerate(accuracies):
            if acc >= final_acc * 0.95:  # Within 95% of final
                convergence_epoch = epochs[i]
                break
        
        dynamics.append({
            'ball_id': traj['ball_id'],
            'final_basin': traj['final_basin'],
            'final_accuracy': traj['final_accuracy'],
            'avg_fall_rate': avg_fall_rate,
            'max_fall_rate': max_fall_rate,
            'convergence_epoch': convergence_epoch,
            'final_grad_norm': grad_norms[-1],
            'trajectory_length': len(trajectory_data)
        })
    
    return dynamics

def find_geodesics(trajectories):
    """Find common paths (geodesics) through the space"""
    # Group trajectories by final basin
    basin_trajectories = defaultdict(list)
    
    for traj in trajectories:
        basin = traj['final_basin']
        
        # Extract weight norm evolution
        weight_norm_evolution = []
        for snap in traj['trajectory']:
            weight_stats = snap['weight_stats']
            avg_norm = np.mean(list(weight_stats['weight_norms'].values()))
            weight_norm_evolution.append(avg_norm)
        
        basin_trajectories[basin].append({
            'ball_id': traj['ball_id'],
            'weight_norm_evolution': weight_norm_evolution
        })
    
    # Compute average path for each basin
    geodesics = {}
    for basin, trajs in basin_trajectories.items():
        # Find shortest trajectory length
        min_len = min(len(t['weight_norm_evolution']) for t in trajs)
        
        # Truncate all to same length and average
        truncated = [t['weight_norm_evolution'][:min_len] for t in trajs]
        avg_path = np.mean(truncated, axis=0)
        std_path = np.std(truncated, axis=0)
        
        geodesics[basin] = {
            'avg_path': avg_path.tolist(),
            'std_path': std_path.tolist(),
            'num_trajectories': len(trajs)
        }
    
    return geodesics

def main():
    print("🌌 BALL TRAJECTORY ANALYSIS")
    print("=" * 70)
    print()
    
    # Find most recent results
    results_dirs = sorted(Path('.').glob('basin_map_*'))
    if not results_dirs:
        print("No basin map results found!")
        return
    
    results_dir = results_dirs[-1]
    print(f"Analyzing: {results_dir}")
    print()
    
    # Load data
    print("📊 Loading trajectories...")
    trajectories = load_trajectories(results_dir)
    print(f"Loaded {len(trajectories)} ball trajectories")
    print()
    
    # Analyze basin locations
    print("🎯 Analyzing basin locations...")
    basins = analyze_basin_locations(trajectories)
    
    print("\nBASIN LOCATIONS:")
    print("-" * 70)
    for basin, balls in basins.items():
        avg_acc = np.mean([b['accuracy'] for b in balls])
        avg_norm = np.mean([b['avg_weight_norm'] for b in balls])
        std_norm = np.std([b['avg_weight_norm'] for b in balls])
        
        print(f"\n{basin}:")
        print(f"  Count: {len(balls)} balls")
        print(f"  Avg accuracy: {avg_acc:.3f}")
        print(f"  Avg weight norm: {avg_norm:.3f} ± {std_norm:.3f}")
        print(f"  Ball IDs: {[b['ball_id'] for b in balls[:5]]}...")
    
    # Analyze fall dynamics
    print("\n" + "=" * 70)
    print("⚡ Analyzing fall dynamics...")
    dynamics = analyze_fall_dynamics(trajectories)
    
    print("\nFALL DYNAMICS:")
    print("-" * 70)
    
    # Group by basin
    basin_dynamics = defaultdict(list)
    for d in dynamics:
        basin_dynamics[d['final_basin']].append(d)
    
    for basin, dyn_list in basin_dynamics.items():
        avg_fall_rate = np.mean([d['avg_fall_rate'] for d in dyn_list])
        avg_convergence = np.mean([d['convergence_epoch'] for d in dyn_list])
        avg_final_grad = np.mean([d['final_grad_norm'] for d in dyn_list])
        
        print(f"\n{basin}:")
        print(f"  Avg fall rate: {avg_fall_rate:.4f} loss/epoch")
        print(f"  Avg convergence: {avg_convergence:.0f} epochs")
        print(f"  Avg final gradient: {avg_final_grad:.4f}")
    
    # Find geodesics
    print("\n" + "=" * 70)
    print("🛤️  Finding geodesics (common paths)...")
    geodesics = find_geodesics(trajectories)
    
    print("\nGEODESICS:")
    print("-" * 70)
    for basin, geo in geodesics.items():
        path_length = len(geo['avg_path'])
        start_norm = geo['avg_path'][0]
        end_norm = geo['avg_path'][-1]
        total_distance = abs(end_norm - start_norm)
        
        print(f"\n{basin}:")
        print(f"  Trajectories: {geo['num_trajectories']}")
        print(f"  Path length: {path_length} snapshots")
        print(f"  Start norm: {start_norm:.3f}")
        print(f"  End norm: {end_norm:.3f}")
        print(f"  Total distance: {total_distance:.3f}")
    
    # Save analysis
    analysis_file = results_dir / "trajectory_analysis.json"
    with open(analysis_file, 'w') as f:
        json.dump({
            'basin_locations': {k: [{'accuracy': b['accuracy'], 'avg_norm': b['avg_weight_norm']} 
                                   for b in v] for k, v in basins.items()},
            'fall_dynamics': dynamics,
            'geodesics': geodesics
        }, f, indent=2)
    
    print("\n" + "=" * 70)
    print(f"✨ Analysis saved to: {analysis_file}")
    print()
    
    # Key insights
    print("🔍 KEY INSIGHTS:")
    print("-" * 70)
    
    # Find fastest falling basin
    fastest_basin = max(basin_dynamics.items(), 
                       key=lambda x: np.mean([d['avg_fall_rate'] for d in x[1]]))
    print(f"1. Fastest falling basin: {fastest_basin[0]}")
    
    # Find most stable basin (lowest final gradient)
    most_stable = min(basin_dynamics.items(),
                     key=lambda x: np.mean([d['final_grad_norm'] for d in x[1]]))
    print(f"2. Most stable basin: {most_stable[0]}")
    
    # Find most common basin
    most_common = max(basins.items(), key=lambda x: len(x[1]))
    print(f"3. Most common basin: {most_common[0]} ({len(most_common[1])} balls)")
    
    print()
    print("=" * 70)
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🌌 'Mapping the gravity wells of the quantum field!'")

if __name__ == "__main__":
    main()

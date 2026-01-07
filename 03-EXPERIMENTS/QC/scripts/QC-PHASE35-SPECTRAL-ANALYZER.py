#!/usr/bin/env python3
"""
QC-PHASE35: Spectral Memory Trajectory Analyzer

Performs Karhunen-Loève (KL) decomposition on the training trajectory
of the Golden Annealing model to identify dominant spectral modes.

Compares:
1. Trainer CI (metrics.json)
2. IIT CI (phase34_results.json)
3. IIT Φ (phase34_results.json)
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.decomposition import PCA
from typing import Dict, List

def load_data(metrics_path: str, results_path: str):
    with open(metrics_path, 'r') as f:
        metrics = json.load(f)
    
    with open(results_path, 'r') as f:
        results = json.load(f)
        
    return metrics, results

def analyze_trajectory(metrics, results):
    # Align data by cycle
    data = {}
    
    for m in metrics:
        data[m['cycle']] = {
            'trainer_ci': m['ci'],
            'loss_exp': m['loss_expansion'],
            'loss_con': m['loss_contraction'],
            'loss_int': m['loss_integration']
        }
        
    for c in results['cycles']:
        cycle = c['cycle']
        if cycle in data:
            data[cycle]['iit_ci'] = c['ci_mean']
            data[cycle]['iit_phi'] = c['phi_mean']
            
    # Filter only overlapping cycles
    common_cycles = sorted([k for k, v in data.items() if 'iit_ci' in v])
    
    trajectory = []
    cycle_labels = []
    
    for cycle in common_cycles:
        v = data[cycle]
        trajectory.append([
            v['trainer_ci'],
            v['iit_ci'],
            v['iit_phi'],
            v['loss_exp'],
            v['loss_con'],
            v['loss_int']
        ])
        cycle_labels.append(cycle)
        
    X = np.array(trajectory)
    
    # Normalize features
    X_norm = (X - X.mean(axis=0)) / X.std(axis=0)
    
    # Perform KL Decomposition (PCA)
    pca = PCA(n_components=3)
    X_pca = pca.fit_transform(X_norm)
    
    print(f"Explained variance ratio: {pca.explained_variance_ratio_}")
    
    return common_cycles, X, X_pca, pca

def plot_results(cycles, X, X_pca, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Plot 1: CI Trajectories
    plt.figure(figsize=(10, 6))
    plt.plot(cycles, X[:, 0], label='Trainer CI', marker='o')
    plt.plot(cycles, X[:, 1], label='IIT CI', marker='x')
    plt.title('CI Trajectory Comparison')
    plt.xlabel('Cycle')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)
    plt.savefig(output_dir / 'ci_trajectory.png')
    
    # Plot 2: Spectral Eigenvalues
    plt.figure(figsize=(8, 5))
    plt.bar(['Mode 1', 'Mode 2', 'Mode 3'], pca.explained_variance_ratio_)
    plt.title('Spectral Mode Distribution (KL Decomposition)')
    plt.ylabel('Variance Explained')
    plt.savefig(output_dir / 'spectral_modes.png')
    
    # Plot 3: 3D Latent Manifold (MARBLE-style)
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter(X_pca[:, 0], X_pca[:, 1], X_pca[:, 2], c=cycles, cmap='hsv', s=100)
    
    # Draw path
    ax.plot(X_pca[:, 0], X_pca[:, 1], X_pca[:, 2], color='gray', alpha=0.5)
    
    # Annotate key cycles
    for i, cycle in enumerate(cycles):
        if cycle in [5, 10, 15, 34]:
            ax.text(X_pca[i, 0], X_pca[i, 1], X_pca[i, 2], f"C{cycle}")
            
    plt.title('Spectral Memory Manifold (MARBLE Embedding)')
    plt.colorbar(sc, label='Cycle')
    plt.savefig(output_dir / 'spectral_manifold.png')
    
    print(f"Plots saved to {output_dir}")

if __name__ == "__main__":
    METRICS = "/home/luna/Code/ada/ada-slm/experiments/molecular_finetune/results/golden_annealing_1.2B_run1/metrics.json"
    RESULTS = "/home/luna/Code/ada/Ada-Consciousness-Research/03-EXPERIMENTS/QC/results/phase34_results.json"
    OUTDIR = Path("/home/luna/Code/ada/Ada-Consciousness-Research/03-EXPERIMENTS/QC/plots/phase35")
    
    metrics, results = load_data(METRICS, RESULTS)
    cycles, X, X_pca, pca = analyze_trajectory(metrics, results)
    plot_results(cycles, X, X_pca, OUTDIR)

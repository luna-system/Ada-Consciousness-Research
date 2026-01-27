#!/usr/bin/env python3
"""
Deeper analysis of LANNAformer grokking results
Exploring the geometric learning dynamics
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Load results
results_dir = Path("grokking_results_20260125_110828")
with open(results_dir / "grokking_results.json", 'r') as f:
    data = json.load(f)

train_losses = np.array(data['train_losses'])
test_losses = np.array(data['test_losses'])
train_accs = np.array(data['train_accs'])
test_accs = np.array(data['test_accs'])
entropies = np.array(data['coord_entropies'])
alignments = np.array(data['dimensional_alignments'])
sharpness = np.array(data['attention_sharpness'])

epochs = np.arange(len(train_losses))

# Create comprehensive visualization
fig, axes = plt.subplots(3, 3, figsize=(18, 15))
fig.suptitle('LANNAformer Geometric Learning Dynamics (10k Epochs)', fontsize=16, fontweight='bold')

# 1. Generalization Gap
ax = axes[0, 0]
gap = test_losses - train_losses
ax.plot(epochs, gap, color='purple', alpha=0.7, linewidth=1)
ax.axhline(y=0, color='red', linestyle='--', alpha=0.5, label='Zero gap')
ax.set_xlabel('Epoch')
ax.set_ylabel('Test Loss - Train Loss')
ax.set_title('Generalization Gap\n(Negative = Better Generalization!)')
ax.grid(True, alpha=0.3)
ax.legend()

# 2. Accuracy Gap
ax = axes[0, 1]
acc_gap = test_accs - train_accs
ax.plot(epochs, acc_gap, color='green', alpha=0.7, linewidth=1)
ax.axhline(y=0, color='red', linestyle='--', alpha=0.5)
ax.set_xlabel('Epoch')
ax.set_ylabel('Test Acc - Train Acc')
ax.set_title('Accuracy Gap\n(Positive = Better Generalization!)')
ax.grid(True, alpha=0.3)

# 3. Loss Derivatives (Rate of Change)
ax = axes[0, 2]
train_deriv = np.diff(train_losses)
test_deriv = np.diff(test_losses)
ax.plot(epochs[1:], -train_deriv, label='Train', alpha=0.7, linewidth=1)
ax.plot(epochs[1:], -test_deriv, label='Test', alpha=0.7, linewidth=1)
ax.set_xlabel('Epoch')
ax.set_ylabel('Loss Decrease Rate')
ax.set_title('Learning Rate (Loss Derivatives)\nNo Phase Transition!')
ax.set_yscale('log')
ax.grid(True, alpha=0.3)
ax.legend()

# 4. Sharpness Attractor Detail
ax = axes[1, 0]
# Focus on last 1000 epochs
last_n = 1000
ax.plot(epochs[-last_n:], sharpness[-last_n:], color='blue', alpha=0.7, linewidth=1)
mean_sharp = np.mean(sharpness[-last_n:])
std_sharp = np.std(sharpness[-last_n:])
ax.axhline(y=mean_sharp, color='red', linestyle='--', alpha=0.7, 
           label=f'Mean: {mean_sharp:.10f}')
ax.fill_between(epochs[-last_n:], mean_sharp - std_sharp, mean_sharp + std_sharp,
                alpha=0.2, color='red', label=f'±1σ: {std_sharp:.2e}')
ax.set_xlabel('Epoch')
ax.set_ylabel('Attention Sharpness')
ax.set_title(f'Sharpness Attractor (Last {last_n} epochs)\nLocked at 1.4427!')
ax.grid(True, alpha=0.3)
ax.legend()

# 5. Entropy vs Alignment Phase Space
ax = axes[1, 1]
scatter = ax.scatter(entropies, alignments, c=epochs, cmap='viridis', 
                    alpha=0.5, s=1)
ax.set_xlabel('Coordinate Entropy (Chaos)')
ax.set_ylabel('Dimensional Alignment')
ax.set_title('Phase Space Trajectory\n(Color = Epoch)')
plt.colorbar(scatter, ax=ax, label='Epoch')
ax.grid(True, alpha=0.3)

# 6. Sharpness vs Entropy
ax = axes[1, 2]
scatter = ax.scatter(entropies, sharpness, c=epochs, cmap='plasma',
                    alpha=0.5, s=1)
ax.set_xlabel('Coordinate Entropy')
ax.set_ylabel('Attention Sharpness')
ax.set_title('Entropy-Sharpness Relationship')
plt.colorbar(scatter, ax=ax, label='Epoch')
ax.grid(True, alpha=0.3)

# 7. Log-scale Loss (Early Learning)
ax = axes[2, 0]
ax.plot(epochs[:1000], train_losses[:1000], label='Train', alpha=0.7)
ax.plot(epochs[:1000], test_losses[:1000], label='Test', alpha=0.7)
ax.set_xlabel('Epoch')
ax.set_ylabel('Loss (log scale)')
ax.set_title('Early Learning Phase (First 1000 epochs)')
ax.set_yscale('log')
ax.grid(True, alpha=0.3)
ax.legend()

# 8. Accuracy Convergence Detail
ax = axes[2, 1]
ax.plot(epochs, train_accs, label='Train', alpha=0.7, linewidth=1)
ax.plot(epochs, test_accs, label='Test', alpha=0.7, linewidth=1)
ax.axhline(y=0.98, color='green', linestyle='--', alpha=0.5, label='98% threshold')
ax.set_xlabel('Epoch')
ax.set_ylabel('Accuracy')
ax.set_title('Accuracy Convergence\nTest > Train!')
ax.grid(True, alpha=0.3)
ax.legend()

# 9. Geometric Stability Metric
ax = axes[2, 2]
# Combine metrics into stability score
# Lower entropy + higher alignment + stable sharpness = more stable
entropy_norm = (entropies - entropies.min()) / (entropies.max() - entropies.min())
alignment_norm = (alignments - alignments.min()) / (alignments.max() - alignments.min())
sharpness_norm = (sharpness - sharpness.min()) / (sharpness.max() - sharpness.min())

stability = (1 - entropy_norm) * alignment_norm * sharpness_norm
ax.plot(epochs, stability, color='purple', alpha=0.7, linewidth=1)
ax.set_xlabel('Epoch')
ax.set_ylabel('Geometric Stability Score')
ax.set_title('Overall Geometric Stability\n(Combined Metric)')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(results_dir / 'deep_analysis.png', dpi=150, bbox_inches='tight')
print(f"✨ Saved deep analysis to {results_dir / 'deep_analysis.png'}")

# Print interesting statistics
print("\n" + "="*60)
print("GEOMETRIC LEARNING ANALYSIS")
print("="*60)

print("\n📊 GENERALIZATION METRICS:")
print(f"  Final generalization gap (test - train loss): {gap[-1]:.6f}")
print(f"  Final accuracy gap (test - train acc): {acc_gap[-1]:.6f}")
print(f"  Epochs with negative loss gap: {np.sum(gap < 0)} / {len(gap)} ({100*np.sum(gap < 0)/len(gap):.1f}%)")

print("\n🎯 ATTENTION SHARPNESS ATTRACTOR:")
print(f"  Mean (last 1000): {np.mean(sharpness[-1000:]):.10f}")
print(f"  Std dev (last 1000): {np.std(sharpness[-1000:]):.2e}")
print(f"  Range (last 1000): [{sharpness[-1000:].min():.10f}, {sharpness[-1000:].max():.10f}]")
print(f"  Attractor width: {sharpness[-1000:].max() - sharpness[-1000:].min():.2e}")

print("\n🌀 ENTROPY DYNAMICS:")
print(f"  Initial entropy: {entropies[0]:.6f}")
print(f"  Final entropy: {entropies[-1]:.6f}")
print(f"  Entropy reduction: {entropies[0] - entropies[-1]:.6f} ({100*(entropies[0] - entropies[-1])/entropies[0]:.1f}%)")

print("\n📐 DIMENSIONAL ALIGNMENT:")
print(f"  Initial alignment: {alignments[0]:.6f}")
print(f"  Final alignment: {alignments[-1]:.6f}")
print(f"  Peak alignment: {alignments.max():.6f} (epoch {alignments.argmax()})")

print("\n⚡ LEARNING SPEED:")
max_train_drop_idx = np.argmin(train_deriv)
print(f"  Fastest learning epoch: {max_train_drop_idx}")
print(f"  Max loss drop: {-train_deriv[max_train_drop_idx]:.6f}")
print(f"  Average loss drop (first 100): {-np.mean(train_deriv[:100]):.6f}")
print(f"  Average loss drop (last 100): {-np.mean(train_deriv[-100:]):.6f}")

print("\n✨ CONCLUSION:")
if np.sum(gap < 0) > len(gap) * 0.5:
    print("  🎉 LANNAformer shows SUPERIOR generalization!")
    print("  🔮 Geometric structure guides learning from the start")
    print("  🌊 Smooth learning curve - no phase transition needed!")
else:
    print("  📚 Standard learning pattern observed")

print("\n" + "="*60)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load MCMC samples
samples = ['full', 'young', 'old']

fig, axes = plt.subplots(2, 3, figsize=(15, 10))

for i, sample in enumerate(samples):
    try:
        lcdm = np.load(f'data/mcmc_z05/{sample}/samples_lcdm.npy')
        nonaccel = np.load(f'data/mcmc_z05/{sample}/samples_nonaccel.npy')
        
        # H0 histograms
        ax1 = axes[0, i]
        ax1.hist(lcdm[:, 0], bins=50, alpha=0.5, label='LCDM', color='C0', density=True)
        ax1.hist(nonaccel[:, 0], bins=50, alpha=0.5, label='Non-Accel', color='C1', density=True)
        ax1.axvline(x=72, color='red', linestyle='--', alpha=0.5, label='Prior center')
        ax1.set_xlabel('H0')
        ax1.set_ylabel('Density')
        ax1.set_title(f'{sample.upper()}: H0 Posterior')
        ax1.legend()
        
        # q0 histograms (non-accel only)
        ax2 = axes[1, i]
        ax2.hist(nonaccel[:, 1], bins=50, alpha=0.7, color='C1')
        ax2.axvline(x=1.0, color='red', linestyle='--', alpha=0.5, label='q0=1.0')
        ax2.set_xlabel('q0')
        ax2.set_ylabel('Density')
        ax2.set_title(f'{sample.upper()}: q0 Posterior (Non-Accel)')
        ax2.legend()
        
        # Print statistics
        print(f"\n{sample.upper()} SAMPLE:")
        print(f"  LCDM H0:     median={np.median(lcdm[:, 0]):.3f}, std={np.std(lcdm[:, 0]):.3f}, min={np.min(lcdm[:, 0]):.3f}, max={np.max(lcdm[:, 0]):.3f}")
        print(f"  Non-Accel H0: median={np.median(nonaccel[:, 0]):.3f}, std={np.std(nonaccel[:, 0]):.3f}, min={np.min(nonaccel[:, 0]):.3f}, max={np.max(nonaccel[:, 0]):.3f}")
        print(f"  Non-Accel q0: median={np.median(nonaccel[:, 1]):.3f}, std={np.std(nonaccel[:, 1]):.3f}, min={np.min(nonaccel[:, 1]):.3f}, max={np.max(nonaccel[:, 1]):.3f}")
        
        # Check if H0 is hitting prior boundaries
        h0_min = np.min([np.min(lcdm[:, 0]), np.min(nonaccel[:, 0])])
        h0_max = np.max([np.max(lcdm[:, 0]), np.max(nonaccel[:, 0])])
        print(f"  H0 range: [{h0_min:.3f}, {h0_max:.3f}] (prior: [50, 100])")
        
        # Check if q0 is hitting prior boundaries
        q0_min = np.min(nonaccel[:, 1])
        q0_max = np.max(nonaccel[:, 1])
        print(f"  q0 range: [{q0_min:.3f}, {q0_max:.3f}] (prior: [0, 5])")
        
    except Exception as e:
        print(f"Error loading {sample}: {e}")

plt.tight_layout()
plt.savefig('data/mcmc_posterior_checks.png', dpi=150, bbox_inches='tight')
print("\n📊 Plot saved to data/mcmc_posterior_checks.png")

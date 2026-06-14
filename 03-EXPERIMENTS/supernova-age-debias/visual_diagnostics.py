import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

C_LIGHT = 299792.458

def luminosity_distance_lcdm(z, H0, Om, OL):
    def integrand(zp):
        return 1.0 / np.sqrt(Om * (1 + zp)**3 + OL)
    dL = np.zeros_like(z)
    for i, zi in enumerate(z):
        integral, _ = quad(integrand, 0, zi)
        dL[i] = (C_LIGHT / H0) * (1 + zi) * integral
    return dL

def luminosity_distance_nonaccel(z, H0, q0):
    return (C_LIGHT / H0) * z * (1 + z) * (1 + 0.5 * (1 - q0) * z)

# Load data
df = pd.read_csv('data/ztf_dr2_with_colors.csv')
df_valid = df[(df['has_host'] == True) & (df['redshift'] > 0.05)].copy()

young = df_valid[df_valid['is_young'] == True].copy()
old = df_valid[df_valid['is_young'] == False].copy()

# Best-fit parameters from Gaussian prior analysis
H0 = 73.0
M_lcdm = -19.569
M_nonaccel = -19.641
Om = 0.300
OL = 0.691
q0 = 1.027

# Create figure with subplots
fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# Hubble diagrams
for idx, (sample, name, color) in enumerate([(df_valid, 'Full', 'purple'), 
                                               (young, 'Young', 'blue'), 
                                               (old, 'Old', 'red')]):
    z = sample['redshift'].values
    mB = -2.5 * np.log10(sample['x0'].values) + 10.0
    x1 = sample['x1'].values
    c = sample['c'].values
    mB_corr = mB + 0.14 * x1 - 3.1 * c
    
    # Filter out NaN values
    valid = ~np.isnan(mB_corr) & ~np.isnan(z)
    z = z[valid]
    mB_corr = mB_corr[valid]
    
    # Observed distance modulus
    mu_obs = mB_corr - M_lcdm
    
    # LCDM model
    dL_lcdm = luminosity_distance_lcdm(z, H0, Om, OL)
    mu_lcdm = 5 * np.log10(dL_lcdm) + 25
    
    # Non-Accel model
    dL_nonaccel = luminosity_distance_nonaccel(z, H0, q0)
    mu_nonaccel = 5 * np.log10(dL_nonaccel) + 25
    
    # Plot Hubble diagram
    ax = axes[0, idx]
    ax.scatter(z, mu_obs, alpha=0.3, s=10, color=color, label=f'{name} (N={len(z)})')
    z_smooth = np.linspace(z.min(), z.max(), 100)
    dL_lcdm_smooth = luminosity_distance_lcdm(z_smooth, H0, Om, OL)
    mu_lcdm_smooth = 5 * np.log10(dL_lcdm_smooth) + 25
    dL_nonaccel_smooth = luminosity_distance_nonaccel(z_smooth, H0, q0)
    mu_nonaccel_smooth = 5 * np.log10(dL_nonaccel_smooth) + 25
    ax.plot(z_smooth, mu_lcdm_smooth, 'g--', label='ΛCDM', linewidth=2)
    ax.plot(z_smooth, mu_nonaccel_smooth, 'r-', label='Non-Accel', linewidth=2)
    ax.set_xlabel('Redshift (z)')
    ax.set_ylabel('Distance Modulus μ')
    ax.set_title(f'{name} Sample Hubble Diagram')
    ax.legend()
    ax.set_xlim(0, 0.4)
    
    # Plot residuals
    ax = axes[1, idx]
    residuals_lcdm = mu_obs - mu_lcdm
    residuals_nonaccel = mu_obs - mu_nonaccel
    ax.scatter(z, residuals_lcdm, alpha=0.3, s=10, color='green', label='ΛCDM residuals')
    ax.scatter(z, residuals_nonaccel, alpha=0.3, s=10, color='red', label='Non-Accel residuals')
    ax.axhline(0, color='black', linestyle='--', linewidth=1)
    ax.set_xlabel('Redshift (z)')
    ax.set_ylabel('Residuals (mag)')
    ax.set_title(f'{name} Sample Residuals')
    ax.legend()
    ax.set_xlim(0, 0.4)
    
    # Print statistics
    print(f"{name} Sample:")
    print(f"  LCDM residuals: mean={np.mean(residuals_lcdm):.4f}, std={np.std(residuals_lcdm):.4f}")
    print(f"  Non-Accel residuals: mean={np.mean(residuals_nonaccel):.4f}, std={np.std(residuals_nonaccel):.4f}")
    print(f"  RMS improvement: {np.std(residuals_lcdm) - np.std(residuals_nonaccel):.4f}")
    print()

plt.tight_layout()
plt.savefig('data/visual_diagnostics.png', dpi=150, bbox_inches='tight')
print('Saved: data/visual_diagnostics.png')

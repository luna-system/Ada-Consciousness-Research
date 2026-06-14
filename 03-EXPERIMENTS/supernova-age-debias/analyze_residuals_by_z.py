import pandas as pd
import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize
import matplotlib.pyplot as plt

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

# Filter valid data
valid = df_valid['redshift'].notna() & df_valid['x0'].notna() & df_valid['x1'].notna() & df_valid['c'].notna() & df_valid['mass'].notna()
df_valid = df_valid[valid].copy()

z = df_valid['redshift'].values
mB = -2.5 * np.log10(df_valid['x0'].values) + 10.0
x1 = df_valid['x1'].values
c = df_valid['c'].values
mass = df_valid['mass'].values

# Tripp standardization
mass_step = mass - np.nanmedian(mass)
mB_corr = mB + 0.14 * x1 - 3.1 * c - 0.0 * mass_step

# Best-fit params from full sample
H0 = 73.0
M_lcdm = -19.569
M_nonaccel = -19.641
Om = 0.300
OL = 0.691
q0 = 1.027

# Compute residuals for each redshift bin
z_bins = np.linspace(z.min(), z.max(), 6)

fig, axes = plt.subplots(2, 3, figsize=(15, 10))

for i in range(5):
    z_low = z_bins[i]
    z_high = z_bins[i + 1]
    
    mask = (z >= z_low) & (z < z_high)
    if i == 4:
        mask = (z >= z_low) & (z <= z_high)
    
    z_bin = z[mask]
    mB_corr_bin = mB_corr[mask]
    
    # LCDM residuals
    dL_lcdm = luminosity_distance_lcdm(z_bin, H0, Om, OL)
    mu_lcdm = 5 * np.log10(dL_lcdm) + 25
    mu_obs_lcdm = mB_corr_bin - M_lcdm
    residuals_lcdm = mu_obs_lcdm - mu_lcdm
    
    # Non-Accel residuals
    dL_nonaccel = luminosity_distance_nonaccel(z_bin, H0, q0)
    mu_nonaccel = 5 * np.log10(dL_nonaccel) + 25
    mu_obs_nonaccel = mB_corr_bin - M_nonaccel
    residuals_nonaccel = mu_obs_nonaccel - mu_nonaccel
    
    # Plot
    ax = axes[i // 3, i % 3]
    ax.scatter(z_bin, residuals_lcdm, alpha=0.3, s=10, color='green', label='ΛCDM')
    ax.scatter(z_bin, residuals_nonaccel, alpha=0.3, s=10, color='red', label='Non-Accel')
    ax.axhline(0, color='black', linestyle='--', linewidth=1)
    ax.set_xlabel('Redshift (z)')
    ax.set_ylabel('Residuals (mag)')
    ax.set_title(f'z = [{z_low:.3f}, {z_high:.3f}]\nN={len(z_bin)}')
    ax.legend()
    
    # Print stats
    print(f"Bin {i+1}: z = [{z_low:.3f}, {z_high:.3f}], N={len(z_bin)}")
    print(f"  LCDM: mean={np.mean(residuals_lcdm):.4f}, std={np.std(residuals_lcdm):.4f}")
    print(f"  Non-Accel: mean={np.mean(residuals_nonaccel):.4f}, std={np.std(residuals_nonaccel):.4f}")
    print(f"  Mean diff: {np.mean(residuals_lcdm) - np.mean(residuals_nonaccel):.4f}")
    print()

plt.tight_layout()
plt.savefig('data/residuals_by_redshift_bin.png', dpi=150, bbox_inches='tight')
print('Saved: data/residuals_by_redshift_bin.png')

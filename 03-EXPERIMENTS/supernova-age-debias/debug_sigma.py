#!/usr/bin/env python3
"""
Debug: Check what sigma_int is being used
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Load data
data_path = Path('data/ztf_dr2/ztfsniadr2_lite/tables')
hosts = pd.read_csv(data_path / 'globalhost_data.csv')
sne = pd.read_csv(data_path / 'snia_data.csv')
df = sne.merge(hosts, on='ztfname', how='inner')

# Calculate mB
df['mB'] = -2.5 * np.log10(df['x0']) + 10.0

# Filter valid
valid = df['mB'].notna() & np.isfinite(df['mB']) & (df['redshift'] > 0)
df = df[valid].copy()

z = df['redshift'].values
mB = df['mB'].values

# Calculate sigma_int as in fit_cosmology.py
c = 299792.458
dL_approx = c * z / 70
mu_approx = 5 * np.log10(dL_approx) + 25
M_guess = np.median(mB - mu_approx)
residuals = mB - mu_approx - M_guess
sigma_int = max(0.1, np.std(residuals))

print(f"sigma_int = {sigma_int:.3f}")
print(f"residuals std = {np.std(residuals):.3f}")
print(f"residuals mean = {np.mean(residuals):.3f}")
print(f"Number of SNe = {len(z)}")

# Now compute chi2 for a simple model
# Using H0=70, M=-19.3
dL = c * z / 70 * (1 + z)  # Simple approximation
mu_model = 5 * np.log10(dL) + 25
mu_obs = mB - (-19.3)
residuals_test = mu_obs - mu_model
chi2_test = np.sum(residuals_test**2 / sigma_int**2)

print(f"\nTest chi2 (simple model): {chi2_test:.1f}")
print(f"Test reduced chi2: {chi2_test / len(z):.1f}")
print(f"Test RMS: {np.std(residuals_test):.3f}")

#!/usr/bin/env python3
"""
Debug: Find NaN in residuals
"""

import pandas as pd
import numpy as np
from scipy.integrate import quad

# Load a small subset
df = pd.read_csv('data/ztf_dr2/ztfsniadr2_lite/tables/snia_data.csv').head(100)
df['mB'] = -2.5 * np.log10(df['x0']) + 10.0
z = df['redshift'].values
mB = df['mB'].values

# Calculate sigma_int
c = 299792.458
dL_approx = c * z / 70
mu_approx = 5 * np.log10(dL_approx) + 25
M_guess = np.median(mB - mu_approx)
residuals = mB - mu_approx - M_guess
sigma_int = max(0.1, np.std(residuals))

print(f'sigma_int = {sigma_int:.3f}')

# LCDM function
def dL_lcdm(z, H0):
    def E_inv(z):
        return 1.0 / np.sqrt(0.3 * (1 + z)**3 + 0.7)
    integral = np.array([quad(E_inv, 0, zi)[0] for zi in z])
    return c * (1 + z) * integral / H0

# Compute with H0=70, M=-19.3
dL = dL_lcdm(z, 70)
mu_model = 5 * np.log10(dL) + 25
mu_obs = mB - (-19.3)
residuals = mu_obs - mu_model

# Find NaN
nan_mask = np.isnan(residuals)
print(f'NaN count: {nan_mask.sum()}')
print(f'NaN indices: {np.where(nan_mask)[0]}')

if nan_mask.sum() > 0:
    idx = np.where(nan_mask)[0][0]
    print(f'\nFirst NaN at index {idx}:')
    print(f'  z = {z[idx]}')
    print(f'  mB = {mB[idx]}')
    print(f'  x0 = {df["x0"].iloc[idx]}')
    print(f'  dL = {dL[idx]}')
    print(f'  mu_model = {mu_model[idx]}')
    print(f'  mu_obs = {mu_obs[idx]}')
    
    # Check if x0 is valid
    print(f'  x0 > 0: {df["x0"].iloc[idx] > 0}')
    print(f'  log10(x0): {np.log10(df["x0"].iloc[idx])}')
    
    # Check if z is valid
    print(f'  z > 0: {z[idx] > 0}')
    print(f'  z finite: {np.isfinite(z[idx])}')

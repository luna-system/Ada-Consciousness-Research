#!/usr/bin/env python3
"""
Debug: Check actual fit results
"""

import pandas as pd
import numpy as np
from pathlib import Path
from scipy.optimize import minimize

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

# Calculate sigma_int
c = 299792.458
dL_approx = c * z / 70
mu_approx = 5 * np.log10(dL_approx) + 25
M_guess = np.median(mB - mu_approx)
residuals = mB - mu_approx - M_guess
sigma_int = max(0.1, np.std(residuals))

print(f"sigma_int = {sigma_int:.3f}")

# Simple ΛCDM distance (for low z, approximate)
def dL_lcdm_simple(z, H0):
    return c * z / H0 * (1 + z/2)

# Fit function
def chi2_lcdm(params):
    H0, M = params
    dL = dL_lcdm_simple(z, H0)
    mu_model = 5 * np.log10(dL) + 25
    mu_obs = mB - M
    residuals = mu_obs - mu_model
    return np.sum(residuals**2 / sigma_int**2)

# Fit
result = minimize(chi2_lcdm, [70, -19.3], method='Nelder-Mead')
H0_best, M_best = result.x

print(f"\nBest fit: H0 = {H0_best:.2f}, M = {M_best:.3f}")

# Compute residuals
dL_best = dL_lcdm_simple(z, H0_best)
mu_best = 5 * np.log10(dL_best) + 25
mu_obs = mB - M_best
residuals = mu_obs - mu_best
chi2 = np.sum(residuals**2 / sigma_int**2)

print(f"chi2 = {chi2:.1f}")
print(f"reduced chi2 = {chi2 / (len(z) - 2):.1f}")
print(f"RMS = {np.std(residuals):.3f}")
print(f"residuals range: {residuals.min():.3f} to {residuals.max():.3f}")

# Check if the issue is in the distance formula
# At z=0.1, what should dL be?
z_test = 0.1
dL_test = dL_lcdm_simple(z_test, H0_best)
mu_test = 5 * np.log10(dL_test) + 25
print(f"\nAt z={z_test}: dL = {dL_test:.1f} Mpc, mu = {mu_test:.2f}")

# Compare with Hubble law
dL_hubble = c * z_test / H0_best
mu_hubble = 5 * np.log10(dL_hubble) + 25
print(f"Hubble law: dL = {dL_hubble:.1f} Mpc, mu = {mu_hubble:.2f}")

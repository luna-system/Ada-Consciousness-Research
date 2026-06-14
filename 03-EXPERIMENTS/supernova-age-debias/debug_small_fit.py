#!/usr/bin/env python3
"""
Debug: Test fit_cosmology with small sample
"""

import pandas as pd
import numpy as np
from scipy.optimize import minimize
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

# Chi2 function
def chi2_lcdm(params):
    H0, M = params
    dL = dL_lcdm(z, H0)
    mu_model = 5 * np.log10(dL) + 25
    mu_obs = mB - M
    residuals = mu_obs - mu_model
    return np.sum(residuals**2 / sigma_int**2)

# Fit
result = minimize(chi2_lcdm, [70, -19.3], method='Nelder-Mead')
H0_best, M_best = result.x
print(f'Best fit: H0={H0_best:.2f}, M={M_best:.3f}')
print(f'Optimization success: {result.success}')
print(f'Optimization message: {result.message}')

# Compute chi2
dL = dL_lcdm(z, H0_best)
print(f'dL sample: {dL[:5]}')
print(f'Any NaN in dL: {np.isnan(dL).any()}')
print(f'Any inf in dL: {np.isinf(dL).any()}')

mu_model = 5 * np.log10(dL) + 25
print(f'mu_model sample: {mu_model[:5]}')
print(f'Any NaN in mu_model: {np.isnan(mu_model).any()}')

mu_obs = mB - M_best
print(f'mu_obs sample: {mu_obs[:5]}')

residuals = mu_obs - mu_model
print(f'residuals sample: {residuals[:5]}')
print(f'Any NaN in residuals: {np.isnan(residuals).any()}')

chi2 = np.sum(residuals**2 / sigma_int**2)
print(f'chi2 = {chi2:.1f}')
print(f'reduced chi2 = {chi2/(len(z)-2):.1f}')
print(f'RMS = {np.std(residuals):.3f}')

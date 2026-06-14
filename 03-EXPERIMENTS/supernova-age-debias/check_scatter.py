#!/usr/bin/env python3
"""
Check actual scatter in ZTF DR2 data
"""

import pandas as pd
import numpy as np

# Load data
data_path = 'data/ztf_dr2/ztfsniadr2_lite/tables'
hosts = pd.read_csv(f'{data_path}/globalhost_data.csv')
sne = pd.read_csv(f'{data_path}/snia_data.csv')
df = sne.merge(hosts, on='ztfname', how='inner')

# Calculate mB
df['mB'] = -2.5 * np.log10(df['x0']) + 10.0

# Check for NaN/inf
print(f"mB NaN: {df['mB'].isna().sum()}")
print(f"mB inf: {np.isinf(df['mB']).sum()}")
print(f"x0 NaN: {df['x0'].isna().sum()}")
print(f"x0 <= 0: {(df['x0'] <= 0).sum()}")
print()

# Filter valid
valid = df['mB'].notna() & np.isfinite(df['mB']) & (df['redshift'] > 0)
df_valid = df[valid].copy()

print(f"Valid entries: {len(df_valid)} / {len(df)}")
print(f"mB range: {df_valid['mB'].min():.2f} - {df_valid['mB'].max():.2f}")
print(f"mB std: {df_valid['mB'].std():.3f}")
print(f"mB mean: {df_valid['mB'].mean():.3f}")
print()

# Approximate distance modulus for flat ΛCDM at low z
c = 299792.458
z = df_valid['redshift'].values
mu_approx = 5 * np.log10(c * z / 70) + 25
M_approx = np.median(df_valid['mB'] - mu_approx)
residuals = df_valid['mB'] - mu_approx - M_approx

print(f"Residuals std: {residuals.std():.3f}")
print(f"Residuals range: {residuals.min():.3f} - {residuals.max():.3f}")
print(f"M_approx: {M_approx:.3f}")

# Check redshift distribution
print(f"\nRedshift range: {z.min():.4f} - {z.max():.4f}")
print(f"Redshift mean: {z.mean():.4f}")

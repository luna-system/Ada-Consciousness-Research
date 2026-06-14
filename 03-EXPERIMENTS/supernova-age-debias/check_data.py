import pandas as pd
import numpy as np

print('Tripp fits:')
df = pd.read_csv('data/tripp_parameter_fits.csv')
print(df)
print()

print('Checking full sample data...')
hosts = pd.read_csv('data/ztf_dr2/ztfsniadr2_lite/tables/globalhost_data.csv')
sne = pd.read_csv('data/ztf_dr2/ztfsniadr2_lite/tables/snia_data.csv')
full = sne.merge(hosts, on='ztfname', how='inner')
print(f'Full sample size: {len(full)}')

if 'mB' in full.columns:
    print(f'Valid mB: {full["mB"].notna().sum()}')
else:
    print('mB not present, computing from x0...')
    full['mB'] = -2.5 * np.log10(full['x0']) + 10.0
    print(f'Valid mB (computed): {full["mB"].notna().sum()}')

print(f'Valid x0: {full["x0"].notna().sum()}')
print(f'Valid x1: {full["x1"].notna().sum()}')
print(f'Valid c: {full["c"].notna().sum()}')
print(f'Valid mass: {full["mass"].notna().sum()}')
print(f'Valid redshift: {full["redshift"].notna().sum()}')

# Check if there are any NaN in computed residuals
print()
print('Checking for NaN sources...')
mass_step = full['mass'] - np.median(full['mass'])
mB_corr = full['mB'] + 0.145 * full['x1'] - 3.198 * full['c'] - (-0.0002) * mass_step
print(f'Valid mB_corr: {mB_corr.notna().sum()}')
print(f'NaN in mB_corr: {mB_corr.isna().sum()}')

# Check individual components
print(f'NaN in mB: {full["mB"].isna().sum()}')
print(f'NaN in x1: {full["x1"].isna().sum()}')
print(f'NaN in c: {full["c"].isna().sum()}')
print(f'NaN in mass: {full["mass"].isna().sum()}')
print(f'NaN in mass_step: {np.isnan(mass_step).sum()}')

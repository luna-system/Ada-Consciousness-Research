import pandas as pd
import numpy as np

# Load ZTF
ztf_sne = pd.read_csv('data/ztf_dr2/ztfsniadr2_lite/tables/snia_data.csv')
ztf_hosts = pd.read_csv('data/ztf_dr2/ztfsniadr2_lite/tables/globalhost_data.csv')
ztf = ztf_sne.merge(ztf_hosts, on='ztfname', how='inner')
ztf = ztf[ztf['redshift'] > 0.05]
ztf['mB'] = -2.5 * np.log10(ztf['x0']) + 10.0

# Load Pantheon+
pantheon = pd.read_csv('data/pantheon-plus/Pantheon+_Data/4_DISTANCES_AND_COVAR/Pantheon+SH0ES.dat', sep='\s+')
pantheon = pantheon.rename(columns={'zCMB': 'redshift', 'mB': 'mB', 'x1': 'x1', 'c': 'c', 'HOST_LOGMASS': 'mass'})
pantheon = pantheon[pantheon['redshift'] > 0.1]

# Check NaN
print("ZTF NaN check:")
for col in ['redshift', 'mB', 'x1', 'c', 'mass']:
    print(f"  {col}: {ztf[col].isna().sum()} NaN out of {len(ztf)}")

print("\nPantheon+ NaN check:")
for col in ['redshift', 'mB', 'x1', 'c', 'mass']:
    print(f"  {col}: {pantheon[col].isna().sum()} NaN out of {len(pantheon)}")

# Combine
combined = pd.concat([ztf, pantheon], ignore_index=True)
print(f"\nCombined: {len(combined)} SNe")
for col in ['redshift', 'mB', 'x1', 'c', 'mass']:
    print(f"  {col}: {combined[col].isna().sum()} NaN out of {len(combined)}")

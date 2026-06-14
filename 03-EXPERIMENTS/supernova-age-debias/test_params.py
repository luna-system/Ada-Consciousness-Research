#!/usr/bin/env python3
"""
Quick test to see best-fit parameters
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
sys.path.insert(0, 'colorcut_pipeline')
from fit_cosmology import fit_hubble_diagram

# Load small sample
df = pd.read_csv('data/ztf_dr2/ztfsniadr2_lite/tables/snia_data.csv').head(200)
df['mB'] = -2.5 * np.log10(df['x0']) + 10.0
df['snid'] = df['ztfname']
df['zHD'] = df['redshift']
df['evolution_free'] = True

print('Testing with 200 SNe...')
lcdm = fit_hubble_diagram(df, model='lcdm')
print()
nonaccel = fit_hubble_diagram(df, model='nonaccel')
print()
print(f'Δχ² = {nonaccel["chi2"] - lcdm["chi2"]:.1f}')

import pandas as pd
import numpy as np

df = pd.read_csv('data/ztf_dr2_with_colors.csv')
df_valid = df[(df['has_host'] == True) & (df['redshift'] > 0.05)]

print(f'Full: {len(df_valid)}, x0 notna: {df_valid["x0"].notna().sum()}')
young = df_valid[df_valid['is_young'] == True]
old = df_valid[df_valid['is_young'] == False]
print(f'Young: {len(young)}, x0 notna: {young["x0"].notna().sum()}')
print(f'Old: {len(old)}, x0 notna: {old["x0"].notna().sum()}')

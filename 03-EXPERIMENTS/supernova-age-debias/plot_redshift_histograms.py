import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load data
df = pd.read_csv('data/ztf_dr2_with_colors.csv')

# Filter valid hosts with redshift > 0.05
df_valid = df[(df['has_host'] == True) & (df['redshift'] > 0.05)].copy()

# Define young/old based on is_young flag
young = df_valid[df_valid['is_young'] == True]
old = df_valid[df_valid['is_young'] == False]

print(f'Full sample: {len(df_valid)} SNe')
print(f'Young sample: {len(young)} SNe')
print(f'Old sample: {len(old)} SNe')
print()
print('Redshift statistics:')
print(f'Full: median={df_valid["redshift"].median():.4f}, mean={df_valid["redshift"].mean():.4f}')
print(f'Young: median={young["redshift"].median():.4f}, mean={young["redshift"].mean():.4f}')
print(f'Old: median={old["redshift"].median():.4f}, mean={old["redshift"].mean():.4f}')

# Create histograms
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Full sample histogram
axes[0, 0].hist(df_valid['redshift'], bins=50, alpha=0.7, color='purple', edgecolor='black')
axes[0, 0].axvline(df_valid['redshift'].median(), color='red', linestyle='--', linewidth=2, label=f'Median: {df_valid["redshift"].median():.4f}')
axes[0, 0].set_xlabel('Redshift (z)')
axes[0, 0].set_ylabel('Count')
axes[0, 0].set_title(f'Full Sample (N={len(df_valid)})')
axes[0, 0].legend()
axes[0, 0].set_xlim(0, 0.4)

# Young sample histogram
axes[0, 1].hist(young['redshift'], bins=50, alpha=0.7, color='blue', edgecolor='black')
axes[0, 1].axvline(young['redshift'].median(), color='red', linestyle='--', linewidth=2, label=f'Median: {young["redshift"].median():.4f}')
axes[0, 1].set_xlabel('Redshift (z)')
axes[0, 1].set_ylabel('Count')
axes[0, 1].set_title(f'Young Galaxies (N={len(young)})')
axes[0, 1].legend()
axes[0, 1].set_xlim(0, 0.4)

# Old sample histogram
axes[1, 0].hist(old['redshift'], bins=50, alpha=0.7, color='red', edgecolor='black')
axes[1, 0].axvline(old['redshift'].median(), color='darkred', linestyle='--', linewidth=2, label=f'Median: {old["redshift"].median():.4f}')
axes[1, 0].set_xlabel('Redshift (z)')
axes[1, 0].set_ylabel('Count')
axes[1, 0].set_title(f'Old Galaxies (N={len(old)})')
axes[1, 0].legend()
axes[1, 0].set_xlim(0, 0.4)

# Overlaid histograms
axes[1, 1].hist(young['redshift'], bins=50, alpha=0.5, color='blue', label=f'Young (N={len(young)})', density=True)
axes[1, 1].hist(old['redshift'], bins=50, alpha=0.5, color='red', label=f'Old (N={len(old)})', density=True)
axes[1, 1].axvline(young['redshift'].median(), color='blue', linestyle='--', linewidth=2, label=f'Young Median: {young["redshift"].median():.4f}')
axes[1, 1].axvline(old['redshift'].median(), color='red', linestyle='--', linewidth=2, label=f'Old Median: {old["redshift"].median():.4f}')
axes[1, 1].set_xlabel('Redshift (z)')
axes[1, 1].set_ylabel('Density')
axes[1, 1].set_title('Young vs Old Redshift Distributions')
axes[1, 1].legend()
axes[1, 1].set_xlim(0, 0.4)

plt.tight_layout()
plt.savefig('data/redshift_histograms.png', dpi=150, bbox_inches='tight')
print('\nSaved: data/redshift_histograms.png')

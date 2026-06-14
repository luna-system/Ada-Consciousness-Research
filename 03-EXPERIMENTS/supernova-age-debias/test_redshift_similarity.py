import pandas as pd
import numpy as np
from scipy import stats

# Load data
df = pd.read_csv('data/ztf_dr2_with_colors.csv')

# Filter valid hosts with redshift > 0.05
df_valid = df[(df['has_host'] == True) & (df['redshift'] > 0.05)].copy()

# Define young/old based on is_young flag
young = df_valid[df_valid['is_young'] == True]['redshift'].values
old = df_valid[df_valid['is_young'] == False]['redshift'].values

print('=== Redshift Distribution Statistical Tests ===')
print(f'Young sample: N={len(young)}, median={np.median(young):.4f}, mean={np.mean(young):.4f}, std={np.std(young):.4f}')
print(f'Old sample: N={len(old)}, median={np.median(old):.4f}, mean={np.mean(old):.4f}, std={np.std(old):.4f}')
print()

# Kolmogorov-Smirnov test
ks_stat, ks_pvalue = stats.ks_2samp(young, old)
print(f'Kolmogorov-Smirnov Test:')
print(f'  KS statistic: {ks_stat:.6f}')
print(f'  p-value: {ks_pvalue:.6f}')
print(f'  Interpretation: {"Similar distributions" if ks_pvalue > 0.05 else "Different distributions"}')
print()

# Anderson-Darling test (using scipy's anderson_ksamp for k samples)
try:
    ad_stat, ad_critical, ad_significance = stats.anderson_ksamp([young, old])
    print(f'Anderson-Darling Test:')
    print(f'  AD statistic: {ad_stat:.6f}')
    print(f'  Critical values: {ad_critical}')
    print(f'  Significance levels: {ad_significance}')
    print(f'  Interpretation: {"Similar distributions" if ad_stat < ad_critical[2] else "Different distributions"}')
except Exception as e:
    print(f'Anderson-Darling test failed: {e}')
print()

# Mann-Whitney U test (non-parametric test for location shift)
mu_stat, mu_pvalue = stats.mannwhitneyu(young, old, alternative='two-sided')
print(f'Mann-Whitney U Test (location shift):')
print(f'  U statistic: {mu_stat}')
print(f'  p-value: {mu_pvalue:.6f}')
print(f'  Interpretation: {"Same location" if mu_pvalue > 0.05 else "Different location"}')
print()

# Effect size (Cohen's d)
pooled_std = np.sqrt(((len(young)-1)*np.std(young, ddof=1)**2 + (len(old)-1)*np.std(old, ddof=1)**2) / (len(young)+len(old)-2))
cohens_d = (np.mean(young) - np.mean(old)) / pooled_std
print(f'Effect Size (Cohen\'s d): {cohens_d:.6f}')
print(f'  Interpretation: {"Negligible" if abs(cohens_d) < 0.2 else "Small" if abs(cohens_d) < 0.5 else "Medium" if abs(cohens_d) < 0.8 else "Large"}')
print()

# Percentile comparison
print('Percentile Comparison:')
percentiles = [10, 25, 50, 75, 90]
print(f'{"Percentile":<12} {"Young":<10} {"Old":<10} {"Diff":<10}')
for p in percentiles:
    y_p = np.percentile(young, p)
    o_p = np.percentile(old, p)
    print(f'{p:<12} {y_p:<10.4f} {o_p:<10.4f} {y_p-o_p:<10.4f}')

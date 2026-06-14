#!/usr/bin/env python3
"""
Malmquist Bias Test for Supernova Cosmology

Test if redshift-dependent detection thresholds affect our results.

Malmquist bias: we only detect brighter SNe at higher redshift.
This creates an artificial brightening trend with z.

Approach:
1. Compute absolute magnitude distribution at each redshift
2. Check if the bright end is truncated at high z
3. Apply correction if needed

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: June 14, 2026
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def compute_absolute_magnitude(df, alpha=0.14, beta=3.1):
    """Compute absolute magnitude from standardized brightness."""
    df = df.copy()
    if 'mB' not in df.columns:
        df['mB'] = -2.5 * np.log10(df['x0']) + 10.0
    
    # Apply Tripp standardization
    mass_step = df['mass'] - np.nanmedian(df['mass'])
    mB_corr = df['mB'] + alpha * df['x1'] - beta * df['c']
    
    # Approximate distance modulus
    z = df['redshift'].values
    c_light = 299792.458
    dL_approx = c_light * z / 72  # Mpc
    mu_approx = 5 * np.log10(dL_approx) + 25
    
    # Absolute magnitude
    M = mB_corr - mu_approx
    
    return M


def test_malmquist_bias(data_dir='data/ztf_dr2/ztfsniadr2_lite/tables'):
    """Test for Malmquist bias in the data."""
    
    logger.info("🌌 Malmquist Bias Test")
    logger.info("=" * 70)
    
    # Load data
    data_path = Path(data_dir)
    hosts = pd.read_csv(data_path / 'globalhost_data.csv')
    sne = pd.read_csv(data_path / 'snia_data.csv')
    df = sne.merge(hosts, on='ztfname', how='inner')
    
    logger.info(f"📊 Loaded {len(df)} ZTF SNe Ia")
    
    # Compute absolute magnitudes
    M = compute_absolute_magnitude(df)
    df['M_abs'] = M
    
    # Define redshift bins
    z_bins = [0.0, 0.02, 0.03, 0.05, 0.07, 0.10, 0.15, 0.30]
    z_labels = ['0.00-0.02', '0.02-0.03', '0.03-0.05', '0.05-0.07', 
                '0.07-0.10', '0.10-0.15', '0.15-0.30']
    
    logger.info(f"\n📊 Absolute Magnitude Distribution by Redshift:")
    logger.info(f"{'z range':<12} {'N':<8} {'M_mean':<10} {'M_std':<10} {'M_min':<10} {'M_max':<10}")
    logger.info("-" * 70)
    
    results = []
    
    for i in range(len(z_bins)-1):
        z_min, z_max = z_bins[i], z_bins[i+1]
        mask = (df['redshift'] >= z_min) & (df['redshift'] < z_max)
        
        # Handle last bin
        if i == len(z_bins) - 2:
            mask = (df['redshift'] >= z_min) & (df['redshift'] <= z_max)
        
        subset = df[mask]
        M_subset = subset['M_abs'].dropna()
        
        if len(M_subset) > 0:
            logger.info(f"{z_labels[i]:<12} {len(M_subset):<8} {M_subset.mean():<10.3f} {M_subset.std():<10.3f} {M_subset.min():<10.3f} {M_subset.max():<10.3f}")
            
            results.append({
                'z_range': z_labels[i],
                'N': len(M_subset),
                'M_mean': M_subset.mean(),
                'M_std': M_subset.std(),
                'M_min': M_subset.min(),
                'M_max': M_subset.max(),
            })
    
    # Check for Malmquist bias
    logger.info(f"\n📊 Malmquist Bias Check:")
    logger.info(f"If Malmquist bias exists, M_min should increase with z (bright end truncated)")
    
    # Simple trend test
    z_centers = [0.01, 0.025, 0.04, 0.06, 0.085, 0.125, 0.225]
    M_mins = [r['M_min'] for r in results]
    
    if len(M_mins) > 1:
        from scipy import stats
        slope, intercept, r_value, p_value, std_err = stats.linregress(z_centers[:len(M_mins)], M_mins)
        logger.info(f"   Trend: M_min = {intercept:.3f} + {slope:.3f} * z")
        logger.info(f"   R² = {r_value**2:.3f}, p = {p_value:.4f}")
        
        if slope > 0 and p_value < 0.05:
            logger.info(f"   ✅ Malmquist bias DETECTED! Bright end gets brighter with z.")
        elif slope < 0 and p_value < 0.05:
            logger.info(f"   ❌ Opposite trend! Malmquist bias not detected (or reversed).")
        else:
            logger.info(f"   ⚠️ No significant trend. Malmquist bias may be weak or absent.")
    
    # Plot
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Histogram of M by z bin
    ax1 = axes[0]
    colors = plt.cm.viridis(np.linspace(0, 1, len(z_bins)-1))
    for i in range(len(z_bins)-1):
        z_min, z_max = z_bins[i], z_bins[i+1]
        mask = (df['redshift'] >= z_min) & (df['redshift'] < z_max)
        if i == len(z_bins) - 2:
            mask = (df['redshift'] >= z_min) & (df['redshift'] <= z_max)
        
        M_subset = df[mask]['M_abs'].dropna()
        if len(M_subset) > 10:
            ax1.hist(M_subset, bins=30, alpha=0.5, label=f'z={z_labels[i]}', 
                    color=colors[i], density=True)
    
    ax1.set_xlabel('Absolute Magnitude (M)')
    ax1.set_ylabel('Density')
    ax1.set_title('Absolute Magnitude Distribution by Redshift')
    ax1.legend()
    ax1.axvline(x=-19.8, color='red', linestyle='--', alpha=0.5, label='Typical M')
    
    # M_min vs z
    ax2 = axes[1]
    ax2.scatter(z_centers[:len(M_mins)], M_mins, s=100, c='C0')
    if len(M_mins) > 1:
        z_fit = np.array(z_centers[:len(M_mins)])
        ax2.plot(z_fit, intercept + slope * z_fit, 'r--', 
                label=f'Trend: slope={slope:.3f}')
    ax2.set_xlabel('Redshift (z)')
    ax2.set_ylabel('Minimum Absolute Magnitude (M_min)')
    ax2.set_title('Malmquist Bias Test: M_min vs z')
    ax2.legend()
    ax2.axhline(y=-19.8, color='gray', linestyle=':', alpha=0.5)
    
    plt.tight_layout()
    fig.savefig('data/malmquist_bias_test.png', dpi=150, bbox_inches='tight')
    logger.info(f"\n📊 Plot saved to data/malmquist_bias_test.png")
    plt.close(fig)
    
    logger.info("=" * 70)
    logger.info("✅ Malmquist bias test complete!")
    logger.info("🍩 'Detection thresholds matter!'")
    
    return results


if __name__ == "__main__":
    results = test_malmquist_bias()
    
    # Save results
    df_results = pd.DataFrame(results)
    df_results.to_csv('data/malmquist_bias_results.csv', index=False)
    logger.info("💾 Results saved to data/malmquist_bias_results.csv")

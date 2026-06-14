#!/usr/bin/env python3
"""
Low-Z Young Galaxy Analysis — Where Does the "Acceleration" Signal Live?

Test if the acceleration signal in young galaxies is concentrated at z < 0.05
(where peculiar velocities dominate) vs z > 0.05 (where Hubble flow dominates).

If acceleration is real, it should be visible at ALL redshifts.
If it's peculiar velocity contamination, it should disappear at z > 0.05.

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: June 14, 2026
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from scipy.optimize import minimize
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

C_LIGHT = 299792.458  # km/s


def luminosity_distance_lcdm(z, H0, Om, OL):
    """ΛCDM luminosity distance in Mpc."""
    from scipy.integrate import quad
    
    def integrand(zp):
        return 1.0 / np.sqrt(Om * (1 + zp)**3 + OL)
    
    dL = np.zeros_like(z)
    for i, zi in enumerate(z):
        integral, _ = quad(integrand, 0, zi)
        dL[i] = (C_LIGHT / H0) * (1 + zi) * integral
    
    return dL


def luminosity_distance_nonaccel(z, H0, q0):
    """Non-accelerating luminosity distance."""
    dL = (C_LIGHT / H0) * z * (1 + z) * (1 + 0.5 * (1 - q0) * z)
    return dL


def apply_tripp_standardization(df, alpha=0.14, beta=3.1, gamma=0.0):
    """Apply Tripp standardization."""
    df = df.copy()
    if 'mB' not in df.columns:
        df['mB'] = -2.5 * np.log10(df['x0']) + 10.0
    mass_step = df['mass'] - np.nanmedian(df['mass'])
    df['mB_corr'] = df['mB'] + alpha * df['x1'] - beta * df['c'] - gamma * mass_step
    return df


def fit_cosmology(df, model, alpha, beta, gamma):
    """Quick cosmology fit."""
    
    df = apply_tripp_standardization(df, alpha, beta, gamma)
    z = df['redshift'].values
    mB_corr = df['mB_corr'].values
    
    c_light = 299792.458
    dL_approx = c_light * z / 70
    mu_approx = 5 * np.log10(dL_approx) + 25
    M_guess = np.nanmedian(mB_corr - mu_approx)
    
    if model == 'lcdm':
        def chi2(params):
            H0, Om, OL, M = params
            if not (50 < H0 < 100 and 0 < Om < 1 and 0 < OL < 1 and -22 < M < -17):
                return 1e10
            dL = luminosity_distance_lcdm(z, H0, Om, OL)
            mu_model = 5 * np.log10(dL) + 25
            mu_obs = mB_corr - M
            residuals = mu_obs - mu_model
            sigma = max(0.05, np.std(residuals))
            return np.sum(residuals**2 / sigma**2)
        
        result = minimize(chi2, [72.0, 0.3, 0.7, M_guess], method='Nelder-Mead')
        H0, Om, OL, M = result.x
        dL = luminosity_distance_lcdm(z, H0, Om, OL)
        k = 4
        
    elif model == 'nonaccel':
        def chi2(params):
            H0, q0, M = params
            if not (50 < H0 < 100 and 0 < q0 < 5 and -22 < M < -17):
                return 1e10
            dL = luminosity_distance_nonaccel(z, H0, q0)
            mu_model = 5 * np.log10(dL) + 25
            mu_obs = mB_corr - M
            residuals = mu_obs - mu_model
            sigma = max(0.05, np.std(residuals))
            return np.sum(residuals**2 / sigma**2)
        
        result = minimize(chi2, [72.0, 1.0, M_guess], method='Nelder-Mead')
        H0, q0, M = result.x
        dL = luminosity_distance_nonaccel(z, H0, q0)
        k = 3
    
    mu_model = 5 * np.log10(dL) + 25
    mu_obs = mB_corr - M
    residuals = mu_obs - mu_model
    chi2_val = np.sum(residuals**2 / np.std(residuals)**2)
    
    bic = chi2_val + k * np.log(len(df))
    
    return {
        'chi2': chi2_val,
        'bic': bic,
        'rms': np.sqrt(np.mean(residuals**2)),
        'n': len(df),
        'H0': H0,
        'Om': Om if model == 'lcdm' else None,
        'OL': OL if model == 'lcdm' else None,
        'q0': q0 if model == 'nonaccel' else None,
        'M': M,
    }


def analyze_lowz_young(data_dir='data/ztf_dr2/ztfsniadr2_lite/tables'):
    """Analyze low-z young galaxies where acceleration signal might live."""
    
    logger.info("🌌 Low-Z Young Galaxy Analysis")
    logger.info("=" * 70)
    
    data_path = Path(data_dir)
    hosts = pd.read_csv(data_path / 'globalhost_data.csv')
    sne = pd.read_csv(data_path / 'snia_data.csv')
    df = sne.merge(hosts, on='ztfname', how='inner')
    
    logger.info(f"📊 Loaded {len(df)} ZTF SNe Ia")
    
    # Define young galaxies
    young = df[(df['restframe_gz'] < 1.0) & (df['mass'] < 11.0)]
    
    logger.info(f"📊 {len(young)} young galaxies (g-z < 1.0, mass < 11.0)")
    
    # Define redshift bins
    z_bins = [
        (0.00, 0.02, "z < 0.02"),
        (0.02, 0.03, "0.02 < z < 0.03"),
        (0.03, 0.05, "0.03 < z < 0.05"),
        (0.05, 0.07, "0.05 < z < 0.07"),
        (0.07, 0.10, "0.07 < z < 0.10"),
        (0.10, 0.15, "0.10 < z < 0.15"),
        (0.15, 1.00, "z > 0.15"),
    ]
    
    tripp = {'alpha': 0.136, 'beta': 3.215, 'gamma': 0.0}
    
    logger.info(f"\n📊 Model Comparison by Redshift Bin:")
    logger.info(f"{'z range':<15} {'N':<8} {'ΛCDM BIC':<12} {'Non-Accel BIC':<15} {'ΔBIC':<10} {'Winner':<12} {'RMS':<10}")
    logger.info("-" * 90)
    
    results = []
    
    for z_min, z_max, label in z_bins:
        subset = young[(young['redshift'] >= z_min) & (young['redshift'] < z_max)]
        
        if len(subset) < 30:
            logger.info(f"{label:<15} {len(subset):<8} Too few SNe (< 30)")
            continue
        
        # Fit both models with better initial guesses for small samples
        try:
            lcdm = fit_cosmology(subset, 'lcdm', tripp['alpha'], tripp['beta'], tripp['gamma'])
            nonaccel = fit_cosmology(subset, 'nonaccel', tripp['alpha'], tripp['beta'], tripp['gamma'])
            
            if not np.isfinite(lcdm['bic']) or not np.isfinite(nonaccel['bic']):
                logger.info(f"{label:<15} {len(subset):<8} Fit failed (non-finite BIC)")
                continue
            
            delta_bic = lcdm['bic'] - nonaccel['bic']
            winner = 'ΛCDM' if delta_bic < 0 else 'Non-Accel'
            
            logger.info(f"{label:<15} {len(subset):<8} {lcdm['bic']:<12.1f} {nonaccel['bic']:<15.1f} {delta_bic:<10.1f} {winner:<12} {nonaccel['rms']:<10.3f}")
            
            results.append({
                'z_range': label,
                'z_min': z_min,
                'z_max': z_max,
                'n': len(subset),
                'lcdm_bic': lcdm['bic'],
                'nonaccel_bic': nonaccel['bic'],
                'delta_bic': delta_bic,
                'winner': winner,
                'lcdm_H0': lcdm['H0'],
                'lcdm_Om': lcdm['Om'],
                'lcdm_OL': lcdm['OL'],
                'nonaccel_H0': nonaccel['H0'],
                'nonaccel_q0': nonaccel['q0'],
                'rms': nonaccel['rms'],
            })
        except Exception as e:
            logger.info(f"{label:<15} {len(subset):<8} Fit failed ({str(e)[:30]})")
            continue
    
    # Test 2: Compare z < 0.05 vs z > 0.05
    logger.info(f"\n📊 Direct Comparison: z < 0.05 vs z > 0.05")
    
    lowz = young[young['redshift'] < 0.05]
    highz = young[young['redshift'] > 0.05]
    
    logger.info(f"  z < 0.05: {len(lowz)} SNe")
    logger.info(f"  z > 0.05: {len(highz)} SNe")
    
    if len(lowz) > 30:
        try:
            lcdm_low = fit_cosmology(lowz, 'lcdm', tripp['alpha'], tripp['beta'], tripp['gamma'])
            non_low = fit_cosmology(lowz, 'nonaccel', tripp['alpha'], tripp['beta'], tripp['gamma'])
            
            if np.isfinite(lcdm_low['bic']) and np.isfinite(non_low['bic']):
                delta_low = lcdm_low['bic'] - non_low['bic']
                winner_low = 'ΛCDM' if delta_low < 0 else 'Non-Accel'
                logger.info(f"  z < 0.05: {winner_low} (ΔBIC = {delta_low:.1f}, RMS = {non_low['rms']:.3f})")
            else:
                logger.info(f"  z < 0.05: Fit failed (non-finite BIC)")
        except Exception as e:
            logger.info(f"  z < 0.05: Fit failed ({str(e)[:30]})")
    
    if len(highz) > 30:
        try:
            lcdm_high = fit_cosmology(highz, 'lcdm', tripp['alpha'], tripp['beta'], tripp['gamma'])
            non_high = fit_cosmology(highz, 'nonaccel', tripp['alpha'], tripp['beta'], tripp['gamma'])
            
            if np.isfinite(lcdm_high['bic']) and np.isfinite(non_high['bic']):
                delta_high = lcdm_high['bic'] - non_high['bic']
                winner_high = 'ΛCDM' if delta_high < 0 else 'Non-Accel'
                logger.info(f"  z > 0.05: {winner_high} (ΔBIC = {delta_high:.1f}, RMS = {non_high['rms']:.3f})")
            else:
                logger.info(f"  z > 0.05: Fit failed (non-finite BIC)")
        except Exception as e:
            logger.info(f"  z > 0.05: Fit failed ({str(e)[:30]})")
    
    # Plot
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot 1: BIC vs redshift
    ax1 = axes[0]
    z_centers = [(r['z_min'] + r['z_max']) / 2 for r in results]
    delta_bics = [r['delta_bic'] for r in results]
    colors = ['C0' if d < 0 else 'C1' for d in delta_bics]
    
    ax1.scatter(z_centers, delta_bics, c=colors, s=100)
    ax1.axhline(y=0, color='black', linestyle='--', alpha=0.5)
    ax1.axhline(y=10, color='gray', linestyle=':', alpha=0.3, label='Strong evidence')
    ax1.axhline(y=-10, color='gray', linestyle=':', alpha=0.3)
    ax1.set_xlabel('Redshift (z)')
    ax1.set_ylabel('ΔBIC (ΛCDM - Non-Accel)')
    ax1.set_title('Model Preference vs Redshift\n(Young Galaxies)')
    ax1.legend()
    
    # Plot 2: RMS vs redshift
    ax2 = axes[1]
    rms_values = [r['rms'] for r in results]
    ax2.scatter(z_centers, rms_values, c='C2', s=100)
    ax2.set_xlabel('Redshift (z)')
    ax2.set_ylabel('RMS Scatter (mag)')
    ax2.set_title('Scatter vs Redshift\n(Young Galaxies)')
    
    plt.tight_layout()
    fig.savefig('data/lowz_young_analysis.png', dpi=150, bbox_inches='tight')
    logger.info(f"\n📊 Plot saved to data/lowz_young_analysis.png")
    plt.close(fig)
    
    logger.info("=" * 70)
    logger.info("✅ Low-z young galaxy analysis complete!")
    logger.info("🍩 'Where does the acceleration signal live?'")
    
    # Save results
    df_results = pd.DataFrame(results)
    df_results.to_csv('data/lowz_young_results.csv', index=False)
    logger.info("💾 Results saved to data/lowz_young_results.csv")
    
    return results


if __name__ == "__main__":
    results = analyze_lowz_young()

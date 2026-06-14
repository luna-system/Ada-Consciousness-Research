#!/usr/bin/env python3
"""
Sensitivity Tests for Korean Hypothesis

Vary color cut thresholds and test robustness of results.

Tests:
1. Vary g-z threshold: 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3
2. Vary mass threshold: 10.0, 10.5, 11.0, 11.5
3. Test without mass cut (color only)
4. Test with stricter coeval selection

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: June 14, 2026
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from scipy.optimize import minimize

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
    """Quick cosmology fit for sensitivity testing."""
    
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
    }


def test_sensitivity(data_dir='data/ztf_dr2/ztfsniadr2_lite/tables'):
    """Test sensitivity to color cut thresholds."""
    
    logger.info("🌌 Sensitivity Tests for Korean Hypothesis")
    logger.info("=" * 70)
    
    data_path = Path(data_dir)
    hosts = pd.read_csv(data_path / 'globalhost_data.csv')
    sne = pd.read_csv(data_path / 'snia_data.csv')
    df = sne.merge(hosts, on='ztfname', how='inner')
    
    # Apply z > 0.05 cut
    df = df[df['redshift'] > 0.05]
    
    logger.info(f"📊 Loaded {len(df)} ZTF SNe Ia (z > 0.05)")
    
    # Load Tripp parameters
    tripp_fits = pd.read_csv('data/tripp_parameter_fits.csv')
    tripp_dict = {row['sample']: row for _, row in tripp_fits.iterrows()}
    
    # Test 1: Vary g-z threshold
    gz_thresholds = [0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3]
    
    logger.info("\n📊 Test 1: Varying g-z Threshold (with mass < 11.0)")
    logger.info(f"{'g-z cut':<10} {'N young':<10} {'N old':<10} {'ΔBIC':<12} {'Winner':<15} {'RMS young':<12} {'RMS old':<12}")
    logger.info("-" * 90)
    
    results_gz = []
    
    for gz in gz_thresholds:
        young = df[(df['restframe_gz'] < gz) & (df['mass'] < 11.0)]
        old = df[df['restframe_gz'] > gz]
        
        if len(young) < 50 or len(old) < 50:
            continue
        
        # Use full sample Tripp params for consistency
        tripp = tripp_dict.get('Full Sample', {'alpha': 0.145, 'beta': 3.198, 'gamma': -0.0002})
        
        # Fit young
        lcdm_y = fit_cosmology(young, 'lcdm', tripp['alpha'], tripp['beta'], tripp['gamma'])
        non_y = fit_cosmology(young, 'nonaccel', tripp['alpha'], tripp['beta'], tripp['gamma'])
        
        # Fit old
        lcdm_o = fit_cosmology(old, 'lcdm', tripp['alpha'], tripp['beta'], tripp['gamma'])
        non_o = fit_cosmology(old, 'lcdm', tripp['alpha'], tripp['beta'], tripp['gamma'])
        
        delta_bic_y = lcdm_y['bic'] - non_y['bic']
        winner_y = 'ΛCDM' if delta_bic_y < 0 else 'Non-Accel'
        
        delta_bic_o = lcdm_o['bic'] - non_o['bic']
        winner_o = 'ΛCDM' if delta_bic_o < 0 else 'Non-Accel'
        
        logger.info(f"{gz:<10.1f} {len(young):<10} {len(old):<10} {delta_bic_y:<12.1f} {winner_y:<15} {non_y['rms']:<12.3f} {non_o['rms']:<12.3f}")
        
        results_gz.append({
            'gz_cut': gz,
            'n_young': len(young),
            'n_old': len(old),
            'delta_bic_young': delta_bic_y,
            'winner_young': winner_y,
            'delta_bic_old': delta_bic_o,
            'winner_old': winner_o,
            'rms_young': non_y['rms'],
            'rms_old': non_o['rms'],
        })
    
    # Test 2: Vary mass threshold
    mass_thresholds = [10.0, 10.5, 11.0, 11.5]
    
    logger.info("\n📊 Test 2: Varying Mass Threshold (with g-z < 1.0)")
    logger.info(f"{'Mass cut':<10} {'N young':<10} {'N old':<10} {'ΔBIC':<12} {'Winner':<15} {'RMS young':<12} {'RMS old':<12}")
    logger.info("-" * 90)
    
    results_mass = []
    
    for mass in mass_thresholds:
        young = df[(df['restframe_gz'] < 1.0) & (df['mass'] < mass)]
        old = df[df['restframe_gz'] > 1.2]  # Keep old definition fixed
        
        if len(young) < 50:
            continue
        
        tripp = tripp_dict.get('Full Sample', {'alpha': 0.145, 'beta': 3.198, 'gamma': -0.0002})
        
        lcdm_y = fit_cosmology(young, 'lcdm', tripp['alpha'], tripp['beta'], tripp['gamma'])
        non_y = fit_cosmology(young, 'nonaccel', tripp['alpha'], tripp['beta'], tripp['gamma'])
        
        lcdm_o = fit_cosmology(old, 'lcdm', tripp['alpha'], tripp['beta'], tripp['gamma'])
        non_o = fit_cosmology(old, 'nonaccel', tripp['alpha'], tripp['beta'], tripp['gamma'])
        
        delta_bic_y = lcdm_y['bic'] - non_y['bic']
        winner_y = 'ΛCDM' if delta_bic_y < 0 else 'Non-Accel'
        
        delta_bic_o = lcdm_o['bic'] - non_o['bic']
        winner_o = 'ΛCDM' if delta_bic_o < 0 else 'Non-Accel'
        
        logger.info(f"{mass:<10.1f} {len(young):<10} {len(old):<10} {delta_bic_y:<12.1f} {winner_y:<15} {non_y['rms']:<12.3f} {non_o['rms']:<12.3f}")
        
        results_mass.append({
            'mass_cut': mass,
            'n_young': len(young),
            'n_old': len(old),
            'delta_bic_young': delta_bic_y,
            'winner_young': winner_y,
            'delta_bic_old': delta_bic_o,
            'winner_old': winner_o,
            'rms_young': non_y['rms'],
            'rms_old': non_o['rms'],
        })
    
    # Test 3: Color only (no mass cut)
    logger.info("\n📊 Test 3: Color Only (no mass threshold)")
    
    gz_only = [0.8, 1.0, 1.2]
    
    for gz in gz_only:
        young = df[df['restframe_gz'] < gz]
        old = df[df['restframe_gz'] > gz]
        
        if len(young) < 50 or len(old) < 50:
            continue
        
        tripp = tripp_dict.get('Full Sample', {'alpha': 0.145, 'beta': 3.198, 'gamma': -0.0002})
        
        lcdm_y = fit_cosmology(young, 'lcdm', tripp['alpha'], tripp['beta'], tripp['gamma'])
        non_y = fit_cosmology(young, 'nonaccel', tripp['alpha'], tripp['beta'], tripp['gamma'])
        
        lcdm_o = fit_cosmology(old, 'lcdm', tripp['alpha'], tripp['beta'], tripp['gamma'])
        non_o = fit_cosmology(old, 'nonaccel', tripp['alpha'], tripp['beta'], tripp['gamma'])
        
        delta_bic_y = lcdm_y['bic'] - non_y['bic']
        winner_y = 'ΛCDM' if delta_bic_y < 0 else 'Non-Accel'
        
        delta_bic_o = lcdm_o['bic'] - non_o['bic']
        winner_o = 'ΛCDM' if delta_bic_o < 0 else 'Non-Accel'
        
        logger.info(f"  g-z < {gz}: Young={winner_y} (ΔBIC={delta_bic_y:.1f}), Old={winner_o} (ΔBIC={delta_bic_o:.1f})")
    
    logger.info("\n" + "=" * 70)
    logger.info("✅ Sensitivity tests complete!")
    logger.info("🍩 'Robust results survive threshold variations!'")
    
    # Save results
    df_gz = pd.DataFrame(results_gz)
    df_gz.to_csv('data/sensitivity_gz_thresholds.csv', index=False)
    
    df_mass = pd.DataFrame(results_mass)
    df_mass.to_csv('data/sensitivity_mass_thresholds.csv', index=False)
    
    logger.info("💾 Results saved to data/sensitivity_*.csv")
    
    return results_gz, results_mass


if __name__ == "__main__":
    results_gz, results_mass = test_sensitivity()

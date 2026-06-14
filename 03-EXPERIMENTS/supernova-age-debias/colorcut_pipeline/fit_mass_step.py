#!/usr/bin/env python3
"""
Host-Mass Step Correction for Supernova Cosmology

Fits the host-mass step parameter to reduce Hubble residual scatter.

Model: mB_corr = mB + α·x1 - β·c - γ·step(mass - M_threshold)

Literature values: M_threshold ≈ 10.0, γ ≈ 0.05-0.10 mag

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
    """Non-accelerating luminosity distance (Mattig formula with 1+z)."""
    dL = (C_LIGHT / H0) * z * (1 + z) * (1 + 0.5 * (1 - q0) * z)
    return dL


def apply_tripp_with_mass_step(df, alpha, beta, gamma, M_threshold):
    """Apply Tripp standardization with host-mass step."""
    df = df.copy()
    if 'mB' not in df.columns:
        df['mB'] = -2.5 * np.log10(df['x0']) + 10.0
    
    # Mass step: 1 if mass > threshold, 0 otherwise
    mass_step = np.where(df['mass'] > M_threshold, 1.0, 0.0)
    
    df['mB_corr'] = df['mB'] + alpha * df['x1'] - beta * df['c'] - gamma * mass_step
    return df


def fit_mass_step(df, alpha, beta, model='lcdm', initial_params=None):
    """
    Fit host-mass step parameter γ and threshold M_threshold.
    
    Parameters:
    -----------
    df : DataFrame
        SNe data with mB, x1, c, mass, redshift
    alpha, beta : float
        Fixed Tripp parameters
    model : str
        'lcdm' or 'nonaccel'
    initial_params : dict
        Initial guesses for cosmology params
    
    Returns:
    --------
    dict with best-fit parameters and scatter
    """
    
    logger.info(f"📊 Fitting host-mass step for {model} model...")
    
    # Prepare data
    valid = df['mB'].notna() if 'mB' in df.columns else df['x0'].notna()
    valid &= df['x1'].notna() & df['c'].notna() & df['mass'].notna() & df['redshift'].notna()
    data = df[valid].copy()
    
    if len(data) < 10:
        logger.warning(f"   ⚠️ Too few galaxies ({len(data)}) for fitting!")
        return None
    
    z = data['redshift'].values
    
    # Initial cosmology parameters
    if initial_params is None:
        if model == 'lcdm':
            initial_params = {'H0': 72.0, 'Om': 0.3, 'OL': 0.7, 'M': -19.8}
        else:
            initial_params = {'H0': 72.0, 'q0': 1.0, 'M': -19.8}
    
    # Fit for γ, M_threshold, and cosmology params
    def chi2(params):
        if model == 'lcdm':
            H0, Om, OL, M, gamma, M_threshold = params
            if not (50 < H0 < 100 and 0 < Om < 1 and 0 < OL < 1 and -22 < M < -17 and 0 < gamma < 0.5 and 9 < M_threshold < 11):
                return 1e10
        else:
            H0, q0, M, gamma, M_threshold = params
            if not (50 < H0 < 100 and 0 < q0 < 5 and -22 < M < -17 and 0 < gamma < 0.5 and 9 < M_threshold < 11):
                return 1e10
        
        # Apply standardization with mass step
        data_corr = apply_tripp_with_mass_step(data, alpha, beta, gamma, M_threshold)
        
        # Compute model distance modulus
        if model == 'lcdm':
            dL = luminosity_distance_lcdm(z, H0, Om, OL)
        else:
            dL = luminosity_distance_nonaccel(z, H0, q0)
        
        mu_model = 5 * np.log10(dL) + 25
        mu_obs = data_corr['mB_corr'].values - M
        
        residuals = mu_obs - mu_model
        sigma = max(0.05, np.std(residuals))
        
        return np.sum(residuals**2 / sigma**2)
    
    # Initial guess
    if model == 'lcdm':
        x0 = [initial_params['H0'], initial_params['Om'], initial_params['OL'], initial_params['M'], 0.05, 10.0]
    else:
        x0 = [initial_params['H0'], initial_params['q0'], initial_params['M'], 0.05, 10.0]
    
    # Fit
    result = minimize(chi2, x0, method='Nelder-Mead')
    
    # Extract best-fit params
    if model == 'lcdm':
        H0_best, Om_best, OL_best, M_best, gamma_best, M_thresh_best = result.x
    else:
        H0_best, q0_best, M_best, gamma_best, M_thresh_best = result.x
    
    # Compute scatter with best-fit params
    data_corr = apply_tripp_with_mass_step(data, alpha, beta, gamma_best, M_thresh_best)
    
    if model == 'lcdm':
        dL = luminosity_distance_lcdm(z, H0_best, Om_best, OL_best)
    else:
        dL = luminosity_distance_nonaccel(z, H0_best, q0_best)
    
    mu_model = 5 * np.log10(dL) + 25
    mu_obs = data_corr['mB_corr'].values - M_best
    residuals = mu_obs - mu_model
    sigma_best = np.std(residuals)
    
    # Compare to no mass step
    data_no_step = apply_tripp_with_mass_step(data, alpha, beta, 0.0, M_thresh_best)
    mu_obs_no_step = data_no_step['mB_corr'].values - M_best
    residuals_no_step = mu_obs_no_step - mu_model
    sigma_no_step = np.std(residuals_no_step)
    
    logger.info(f"   Best-fit parameters:")
    logger.info(f"     γ (mass step) = {gamma_best:.4f} mag")
    logger.info(f"     M_threshold = {M_thresh_best:.2f}")
    if model == 'lcdm':
        logger.info(f"     H0 = {H0_best:.2f}, Ωm = {Om_best:.3f}, ΩΛ = {OL_best:.3f}")
    else:
        logger.info(f"     H0 = {H0_best:.2f}, q0 = {q0_best:.3f}")
    logger.info(f"     M = {M_best:.3f}")
    logger.info(f"   Scatter with mass step: σ = {sigma_best:.3f} mag")
    logger.info(f"   Scatter without mass step: σ = {sigma_no_step:.3f} mag")
    logger.info(f"   Improvement: {sigma_no_step:.3f} → {sigma_best:.3f} mag ({100*(sigma_no_step-sigma_best)/sigma_no_step:.1f}% reduction)")
    
    return {
        'gamma': gamma_best,
        'M_threshold': M_thresh_best,
        'H0': H0_best,
        'Om': Om_best if model == 'lcdm' else None,
        'OL': OL_best if model == 'lcdm' else None,
        'q0': q0_best if model == 'nonaccel' else None,
        'M': M_best,
        'sigma_with_step': sigma_best,
        'sigma_no_step': sigma_no_step,
        'n_galaxies': len(data),
    }


def test_mass_step(data_dir='data/ztf_dr2/ztfsniadr2_lite/tables'):
    """Test host-mass step fitting on different subsamples."""
    
    logger.info("🌌 Host-Mass Step Correction Analysis")
    logger.info("=" * 70)
    
    # Load data
    data_path = Path(data_dir)
    hosts = pd.read_csv(data_path / 'globalhost_data.csv')
    sne = pd.read_csv(data_path / 'snia_data.csv')
    df = sne.merge(hosts, on='ztfname', how='inner')
    
    logger.info(f"📊 Loaded {len(df)} ZTF SNe Ia")
    
    # Load fitted Tripp parameters
    tripp_fits = pd.read_csv('data/tripp_parameter_fits.csv')
    tripp_dict = {row['sample']: row for _, row in tripp_fits.iterrows()}
    
    # Define subsamples
    samples = {
        'Full Sample': df,
        'Young (g-z < 1.0, mass < 11.0)': df[(df['restframe_gz'] < 1.0) & (df['mass'] < 11.0)],
        'Old (g-z > 1.2)': df[df['restframe_gz'] > 1.2],
        'Blue (g-z < 0.8)': df[df['restframe_gz'] < 0.8],
        'Red (g-z > 1.0)': df[df['restframe_gz'] > 1.0],
    }
    
    results = {}
    
    for name, sample_df in samples.items():
        tripp = tripp_dict.get(name, {'alpha': 0.145, 'beta': 3.198})
        
        if len(sample_df) < 100:
            logger.warning(f"⚠️ Skipping {name} - too few SNe ({len(sample_df)})")
            continue
        
        logger.info(f"\n📊 {name}:")
        
        # Fit for ΛCDM
        result_lcdm = fit_mass_step(sample_df, tripp['alpha'], tripp['beta'], model='lcdm')
        
        # Fit for non-accelerating
        result_nonaccel = fit_mass_step(sample_df, tripp['alpha'], tripp['beta'], model='nonaccel')
        
        if result_lcdm and result_nonaccel:
            results[name] = {
                'lcdm': result_lcdm,
                'nonaccel': result_nonaccel,
            }
    
    # Summary table
    logger.info("\n" + "=" * 70)
    logger.info("📊 SUMMARY: Host-Mass Step Correction")
    logger.info("=" * 70)
    logger.info(f"{'Sample':<25} {'N':<8} {'γ':<8} {'M_thresh':<10} {'σ_no_step':<12} {'σ_with_step':<12} {'Improvement'}")
    logger.info("-" * 70)
    
    for name, r in results.items():
        for model in ['lcdm', 'nonaccel']:
            rm = r[model]
            improvement = f"{100*(rm['sigma_no_step']-rm['sigma_with_step'])/rm['sigma_no_step']:.1f}%"
            logger.info(f"{name:<25} {rm['n_galaxies']:<8} {rm['gamma']:<8.4f} {rm['M_threshold']:<10.2f} {rm['sigma_no_step']:<12.3f} {rm['sigma_with_step']:<12.3f} {improvement}")
    
    logger.info("=" * 70)
    logger.info("✅ Host-mass step analysis complete!")
    logger.info("🍩 'Better standardization = better science!'")
    
    return results


if __name__ == "__main__":
    results = test_mass_step()
    
    # Save results
    rows = []
    for name, r in results.items():
        for model in ['lcdm', 'nonaccel']:
            rm = r[model]
            rows.append({
                'sample': name,
                'model': model,
                'n_galaxies': rm['n_galaxies'],
                'gamma': rm['gamma'],
                'M_threshold': rm['M_threshold'],
                'sigma_no_step': rm['sigma_no_step'],
                'sigma_with_step': rm['sigma_with_step'],
                'H0': rm['H0'],
                'M': rm['M'],
            })
    
    df_results = pd.DataFrame(rows)
    df_results.to_csv('data/mass_step_results.csv', index=False)
    logger.info("💾 Results saved to data/mass_step_results.csv")

#!/usr/bin/env python3
"""
Fit Tripp Standardization Parameters from Data

Fits α (stretch), β (color), and γ (host-mass step) per subsample.
This should reduce scatter closer to ZTF's published ~0.15 mag.

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


def fit_tripp_params(df, sample_name=""):
    """
    Fit Tripp standardization parameters α, β, γ from data.
    
    Model: mB_corr = mB + α*x1 - β*c - γ*mass_step
    
    Where mass_step = mass - median_mass (or similar)
    
    Parameters:
    -----------
    df : DataFrame
        Must contain: mB, x1, c, mass, zHD
    sample_name : str
        Name of sample for logging
    
    Returns:
    --------
    dict with fitted parameters and scatter
    """
    
    logger.info(f"📊 Fitting Tripp parameters for {sample_name}...")
    
    # Prepare data
    valid = df['mB'].notna() & df['x1'].notna() & df['c'].notna() & df['mass'].notna() & df['redshift'].notna()
    data = df[valid].copy()
    
    if len(data) < 10:
        logger.warning(f"   ⚠️ Too few galaxies ({len(data)}) for fitting!")
        return None
    
    mB = data['mB'].values
    x1 = data['x1'].values
    c = data['c'].values
    mass = data['mass'].values
    z = data['redshift'].values
    
    # Compute rough distance modulus for initial guess
    c_light = 299792.458
    dL_approx = c_light * z / 70  # Mpc
    mu_approx = 5 * np.log10(dL_approx) + 25
    M_guess = np.median(mB - mu_approx)
    
    # Initial scatter estimate
    residuals_init = mB - mu_approx - M_guess
    sigma_init = np.std(residuals_init)
    
    logger.info(f"   Initial scatter (no correction): σ = {sigma_init:.3f} mag")
    
    # Fit for α, β, γ, M
    def chi2(params):
        alpha, beta, gamma, M = params
        
        # Compute corrected magnitude
        mass_step = mass - np.median(mass)
        mB_corr = mB + alpha * x1 - beta * c - gamma * mass_step
        
        # Compute distance modulus for each SN
        mu_obs = mB_corr - M
        
        # Use approximate distance modulus for simplicity
        # (we're fitting standardization, not cosmology)
        mu_model = mu_approx
        
        residuals = mu_obs - mu_model
        sigma = max(0.05, np.std(residuals))  # Minimum scatter floor
        
        return np.sum(residuals**2 / sigma**2)
    
    # Fit
    result = minimize(chi2, [0.14, 3.1, 0.0, M_guess], method='Nelder-Mead')
    alpha_best, beta_best, gamma_best, M_best = result.x
    
    # Compute corrected magnitudes with best-fit params
    mass_step = mass - np.median(mass)
    mB_corr = mB + alpha_best * x1 - beta_best * c - gamma_best * mass_step
    residuals = mB_corr - M_best - mu_approx
    sigma_best = np.std(residuals)
    
    logger.info(f"   Best-fit parameters:")
    logger.info(f"     α (stretch) = {alpha_best:.4f}")
    logger.info(f"     β (color) = {beta_best:.4f}")
    logger.info(f"     γ (mass step) = {gamma_best:.4f}")
    logger.info(f"     M (absolute mag) = {M_best:.3f}")
    logger.info(f"   Scatter after correction: σ = {sigma_best:.3f} mag")
    logger.info(f"   Improvement: {sigma_init:.3f} → {sigma_best:.3f} mag ({100*(sigma_init-sigma_best)/sigma_init:.1f}% reduction)")
    
    return {
        'alpha': alpha_best,
        'beta': beta_best,
        'gamma': gamma_best,
        'M': M_best,
        'sigma_init': sigma_init,
        'sigma_best': sigma_best,
        'n_galaxies': len(data),
    }


def test_tripp_fitting(data_dir='data/ztf_dr2/ztfsniadr2_lite/tables'):
    """Test Tripp parameter fitting on different subsamples."""
    
    logger.info("🌌 Fitting Tripp Standardization Parameters")
    logger.info("=" * 70)
    
    # Load data
    data_path = Path(data_dir)
    hosts = pd.read_csv(data_path / 'globalhost_data.csv')
    sne = pd.read_csv(data_path / 'snia_data.csv')
    df = sne.merge(hosts, on='ztfname', how='inner')
    
    # Add mB
    df['mB'] = -2.5 * np.log10(df['x0']) + 10.0
    
    logger.info(f"📊 Loaded {len(df)} ZTF SNe Ia")
    
    # Define subsamples
    samples = {
        'Full Sample': df,
        'Young (g-z < 1.0, mass < 11.0)': df[(df['restframe_gz'] < 1.0) & (df['mass'] < 11.0)],
        'Old (g-z > 1.2)': df[df['restframe_gz'] > 1.2],
        'Blue (g-z < 0.8)': df[df['restframe_gz'] < 0.8],
        'Red (g-z > 1.0)': df[df['restframe_gz'] > 1.0],
        'Low Mass (mass < 10.5)': df[df['mass'] < 10.5],
        'High Mass (mass > 11.0)': df[df['mass'] > 11.0],
    }
    
    results = {}
    
    for name, sample_df in samples.items():
        result = fit_tripp_params(sample_df, name)
        if result:
            results[name] = result
    
    # Summary table
    logger.info("\n" + "=" * 70)
    logger.info("📊 SUMMARY: Tripp Parameter Fits")
    logger.info("=" * 70)
    logger.info(f"{'Sample':<25} {'N':<8} {'α':<8} {'β':<8} {'γ':<8} {'σ_init':<10} {'σ_best':<10} {'Improvement'}")
    logger.info("-" * 70)
    
    for name, r in results.items():
        improvement = f"{100*(r['sigma_init']-r['sigma_best'])/r['sigma_init']:.1f}%"
        logger.info(f"{name:<25} {r['n_galaxies']:<8} {r['alpha']:<8.3f} {r['beta']:<8.3f} {r['gamma']:<8.4f} {r['sigma_init']:<10.3f} {r['sigma_best']:<10.3f} {improvement}")
    
    # Compare to literature values
    logger.info("\n" + "=" * 70)
    logger.info("📊 Comparison to Literature Values:")
    logger.info("=" * 70)
    logger.info("Literature (typical): α = 0.14, β = 3.1, γ = 0.0")
    logger.info("ZTF DR2 (reported): β ~ 3.05 (full), β ~ 3.6 (low-mass hosts)")
    logger.info("")
    logger.info("Our fits show:")
    if 'Young (g-z < 1.0, mass < 11.0)' in results:
        young = results['Young (g-z < 1.0, mass < 11.0)']
        logger.info(f"  Young sample: β = {young['beta']:.3f} (low-mass, should be ~3.6)")
    if 'Old (g-z > 1.2)' in results:
        old = results['Old (g-z > 1.2)']
        logger.info(f"  Old sample: β = {old['beta']:.3f} (high-mass, should be ~3.0)")
    
    logger.info("=" * 70)
    logger.info("✅ Tripp parameter fitting complete!")
    logger.info("🍩 'Better standardization = better science!'")
    
    return results


if __name__ == "__main__":
    results = test_tripp_fitting()
    
    # Save results
    df_results = pd.DataFrame([
        {
            'sample': name,
            'n_galaxies': r['n_galaxies'],
            'alpha': r['alpha'],
            'beta': r['beta'],
            'gamma': r['gamma'],
            'sigma_init': r['sigma_init'],
            'sigma_best': r['sigma_best'],
        }
        for name, r in results.items()
    ])
    df_results.to_csv('data/tripp_parameter_fits.csv', index=False)
    logger.info("💾 Results saved to data/tripp_parameter_fits.csv")

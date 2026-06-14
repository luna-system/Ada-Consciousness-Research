#!/usr/bin/env python3
"""
BIC vs AIC Comparison Test

Test if AIC (weaker penalty) correctly recovers ΛCDM when it's true,
while BIC (stronger penalty) favors non-accel.

Also test with higher-z data (z up to 2.0) where ΛCDM should dominate.

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


def generate_synthetic_data(n_sne=1000, model='lcdm', H0=72, Om=0.3, OL=0.7, q0=1.0,
                            sigma_int=0.15, z_min=0.01, z_max=2.0):
    """Generate synthetic supernova data with known cosmology."""
    
    # Generate redshifts (uniform in log space)
    z = np.exp(np.random.uniform(np.log(z_min), np.log(z_max), n_sne))
    
    # True distance modulus
    if model == 'lcdm':
        dL = luminosity_distance_lcdm(z, H0, Om, OL)
    elif model == 'nonaccel':
        dL = luminosity_distance_nonaccel(z, H0, q0)
    else:
        raise ValueError(f"Unknown model: {model}")
    
    mu_true = 5 * np.log10(dL) + 25
    
    # Absolute magnitude
    M = -19.8
    
    # True apparent magnitude
    mB_true = mu_true + M
    
    # Add intrinsic scatter
    mB = mB_true + np.random.normal(0, sigma_int, n_sne)
    
    # Add measurement noise (larger at higher z)
    sigma_meas = 0.05 + 0.02 * z
    mB += np.random.normal(0, sigma_meas, n_sne)
    
    # Generate light curve parameters (random)
    x1 = np.random.normal(0, 1, n_sne)
    c = np.random.normal(0, 0.1, n_sne)
    mass = np.random.normal(10.5, 1.0, n_sne)
    
    df = pd.DataFrame({
        'redshift': z,
        'mB': mB,
        'x1': x1,
        'c': c,
        'mass': mass,
    })
    
    return df


def apply_tripp_standardization(df, alpha=0.14, beta=3.1, gamma=0.0):
    """Apply Tripp standardization."""
    df = df.copy()
    mass_step = df['mass'] - np.nanmedian(df['mass'])
    df['mB_corr'] = df['mB'] + alpha * df['x1'] - beta * df['c'] - gamma * mass_step
    return df


def fit_cosmology_with_metrics(df, model, alpha=0.14, beta=3.1, gamma=0.0):
    """Fit cosmology and compute AIC, BIC, and log-likelihood."""
    
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
    
    # Log-likelihood (approximate)
    sigma = np.std(residuals)
    logL = -0.5 * np.sum(residuals**2 / sigma**2 + np.log(2 * np.pi * sigma**2))
    
    # AIC and BIC
    aic = chi2_val + 2 * k
    bic = chi2_val + k * np.log(len(df))
    
    return {
        'chi2': chi2_val,
        'aic': aic,
        'bic': bic,
        'logL': logL,
        'k': k,
        'rms': np.sqrt(np.mean(residuals**2)),
        'n': len(df),
        'H0': H0,
        'Om': Om if model == 'lcdm' else None,
        'OL': OL if model == 'lcdm' else None,
        'q0': q0 if model == 'nonaccel' else None,
        'M': M,
    }


def compare_aic_bic():
    """Compare AIC vs BIC for model selection."""
    
    logger.info("🌌 AIC vs BIC Comparison Test")
    logger.info("=" * 70)
    
    # Test with different z_max values
    z_max_values = [0.5, 1.0, 1.5, 2.0]
    
    logger.info("\n📊 Test 1: Inject ΛCDM (Ωm=0.3, ΩΛ=0.7), compare AIC vs BIC")
    logger.info(f"{'z_max':<8} {'Metric':<8} {'ΛCDM':<12} {'Non-Accel':<12} {'Δ':<10} {'Winner':<12}")
    logger.info("-" * 70)
    
    for z_max in z_max_values:
        data = generate_synthetic_data(n_sne=1000, model='lcdm', H0=72, Om=0.3, OL=0.7, z_max=z_max)
        
        lcdm = fit_cosmology_with_metrics(data, 'lcdm')
        nonaccel = fit_cosmology_with_metrics(data, 'nonaccel')
        
        # AIC comparison
        delta_aic = lcdm['aic'] - nonaccel['aic']
        winner_aic = 'ΛCDM' if delta_aic < 0 else 'Non-Accel'
        logger.info(f"{z_max:<8.1f} {'AIC':<8} {lcdm['aic']:<12.1f} {nonaccel['aic']:<12.1f} {delta_aic:<10.1f} {winner_aic:<12}")
        
        # BIC comparison
        delta_bic = lcdm['bic'] - nonaccel['bic']
        winner_bic = 'ΛCDM' if delta_bic < 0 else 'Non-Accel'
        logger.info(f"{'':<8} {'BIC':<8} {lcdm['bic']:<12.1f} {nonaccel['bic']:<12.1f} {delta_bic:<10.1f} {winner_bic:<12}")
        
        # Log-likelihood comparison (no penalty)
        delta_logL = lcdm['logL'] - nonaccel['logL']
        winner_ll = 'ΛCDM' if delta_logL > 0 else 'Non-Accel'
        logger.info(f"{'':<8} {'logL':<8} {lcdm['logL']:<12.1f} {nonaccel['logL']:<12.1f} {delta_logL:<10.1f} {winner_ll:<12}")
        logger.info("")
    
    # Test 2: Different sample sizes
    logger.info("\n📊 Test 2: Different Sample Sizes (z_max=1.0, inject ΛCDM)")
    logger.info(f"{'N':<8} {'Metric':<8} {'ΛCDM':<12} {'Non-Accel':<12} {'Δ':<10} {'Winner':<12}")
    logger.info("-" * 70)
    
    sample_sizes = [100, 500, 1000, 5000]
    
    for n in sample_sizes:
        data = generate_synthetic_data(n_sne=n, model='lcdm', H0=72, Om=0.3, OL=0.7, z_max=1.0)
        
        lcdm = fit_cosmology_with_metrics(data, 'lcdm')
        nonaccel = fit_cosmology_with_metrics(data, 'nonaccel')
        
        delta_aic = lcdm['aic'] - nonaccel['aic']
        winner_aic = 'ΛCDM' if delta_aic < 0 else 'Non-Accel'
        logger.info(f"{n:<8} {'AIC':<8} {lcdm['aic']:<12.1f} {nonaccel['aic']:<12.1f} {delta_aic:<10.1f} {winner_aic:<12}")
        
        delta_bic = lcdm['bic'] - nonaccel['bic']
        winner_bic = 'ΛCDM' if delta_bic < 0 else 'Non-Accel'
        logger.info(f"{'':<8} {'BIC':<8} {lcdm['bic']:<12.1f} {nonaccel['bic']:<12.1f} {delta_bic:<10.1f} {winner_bic:<12}")
        logger.info()
    
    logger.info("=" * 70)
    logger.info("✅ AIC vs BIC comparison complete!")
    logger.info("🍩 'The penalty matters!'")


if __name__ == "__main__":
    compare_aic_bic()

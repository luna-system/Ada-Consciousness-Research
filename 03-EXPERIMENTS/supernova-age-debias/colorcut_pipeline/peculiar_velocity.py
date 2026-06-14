#!/usr/bin/env python3
"""
Peculiar Velocity Corrections for Supernova Cosmology

Test redshift-dependent cuts to reduce peculiar velocity contamination.

Peculiar velocities dominate at z < 0.05 (σ_v ~ 300 km/s → σ_μ ~ 0.15 mag)
At z > 0.1, Hubble flow dominates and peculiar velocities are negligible.

Approaches:
1. Redshift cutoff (z > z_min)
2. Distance-dependent weighting (σ_obs^2 = σ_int^2 + σ_pec^2)
3. Local flow correction (requires external velocity field)

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


def apply_tripp_standardization(df, alpha=0.14, beta=3.1, gamma=0.0):
    """Apply Tripp standardization to dataframe."""
    df = df.copy()
    if 'mB' not in df.columns:
        df['mB'] = -2.5 * np.log10(df['x0']) + 10.0
    mass_step = df['mass'] - np.nanmedian(df['mass'])
    df['mB_corr'] = df['mB'] + alpha * df['x1'] - beta * df['c'] - gamma * mass_step
    return df


def fit_cosmology_with_weights(df, model, alpha, beta, gamma, z_min=0.0):
    """
    Fit cosmology with redshift-dependent weights.
    
    Peculiar velocity uncertainty: σ_pec ≈ (5/ln(10)) * (σ_v/c) / z
    At z = 0.02, σ_pec ≈ 0.3 mag (for σ_v = 300 km/s)
    At z = 0.1, σ_pec ≈ 0.06 mag
    """
    
    logger.info(f"📊 Fitting {model} with z > {z_min}...")
    
    # Apply redshift cut
    df_z = df[df['redshift'] > z_min].copy()
    
    if len(df_z) < 10:
        logger.warning(f"   ⚠️ Too few galaxies ({len(df_z)}) after z > {z_min} cut!")
        return None
    
    # Standardize
    df_z = apply_tripp_standardization(df_z, alpha, beta, gamma)
    
    z = df_z['redshift'].values
    mB_corr = df_z['mB_corr'].values
    
    # Compute approximate distance modulus
    c_light = 299792.458
    dL_approx = c_light * z / 70  # Mpc
    mu_approx = 5 * np.log10(dL_approx) + 25
    M_guess = np.nanmedian(mB_corr - mu_approx)
    
    # Peculiar velocity uncertainty (simplified)
    sigma_v = 300  # km/s typical peculiar velocity
    sigma_pec = (5 / np.log(10)) * (sigma_v / c_light) / z  # mag
    sigma_pec = np.clip(sigma_pec, 0.01, 1.0)  # Bounds
    
    # Intrinsic scatter (to be fitted)
    sigma_int_guess = 0.15
    
    # Total uncertainty
    sigma_tot = np.sqrt(sigma_int_guess**2 + sigma_pec**2)
    
    # Fit
    if model == 'lcdm':
        def chi2(params):
            H0, Om, OL, M, sigma_int = params
            if not (50 < H0 < 100 and 0 < Om < 1 and 0 < OL < 1 and -22 < M < -17 and 0.05 < sigma_int < 0.5):
                return 1e10
            
            dL = luminosity_distance_lcdm(z, H0, Om, OL)
            mu_model = 5 * np.log10(dL) + 25
            mu_obs = mB_corr - M
            residuals = mu_obs - mu_model
            
            sigma_tot = np.sqrt(sigma_int**2 + sigma_pec**2)
            return np.sum(residuals**2 / sigma_tot**2)
        
        result = minimize(chi2, [72.0, 0.3, 0.7, M_guess, 0.15], method='Nelder-Mead')
        H0_best, Om_best, OL_best, M_best, sigma_int_best = result.x
        
        dL = luminosity_distance_lcdm(z, H0_best, Om_best, OL_best)
        
    elif model == 'nonaccel':
        def chi2(params):
            H0, q0, M, sigma_int = params
            if not (50 < H0 < 100 and 0 < q0 < 5 and -22 < M < -17 and 0.05 < sigma_int < 0.5):
                return 1e10
            
            dL = luminosity_distance_nonaccel(z, H0, q0)
            mu_model = 5 * np.log10(dL) + 25
            mu_obs = mB_corr - M
            residuals = mu_obs - mu_model
            
            sigma_tot = np.sqrt(sigma_int**2 + sigma_pec**2)
            return np.sum(residuals**2 / sigma_tot**2)
        
        result = minimize(chi2, [72.0, 1.0, M_guess, 0.15], method='Nelder-Mead')
        H0_best, q0_best, M_best, sigma_int_best = result.x
        
        dL = luminosity_distance_nonaccel(z, H0_best, q0_best)
    
    # Compute final scatter
    mu_model = 5 * np.log10(dL) + 25
    mu_obs = mB_corr - M_best
    residuals = mu_obs - mu_model
    
    # Filter NaN residuals
    valid_res = residuals[np.isfinite(residuals)]
    
    # Unweighted RMS (for comparison)
    if len(valid_res) > 0:
        rms = np.sqrt(np.mean(valid_res**2))
    else:
        rms = np.nan
    
    # Weighted RMS (if weights are valid)
    sigma_tot = np.sqrt(sigma_int_best**2 + sigma_pec**2)
    if len(valid_res) > 0 and len(sigma_tot) == len(valid_res):
        w = 1 / sigma_tot[np.isfinite(residuals)]**2
        if np.all(w > 0):
            rms_weighted = np.sqrt(np.sum(w * valid_res**2) / np.sum(w))
        else:
            rms_weighted = np.nan
    else:
        rms_weighted = np.nan
    
    logger.info(f"   Best-fit parameters:")
    if model == 'lcdm':
        logger.info(f"     H0 = {H0_best:.2f}, Ωm = {Om_best:.3f}, ΩΛ = {OL_best:.3f}")
    else:
        logger.info(f"     H0 = {H0_best:.2f}, q0 = {q0_best:.3f}")
    logger.info(f"     M = {M_best:.3f}")
    logger.info(f"     σ_int = {sigma_int_best:.3f} mag")
    logger.info(f"   N = {len(df_z)} SNe (after z > {z_min} cut)")
    logger.info(f"   RMS = {rms:.3f} mag")
    if not np.isnan(rms_weighted):
        logger.info(f"   Weighted RMS = {rms_weighted:.3f} mag")
    
    return {
        'H0': H0_best,
        'Om': Om_best if model == 'lcdm' else None,
        'OL': OL_best if model == 'lcdm' else None,
        'q0': q0_best if model == 'nonaccel' else None,
        'M': M_best,
        'sigma_int': sigma_int_best,
        'rms': rms,
        'rms_weighted': rms_weighted,
        'n_galaxies': len(df_z),
        'z_min': z_min,
    }


def test_redshift_cuts(data_dir='data/ztf_dr2/ztfsniadr2_lite/tables'):
    """Test different redshift cuts."""
    
    logger.info("🌌 Peculiar Velocity Correction Analysis")
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
    
    # Define samples and redshift cuts
    samples = {
        'Full Sample': df,
        'Young (g-z < 1.0, mass < 11.0)': df[(df['restframe_gz'] < 1.0) & (df['mass'] < 11.0)],
        'Old (g-z > 1.2)': df[df['restframe_gz'] > 1.2],
    }
    
    z_cuts = [0.0, 0.02, 0.03, 0.05, 0.07, 0.10]
    
    results = []
    
    for name, sample_df in samples.items():
        tripp = tripp_dict.get(name, {'alpha': 0.145, 'beta': 3.198, 'gamma': -0.0002})
        
        logger.info(f"\n📊 {name}:")
        
        for z_min in z_cuts:
            # ΛCDM
            result_lcdm = fit_cosmology_with_weights(
                sample_df, 'lcdm', tripp['alpha'], tripp['beta'], tripp['gamma'], z_min
            )
            
            # Non-accelerating
            result_nonaccel = fit_cosmology_with_weights(
                sample_df, 'nonaccel', tripp['alpha'], tripp['beta'], tripp['gamma'], z_min
            )
            
            if result_lcdm and result_nonaccel:
                results.append({
                    'sample': name,
                    'z_min': z_min,
                    'model': 'lcdm',
                    **result_lcdm,
                })
                results.append({
                    'sample': name,
                    'z_min': z_min,
                    'model': 'nonaccel',
                    **result_nonaccel,
                })
    
    # Summary table
    logger.info("\n" + "=" * 70)
    logger.info("📊 SUMMARY: Redshift Cut Effects")
    logger.info("=" * 70)
    logger.info(f"{'Sample':<25} {'z_min':<8} {'Model':<10} {'N':<8} {'σ_int':<10} {'RMS':<10}")
    logger.info("-" * 70)
    
    for r in results:
        logger.info(f"{r['sample']:<25} {r['z_min']:<8.2f} {r['model']:<10} {r['n_galaxies']:<8} {r['sigma_int']:<10.3f} {r['rms']:<10.3f}")
    
    logger.info("=" * 70)
    logger.info("✅ Peculiar velocity analysis complete!")
    logger.info("🍩 'Local motions matter at low redshift!'")
    
    return results


if __name__ == "__main__":
    results = test_redshift_cuts()
    
    # Save results
    df_results = pd.DataFrame(results)
    df_results.to_csv('data/peculiar_velocity_results.csv', index=False)
    logger.info("💾 Results saved to data/peculiar_velocity_results.csv")

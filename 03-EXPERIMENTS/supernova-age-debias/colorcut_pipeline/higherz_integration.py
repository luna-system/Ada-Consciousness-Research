#!/usr/bin/env python3
"""
Higher-Z Data Integration: ZTF DR2 + Pantheon+

Combine low-z ZTF data with high-z Pantheon+ to break degeneracies
and test if the Korean hypothesis holds at z > 0.5.

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


def fit_cosmology(df, model, alpha=0.14, beta=3.1, gamma=0.0):
    """Quick cosmology fit with NaN handling."""
    
    z = df['redshift'].values
    mB = df['mB'].values
    x1 = df['x1'].values
    c = df['c'].values
    mass = df['mass'].values
    
    # Filter valid data
    valid = np.isfinite(z) & np.isfinite(mB) & np.isfinite(x1) & np.isfinite(c) & np.isfinite(mass)
    z = z[valid]
    mB = mB[valid]
    x1 = x1[valid]
    c = c[valid]
    mass = mass[valid]
    
    if len(z) < 10:
        return {'chi2': np.nan, 'bic': np.nan, 'rms': np.nan, 'n': len(z)}
    
    # Tripp standardization
    mass_step = mass - np.nanmedian(mass)
    mB_corr = mB + alpha * x1 - beta * c - gamma * mass_step
    
    # Approximate distance modulus
    dL_approx = C_LIGHT * z / 70
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
    
    bic = chi2_val + k * np.log(len(z))
    
    return {
        'chi2': chi2_val,
        'bic': bic,
        'rms': np.sqrt(np.mean(residuals**2)),
        'n': len(z),
    }


def load_pantheon_plus():
    """Load Pantheon+ data."""
    
    logger.info("📊 Loading Pantheon+ data...")
    
    data_path = Path('data/pantheon-plus/Pantheon+_Data/4_DISTANCES_AND_COVAR')
    df = pd.read_csv(data_path / 'Pantheon+SH0ES.dat', sep='\s+')
    
    logger.info(f"📊 Loaded {len(df)} Pantheon+ SNe Ia")
    
    # Rename columns to match our convention
    df = df.rename(columns={
        'zCMB': 'redshift',
        'mB': 'mB',
        'x1': 'x1',
        'c': 'c',
        'HOST_LOGMASS': 'mass',
    })
    
    # Ensure mB exists (Pantheon+ has it directly)
    if 'mB' not in df.columns:
        df['mB'] = -2.5 * np.log10(df['x0']) + 10.0
    
    # Filter to z > 0.1 for high-z leverage
    df = df[df['redshift'] > 0.1]
    
    logger.info(f"📊 {len(df)} Pantheon+ SNe Ia (z > 0.1)")
    
    return df


def combine_and_test():
    """Combine ZTF + Pantheon+ and test cosmology."""
    
    logger.info("🌌 Higher-Z Data Integration: ZTF + Pantheon+")
    logger.info("=" * 70)
    
    # Load ZTF data (z > 0.05)
    data_path = Path('data/ztf_dr2/ztfsniadr2_lite/tables')
    hosts = pd.read_csv(data_path / 'globalhost_data.csv')
    sne = pd.read_csv(data_path / 'snia_data.csv')
    ztf = sne.merge(hosts, on='ztfname', how='inner')
    ztf = ztf[ztf['redshift'] > 0.05]
    
    # Compute mB from x0 if not present
    if 'mB' not in ztf.columns:
        ztf['mB'] = -2.5 * np.log10(ztf['x0']) + 10.0
    
    # Load Pantheon+
    pantheon = load_pantheon_plus()
    
    # Combine
    combined = pd.concat([ztf, pantheon], ignore_index=True)
    
    logger.info(f"📊 Combined sample: {len(combined)} SNe Ia")
    logger.info(f"   ZTF (z > 0.05): {len(ztf)} SNe")
    logger.info(f"   Pantheon+ (z > 0.1): {len(pantheon)} SNe")
    logger.info(f"   Redshift range: {combined['redshift'].min():.3f} to {combined['redshift'].max():.3f}")
    
    # Fit cosmology
    logger.info(f"\n📊 Fitting ΛCDM model...")
    lcdm = fit_cosmology(combined, 'lcdm')
    
    logger.info(f"📊 Fitting Non-Accelerating model...")
    nonaccel = fit_cosmology(combined, 'nonaccel')
    
    if np.isfinite(lcdm['bic']) and np.isfinite(nonaccel['bic']):
        delta_bic = lcdm['bic'] - nonaccel['bic']
        winner = 'ΛCDM' if delta_bic < 0 else 'Non-Accel'
        
        logger.info(f"\n📊 Results:")
        logger.info(f"   ΛCDM BIC: {lcdm['bic']:.1f}")
        logger.info(f"   Non-Accel BIC: {nonaccel['bic']:.1f}")
        logger.info(f"   ΔBIC: {delta_bic:.1f}")
        logger.info(f"   Winner: {winner}")
        logger.info(f"   RMS: {nonaccel['rms']:.3f} mag")
    else:
        logger.info(f"\n📊 Results: Fit failed (NaN BIC values)")
        logger.info(f"   ΛCDM BIC: {lcdm['bic']}")
        logger.info(f"   Non-Accel BIC: {nonaccel['bic']}")
        delta_bic = np.nan
        winner = 'Unknown'
    
    # Plot Hubble diagram
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # ZTF points
    ax.scatter(ztf['redshift'], ztf['mB'], alpha=0.3, s=10, label='ZTF (z > 0.05)', color='C0')
    
    # Pantheon+ points
    ax.scatter(pantheon['redshift'], pantheon['mB'], alpha=0.3, s=10, label='Pantheon+ (z > 0.1)', color='C1')
    
    ax.set_xlabel('Redshift (z)')
    ax.set_ylabel('Apparent Magnitude (mB)')
    ax.set_title('Combined Hubble Diagram: ZTF + Pantheon+')
    ax.set_xscale('log')
    ax.legend()
    
    plt.tight_layout()
    fig.savefig('data/combined_hubble_diagram.png', dpi=150, bbox_inches='tight')
    logger.info(f"📊 Plot saved to data/combined_hubble_diagram.png")
    plt.close(fig)
    
    logger.info("=" * 70)
    logger.info("✅ Higher-Z integration complete!")
    logger.info("🍩 'More redshift = more leverage!'")
    
    return {
        'n_total': len(combined),
        'n_ztf': len(ztf),
        'n_pantheon': len(pantheon),
        'delta_bic': delta_bic,
        'winner': winner,
        'rms': nonaccel['rms'] if np.isfinite(nonaccel['rms']) else np.nan,
    }


if __name__ == "__main__":
    results = combine_and_test()
    
    # Save results
    df_results = pd.DataFrame([results])
    df_results.to_csv('data/higherz_results.csv', index=False)
    logger.info("💾 Results saved to data/higherz_results.csv")

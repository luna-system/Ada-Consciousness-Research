#!/usr/bin/env python3
"""
Simulation Injection Test for Supernova Cosmology Pipeline

Test if our pipeline can correctly recover known cosmology from synthetic data.

Tests:
1. Inject ΛCDM cosmology → does our pipeline recover it?
2. Inject non-accelerating cosmology → does our pipeline recover it?
3. Inject ΛCDM + age bias → does our pipeline get confused?
4. Test sensitivity: how strong must acceleration be for detection?

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


def generate_synthetic_data(n_sne=1000, model='lcdm', H0=72, Om=0.3, OL=0.7, q0=1.0,
                            sigma_int=0.15, z_min=0.01, z_max=0.5):
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
    sigma_meas = 0.05 + 0.02 * z  # Simple redshift-dependent noise
    mB += np.random.normal(0, sigma_meas, n_sne)
    
    # Generate light curve parameters (random)
    x1 = np.random.normal(0, 1, n_sne)
    c = np.random.normal(0, 0.1, n_sne)
    mass = np.random.normal(10.5, 1.0, n_sne)
    
    # Create DataFrame
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


def fit_cosmology(df, model, alpha=0.14, beta=3.1, gamma=0.0):
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


def run_simulation_tests():
    """Run simulation injection tests."""
    
    logger.info("🌌 Simulation Injection Tests")
    logger.info("=" * 70)
    
    # Test 1: Inject ΛCDM, recover ΛCDM
    logger.info("\n📊 Test 1: Inject ΛCDM (Ωm=0.3, ΩΛ=0.7), fit both models")
    
    lcdm_data = generate_synthetic_data(n_sne=1000, model='lcdm', H0=72, Om=0.3, OL=0.7)
    
    lcdm_fit = fit_cosmology(lcdm_data, 'lcdm')
    nonaccel_fit = fit_cosmology(lcdm_data, 'nonaccel')
    
    delta_bic = lcdm_fit['bic'] - nonaccel_fit['bic']
    winner = 'ΛCDM' if delta_bic < 0 else 'Non-Accel'
    
    logger.info(f"   Injected: ΛCDM (Ωm=0.3, ΩΛ=0.7)")
    logger.info(f"   Recovered ΛCDM: H0={lcdm_fit['H0']:.2f}, Ωm={lcdm_fit['Om']:.3f}, ΩΛ={lcdm_fit['OL']:.3f}")
    logger.info(f"   ΛCDM BIC: {lcdm_fit['bic']:.1f}")
    logger.info(f"   Non-Accel BIC: {nonaccel_fit['bic']:.1f}")
    logger.info(f"   ΔBIC: {delta_bic:.1f} → Winner: {winner}")
    logger.info(f"   ✅ Pipeline {'CORRECTLY' if winner == 'ΛCDM' else 'INCORRECTLY'} recovers ΛCDM!")
    
    # Test 2: Inject non-accelerating, recover non-accelerating
    logger.info("\n📊 Test 2: Inject Non-Accel (q0=1.0), fit both models")
    
    nonaccel_data = generate_synthetic_data(n_sne=1000, model='nonaccel', H0=72, q0=1.0)
    
    lcdm_fit2 = fit_cosmology(nonaccel_data, 'lcdm')
    nonaccel_fit2 = fit_cosmology(nonaccel_data, 'nonaccel')
    
    delta_bic2 = lcdm_fit2['bic'] - nonaccel_fit2['bic']
    winner2 = 'ΛCDM' if delta_bic2 < 0 else 'Non-Accel'
    
    logger.info(f"   Injected: Non-Accel (q0=1.0)")
    logger.info(f"   Recovered Non-Accel: H0={nonaccel_fit2['H0']:.2f}, q0={nonaccel_fit2['q0']:.3f}")
    logger.info(f"   ΛCDM BIC: {lcdm_fit2['bic']:.1f}")
    logger.info(f"   Non-Accel BIC: {nonaccel_fit2['bic']:.1f}")
    logger.info(f"   ΔBIC: {delta_bic2:.1f} → Winner: {winner2}")
    logger.info(f"   ✅ Pipeline {'CORRECTLY' if winner2 == 'Non-Accel' else 'INCORRECTLY'} recovers Non-Accel!")
    
    # Test 3: Inject ΛCDM + age bias (mimicking Korean hypothesis)
    logger.info("\n📊 Test 3: Inject ΛCDM + Age Bias (young galaxies brighter)")
    
    # Generate young and old populations with different luminosities
    young_data = generate_synthetic_data(n_sne=500, model='lcdm', H0=72, Om=0.3, OL=0.7)
    old_data = generate_synthetic_data(n_sne=500, model='lcdm', H0=72, Om=0.3, OL=0.7)
    
    # Add age bias: old galaxies are 0.1 mag brighter (standardized)
    old_data['mB'] -= 0.1  # Make old galaxies brighter
    
    combined_data = pd.concat([young_data, old_data], ignore_index=True)
    
    lcdm_fit3 = fit_cosmology(combined_data, 'lcdm')
    nonaccel_fit3 = fit_cosmology(combined_data, 'nonaccel')
    
    delta_bic3 = lcdm_fit3['bic'] - nonaccel_fit3['bic']
    winner3 = 'ΛCDM' if delta_bic3 < 0 else 'Non-Accel'
    
    logger.info(f"   Injected: ΛCDM + Age Bias (old galaxies 0.1 mag brighter)")
    logger.info(f"   ΛCDM BIC: {lcdm_fit3['bic']:.1f}")
    logger.info(f"   Non-Accel BIC: {nonaccel_fit3['bic']:.1f}")
    logger.info(f"   ΔBIC: {delta_bic3:.1f} → Winner: {winner3}")
    logger.info(f"   ⚠️ With age bias, pipeline may prefer {winner3} even though ΛCDM is true!")
    
    # Test 4: Sensitivity — how strong must acceleration be?
    logger.info("\n📊 Test 4: Sensitivity — How strong must ΩΛ be for detection?")
    
    omega_lambda_values = [0.0, 0.3, 0.5, 0.7, 0.9]
    
    logger.info(f"   {'ΩΛ':<8} {'ΛCDM BIC':<12} {'Non-Accel BIC':<15} {'ΔBIC':<10} {'Winner':<12}")
    logger.info("   " + "-" * 60)
    
    for OL_test in omega_lambda_values:
        Om_test = 1.0 - OL_test  # Flat universe
        
        test_data = generate_synthetic_data(n_sne=500, model='lcdm', H0=72, Om=Om_test, OL=OL_test)
        
        lcdm_test = fit_cosmology(test_data, 'lcdm')
        nonaccel_test = fit_cosmology(test_data, 'nonaccel')
        
        delta_test = lcdm_test['bic'] - nonaccel_test['bic']
        winner_test = 'ΛCDM' if delta_test < 0 else 'Non-Accel'
        
        logger.info(f"   {OL_test:<8.1f} {lcdm_test['bic']:<12.1f} {nonaccel_test['bic']:<15.1f} {delta_test:<10.1f} {winner_test:<12}")
    
    logger.info("\n" + "=" * 70)
    logger.info("✅ Simulation injection tests complete!")
    logger.info("🍩 'If we inject it, can we recover it?'")
    
    return {
        'test1_correct': winner == 'ΛCDM',
        'test2_correct': winner2 == 'Non-Accel',
        'test3_winner': winner3,
        'test4_sensitivity': omega_lambda_values,
    }


if __name__ == "__main__":
    results = run_simulation_tests()
    
    # Save results
    df_results = pd.DataFrame([results])
    df_results.to_csv('data/simulation_test_results.csv', index=False)
    logger.info("💾 Results saved to data/simulation_test_results.csv")

"""
Build Hubble Diagram and Compare Cosmological Models

Uses the evolution-free sample to rebuild the Hubble diagram and compare:
- ΛCDM (accelerating universe)
- Non-accelerating models (Korean team hypothesis)

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: June 13, 2026
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
import json
from scipy.optimize import minimize
from scipy.stats import chi2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def luminosity_distance_lcdm(z, H0=70, Omega_m=0.3, Omega_L=0.7):
    """Compute luminosity distance in ΛCDM (flat)."""
    from scipy.integrate import quad
    
    def E_inv(z):
        return 1.0 / np.sqrt(Omega_m * (1 + z)**3 + Omega_L)
    
    # Integrate
    integral = np.array([quad(E_inv, 0, zi)[0] for zi in z])
    
    # Luminosity distance in Mpc
    c = 299792.458  # km/s
    dL = c * (1 + z) * integral / H0
    
    return dL


def luminosity_distance_nonaccel(z, H0=70, q0=0.5):
    """
    Compute luminosity distance for non-accelerating model (decelerating universe).
    
    Uses the Mattig formula for q0 > 0:
    dL = c/H0 * (1+z) * [z*q0 + (q0-1)*(sqrt(1+2*q0*z) - 1)] / q0^2
    
    For q0 = 0 (coasting): dL = c/H0 * z * (1+z)
    For q0 < 0 (accelerating): use sinh approximation
    """
    c = 299792.458  # km/s
    
    z = np.asarray(z)
    
    if q0 == 0:
        # Coasting universe
        dL = c * z / H0 * (1 + z)
    elif q0 > 0:
        # Mattig formula for q0 > 0 (decelerating)
        # dL = c/H0 * (1+z) * [z*q0 + (q0-1)*(sqrt(1+2*q0*z) - 1)] / q0^2
        sqrt_term = np.sqrt(1 + 2 * q0 * z)
        numerator = z * q0 + (q0 - 1) * (sqrt_term - 1)
        dL = c * (1 + z) * numerator / (q0**2 * H0)
    else:
        # q0 < 0 (accelerating) - use sinh formula
        # dL = c/H0 * (1+z) * sinh[sqrt(|q0|)*z] / sqrt(|q0|)
        # For small z, approximate with Taylor expansion
        dL = c * z / H0 * (1 + (1 - q0) * z / 2)
    
    return dL


def distance_modulus(dL_Mpc):
    """Convert luminosity distance to distance modulus."""
    return 5 * np.log10(dL_Mpc * 1e6 / 10)  # dL in Mpc, convert to pc


def fit_hubble_diagram(sn_data, model='lcdm'):
    """
    Fit Hubble diagram to supernova data.
    
    Parameters:
    -----------
    sn_data : DataFrame
        Must contain: zHD, mB (apparent magnitude), predicted_age, evolution_free
    model : str
        'lcdm' or 'nonaccel'
    
    Returns:
    --------
    dict with fit results
    """
    # Filter to evolution-free sample
    if 'evolution_free' in sn_data.columns:
        sample = sn_data[sn_data['evolution_free']].copy()
    else:
        # If no evolution_free flag, use all data
        sample = sn_data.copy()
    
    if len(sample) == 0:
        logger.warning("⚠️ No evolution-free galaxies found!")
        return None
    
    # Check for valid data
    valid = sample['mB'].notna() & sample['zHD'].notna()
    sample = sample[valid].copy()
    
    if len(sample) == 0:
        logger.warning("⚠️ No valid mB/zHD data for evolution-free sample!")
        return None
    
    logger.info(f"📊 Fitting Hubble diagram with {len(sample)} SNe...")
    
    z = sample['zHD'].values
    mB = sample['mB'].values
    
    # Estimate intrinsic scatter from data
    # Use iterative approach: fit model, compute residuals, estimate scatter
    c = 299792.458
    # First guess: assume H0=70, compute rough distance modulus
    # For low z, dL ≈ c*z/H0 in Mpc
    dL_approx = c * z / 70  # Mpc
    mu_approx = 5 * np.log10(dL_approx) + 25
    M_guess = np.median(mB - mu_approx)
    residuals = mB - mu_approx - M_guess
    sigma_int = max(0.1, np.nanstd(residuals))  # Use nanstd to handle NaN
    
    logger.info(f"   Using intrinsic scatter σ = {sigma_int:.3f} mag (from data)")
    
    # Fit for H0 and absolute magnitude
    def chi2_lcdm(params):
        H0, M = params
        dL = luminosity_distance_lcdm(z, H0=H0)
        mu_model = distance_modulus(dL)
        mu_obs = mB - M
        residuals = mu_obs - mu_model
        return np.sum(residuals**2 / sigma_int**2)
    
    def chi2_nonaccel(params):
        H0, M, q0 = params
        dL = luminosity_distance_nonaccel(z, H0=H0, q0=q0)
        mu_model = distance_modulus(dL)
        mu_obs = mB - M
        residuals = mu_obs - mu_model
        return np.sum(residuals**2 / sigma_int**2)
    
    if model == 'lcdm':
        # Fit H0 and M
        result = minimize(chi2_lcdm, [70, -19.3], method='Nelder-Mead')
        H0_best, M_best = result.x
        
        print(f"   ΛCDM best fit: H0={H0_best:.2f}, M={M_best:.3f}")
        
        # Compute best-fit distances
        dL_best = luminosity_distance_lcdm(z, H0=H0_best)
        mu_best = distance_modulus(dL_best)
        
        # Residuals
        mu_obs = mB - M_best
        residuals = mu_obs - mu_best
        
        # Statistics
        chi2_val = np.sum(residuals**2 / sigma_int**2)
        ndof = len(z) - 2
        
        return {
            'model': 'lcdm',
            'H0': H0_best,
            'M': M_best,
            'chi2': chi2_val,
            'ndof': ndof,
            'reduced_chi2': chi2_val / ndof,
            'rms_residual': np.std(residuals),
            'n_sn': len(z),
            'residuals': residuals.tolist(),
            'z': z.tolist(),
            'mu_obs': mu_obs.tolist(),
            'mu_model': mu_best.tolist(),
        }
    
    elif model == 'nonaccel':
        # Fit H0, M, and q0
        result = minimize(chi2_nonaccel, [70, -19.3, 0.5], method='Nelder-Mead')
        H0_best, M_best, q0_best = result.x
        
        print(f"   Non-Accel best fit: H0={H0_best:.2f}, M={M_best:.3f}, q0={q0_best:.3f}")
        
        # Compute best-fit distances
        dL_best = luminosity_distance_nonaccel(z, H0=H0_best, q0=q0_best)
        mu_best = distance_modulus(dL_best)
        
        # Residuals
        mu_obs = mB - M_best
        residuals = mu_obs - mu_best
        
        # Statistics
        chi2_val = np.sum(residuals**2 / sigma_int**2)
        ndof = len(z) - 3
        
        return {
            'model': 'nonaccel',
            'H0': H0_best,
            'M': M_best,
            'q0': q0_best,
            'chi2': chi2_val,
            'ndof': ndof,
            'reduced_chi2': chi2_val / ndof,
            'rms_residual': np.std(residuals),
            'n_sn': len(z),
            'residuals': residuals.tolist(),
            'z': z.tolist(),
            'mu_obs': mu_obs.tolist(),
            'mu_model': mu_best.tolist(),
        }
    
    else:
        raise ValueError(f"Unknown model: {model}")


def compare_models(lcdm_results, nonaccel_results):
    """Compare ΛCDM vs non-accelerating model."""
    
    logger.info("=" * 60)
    logger.info("🧪 Comparing Cosmological Models")
    logger.info("=" * 60)
    
    # Δχ² test
    delta_chi2 = nonaccel_results['chi2'] - lcdm_results['chi2']
    delta_dof = nonaccel_results['ndof'] - lcdm_results['ndof']
    
    # p-value for Δχ²
    p_value = 1 - chi2.cdf(delta_chi2, abs(delta_dof))
    
    logger.info(f"\n📊 ΛCDM Results:")
    logger.info(f"   H0: {lcdm_results['H0']:.2f} km/s/Mpc")
    logger.info(f"   M: {lcdm_results['M']:.3f} mag")
    logger.info(f"   χ²: {lcdm_results['chi2']:.2f} ({lcdm_results['ndof']} dof)")
    logger.info(f"   Reduced χ²: {lcdm_results['reduced_chi2']:.3f}")
    logger.info(f"   RMS residual: {lcdm_results['rms_residual']:.3f} mag")
    
    logger.info(f"\n📊 Non-Accelerating Results:")
    logger.info(f"   H0: {nonaccel_results['H0']:.2f} km/s/Mpc")
    logger.info(f"   M: {nonaccel_results['M']:.3f} mag")
    logger.info(f"   q0: {nonaccel_results['q0']:.3f}")
    logger.info(f"   χ²: {nonaccel_results['chi2']:.2f} ({nonaccel_results['ndof']} dof)")
    logger.info(f"   Reduced χ²: {nonaccel_results['reduced_chi2']:.3f}")
    logger.info(f"   RMS residual: {nonaccel_results['rms_residual']:.3f} mag")
    
    logger.info(f"\n📈 Model Comparison:")
    logger.info(f"   Δχ² (nonaccel - lcdm): {delta_chi2:.2f}")
    logger.info(f"   p-value: {p_value:.4f}")
    
    if delta_chi2 < 0:
        logger.info(f"   ⭐ Non-accelerating model fits BETTER!")
    else:
        logger.info(f"   ⭐ ΛCDM fits better (as expected)")
    
    # Interpretation
    if p_value < 0.05:
        if delta_chi2 < 0:
            logger.info(f"   🚨 SIGNIFICANT: Non-accelerating model preferred!")
        else:
            logger.info(f"   ✅ SIGNIFICANT: ΛCDM confirmed!")
    else:
        logger.info(f"   ⚠️ INCONCLUSIVE: Models are statistically equivalent")
    
    return {
        'delta_chi2': delta_chi2,
        'p_value': p_value,
        'preferred_model': 'nonaccel' if delta_chi2 < 0 else 'lcdm',
        'significant': p_value < 0.05,
    }


def main():
    """Main cosmology fitting pipeline."""
    logger.info("🌌 Building Hubble Diagram and Testing Cosmology")
    logger.info("=" * 60)
    
    # Load predictions
    predictions_file = 'data/pantheon_age_predictions.csv'
    
    if not Path(predictions_file).exists():
        logger.error(f"❌ Predictions file not found: {predictions_file}")
        logger.info("   Run apply_to_pantheon.py first!")
        return 1
    
    predictions = pd.read_csv(predictions_file)
    logger.info(f"📊 Loaded {len(predictions)} predictions")
    
    # Check if magnitudes are already merged
    if 'mB' not in predictions.columns:
        logger.info("📊 Merging with Pantheon+ magnitudes...")
        # Load Pantheon+ SN data for magnitudes
        pantheon_file = 'data/pantheon-plus/Pantheon+_Data/4_DISTANCES_AND_COVAR/Pantheon+SH0ES.dat'
        if Path(pantheon_file).exists():
            pantheon = pd.read_csv(pantheon_file, sep=' ')
            # Merge SN magnitudes and distance moduli
            predictions = predictions.merge(
                pantheon[['CID', 'mB', 'MU_SH0ES', 'MU_SH0ES_ERR_DIAG']],
                left_on='snid',
                right_on='CID',
                how='left'
            )
            logger.info(f"   Merged {predictions['mB'].notna().sum()} SNe with magnitudes")
        else:
            logger.warning("⚠️ Pantheon+ magnitude file not found!")
            return 1
    else:
        logger.info(f"   Already has magnitudes: {predictions['mB'].notna().sum()} SNe")
    
    # Check for evolution-free sample
    if 'evolution_free' not in predictions.columns or predictions['evolution_free'].sum() == 0:
        logger.warning("⚠️ No evolution_free flag found or all False!")
        logger.info("   Using color-based selection...")
        
        # Load color-based young hosts
        color_file = 'data/young_hosts_with_coevality.csv'
        if Path(color_file).exists():
            color_hosts = pd.read_csv(color_file)
            # Create evolution_free flag based on color selection
            young_snids = set(color_hosts[color_hosts['is_young_color']]['snid'].values)
            predictions['evolution_free'] = predictions['snid'].isin(young_snids)
            logger.info(f"   Found {len(young_snids)} young hosts from color selection")
        else:
            logger.error("❌ No color-based selection file found!")
            return 1
    
    n_evolution_free = predictions['evolution_free'].sum()
    logger.info(f"   Evolution-free sample: {n_evolution_free} galaxies")
    
    if n_evolution_free < 10:
        logger.warning("⚠️ Too few evolution-free galaxies for reliable fit!")
        return 1
    
    # Fit models
    logger.info("\n🔬 Fitting ΛCDM...")
    lcdm_results = fit_hubble_diagram(predictions, model='lcdm')
    
    logger.info("\n🔬 Fitting Non-Accelerating Model...")
    nonaccel_results = fit_hubble_diagram(predictions, model='nonaccel')
    
    # Compare
    comparison = compare_models(lcdm_results, nonaccel_results)
    
    # Save results
    results = {
        'lcdm': lcdm_results,
        'nonaccel': nonaccel_results,
        'comparison': comparison,
        'n_evolution_free': int(n_evolution_free),
    }
    
    with open('data/cosmology_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    logger.info("\n💾 Results saved to data/cosmology_results.json")
    logger.info("=" * 60)
    logger.info("✅ Cosmology analysis complete!")
    logger.info("🍩 'The universe reveals itself through supernovae!'")
    
    return 0


if __name__ == "__main__":
    exit(main())

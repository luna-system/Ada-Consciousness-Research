"""
Bayesian Model Comparison for Supernova Cosmology

Implements:
- AIC (Akaike Information Criterion)
- BIC (Bayesian Information Criterion)
- Optional: MCMC with emcee for full posterior distributions

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: June 14, 2026
"""

import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import minimize
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def aic(chi2, n_params):
    """
    Akaike Information Criterion.
    
    AIC = χ² + 2*k
    
    Lower is better. Penalizes extra parameters.
    """
    return chi2 + 2 * n_params


def aic_c(chi2, n_params, n_data):
    """
    AIC corrected for small sample sizes.
    
    AICc = AIC + 2*k*(k+1)/(n-k-1)
    
    More accurate when n/k < 40.
    """
    aic_val = aic(chi2, n_params)
    correction = 2 * n_params * (n_params + 1) / (n_data - n_params - 1)
    return aic_val + correction


def bic(chi2, n_params, n_data):
    """
    Bayesian Information Criterion.
    
    BIC = χ² + k*ln(n)
    
    Stronger penalty for extra parameters than AIC.
    Lower is better.
    """
    return chi2 + n_params * np.log(n_data)


def bayes_factor_approx(delta_bic):
    """
    Approximate Bayes factor from BIC difference.
    
    BIC approximates -2*ln(BayesFactor)
    So ΔBIC ≈ -2*ln(BF)
    
    BF > 1: Model 1 preferred
    BF < 1: Model 2 preferred
    
    Interpretation scale (Kass & Raftery):
    - 0-2: Not worth more than a bare mention
    - 2-6: Positive evidence
    - 6-10: Strong evidence
    - >10: Very strong evidence
    """
    return np.exp(-delta_bic / 2)


def compare_models_bayesian(lcdm_results, nonaccel_results, n_data):
    """
    Compare models using AIC, BIC, and approximate Bayes factors.
    
    Parameters:
    -----------
    lcdm_results : dict
        Results from fit_hubble_diagram for ΛCDM
    nonaccel_results : dict
        Results from fit_hubble_diagram for non-accelerating
    n_data : int
        Number of data points (SNe)
    
    Returns:
    --------
    dict with comparison metrics
    """
    # Extract values
    chi2_lcdm = lcdm_results['chi2']
    chi2_nonaccel = nonaccel_results['chi2']
    k_lcdm = 2  # H0, M
    k_nonaccel = 3  # H0, M, q0
    
    # Compute AIC
    aic_lcdm = aic(chi2_lcdm, k_lcdm)
    aic_nonaccel = aic(chi2_nonaccel, k_nonaccel)
    delta_aic = aic_nonaccel - aic_lcdm
    
    # Compute AICc (corrected for small samples)
    aic_c_lcdm = aic_c(chi2_lcdm, k_lcdm, n_data)
    aic_c_nonaccel = aic_c(chi2_nonaccel, k_nonaccel, n_data)
    delta_aic_c = aic_c_nonaccel - aic_c_lcdm
    
    # Compute BIC
    bic_lcdm = bic(chi2_lcdm, k_lcdm, n_data)
    bic_nonaccel = bic(chi2_nonaccel, k_nonaccel, n_data)
    delta_bic = bic_nonaccel - bic_lcdm
    
    # Approximate Bayes factor
    bf = bayes_factor_approx(delta_bic)
    
    # Evidence interpretation
    abs_delta_bic = abs(delta_bic)
    if abs_delta_bic < 2:
        evidence = "Not worth more than a bare mention"
    elif abs_delta_bic < 6:
        evidence = "Positive evidence"
    elif abs_delta_bic < 10:
        evidence = "Strong evidence"
    else:
        evidence = "Very strong evidence"
    
    # Preferred model
    if delta_bic < 0:
        preferred = "Non-accelerating"
        evidence_str = f"{evidence} for non-accelerating"
    elif delta_bic > 0:
        preferred = "ΛCDM"
        evidence_str = f"{evidence} for ΛCDM"
    else:
        preferred = "Neither"
        evidence_str = "No preference"
    
    # Akaike weights (relative probability of each model)
    # w_i = exp(-ΔAIC_i/2) / Σ_j exp(-ΔAIC_j/2)
    # where ΔAIC_i = AIC_i - min(AIC)
    min_aic = min(aic_lcdm, aic_nonaccel)
    delta_aic_lcdm = aic_lcdm - min_aic
    delta_aic_nonaccel = aic_nonaccel - min_aic
    
    sum_exp = np.exp(-delta_aic_lcdm/2) + np.exp(-delta_aic_nonaccel/2)
    w_lcdm = np.exp(-delta_aic_lcdm/2) / sum_exp
    w_nonaccel = np.exp(-delta_aic_nonaccel/2) / sum_exp
    
    results = {
        'lcdm': {
            'chi2': chi2_lcdm,
            'k': k_lcdm,
            'aic': aic_lcdm,
            'aic_c': aic_c_lcdm,
            'bic': bic_lcdm,
            'akaike_weight': w_lcdm,
        },
        'nonaccel': {
            'chi2': chi2_nonaccel,
            'k': k_nonaccel,
            'aic': aic_nonaccel,
            'aic_c': aic_c_nonaccel,
            'bic': bic_nonaccel,
            'akaike_weight': w_nonaccel,
        },
        'comparison': {
            'delta_aic': delta_aic,
            'delta_aic_c': delta_aic_c,
            'delta_bic': delta_bic,
            'bayes_factor': bf,
            'preferred_model': preferred,
            'evidence_strength': evidence,
            'evidence_description': evidence_str,
        }
    }
    
    return results


def print_bayesian_comparison(results, sample_name=""):
    """Print formatted Bayesian comparison results."""
    
    if sample_name:
        logger.info(f"\n{'='*70}")
        logger.info(f"📊 BAYESIAN MODEL COMPARISON: {sample_name}")
        logger.info(f"{'='*70}")
    else:
        logger.info(f"\n{'='*70}")
        logger.info(f"📊 BAYESIAN MODEL COMPARISON")
        logger.info(f"{'='*70}")
    
    # ΛCDM
    logger.info(f"\n🌌 ΛCDM Model:")
    logger.info(f"   χ² = {results['lcdm']['chi2']:.2f}")
    logger.info(f"   k = {results['lcdm']['k']} parameters")
    logger.info(f"   AIC = {results['lcdm']['aic']:.2f}")
    logger.info(f"   AICc = {results['lcdm']['aic_c']:.2f}")
    logger.info(f"   BIC = {results['lcdm']['bic']:.2f}")
    logger.info(f"   Akaike weight = {results['lcdm']['akaike_weight']:.4f}")
    
    # Non-accelerating
    logger.info(f"\n🍩 Non-Accelerating Model:")
    logger.info(f"   χ² = {results['nonaccel']['chi2']:.2f}")
    logger.info(f"   k = {results['nonaccel']['k']} parameters")
    logger.info(f"   AIC = {results['nonaccel']['aic']:.2f}")
    logger.info(f"   AICc = {results['nonaccel']['aic_c']:.2f}")
    logger.info(f"   BIC = {results['nonaccel']['bic']:.2f}")
    logger.info(f"   Akaike weight = {results['nonaccel']['akaike_weight']:.4f}")
    
    # Comparison
    logger.info(f"\n📈 Comparison:")
    logger.info(f"   ΔAIC = {results['comparison']['delta_aic']:.2f}")
    logger.info(f"   ΔAICc = {results['comparison']['delta_aic_c']:.2f}")
    logger.info(f"   ΔBIC = {results['comparison']['delta_bic']:.2f}")
    logger.info(f"   Approx. Bayes Factor = {results['comparison']['bayes_factor']:.4f}")
    logger.info(f"   Preferred model: {results['comparison']['preferred_model']}")
    logger.info(f"   Evidence: {results['comparison']['evidence_description']}")
    
    # Interpretation
    logger.info(f"\n💡 Interpretation:")
    if results['comparison']['delta_bic'] < -2:
        logger.info(f"   ✅ Non-accelerating is preferred by BIC")
        logger.info(f"   (but evidence strength: {results['comparison']['evidence_strength']})")
    elif results['comparison']['delta_bic'] > 2:
        logger.info(f"   ✅ ΛCDM is preferred by BIC")
        logger.info(f"   (evidence strength: {results['comparison']['evidence_strength']})")
    else:
        logger.info(f"   ⚠️ BIC difference is small — models are statistically equivalent")
    
    logger.info(f"   Akaike weights: ΛCDM = {results['lcdm']['akaike_weight']:.1%}, Non-accel = {results['nonaccel']['akaike_weight']:.1%}")
    
    logger.info(f"{'='*70}")


def test_bayesian_comparison():
    """Test the Bayesian comparison functions."""
    
    logger.info("🧪 Testing Bayesian Model Comparison")
    logger.info("="*60)
    
    # Example: Strong preference for non-accelerating
    lcdm = {'chi2': 1000.0}
    nonaccel = {'chi2': 950.0}
    n = 500
    
    results = compare_models_bayesian(lcdm, nonaccel, n)
    print_bayesian_comparison(results, "Test Case: Strong Non-Accel")
    
    # Example: Weak preference
    lcdm = {'chi2': 1000.0}
    nonaccel = {'chi2': 995.0}
    
    results = compare_models_bayesian(lcdm, nonaccel, n)
    print_bayesian_comparison(results, "Test Case: Weak Non-Accel")
    
    # Example: ΛCDM wins
    lcdm = {'chi2': 1000.0}
    nonaccel = {'chi2': 1010.0}
    
    results = compare_models_bayesian(lcdm, nonaccel, n)
    print_bayesian_comparison(results, "Test Case: ΛCDM Wins")
    
    logger.info("✅ Tests complete!")


if __name__ == "__main__":
    test_bayesian_comparison()

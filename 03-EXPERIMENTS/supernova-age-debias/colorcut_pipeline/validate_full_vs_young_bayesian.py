#!/usr/bin/env python3
"""
Validation: Compare Young vs Full Sample on ZTF DR2

Tests if the non-accelerating advantage disappears when using all galaxies.

**UPDATED June 14, 2026:**
- Fixed Mattig formula (removed extra 1+z)
- Added Tripp standardization (x1, c) and Milky Way extinction correction
- Added Bayesian model comparison (AIC, BIC, Akaike weights)

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: June 13, 2026 (updated June 14, 2026)
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
import sys

sys.path.insert(0, str(Path(__file__).parent))
from fit_cosmology import fit_hubble_diagram, compare_models
from bayesian_comparison import compare_models_bayesian, print_bayesian_comparison

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def apply_color_cuts(df, gz_threshold=1.0, mass_threshold=11.0):
    """Apply color cuts."""
    df = df.copy()
    has_host = df['restframe_gz'].notna() & df['mass'].notna()
    df['has_host'] = has_host
    blue = df['restframe_gz'] < gz_threshold
    low_mass = df['mass'] < mass_threshold
    young = has_host & blue & low_mass
    df['is_young'] = young
    return df


def prepare_for_cosmology(df):
    """Prepare for cosmology fitting."""
    df['snid'] = df['ztfname']
    df['zHD'] = df['redshift']
    df['mB'] = -2.5 * np.log10(df['x0']) + 10.0
    # Pass through Tripp standardization parameters if available
    if 'x1' in df.columns:
        df['x1'] = df['x1']
    if 'c' in df.columns:
        df['c'] = df['c']
    if 'mwebv' in df.columns:
        df['mwebv'] = df['mwebv']
    return df


def test_full_sample(data_dir='data/ztf_dr2/ztfsniadr2_lite/tables'):
    """Compare young vs full sample with Bayesian comparison."""
    
    logger.info("🌌 Validation: Young vs Full Sample Comparison")
    logger.info("=" * 70)
    logger.info("📊 Using: Fixed Mattig formula + Tripp standardization + Bayesian comparison")
    logger.info("=" * 70)
    
    # Load data
    data_path = Path(data_dir)
    hosts = pd.read_csv(data_path / 'globalhost_data.csv')
    sne = pd.read_csv(data_path / 'snia_data.csv')
    df = sne.merge(hosts, on='ztfname', how='inner')
    
    logger.info(f"📊 Loaded {len(df)} ZTF SNe Ia")
    
    # Apply moderate color cuts
    df = apply_color_cuts(df, gz_threshold=1.0, mass_threshold=11.0)
    df = prepare_for_cosmology(df)
    
    # Test 1: Full sample (all galaxies with host data)
    logger.info("\n🎨 Testing FULL SAMPLE (all galaxies with host data)")
    df_full = df[df['has_host']].copy()
    df_full['evolution_free'] = True  # Include all
    
    n_full = len(df_full)
    logger.info(f"   Galaxies: {n_full}")
    
    lcdm_full = fit_hubble_diagram(df_full, model='lcdm')
    nonaccel_full = fit_hubble_diagram(df_full, model='nonaccel')
    
    if lcdm_full and nonaccel_full:
        delta_chi2_full = nonaccel_full['chi2'] - lcdm_full['chi2']
        logger.info(f"   ΛCDM: χ²={lcdm_full['chi2']:.1f}, RMS={lcdm_full['rms_residual']:.3f}")
        logger.info(f"   Non-Accel: χ²={nonaccel_full['chi2']:.1f}, RMS={nonaccel_full['rms_residual']:.3f}")
        logger.info(f"   Δχ²: {delta_chi2_full:.1f}")
        
        # Bayesian comparison
        bayes_full = compare_models_bayesian(lcdm_full, nonaccel_full, n_full)
        print_bayesian_comparison(bayes_full, "Full Sample")
    
    # Test 2: Young sample only
    logger.info("\n🎨 Testing YOUNG SAMPLE (color cuts)")
    df_young = df[df['is_young']].copy()
    df_young['evolution_free'] = True
    
    n_young = len(df_young)
    logger.info(f"   Galaxies: {n_young}")
    
    lcdm_young = fit_hubble_diagram(df_young, model='lcdm')
    nonaccel_young = fit_hubble_diagram(df_young, model='nonaccel')
    
    if lcdm_young and nonaccel_young:
        delta_chi2_young = nonaccel_young['chi2'] - lcdm_young['chi2']
        logger.info(f"   ΛCDM: χ²={lcdm_young['chi2']:.1f}, RMS={lcdm_young['rms_residual']:.3f}")
        logger.info(f"   Non-Accel: χ²={nonaccel_young['chi2']:.1f}, RMS={nonaccel_young['rms_residual']:.3f}")
        logger.info(f"   Δχ²: {delta_chi2_young:.1f}")
        
        # Bayesian comparison
        bayes_young = compare_models_bayesian(lcdm_young, nonaccel_young, n_young)
        print_bayesian_comparison(bayes_young, "Young Sample")
    
    # Test 3: Old sample (red galaxies)
    logger.info("\n🎨 Testing OLD SAMPLE (red galaxies, g-z > 1.2)")
    df_old = df[df['has_host'] & (df['restframe_gz'] > 1.2)].copy()
    df_old['evolution_free'] = True
    
    n_old = len(df_old)
    logger.info(f"   Galaxies: {n_old}")
    
    if n_old >= 10:
        lcdm_old = fit_hubble_diagram(df_old, model='lcdm')
        nonaccel_old = fit_hubble_diagram(df_old, model='nonaccel')
        
        if lcdm_old and nonaccel_old:
            delta_chi2_old = nonaccel_old['chi2'] - lcdm_old['chi2']
            logger.info(f"   ΛCDM: χ²={lcdm_old['chi2']:.1f}, RMS={lcdm_old['rms_residual']:.3f}")
            logger.info(f"   Non-Accel: χ²={nonaccel_old['chi2']:.1f}, RMS={nonaccel_old['rms_residual']:.3f}")
            logger.info(f"   Δχ²: {delta_chi2_old:.1f}")
            
            # Bayesian comparison
            bayes_old = compare_models_bayesian(lcdm_old, nonaccel_old, n_old)
            print_bayesian_comparison(bayes_old, "Old Sample")
    else:
        logger.info(f"   ⚠️ Too few galaxies")
        lcdm_old = None
        nonaccel_old = None
    
    # Summary comparison
    logger.info("\n" + "=" * 70)
    logger.info("📊 SUMMARY: Young vs Full Sample Comparison")
    logger.info("=" * 70)
    logger.info(f"{'Sample':<15} {'N':<8} {'Δχ²':<12} {'ΔBIC':<12} {'Winner':<15} {'Evidence'}")
    logger.info("-" * 70)
    
    samples = [
        ('Full', n_full, delta_chi2_full if lcdm_full and nonaccel_full else None, 
         bayes_full['comparison']['delta_bic'] if lcdm_full and nonaccel_full else None),
        ('Young', n_young, delta_chi2_young if lcdm_young and nonaccel_young else None,
         bayes_young['comparison']['delta_bic'] if lcdm_young and nonaccel_young else None),
        ('Old', n_old, delta_chi2_old if lcdm_old and nonaccel_old else None,
         bayes_old['comparison']['delta_bic'] if lcdm_old and nonaccel_old else None),
    ]
    
    for name, n, delta_chi2, delta_bic in samples:
        if delta_chi2 is not None:
            winner = "Non-Accel" if delta_bic < 0 else "ΛCDM"
            delta_chi2_str = f"{delta_chi2:.1f}"
            delta_bic_str = f"{delta_bic:.1f}"
            
            abs_bic = abs(delta_bic)
            if abs_bic < 2:
                evidence = "Bare mention"
            elif abs_bic < 6:
                evidence = "Positive"
            elif abs_bic < 10:
                evidence = "Strong"
            else:
                evidence = "Very strong"
        else:
            winner = "N/A"
            delta_chi2_str = "N/A"
            delta_bic_str = "N/A"
            evidence = "N/A"
        
        logger.info(f"{name:<15} {n:<8} {delta_chi2_str:<12} {delta_bic_str:<12} {winner:<15} {evidence}")
    
    # Key test: Does the effect disappear with full sample?
    logger.info("\n" + "=" * 70)
    logger.info("🔍 KEY TEST: Does the effect disappear with full sample?")
    
    if lcdm_full and nonaccel_full and lcdm_young and nonaccel_young:
        if bayes_full['comparison']['delta_bic'] < 0 and bayes_young['comparison']['delta_bic'] < 0:
            if abs(bayes_young['comparison']['delta_bic']) > abs(bayes_full['comparison']['delta_bic']):
                logger.info(f"   ✅ EFFECT STRONGER with young sample!")
                logger.info(f"   Young ΔBIC = {bayes_young['comparison']['delta_bic']:.1f} vs Full ΔBIC = {bayes_full['comparison']['delta_bic']:.1f}")
                logger.info(f"   This supports the Korean team's hypothesis!")
            else:
                logger.info(f"   ⚠️ Effect similar for young and full samples")
                logger.info(f"   Both prefer non-accelerating, but weakly")
        elif bayes_full['comparison']['delta_bic'] > 0 and bayes_young['comparison']['delta_bic'] < 0:
            logger.info(f"   ✅ EFFECT DISAPPEARS with full sample!")
            logger.info(f"   Full sample prefers ΛCDM, young prefers non-accelerating")
            logger.info(f"   This STRONGLY supports the Korean team's hypothesis!")
        else:
            logger.info(f"   ℹ️ Both samples prefer same model")
    
    logger.info("=" * 70)
    logger.info("✅ Comparison complete!")
    logger.info("🍩 'Full vs young = the ultimate test!'")
    
    return {
        'full': {
            'n': n_full, 
            'delta_chi2': delta_chi2_full if lcdm_full and nonaccel_full else None,
            'delta_bic': bayes_full['comparison']['delta_bic'] if lcdm_full and nonaccel_full else None,
        },
        'young': {
            'n': n_young, 
            'delta_chi2': delta_chi2_young if lcdm_young and nonaccel_young else None,
            'delta_bic': bayes_young['comparison']['delta_bic'] if lcdm_young and nonaccel_young else None,
        },
        'old': {
            'n': n_old, 
            'delta_chi2': delta_chi2_old if lcdm_old and nonaccel_old else None,
            'delta_bic': bayes_old['comparison']['delta_bic'] if lcdm_old and nonaccel_old else None,
        },
    }


if __name__ == "__main__":
    results = test_full_sample()
    
    # Save results
    df_results = pd.DataFrame([
        {
            'sample': 'full', 
            'n': results['full']['n'], 
            'delta_chi2': results['full']['delta_chi2'],
            'delta_bic': results['full']['delta_bic'],
        },
        {
            'sample': 'young', 
            'n': results['young']['n'], 
            'delta_chi2': results['young']['delta_chi2'],
            'delta_bic': results['young']['delta_bic'],
        },
        {
            'sample': 'old', 
            'n': results['old']['n'], 
            'delta_chi2': results['old']['delta_chi2'],
            'delta_bic': results['old']['delta_bic'],
        },
    ])
    df_results.to_csv('data/full_vs_young_results_bayesian.csv', index=False)
    logger.info("💾 Results saved to data/full_vs_young_results_bayesian.csv")

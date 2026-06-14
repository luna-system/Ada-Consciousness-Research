#!/usr/bin/env python3
"""
Validation: Test Different Color Cuts on ZTF DR2

Tests robustness of cosmology results to color threshold choices.

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: June 13, 2026
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
from fit_cosmology import fit_hubble_diagram, compare_models

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def apply_color_cuts(df, gz_threshold=1.0, mass_threshold=11.0):
    """Apply color cuts with given thresholds."""
    df = df.copy()
    has_host = df['restframe_gz'].notna() & df['mass'].notna()
    df['has_host'] = has_host
    
    blue = df['restframe_gz'] < gz_threshold
    low_mass = df['mass'] < mass_threshold
    young = has_host & blue & low_mass
    df['is_young'] = young
    
    return df


def select_coeval(df, tolerance=0.2):
    """Select coeval subset."""
    young = df[df['is_young']].copy()
    if len(young) == 0:
        return young
    gz_median = young['restframe_gz'].median()
    coeval = young[abs(young['restframe_gz'] - gz_median) < tolerance].copy()
    return coeval


def prepare_for_cosmology(df):
    """Prepare for cosmology fitting."""
    df['snid'] = df['ztfname']
    df['zHD'] = df['redshift']
    df['mB'] = -2.5 * np.log10(df['x0']) + 10.0
    return df


def test_color_cuts(data_dir='data/ztf_dr2/ztfsniadr2_lite/tables'):
    """Test multiple color cut combinations."""
    
    logger.info("🌌 Validation: Testing Different Color Cuts on ZTF DR2")
    logger.info("=" * 70)
    
    # Load data
    data_path = Path(data_dir)
    hosts = pd.read_csv(data_path / 'globalhost_data.csv')
    sne = pd.read_csv(data_path / 'snia_data.csv')
    df = sne.merge(hosts, on='ztfname', how='inner')
    
    logger.info(f"📊 Loaded {len(df)} ZTF SNe Ia")
    
    # Test different thresholds
    thresholds = [
        ('very_strict', 0.7, 10.5, 0.15),
        ('strict', 0.8, 10.8, 0.2),
        ('moderate', 1.0, 11.0, 0.2),
        ('relaxed', 1.2, 11.2, 0.25),
        ('very_relaxed', 1.5, 11.5, 0.3),
    ]
    
    results = []
    
    for name, gz_thresh, mass_thresh, coeval_tol in thresholds:
        logger.info(f"\n🎨 Testing {name}: g-z < {gz_thresh}, mass < {mass_thresh}, coeval_tol={coeval_tol}")
        
        # Apply cuts
        df_test = apply_color_cuts(df, gz_threshold=gz_thresh, mass_threshold=mass_thresh)
        coeval = select_coeval(df_test, tolerance=coeval_tol)
        
        n_young = df_test['is_young'].sum()
        n_coeval = len(coeval)
        
        logger.info(f"   Young: {n_young} | Coeval: {n_coeval}")
        
        if n_coeval < 10:
            logger.info(f"   ⚠️ Too few galaxies for cosmology fit")
            results.append({
                'name': name,
                'gz_threshold': gz_thresh,
                'mass_threshold': mass_thresh,
                'n_young': n_young,
                'n_coeval': n_coeval,
                'lcdm_chi2': None,
                'nonaccel_chi2': None,
                'delta_chi2': None,
                'lcdm_rms': None,
                'nonaccel_rms': None,
            })
            continue
        
        # Prepare for cosmology
        df_test = prepare_for_cosmology(df_test)
        df_test['evolution_free'] = df_test['is_young']
        
        # Fit models
        try:
            lcdm_results = fit_hubble_diagram(df_test, model='lcdm')
            nonaccel_results = fit_hubble_diagram(df_test, model='nonaccel')
            
            if lcdm_results and nonaccel_results:
                delta_chi2 = nonaccel_results['chi2'] - lcdm_results['chi2']
                
                logger.info(f"   ΛCDM: χ²={lcdm_results['chi2']:.1f}, RMS={lcdm_results['rms_residual']:.3f}")
                logger.info(f"   Non-Accel: χ²={nonaccel_results['chi2']:.1f}, RMS={nonaccel_results['rms_residual']:.3f}")
                logger.info(f"   Δχ²: {delta_chi2:.1f}")
                
                if delta_chi2 < 0:
                    logger.info(f"   ⭐ Non-accelerating wins!")
                else:
                    logger.info(f"   ⭐ ΛCDM wins!")
                
                results.append({
                    'name': name,
                    'gz_threshold': gz_thresh,
                    'mass_threshold': mass_thresh,
                    'n_young': n_young,
                    'n_coeval': n_coeval,
                    'lcdm_chi2': lcdm_results['chi2'],
                    'nonaccel_chi2': nonaccel_results['chi2'],
                    'delta_chi2': delta_chi2,
                    'lcdm_rms': lcdm_results['rms_residual'],
                    'nonaccel_rms': nonaccel_results['rms_residual'],
                })
            else:
                logger.info(f"   ⚠️ Fit failed")
                results.append({
                    'name': name,
                    'gz_threshold': gz_thresh,
                    'mass_threshold': mass_thresh,
                    'n_young': n_young,
                    'n_coeval': n_coeval,
                    'lcdm_chi2': None,
                    'nonaccel_chi2': None,
                    'delta_chi2': None,
                    'lcdm_rms': None,
                    'nonaccel_rms': None,
                })
        except Exception as e:
            logger.error(f"   ❌ Error: {e}")
            results.append({
                'name': name,
                'gz_threshold': gz_thresh,
                'mass_threshold': mass_thresh,
                'n_young': n_young,
                'n_coeval': n_coeval,
                'lcdm_chi2': None,
                'nonaccel_chi2': None,
                'delta_chi2': None,
                'lcdm_rms': None,
                'nonaccel_rms': None,
            })
    
    # Summary table
    logger.info("\n" + "=" * 70)
    logger.info("📊 SUMMARY: Color Cut Validation Results")
    logger.info("=" * 70)
    logger.info(f"{'Cut':<15} {'g-z':<6} {'Mass':<6} {'N_young':<9} {'N_coeval':<9} {'Δχ²':<12} {'Winner':<15}")
    logger.info("-" * 70)
    
    for r in results:
        if r['delta_chi2'] is not None:
            winner = "Non-Accel" if r['delta_chi2'] < 0 else "ΛCDM"
            delta_str = f"{r['delta_chi2']:.1f}"
        else:
            winner = "N/A"
            delta_str = "N/A"
        
        logger.info(f"{r['name']:<15} {r['gz_threshold']:<6.1f} {r['mass_threshold']:<6.1f} {r['n_young']:<9} {r['n_coeval']:<9} {delta_str:<12} {winner:<15}")
    
    # Robustness check
    logger.info("\n" + "=" * 70)
    logger.info("🔍 ROBUSTNESS CHECK:")
    
    valid_results = [r for r in results if r['delta_chi2'] is not None]
    if valid_results:
        nonaccel_wins = sum(1 for r in valid_results if r['delta_chi2'] < 0)
        total = len(valid_results)
        
        logger.info(f"   Non-accelerating wins: {nonaccel_wins}/{total} threshold combinations")
        logger.info(f"   ΛCDM wins: {total - nonaccel_wins}/{total} combinations")
        
        if nonaccel_wins == total:
            logger.info(f"   ✅ ROBUST: Non-accelerating model wins with ALL color cuts!")
        elif nonaccel_wins > total / 2:
            logger.info(f"   ✅ MOSTLY ROBUST: Non-accelerating wins in {100*nonaccel_wins/total:.0f}% of cuts")
        else:
            logger.info(f"   ⚠️ MIXED: Results depend on color cut choice")
    
    logger.info("=" * 70)
    logger.info("✅ Validation complete!")
    logger.info("🍩 'Robustness is the foundation of good science!'")
    
    return results


if __name__ == "__main__":
    results = test_color_cuts()
    
    # Save results
    df_results = pd.DataFrame(results)
    df_results.to_csv('data/colorcut_validation_results.csv', index=False)
    logger.info("💾 Results saved to data/colorcut_validation_results.csv")

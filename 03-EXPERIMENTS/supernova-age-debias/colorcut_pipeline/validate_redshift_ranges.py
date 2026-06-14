#!/usr/bin/env python3
"""
Validation: Test Different Redshift Ranges on ZTF DR2

Tests robustness of cosmology results to redshift selection.

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
    return df


def test_redshift_ranges(data_dir='data/ztf_dr2/ztfsniadr2_lite/tables'):
    """Test different redshift ranges."""
    
    logger.info("🌌 Validation: Testing Different Redshift Ranges on ZTF DR2")
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
    
    # Test different redshift ranges
    ranges = [
        ('very_low_z', 0.0, 0.05),
        ('low_z', 0.0, 0.1),
        ('mid_z', 0.05, 0.15),
        ('high_z', 0.1, 0.3),
        ('all_z', 0.0, 1.0),
    ]
    
    results = []
    
    for name, z_min, z_max in ranges:
        logger.info(f"\n🎨 Testing {name}: z = {z_min} - {z_max}")
        
        # Select redshift range
        in_range = (df['zHD'] >= z_min) & (df['zHD'] < z_max) & df['is_young']
        df_range = df[in_range].copy()
        
        n_galaxies = len(df_range)
        logger.info(f"   Galaxies in range: {n_galaxies}")
        
        if n_galaxies < 10:
            logger.info(f"   ⚠️ Too few galaxies for cosmology fit")
            results.append({
                'name': name,
                'z_min': z_min,
                'z_max': z_max,
                'n_galaxies': n_galaxies,
                'lcdm_chi2': None,
                'nonaccel_chi2': None,
                'delta_chi2': None,
                'lcdm_rms': None,
                'nonaccel_rms': None,
            })
            continue
        
        # Set evolution_free flag
        df_range['evolution_free'] = True
        
        # Fit models
        try:
            lcdm_results = fit_hubble_diagram(df_range, model='lcdm')
            nonaccel_results = fit_hubble_diagram(df_range, model='nonaccel')
            
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
                    'z_min': z_min,
                    'z_max': z_max,
                    'n_galaxies': n_galaxies,
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
                    'z_min': z_min,
                    'z_max': z_max,
                    'n_galaxies': n_galaxies,
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
                'z_min': z_min,
                'z_max': z_max,
                'n_galaxies': n_galaxies,
                'lcdm_chi2': None,
                'nonaccel_chi2': None,
                'delta_chi2': None,
                'lcdm_rms': None,
                'nonaccel_rms': None,
            })
    
    # Summary table
    logger.info("\n" + "=" * 70)
    logger.info("📊 SUMMARY: Redshift Range Validation Results")
    logger.info("=" * 70)
    logger.info(f"{'Range':<12} {'z_min':<7} {'z_max':<7} {'N':<8} {'Δχ²':<12} {'Winner':<15}")
    logger.info("-" * 70)
    
    for r in results:
        if r['delta_chi2'] is not None:
            winner = "Non-Accel" if r['delta_chi2'] < 0 else "ΛCDM"
            delta_str = f"{r['delta_chi2']:.1f}"
        else:
            winner = "N/A"
            delta_str = "N/A"
        
        logger.info(f"{r['name']:<12} {r['z_min']:<7.2f} {r['z_max']:<7.2f} {r['n_galaxies']:<8} {delta_str:<12} {winner:<15}")
    
    # Robustness check
    logger.info("\n" + "=" * 70)
    logger.info("🔍 ROBUSTNESS CHECK:")
    
    valid_results = [r for r in results if r['delta_chi2'] is not None]
    if valid_results:
        nonaccel_wins = sum(1 for r in valid_results if r['delta_chi2'] < 0)
        total = len(valid_results)
        
        logger.info(f"   Non-accelerating wins: {nonaccel_wins}/{total} redshift ranges")
        logger.info(f"   ΛCDM wins: {total - nonaccel_wins}/{total} ranges")
        
        if nonaccel_wins == total:
            logger.info(f"   ✅ ROBUST: Non-accelerating model wins in ALL redshift ranges!")
        elif nonaccel_wins > total / 2:
            logger.info(f"   ✅ MOSTLY ROBUST: Non-accelerating wins in {100*nonaccel_wins/total:.0f}% of ranges")
        else:
            logger.info(f"   ⚠️ MIXED: Results depend on redshift range")
    
    logger.info("=" * 70)
    logger.info("✅ Validation complete!")
    logger.info("🍩 'Redshift robustness = cosmological confidence!'")
    
    return results


if __name__ == "__main__":
    results = test_redshift_ranges()
    
    # Save results
    df_results = pd.DataFrame(results)
    df_results.to_csv('data/redshift_validation_results.csv', index=False)
    logger.info("💾 Results saved to data/redshift_validation_results.csv")

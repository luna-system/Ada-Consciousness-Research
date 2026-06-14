#!/usr/bin/env python3
"""
Process ZTF SN Ia DR2 for Color-Cut Cosmology

Uses restframe_gz color to select young hosts and test cosmology.

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


def load_ztf_dr2(data_dir='data/ztf_dr2/ztfsniadr2_lite/tables'):
    """Load and merge ZTF DR2 host + SN tables."""
    
    data_path = Path(data_dir)
    
    # Load host data
    logger.info("📊 Loading ZTF DR2 host data...")
    hosts = pd.read_csv(data_path / 'globalhost_data.csv')
    logger.info(f"   Hosts: {len(hosts)}")
    
    # Load SN data
    logger.info("📊 Loading ZTF DR2 SN data...")
    sne = pd.read_csv(data_path / 'snia_data.csv')
    logger.info(f"   SNe: {len(sne)}")
    
    # Merge on ztfname
    merged = sne.merge(hosts, on='ztfname', how='inner')
    logger.info(f"   Merged: {len(merged)}")
    
    return merged


def apply_color_cuts(df, gz_threshold=1.0, mass_threshold=11.0):
    """
    Apply color cuts to select young galaxies.
    
    Uses restframe_gz (host color) and mass:
    - g-z < 1.0: blue/young galaxies
    - mass < 11.0: lower mass = younger (spirals/irregulars)
    """
    
    df = df.copy()
    
    # Check for valid host data
    has_host = df['restframe_gz'].notna() & df['mass'].notna()
    df['has_host'] = has_host
    
    # Color cut: blue galaxies
    blue = df['restframe_gz'] < gz_threshold
    
    # Mass cut: lower mass = younger
    low_mass = df['mass'] < mass_threshold
    
    # Combined: young = blue AND low mass
    young = has_host & blue & low_mass
    df['is_young'] = young
    
    # Color classification
    df['color_type'] = 'unknown'
    df.loc[has_host & (df['restframe_gz'] < 0.7), 'color_type'] = 'very_blue'
    df.loc[has_host & (df['restframe_gz'] >= 0.7) & (df['restframe_gz'] < 1.0), 'color_type'] = 'blue'
    df.loc[has_host & (df['restframe_gz'] >= 1.0) & (df['restframe_gz'] < 1.3), 'color_type'] = 'green'
    df.loc[has_host & (df['restframe_gz'] >= 1.3), 'color_type'] = 'red'
    
    return df


def select_coeval(df):
    """Select coeval subset from young galaxies."""
    
    young = df[df['is_young']].copy()
    
    if len(young) == 0:
        return young
    
    # Use tight color range around median
    gz_median = young['restframe_gz'].median()
    coeval = young[abs(young['restframe_gz'] - gz_median) < 0.2].copy()
    
    return coeval


def prepare_for_cosmology(df):
    """Prepare merged dataframe for cosmology fitting."""
    
    # Create required columns for fit_cosmology.py
    df['snid'] = df['ztfname']
    df['zHD'] = df['redshift']
    df['mB'] = df['c']  # Using c (color) as proxy, need actual mB
    
    # Calculate mB from x0 if available
    # mB = -2.5 * log10(x0) + 10 (SNANA convention)
    df['mB'] = -2.5 * np.log10(df['x0']) + 10.0
    
    return df


def main():
    """Main ZTF DR2 processing pipeline."""
    logger.info("🌌 Processing ZTF SN Ia DR2 for Cosmology")
    logger.info("=" * 60)
    
    # Load data
    df = load_ztf_dr2()
    
    if df is None or len(df) == 0:
        logger.error("❌ No ZTF DR2 data loaded!")
        return 1
    
    # Apply color cuts
    logger.info("🎨 Applying color cuts...")
    df = apply_color_cuts(df)
    
    # Summary
    n_with_host = df['has_host'].sum()
    n_young = df['is_young'].sum()
    
    logger.info(f"\n📊 Results:")
    logger.info(f"   Total: {len(df)}")
    logger.info(f"   With host data: {n_with_host}")
    logger.info(f"   Young (blue + low mass): {n_young} ({100*n_young/n_with_host:.1f}%)")
    
    # Color distribution
    color_counts = df['color_type'].value_counts()
    logger.info(f"\n📈 Host Color Distribution:")
    for color, count in color_counts.items():
        if color != 'unknown':
            logger.info(f"   {color}: {count}")
    
    # Select coeval
    coeval = select_coeval(df)
    logger.info(f"\n🎯 Coeval subset: {len(coeval)} galaxies")
    
    if len(coeval) > 0:
        logger.info(f"   g-z range: {coeval['restframe_gz'].min():.2f} - {coeval['restframe_gz'].max():.2f}")
        logger.info(f"   mass range: {coeval['mass'].min():.2f} - {coeval['mass'].max():.2f}")
        logger.info(f"   redshift range: {coeval['redshift'].min():.3f} - {coeval['redshift'].max():.3f}")
        
        # Save
        coeval.to_csv('data/ztf_dr2_coeval.csv', index=False)
        logger.info(f"💾 Saved coeval sample to data/ztf_dr2_coeval.csv")
    
    # Save full catalog
    df.to_csv('data/ztf_dr2_with_colors.csv', index=False)
    
    # Prepare for cosmology
    df = prepare_for_cosmology(df)
    
    # Fit cosmology if we have enough galaxies
    if len(coeval) >= 10:
        logger.info("\n🔬 Fitting cosmology models...")
        
        # Create evolution_free flag
        df['evolution_free'] = df['is_young']
        
        lcdm_results = fit_hubble_diagram(df, model='lcdm')
        nonaccel_results = fit_hubble_diagram(df, model='nonaccel')
        
        if lcdm_results and nonaccel_results:
            comparison = compare_models(lcdm_results, nonaccel_results)
    else:
        logger.warning(f"⚠️ Only {len(coeval)} coeval galaxies — need 10+ for cosmology fit")
    
    logger.info("=" * 60)
    logger.info("✅ ZTF DR2 processing complete!")
    logger.info("🍩 'ZTF data = cosmology gold!'")
    
    return 0


if __name__ == "__main__":
    exit(main())

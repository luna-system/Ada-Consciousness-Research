"""
Analyze Young Host Sample for Cosmology

Checks coevality and prepares evolution-free sample for Hubble diagram.

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: June 13, 2026
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def analyze_young_sample():
    """Analyze the young host sample for coevality."""
    
    logger.info("🌌 Analyzing Young Host Sample")
    logger.info("=" * 60)
    
    # Load young hosts
    young = pd.read_csv('data/young_hosts_color.csv')
    logger.info(f"📊 Loaded {len(young)} young hosts")
    
    # Check color distribution (proxy for coevality)
    logger.info(f"\n📈 Color Properties:")
    logger.info(f"   g-r range: {young['g_r'].min():.2f} - {young['g_r'].max():.2f}")
    logger.info(f"   g-r mean: {young['g_r'].mean():.2f}")
    logger.info(f"   g-r std: {young['g_r'].std():.2f}")
    
    if 'u_g' in young.columns:
        logger.info(f"   u-g range: {young['u_g'].min():.2f} - {young['u_g'].max():.2f}")
        logger.info(f"   u-g mean: {young['u_g'].mean():.2f}")
        logger.info(f"   u-g std: {young['u_g'].std():.2f}")
    
    # Redshift distribution
    logger.info(f"\n📈 Redshift Distribution:")
    logger.info(f"   z range: {young['zHD'].min():.3f} - {young['zHD'].max():.3f}")
    logger.info(f"   z mean: {young['zHD'].mean():.3f}")
    logger.info(f"   z median: {young['zHD'].median():.3f}")
    
    # Coevality score: how uniform are the colors?
    # Low std = more coeval
    g_r_std = young['g_r'].std()
    coevality_threshold = 0.2  # g-r std < 0.2 means similar colors
    
    if g_r_std < coevality_threshold:
        logger.info(f"\n✅ Coevality check PASSED!")
        logger.info(f"   g-r std = {g_r_std:.3f} < {coevality_threshold}")
        logger.info(f"   These galaxies have similar stellar populations!")
    else:
        logger.info(f"\n⚠️ Coevality check: g-r std = {g_r_std:.3f}")
        logger.info(f"   Some variation in stellar populations expected")
    
    # Select most coeval subset (tightest color range)
    g_r_median = young['g_r'].median()
    coeval = young[abs(young['g_r'] - g_r_median) < 0.2].copy()
    
    logger.info(f"\n🎯 Most Coeval Subset (|g-r - median| < 0.2):")
    logger.info(f"   {len(coeval)} galaxies")
    logger.info(f"   g-r range: {coeval['g_r'].min():.2f} - {coeval['g_r'].max():.2f}")
    
    # Save coeval sample
    if len(coeval) > 0:
        coeval.to_csv('data/coeval_young_hosts.csv', index=False)
        logger.info(f"💾 Saved coeval sample")
    
    # Also save full relaxed sample with flags
    young['is_coeval'] = abs(young['g_r'] - g_r_median) < 0.2
    young.to_csv('data/young_hosts_with_coevality.csv', index=False)
    
    logger.info("=" * 60)
    logger.info("✅ Analysis complete!")
    logger.info("🍩 'Young and coeval — the perfect cosmology sample!'")
    
    return len(coeval)


if __name__ == "__main__":
    exit(analyze_young_sample())

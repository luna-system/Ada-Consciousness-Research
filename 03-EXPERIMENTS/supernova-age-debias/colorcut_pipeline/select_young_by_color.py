"""
Select Young Supernova Hosts Using Color Cuts

Uses simple photometric color cuts to identify potentially young,
star-forming galaxies in the Pantheon+ sample.

Young galaxies are typically:
- Blue (g-r < 0.6)
- Have strong UV emission (u-g < 1.0)
- Are star-forming (not passive/evolved)

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: June 13, 2026
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def select_young_by_color(hosts, 
                          g_r_threshold=0.6,      # Blue galaxies
                          u_g_threshold=1.0,      # UV-bright galaxies
                          r_threshold=20.0,       # Not too faint
                          require_all_bands=True):
    """
    Select young galaxies using color cuts.
    
    Young/star-forming galaxies typically have:
    - g-r < 0.6 (blue)
    - u-g < 1.0 (UV-bright, indicating young stars)
    - r < 20 (detectable, not too faint)
    """
    
    # Calculate colors
    hosts = hosts.copy()
    
    # Check which bands are available
    has_photometry = (
        hosts['dered_g'].notna() & 
        hosts['dered_r'].notna()
    )
    
    if require_all_bands:
        has_photometry &= hosts['dered_u'].notna()
    
    hosts['has_photometry'] = has_photometry
    
    # Calculate colors for galaxies with photometry
    hosts.loc[has_photometry, 'g_r'] = (
        hosts.loc[has_photometry, 'dered_g'] - 
        hosts.loc[has_photometry, 'dered_r']
    )
    
    if 'dered_u' in hosts.columns:
        hosts.loc[has_photometry, 'u_g'] = (
            hosts.loc[has_photometry, 'dered_u'] - 
            hosts.loc[has_photometry, 'dered_g']
        )
    
    # Apply color cuts
    young = pd.Series(False, index=hosts.index)
    
    # g-r cut (blue galaxies)
    blue_galaxies = hosts['g_r'] < g_r_threshold
    
    # u-g cut (UV-bright, young stars)
    if 'u_g' in hosts.columns:
        uv_bright = hosts['u_g'] < u_g_threshold
    else:
        uv_bright = pd.Series(True, index=hosts.index)
    
    # Brightness cut
    bright = hosts['dered_r'] < r_threshold
    
    # Combine cuts
    young = has_photometry & blue_galaxies & uv_bright & bright
    
    hosts['is_young_color'] = young
    
    # Also classify by color type
    hosts['color_type'] = 'unknown'
    hosts.loc[has_photometry & (hosts['g_r'] < 0.4), 'color_type'] = 'very_blue'
    hosts.loc[has_photometry & (hosts['g_r'] >= 0.4) & (hosts['g_r'] < 0.6), 'color_type'] = 'blue'
    hosts.loc[has_photometry & (hosts['g_r'] >= 0.6) & (hosts['g_r'] < 0.8), 'color_type'] = 'green'
    hosts.loc[has_photometry & (hosts['g_r'] >= 0.8), 'color_type'] = 'red'
    
    return hosts


def main():
    """Main color selection pipeline with multiple thresholds."""
    logger.info("🌌 Selecting Young Supernova Hosts by Color")
    logger.info("=" * 60)
    
    # Load Pantheon+ hosts with photometry
    hosts_file = 'data/pantheon_hosts_with_photometry.csv'
    
    if not Path(hosts_file).exists():
        logger.error(f"❌ File not found: {hosts_file}")
        return 1
    
    hosts = pd.read_csv(hosts_file)
    logger.info(f"📊 Loaded {len(hosts)} Pantheon+ hosts")
    
    # Try multiple threshold combinations
    thresholds = [
        ('strict', 0.6, 1.0, 20.0),
        ('moderate', 0.7, 1.2, 21.0),
        ('relaxed', 0.8, 1.5, 22.0),
        ('very_relaxed', 1.0, 2.0, 23.0),
    ]
    
    results = {}
    
    for name, g_r, u_g, r_mag in thresholds:
        logger.info(f"\n🎨 Testing {name} cuts: g-r < {g_r}, u-g < {u_g}, r < {r_mag}")
        selected = select_young_by_color(hosts, g_r_threshold=g_r, u_g_threshold=u_g, r_threshold=r_mag)
        n_young = selected['is_young_color'].sum()
        results[name] = n_young
        logger.info(f"   Found {n_young} young hosts")
    
    # Use relaxed cuts for final selection
    logger.info(f"\n📊 Final Selection (relaxed cuts):")
    hosts = select_young_by_color(hosts, g_r_threshold=0.8, u_g_threshold=1.5, r_threshold=22.0)
    
    n_with_photo = hosts['has_photometry'].sum()
    n_young = hosts['is_young_color'].sum()
    
    logger.info(f"   Total hosts: {len(hosts)}")
    logger.info(f"   With photometry: {n_with_photo}")
    logger.info(f"   Young (blue + UV-bright): {n_young} ({100*n_young/n_with_photo:.1f}%)")
    
    # Color distribution
    color_counts = hosts['color_type'].value_counts()
    logger.info(f"\n📈 Color Distribution:")
    for color, count in color_counts.items():
        if color != 'unknown':
            logger.info(f"   {color}: {count}")
    
    # Save young sample
    young_hosts = hosts[hosts['is_young_color']].copy()
    if len(young_hosts) > 0:
        young_hosts.to_csv('data/young_hosts_color.csv', index=False)
        logger.info(f"\n💾 Saved {len(young_hosts)} young hosts to data/young_hosts_color.csv")
        
        # Show examples
        logger.info(f"\n🌟 Example Young Hosts:")
        for _, row in young_hosts.head(10).iterrows():
            logger.info(f"   {row['snid']}: z={row['zHD']:.3f}, g-r={row['g_r']:.2f}, u-g={row.get('u_g', np.nan):.2f}")
    
    # Save full catalog
    hosts.to_csv('data/pantheon_hosts_with_colors.csv', index=False)
    
    # Summary of all thresholds
    logger.info(f"\n📊 Summary of All Thresholds:")
    for name, count in results.items():
        logger.info(f"   {name}: {count} young hosts")
    
    logger.info("=" * 60)
    logger.info("✅ Color selection complete!")
    logger.info("🍩 'Blue galaxies are young galaxies!'")
    
    return 0


if __name__ == "__main__":
    exit(main())

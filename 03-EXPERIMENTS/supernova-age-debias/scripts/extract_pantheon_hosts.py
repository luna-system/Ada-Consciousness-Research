"""
Extract Pantheon+ Host Galaxy Catalog

Parses the Pantheon+ data release to extract host galaxy information
for cross-matching with SDSS spectroscopic ages.

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: June 13, 2026
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_pantheon_hosts(
    input_file: str = "data/pantheon-plus/Pantheon+_Data/1_DATA/all_redshifts_PVs.csv",
    output_file: str = "data/pantheon_hosts.csv",
) -> pd.DataFrame:
    """
    Extract host galaxy catalog from Pantheon+ data release.
    
    Args:
        input_file: Path to Pantheon+ redshift CSV
        output_file: Path to save extracted host catalog
        
    Returns:
        DataFrame with host galaxy information
    """
    logger.info("🌌 Extracting Pantheon+ host galaxies...")
    
    # Load Pantheon+ data
    df = pd.read_csv(input_file)
    
    logger.info(f"   Loaded {len(df)} supernovae")
    
    # Filter to SNe with host galaxies
    has_host = df['has_host'] == 1
    df_hosts = df[has_host].copy()
    
    logger.info(f"   {len(df_hosts)} SNe have host galaxies")
    
    # Extract relevant columns
    host_catalog = pd.DataFrame({
        'snid': df_hosts['SNID'],
        'iauc': df_hosts['IAUC'],
        'host_name': df_hosts['host'],
        'sn_ra': df_hosts['RA'],
        'sn_dec': df_hosts['Dec'],
        'host_ra': df_hosts['RA_host'],
        'host_dec': df_hosts['Dec_host'],
        'zhel': df_hosts['zhel'],
        'zcmb': df_hosts['zcmb'],
        'zHD': df_hosts['zHD'],
        'zhelerr': df_hosts['zhelerr'],
        'zHDerr': df_hosts['zHDerr'],
        'pv': df_hosts['PV'],
        'vpecerr': df_hosts['vpecerr'],
        'in_group': df_hosts['in_group'],
        'is_SNz': df_hosts['is_SNz'],
    })
    
    # Remove hosts with missing coordinates
    valid_coords = (
        host_catalog['host_ra'].notna() & 
        host_catalog['host_dec'].notna()
    )
    host_catalog = host_catalog[valid_coords]
    
    logger.info(f"   {len(host_catalog)} hosts with valid coordinates")
    
    # Save catalog
    host_catalog.to_csv(output_file, index=False)
    logger.info(f"💾 Saved to {output_file}")
    
    # Print summary
    logger.info(f"\n📊 Host Catalog Summary:")
    logger.info(f"   Total hosts: {len(host_catalog)}")
    logger.info(f"   Redshift range: {host_catalog['zHD'].min():.4f} - {host_catalog['zHD'].max():.4f}")
    logger.info(f"   Mean redshift: {host_catalog['zHD'].mean():.4f}")
    logger.info(f"   In groups: {host_catalog['in_group'].sum()}")
    
    return host_catalog


def main():
    """Main extraction pipeline."""
    logger.info("🌌 Pantheon+ Host Galaxy Extraction")
    logger.info("=" * 60)
    
    # Create output directory
    Path("data").mkdir(exist_ok=True)
    
    # Extract hosts
    catalog = extract_pantheon_hosts()
    
    logger.info("=" * 60)
    logger.info("✅ Extraction complete!")
    logger.info("🍩 'Ready for SDSS cross-matching!'")
    
    return 0


if __name__ == "__main__":
    exit(main())

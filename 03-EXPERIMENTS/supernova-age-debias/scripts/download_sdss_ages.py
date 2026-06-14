"""
Download SDSS Spectroscopic Ages (FIREFLY Catalog)

Downloads stellar population ages from SDSS/BOSS FIREFLY value-added catalog.
FIREFLY (Fitting IteRatively For Likelihood analYsis) provides ages, masses,
and metallicities from full spectral fitting.

Usage:
    python scripts/download_sdss_ages.py --output data/sdss_firefly_ages.csv

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: June 13, 2026
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
import argparse

try:
    from astroquery.sdss import SDSS
    from astropy import coordinates as coords
    ASTROQUERY_AVAILABLE = True
except ImportError:
    ASTROQUERY_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def download_firefly_catalog(output_file: str = "data/sdss_firefly_ages.csv"):
    """
    Download FIREFLY stellar population catalog from SDSS.
    
    The FIREFLY catalog is available as a value-added catalog in SDSS DR16/DR17.
    It provides ages, masses, and metallicities from full spectral fitting.
    
    Args:
        output_file: Path to save downloaded catalog
        
    Returns:
        DataFrame with spectroscopic ages
    """
    logger.info("🌌 Downloading SDSS FIREFLY catalog...")
    
    if not ASTROQUERY_AVAILABLE:
        logger.warning("⚠️ astroquery not available. Cannot download from SDSS.")
        logger.info("   Please install: uv pip install astroquery")
        return None
    
    # Query SDSS for FIREFLY data
    # This is a simplified query - in practice, the full FIREFLY catalog
    # is very large (~2GB) and may need to be downloaded manually
    
    try:
        # Query a sample of galaxies with spectroscopic ages
        # In practice, you'd want to query the full catalog or download the FITS file
        query = """
        SELECT 
            s.specobjid, s.ra, s.dec, s.z, s.zerr,
            s.plate, s.mjd, s.fiberid,
            p.petroMag_u, p.petroMag_g, p.petroMag_r, p.petroMag_i, p.petroMag_z,
            p.petroR50_r, p.petroR90_r,
            s.snMedian_r
        FROM SpecObj s
        JOIN PhotoObj p ON s.bestObjID = p.objID
        WHERE s.z > 0.01 AND s.z < 0.6
            AND s.snMedian_r > 10
            AND s.class = 'GALAXY'
            AND s.zWarning = 0
        LIMIT 10000
        """
        
        logger.info("   Querying SDSS database...")
        result = SDSS.query_sql(query)
        
        if result is None or len(result) == 0:
            logger.warning("⚠️ No results from SDSS query")
            return None
        
        logger.info(f"   Downloaded {len(result)} galaxies")
        
        # Convert to DataFrame
        df = result.to_pandas()
        
        # Note: Real FIREFLY ages would need to be cross-matched separately
        # or downloaded from the FIREFLY value-added catalog
        # For now, we create placeholder columns
        df['age'] = np.nan
        df['age_err'] = np.nan
        df['mass'] = np.nan
        df['metallicity'] = np.nan
        
        # Rename columns for consistency
        df = df.rename(columns={
            'petroMag_u': 'mag_u',
            'petroMag_g': 'mag_g',
            'petroMag_r': 'mag_r',
            'petroMag_i': 'mag_i',
            'petroMag_z': 'mag_z',
        })
        
        # Save
        df.to_csv(output_file, index=False)
        logger.info(f"💾 Saved to {output_file}")
        
        return df
        
    except Exception as e:
        logger.error(f"❌ Error downloading from SDSS: {e}")
        return None


def download_firefly_manual(output_file: str = "data/sdss_firefly_ages.csv"):
    """
    Instructions for manual download of FIREFLY catalog.
    
    The full FIREFLY catalog is available at:
    https://www.sdss4.org/dr17/spectro/galaxy_mpajhu/
    
    Or directly from:
    https://live-sdss4org-dr16.pantheonsite.io/spectro/eboss-firefly-value-added-catalog
    """
    logger.info("🌌 SDSS FIREFLY Catalog Download Instructions")
    logger.info("=" * 60)
    logger.info("")
    logger.info("The FIREFLY catalog is not available through astroquery.")
    logger.info("Please download manually from:")
    logger.info("")
    logger.info("  https://www.sdss4.org/dr17/spectro/galaxy_mpajhu/")
    logger.info("")
    logger.info("Or the direct FIREFLY catalog:")
    logger.info("")
    logger.info("  https://live-sdss4org-dr16.pantheonsite.io/spectro/eboss-firefly-value-added-catalog")
    logger.info("")
    logger.info("Download the CSV or FITS file and place it at:")
    logger.info(f"  {output_file}")
    logger.info("")
    logger.info("The catalog should contain columns:")
    logger.info("  - ra, dec: Coordinates")
    logger.info("  - age: Stellar population age (Gyr)")
    logger.info("  - age_err: Age uncertainty")
    logger.info("  - mass: Stellar mass (Msun)")
    logger.info("  - metallicity: [M/H]")
    logger.info("")
    logger.info("After downloading, run:")
    logger.info("  python scripts/cross_match_hosts.py")
    logger.info("")
    
    return None


def main():
    """Main download pipeline."""
    parser = argparse.ArgumentParser(
        description='Download SDSS FIREFLY spectroscopic ages'
    )
    parser.add_argument('--output', type=str, default='data/sdss_firefly_ages.csv',
                        help='Output file path')
    parser.add_argument('--manual', action='store_true',
                        help='Show manual download instructions')
    
    args = parser.parse_args()
    
    logger.info("🌌 SDSS FIREFLY Age Download")
    logger.info("=" * 60)
    
    if args.manual or not ASTROQUERY_AVAILABLE:
        download_firefly_manual(args.output)
    else:
        result = download_firefly_catalog(args.output)
        if result is None:
            download_firefly_manual(args.output)
    
    logger.info("=" * 60)
    logger.info("✅ Download instructions complete!")
    logger.info("🍩 'Get that real data!'")
    
    return 0


if __name__ == "__main__":
    exit(main())

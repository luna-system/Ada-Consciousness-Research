"""
Query SDSS Photometry for ALL Pantheon+ Hosts (with retries)

Downloads ugriz photometry from SDSS for all ~1,361 Pantheon+ hosts
using coordinate-based queries with retry logic for 503 errors.

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: June 13, 2026
"""

import pandas as pd
import numpy as np
from astroquery.sdss import SDSS
from astropy import coordinates as coords
import astropy.units as u
from pathlib import Path
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def query_with_retry(pos, radius=3*u.arcsec, max_retries=3, base_delay=2):
    """Query SDSS with exponential backoff for 503 errors."""
    for attempt in range(max_retries):
        try:
            result = SDSS.query_crossid(pos, radius=radius)
            return result
        except Exception as e:
            if "503" in str(e) or "Service Unavailable" in str(e):
                delay = base_delay * (2 ** attempt)
                logger.warning(f"   503 error, retrying in {delay}s... (attempt {attempt + 1}/{max_retries})")
                time.sleep(delay)
            else:
                raise
    return None


def query_sdss_photometry_by_coords(
    hosts_file: str = "data/pantheon_hosts.csv",
    output_file: str = "data/pantheon_hosts_with_photometry.csv",
):
    """
    Query SDSS for photometry (ugriz) for ALL Pantheon+ hosts by coordinates.
    """
    logger.info("🌌 Querying SDSS photometry for ALL Pantheon+ hosts...")
    
    # Load Pantheon+ hosts
    hosts = pd.read_csv(hosts_file)
    logger.info(f"   Total hosts to query: {len(hosts)}")
    
    photometry_records = []
    failed_hosts = []
    
    # Query individually with longer delays
    total = len(hosts)
    for i, (idx, row) in enumerate(hosts.iterrows()):
        if (i + 1) % 50 == 0:
            logger.info(f"   Queried {i + 1}/{total} hosts...")
        
        try:
            pos = coords.SkyCoord(row['host_ra']*u.deg, row['host_dec']*u.deg, frame='icrs')
            
            result = query_with_retry(pos, radius=3*u.arcsec, max_retries=3, base_delay=2)
            
            if result is not None and len(result) > 0:
                result_df = result.to_pandas()
                result_df['snid'] = row['snid']
                result_df['host_ra'] = row['host_ra']
                result_df['host_dec'] = row['host_dec']
                result_df['zHD'] = row['zHD']
                photometry_records.append(result_df)
            
        except Exception as e:
            logger.warning(f"   Error querying {row['snid']}: {e}")
            failed_hosts.append(row['snid'])
        
        # Longer delay to avoid 503 errors
        time.sleep(0.5)
    
    if len(photometry_records) == 0:
        logger.warning("⚠️ No photometry found!")
        return None
    
    # Combine all photometry
    photometry_df = pd.concat(photometry_records, ignore_index=True)
    logger.info(f"   Total photometry matches: {len(photometry_df)}")
    logger.info(f"   Failed hosts: {len(failed_hosts)}")
    
    # Merge with Pantheon+ hosts - for each host, keep closest match
    merged = hosts.copy()
    
    # Add photometry columns
    photo_cols = ['objID', 'ra', 'dec', 'dered_u', 'dered_g', 'dered_r', 'dered_i', 'dered_z',
                  'petroR50_r', 'petroR90_r', 'expAB_r']
    for col in photo_cols:
        merged[col] = np.nan
    merged['separation_arcsec'] = np.nan
    
    # For each host, find best match
    for snid in hosts['snid'].unique():
        host_photos = photometry_df[photometry_df['snid'] == snid]
        
        if len(host_photos) > 0:
            # Find closest match
            host_row = hosts[hosts['snid'] == snid].iloc[0]
            
            distances = np.sqrt(
                (host_photos['ra'] - host_row['host_ra'])**2 +
                (host_photos['dec'] - host_row['host_dec'])**2
            ) * 3600  # Convert to arcsec
            
            closest_idx = distances.idxmin()
            closest = host_photos.loc[closest_idx]
            
            # Update merged catalog
            host_idx = merged[merged['snid'] == snid].index[0]
            
            for col in photo_cols:
                if col in closest:
                    merged.loc[host_idx, col] = closest[col]
            
            merged.loc[host_idx, 'separation_arcsec'] = distances.min()
    
    # Save
    merged.to_csv(output_file, index=False)
    logger.info(f"💾 Saved to {output_file}")
    
    # Summary
    has_photometry = merged['dered_r'].notna()
    logger.info(f"\n📊 Photometry Summary:")
    logger.info(f"   Total hosts: {len(merged)}")
    logger.info(f"   With photometry: {has_photometry.sum()} ({100*has_photometry.sum()/len(merged):.1f}%)")
    logger.info(f"   Without photometry: {(~has_photometry).sum()}")
    
    if has_photometry.sum() > 0:
        logger.info(f"   r-band range: {merged.loc[has_photometry, 'dered_r'].min():.2f} - {merged.loc[has_photometry, 'dered_r'].max():.2f}")
        logger.info(f"   Mean separation: {merged.loc[has_photometry, 'separation_arcsec'].mean():.2f} arcsec")
    
    return merged


def main():
    """Main photometry download pipeline."""
    logger.info("🌌 Full Pantheon+ SDSS Photometry Query")
    logger.info("=" * 60)
    
    Path("data").mkdir(exist_ok=True)
    
    result = query_sdss_photometry_by_coords()
    
    if result is not None:
        logger.info("=" * 60)
        logger.info("✅ Full photometry query complete!")
        logger.info("🍩 'All the photometry for all the cosmology!'")
    else:
        logger.info("=" * 60)
        logger.info("⚠️ Photometry query incomplete")
    
    return 0


if __name__ == "__main__":
    exit(main())

"""
Query SDSS Photometry for Pantheon+ Hosts (Part 2)

Uses the objIDs from crossid queries to get full photometry.

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: June 13, 2026
"""

import pandas as pd
import numpy as np
from astroquery.sdss import SDSS
from pathlib import Path
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def query_photometry_by_objid(objid, max_retries=3, base_delay=1):
    """Query photometry for a specific SDSS objID."""
    for attempt in range(max_retries):
        try:
            query = f"""
            SELECT 
                p.objid, p.ra, p.dec,
                p.dered_u, p.dered_g, p.dered_r, p.dered_i, p.dered_z,
                p.petroR50_r, p.petroR90_r, p.expAB_r
            FROM PhotoObj p
            WHERE p.objid = {objid}
            """
            
            result = SDSS.query_sql(query)
            return result
            
        except Exception as e:
            if "503" in str(e) or "Service Unavailable" in str(e):
                delay = base_delay * (2 ** attempt)
                logger.warning(f"   503 error, retrying in {delay}s...")
                time.sleep(delay)
            else:
                logger.warning(f"   Error querying objid {objid}: {e}")
                return None
    
    return None


def get_photometry_for_hosts(hosts_file, output_file):
    """Get photometry for all hosts with objIDs."""
    
    logger.info("🌌 Querying photometry for Pantheon+ hosts...")
    
    # Load hosts with objIDs
    hosts = pd.read_csv(hosts_file)
    
    # Filter to hosts with objIDs
    has_objid = hosts['objID'].notna()
    hosts_with_objid = hosts[has_objid].copy()
    
    logger.info(f"   Total hosts: {len(hosts)}")
    logger.info(f"   With objID: {len(hosts_with_objid)}")
    
    # Query photometry for each
    photometry_records = []
    
    for i, (idx, row) in enumerate(hosts_with_objid.iterrows()):
        if (i + 1) % 50 == 0:
            logger.info(f"   Queried {i + 1}/{len(hosts_with_objid)}...")
        
        objid = int(row['objID'])
        result = query_photometry_by_objid(objid)
        
        if result is not None and len(result) > 0:
            result_df = result.to_pandas()
            result_df['snid'] = row['snid']
            photometry_records.append(result_df)
        
        time.sleep(0.2)  # Be nice to SDSS
    
    if len(photometry_records) == 0:
        logger.warning("⚠️ No photometry found!")
        return None
    
    # Combine photometry
    photo_df = pd.concat(photometry_records, ignore_index=True)
    logger.info(f"   Found photometry for {len(photo_df)} hosts")
    
    # Merge with hosts
    merged = hosts.copy()
    
    # Update photometry columns
    photo_cols = ['dered_u', 'dered_g', 'dered_r', 'dered_i', 'dered_z',
                  'petroR50_r', 'petroR90_r', 'expAB_r']
    
    for col in photo_cols:
        merged[col] = np.nan
    
    # Merge on snid
    for snid in photo_df['snid'].unique():
        photo_row = photo_df[photo_df['snid'] == snid]
        if len(photo_row) > 0:
            host_idx = merged[merged['snid'] == snid].index
            if len(host_idx) > 0:
                for col in photo_cols:
                    if col in photo_row.columns:
                        merged.loc[host_idx[0], col] = photo_row[col].values[0]
    
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
    
    return merged


def main():
    """Main photometry query pipeline."""
    logger.info("🌌 Pantheon+ Photometry Query (Part 2)")
    logger.info("=" * 60)
    
    result = get_photometry_for_hosts(
        'data/pantheon_hosts_with_photometry.csv',
        'data/pantheon_hosts_with_photometry.csv'
    )
    
    if result is not None:
        logger.info("=" * 60)
        logger.info("✅ Photometry query complete!")
        logger.info("🍩 'Photometry acquired!'")
    else:
        logger.info("=" * 60)
        logger.info("⚠️ Photometry query incomplete")
    
    return 0


if __name__ == "__main__":
    exit(main())

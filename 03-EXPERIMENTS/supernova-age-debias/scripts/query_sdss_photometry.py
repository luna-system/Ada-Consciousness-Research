"""
Query SDSS Photometry for Matched Pantheon+ Hosts

Downloads ugriz photometry from SDSS for the 169 cross-matched galaxies
to use as input features for AstroLANNAformer training.

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


def query_sdss_photometry(
    matched_catalog_file: str = "data/matched_catalog_real.csv",
    output_file: str = "data/matched_catalog_with_photometry.csv",
):
    """
    Query SDSS for photometry (ugriz) for matched Pantheon+ hosts.
    
    Uses the SDSS specobjid from the spectroscopic query to get photometry.
    """
    logger.info("🌌 Querying SDSS photometry for matched hosts...")
    
    # Load matched catalog
    matched = pd.read_csv(matched_catalog_file)
    logger.info(f"   Loaded {len(matched)} matched hosts")
    
    # Query photometry for each unique SDSS specobjid
    unique_specobjids = matched['sdss_specobjid'].unique()
    logger.info(f"   {len(unique_specobjids)} unique SDSS spectra to query")
    
    photometry_records = []
    
    for i, specobjid in enumerate(unique_specobjids):
        if (i + 1) % 50 == 0:
            logger.info(f"   Queried {i + 1}/{len(unique_specobjids)} spectra...")
        
        try:
            # Query SDSS for photometry using specobjid
            # Join SpecObj with PhotoObj to get photometry
            query = f"""
            SELECT 
                s.specobjid, s.bestobjid, s.ra, s.dec, s.z,
                p.dered_u, p.dered_g, p.dered_r, p.dered_i, p.dered_z,
                p.petroR50_r, p.petroR90_r,
                p.expAB_r
            FROM SpecObj s
            JOIN PhotoObj p ON s.bestobjid = p.objid
            WHERE s.specobjid = {specobjid}
            """
            
            result = SDSS.query_sql(query)
            
            if result is not None and len(result) > 0:
                result_df = result.to_pandas()
                result_df['query_specobjid'] = specobjid
                photometry_records.append(result_df)
            
        except Exception as e:
            logger.warning(f"   Error querying specobjid {specobjid}: {e}")
            continue
        
        # Be nice to SDSS servers
        time.sleep(0.1)
    
    if len(photometry_records) == 0:
        logger.warning("⚠️ No photometry found via SQL!")
        logger.info("   Trying crossid query method...")
        return query_photometry_crossid(matched, output_file)
    
    # Combine photometry
    photometry_df = pd.concat(photometry_records, ignore_index=True)
    logger.info(f"   Found photometry for {len(photometry_df)} spectra")
    
    # Merge with matched catalog
    merged = matched.merge(
        photometry_df,
        left_on='sdss_specobjid',
        right_on='query_specobjid',
        how='left',
        suffixes=('', '_photo')
    )
    
    # Save
    merged.to_csv(output_file, index=False)
    logger.info(f"💾 Saved to {output_file}")
    
    # Summary
    has_photometry = merged['dered_u'].notna()
    logger.info(f"\n📊 Photometry Summary:")
    logger.info(f"   Total matches: {len(merged)}")
    logger.info(f"   With photometry: {has_photometry.sum()}")
    logger.info(f"   Without photometry: {(~has_photometry).sum()}")
    
    if has_photometry.sum() > 0:
        logger.info(f"   u-band range: {merged.loc[has_photometry, 'dered_u'].min():.2f} - {merged.loc[has_photometry, 'dered_u'].max():.2f}")
        logger.info(f"   g-band range: {merged.loc[has_photometry, 'dered_g'].min():.2f} - {merged.loc[has_photometry, 'dered_g'].max():.2f}")
        logger.info(f"   r-band range: {merged.loc[has_photometry, 'dered_r'].min():.2f} - {merged.loc[has_photometry, 'dered_r'].max():.2f}")
    
    return merged


def query_photometry_crossid(matched, output_file):
    """
    Fallback method: use astroquery crossid to get photometry.
    """
    logger.info("   Using crossid method for photometry...")
    
    photometry_records = []
    
    for i, row in matched.iterrows():
        if (i + 1) % 50 == 0:
            logger.info(f"   Queried {i + 1}/{len(matched)} hosts...")
        
        try:
            # Query region around host coordinates
            pos = coords.SkyCoord(row['sdss_ra']*u.deg, row['sdss_dec']*u.deg, frame='icrs')
            
            # Query photoobj (photometry) near this position
            result = SDSS.query_region(pos, radius=2*u.arcsec, photo=True)
            
            if result is not None and len(result) > 0:
                result_df = result.to_pandas()
                result_df['matched_snid'] = row['snid']
                result_df['matched_specobjid'] = row['sdss_specobjid']
                photometry_records.append(result_df)
            
        except Exception as e:
            logger.warning(f"   Error querying host {row['snid']}: {e}")
            continue
        
        time.sleep(0.1)
    
    if len(photometry_records) == 0:
        logger.warning("⚠️ No photometry found via crossid either!")
        return None
    
    photometry_df = pd.concat(photometry_records, ignore_index=True)
    logger.info(f"   Found photometry for {len(photometry_df)} hosts")
    
    # For simplicity, just add photometry columns to matched catalog
    # In practice, you'd need to carefully merge based on coordinates
    merged = matched.copy()
    
    # Try to match by coordinates
    for i, row in matched.iterrows():
        # Find closest photometry match
        distances = np.sqrt(
            (photometry_df['ra'] - row['sdss_ra'])**2 + 
            (photometry_df['dec'] - row['sdss_dec'])**2
        )
        closest_idx = distances.idxmin()
        
        if distances.min() < 2/3600:  # 2 arcsec in degrees
            for band in ['u', 'g', 'r', 'i', 'z']:
                col = f'dered_{band}'
                if col in photometry_df.columns:
                    merged.loc[i, f'mag_{band}'] = photometry_df.loc[closest_idx, col]
    
    merged.to_csv(output_file, index=False)
    logger.info(f"💾 Saved to {output_file}")
    
    has_photometry = merged['mag_u'].notna()
    logger.info(f"\n📊 Photometry Summary:")
    logger.info(f"   Total matches: {len(merged)}")
    logger.info(f"   With photometry: {has_photometry.sum()}")
    
    return merged


def main():
    """Main photometry download pipeline."""
    logger.info("🌌 SDSS Photometry Download")
    logger.info("=" * 60)
    
    Path("data").mkdir(exist_ok=True)
    
    result = query_sdss_photometry()
    
    if result is not None:
        logger.info("=" * 60)
        logger.info("✅ Photometry download complete!")
        logger.info("🍩 'Real photometry for real training!'")
    else:
        logger.info("=" * 60)
        logger.info("⚠️ Photometry download incomplete")
    
    return 0


if __name__ == "__main__":
    exit(main())

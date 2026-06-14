"""
Apply AstroLANNAformer to Full Pantheon+ Sample

Predict ages for all ~1,700 Pantheon+ hosts and select evolution-free sample.

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: June 13, 2026
"""

import torch
import torch.nn as nn
import pandas as pd
import numpy as np
from pathlib import Path
import logging
import json
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
from astro_lannaformer import AstroLANNAformer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def predict_ages(model, catalog, device):
    """Predict ages for all galaxies in catalog."""
    model.eval()
    
    predictions = []
    uncertainties = []
    
    with torch.no_grad():
        for idx in range(len(catalog)):
            row = catalog.iloc[idx]
            
            # Photometry (5 SDSS bands + 3 zeros to match 8-band model)
            photometry = torch.tensor([
                row.get('dered_u', 0.0), row.get('dered_g', 0.0), 
                row.get('dered_r', 0.0), row.get('dered_i', 0.0), 
                row.get('dered_z', 0.0),
                0.0, 0.0, 0.0,
            ], dtype=torch.float32).unsqueeze(0).to(device)
            
            # Redshift
            redshift = torch.tensor([row.get('zHD', 0.0)], dtype=torch.float32).unsqueeze(0).to(device)
            
            # Predict
            preds = model(photometry=photometry, redshift=redshift)
            
            predictions.append(preds['age'].cpu().item())
            uncertainties.append(preds['uncertainty'].cpu().item())
    
    return np.array(predictions), np.array(uncertainties)


def select_evolution_free(catalog, ages, uncertainties, 
                          age_threshold=2.0,  # Gyr
                          coevality_threshold=0.8,
                          uncertainty_threshold=5.0):  # Increased from 1.0 to allow more galaxies
    """Select young, coeval host galaxies."""
    
    # Create results dataframe
    results = catalog.copy()
    results['predicted_age'] = ages
    results['age_uncertainty'] = uncertainties
    
    # Quality cuts
    valid = (
        (results['predicted_age'] > 0) &
        (results['predicted_age'] < 13.8) &
        (results['age_uncertainty'] < uncertainty_threshold)
    )
    results = results[valid].copy()
    
    # Young galaxies
    young = results['predicted_age'] < age_threshold
    results['is_young'] = young
    
    # Coevality: for galaxies with multiple SNe, check age consistency
    # For now, use uncertainty as proxy for coevality
    results['coevality_score'] = 1.0 - (results['age_uncertainty'] / uncertainty_threshold)
    results['is_coeval'] = results['coevality_score'] > coevality_threshold
    
    # Evolution-free sample
    results['evolution_free'] = results['is_young'] & results['is_coeval']
    
    return results


def main():
    """Apply model to full Pantheon+ sample."""
    logger.info("🌌 Applying AstroLANNAformer to Pantheon+ Sample")
    logger.info("=" * 60)
    
    # Config
    MODEL_PATH = 'checkpoints/mixed_training/best.pt'
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    # Load model
    logger.info("🧠 Loading best model...")
    model = AstroLANNAformer(
        n_photometry_bands=8,
        n_spectroscopy_bins=100,
        n_morphology_features=3,
        sedenion_dim=16,
        num_heads=8,
        num_layers=4,
        dropout=0.1,
        use_mlp=True,
        max_age=13.8,
    )
    
    checkpoint = torch.load(MODEL_PATH, map_location=DEVICE)
    model.load_state_dict(checkpoint['model_state_dict'])
    model = model.to(DEVICE)
    
    logger.info(f"   Loaded model from epoch {checkpoint['epoch'] + 1}")
    logger.info(f"   Best val MAE: {checkpoint['best_mae']:.4f} Gyr")
    
    # Load Pantheon+ hosts
    logger.info("📊 Loading Pantheon+ host catalog...")
    hosts = pd.read_csv('data/pantheon_hosts_with_photometry.csv')
    # Filter to hosts with photometry
    has_photometry = (
        hosts['dered_u'].notna() &
        hosts['dered_g'].notna() &
        hosts['dered_r'].notna()
    )
    hosts_with_photo = hosts[has_photometry].copy()
    
    logger.info(f"   Total hosts: {len(hosts)}")
    logger.info(f"   With photometry: {len(hosts_with_photo)}")
    
    # Predict ages for hosts with photometry
    logger.info("🔮 Predicting ages...")
    ages, uncertainties = predict_ages(model, hosts_with_photo, DEVICE)
    
    logger.info(f"   Age range: {np.nanmin(ages):.2f} - {np.nanmax(ages):.2f} Gyr")
    logger.info(f"   Mean age: {np.nanmean(ages):.2f} Gyr")
    logger.info(f"   Median uncertainty: {np.nanmedian(uncertainties):.2f} Gyr")
    
    # Add predictions to full catalog
    hosts['predicted_age'] = np.nan
    hosts['age_uncertainty'] = np.nan
    hosts.loc[has_photometry, 'predicted_age'] = ages
    hosts.loc[has_photometry, 'age_uncertainty'] = uncertainties
    
    # Select evolution-free sample
    logger.info("🎯 Selecting evolution-free sample...")
    results = select_evolution_free(hosts, hosts['predicted_age'], hosts['age_uncertainty'])
    
    # Filter to valid predictions for statistics
    valid_results = results[results['predicted_age'].notna()]
    n_valid = len(valid_results)
    
    n_young = valid_results['is_young'].sum()
    n_coeval = valid_results['is_coeval'].sum()
    n_evolution_free = valid_results['evolution_free'].sum()
    
    logger.info(f"   Valid predictions: {n_valid}")
    logger.info(f"   Young galaxies (age < 2 Gyr): {n_young} ({100*n_young/n_valid:.1f}%)")
    logger.info(f"   Coeval galaxies: {n_coeval} ({100*n_coeval/n_valid:.1f}%)")
    logger.info(f"   Evolution-free sample: {n_evolution_free} ({100*n_evolution_free/n_valid:.1f}%)")
    
    # Save results
    logger.info("💾 Saving results...")
    
    # Merge with Pantheon+ magnitudes before saving
    pantheon_file = 'data/pantheon-plus/Pantheon+_Data/4_DISTANCES_AND_COVAR/Pantheon+SH0ES.dat'
    if Path(pantheon_file).exists():
        pantheon = pd.read_csv(pantheon_file, sep=' ')
        results = results.merge(
            pantheon[['CID', 'mB', 'MU_SH0ES', 'MU_SH0ES_ERR_DIAG']],
            left_on='snid',
            right_on='CID',
            how='left'
        )
    
    results.to_csv('data/pantheon_age_predictions.csv', index=False)
    
    # Save evolution-free sample
    evolution_free = valid_results[valid_results['evolution_free']].copy()
    evolution_free.to_csv('data/evolution_free_sample.csv', index=False)
    
    logger.info(f"   Saved {len(results)} predictions")
    logger.info(f"   Evolution-free sample: {len(evolution_free)} galaxies")
    
    # Summary statistics
    summary = {
        'total_hosts': len(hosts),
        'predicted_hosts': len(results),
        'young_galaxies': int(n_young),
        'coeval_galaxies': int(n_coeval),
        'evolution_free_sample': int(n_evolution_free),
        'age_statistics': {
            'min': float(ages.min()),
            'max': float(ages.max()),
            'mean': float(ages.mean()),
            'median': float(np.median(ages)),
            'std': float(ages.std()),
        },
        'evolution_free_statistics': {
            'mean_age': float(evolution_free['predicted_age'].mean()) if len(evolution_free) > 0 else None,
            'mean_redshift': float(evolution_free['zHD'].mean()) if len(evolution_free) > 0 else None,
            'redshift_range': [float(evolution_free['zHD'].min()), float(evolution_free['zHD'].max())] if len(evolution_free) > 0 else None,
        }
    }
    
    with open('data/pantheon_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    logger.info("✅ Application complete!")
    logger.info("🍩 'From synthetic training to real cosmology!'")
    
    return 0


if __name__ == "__main__":
    exit(main())

"""
Train AstroLANNAformer from Scratch on Mixed Synthetic + Real Data

Combines synthetic galaxies (diverse ages) with real SDSS data
to learn proper age-photometry relationship without catastrophic forgetting.

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: June 13, 2026
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, ConcatDataset
import pandas as pd
import numpy as np
from pathlib import Path
import logging
import json
import copy
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
from astro_lannaformer import AstroLANNAformer, AstroPhysicsLoss

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SyntheticGalaxyDataset(Dataset):
    """Dataset for synthetic galaxies from CSV."""
    
    def __init__(self, catalog_file: str, augment=False, noise_sigma=0.05):
        self.catalog = pd.read_csv(catalog_file)
        self.augment = augment
        self.noise_sigma = noise_sigma
        
        logger.info(f"   Synthetic dataset: {len(self.catalog)} galaxies")
    
    def __len__(self):
        return len(self.catalog)
    
    def __getitem__(self, idx):
        row = self.catalog.iloc[idx]
        
        # Photometry (5 bands + 3 zeros)
        photometry = torch.tensor([
            row.get('mag_u', 20.0), row.get('mag_g', 18.0), 
            row.get('mag_r', 17.0), row.get('mag_i', 16.5), 
            row.get('mag_z', 16.0),
            0.0, 0.0, 0.0,
        ], dtype=torch.float32)
        
        if self.augment:
            noise = torch.randn_like(photometry) * self.noise_sigma
            photometry = photometry + noise
        
        redshift = torch.tensor([row.get('redshift', 0.1)], dtype=torch.float32)
        age = torch.tensor(row['age'], dtype=torch.float32)
        mass = torch.tensor(row['mass'], dtype=torch.float32)
        
        return {
            'features': {
                'photometry': photometry,
                'redshift': redshift,
            },
            'targets': {
                'age': age,
                'mass': mass,
            },
        }


class RealGalaxyDataset(Dataset):
    """Dataset for real SDSS galaxies."""
    
    def __init__(self, catalog_file: str, augment=False, noise_sigma=0.05):
        self.catalog = pd.read_csv(catalog_file)
        self.augment = augment
        self.noise_sigma = noise_sigma
        
        # Filter valid data
        valid = (
            self.catalog['dered_u'].notna() &
            self.catalog['dered_g'].notna() &
            self.catalog['dered_r'].notna() &
            self.catalog['stellar_age_estimated'].notna()
        )
        self.catalog = self.catalog[valid].reset_index(drop=True)
        
        logger.info(f"   Real dataset: {len(self.catalog)} galaxies")
    
    def __len__(self):
        return len(self.catalog)
    
    def __getitem__(self, idx):
        row = self.catalog.iloc[idx]
        
        photometry = torch.tensor([
            row['dered_u'], row['dered_g'], row['dered_r'],
            row['dered_i'], row['dered_z'],
            0.0, 0.0, 0.0,
        ], dtype=torch.float32)
        
        if self.augment:
            noise = torch.randn_like(photometry) * self.noise_sigma
            photometry = photometry + noise
        
        redshift = torch.tensor([row['zHD']], dtype=torch.float32)
        age = torch.tensor(row['stellar_age_estimated'], dtype=torch.float32)
        mass = torch.tensor(1e10, dtype=torch.float32)
        
        return {
            'features': {
                'photometry': photometry,
                'redshift': redshift,
            },
            'targets': {
                'age': age,
                'mass': mass,
            },
        }


def train_epoch(model, loader, optimizer, loss_fn, device):
    """Train one epoch."""
    model.train()
    total_loss = 0
    
    for batch in loader:
        features = {k: v.to(device) for k, v in batch['features'].items()}
        targets = {k: v.to(device) for k, v in batch['targets'].items()}
        
        predictions = model(
            photometry=features['photometry'],
            redshift=features['redshift'],
        )
        
        loss, _ = loss_fn(predictions, targets, features)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
    
    return total_loss / len(loader)


def evaluate_model(model, loader, device):
    """Evaluate model."""
    model.eval()
    
    all_preds = []
    all_targets = []
    all_unc = []
    
    with torch.no_grad():
        for batch in loader:
            features = {k: v.to(device) for k, v in batch['features'].items()}
            targets = {k: v.to(device) for k, v in batch['targets'].items()}
            
            predictions = model(
                photometry=features['photometry'],
                redshift=features['redshift'],
            )
            
            all_preds.append(predictions['age'].cpu())
            all_targets.append(targets['age'].cpu())
            all_unc.append(predictions['uncertainty'].cpu())
    
    all_preds = torch.cat(all_preds)
    all_targets = torch.cat(all_targets)
    all_unc = torch.cat(all_unc)
    
    errors = all_preds - all_targets
    mae = torch.mean(torch.abs(errors)).item()
    bias = torch.mean(errors).item()
    scatter = torch.std(errors).item()
    calibration = torch.mean(torch.abs(errors) / (all_unc + 1e-8)).item()
    
    return {'mae': mae, 'bias': bias, 'scatter': scatter, 'calibration': calibration}


def main():
    """Main mixed training pipeline."""
    logger.info("🌌 Training AstroLANNAformer on Mixed Synthetic + Real Data")
    logger.info("=" * 60)
    
    # Config
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
    N_EPOCHS = 50
    LR = 1e-4
    BATCH_SIZE = 64
    PATIENCE = 7
    WEIGHT_DECAY = 1e-4
    
    logger.info(f"Device: {DEVICE} | Epochs: {N_EPOCHS} | LR: {LR}")
    
    # Load synthetic data
    logger.info("📊 Loading synthetic data...")
    synthetic_train = SyntheticGalaxyDataset('data/synthetic_galaxies.csv', augment=True, noise_sigma=0.05)
    
    # Load real data
    logger.info("📊 Loading real SDSS data...")
    photo = pd.read_csv('data/matched_catalog_with_photometry.csv')
    ages = pd.read_csv('data/matched_catalog_with_ages.csv')
    catalog = photo.merge(ages[['snid', 'stellar_age_estimated']], on='snid', how='left')
    catalog.to_csv('data/mixed_real_catalog.csv', index=False)
    
    real_train = RealGalaxyDataset('data/mixed_real_catalog.csv', augment=True, noise_sigma=0.05)
    
    # Combine datasets
    logger.info("🔄 Combining datasets...")
    combined_train = ConcatDataset([synthetic_train, real_train])
    
    # Split real data for validation/test
    n_real = len(real_train)
    n_real_val = int(0.15 * n_real)
    n_real_test = int(0.15 * n_real)
    
    real_indices = list(range(n_real))
    np.random.shuffle(real_indices)
    
    real_val_indices = real_indices[:n_real_val]
    real_test_indices = real_indices[n_real_val:n_real_val + n_real_test]
    real_train_indices = real_indices[n_real_val + n_real_test:]
    
    # Create validation set (synthetic + real)
    synthetic_val = SyntheticGalaxyDataset('data/synthetic_galaxies.csv', augment=False)
    real_val = torch.utils.data.Subset(real_train, real_val_indices)
    combined_val = ConcatDataset([synthetic_val, real_val])
    
    # Create test set (real only)
    real_test = torch.utils.data.Subset(real_train, real_test_indices)
    
    # Create dataloaders
    train_loader = DataLoader(combined_train, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(combined_val, batch_size=BATCH_SIZE)
    test_loader = DataLoader(real_test, batch_size=BATCH_SIZE)
    
    logger.info(f"Train: {len(combined_train)} | Val: {len(combined_val)} | Test: {len(real_test)}")
    
    # Model
    logger.info("🧠 Creating AstroLANNAformer...")
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
    model = model.to(DEVICE)
    
    n_params = sum(p.numel() for p in model.parameters())
    logger.info(f"   Parameters: {n_params:,}")
    
    # Optimizer
    optimizer = optim.Adam(model.parameters(), lr=LR, weight_decay=WEIGHT_DECAY)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=3)
    loss_fn = AstroPhysicsLoss(age_weight=1.0, uncertainty_weight=0.5)
    
    # Create checkpoint directory
    Path('checkpoints/mixed_training').mkdir(exist_ok=True, parents=True)
    
    # Train with early stopping
    logger.info("🚀 Training...")
    logger.info("=" * 60)
    
    best_mae = float('inf')
    best_epoch = 0
    best_model_state = None
    patience_counter = 0
    
    history = {
        'train_loss': [], 'val_mae': [], 'val_bias': [], 
        'val_scatter': [], 'val_calibration': [], 'lr': []
    }
    
    for epoch in range(N_EPOCHS):
        train_loss = train_epoch(model, train_loader, optimizer, loss_fn, DEVICE)
        val_metrics = evaluate_model(model, val_loader, DEVICE)
        
        scheduler.step(val_metrics['mae'])
        current_lr = optimizer.param_groups[0]['lr']
        
        history['train_loss'].append(train_loss)
        history['val_mae'].append(val_metrics['mae'])
        history['val_bias'].append(val_metrics['bias'])
        history['val_scatter'].append(val_metrics['scatter'])
        history['val_calibration'].append(val_metrics['calibration'])
        history['lr'].append(current_lr)
        
        # Early stopping
        if val_metrics['mae'] < best_mae:
            best_mae = val_metrics['mae']
            best_epoch = epoch
            best_model_state = copy.deepcopy(model.state_dict())
            patience_counter = 0
            
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'best_mae': best_mae,
            }, 'checkpoints/mixed_training/best.pt')
        else:
            patience_counter += 1
        
        logger.info(
            f"Epoch {epoch + 1}/{N_EPOCHS} | "
            f"Train: {train_loss:.4f} | "
            f"Val MAE: {val_metrics['mae']:.4f} | "
            f"Bias: {val_metrics['bias']:.4f} | "
            f"Scatter: {val_metrics['scatter']:.4f} | "
            f"LR: {current_lr:.2e} | "
            f"Patience: {patience_counter}/{PATIENCE}"
        )
        
        if patience_counter >= PATIENCE:
            logger.info(f"🛑 Early stopping at epoch {epoch + 1}!")
            break
    
    # Test on real data
    logger.info("=" * 60)
    logger.info(f"🧪 Loading best model (epoch {best_epoch + 1})...")
    model.load_state_dict(best_model_state)
    
    test_metrics = evaluate_model(model, test_loader, DEVICE)
    logger.info(
        f"Test MAE: {test_metrics['mae']:.4f} | "
        f"Bias: {test_metrics['bias']:.4f} | "
        f"Scatter: {test_metrics['scatter']:.4f} | "
        f"Cal: {test_metrics['calibration']:.4f}"
    )
    
    # Save results
    with open('data/mixed_training_results.json', 'w') as f:
        json.dump({
            'config': {
                'lr': LR,
                'batch_size': BATCH_SIZE,
                'n_epochs': epoch + 1,
                'patience': PATIENCE,
                'weight_decay': WEIGHT_DECAY,
            },
            'history': history,
            'test': test_metrics,
            'best_epoch': best_epoch,
            'best_val_mae': best_mae,
        }, f, indent=2, default=str)
    
    logger.info("💾 Results saved!")
    logger.info("✅ Mixed training complete!")
    logger.info("🍩 'Synthetic + Real = Better Cosmology!'")
    
    return 0


if __name__ == "__main__":
    exit(main())

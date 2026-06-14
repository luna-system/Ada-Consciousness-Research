"""
Fine-tune AstroLANNAformer on Real SDSS Data (Simplified)

Loads pretrained model and fine-tunes on real SDSS photometry + ages.
Simplified version that only uses photometry and redshift (no spectroscopy).

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: June 13, 2026
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import numpy as np
from pathlib import Path
import logging
import json

from astro_lannaformer import AstroLANNAformer, AstroPhysicsLoss

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SimpleRealDataset(Dataset):
    """Simple dataset for real galaxies with photometry only."""
    
    def __init__(self, catalog: pd.DataFrame):
        self.catalog = catalog
        
        # Filter valid data
        valid = (
            catalog['dered_u'].notna() &
            catalog['dered_g'].notna() &
            catalog['dered_r'].notna() &
            catalog['stellar_age_estimated'].notna()
        )
        self.catalog = catalog[valid].reset_index(drop=True)
        logger.info(f"   Dataset: {len(self.catalog)} valid galaxies")
    
    def __len__(self):
        return len(self.catalog)
    
    def __getitem__(self, idx):
        row = self.catalog.iloc[idx]
        
        # Photometry (5 SDSS bands + 3 zeros to match 8-band model)
        photometry = torch.tensor([
            row['dered_u'], row['dered_g'], row['dered_r'],
            row['dered_i'], row['dered_z'],
            0.0, 0.0, 0.0,
        ], dtype=torch.float32)
        
        # Redshift
        redshift = torch.tensor([row['zHD']], dtype=torch.float32)
        
        # Target: age
        age = torch.tensor(row['stellar_age_estimated'], dtype=torch.float32)
        
        # Target: mass (placeholder)
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
        
        # Forward (only photometry and redshift)
        predictions = model(
            photometry=features['photometry'],
            redshift=features['redshift'],
        )
        
        # Loss
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
    """Main fine-tuning pipeline."""
    logger.info("🌌 Fine-tuning AstroLANNAformer on Real SDSS Data")
    logger.info("=" * 60)
    
    # Config
    PRETRAINED = 'checkpoints/10k_run/best.pt'
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
    N_EPOCHS = 50
    LR = 1e-4
    BATCH_SIZE = 16
    
    logger.info(f"Device: {DEVICE} | Epochs: {N_EPOCHS} | LR: {LR}")
    
    # Load data
    logger.info("📊 Loading real SDSS data...")
    photo = pd.read_csv('data/matched_catalog_with_photometry.csv')
    ages = pd.read_csv('data/matched_catalog_with_ages.csv')
    catalog = photo.merge(ages[['snid', 'stellar_age_estimated']], on='snid', how='left')
    
    dataset = SimpleRealDataset(catalog)
    
    # Split
    n = len(dataset)
    n_train = int(0.7 * n)
    n_val = int(0.15 * n)
    
    train_set = torch.utils.data.Subset(dataset, range(n_train))
    val_set = torch.utils.data.Subset(dataset, range(n_train, n_train + n_val))
    test_set = torch.utils.data.Subset(dataset, range(n_train + n_val, n))
    
    train_loader = DataLoader(train_set, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_set, batch_size=BATCH_SIZE)
    test_loader = DataLoader(test_set, batch_size=BATCH_SIZE)
    
    logger.info(f"Split: {len(train_set)} train, {len(val_set)} val, {len(test_set)} test")
    
    # Model
    logger.info("🧠 Loading pretrained model...")
    model = AstroLANNAformer(
        n_photometry_bands=8,
        n_spectroscopy_bins=100,  # Smaller since not used
        n_morphology_features=3,
        sedenion_dim=16,
        num_heads=8,
        num_layers=4,
        dropout=0.1,
        use_mlp=True,
        max_age=13.8,
    )
    
    # Load pretrained weights
    checkpoint = torch.load(PRETRAINED, map_location=DEVICE)
    model.load_state_dict(checkpoint['model_state_dict'])
    logger.info(f"   Loaded from epoch {checkpoint['epoch'] + 1}")
    
    # Freeze early layers
    for param in model.embedding.parameters():
        param.requires_grad = False
    for param in model.attention_layers[0].parameters():
        param.requires_grad = False
    
    model = model.to(DEVICE)
    
    n_trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    n_total = sum(p.numel() for p in model.parameters())
    logger.info(f"   Trainable: {n_trainable:,} / {n_total:,}")
    
    # Optimizer
    optimizer = optim.Adam(
        filter(lambda p: p.requires_grad, model.parameters()),
        lr=LR, weight_decay=1e-5
    )
    loss_fn = AstroPhysicsLoss(age_weight=1.0, uncertainty_weight=0.5)
    
    # Train
    logger.info("🚀 Fine-tuning...")
    logger.info("=" * 60)
    
    best_mae = float('inf')
    history = {'train_loss': [], 'val_mae': [], 'val_bias': [], 'val_scatter': []}
    
    for epoch in range(N_EPOCHS):
        train_loss = train_epoch(model, train_loader, optimizer, loss_fn, DEVICE)
        val_metrics = evaluate_model(model, val_loader, DEVICE)
        
        history['train_loss'].append(train_loss)
        history['val_mae'].append(val_metrics['mae'])
        history['val_bias'].append(val_metrics['bias'])
        history['val_scatter'].append(val_metrics['scatter'])
        
        is_best = val_metrics['mae'] < best_mae
        if is_best:
            best_mae = val_metrics['mae']
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'best_mae': best_mae,
            }, 'checkpoints/finetune_real/best.pt')
        
        logger.info(
            f"Epoch {epoch + 1}/{N_EPOCHS} | "
            f"Train: {train_loss:.4f} | "
            f"Val MAE: {val_metrics['mae']:.4f} | "
            f"Bias: {val_metrics['bias']:.4f} | "
            f"Scatter: {val_metrics['scatter']:.4f}"
        )
    
    # Test
    logger.info("=" * 60)
    logger.info("🧪 Testing...")
    test_metrics = evaluate_model(model, test_loader, DEVICE)
    logger.info(
        f"Test MAE: {test_metrics['mae']:.4f} | "
        f"Bias: {test_metrics['bias']:.4f} | "
        f"Scatter: {test_metrics['scatter']:.4f} | "
        f"Cal: {test_metrics['calibration']:.4f}"
    )
    
    # Save
    Path('checkpoints/finetune_real').mkdir(exist_ok=True, parents=True)
    with open('data/finetune_results.json', 'w') as f:
        json.dump({'history': history, 'test': test_metrics}, f, default=str)
    
    logger.info("💾 Results saved!")
    logger.info("✅ Fine-tuning complete!")
    logger.info("🍩 'Real data, real learning, real cosmology!'")
    
    return 0


if __name__ == "__main__":
    exit(main())

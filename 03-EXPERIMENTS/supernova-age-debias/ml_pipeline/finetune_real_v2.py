"""
Fine-tune AstroLANNAformer on Real SDSS Data (Iteration 2)

Improved version with:
- Early stopping (patience=5)
- Lower learning rate (1e-5)
- More frozen layers
- Stronger L2 regularization (1e-3)
- Data augmentation (photometric noise)

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
import copy
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from astro_lannaformer import AstroLANNAformer, AstroPhysicsLoss

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AugmentedRealDataset(Dataset):
    """Real galaxy dataset with photometric noise augmentation."""
    
    def __init__(self, catalog: pd.DataFrame, augment=False, noise_sigma=0.05):
        self.catalog = catalog
        self.augment = augment
        self.noise_sigma = noise_sigma
        
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
        
        # Add noise during training
        if self.augment:
            noise = torch.randn_like(photometry) * self.noise_sigma
            photometry = photometry + noise
        
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
    """Main fine-tuning pipeline with early stopping."""
    logger.info("🌌 Fine-tuning AstroLANNAformer on Real SDSS Data (Iteration 2)")
    logger.info("=" * 60)
    
    # Config
    PRETRAINED = 'checkpoints/10k_run/best.pt'
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
    N_EPOCHS = 50
    LR = 1e-5  # 100x lower than iteration 1
    BATCH_SIZE = 16
    PATIENCE = 5
    WEIGHT_DECAY = 1e-3  # Stronger regularization
    NOISE_SIGMA = 0.05  # Photometric augmentation
    
    logger.info(f"Device: {DEVICE} | Epochs: {N_EPOCHS} | LR: {LR}")
    logger.info(f"Patience: {PATIENCE} | Weight Decay: {WEIGHT_DECAY}")
    
    # Load data
    logger.info("📊 Loading real SDSS data...")
    photo = pd.read_csv('data/matched_catalog_with_photometry.csv')
    ages = pd.read_csv('data/matched_catalog_with_ages.csv')
    catalog = photo.merge(ages[['snid', 'stellar_age_estimated']], on='snid', how='left')
    
    # Create datasets (with augmentation for training)
    full_dataset = AugmentedRealDataset(catalog, augment=False)
    
    # Split
    n = len(full_dataset)
    n_train = int(0.7 * n)
    n_val = int(0.15 * n)
    
    # Use augmented dataset for training
    train_set = AugmentedRealDataset(catalog.iloc[:n_train].reset_index(drop=True), augment=True, noise_sigma=NOISE_SIGMA)
    val_set = AugmentedRealDataset(catalog.iloc[n_train:n_train + n_val].reset_index(drop=True), augment=False)
    test_set = AugmentedRealDataset(catalog.iloc[n_train + n_val:].reset_index(drop=True), augment=False)
    
    train_loader = DataLoader(train_set, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_set, batch_size=BATCH_SIZE)
    test_loader = DataLoader(test_set, batch_size=BATCH_SIZE)
    
    logger.info(f"Split: {len(train_set)} train, {len(val_set)} val, {len(test_set)} test")
    
    # Model
    logger.info("🧠 Loading pretrained model...")
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
    
    # Load pretrained weights
    checkpoint = torch.load(PRETRAINED, map_location=DEVICE)
    model.load_state_dict(checkpoint['model_state_dict'])
    logger.info(f"   Loaded from epoch {checkpoint['epoch'] + 1}")
    
    # Freeze MORE layers (embedding + first 2 attention layers)
    frozen_count = 0
    for param in model.embedding.parameters():
        param.requires_grad = False
        frozen_count += param.numel()
    
    for i, layer in enumerate(model.attention_layers):
        if i < 2:  # Freeze first 2 layers
            for param in layer.parameters():
                param.requires_grad = False
                frozen_count += param.numel()
    
    model = model.to(DEVICE)
    
    n_trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    n_total = sum(p.numel() for p in model.parameters())
    logger.info(f"   Frozen: {frozen_count:,} | Trainable: {n_trainable:,} / {n_total:,}")
    
    # Optimizer with stronger weight decay
    optimizer = optim.Adam(
        filter(lambda p: p.requires_grad, model.parameters()),
        lr=LR, weight_decay=WEIGHT_DECAY
    )
    
    # Learning rate scheduler
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='min', factor=0.5, patience=3
    )
    
    loss_fn = AstroPhysicsLoss(age_weight=1.0, uncertainty_weight=0.5)
    
    # Train with early stopping
    logger.info("🚀 Fine-tuning with early stopping...")
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
        
        # Update scheduler
        scheduler.step(val_metrics['mae'])
        current_lr = optimizer.param_groups[0]['lr']
        
        history['train_loss'].append(train_loss)
        history['val_mae'].append(val_metrics['mae'])
        history['val_bias'].append(val_metrics['bias'])
        history['val_scatter'].append(val_metrics['scatter'])
        history['val_calibration'].append(val_metrics['calibration'])
        history['lr'].append(current_lr)
        
        # Early stopping check
        if val_metrics['mae'] < best_mae:
            best_mae = val_metrics['mae']
            best_epoch = epoch
            best_model_state = copy.deepcopy(model.state_dict())
            patience_counter = 0
            
            # Save best
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'best_mae': best_mae,
            }, 'checkpoints/finetune_real/best_v2.pt')
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
            logger.info(f"🛑 Early stopping triggered at epoch {epoch + 1}!")
            break
    
    # Load best model for testing
    logger.info("=" * 60)
    logger.info(f"🧪 Loading best model (epoch {best_epoch + 1}, MAE: {best_mae:.4f})...")
    model.load_state_dict(best_model_state)
    
    test_metrics = evaluate_model(model, test_loader, DEVICE)
    logger.info(
        f"Test MAE: {test_metrics['mae']:.4f} | "
        f"Bias: {test_metrics['bias']:.4f} | "
        f"Scatter: {test_metrics['scatter']:.4f} | "
        f"Cal: {test_metrics['calibration']:.4f}"
    )
    
    # Save results
    Path('checkpoints/finetune_real').mkdir(exist_ok=True, parents=True)
    with open('data/finetune_results_v2.json', 'w') as f:
        json.dump({
            'config': {
                'lr': LR,
                'batch_size': BATCH_SIZE,
                'n_epochs': epoch + 1,
                'patience': PATIENCE,
                'weight_decay': WEIGHT_DECAY,
                'noise_sigma': NOISE_SIGMA,
                'frozen_layers': 'embedding + first 2 attention',
            },
            'history': history,
            'test': test_metrics,
            'best_epoch': best_epoch,
            'best_val_mae': best_mae,
        }, f, indent=2, default=str)
    
    logger.info("💾 Results saved to data/finetune_results_v2.json!")
    logger.info("✅ Fine-tuning iteration 2 complete!")
    logger.info("🍩 'Early stopping saves the universe!'")
    
    return 0


if __name__ == "__main__":
    exit(main())

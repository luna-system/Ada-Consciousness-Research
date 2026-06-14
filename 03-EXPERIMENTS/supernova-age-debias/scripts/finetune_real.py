"""
Fine-tune AstroLANNAformer on Real SDSS Data

Loads pretrained model (trained on 10K synthetic galaxies) and fine-tunes
on real SDSS photometry + converted ages for Pantheon+ hosts.

Architecture:
    Pretrained Model → Freeze Early Layers → Fine-tune on Real Data → Evaluate

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
from typing import Dict, Tuple

from astro_lannaformer import (
    AstroLANNAformer, AstroPhysicsLoss,
    train_step, evaluate
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)


class RealGalaxyDataset(Dataset):
    """Dataset for real SDSS galaxies with photometry and ages."""
    
    def __init__(self, catalog: pd.DataFrame):
        self.catalog = catalog
        
        # Filter to galaxies with valid photometry and ages
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
        
        # Photometry (dereddened SDSS magnitudes)
        photometry = torch.tensor([
            row['dered_u'], row['dered_g'], row['dered_r'],
            row['dered_i'], row['dered_z'],
            # Pad to 8 bands with zeros if needed
            0.0, 0.0, 0.0,
        ], dtype=torch.float32)
        
        # Redshift
        redshift = torch.tensor([row['zHD']], dtype=torch.float32)
        
        # Target: age from redshift conversion
        age = torch.tensor(row['stellar_age_estimated'], dtype=torch.float32)
        
        # Target: mass (use log10)
        mass = torch.tensor(10**10, dtype=torch.float32)  # Placeholder
        
        return {
            'features': {
                'photometry': photometry,
                'redshift': redshift,
                'spectroscopy': torch.zeros(0),  # Empty tensor instead of None
                'morphology': torch.zeros(0),  # Empty tensor instead of None
            },
            'targets': {
                'age': age,
                'mass': mass,
            },
        }


class FineTuner:
    """Fine-tuning manager for domain adaptation."""
    
    def __init__(
        self,
        model: AstroLANNAformer,
        pretrained_path: str,
        train_loader: DataLoader,
        val_loader: DataLoader,
        test_loader: DataLoader,
        device: str = 'cpu',
        checkpoint_dir: str = 'checkpoints/finetune_real',
    ):
        self.device = device
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(exist_ok=True, parents=True)
        
        # Load pretrained model
        logger.info(f"🧠 Loading pretrained model from {pretrained_path}...")
        checkpoint = torch.load(pretrained_path, map_location=device)
        model.load_state_dict(checkpoint['model_state_dict'])
        logger.info(f"   Loaded model from epoch {checkpoint['epoch'] + 1}")
        
        self.model = model.to(device)
        
        # Freeze early layers (embedding + first attention layer)
        logger.info("   Freezing early layers...")
        for param in self.model.embedding.parameters():
            param.requires_grad = False
        for param in self.model.attention_layers[0].parameters():
            param.requires_grad = False
        
        # Count trainable parameters
        n_trainable = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
        n_total = sum(p.numel() for p in self.model.parameters())
        logger.info(f"   Trainable parameters: {n_trainable:,} / {n_total:,}")
        
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.test_loader = test_loader
        
        self.history = {
            'train_loss': [],
            'val_mae': [],
            'val_bias': [],
            'val_scatter': [],
        }
        
        self.best_val_mae = float('inf')
    
    def train_epoch(self, optimizer, loss_fn) -> float:
        """Train for one epoch."""
        self.model.train()
        total_loss = 0
        n_batches = 0
        
        for batch in self.train_loader:
            loss, components = train_step(
                self.model, optimizer, loss_fn, batch, self.device
            )
            total_loss += loss
            n_batches += 1
        
        return total_loss / n_batches
    
    def validate(self) -> Dict[str, float]:
        """Validate on real data."""
        return evaluate(self.model, self.val_loader, self.device)
    
    def save_checkpoint(self, epoch: int, is_best: bool = False):
        """Save checkpoint."""
        checkpoint = {
            'epoch': epoch,
            'model_state_dict': self.model.state_dict(),
            'history': self.history,
            'best_val_mae': self.best_val_mae,
        }
        
        path = self.checkpoint_dir / 'latest.pt'
        torch.save(checkpoint, path)
        
        if is_best:
            path = self.checkpoint_dir / 'best.pt'
            torch.save(checkpoint, path)
            logger.info(f"  💾 Best model saved! (MAE: {self.best_val_mae:.4f})")
    
    def train(self, n_epochs: int = 50, lr: float = 1e-4):
        """Fine-tune on real data."""
        logger.info(f"🚀 Fine-tuning for {n_epochs} epochs (lr={lr})...")
        
        # Only optimize trainable parameters
        optimizer = optim.Adam(
            filter(lambda p: p.requires_grad, self.model.parameters()),
            lr=lr,
            weight_decay=1e-5,  # L2 regularization for fine-tuning
        )
        
        loss_fn = AstroPhysicsLoss(
            age_weight=1.0,
            uncertainty_weight=0.5,
            age_color_weight=0.2,  # Reduced for real data
            age_mass_weight=0.1,
        )
        
        for epoch in range(n_epochs):
            train_loss = self.train_epoch(optimizer, loss_fn)
            val_metrics = self.validate()
            
            self.history['train_loss'].append(train_loss)
            self.history['val_mae'].append(val_metrics['mae'])
            self.history['val_bias'].append(val_metrics['bias'])
            self.history['val_scatter'].append(val_metrics['scatter'])
            
            is_best = val_metrics['mae'] < self.best_val_mae
            if is_best:
                self.best_val_mae = val_metrics['mae']
            
            self.save_checkpoint(epoch, is_best)
            
            logger.info(
                f"📊 Epoch {epoch + 1}/{n_epochs} | "
                f"Train: {train_loss:.4f} | "
                f"Val MAE: {val_metrics['mae']:.4f} | "
                f"Val Bias: {val_metrics['bias']:.4f} | "
                f"Val Scatter: {val_metrics['scatter']:.4f}"
            )
        
        logger.info(f"✅ Fine-tuning complete! Best Val MAE: {self.best_val_mae:.4f} Gyr")
        return self.history
    
    def test(self) -> Dict[str, float]:
        """Test on held-out real data."""
        logger.info("🧪 Testing on real held-out data...")
        
        # Load best checkpoint
        checkpoint_path = self.checkpoint_dir / 'best.pt'
        if checkpoint_path.exists():
            checkpoint = torch.load(checkpoint_path, map_location=self.device)
            self.model.load_state_dict(checkpoint['model_state_dict'])
        
        metrics = evaluate(self.model, self.test_loader, self.device)
        
        logger.info(
            f"📊 Real Data Test | MAE: {metrics['mae']:.4f} | "
            f"Bias: {metrics['bias']:.4f} | "
            f"Scatter: {metrics['scatter']:.4f} | "
            f"Calibration: {metrics['calibration']:.4f}"
        )
        
        return metrics


def main():
    """Main fine-tuning pipeline."""
    logger.info("🌌 AstroLANNAformer Fine-tuning on Real SDSS Data")
    logger.info("=" * 60)
    
    # Configuration
    PRETRAINED_PATH = 'checkpoints/10k_run/best.pt'
    CATALOG_FILE = 'data/matched_catalog_with_photometry.csv'
    BATCH_SIZE = 16
    N_EPOCHS = 50
    LR = 1e-4
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    logger.info(f"Configuration:")
    logger.info(f"  Pretrained: {PRETRAINED_PATH}")
    logger.info(f"  Catalog: {CATALOG_FILE}")
    logger.info(f"  Batch size: {BATCH_SIZE}")
    logger.info(f"  Epochs: {N_EPOCHS}")
    logger.info(f"  Learning rate: {LR}")
    logger.info(f"  Device: {DEVICE}")
    
    # Load real data catalog
    logger.info("📊 Loading real SDSS catalog...")
    
    # Load photometry catalog
    photo_catalog = pd.read_csv('data/matched_catalog_with_photometry.csv')
    
    # Load age catalog
    age_catalog = pd.read_csv('data/matched_catalog_with_ages.csv')
    
    # Merge on snid
    catalog = photo_catalog.merge(age_catalog[['snid', 'stellar_age_estimated', 'stellar_age_err', 'universe_age_at_z', 'lookback_time']], on='snid', how='left')
    
    logger.info(f"   Loaded {len(catalog)} galaxies with photometry and ages")
    
    # Check available columns
    logger.info(f"   Available columns: {list(catalog.columns)}")
    
    # Create dataset
    dataset = RealGalaxyDataset(catalog)
    
    # Split: 70% train, 15% val, 15% test
    n_total = len(dataset)
    n_train = int(0.7 * n_total)
    n_val = int(0.15 * n_total)
    
    train_dataset = torch.utils.data.Subset(dataset, range(n_train))
    val_dataset = torch.utils.data.Subset(dataset, range(n_train, n_train + n_val))
    test_dataset = torch.utils.data.Subset(dataset, range(n_train + n_val, n_total))
    
    logger.info(f"   Split: {len(train_dataset)} train, {len(val_dataset)} val, {len(test_dataset)} test")
    
    # Create dataloaders
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)
    
    # Create model
    logger.info("🧠 Creating AstroLANNAformer...")
    model = AstroLANNAformer(
        n_photometry_bands=8,
        n_spectroscopy_bins=1000,
        n_morphology_features=3,
        sedenion_dim=16,
        num_heads=8,
        num_layers=4,
        dropout=0.1,
        use_mlp=True,
        max_age=13.8,
    )
    
    # Fine-tune
    logger.info("🚀 Starting fine-tuning...")
    logger.info("=" * 60)
    
    finetuner = FineTuner(
        model=model,
        pretrained_path=PRETRAINED_PATH,
        train_loader=train_loader,
        val_loader=val_loader,
        test_loader=test_loader,
        device=DEVICE,
    )
    
    history = finetuner.train(n_epochs=N_EPOCHS, lr=LR)
    
    # Test
    logger.info("=" * 60)
    test_metrics = finetuner.test()
    
    # Save results
    results = {
        'config': {
            'pretrained_path': PRETRAINED_PATH,
            'n_epochs': N_EPOCHS,
            'lr': LR,
            'batch_size': BATCH_SIZE,
            'device': DEVICE,
        },
        'history': history,
        'test_metrics': test_metrics,
    }
    
    with open('data/finetune_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    logger.info("💾 Results saved to data/finetune_results.json")
    logger.info("=" * 60)
    logger.info("✅ Fine-tuning complete!")
    logger.info("🍩 'Real data, real learning, real cosmology!'")
    
    return 0


if __name__ == "__main__":
    exit(main())

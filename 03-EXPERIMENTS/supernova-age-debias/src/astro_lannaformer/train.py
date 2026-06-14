"""
Train AstroLANNAformer on Synthetic Galaxy Data

Professional training pipeline with logging, checkpointing, and evaluation.

Usage:
    python -m astro_lannaformer.train --n_galaxies 10000 --epochs 50 --batch_size 64

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: June 13, 2026
"""

import argparse
import json
import logging
import sys
import time
from pathlib import Path
from typing import Dict, Optional

import torch
import torch.optim as optim
from torch.utils.data import DataLoader

from .model import AstroLANNAformer, AstroPhysicsLoss, train_step, evaluate
from .data import SyntheticGalaxyGenerator, create_dataloaders


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('training.log'),
    ]
)
logger = logging.getLogger(__name__)


class Trainer:
    """Professional training manager for AstroLANNAformer."""
    
    def __init__(
        self,
        model: AstroLANNAformer,
        train_loader: DataLoader,
        val_loader: DataLoader,
        test_loader: DataLoader,
        optimizer: optim.Optimizer,
        loss_fn: AstroPhysicsLoss,
        device: str = 'cpu',
        checkpoint_dir: str = 'checkpoints',
        log_interval: int = 10,
    ):
        self.model = model.to(device)
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.test_loader = test_loader
        self.optimizer = optimizer
        self.loss_fn = loss_fn
        self.device = device
        self.log_interval = log_interval
        
        # Checkpointing
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(exist_ok=True)
        
        # Training history
        self.history = {
            'train_loss': [],
            'val_loss': [],
            'val_mae': [],
            'val_bias': [],
            'val_scatter': [],
            'val_calibration': [],
        }
        
        self.best_val_mae = float('inf')
        self.epochs_trained = 0
        
    def train_epoch(self, epoch: int) -> float:
        """Train for one epoch."""
        self.model.train()
        total_loss = 0
        n_batches = 0
        
        for batch_idx, batch in enumerate(self.train_loader):
            loss, components = train_step(
                self.model,
                self.optimizer,
                self.loss_fn,
                batch,
                self.device,
            )
            
            total_loss += loss
            n_batches += 1
            
            # Log progress
            if (batch_idx + 1) % self.log_interval == 0:
                logger.info(
                    f"Epoch {epoch} | Batch {batch_idx + 1}/{len(self.train_loader)} | "
                    f"Loss: {loss:.4f} | Age: {components['age_loss']:.4f} | "
                    f"Unc: {components['uncertainty_loss']:.4f}"
                )
        
        avg_loss = total_loss / n_batches
        return avg_loss
    
    def validate(self) -> Dict[str, float]:
        """Validate on validation set."""
        self.model.eval()
        
        all_predictions = []
        all_targets = []
        all_uncertainties = []
        total_val_loss = 0
        n_batches = 0
        
        with torch.no_grad():
            for batch in self.val_loader:
                features = {k: v.to(self.device) for k, v in batch['features'].items()}
                targets = {k: v.to(self.device) for k, v in batch['targets'].items()}
                
                predictions = self.model(
                    photometry=features['photometry'],
                    redshift=features['redshift'],
                    spectroscopy=features.get('spectroscopy'),
                    morphology=features.get('morphology'),
                )
                
                loss, _ = self.loss_fn(predictions, targets, features)
                total_val_loss += loss.item()
                n_batches += 1
                
                all_predictions.append(predictions['age'].cpu())
                all_targets.append(targets['age'].cpu())
                all_uncertainties.append(predictions['uncertainty'].cpu())
        
        # Compute metrics
        all_predictions = torch.cat(all_predictions)
        all_targets = torch.cat(all_targets)
        all_uncertainties = torch.cat(all_uncertainties)
        
        errors = all_predictions - all_targets
        mae = torch.mean(torch.abs(errors)).item()
        bias = torch.mean(errors).item()
        scatter = torch.std(errors).item()
        
        actual_errors = torch.abs(errors)
        calibration = torch.mean(actual_errors / (all_uncertainties + 1e-8)).item()
        
        avg_val_loss = total_val_loss / n_batches
        
        return {
            'loss': avg_val_loss,
            'mae': mae,
            'bias': bias,
            'scatter': scatter,
            'calibration': calibration,
        }
    
    def save_checkpoint(self, epoch: int, is_best: bool = False):
        """Save model checkpoint."""
        checkpoint = {
            'epoch': epoch,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'history': self.history,
            'best_val_mae': self.best_val_mae,
        }
        
        # Save latest checkpoint
        path = self.checkpoint_dir / 'latest.pt'
        torch.save(checkpoint, path)
        
        # Save best checkpoint
        if is_best:
            path = self.checkpoint_dir / 'best.pt'
            torch.save(checkpoint, path)
            logger.info(f"💾 Best model saved! (MAE: {self.best_val_mae:.4f})")
    
    def train(self, n_epochs: int = 50):
        """Full training loop."""
        logger.info(f"🚀 Starting training for {n_epochs} epochs...")
        logger.info(f"   Device: {self.device}")
        logger.info(f"   Model parameters: {sum(p.numel() for p in self.model.parameters()):,}")
        
        for epoch in range(n_epochs):
            start_time = time.time()
            
            # Train
            logger.info(f"📚 Epoch {epoch + 1}/{n_epochs}")
            train_loss = self.train_epoch(epoch)
            
            # Validate
            val_metrics = self.validate()
            
            # Update history
            self.history['train_loss'].append(train_loss)
            self.history['val_loss'].append(val_metrics['loss'])
            self.history['val_mae'].append(val_metrics['mae'])
            self.history['val_bias'].append(val_metrics['bias'])
            self.history['val_scatter'].append(val_metrics['scatter'])
            self.history['val_calibration'].append(val_metrics['calibration'])
            
            # Check if best model
            is_best = val_metrics['mae'] < self.best_val_mae
            if is_best:
                self.best_val_mae = val_metrics['mae']
            
            # Save checkpoint
            self.save_checkpoint(epoch, is_best)
            
            # Print summary
            epoch_time = time.time() - start_time
            logger.info(
                f"📊 Epoch {epoch + 1} | Train: {train_loss:.4f} | "
                f"Val MAE: {val_metrics['mae']:.4f} | "
                f"Val Bias: {val_metrics['bias']:.4f} | "
                f"Val Scatter: {val_metrics['scatter']:.4f} | "
                f"Val Cal: {val_metrics['calibration']:.4f} | "
                f"Time: {epoch_time:.1f}s"
            )
            
            self.epochs_trained = epoch + 1
        
        logger.info(f"✅ Training complete! Best Val MAE: {self.best_val_mae:.4f} Gyr")
        
        return self.history
    
    def test(self) -> Dict[str, float]:
        """Evaluate on test set."""
        logger.info("🧪 Testing on held-out test set...")
        
        # Load best checkpoint
        checkpoint_path = self.checkpoint_dir / 'best.pt'
        if checkpoint_path.exists():
            checkpoint = torch.load(checkpoint_path, map_location=self.device)
            self.model.load_state_dict(checkpoint['model_state_dict'])
            logger.info(f"   Loaded best model from epoch {checkpoint['epoch'] + 1}")
        
        # Evaluate
        metrics = evaluate(self.model, self.test_loader, self.device)
        
        logger.info(
            f"📊 Test Results | MAE: {metrics['mae']:.4f} | "
            f"Bias: {metrics['bias']:.4f} | "
            f"Scatter: {metrics['scatter']:.4f} | "
            f"Calibration: {metrics['calibration']:.4f}"
        )
        
        return metrics


def main():
    """Main training pipeline with CLI arguments."""
    parser = argparse.ArgumentParser(
        description='Train AstroLANNAformer on synthetic galaxy data'
    )
    
    # Data arguments
    parser.add_argument('--n_galaxies', type=int, default=1000,
                        help='Number of synthetic galaxies to generate')
    parser.add_argument('--use_fsps', action='store_true', default=True,
                        help='Use real FSPS stellar population synthesis')
    parser.add_argument('--batch_size', type=int, default=32,
                        help='Batch size for training')
    
    # Model arguments
    parser.add_argument('--sedenion_dim', type=int, default=16,
                        help='Dimension of sedenion space')
    parser.add_argument('--num_heads', type=int, default=4,
                        help='Number of attention heads')
    parser.add_argument('--num_layers', type=int, default=2,
                        help='Number of attention layers')
    parser.add_argument('--dropout', type=float, default=0.1,
                        help='Dropout rate')
    
    # Training arguments
    parser.add_argument('--epochs', type=int, default=50,
                        help='Number of training epochs')
    parser.add_argument('--lr', type=float, default=1e-3,
                        help='Learning rate')
    parser.add_argument('--device', type=str, default='auto',
                        help='Device to use (auto/cpu/cuda)')
    
    # Loss arguments
    parser.add_argument('--age_weight', type=float, default=1.0,
                        help='Weight for age loss')
    parser.add_argument('--uncertainty_weight', type=float, default=0.5,
                        help='Weight for uncertainty loss')
    parser.add_argument('--age_color_weight', type=float, default=0.3,
                        help='Weight for age-color regularization')
    parser.add_argument('--age_mass_weight', type=float, default=0.2,
                        help='Weight for age-mass regularization')
    
    # Other arguments
    parser.add_argument('--seed', type=int, default=42,
                        help='Random seed')
    parser.add_argument('--checkpoint_dir', type=str, default='checkpoints',
                        help='Directory to save checkpoints')
    parser.add_argument('--log_interval', type=int, default=10,
                        help='Logging interval (batches)')
    
    args = parser.parse_args()
    
    # Set random seed
    torch.manual_seed(args.seed)
    
    # Determine device
    if args.device == 'auto':
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
    else:
        device = args.device
    
    logger.info("🌌 AstroLANNAformer Training Pipeline")
    logger.info("=" * 60)
    logger.info(f"Configuration:")
    logger.info(f"  Galaxies: {args.n_galaxies}")
    logger.info(f"  Batch size: {args.batch_size}")
    logger.info(f"  Epochs: {args.epochs}")
    logger.info(f"  Learning rate: {args.lr}")
    logger.info(f"  Device: {device}")
    logger.info(f"  Model: {args.num_layers} layers, {args.num_heads} heads")
    logger.info(f"  FSPS: {args.use_fsps}")
    
    # Step 1: Generate synthetic data
    logger.info("🌌 Step 1: Generating synthetic galaxies...")
    generator = SyntheticGalaxyGenerator(
        n_galaxies=args.n_galaxies,
        seed=args.seed,
        use_fsps=args.use_fsps,
    )
    catalog = generator.generate_catalog(save_path='data/synthetic_galaxies.csv')
    
    # Step 2: Create dataloaders
    logger.info("📊 Step 2: Creating DataLoaders...")
    train_loader, val_loader, test_loader = create_dataloaders(
        catalog,
        batch_size=args.batch_size,
        train_frac=0.8,
        val_frac=0.1,
        use_spectroscopy=True,
        use_morphology=True,
    )
    
    # Step 3: Create model
    logger.info("🧠 Step 3: Creating AstroLANNAformer...")
    model = AstroLANNAformer(
        n_photometry_bands=8,
        n_spectroscopy_bins=1000,
        n_morphology_features=3,
        sedenion_dim=args.sedenion_dim,
        num_heads=args.num_heads,
        num_layers=args.num_layers,
        dropout=args.dropout,
        use_mlp=True,
        max_age=13.8,
    )
    logger.info(f"   Model parameters: {sum(p.numel() for p in model.parameters()):,}")
    
    # Step 4: Create optimizer and loss
    optimizer = optim.Adam(model.parameters(), lr=args.lr)
    loss_fn = AstroPhysicsLoss(
        age_weight=args.age_weight,
        uncertainty_weight=args.uncertainty_weight,
        age_color_weight=args.age_color_weight,
        age_mass_weight=args.age_mass_weight,
    )
    logger.info("⚙️ Optimizer and loss function created")
    
    # Step 5: Train
    logger.info("🚀 Step 4: Training...")
    logger.info("=" * 60)
    
    trainer = Trainer(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        test_loader=test_loader,
        optimizer=optimizer,
        loss_fn=loss_fn,
        device=device,
        checkpoint_dir=args.checkpoint_dir,
        log_interval=args.log_interval,
    )
    
    history = trainer.train(n_epochs=args.epochs)
    
    # Step 6: Test
    logger.info("=" * 60)
    test_metrics = trainer.test()
    
    # Step 7: Save results
    logger.info("💾 Saving results...")
    results = {
        'config': vars(args),
        'history': history,
        'test_metrics': test_metrics,
    }
    
    with open('data/training_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    logger.info("   Results saved to data/training_results.json")
    
    logger.info("=" * 60)
    logger.info("💜 Training complete!")
    logger.info("🍩 'From synthetic galaxies to real cosmology!'")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

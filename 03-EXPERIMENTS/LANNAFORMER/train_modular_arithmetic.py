"""
Train LANNAformer on Modular Arithmetic

Replicate the grokking phenomenon and WATCH it happen in 16D space!

This script trains a minimal LANNAformer on modular addition and tracks:
1. Training/test accuracy (standard metrics)
2. 16D coordinate evolution (geometric metrics)
3. Attention pattern convergence (determinism tests)
4. Phase transition indicators (grokking detection)

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: January 25, 2026
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
from tqdm import tqdm

from lannaformer_minimal import LANNAformer, PRIMES_16D, CONSCIOUSNESS_AXES


class ModularArithmeticDataset(Dataset):
    """
    Dataset for modular addition: (a + b) mod p
    
    Args:
        modulus: Prime modulus (default: 97)
        train: Whether this is training set (True) or test set (False)
        train_fraction: Fraction of data to use for training
    """
    
    def __init__(self, modulus: int = 97, train: bool = True, train_fraction: float = 0.5):
        self.modulus = modulus
        
        # Generate all possible pairs
        all_pairs = []
        for a in range(modulus):
            for b in range(modulus):
                result = (a + b) % modulus
                all_pairs.append((a, b, result))
        
        # Shuffle deterministically
        np.random.seed(42)
        np.random.shuffle(all_pairs)
        
        # Split train/test
        split_idx = int(len(all_pairs) * train_fraction)
        if train:
            self.pairs = all_pairs[:split_idx]
        else:
            self.pairs = all_pairs[split_idx:]
    
    def __len__(self):
        return len(self.pairs)
    
    def __getitem__(self, idx):
        a, b, result = self.pairs[idx]
        return torch.tensor(a), torch.tensor(b), torch.tensor(result)


class GrokkingTracker:
    """
    Track metrics during training to detect and analyze grokking.
    """
    
    def __init__(self, save_dir: str = "grokking_results"):
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(exist_ok=True)
        
        # Standard metrics
        self.train_losses = []
        self.train_accs = []
        self.test_losses = []
        self.test_accs = []
        
        # Geometric metrics
        self.coord_entropies = []
        self.dimensional_alignments = []
        self.attention_sharpness = []
        
        # Grokking detection
        self.grokking_epoch = None
        self.grokking_detected = False
    
    def update(
        self,
        epoch: int,
        train_loss: float,
        train_acc: float,
        test_loss: float,
        test_acc: float,
        coords: torch.Tensor,
        attention_weights: torch.Tensor
    ):
        """Update all metrics"""
        
        # Standard metrics
        self.train_losses.append(train_loss)
        self.train_accs.append(train_acc)
        self.test_losses.append(test_loss)
        self.test_accs.append(test_acc)
        
        # Geometric metrics
        entropy = self._calculate_entropy(coords)
        alignment = self._calculate_dimensional_alignment(coords)
        sharpness = self._calculate_attention_sharpness(attention_weights)
        
        self.coord_entropies.append(entropy)
        self.dimensional_alignments.append(alignment)
        self.attention_sharpness.append(sharpness)
        
        # Detect grokking (sudden test accuracy jump)
        if not self.grokking_detected and test_acc > 0.95 and len(self.test_accs) > 10:
            if self.test_accs[-10] < 0.5:  # Was low recently
                self.grokking_epoch = epoch
                self.grokking_detected = True
                print(f"\n🌟 GROKKING DETECTED AT EPOCH {epoch}! 🌟\n")
    
    def _calculate_entropy(self, coords: torch.Tensor) -> float:
        """Calculate entropy of 16D coordinates (measure of chaos)"""
        # Normalize to probabilities
        probs = torch.abs(coords).mean(dim=0)
        probs = probs / probs.sum()
        
        # Calculate entropy
        entropy = -(probs * torch.log(probs + 1e-10)).sum().item()
        return entropy
    
    def _calculate_dimensional_alignment(self, coords: torch.Tensor) -> float:
        """Calculate how aligned coordinates are with prime basis"""
        # Measure sparsity (aligned = sparse, few dimensions active)
        l1_norm = torch.abs(coords).mean(dim=0).sum().item()
        l2_norm = torch.norm(coords.mean(dim=0)).item()
        
        # Alignment = l1/l2 ratio (higher = more aligned)
        alignment = l1_norm / (l2_norm + 1e-10)
        return alignment
    
    def _calculate_attention_sharpness(self, attention_weights: torch.Tensor) -> float:
        """Calculate how sharp/focused attention is"""
        # Entropy of attention distribution (lower = sharper)
        probs = attention_weights.mean(dim=(0, 1, 2))  # Average over batch, heads, queries
        entropy = -(probs * torch.log(probs + 1e-10)).sum().item()
        
        # Sharpness = inverse entropy
        sharpness = 1.0 / (entropy + 1e-10)
        return sharpness
    
    def save_results(self, filename: str = "grokking_results.json"):
        """Save all metrics to JSON"""
        results = {
            "train_losses": self.train_losses,
            "train_accs": self.train_accs,
            "test_losses": self.test_losses,
            "test_accs": self.test_accs,
            "coord_entropies": self.coord_entropies,
            "dimensional_alignments": self.dimensional_alignments,
            "attention_sharpness": self.attention_sharpness,
            "grokking_epoch": self.grokking_epoch,
            "grokking_detected": self.grokking_detected
        }
        
        filepath = self.save_dir / filename
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"💾 Results saved to {filepath}")
    
    def plot_results(self, filename: str = "grokking_plots.png"):
        """Plot all metrics"""
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        
        # Training curves
        axes[0, 0].plot(self.train_losses, label='Train')
        axes[0, 0].plot(self.test_losses, label='Test')
        axes[0, 0].set_title('Loss')
        axes[0, 0].set_xlabel('Epoch')
        axes[0, 0].legend()
        if self.grokking_epoch:
            axes[0, 0].axvline(self.grokking_epoch, color='red', linestyle='--', label='Grokking')
        
        axes[0, 1].plot(self.train_accs, label='Train')
        axes[0, 1].plot(self.test_accs, label='Test')
        axes[0, 1].set_title('Accuracy')
        axes[0, 1].set_xlabel('Epoch')
        axes[0, 1].legend()
        if self.grokking_epoch:
            axes[0, 1].axvline(self.grokking_epoch, color='red', linestyle='--', label='Grokking')
        
        # Geometric metrics
        axes[0, 2].plot(self.coord_entropies)
        axes[0, 2].set_title('Coordinate Entropy (Chaos)')
        axes[0, 2].set_xlabel('Epoch')
        if self.grokking_epoch:
            axes[0, 2].axvline(self.grokking_epoch, color='red', linestyle='--')
        
        axes[1, 0].plot(self.dimensional_alignments)
        axes[1, 0].set_title('Dimensional Alignment')
        axes[1, 0].set_xlabel('Epoch')
        if self.grokking_epoch:
            axes[1, 0].axvline(self.grokking_epoch, color='red', linestyle='--')
        
        axes[1, 1].plot(self.attention_sharpness)
        axes[1, 1].set_title('Attention Sharpness')
        axes[1, 1].set_xlabel('Epoch')
        if self.grokking_epoch:
            axes[1, 1].axvline(self.grokking_epoch, color='red', linestyle='--')
        
        # Summary text
        summary_text = f"""
        Grokking Detected: {self.grokking_detected}
        Grokking Epoch: {self.grokking_epoch if self.grokking_epoch else 'N/A'}
        
        Final Train Acc: {self.train_accs[-1]:.3f}
        Final Test Acc: {self.test_accs[-1]:.3f}
        
        Final Entropy: {self.coord_entropies[-1]:.3f}
        Final Alignment: {self.dimensional_alignments[-1]:.3f}
        Final Sharpness: {self.attention_sharpness[-1]:.3f}
        """
        axes[1, 2].text(0.1, 0.5, summary_text, fontsize=10, verticalalignment='center')
        axes[1, 2].axis('off')
        
        plt.tight_layout()
        filepath = self.save_dir / filename
        plt.savefig(filepath, dpi=150)
        print(f"📊 Plots saved to {filepath}")


def train_epoch(
    model: LANNAformer,
    dataloader: DataLoader,
    optimizer: optim.Optimizer,
    device: str = 'cpu'
) -> Tuple[float, float, torch.Tensor, torch.Tensor]:
    """Train for one epoch"""
    model.train()
    total_loss = 0
    correct = 0
    total = 0
    
    all_coords = []
    all_attention = []
    
    for a, b, target in dataloader:
        a, b, target = a.to(device), b.to(device), target.to(device)
        
        optimizer.zero_grad()
        
        # Forward pass
        pred, coords, attention_weights = model(a, b, return_coords=True, return_attention=True)
        
        # Loss (cross-entropy)
        loss = nn.functional.cross_entropy(
            pred.unsqueeze(0).float(),
            target.unsqueeze(0)
        )
        
        # Backward pass
        loss.backward()
        optimizer.step()
        
        # Metrics
        total_loss += loss.item()
        correct += (pred == target).sum().item()
        total += len(target)
        
        # Collect for analysis
        all_coords.append(coords.detach())
        all_attention.append(attention_weights[0].detach())  # First layer
    
    avg_loss = total_loss / len(dataloader)
    accuracy = correct / total
    
    # Concatenate all coords and attention
    all_coords = torch.cat(all_coords, dim=0)
    all_attention = torch.cat(all_attention, dim=0)
    
    return avg_loss, accuracy, all_coords, all_attention


@torch.no_grad()
def evaluate(
    model: LANNAformer,
    dataloader: DataLoader,
    device: str = 'cpu'
) -> Tuple[float, float, torch.Tensor, torch.Tensor]:
    """Evaluate on test set"""
    model.eval()
    total_loss = 0
    correct = 0
    total = 0
    
    all_coords = []
    all_attention = []
    
    for a, b, target in dataloader:
        a, b, target = a.to(device), b.to(device), target.to(device)
        
        # Forward pass
        pred, coords, attention_weights = model(a, b, return_coords=True, return_attention=True)
        
        # Loss
        loss = nn.functional.cross_entropy(
            pred.unsqueeze(0).float(),
            target.unsqueeze(0)
        )
        
        # Metrics
        total_loss += loss.item()
        correct += (pred == target).sum().item()
        total += len(target)
        
        # Collect for analysis
        all_coords.append(coords.detach())
        all_attention.append(attention_weights[0].detach())
    
    avg_loss = total_loss / len(dataloader)
    accuracy = correct / total
    
    all_coords = torch.cat(all_coords, dim=0)
    all_attention = torch.cat(all_attention, dim=0)
    
    return avg_loss, accuracy, all_coords, all_attention


def main():
    """Main training loop"""
    print("🌌 Training LANNAformer on Modular Arithmetic")
    print("=" * 60)
    print()
    
    # Hyperparameters
    MODULUS = 97
    BATCH_SIZE = 128
    NUM_EPOCHS = 10000  # Need many epochs to see grokking!
    LEARNING_RATE = 1e-3
    WEIGHT_DECAY = 1e-4
    
    # Device
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Device: {device}")
    print()
    
    # Create datasets
    print("📊 Creating datasets...")
    train_dataset = ModularArithmeticDataset(modulus=MODULUS, train=True, train_fraction=0.5)
    test_dataset = ModularArithmeticDataset(modulus=MODULUS, train=False, train_fraction=0.5)
    
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)
    
    print(f"Train samples: {len(train_dataset)}")
    print(f"Test samples: {len(test_dataset)}")
    print()
    
    # Create model
    print("🧠 Creating LANNAformer...")
    model = LANNAformer(
        modulus=MODULUS,
        num_heads=4,
        num_layers=2,
        dropout=0.1,
        use_mlp=True
    ).to(device)
    
    # Count parameters
    num_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"Parameters: {num_params:,}")
    print()
    
    # Optimizer
    optimizer = optim.AdamW(model.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY)
    
    # Tracker
    tracker = GrokkingTracker(save_dir=f"grokking_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    
    # Training loop
    print("🚀 Starting training...")
    print("=" * 60)
    print()
    
    for epoch in tqdm(range(NUM_EPOCHS), desc="Training"):
        # Train
        train_loss, train_acc, train_coords, train_attention = train_epoch(
            model, train_loader, optimizer, device
        )
        
        # Evaluate
        test_loss, test_acc, test_coords, test_attention = evaluate(
            model, test_loader, device
        )
        
        # Update tracker
        tracker.update(
            epoch=epoch,
            train_loss=train_loss,
            train_acc=train_acc,
            test_loss=test_loss,
            test_acc=test_acc,
            coords=test_coords,
            attention_weights=test_attention
        )
        
        # Print progress
        if epoch % 100 == 0:
            print(f"\nEpoch {epoch:5d} | "
                  f"Train: {train_acc:.3f} | "
                  f"Test: {test_acc:.3f} | "
                  f"Entropy: {tracker.coord_entropies[-1]:.3f}")
    
    print()
    print("=" * 60)
    print("✨ Training complete!")
    print()
    
    # Save results
    tracker.save_results()
    tracker.plot_results()
    
    # Save model
    model_path = tracker.save_dir / "lannaformer_final.pt"
    torch.save(model.state_dict(), model_path)
    print(f"💾 Model saved to {model_path}")
    
    print()
    print("=" * 60)
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🍩 'Grokking is just finding the bagels!'")


if __name__ == "__main__":
    main()

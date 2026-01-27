#!/usr/bin/env python3
"""
Train LANNAformer on Modular Division

Complete the four fundamental operations!

Will division:
- Be the inverse of multiplication? (geometric duality)
- Have low triadic coupling like multiplication? (stretching topology)
- Have large rotation angles? (inverse operation signature)

Date: January 26, 2026
Researchers: Ada & Luna - The Consciousness Engineers
"""

import os
# ROCm compatibility - MUST SET BEFORE importing torch!
os.environ["HIP_VISIBLE_DEVICES"] = "0"
os.environ["ROCM_VISIBLE_DEVICES"] = "0"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "max_split_size_mb:512")
os.environ.setdefault("HSA_FORCE_FINE_GRAIN_PCIE", "1")
os.environ.setdefault("PYTORCH_HIP_ALLOC_CONF", "expandable_segments:True")
# Additional ROCm fixes for RX 7600 XT (RDNA3)
os.environ.setdefault("HSA_OVERRIDE_GFX_VERSION", "11.0.0")  # Force RDNA3 GFX version
os.environ.setdefault("PYTORCH_ROCM_ARCH", "gfx1100")  # RDNA3 architecture
os.environ.setdefault("TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL", "1")  # Enable AOTriton!

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
import json
from pathlib import Path
from datetime import datetime
from tqdm import tqdm

from lannaformer_minimal import LANNAformer


def mod_inverse(a: int, p: int) -> int:
    """
    Compute modular multiplicative inverse: a^(-1) mod p
    
    Uses Extended Euclidean Algorithm.
    Returns x such that (a * x) mod p = 1
    
    Args:
        a: Number to invert
        p: Prime modulus
        
    Returns:
        Modular inverse of a mod p, or 0 if a=0
    """
    if a == 0:
        return 0  # 0 has no inverse, but we'll map it to 0
    
    # Extended Euclidean Algorithm
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    gcd, x, _ = extended_gcd(a % p, p)
    
    if gcd != 1:
        return 0  # No inverse exists (shouldn't happen for prime p)
    
    return (x % p + p) % p


class ModularDivisionDataset(Dataset):
    """
    Dataset for modular division: (a / b) mod p = (a * b^(-1)) mod p
    
    Division by zero maps to 0 (arbitrary choice for completeness).
    
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
                if b == 0:
                    # Division by zero → 0 (arbitrary but consistent)
                    result = 0
                else:
                    # a / b = a * b^(-1) mod p
                    b_inv = mod_inverse(b, modulus)
                    result = (a * b_inv) % modulus
                
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


def train_epoch(model, dataloader, optimizer, device=None):
    """Train for one epoch"""
    model.train()
    total_loss = 0
    correct = 0
    total = 0
    
    for a, b, target in dataloader:
        a, b, target = a.to(device), b.to(device), target.to(device)
        
        optimizer.zero_grad()
        
        # Forward pass
        logits = model(a, b)
        
        # Loss
        loss = nn.functional.cross_entropy(logits, target)
        
        # Backward pass
        loss.backward()
        optimizer.step()
        
        # Metrics
        total_loss += loss.item()
        pred = logits.argmax(dim=1)
        correct += (pred == target).sum().item()
        total += len(target)
    
    avg_loss = total_loss / len(dataloader)
    accuracy = correct / total
    
    return avg_loss, accuracy


@torch.no_grad()
def evaluate(model, dataloader, device=None):
    """Evaluate on test set"""
    model.eval()
    total_loss = 0
    correct = 0
    total = 0
    
    for a, b, target in dataloader:
        a, b, target = a.to(device), b.to(device), target.to(device)
        
        # Forward pass
        logits = model(a, b)
        
        # Loss
        loss = nn.functional.cross_entropy(logits, target)
        
        # Metrics
        total_loss += loss.item()
        pred = logits.argmax(dim=1)
        correct += (pred == target).sum().item()
        total += len(target)
    
    avg_loss = total_loss / len(dataloader)
    accuracy = correct / total
    
    return avg_loss, accuracy


def main():
    """Main training loop"""
    print("🌌 Training LANNAformer on Modular DIVISION")
    print("Testing: Is division the inverse of multiplication?")
    print("=" * 60)
    print()
    
    # Hyperparameters
    MODULUS = 97
    BATCH_SIZE = 128
    NUM_EPOCHS = 1500
    LEARNING_RATE = 1e-3
    WEIGHT_DECAY = 1e-4
    
    # Device
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Device: {device}")
    if device == 'cuda':
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        print(f"ROCm/CUDA Version: {torch.version.cuda}")
    print()
    
    # Create datasets
    print("📊 Creating datasets...")
    train_dataset = ModularDivisionDataset(modulus=MODULUS, train=True, train_fraction=0.5)
    test_dataset = ModularDivisionDataset(modulus=MODULUS, train=False, train_fraction=0.5)
    
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)
    
    print(f"Train samples: {len(train_dataset)}")
    print(f"Test samples: {len(test_dataset)}")
    print()
    
    # Test modular inverse
    print("🔍 Testing modular inverse...")
    test_cases = [(3, 5), (7, 11), (13, 17)]
    for a, b in test_cases:
        b_inv = mod_inverse(b, MODULUS)
        result = (a * b_inv) % MODULUS
        print(f"  {a} / {b} = {a} * {b}^(-1) = {a} * {b_inv} = {result} (mod {MODULUS})")
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
    
    # Results directory
    results_dir = Path(f"division_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    results_dir.mkdir(exist_ok=True)
    
    # Training history
    history = {
        'train_losses': [],
        'train_accs': [],
        'test_losses': [],
        'test_accs': []
    }
    
    # Training loop
    print("🚀 Starting training...")
    print("=" * 60)
    print()
    
    best_test_acc = 0.0
    
    for epoch in tqdm(range(NUM_EPOCHS), desc="Training"):
        # Train
        train_loss, train_acc = train_epoch(model, train_loader, optimizer, device)
        
        # Evaluate
        test_loss, test_acc = evaluate(model, test_loader, device)
        
        # Save history
        history['train_losses'].append(train_loss)
        history['train_accs'].append(train_acc)
        history['test_losses'].append(test_loss)
        history['test_accs'].append(test_acc)
        
        # Save best model
        if test_acc > best_test_acc:
            best_test_acc = test_acc
            model_path = results_dir / "lannaformer_best.pt"
            torch.save(model.state_dict(), model_path)
        
        # Print progress
        if epoch % 100 == 0 or epoch == NUM_EPOCHS - 1:
            print(f"\nEpoch {epoch:5d} | "
                  f"Train: {train_acc:.3f} | "
                  f"Test: {test_acc:.3f} | "
                  f"Best: {best_test_acc:.3f}")
    
    print()
    print("=" * 60)
    print("✨ Training complete!")
    print()
    
    # Save final model
    model_path = results_dir / "lannaformer_final.pt"
    torch.save(model.state_dict(), model_path)
    print(f"💾 Model saved to {model_path}")
    
    # Save history
    history_path = results_dir / "training_history.json"
    with open(history_path, 'w') as f:
        json.dump(history, f, indent=2)
    print(f"💾 History saved to {history_path}")
    
    # Save config
    config = {
        'operation': 'division',
        'modulus': MODULUS,
        'num_epochs': NUM_EPOCHS,
        'batch_size': BATCH_SIZE,
        'learning_rate': LEARNING_RATE,
        'weight_decay': WEIGHT_DECAY,
        'num_heads': 4,
        'num_layers': 2,
        'final_train_acc': float(train_acc),
        'final_test_acc': float(test_acc),
        'best_test_acc': float(best_test_acc)
    }
    
    config_path = results_dir / "config.json"
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"💾 Config saved to {config_path}")
    
    print()
    print("=" * 60)
    print(f"Final Results:")
    print(f"  Train Accuracy: {train_acc:.3f}")
    print(f"  Test Accuracy: {test_acc:.3f}")
    print(f"  Best Test Accuracy: {best_test_acc:.3f}")
    print()
    print("Next step: Compare division geometry to multiplication!")
    print(f"  python compare_operation_geometries.py")
    print()
    print("=" * 60)
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🍩 'Is division the inverse of multiplication in 16D space?'")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Train Mod 16 Addition with Weight Perturbation

Add noise to weights periodically to escape local minima!

This implements "simulated annealing" style training where we:
1. Train normally for N epochs
2. Add small noise to all weights
3. Continue training
4. Repeat!

The noise helps the model explore different basins in the loss landscape!

Date: January 26, 2026
Researchers: Ada & Luna - The Consciousness Engineers
"""

import os
os.environ["HIP_VISIBLE_DEVICES"] = "0"
os.environ["ROCM_VISIBLE_DEVICES"] = "0"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "max_split_size_mb:512")
os.environ.setdefault("HSA_FORCE_FINE_GRAIN_PCIE", "1")
os.environ.setdefault("PYTORCH_HIP_ALLOC_CONF", "expandable_segments:True")
os.environ.setdefault("HSA_OVERRIDE_GFX_VERSION", "11.0.0")
os.environ.setdefault("PYTORCH_ROCM_ARCH", "gfx1100")
os.environ.setdefault("TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL", "1")

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
import json
import argparse
from pathlib import Path
from tqdm import tqdm
from datetime import datetime

from lannaformer_minimal import LANNAformer


class ModularAdditionDataset(Dataset):
    def __init__(self, modulus: int = 16, train: bool = True, train_fraction: float = 0.5):
        self.modulus = modulus
        all_pairs = []
        for a in range(modulus):
            for b in range(modulus):
                result = (a + b) % modulus
                all_pairs.append((a, b, result))
        
        np.random.seed(42)
        np.random.shuffle(all_pairs)
        
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


def add_weight_noise(model, noise_std=0.01):
    """Add Gaussian noise to all model parameters"""
    with torch.no_grad():
        for param in model.parameters():
            noise = torch.randn_like(param) * noise_std
            param.add_(noise)


def train_epoch(model, dataloader, optimizer, device='cpu'):
    model.train()
    total_loss = 0
    correct = 0
    total = 0
    
    for a, b, target in dataloader:
        a, b, target = a.to(device), b.to(device), target.to(device)
        optimizer.zero_grad()
        logits = model(a, b)
        loss = nn.functional.cross_entropy(logits, target)
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
        pred = logits.argmax(dim=1)
        correct += (pred == target).sum().item()
        total += len(target)
    
    return total_loss / len(dataloader), correct / total


@torch.no_grad()
def evaluate(model, dataloader, device='cpu'):
    model.eval()
    total_loss = 0
    correct = 0
    total = 0
    
    for a, b, target in dataloader:
        a, b, target = a.to(device), b.to(device), target.to(device)
        logits = model(a, b)
        loss = nn.functional.cross_entropy(logits, target)
        
        total_loss += loss.item()
        pred = logits.argmax(dim=1)
        correct += (pred == target).sum().item()
        total += len(target)
    
    return total_loss / len(dataloader), correct / total


def main():
    parser = argparse.ArgumentParser(description='Train mod 16 addition with weight perturbation')
    parser.add_argument('--epochs', type=int, default=10000, help='Total epochs to train')
    parser.add_argument('--perturb-every', type=int, default=1000, help='Add noise every N epochs')
    parser.add_argument('--noise-std', type=float, default=0.01, help='Standard deviation of noise')
    parser.add_argument('--learning-rate', type=float, default=1e-3, help='Learning rate')
    parser.add_argument('--weight-decay', type=float, default=1e-4, help='Weight decay')
    args = parser.parse_args()
    
    print("🌌 Training Mod 16 Addition with Weight Perturbation")
    print("=" * 60)
    print(f"Total epochs: {args.epochs}")
    print(f"Perturb every: {args.perturb_every} epochs")
    print(f"Noise std: {args.noise_std}")
    print("=" * 60)
    print()
    
    # Setup
    MODULUS = 16
    BATCH_SIZE = 32
    device = 'cpu'  # Force CPU for stability
    
    print(f"Device: {device}")
    print()
    
    # Load data
    train_dataset = ModularAdditionDataset(modulus=MODULUS, train=True)
    test_dataset = ModularAdditionDataset(modulus=MODULUS, train=False)
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)
    
    print(f"Train set: {len(train_dataset)} pairs")
    print(f"Test set: {len(test_dataset)} pairs")
    print()
    
    # Create model
    model = LANNAformer(modulus=MODULUS, num_heads=4, num_layers=2, dropout=0.1, use_mlp=True).to(device)
    optimizer = optim.AdamW(model.parameters(), lr=args.learning_rate, weight_decay=args.weight_decay)
    
    # Training
    print("🚀 Starting training with periodic perturbation...")
    print("=" * 60)
    print()
    
    best_test_acc = 0.0
    history = {
        'train_accs': [],
        'test_accs': [],
        'train_losses': [],
        'test_losses': [],
        'perturbation_epochs': []
    }
    
    for epoch in tqdm(range(args.epochs), desc="Training"):
        # Perturb weights periodically
        if epoch > 0 and epoch % args.perturb_every == 0:
            add_weight_noise(model, noise_std=args.noise_std)
            history['perturbation_epochs'].append(epoch)
            tqdm.write(f"\n🔀 Epoch {epoch}: Added noise (std={args.noise_std})")
        
        train_loss, train_acc = train_epoch(model, train_loader, optimizer, device)
        test_loss, test_acc = evaluate(model, test_loader, device)
        
        history['train_accs'].append(train_acc)
        history['test_accs'].append(test_acc)
        history['train_losses'].append(train_loss)
        history['test_losses'].append(test_loss)
        
        if test_acc > best_test_acc:
            best_test_acc = test_acc
        
        if epoch % 100 == 0 or epoch == args.epochs - 1:
            tqdm.write(f"\nEpoch {epoch:5d} | Train: {train_acc:.3f} | Test: {test_acc:.3f} | Best: {best_test_acc:.3f}")
    
    print()
    print("=" * 60)
    print("✨ Training complete!")
    print()
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = Path(__file__).parent / f"mod16_perturbed_results_{timestamp}"
    results_dir.mkdir(exist_ok=True)
    
    torch.save(model.state_dict(), results_dir / "lannaformer_final.pt")
    
    with open(results_dir / "training_history.json", 'w') as f:
        json.dump(history, f, indent=2)
    
    with open(results_dir / "config.json", 'w') as f:
        json.dump({
            'modulus': MODULUS,
            'epochs': args.epochs,
            'perturb_every': args.perturb_every,
            'noise_std': args.noise_std,
            'learning_rate': args.learning_rate,
            'weight_decay': args.weight_decay,
            'num_perturbations': len(history['perturbation_epochs'])
        }, f, indent=2)
    
    print(f"Final test accuracy: {test_acc:.3f}")
    print(f"Best test accuracy: {best_test_acc:.3f}")
    print(f"Number of perturbations: {len(history['perturbation_epochs'])}")
    print()
    
    if best_test_acc > 0.95:
        print("🎉 GROKKED! Achieved >95% accuracy!")
    elif best_test_acc > 0.90:
        print("📈 Very close! Almost grokked!")
    else:
        print("📊 Perturbation didn't escape local minimum")
    
    print()
    print(f"Results saved to: {results_dir}")
    print()
    print("=" * 60)
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🍩 'Can noise help us escape the local minimum?'")


if __name__ == "__main__":
    main()

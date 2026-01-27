#!/usr/bin/env python3
"""
Train Mod 16 Addition with 16 Heads × 3 Layers

Testing if matching heads to dimensions unlocks full capacity!

Architecture:
- 16 heads (one per sedenion dimension!)
- 3 layers (separate → combine → refine)
- 16D sedenion space (fixed by geometry)

Hypothesis: Each head can specialize in one dimension, and 3 layers
gives enough depth to fully learn the geometric transformation!

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
    parser = argparse.ArgumentParser(description='Train mod 16 addition with 16 heads × 3 layers')
    parser.add_argument('--epochs', type=int, default=5000, help='Number of epochs to train')
    parser.add_argument('--learning-rate', type=float, default=1e-3, help='Learning rate')
    parser.add_argument('--weight-decay', type=float, default=1e-4, help='Weight decay')
    parser.add_argument('--batch-size', type=int, default=32, help='Batch size')
    args = parser.parse_args()
    
    print("🌌 Training Mod 16 Addition with 16 Heads × 3 Layers")
    print("=" * 60)
    print("Architecture:")
    print("  - 16 heads (one per sedenion dimension!)")
    print("  - 3 layers (separate → combine → refine)")
    print("  - 16D sedenion space")
    print()
    print(f"Training for {args.epochs} epochs")
    print("=" * 60)
    print()
    
    # Setup
    MODULUS = 16
    NUM_HEADS = 16  # Match dimensions!
    NUM_LAYERS = 3  # Three-step transformation
    device = 'cpu'  # Force CPU for stability
    
    print(f"Device: {device}")
    print()
    
    # Load data
    train_dataset = ModularAdditionDataset(modulus=MODULUS, train=True)
    test_dataset = ModularAdditionDataset(modulus=MODULUS, train=False)
    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=args.batch_size, shuffle=False)
    
    print(f"Train set: {len(train_dataset)} pairs")
    print(f"Test set: {len(test_dataset)} pairs")
    print()
    
    # Create model with expanded architecture
    print("Creating model...")
    model = LANNAformer(
        modulus=MODULUS,
        num_heads=NUM_HEADS,
        num_layers=NUM_LAYERS,
        dropout=0.1,
        use_mlp=True
    ).to(device)
    
    # Count parameters
    total_params = sum(p.numel() for p in model.parameters())
    print(f"Total parameters: {total_params:,}")
    print()
    
    optimizer = optim.AdamW(model.parameters(), lr=args.learning_rate, weight_decay=args.weight_decay)
    
    # Training
    print("🚀 Starting training...")
    print("=" * 60)
    print()
    
    best_test_acc = 0.0
    best_epoch = 0
    history = {
        'train_accs': [],
        'test_accs': [],
        'train_losses': [],
        'test_losses': []
    }
    
    for epoch in tqdm(range(args.epochs), desc="Training"):
        train_loss, train_acc = train_epoch(model, train_loader, optimizer, device)
        test_loss, test_acc = evaluate(model, test_loader, device)
        
        history['train_accs'].append(train_acc)
        history['test_accs'].append(test_acc)
        history['train_losses'].append(train_loss)
        history['test_losses'].append(test_loss)
        
        if test_acc > best_test_acc:
            best_test_acc = test_acc
            best_epoch = epoch
        
        if epoch % 100 == 0 or epoch == args.epochs - 1:
            tqdm.write(f"\nEpoch {epoch:5d} | Train: {train_acc:.3f} | Test: {test_acc:.3f} | Best: {best_test_acc:.3f} (epoch {best_epoch})")
    
    print()
    print("=" * 60)
    print("✨ Training complete!")
    print()
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = Path(__file__).parent / f"mod16_16h3l_results_{timestamp}"
    results_dir.mkdir(exist_ok=True)
    
    torch.save(model.state_dict(), results_dir / "lannaformer_final.pt")
    
    with open(results_dir / "training_history.json", 'w') as f:
        json.dump(history, f, indent=2)
    
    with open(results_dir / "config.json", 'w') as f:
        json.dump({
            'modulus': MODULUS,
            'num_heads': NUM_HEADS,
            'num_layers': NUM_LAYERS,
            'epochs': args.epochs,
            'learning_rate': args.learning_rate,
            'weight_decay': args.weight_decay,
            'batch_size': args.batch_size,
            'total_params': total_params,
            'best_epoch': best_epoch,
            'best_test_acc': float(best_test_acc)
        }, f, indent=2)
    
    print(f"Final test accuracy: {test_acc:.3f}")
    print(f"Best test accuracy: {best_test_acc:.3f} (epoch {best_epoch})")
    print(f"Total parameters: {total_params:,}")
    print()
    
    if best_test_acc > 0.95:
        print("🎉 GROKKED! Achieved >95% accuracy!")
        print("✨ 16 heads × 3 layers was the key!")
    elif best_test_acc > 0.90:
        print("📈 Very close! Almost grokked!")
        print("🤔 Maybe needs more epochs or different hyperparams?")
    else:
        print("📊 Interesting! More capacity didn't break the plateau")
        print("💡 The 89% limit might be fundamental to this setup")
    
    print()
    print(f"Results saved to: {results_dir}")
    print()
    print("=" * 60)
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🍩 'Does matching heads to dimensions unlock full capacity?'")


if __name__ == "__main__":
    main()

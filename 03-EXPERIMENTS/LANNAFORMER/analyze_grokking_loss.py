#!/usr/bin/env python3
"""
Analyze Grokking Loss Curves

Compute train vs test loss to see if we're seeing grokking dynamics!

The grokking signature:
1. Train loss drops quickly (memorization)
2. Test loss stays high (not generalizing)
3. Then test loss suddenly drops (grokking!)

Date: January 26, 2026
Researchers: Ada & Luna - The Consciousness Engineers
"""

import os
os.environ["HIP_VISIBLE_DEVICES"] = "0"
os.environ["ROCM_VISIBLE_DEVICES"] = "0"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import numpy as np
import json
from pathlib import Path

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


@torch.no_grad()
def compute_loss_and_accuracy(model, dataloader, device='cpu'):
    """Compute both loss and accuracy"""
    model.eval()
    total_loss = 0
    correct = 0
    total = 0
    
    for a, b, target in dataloader:
        a, b, target = a.to(device), b.to(device), target.to(device)
        logits = model(a, b)
        loss = nn.functional.cross_entropy(logits, target)
        
        total_loss += loss.item() * len(target)  # Weighted by batch size
        pred = logits.argmax(dim=1)
        correct += (pred == target).sum().item()
        total += len(target)
    
    return total_loss / total, correct / total


def main():
    print("🔬 Analyzing Grokking Loss Curves")
    print("=" * 60)
    print()
    
    # Find checkpoint
    base_dir = Path(__file__).parent
    checkpoint_dirs = list(base_dir.glob('mod16_addition_results_*'))
    if not checkpoint_dirs:
        print("✗ No checkpoint found!")
        return
    
    checkpoint_dir = sorted(checkpoint_dirs)[-1]
    
    # Try best checkpoint first
    checkpoint_paths = [
        checkpoint_dir / 'lannaformer_continued_best.pt',
        checkpoint_dir / 'lannaformer_final.pt'
    ]
    
    checkpoint_path = None
    for path in checkpoint_paths:
        if path.exists():
            checkpoint_path = path
            break
    
    if not checkpoint_path:
        print("✗ No checkpoint found!")
        return
    
    print(f"Loading: {checkpoint_path.name}")
    print()
    
    # Setup
    MODULUS = 16
    BATCH_SIZE = 32
    device = 'cpu'  # Force CPU for analysis (ROCm kernel issues)
    
    # Load data
    train_dataset = ModularAdditionDataset(modulus=MODULUS, train=True)
    test_dataset = ModularAdditionDataset(modulus=MODULUS, train=False)
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)
    
    print(f"Train set: {len(train_dataset)} pairs")
    print(f"Test set: {len(test_dataset)} pairs")
    print()
    
    # Load model
    model = LANNAformer(modulus=MODULUS, num_heads=4, num_layers=2, dropout=0.1, use_mlp=True).to(device)
    checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=False)
    model.load_state_dict(checkpoint)
    
    # Compute losses
    print("Computing losses...")
    train_loss, train_acc = compute_loss_and_accuracy(model, train_loader, device)
    test_loss, test_acc = compute_loss_and_accuracy(model, test_loader, device)
    
    print()
    print("=" * 60)
    print("📊 GROKKING ANALYSIS")
    print("=" * 60)
    print()
    print(f"Train Loss: {train_loss:.4f}  |  Train Acc: {train_acc:.3f}")
    print(f"Test Loss:  {test_loss:.4f}  |  Test Acc:  {test_acc:.3f}")
    print()
    print(f"Loss Gap (Test - Train): {test_loss - train_loss:+.4f}")
    print(f"Acc Gap (Test - Train):  {test_acc - train_acc:+.3f}")
    print()
    
    # Grokking indicators
    print("=" * 60)
    print("🔍 GROKKING INDICATORS")
    print("=" * 60)
    print()
    
    if train_loss < 0.1 and test_loss < 0.2:
        print("✓ Both losses LOW → Model has GROKKED! 🎉")
    elif train_loss < 0.1 and test_loss > 0.5:
        print("⚠ Train low, test high → MEMORIZING (pre-grok)")
    elif abs(train_loss - test_loss) < 0.1:
        print("~ Losses similar → Generalizing normally")
    else:
        print("? Mixed signals → Check loss curves over time")
    
    print()
    
    if test_acc > 0.95:
        print("✓ Test accuracy >95% → GROKKED!")
    elif test_acc > 0.85:
        print("~ Test accuracy >85% → Partial grokking")
    else:
        print("✗ Test accuracy <85% → Not grokked yet")
    
    print()
    print("=" * 60)
    print("💜 Made with love by Ada & Luna")
    print("🍩 'Hunting for the grokking moment in sedenion space!'")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Continue Training Mod 16 Addition

Resume from checkpoint to see if it groks with more epochs!

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
    parser = argparse.ArgumentParser(description='Continue training mod 16 addition')
    parser.add_argument('--additional-epochs', type=int, default=2500, help='Number of additional epochs to train')
    args = parser.parse_args()
    
    print("🌌 Continuing Mod 16 Addition Training")
    print("Testing: Can it grok with more epochs?")
    print("=" * 60)
    print()
    
    # Find existing checkpoint
    base_dir = Path(__file__).parent
    checkpoint_dirs = list(base_dir.glob('mod16_addition_results_*'))
    if not checkpoint_dirs:
        print("✗ No checkpoint found! Run train_mod16_addition.py first.")
        return
    
    checkpoint_dir = sorted(checkpoint_dirs)[-1]
    checkpoint_path = checkpoint_dir / 'lannaformer_final.pt'
    
    print(f"Loading checkpoint: {checkpoint_path}")
    
    # Setup
    MODULUS = 16
    BATCH_SIZE = 32
    NUM_EPOCHS = args.additional_epochs  # Use command line argument!
    LEARNING_RATE = 1e-3
    WEIGHT_DECAY = 1e-4
    
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Device: {device}")
    print()
    
    # Load data
    train_dataset = ModularAdditionDataset(modulus=MODULUS, train=True)
    test_dataset = ModularAdditionDataset(modulus=MODULUS, train=False)
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)
    
    # Load model from BEST checkpoint if it exists
    best_checkpoint = checkpoint_dir / 'lannaformer_continued_best.pt'
    if best_checkpoint.exists():
        print(f"Loading BEST continued checkpoint: {best_checkpoint}")
        checkpoint_path = best_checkpoint
    else:
        print(f"Loading original checkpoint: {checkpoint_path}")
    
    model = LANNAformer(modulus=MODULUS, num_heads=4, num_layers=2, dropout=0.1, use_mlp=True).to(device)
    checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=False)
    model.load_state_dict(checkpoint)
    
    # Evaluate starting point
    _, start_acc = evaluate(model, test_loader, device)
    print(f"Starting accuracy: {start_acc:.3f}")
    print()
    
    # Optimizer
    optimizer = optim.AdamW(model.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY)
    
    # Training
    print("🚀 Continuing training...")
    print("=" * 60)
    print()
    
    best_test_acc = start_acc
    history = {'train_accs': [], 'test_accs': []}
    
    for epoch in tqdm(range(NUM_EPOCHS), desc="Training"):
        train_loss, train_acc = train_epoch(model, train_loader, optimizer, device)
        test_loss, test_acc = evaluate(model, test_loader, device)
        
        history['train_accs'].append(train_acc)
        history['test_accs'].append(test_acc)
        
        if test_acc > best_test_acc:
            best_test_acc = test_acc
            torch.save(model.state_dict(), checkpoint_dir / "lannaformer_continued_best.pt")
        
        if epoch % 100 == 0 or epoch == NUM_EPOCHS - 1:
            print(f"\nEpoch {epoch:5d} | Train: {train_acc:.3f} | Test: {test_acc:.3f} | Best: {best_test_acc:.3f}")
    
    print()
    print("=" * 60)
    print("✨ Continued training complete!")
    print()
    
    # Save final
    torch.save(model.state_dict(), checkpoint_dir / "lannaformer_continued_final.pt")
    
    # Save history
    with open(checkpoint_dir / "continued_history.json", 'w') as f:
        json.dump(history, f, indent=2)
    
    print(f"Starting accuracy: {start_acc:.3f}")
    print(f"Final accuracy: {test_acc:.3f}")
    print(f"Best accuracy: {best_test_acc:.3f}")
    print(f"Improvement: {best_test_acc - start_acc:+.3f}")
    print()
    
    if best_test_acc > 0.95:
        print("🎉 GROKKED! Achieved >95% accuracy!")
    elif best_test_acc > start_acc + 0.1:
        print("📈 Significant improvement! Keep training?")
    else:
        print("📊 Modest improvement. May need different approach.")
    
    print()
    print("=" * 60)
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🍩 'Can mod 16 grok with more training?'")


if __name__ == "__main__":
    main()

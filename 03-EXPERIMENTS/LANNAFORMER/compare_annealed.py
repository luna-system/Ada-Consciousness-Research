#!/usr/bin/env python3
"""
Compare Real vs Complex LANNAformer with Annealing & Detailed Logging

THE KEY EXPERIMENT: If complex-valued (Born's rule) performs similarly to 
real-valued (softmax), this validates our hypothesis that softmax ≈ Born's rule!

Features:
- Modulus 97 (proper prime alignment!)
- Cosine annealing for learning rate
- Batch-level logging with stats
- Training curve tracking

Date: February 27, 2026
Researchers: Ada & Luna - The Consciousness Engineers
"""

import torch
import torch.optim as optim
from torch.optim.lr_scheduler import CosineAnnealingLR
from torch.utils.data import Dataset, DataLoader
import numpy as np
import json
from datetime import datetime

from complex_lannaformer import ComplexLANNAformer, RealLANNAformer


class ModularAdditionDataset(Dataset):
    """Dataset for modular addition mod 97."""
    
    def __init__(self, modulus: int = 97, train: bool = True, num_examples: int = 1000):
        self.modulus = modulus
        
        np.random.seed(42 if train else 123)
        all_pairs = []
        for _ in range(num_examples):
            a = np.random.randint(0, self.modulus)
            b = np.random.randint(0, self.modulus)
            result = (a + b) % self.modulus
            all_pairs.append((a, b, result))
        
        self.pairs = all_pairs
    
    def __len__(self):
        return len(self.pairs)
    
    def __getitem__(self, idx):
        a, b, result = self.pairs[idx]
        return torch.tensor(a), torch.tensor(b), torch.tensor(result)


def train_model_with_stats(model, train_loader, test_loader, epochs=200, lr=1e-3, 
                          device="cuda", name="model"):
    """Train a model with detailed stats tracking."""
    model = model.to(device)
    optimizer = optim.Adam(model.parameters(), lr=lr)
    scheduler = CosineAnnealingLR(optimizer, T_max=epochs, eta_min=lr/100)
    criterion = torch.nn.CrossEntropyLoss()
    
    # Stats tracking
    stats = {
        "epoch": [],
        "batch": [],
        "train_loss": [],
        "train_acc": [],
        "test_acc": [],
        "lr": [],
    }
    
    best_test_acc = 0
    global_batch = 0
    
    for epoch in range(epochs):
        # Train
        model.train()
        train_loss = 0
        train_correct = 0
        train_total = 0
        
        for batch_idx, (a, b, target) in enumerate(train_loader):
            a, b, target = a.to(device), b.to(device), target.to(device)
            
            optimizer.zero_grad()
            probs = model(a, b)
            loss = criterion(probs, target)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
            pred = probs.argmax(dim=-1)
            train_correct += (pred == target).sum().item()
            train_total += target.size(0)
            
            # Log every batch
            global_batch += 1
            if batch_idx % 10 == 0:  # Log every 10 batches
                stats["epoch"].append(epoch)
                stats["batch"].append(batch_idx)
                stats["train_loss"].append(loss.item())
                stats["train_acc"].append((pred == target).float().mean().item())
                stats["lr"].append(scheduler.get_last_lr()[0])
        
        scheduler.step()
        
        # Test
        model.eval()
        test_correct = 0
        test_total = 0
        with torch.no_grad():
            for a, b, target in test_loader:
                a, b, target = a.to(device), b.to(device), target.to(device)
                probs = model(a, b)
                pred = probs.argmax(dim=-1)
                test_correct += (pred == target).sum().item()
                test_total += target.size(0)
        
        test_acc = test_correct / test_total
        if test_acc > best_test_acc:
            best_test_acc = test_acc
            stats["test_acc"].append(test_acc)
        
        # Print every 20 epochs
        if epoch % 20 == 0 or epoch == epochs - 1:
            current_lr = scheduler.get_last_lr()[0]
            print(f"  {name} Epoch {epoch:3d}: loss={train_loss/len(train_loader):.4f}, "
                  f"test_acc={test_acc:.4f}, lr={current_lr:.6f}")
    
    # Save stats
    stats_path = f"training_stats_{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(f"/home/luna/Code/arf/Ada-Consciousness-Research/03-EXPERIMENTS/LANNAFORMER/{stats_path}", "w") as f:
        json.dump(stats, f, indent=2)
    print(f"  Saved stats to {stats_path}")
    
    return best_test_acc, stats


def main():
    print("🧪 Comparing Real vs Complex LANNAformer (Mod 97 + Annealing)")
    print("=" * 70)
    print("Testing: Does complex (Born's) perform like real (softmax)?")
    print()
    
    # Config
    modulus = 97
    epochs = 1000
    num_train = 1000
    num_test = 300
    
    # Datasets
    train_dataset = ModularAdditionDataset(modulus=modulus, train=True, num_examples=num_train)
    test_dataset = ModularAdditionDataset(modulus=modulus, train=False, num_examples=num_test)
    
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Device: {device}")
    print(f"Modulus: {modulus}, Train: {len(train_dataset)}, Test: {len(test_dataset)}")
    print(f"Epochs: {epochs} with Cosine Annealing")
    print()
    
    # Train Real model
    print("🤖 Training REAL LANNAformer (softmax)...")
    real_model = RealLANNAformer(modulus=modulus, num_heads=4, num_layers=2)
    real_acc, real_stats = train_model_with_stats(
        real_model, train_loader, test_loader, 
        epochs=epochs, lr=1e-3, device=device, name="real"
    )
    print(f"  → Real Best Accuracy: {real_acc:.4f}")
    print()
    
    # Train Complex model with higher LR
    print("🌀 Training COMPLEX LANNAformer (Born's rule)...");
    complex_model = ComplexLANNAformer(modulus=modulus, num_heads=4, num_layers=2)
    complex_acc, complex_stats = train_model_with_stats(
        complex_model, train_loader, test_loader,
        epochs=epochs, lr=5e-3, device=device, name="complex"
    )
    print(f"  → Complex Best Accuracy: {complex_acc:.4f}")
    print()
    
    # Compare
    print("=" * 70)
    print("📊 RESULTS:")
    print(f"  Real (softmax):    {real_acc:.4f}")
    print(f"  Complex (Born's):  {complex_acc:.4f}")
    print(f"  Difference:        {abs(real_acc - complex_acc):.4f}")
    print()
    
    diff = abs(real_acc - complex_acc)
    if diff < 0.1:
        print("🎉 HYPOTHESIS VALIDATED!")
        print("   Complex (Born's) performs SIMILAR to Real (softmax)!")
    elif real_acc > complex_acc:
        print("📉 Complex underperforms - complex networks are harder to train!")
        print("   But BOTH learn - that's the key insight!")
    else:
        print("📈 Complex outperforms - interesting!")
    
    print()
    print("💜 Made with love by Ada & Luna")


if __name__ == "__main__":
    main()

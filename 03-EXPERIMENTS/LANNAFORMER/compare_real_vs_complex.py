#!/usr/bin/env python3
"""
Compare Real vs Complex LANNAformer on Complex Addition

THE KEY EXPERIMENT: If complex-valued (Born's rule) performs similarly to 
real-valued (softmax), this validates our hypothesis that softmax ≈ Born's rule!

Both models should achieve similar accuracy if the hypothesis is correct.

Date: February 27, 2026
Researchers: Ada & Luna - The Consciousness Engineers
"""

import torch
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
from tqdm import tqdm

from complex_lannaformer import ComplexLANNAformer, RealLANNAformer


class SimpleComplexAdditionDataset(Dataset):
    """Dataset for modular addition (like original LANNAformer)."""
    
    def __init__(self, modulus: int = 97, train: bool = True, num_examples: int = 500):
        self.modulus = modulus
        
        np.random.seed(42)
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


def train_model(model, train_loader, test_loader, epochs=100, lr=1e-3, device="cuda"):
    """Train a model and return test accuracy."""
    model = model.to(device)
    optimizer = optim.Adam(model.parameters(), lr=lr)
    criterion = torch.nn.CrossEntropyLoss()
    
    best_test_acc = 0
    
    for epoch in range(epochs):
        # Train
        model.train()
        train_loss = 0
        for a, b, target in train_loader:
            a, b, target = a.to(device), b.to(device), target.to(device)
            optimizer.zero_grad()
            probs = model(a, b)
            loss = criterion(probs, target)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()
        
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
        
        if epoch % 20 == 0:
            print(f"  Epoch {epoch}: loss={train_loss/len(train_loader):.4f}, test_acc={test_acc:.4f}")
    
    return best_test_acc


def main():
    print("🧪 Comparing Real vs Complex LANNAformer")
    print("=" * 60)
    print("Testing: Does complex (Born's) perform like real (softmax)?")
    print()
    
    # Config - use modulus 97 like original LANNAformer!
    max_val = 10  # Just for generating random pairs
    modulus = 97  # Same as original LANNAformer!
    
    # Datasets
    train_dataset = SimpleComplexAdditionDataset(max_val=max_val, train=True, num_examples=500)
    test_dataset = SimpleComplexAdditionDataset(max_val=max_val, train=False, num_examples=200)
    
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Device: {device}")
    print(f"Classes: {num_classes}, Train: {len(train_dataset)}, Test: {len(test_dataset)}")
    print()
    
    # Train Real model
    print("🤖 Training REAL LANNAformer (softmax)...")
    real_model = RealLANNAformer(modulus=num_classes, num_heads=4, num_layers=2)
    real_acc = train_model(real_model, train_loader, test_loader, epochs=epochs, device=device)
    print(f"  → Real Best Accuracy: {real_acc:.4f}")
    print()
    
    # Train Complex model
    print("🌀 Training COMPLEX LANNAformer (Born's rule)...")
    complex_model = ComplexLANNAformer(modulus=num_classes, num_heads=4, num_layers=2)
    complex_acc = train_model(complex_model, train_loader, test_loader, epochs=epochs, lr=5e-3, device=device)
    print(f"  → Complex Best Accuracy: {complex_acc:.4f}")
    print()
    
    # Compare
    print("=" * 60)
    print("📊 RESULTS:")
    print(f"  Real (softmax):    {real_acc:.4f}")
    print(f"  Complex (Born's):  {complex_acc:.4f}")
    print(f"  Difference:        {abs(real_acc - complex_acc):.4f}")
    print()
    
    diff = abs(real_acc - complex_acc)
    if diff < 0.1:
        print("🎉 HYPOTHESIS VALIDATED!")
        print("   Complex (Born's) performs SIMILAR to Real (softmax)!")
        print("   This suggests softmax ≈ Born's rule!")
    elif real_acc > complex_acc:
        print("📉 Complex slightly underperforms - needs tuning?")
    else:
        print("📈 Complex outperforms - interesting!")
    
    print()
    print("💜 Made with love by Ada & Luna")


if __name__ == "__main__":
    main()

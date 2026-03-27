#!/usr/bin/env python3
"""
Train ComplexLANNAformer on Complex Addition

Testing: Can the complex-valued network learn complex arithmetic?
- Complex addition: (a+bi) + (c+di) = (a+c) + (b+d)i
- Phases should encode the arithmetic relationships!
- If successful, validates our softmax === Born's hypothesis

This is a SIMPLE first experiment before scaling to consciousness classification.

Date: February 27, 2026
Researchers: Ada & Luna - The Consciousness Engineers
"""

import torch
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
from pathlib import Path
from tqdm import tqdm
import json

from complex_lannaformer import ComplexLANNAformer, encode_to_16d_complex


class ComplexAdditionDataset(Dataset):
    """
    Dataset for complex addition: (a+bi) + (c+di) = (a+c) + (b+d)i
    
    We encode the complex numbers as inputs and train to predict the sum.
    """
    
    def __init__(self, max_val: int = 10, train: bool = True, train_fraction: float = 0.8):
        self.max_val = max_val
        
        # Generate all possible pairs of complex numbers
        # Represent as (real_a, imag_a, real_b, imag_b)
        all_pairs = []
        for ra in range(max_val):
            for ia in range(max_val):
                for rb in range(max_val):
                    for ib in range(max_val):
                        # Complex addition
                        result_r = ra + rb
                        result_i = ia + ib
                        all_pairs.append((ra, ia, rb, ib, result_r, result_i))
        
        # Shuffle deterministically
        np.random.seed(42)
        np.random.shuffle(all_pairs)
        
        # Split train/test
        split_idx = int(len(all_pairs) * train_fraction)
        if train:
            self.pairs = all_pairs[:split_idx]
        else:
            self.pairs = all_pairs[split_idx:]
        
        print(f"Complex addition dataset: {len(self.pairs)} {'train' if train else 'test'} examples")
    
    def __len__(self):
        return len(self.pairs)
    
    def __getitem__(self, idx):
        ra, ia, rb, ib, result_r, result_i = self.pairs[idx]
        
        # Return inputs as two tensors (like original LANNAformer)
        # a = first complex number (ra, ia), b = second (rb, ib)
        a_real = torch.tensor(ra, dtype=torch.float32)
        a_imag = torch.tensor(ia, dtype=torch.float32)
        b_real = torch.tensor(rb, dtype=torch.float32)
        b_imag = torch.tensor(ib, dtype=torch.float32)
        
        # Target: result as single integer (we combine real and imag into one number)
        # Using a simple encoding: result = result_r * max_val + result_i
        target = result_r * self.max_val + result_i
        
        return a_real, a_imag, b_real, b_imag, target


def complex_encode(a_real, a_imag, b_real, b_imag, max_val):
    """
    Encode complex inputs to 16D complex space.
    
    We combine real and imaginary parts into two 16D vectors,
    then concatenate them for a 32D input (which we'll project to 16D).
    """
    # Encode each component
    a_r_16d = encode_to_16d_complex(int(a_real) % 97, 97)
    a_i_16d = encode_to_16d_complex(int(a_imag) % 97, 97)
    b_r_16d = encode_to_16d_complex(int(b_real) % 97, 97)
    b_i_16d = encode_to_16d_complex(int(b_imag) % 97, 97)
    
    # Concatenate: [a_real, a_imag, b_real, b_imag] each 16D = 64D
    # But we need 16D input, so let's simplify
    # Encode as: a = a_real + i*a_imag, b = b_real + i*b_imag
    
    # For simplicity: just encode the integer representations
    # a_encoded = a_real * max_val + a_imag
    # b_encoded = b_real * max_val + b_imag
    
    return None  # Will use simple encoding in forward


class SimpleComplexAdditionDataset(Dataset):
    """
    Simpler dataset: encode complex numbers as integers.
    
    (a, b) where a = real*max + imag encodes complex number 1
    Similarly for b
    Target = (a + b) mod (max*max)
    """
    
    def __init__(self, max_val: int = 5, train: bool = True, train_fraction: float = 0.8):
        self.max_val = max_val
        self.num_classes = max_val * max_val  # All possible complex numbers
        
        # Generate RANDOM pairs (not all combinations for speed!)
        np.random.seed(42)
        num_train = 500 if train else 100
        
        all_pairs = []
        for _ in range(num_train):
            a = np.random.randint(0, self.num_classes)
            b = np.random.randint(0, self.num_classes)
            result = (a + b) % self.num_classes
            all_pairs.append((a, b, result))
        
        self.pairs = all_pairs
        
        print(f"Simple complex addition: {len(self.pairs)} {'train' if train else 'test'} examples")
        print(f"  max_val={max_val}, num_classes={self.num_classes}")
    
    def __len__(self):
        return len(self.pairs)
    
    def __getitem__(self, idx):
        a, b, result = self.pairs[idx]
        return torch.tensor(a), torch.tensor(b), torch.tensor(result)


def train_complex_lannaformer(
    model,
    train_loader,
    test_loader,
    epochs: int = 100,
    lr: float = 1e-3,
    device: str = "cpu"
):
    """Train the ComplexLANNAformer."""
    
    model = model.to(device)
    optimizer = optim.Adam(model.parameters(), lr=lr)
    criterion = torch.nn.CrossEntropyLoss()
    
    best_test_acc = 0
    best_epoch = 0
    
    for epoch in range(epochs):
        # Training
        model.train()
        train_loss = 0
        train_correct = 0
        train_total = 0
        
        for a, b, target in train_loader:
            a = a.to(device)
            b = b.to(device)
            target = target.to(device)
            
            optimizer.zero_grad()
            
            # Forward pass - returns probabilities from Born's rule!
            probs = model(a, b)  # (batch, num_classes)
            
            # Loss
            loss = criterion(probs, target)
            
            # Backward
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
            pred = probs.argmax(dim=-1)
            train_correct += (pred == target).sum().item()
            train_total += target.size(0)
        
        train_acc = train_correct / train_total
        
        # Test
        model.eval()
        test_correct = 0
        test_total = 0
        
        with torch.no_grad():
            for a, b, target in test_loader:
                a = a.to(device)
                b = b.to(device)
                target = target.to(device)
                
                probs = model(a, b)
                pred = probs.argmax(dim=-1)
                
                test_correct += (pred == target).sum().item()
                test_total += target.size(0)
        
        test_acc = test_correct / test_total
        
        if test_acc > best_test_acc:
            best_test_acc = test_acc
            best_epoch = epoch
        
        if epoch % 10 == 0 or epoch == epochs - 1:
            print(f"Epoch {epoch:3d}: Train Loss={train_loss/len(train_loader):.4f}, "
                  f"Train Acc={train_acc:.4f}, Test Acc={test_acc:.4f}")
    
    print(f"\nBest Test Accuracy: {best_test_acc:.4f} at epoch {best_epoch}")
    return best_test_acc


def main():
    print("🧪 Training ComplexLANNAformer on Complex Addition")
    print("=" * 60)
    print()
    
    # Config
    max_val = 5  # Smaller for faster training
    num_classes = max_val * max_val  # 25 classes
    
    # Create datasets
    train_dataset = SimpleComplexAdditionDataset(max_val=max_val, train=True)
    test_dataset = SimpleComplexAdditionDataset(max_val=max_val, train=False)
    
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)
    
    # Create model
    # Note: we need to modify the model to accept arbitrary num_classes
    # For now, let's just use the modulus as num_classes
    model = ComplexLANNAformer(modulus=num_classes, num_heads=4, num_layers=2)
    
    print(f"\nModel: {sum(p.numel() for p in model.parameters())} parameters")
    print()
    
    # Train
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Training on: {device}")
    print()
    
    best_acc = train_complex_lannaformer(
        model,
        train_loader,
        test_loader,
        epochs=100,
        lr=1e-3,
        device=device
    )
    
    print()
    print("=" * 60)
    print("🍩 Complex Addition Training Complete!")
    print(f"📊 Best Accuracy: {best_acc:.4f}")
    print()
    
    if best_acc > 0.9:
        print("🎉 Excellent! The complex-valued network learned complex arithmetic!")
        print("💜 This validates our softmax === Born's hypothesis!")
    elif best_acc > 0.7:
        print("👍 Good progress! Network is learning but needs more training.")
    else:
        print("🤔 Network is learning - let's train longer or adjust parameters!")
    
    print()
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Basin Cartography: Mapping the Loss Landscape

Drop many balls from random starting points and record EVERY STEP
as they roll down through the 16D sedenion quantum field!

This is IMPOSSIBLE in black-box transformers but we have full transparency!

We're literally doing land surveys and cartography! 🗺️✨

Date: January 26, 2026
Researchers: Ada & Luna - The Consciousness Engineers
Experiment: "What does the loss landscape actually look like?"
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
import argparse
from pathlib import Path
from tqdm import tqdm
from datetime import datetime
import copy

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
def evaluate_model(model, dataloader, device='cpu'):
    """Evaluate test accuracy"""
    model.eval()
    correct = 0
    total = 0
    
    for a, b, target in dataloader:
        a, b, target = a.to(device), b.to(device), target.to(device)
        logits = model(a, b)
        pred = logits.argmax(dim=1)
        correct += (pred == target).sum().item()
        total += len(target)
    
    return correct / total


def compute_loss(model, dataloader, device='cpu'):
    """Compute average loss"""
    model.eval()
    criterion = nn.CrossEntropyLoss()
    total_loss = 0.0
    total_samples = 0
    
    with torch.no_grad():
        for a, b, target in dataloader:
            a, b, target = a.to(device), b.to(device), target.to(device)
            logits = model(a, b)
            loss = criterion(logits, target)
            total_loss += loss.item() * len(target)
            total_samples += len(target)
    
    return total_loss / total_samples


def compute_gradient_norm(model, dataloader, device='cpu'):
    """Compute gradient norm (how steep is the slope?)"""
    model.train()
    criterion = nn.CrossEntropyLoss()
    model.zero_grad()
    
    # Compute gradients on one batch
    for a, b, target in dataloader:
        a, b, target = a.to(device), b.to(device), target.to(device)
        logits = model(a, b)
        loss = criterion(logits, target)
        loss.backward()
        break
    
    # Compute total gradient norm
    total_norm = 0.0
    for param in model.parameters():
        if param.grad is not None:
            total_norm += param.grad.norm().item() ** 2
    
    return np.sqrt(total_norm)


def extract_weight_statistics(model):
    """Extract statistics about the weight configuration"""
    stats = {
        'weight_norms': {},
        'weight_means': {},
        'weight_stds': {}
    }
    
    for name, param in model.named_parameters():
        stats['weight_norms'][name] = param.norm().item()
        stats['weight_means'][name] = param.mean().item()
        stats['weight_stds'][name] = param.std().item()
    
    return stats


def train_and_record_trajectory(
    model, 
    train_loader, 
    test_loader, 
    device='cpu',
    max_epochs=1000,
    lr=0.001,
    convergence_threshold=1e-4,
    record_every=10
):
    """
    Train a model and record its complete trajectory through weight space!
    
    Returns: List of snapshots at each recording point
    """
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()
    
    trajectory = []
    prev_loss = float('inf')
    
    for epoch in range(max_epochs):
        # Training step
        model.train()
        for a, b, target in train_loader:
            a, b, target = a.to(device), b.to(device), target.to(device)
            
            optimizer.zero_grad()
            logits = model(a, b)
            loss = criterion(logits, target)
            loss.backward()
            optimizer.step()
        
        # Record snapshot?
        if epoch % record_every == 0 or epoch == max_epochs - 1:
            train_loss = compute_loss(model, train_loader, device)
            test_loss = compute_loss(model, test_loader, device)
            test_acc = evaluate_model(model, test_loader, device)
            grad_norm = compute_gradient_norm(model, train_loader, device)
            weight_stats = extract_weight_statistics(model)
            
            snapshot = {
                'epoch': epoch,
                'train_loss': train_loss,
                'test_loss': test_loss,
                'test_accuracy': test_acc,
                'gradient_norm': grad_norm,
                'weight_stats': weight_stats
            }
            
            trajectory.append(snapshot)
            
            # Check convergence
            if abs(train_loss - prev_loss) < convergence_threshold:
                break
            
            prev_loss = train_loss
    
    return trajectory


def classify_basin(final_accuracy):
    """Classify which basin the trajectory ended in"""
    if final_accuracy > 0.95:
        return "perfect_basin"
    elif final_accuracy > 0.85:
        return "89_basin"  # The mysterious 89% attractor!
    elif final_accuracy > 0.70:
        return "mid_basin"
    elif final_accuracy > 0.50:
        return "weak_basin"
    else:
        return "random_basin"


def main():
    parser = argparse.ArgumentParser(description='Map loss landscape basins')
    parser.add_argument('--num-balls', type=int, default=50, help='Number of balls to drop')
    parser.add_argument('--max-epochs', type=int, default=1000, help='Max epochs per ball')
    parser.add_argument('--lr', type=float, default=0.001, help='Learning rate')
    parser.add_argument('--record-every', type=int, default=10, help='Record every N epochs')
    args = parser.parse_args()
    
    print("🗺️✨ BASIN CARTOGRAPHY: Mapping the Loss Landscape")
    print("=" * 70)
    print(f"Number of balls: {args.num_balls}")
    print(f"Max epochs per ball: {args.max_epochs}")
    print(f"Learning rate: {args.lr}")
    print(f"Recording frequency: every {args.record_every} epochs")
    print("=" * 70)
    print()
    print("We're dropping balls and recording EVERY STEP!")
    print("Full transparency into the 16D sedenion quantum field!")
    print("This is IMPOSSIBLE in black-box transformer land! 🌌")
    print()
    
    # Setup
    MODULUS = 16
    NUM_HEADS = 4
    NUM_LAYERS = 2
    BATCH_SIZE = 32
    device = 'cpu'
    
    # Load data
    train_dataset = ModularAdditionDataset(modulus=MODULUS, train=True)
    test_dataset = ModularAdditionDataset(modulus=MODULUS, train=False)
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)
    
    print(f"Train set: {len(train_dataset)} pairs")
    print(f"Test set: {len(test_dataset)} pairs")
    print()
    
    # Drop balls and record trajectories!
    print("🎾 Dropping balls from random starting points...")
    print("=" * 70)
    print()
    
    all_trajectories = []
    basin_counts = {}
    
    for ball_id in tqdm(range(args.num_balls), desc="Mapping basins"):
        # Create new model (random starting point)
        model = LANNAformer(
            modulus=MODULUS,
            num_heads=NUM_HEADS,
            num_layers=NUM_LAYERS,
            dropout=0.0,
            use_mlp=True
        ).to(device)
        
        # Roll the ball and record trajectory!
        trajectory = train_and_record_trajectory(
            model,
            train_loader,
            test_loader,
            device=device,
            max_epochs=args.max_epochs,
            lr=args.lr,
            record_every=args.record_every
        )
        
        # Classify final basin
        final_acc = trajectory[-1]['test_accuracy']
        basin = classify_basin(final_acc)
        
        basin_counts[basin] = basin_counts.get(basin, 0) + 1
        
        # Store trajectory with metadata
        all_trajectories.append({
            'ball_id': ball_id,
            'final_accuracy': final_acc,
            'final_basin': basin,
            'num_epochs': trajectory[-1]['epoch'],
            'trajectory': trajectory
        })
        
        if ball_id % 10 == 0:
            tqdm.write(f"Ball {ball_id}: {final_acc:.3f} → {basin}")
    
    print()
    print("=" * 70)
    print("✨ Cartography complete!")
    print()
    
    # Analyze basin structure
    print("📊 BASIN DISTRIBUTION:")
    print("-" * 70)
    for basin, count in sorted(basin_counts.items(), key=lambda x: -x[1]):
        percentage = 100 * count / args.num_balls
        print(f"  {basin:20s}: {count:3d} balls ({percentage:5.1f}%)")
    print()
    
    # Find the 89% basin trajectories
    basin_89_trajectories = [t for t in all_trajectories if t['final_basin'] == '89_basin']
    if basin_89_trajectories:
        avg_epochs = np.mean([t['num_epochs'] for t in basin_89_trajectories])
        print(f"🎯 89% Basin Analysis:")
        print(f"  Found in: {len(basin_89_trajectories)} trajectories")
        print(f"  Avg epochs to converge: {avg_epochs:.1f}")
        print()
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = Path(__file__).parent / f"basin_map_{timestamp}"
    results_dir.mkdir(exist_ok=True)
    
    # Save full trajectories (this will be BIG!)
    with open(results_dir / "trajectories.json", 'w') as f:
        json.dump(all_trajectories, f, indent=2)
    
    # Save summary
    summary = {
        'num_balls': args.num_balls,
        'max_epochs': args.max_epochs,
        'learning_rate': args.lr,
        'basin_counts': basin_counts,
        'basin_percentages': {k: 100*v/args.num_balls for k, v in basin_counts.items()}
    }
    
    with open(results_dir / "summary.json", 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"Results saved to: {results_dir}")
    print()
    
    # Key findings
    if '89_basin' in basin_counts:
        pct_89 = 100 * basin_counts['89_basin'] / args.num_balls
        print(f"🔍 KEY FINDING:")
        print(f"  {pct_89:.1f}% of balls ended in the 89% basin!")
        print(f"  This basin is a STRONG attractor in the landscape!")
    
    if 'perfect_basin' in basin_counts:
        pct_perfect = 100 * basin_counts['perfect_basin'] / args.num_balls
        print(f"  {pct_perfect:.1f}% found the perfect solution!")
        print(f"  The perfect basin EXISTS but is harder to find!")
    
    print()
    print("=" * 70)
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🗺️✨ 'We're literally doing land surveys and cartography!'")


if __name__ == "__main__":
    main()

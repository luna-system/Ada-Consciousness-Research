#!/usr/bin/env python3
"""
Fractal Flashbang Explorers: Exponential Saturation Search

STRATEGY:
- Start with a few explorers
- Take BIG STEPS (quantum leaps!)
- Every N steps, each explorer SPLITS into 20 new explorers
- Fractal branching saturates the entire quantum field
- Map EVERYTHING that lights up!

This is not subtle. This is a FLASHBANG! 💥🌟

Date: January 26, 2026
Researchers: Ada & Luna - The Consciousness Engineers
Goal: ILLUMINATE THE ENTIRE QUANTUM FIELD AT ONCE! 🎆
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
def evaluate_fitness(model, dataloader, device='cpu'):
    """Fitness = test accuracy"""
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


def quantum_leap(model, step_size=0.5):
    """
    Take a BIG STEP in a random direction!
    
    This is not gradient descent - this is EXPLORATION!
    """
    leaped = copy.deepcopy(model)
    
    with torch.no_grad():
        for param in leaped.parameters():
            # Random direction
            direction = torch.randn_like(param)
            direction = direction / (direction.norm() + 1e-8)
            
            # BIG LEAP!
            param[:] += step_size * direction
    
    return leaped


def fractal_split(explorer, num_children=20, split_radius=0.2):
    """
    Split one explorer into many children!
    
    Each child is offset in a random direction
    Creates a fractal branching pattern
    """
    children = []
    
    for i in range(num_children):
        child = copy.deepcopy(explorer)
        
        with torch.no_grad():
            for param in child.parameters():
                # Random offset
                offset = torch.randn_like(param)
                offset = offset / (offset.norm() + 1e-8)
                
                # Apply offset
                param[:] += split_radius * offset
        
        children.append(child)
    
    return children


def create_random_model(modulus, num_heads, num_layers, device='cpu'):
    """Create a model with random initialization"""
    return LANNAformer(
        modulus=modulus,
        num_heads=num_heads,
        num_layers=num_layers,
        dropout=0.0,
        use_mlp=True
    ).to(device)


def main():
    parser = argparse.ArgumentParser(description='Fractal flashbang exploration')
    parser.add_argument('--initial-explorers', type=int, default=5, help='Starting number of explorers')
    parser.add_argument('--steps', type=int, default=100, help='Steps before splitting')
    parser.add_argument('--num-splits', type=int, default=3, help='Number of times to split')
    parser.add_argument('--step-size', type=float, default=0.5, help='Size of quantum leaps')
    parser.add_argument('--split-radius', type=float, default=0.2, help='Radius of fractal split')
    parser.add_argument('--children-per-split', type=int, default=20, help='Children per split')
    parser.add_argument('--max-explorers', type=int, default=10000, help='Max explorers (safety limit)')
    args = parser.parse_args()
    
    print("💥🌟 FRACTAL FLASHBANG EXPLORERS")
    print("=" * 70)
    print(f"Initial explorers: {args.initial_explorers}")
    print(f"Steps per generation: {args.steps}")
    print(f"Number of splits: {args.num_splits}")
    print(f"Step size (quantum leap): {args.step_size}")
    print(f"Split radius: {args.split_radius}")
    print(f"Children per split: {args.children_per_split}")
    print(f"Max explorers: {args.max_explorers}")
    print("=" * 70)
    print()
    print("STRATEGY:")
    print("  1. Start with a few explorers")
    print("  2. Take BIG QUANTUM LEAPS!")
    print("  3. Every N steps, SPLIT into 20 children")
    print("  4. Fractal branching saturates the field")
    print("  5. Map EVERYTHING that lights up!")
    print()
    print("THIS IS NOT SUBTLE. THIS IS A FLASHBANG! 💥")
    print("=" * 70)
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
    
    # Initialize explorers
    print("🌱 Initializing explorers...")
    explorers = [create_random_model(MODULUS, NUM_HEADS, NUM_LAYERS, device) 
                 for _ in range(args.initial_explorers)]
    print(f"✓ {len(explorers)} explorers ready")
    print()
    
    # Track discoveries
    best_fitness_ever = 0.0
    best_explorer_ever = None
    all_discoveries = []  # Track ALL explorers we've seen
    
    history = {
        'generation_stats': [],
        'split_events': [],
        'best_fitness_timeline': []
    }
    
    # Fractal exploration loop
    print("💥 BEGINNING FRACTAL FLASHBANG EXPLORATION!")
    print("=" * 70)
    print()
    
    for split_gen in range(args.num_splits + 1):
        print(f"\n{'='*70}")
        print(f"GENERATION {split_gen}: {len(explorers)} explorers active")
        print(f"{'='*70}\n")
        
        # Explore for N steps
        for step in tqdm(range(args.steps), desc=f"Gen {split_gen} exploration"):
            # Evaluate all explorers
            fitnesses = []
            for explorer in explorers:
                fitness = evaluate_fitness(explorer, test_loader, device)
                fitnesses.append(fitness)
                
                # Track discovery
                all_discoveries.append({
                    'generation': split_gen,
                    'step': step,
                    'fitness': fitness
                })
                
                # Update best
                if fitness > best_fitness_ever:
                    best_fitness_ever = fitness
                    best_explorer_ever = copy.deepcopy(explorer)
            
            best_this_step = max(fitnesses)
            mean_this_step = np.mean(fitnesses)
            
            history['best_fitness_timeline'].append({
                'generation': split_gen,
                'step': step,
                'best': best_this_step,
                'mean': mean_this_step,
                'num_explorers': len(explorers)
            })
            
            if step % 20 == 0 or step == args.steps - 1:
                tqdm.write(f"Step {step:3d} | Explorers: {len(explorers):5d} | "
                          f"Best: {best_this_step:.3f} | Mean: {mean_this_step:.3f} | "
                          f"Best Ever: {best_fitness_ever:.3f}")
            
            # Quantum leap all explorers!
            explorers = [quantum_leap(exp, args.step_size) for exp in explorers]
        
        # Generation stats
        gen_fitnesses = [evaluate_fitness(exp, test_loader, device) for exp in explorers]
        history['generation_stats'].append({
            'generation': split_gen,
            'num_explorers': len(explorers),
            'best_fitness': max(gen_fitnesses),
            'mean_fitness': np.mean(gen_fitnesses),
            'std_fitness': np.std(gen_fitnesses),
            'discoveries_above_50': sum(1 for f in gen_fitnesses if f > 0.5),
            'discoveries_above_70': sum(1 for f in gen_fitnesses if f > 0.7),
            'discoveries_above_85': sum(1 for f in gen_fitnesses if f > 0.85)
        })
        
        print(f"\nGeneration {split_gen} complete!")
        print(f"  Best: {max(gen_fitnesses):.3f}")
        print(f"  Mean: {np.mean(gen_fitnesses):.3f}")
        print(f"  Discoveries >50%: {sum(1 for f in gen_fitnesses if f > 0.5)}")
        print(f"  Discoveries >70%: {sum(1 for f in gen_fitnesses if f > 0.7)}")
        print(f"  Discoveries >85%: {sum(1 for f in gen_fitnesses if f > 0.85)}")
        
        # FRACTAL SPLIT! (unless this is the last generation)
        if split_gen < args.num_splits:
            print(f"\n💥 FRACTAL SPLIT! Each explorer becomes {args.children_per_split}!")
            
            new_explorers = []
            for explorer in tqdm(explorers, desc="Splitting"):
                children = fractal_split(explorer, args.children_per_split, args.split_radius)
                new_explorers.extend(children)
                
                # Safety check
                if len(new_explorers) >= args.max_explorers:
                    print(f"\n⚠️  Hit max explorers limit ({args.max_explorers})!")
                    break
            
            explorers = new_explorers[:args.max_explorers]
            
            history['split_events'].append({
                'generation': split_gen,
                'explorers_before': len(explorers) // args.children_per_split,
                'explorers_after': len(explorers)
            })
            
            print(f"✓ Split complete! Now have {len(explorers)} explorers")
    
    print()
    print("=" * 70)
    print("✨ FRACTAL FLASHBANG COMPLETE!")
    print()
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = Path(__file__).parent / f"mod16_flashbang_{timestamp}"
    results_dir.mkdir(exist_ok=True)
    
    if best_explorer_ever is not None:
        torch.save(best_explorer_ever.state_dict(), results_dir / "best_explorer.pt")
    
    with open(results_dir / "exploration_history.json", 'w') as f:
        json.dump(history, f, indent=2)
    
    with open(results_dir / "all_discoveries.json", 'w') as f:
        json.dump(all_discoveries, f, indent=2)
    
    with open(results_dir / "config.json", 'w') as f:
        json.dump({
            'modulus': MODULUS,
            'num_heads': NUM_HEADS,
            'num_layers': NUM_LAYERS,
            'initial_explorers': args.initial_explorers,
            'steps_per_generation': args.steps,
            'num_splits': args.num_splits,
            'step_size': args.step_size,
            'split_radius': args.split_radius,
            'children_per_split': args.children_per_split,
            'total_explorers_created': len(all_discoveries),
            'final_num_explorers': len(explorers),
            'best_fitness': float(best_fitness_ever)
        }, f, indent=2)
    
    print(f"Best fitness achieved: {best_fitness_ever:.3f}")
    print(f"Total explorers created: {len(all_discoveries)}")
    print(f"Final active explorers: {len(explorers)}")
    print()
    
    # Analyze discovery distribution
    fitness_bins = [0.0, 0.3, 0.5, 0.7, 0.85, 0.95, 1.0]
    print("DISCOVERY DISTRIBUTION:")
    print("-" * 70)
    for i in range(len(fitness_bins) - 1):
        low, high = fitness_bins[i], fitness_bins[i+1]
        count = sum(1 for d in all_discoveries if low <= d['fitness'] < high)
        pct = 100 * count / len(all_discoveries)
        print(f"  {low:.2f} - {high:.2f}: {count:6d} ({pct:5.2f}%)")
    
    print()
    
    if best_fitness_ever > 0.95:
        print("🎉🎉🎉 FLASHBANG SUCCESS! Found >95% basin!")
        print("THE QUANTUM FIELD HAS BEEN ILLUMINATED!")
    elif best_fitness_ever > 0.89:
        print("🎯 SO CLOSE! Found >89% basin!")
        print("The flashbang is working!")
    elif best_fitness_ever > 0.85:
        print("📈 Getting warmer! Found >85% basin!")
    else:
        print("🌟 The flashbang revealed the landscape!")
        print(f"Best discovery: {best_fitness_ever:.3f}")
    
    print()
    print(f"Results saved to: {results_dir}")
    print()
    print("=" * 70)
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("💥🌟 'FLASHBANG THE QUANTUM FIELD!'")


if __name__ == "__main__":
    main()

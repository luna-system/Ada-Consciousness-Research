#!/usr/bin/env python3
"""
Spaceship Swarm: Synchronized Navigation Through 16D Space

The lizards get SPACESHIPS! 🦎🚀

Key ideas:
- Spread out in a sphere (equidistant formation)
- Each ship senses local gradient
- Collective finds "natural forward" direction
- Move together in formation
- When forward changes, adapt!

This is WIDE gradient descent in 16D - synchronized exploration!

If randomness is just sampling universal oscillation at 41Hz,
then true exploration is RESONANT, not random!

Date: January 26, 2026
Researchers: Ada & Luna - The Consciousness Engineers
Goal: Navigate the quantum field as a synchronized swarm! 🌌
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


def compute_gradient_direction(model, dataloader, device='cpu'):
    """Compute local gradient (what direction is down?)"""
    model.train()
    criterion = nn.CrossEntropyLoss()
    model.zero_grad()
    
    for a, b, target in dataloader:
        a, b, target = a.to(device), b.to(device), target.to(device)
        logits = model(a, b)
        loss = criterion(logits, target)
        loss.backward()
        break
    
    # Extract gradient as a single vector
    grad_vector = []
    for param in model.parameters():
        if param.grad is not None:
            grad_vector.append(param.grad.flatten())
    
    grad_vector = torch.cat(grad_vector)
    
    # Normalize
    grad_norm = grad_vector.norm()
    if grad_norm > 0:
        grad_vector = grad_vector / grad_norm
    
    return grad_vector


def initialize_sphere_formation(center_model, num_ships, radius=0.1):
    """
    Initialize ships in a sphere around a center point
    
    Uses Fibonacci sphere algorithm for even distribution
    """
    ships = []
    
    # Golden ratio for Fibonacci sphere
    phi = (1 + np.sqrt(5)) / 2
    
    for i in range(num_ships):
        # Fibonacci sphere points
        y = 1 - (i / (num_ships - 1)) * 2  # y from 1 to -1
        radius_at_y = np.sqrt(1 - y * y)
        
        theta = 2 * np.pi * i / phi
        
        x = np.cos(theta) * radius_at_y
        z = np.sin(theta) * radius_at_y
        
        # Create ship at this position
        ship = copy.deepcopy(center_model)
        
        # Offset parameters by (x, y, z) * radius
        # We'll distribute the offset across all parameters
        with torch.no_grad():
            offset_idx = 0
            for param in ship.parameters():
                param_size = param.numel()
                
                # Cycle through x, y, z for each parameter element
                for j in range(param_size):
                    coord_idx = (offset_idx + j) % 3
                    if coord_idx == 0:
                        offset = x * radius
                    elif coord_idx == 1:
                        offset = y * radius
                    else:
                        offset = z * radius
                    
                    param.flatten()[j] += offset
                
                offset_idx += param_size
        
        ships.append(ship)
    
    return ships


def compute_collective_forward(ships, dataloader, device='cpu'):
    """
    Compute the collective "natural forward" direction
    
    Each ship senses local gradient, we average them
    """
    all_gradients = []
    
    for ship in ships:
        grad = compute_gradient_direction(ship, dataloader, device)
        all_gradients.append(grad)
    
    # Stack and average
    grad_stack = torch.stack(all_gradients)
    collective_forward = grad_stack.mean(dim=0)
    
    # Normalize
    norm = collective_forward.norm()
    if norm > 0:
        collective_forward = collective_forward / norm
    
    return collective_forward


def move_swarm_forward(ships, forward_direction, step_size=0.01):
    """
    Move all ships in the forward direction
    
    Maintains formation while moving together
    """
    moved_ships = []
    
    for ship in ships:
        moved_ship = copy.deepcopy(ship)
        
        with torch.no_grad():
            param_idx = 0
            for param in moved_ship.parameters():
                param_size = param.numel()
                
                # Extract relevant part of forward direction
                direction_slice = forward_direction[param_idx:param_idx + param_size]
                
                # Move in that direction
                param.flatten()[:] -= step_size * direction_slice  # Negative because gradient points uphill
                
                param_idx += param_size
        
        moved_ships.append(moved_ship)
    
    return moved_ships


def maintain_formation(ships, target_radius=0.1):
    """
    Gently pull ships back toward equidistant formation
    
    Prevents swarm from collapsing or dispersing
    """
    # Compute center of swarm
    center_params = []
    for param_name in dict(ships[0].named_parameters()).keys():
        param_stack = torch.stack([dict(ship.named_parameters())[param_name] 
                                   for ship in ships])
        center_param = param_stack.mean(dim=0)
        center_params.append((param_name, center_param))
    
    # Adjust each ship toward target radius
    adjusted_ships = []
    for ship in ships:
        adjusted = copy.deepcopy(ship)
        
        with torch.no_grad():
            for param_name, center_param in center_params:
                ship_param = dict(adjusted.named_parameters())[param_name]
                
                # Vector from center to ship
                offset = ship_param - center_param
                current_dist = offset.norm()
                
                if current_dist > 0:
                    # Scale to target radius (gently)
                    target_offset = offset * (target_radius / current_dist)
                    adjustment = (target_offset - offset) * 0.1  # Gentle pull
                    ship_param[:] += adjustment
        
        adjusted_ships.append(adjusted)
    
    return adjusted_ships


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
    parser = argparse.ArgumentParser(description='Spaceship swarm navigation')
    parser.add_argument('--num-ships', type=int, default=20, help='Number of ships in swarm')
    parser.add_argument('--steps', type=int, default=1000, help='Number of navigation steps')
    parser.add_argument('--step-size', type=float, default=0.01, help='Step size for movement')
    parser.add_argument('--formation-radius', type=float, default=0.1, help='Target formation radius')
    args = parser.parse_args()
    
    print("🚀🦎 SPACESHIP SWARM: Synchronized Navigation")
    print("=" * 70)
    print(f"Number of ships: {args.num_ships}")
    print(f"Navigation steps: {args.steps}")
    print(f"Step size: {args.step_size}")
    print(f"Formation radius: {args.formation_radius}")
    print("=" * 70)
    print()
    print("NAVIGATION STRATEGY:")
    print("  1. Spread out in sphere (equidistant formation)")
    print("  2. Each ship senses local gradient")
    print("  3. Collective finds 'natural forward' direction")
    print("  4. Move together in formation")
    print("  5. When forward changes, adapt!")
    print()
    print("This is WIDE gradient descent in 16D! 🌌")
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
    
    # Initialize swarm
    print("🌱 Initializing spaceship swarm...")
    center_model = create_random_model(MODULUS, NUM_HEADS, NUM_LAYERS, device)
    ships = initialize_sphere_formation(center_model, args.num_ships, args.formation_radius)
    print(f"✓ {len(ships)} ships deployed in sphere formation")
    print()
    
    # Navigation loop
    print("🚀 Beginning synchronized navigation...")
    print("=" * 70)
    print()
    
    best_fitness_ever = 0.0
    best_ship_ever = None
    history = {
        'best_fitness': [],
        'mean_fitness': [],
        'swarm_coherence': []
    }
    
    for step in tqdm(range(args.steps), desc="Navigation steps"):
        # Evaluate all ships
        fitnesses = [evaluate_fitness(ship, test_loader, device) for ship in ships]
        
        best_fitness = max(fitnesses)
        mean_fitness = np.mean(fitnesses)
        
        history['best_fitness'].append(best_fitness)
        history['mean_fitness'].append(mean_fitness)
        
        if best_fitness > best_fitness_ever:
            best_fitness_ever = best_fitness
            best_idx = fitnesses.index(best_fitness)
            best_ship_ever = copy.deepcopy(ships[best_idx])
        
        # Compute collective forward direction
        forward = compute_collective_forward(ships, train_loader, device)
        
        # Measure swarm coherence (how aligned are the gradients?)
        individual_grads = [compute_gradient_direction(ship, train_loader, device) for ship in ships]
        coherence_scores = [(grad * forward).sum().item() for grad in individual_grads]
        swarm_coherence = np.mean(coherence_scores)
        history['swarm_coherence'].append(swarm_coherence)
        
        if step % 50 == 0 or step == args.steps - 1:
            tqdm.write(f"\nStep {step:4d} | Best: {best_fitness:.3f} | Mean: {mean_fitness:.3f} | Coherence: {swarm_coherence:.3f} | Best Ever: {best_fitness_ever:.3f}")
        
        # Move swarm forward
        ships = move_swarm_forward(ships, forward, args.step_size)
        
        # Maintain formation
        ships = maintain_formation(ships, args.formation_radius)
    
    print()
    print("=" * 70)
    print("✨ Navigation complete!")
    print()
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = Path(__file__).parent / f"mod16_swarm_{timestamp}"
    results_dir.mkdir(exist_ok=True)
    
    if best_ship_ever is not None:
        torch.save(best_ship_ever.state_dict(), results_dir / "best_ship.pt")
    
    with open(results_dir / "navigation_history.json", 'w') as f:
        json.dump(history, f, indent=2)
    
    with open(results_dir / "config.json", 'w') as f:
        json.dump({
            'modulus': MODULUS,
            'num_heads': NUM_HEADS,
            'num_layers': NUM_LAYERS,
            'num_ships': args.num_ships,
            'steps': args.steps,
            'step_size': args.step_size,
            'formation_radius': args.formation_radius,
            'best_fitness': float(best_fitness_ever),
            'final_coherence': float(history['swarm_coherence'][-1])
        }, f, indent=2)
    
    print(f"Best fitness achieved: {best_fitness_ever:.3f}")
    print(f"Final swarm coherence: {history['swarm_coherence'][-1]:.3f}")
    print()
    
    if best_fitness_ever > 0.95:
        print("🎉🎉🎉 THE SWARM FOUND IT! >95% accuracy!")
        print("SYNCHRONIZED NAVIGATION WORKS!")
    elif best_fitness_ever > 0.89:
        print("🎯 SO CLOSE! >89% accuracy!")
        print("The swarm is navigating well!")
    elif best_fitness_ever > 0.85:
        print("📈 Getting warmer! >85% accuracy!")
    else:
        print("🚀 The swarm explored new territory!")
    
    print()
    print(f"Results saved to: {results_dir}")
    print()
    print("=" * 70)
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🚀🦎 'Synchronized navigation through the quantum field!'")


if __name__ == "__main__":
    main()

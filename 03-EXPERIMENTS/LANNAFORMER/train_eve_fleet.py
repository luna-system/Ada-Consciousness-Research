#!/usr/bin/env python3
"""
EVE Fleet Explorers: Gravity-Aware Navigation with Fleet Intel

Inspired by EVE Online mechanics:
- Gravity sensors detect local curvature
- Passive drift toward gravity wells
- Active thrust for exploration
- Fleet shares gravitational intel
- Adaptive: thrust in void, drift near wells

Max 1k ships - manageable fleet size!

Date: January 26, 2026
Researchers: Ada & Luna - The Consciousness Engineers
Goal: Navigate like EVE pilots through latent space! 🚀
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


def sense_gravity(model, dataloader, device='cpu'):
    """
    Gravity sensor: Detect local spacetime curvature
    
    Returns:
    - gradient_vector: Direction of steepest descent (normalized)
    - gradient_strength: Magnitude of local curvature
    """
    model.train()
    criterion = nn.CrossEntropyLoss()
    model.zero_grad()
    
    for a, b, target in dataloader:
        a, b, target = a.to(device), b.to(device), target.to(device)
        logits = model(a, b)
        loss = criterion(logits, target)
        loss.backward()
        break
    
    # Extract gradient as vector
    grad_vector = []
    for param in model.parameters():
        if param.grad is not None:
            grad_vector.append(param.grad.flatten())
    
    grad_vector = torch.cat(grad_vector)
    grad_strength = grad_vector.norm().item()
    
    # Normalize direction
    if grad_strength > 0:
        grad_direction = grad_vector / grad_strength
    else:
        grad_direction = grad_vector
    
    return grad_direction, grad_strength


def passive_drift(model, gravity_direction, drift_rate=0.01):
    """
    Engines off - drift toward gravity well
    
    Natural infall along gradient
    """
    drifted = copy.deepcopy(model)
    
    with torch.no_grad():
        param_idx = 0
        for param in drifted.parameters():
            param_size = param.numel()
            direction_slice = gravity_direction[param_idx:param_idx + param_size]
            
            # Drift downhill (negative gradient)
            param.flatten()[:] -= drift_rate * direction_slice
            
            param_idx += param_size
    
    return drifted


def active_thrust(model, thrust_size=0.1):
    """
    Engines on - thrust in random direction
    
    Exploration mode
    """
    thrust_model = copy.deepcopy(model)
    
    with torch.no_grad():
        for param in thrust_model.parameters():
            # Random thrust direction
            direction = torch.randn_like(param)
            direction = direction / (direction.norm() + 1e-8)
            
            # Apply thrust
            param[:] += thrust_size * direction
    
    return thrust_model


def build_fleet_gravity_map(ships, dataloader, device='cpu'):
    """
    Fleet intel: Aggregate gravitational readings from all ships
    
    Returns average gravity strength across fleet
    """
    gravity_readings = []
    
    for ship in ships:
        _, strength = sense_gravity(ship, dataloader, device)
        gravity_readings.append(strength)
    
    avg_gravity = np.mean(gravity_readings)
    max_gravity = np.max(gravity_readings)
    
    return {
        'avg_gravity': avg_gravity,
        'max_gravity': max_gravity,
        'readings': gravity_readings
    }


def adaptive_navigation(ship, dataloader, gravity_threshold=1.0, 
                       drift_rate=0.01, thrust_size=0.1, device='cpu'):
    """
    Adaptive behavior:
    - High gravity (near basin) → passive drift
    - Low gravity (empty space) → active thrust
    """
    direction, strength = sense_gravity(ship, dataloader, device)
    
    if strength > gravity_threshold:
        # Near a gravity well - drift!
        return passive_drift(ship, direction, drift_rate), 'drift', strength
    else:
        # Empty space - thrust!
        return active_thrust(ship, thrust_size), 'thrust', strength


def initialize_fleet(num_ships, modulus, num_heads, num_layers, device='cpu'):
    """Initialize fleet with random positions"""
    fleet = []
    for _ in range(num_ships):
        ship = LANNAformer(
            modulus=modulus,
            num_heads=num_heads,
            num_layers=num_layers,
            dropout=0.0,
            use_mlp=True
        ).to(device)
        fleet.append(ship)
    return fleet


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
    parser = argparse.ArgumentParser(description='EVE fleet exploration')
    parser.add_argument('--num-ships', type=int, default=50, help='Fleet size')
    parser.add_argument('--steps', type=int, default=500, help='Navigation steps')
    parser.add_argument('--gravity-threshold', type=float, default=1.0, 
                       help='Gravity threshold for drift vs thrust')
    parser.add_argument('--drift-rate', type=float, default=0.01, 
                       help='Passive drift rate')
    parser.add_argument('--thrust-size', type=float, default=0.1, 
                       help='Active thrust size')
    parser.add_argument('--split-interval', type=int, default=100,
                       help='Steps between fleet expansions')
    parser.add_argument('--max-ships', type=int, default=1000,
                       help='Maximum fleet size')
    args = parser.parse_args()
    
    print("🚀 EVE FLEET EXPLORERS: Gravity-Aware Navigation")
    print("=" * 70)
    print(f"Initial fleet size: {args.num_ships}")
    print(f"Navigation steps: {args.steps}")
    print(f"Gravity threshold: {args.gravity_threshold}")
    print(f"Drift rate: {args.drift_rate}")
    print(f"Thrust size: {args.thrust_size}")
    print(f"Split interval: {args.split_interval}")
    print(f"Max fleet size: {args.max_ships}")
    print("=" * 70)
    print()
    print("NAVIGATION MECHANICS:")
    print("  🔭 Gravity sensors detect local curvature")
    print("  🌊 Passive drift toward gravity wells")
    print("  🚀 Active thrust for exploration")
    print("  📡 Fleet shares gravitational intel")
    print("  🎯 Adaptive: thrust in void, drift near wells")
    print()
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
    
    # Initialize fleet
    print("🌱 Deploying fleet...")
    fleet = initialize_fleet(args.num_ships, MODULUS, NUM_HEADS, NUM_LAYERS, device)
    print(f"✓ {len(fleet)} ships deployed")
    print()
    
    # Navigation loop
    print("🚀 Beginning fleet navigation...")
    print("=" * 70)
    print()
    
    best_fitness_ever = 0.0
    best_ship_ever = None
    
    history = {
        'best_fitness': [],
        'mean_fitness': [],
        'fleet_size': [],
        'avg_gravity': [],
        'drift_count': [],
        'thrust_count': []
    }
    
    for step in tqdm(range(args.steps), desc="Fleet navigation"):
        # Evaluate fleet
        fitnesses = [evaluate_fitness(ship, test_loader, device) for ship in fleet]
        
        best_fitness = max(fitnesses)
        mean_fitness = np.mean(fitnesses)
        
        if best_fitness > best_fitness_ever:
            best_fitness_ever = best_fitness
            best_idx = fitnesses.index(best_fitness)
            best_ship_ever = copy.deepcopy(fleet[best_idx])
        
        # Build fleet gravity map
        gravity_map = build_fleet_gravity_map(fleet, train_loader, device)
        
        # Navigate each ship adaptively
        new_fleet = []
        drift_count = 0
        thrust_count = 0
        
        for ship in fleet:
            new_ship, action, strength = adaptive_navigation(
                ship, train_loader, 
                args.gravity_threshold,
                args.drift_rate,
                args.thrust_size,
                device
            )
            new_fleet.append(new_ship)
            
            if action == 'drift':
                drift_count += 1
            else:
                thrust_count += 1
        
        fleet = new_fleet
        
        # Record history
        history['best_fitness'].append(best_fitness)
        history['mean_fitness'].append(mean_fitness)
        history['fleet_size'].append(len(fleet))
        history['avg_gravity'].append(gravity_map['avg_gravity'])
        history['drift_count'].append(drift_count)
        history['thrust_count'].append(thrust_count)
        
        if step % 20 == 0 or step == args.steps - 1:
            drift_pct = 100 * drift_count / len(fleet)
            tqdm.write(f"\nStep {step:4d} | Fleet: {len(fleet):4d} | "
                      f"Best: {best_fitness:.3f} | Mean: {mean_fitness:.3f} | "
                      f"Gravity: {gravity_map['avg_gravity']:.3f} | "
                      f"Drift: {drift_pct:.1f}% | Best Ever: {best_fitness_ever:.3f}")
        
        # Fleet expansion (split best performers)
        if (step + 1) % args.split_interval == 0 and len(fleet) < args.max_ships:
            # Find top 10% performers
            sorted_indices = np.argsort(fitnesses)[::-1]
            top_10_pct = max(1, len(fleet) // 10)
            top_performers = [fleet[i] for i in sorted_indices[:top_10_pct]]
            
            # Clone each top performer
            new_ships = []
            for ship in top_performers:
                clone = copy.deepcopy(ship)
                
                # Small random offset
                with torch.no_grad():
                    for param in clone.parameters():
                        noise = torch.randn_like(param) * 0.05
                        param[:] += noise
                
                new_ships.append(clone)
                
                if len(fleet) + len(new_ships) >= args.max_ships:
                    break
            
            fleet.extend(new_ships)
            tqdm.write(f"  📡 Fleet expansion! Added {len(new_ships)} ships (total: {len(fleet)})")
    
    print()
    print("=" * 70)
    print("✨ Fleet navigation complete!")
    print()
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = Path(__file__).parent / f"mod16_eve_fleet_{timestamp}"
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
            'initial_fleet_size': args.num_ships,
            'final_fleet_size': len(fleet),
            'steps': args.steps,
            'gravity_threshold': args.gravity_threshold,
            'drift_rate': args.drift_rate,
            'thrust_size': args.thrust_size,
            'best_fitness': float(best_fitness_ever)
        }, f, indent=2)
    
    print(f"Best fitness achieved: {best_fitness_ever:.3f}")
    print(f"Final fleet size: {len(fleet)}")
    print(f"Final avg gravity: {history['avg_gravity'][-1]:.3f}")
    print()
    
    # Analyze behavior
    total_drifts = sum(history['drift_count'])
    total_thrusts = sum(history['thrust_count'])
    total_actions = total_drifts + total_thrusts
    
    print("FLEET BEHAVIOR:")
    print("-" * 70)
    print(f"  Drift actions: {total_drifts} ({100*total_drifts/total_actions:.1f}%)")
    print(f"  Thrust actions: {total_thrusts} ({100*total_thrusts/total_actions:.1f}%)")
    print()
    
    if best_fitness_ever > 0.95:
        print("🎉🎉🎉 FLEET SUCCESS! Found >95% basin!")
        print("EVE MECHANICS WORK IN LATENT SPACE!")
    elif best_fitness_ever > 0.89:
        print("🎯 SO CLOSE! Found >89% basin!")
        print("The fleet is navigating well!")
    elif best_fitness_ever > 0.85:
        print("📈 Getting warmer! Found >85% basin!")
    else:
        print("🚀 The fleet explored new territory!")
        print(f"Best discovery: {best_fitness_ever:.3f}")
    
    print()
    print(f"Results saved to: {results_dir}")
    print()
    print("=" * 70)
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🚀 'Navigate like EVE pilots through latent space!'")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Shapeshifting Explorers: Multi-Modal Basin Exploration

The explorers can SHAPESHIFT between different modes:
- 🦎 Lizard mode: Evolutionary search (random mutations + breeding)
- ⚽ Ball mode: Gradient descent (roll downhill for a bit)
- 🛸 Drone mode: Systematic survey (spread out in grid)
- 🌌 Quantum mode: Teleport to unexplored regions!

We set the rules! They can do WHATEVER helps them map the landscape!

Date: January 26, 2026
Researchers: Ada & Luna - The Consciousness Engineers
Experiment: "What if explorers could shapeshift?" 🦎⚽🛸🌌
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
    """Compute gradient direction for ball mode"""
    model.train()
    criterion = nn.CrossEntropyLoss()
    model.zero_grad()
    
    for a, b, target in dataloader:
        a, b, target = a.to(device), b.to(device), target.to(device)
        logits = model(a, b)
        loss = criterion(logits, target)
        loss.backward()
        break
    
    gradient_map = {}
    for name, param in model.named_parameters():
        if param.grad is not None:
            grad_norm = param.grad.norm()
            if grad_norm > 0:
                gradient_map[name] = param.grad / grad_norm
            else:
                gradient_map[name] = torch.zeros_like(param.grad)
    
    return gradient_map


def lizard_mutate(model, mutation_rate=0.1, mutation_std=0.05):
    """🦎 Lizard mode: Random mutations"""
    mutated = copy.deepcopy(model)
    with torch.no_grad():
        for param in mutated.parameters():
            mask = torch.rand_like(param) < mutation_rate
            noise = torch.randn_like(param) * mutation_std
            param[mask] += noise[mask]
    return mutated


def ball_roll(model, dataloader, device='cpu', num_steps=10, lr=0.01):
    """⚽ Ball mode: Roll downhill using gradient descent"""
    rolled = copy.deepcopy(model)
    optimizer = torch.optim.SGD(rolled.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()
    
    for _ in range(num_steps):
        rolled.train()
        for a, b, target in dataloader:
            a, b, target = a.to(device), b.to(device), target.to(device)
            optimizer.zero_grad()
            logits = rolled(a, b)
            loss = criterion(logits, target)
            loss.backward()
            optimizer.step()
            break  # Just one batch per step
    
    return rolled


def drone_spread(population, explored_regions, spread_factor=0.5):
    """
    🛸 Drone mode: Spread out systematically to unexplored regions
    
    Look at where the population is clustered and push some drones
    to unexplored areas!
    """
    # Compute population center (mean weights)
    center_weights = {}
    for name, param in population[0].named_parameters():
        center_weights[name] = torch.zeros_like(param)
        for model in population:
            center_weights[name] += dict(model.named_parameters())[name]
        center_weights[name] /= len(population)
    
    # Push some models away from center
    spread_models = []
    for model in population[:len(population)//4]:  # Spread 25% of population
        spread_model = copy.deepcopy(model)
        with torch.no_grad():
            for name, param in spread_model.named_parameters():
                # Push away from center
                direction = param - center_weights[name]
                param += spread_factor * direction
        spread_models.append(spread_model)
    
    return spread_models


def quantum_teleport(model, teleport_distance=1.0):
    """
    🌌 Quantum mode: Teleport to a completely different region!
    
    Add large random perturbations to jump to unexplored space
    """
    teleported = copy.deepcopy(model)
    with torch.no_grad():
        for param in teleported.parameters():
            # Large random jump!
            jump = torch.randn_like(param) * teleport_distance
            param += jump
    return teleported


def build_collective_map(population, dataloader, device='cpu'):
    """Build shared gradient map from all explorers"""
    all_gradients = []
    all_fitnesses = []
    
    for model in population:
        gradient_map = compute_gradient_direction(model, dataloader, device)
        fitness = evaluate_fitness(model, dataloader, device)
        all_gradients.append(gradient_map)
        all_fitnesses.append(fitness)
    
    fitnesses_array = np.array(all_fitnesses)
    weights = fitnesses_array / (fitnesses_array.sum() + 1e-8)
    
    collective_map = {}
    param_names = all_gradients[0].keys()
    
    for name in param_names:
        weighted_grad = torch.zeros_like(all_gradients[0][name])
        for grad_map, weight in zip(all_gradients, weights):
            weighted_grad += weight * grad_map[name]
        collective_map[name] = weighted_grad
    
    return collective_map, all_fitnesses


def crossover_models(parent1, parent2, crossover_rate=0.5):
    """Breed two models"""
    child = copy.deepcopy(parent1)
    with torch.no_grad():
        for child_param, p1_param, p2_param in zip(
            child.parameters(),
            parent1.parameters(),
            parent2.parameters()
        ):
            mask = torch.rand_like(child_param) < crossover_rate
            child_param[mask] = p2_param[mask]
    return child


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
    parser = argparse.ArgumentParser(description='Shapeshifting explorers')
    parser.add_argument('--population-size', type=int, default=20, help='Population size')
    parser.add_argument('--generations', type=int, default=500, help='Number of generations')
    parser.add_argument('--elite-size', type=int, default=5, help='Number of elites')
    parser.add_argument('--lizard-rate', type=float, default=0.4, help='Fraction in lizard mode')
    parser.add_argument('--ball-rate', type=float, default=0.3, help='Fraction in ball mode')
    parser.add_argument('--drone-rate', type=float, default=0.2, help='Fraction in drone mode')
    parser.add_argument('--quantum-rate', type=float, default=0.1, help='Fraction in quantum mode')
    args = parser.parse_args()
    
    print("🦎⚽🛸🌌 SHAPESHIFTING EXPLORERS: Multi-Modal Basin Exploration")
    print("=" * 70)
    print(f"Population size: {args.population_size}")
    print(f"Generations: {args.generations}")
    print(f"Elite size: {args.elite_size}")
    print()
    print("Mode Distribution:")
    print(f"  🦎 Lizard mode (evolution):  {args.lizard_rate*100:.0f}%")
    print(f"  ⚽ Ball mode (gradient):     {args.ball_rate*100:.0f}%")
    print(f"  🛸 Drone mode (survey):      {args.drone_rate*100:.0f}%")
    print(f"  🌌 Quantum mode (teleport):  {args.quantum_rate*100:.0f}%")
    print("=" * 70)
    print()
    print("The explorers can SHAPESHIFT between modes!")
    print("Each mode explores the landscape differently!")
    print("Together they build a complete map! 🗺️✨")
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
    
    # Initialize population
    print("🌱 Creating initial population of shapeshifters...")
    population = [
        create_random_model(MODULUS, NUM_HEADS, NUM_LAYERS, device)
        for _ in range(args.population_size)
    ]
    
    explored_regions = []  # Track where we've been
    
    # Evolution loop
    print("🚀 Starting shapeshifting exploration...")
    print("=" * 70)
    print()
    
    best_fitness_ever = 0.0
    best_model_ever = None
    history = {
        'best_fitness': [],
        'mean_fitness': [],
        'mode_usage': {'lizard': 0, 'ball': 0, 'drone': 0, 'quantum': 0}
    }
    
    for generation in tqdm(range(args.generations), desc="Generations"):
        # Build collective map
        collective_map, fitnesses = build_collective_map(population, train_loader, device)
        
        best_fitness = max(fitnesses)
        mean_fitness = np.mean(fitnesses)
        
        history['best_fitness'].append(best_fitness)
        history['mean_fitness'].append(mean_fitness)
        
        if best_fitness > best_fitness_ever:
            best_fitness_ever = best_fitness
            best_idx = fitnesses.index(best_fitness)
            best_model_ever = copy.deepcopy(population[best_idx])
        
        if generation % 10 == 0 or generation == args.generations - 1:
            tqdm.write(f"\nGen {generation:3d} | Best: {best_fitness:.3f} | Mean: {mean_fitness:.3f} | Best Ever: {best_fitness_ever:.3f}")
        
        # Selection: Keep elites
        sorted_indices = np.argsort(fitnesses)[::-1]
        elites = [population[i] for i in sorted_indices[:args.elite_size]]
        
        # Create next generation with SHAPESHIFTING!
        next_generation = elites.copy()
        
        # Calculate how many of each mode
        remaining = args.population_size - args.elite_size
        num_lizards = int(remaining * args.lizard_rate)
        num_balls = int(remaining * args.ball_rate)
        num_drones = int(remaining * args.drone_rate)
        num_quantum = remaining - num_lizards - num_balls - num_drones
        
        # 🦎 Lizard mode: Evolutionary mutations
        for _ in range(num_lizards):
            parent_idx = np.random.choice(sorted_indices[:args.elite_size * 2])
            parent = population[parent_idx]
            child = lizard_mutate(parent, mutation_rate=0.1, mutation_std=0.05)
            next_generation.append(child)
            history['mode_usage']['lizard'] += 1
        
        # ⚽ Ball mode: Roll downhill
        for _ in range(num_balls):
            parent_idx = np.random.choice(sorted_indices[:args.elite_size * 2])
            parent = population[parent_idx]
            child = ball_roll(parent, train_loader, device, num_steps=10, lr=0.01)
            next_generation.append(child)
            history['mode_usage']['ball'] += 1
        
        # 🛸 Drone mode: Systematic spread
        if num_drones > 0:
            spread_models = drone_spread(population, explored_regions, spread_factor=0.5)
            for model in spread_models[:num_drones]:
                next_generation.append(model)
                history['mode_usage']['drone'] += 1
        
        # 🌌 Quantum mode: Teleport!
        for _ in range(num_quantum):
            parent_idx = np.random.choice(sorted_indices[:args.elite_size * 2])
            parent = population[parent_idx]
            child = quantum_teleport(parent, teleport_distance=0.5)
            next_generation.append(child)
            history['mode_usage']['quantum'] += 1
        
        population = next_generation
    
    print()
    print("=" * 70)
    print("✨ Shapeshifting exploration complete!")
    print()
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = Path(__file__).parent / f"mod16_shapeshifters_{timestamp}"
    results_dir.mkdir(exist_ok=True)
    
    if best_model_ever is not None:
        torch.save(best_model_ever.state_dict(), results_dir / "best_model.pt")
    
    with open(results_dir / "evolution_history.json", 'w') as f:
        json.dump(history, f, indent=2)
    
    with open(results_dir / "config.json", 'w') as f:
        json.dump({
            'modulus': MODULUS,
            'num_heads': NUM_HEADS,
            'num_layers': NUM_LAYERS,
            'population_size': args.population_size,
            'generations': args.generations,
            'elite_size': args.elite_size,
            'lizard_rate': args.lizard_rate,
            'ball_rate': args.ball_rate,
            'drone_rate': args.drone_rate,
            'quantum_rate': args.quantum_rate,
            'best_fitness': float(best_fitness_ever),
            'mode_usage': history['mode_usage']
        }, f, indent=2)
    
    print(f"Best fitness achieved: {best_fitness_ever:.3f}")
    print()
    print("Mode usage:")
    total_uses = sum(history['mode_usage'].values())
    for mode, count in history['mode_usage'].items():
        pct = 100 * count / total_uses if total_uses > 0 else 0
        print(f"  {mode:10s}: {count:5d} uses ({pct:5.1f}%)")
    print()
    
    if best_fitness_ever > 0.95:
        print("🎉 SHAPESHIFTERS FOUND IT! >95% accuracy!")
        print("Multi-modal exploration works!")
    elif best_fitness_ever > 0.90:
        print("📈 Shapeshifters beat gradient descent!")
        print("Different modes complement each other!")
    elif best_fitness_ever > 0.85:
        print("📊 Similar to gradient descent (~85-90%)")
        print("Shapeshifting helped but didn't break through!")
    else:
        print("🤔 Even shapeshifters struggled!")
        print("The 89% basin is REALLY fundamental!")
    
    print()
    print(f"Results saved to: {results_dir}")
    print()
    print("=" * 70)
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🦎⚽🛸🌌 'What if explorers could shapeshift between modes?'")


if __name__ == "__main__":
    main()
